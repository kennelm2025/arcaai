"""D2.2a minimal scenario runner — COMMISSIONING (CL-27).

Spec in, corpus queried at a pinned snapshot, result JSON out. That is the
whole remit, ruled at the D2.2a gate on 2026-08-13 as "runner construction
from nothing, minimal". Anything beyond those three things is out of scope
for this increment and belongs to a later one; the temptation to grow a
results ledger, a regime switch or a scoring-class path here is the reason
the scope was restated in the ruling rather than left implied.

**Regime.** Every run emits ``regime: COMMISSIONING`` and an
inadmissibility line into its own result artefact. Results produced by this
runner are permanently inadmissible as gate evidence (D2.0 frame). The
scenario's own acceptance threshold is deliberately NOT evaluated into a
pass/fail verdict: under the commissioning frame a scenario's pass/fail is
not an exit criterion, and emitting a verdict anyway is how commissioning
output gets promoted by osmosis. The threshold is carried through to the
result so the same spec runs unchanged under Regime 2, and the metric is
computed and recorded — but the comparison is left unmade, marked by
``acceptance.evaluated: false``.

**Refusals are the point.** Three of the four things this module does are
refusals: an invalid spec, a diverged pin, or an unusable index all stop the
run with a non-zero exit and a message naming what failed. A runner that
degrades to a partial run on bad input produces a result artefact that
describes something other than what it claims to, which is worse than no
artefact. Exit codes are distinct per refusal class so a caller can tell
them apart without parsing prose.

**Pins are recomputed, never trusted.** The spec carries the corpus snapshot
pins, but they are copies. Every run recomputes the manifest hashes from the
live manifest (DEC-0014 machinery) and compares. A spec whose pins have gone
stale against the manifest is refused rather than run, because a result
recording the spec's own claim about the corpus would be reproducible only
in the sense that it repeats the same wrong claim.

**ADR-0009.** This is platform-side machinery: it imports from
``arcaai.platform`` and never from ``verticals``. The manifest path, the
index path and the output directory all arrive as arguments — there is no
vertical-shaped default anywhere in this file, and the collection name is
passed through only if the caller supplies one.

**CF-1/B7-a.** ``chromadb`` is not imported here. The vector store arrives
through ``ChromaStore``, the single permitted adapter.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import signal
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from arcaai.platform.governance.corpus import (
    manifest_sha256,
    parse_manifest,
    retrieval_snapshot_sha256,
)

RUNNER_VERSION = "0.1.0-commissioning"

# Rev C §6.8.1 — THE REPRODUCIBILITY IDENTITY HAS FOUR LEGS: spec hash, model
# version, corpus snapshot, and the EVALUATOR version. Every three-leg
# statement in the TOR or elsewhere is superseded as a floor.
#
# The evaluator is versioned INDEPENDENTLY of the runner, and the separation is
# the whole point of the leg: a runner release that does not touch evaluation
# must not present as an evaluator change, and an evaluator change inside an
# otherwise unchanged runner release must not be able to hide. §9.2 rows 7a/7b
# and 8 give this version its consequences.
#
# The same clause states the RUNNER version is deliberately NOT an identity
# leg, because only evaluator semantics bear on how a result is scored and
# pinning the whole runner would make every unrelated release invalidate the
# identity. So these two constants move independently, and neither is a
# substitute for the other.
EVALUATOR_VERSION = "0.1.0-commissioning"

# Rev C §9.5 element 3 — a NAMED list of material vector-index and embedder
# parameters, carried with its own hash. Named rather than "whatever the store
# happens to report": a list that varies with the store cannot evidence that
# two runs shared an environment, because the thing being compared would move
# with the thing being measured.
#
# SEARCH-TIME PARAMETERS ARE IN, not only index-build ones. DeepSeek's delta
# return said so, and the D2.2a spike's own material-parameter list v0.1 —
# authored the same day, without sight of that return — independently carried
# `hnsw_ef_search` under the search-space-pruning limb. Two readings of the
# same clause reaching the same membership is worth more than either alone.
#
# RECONCILIATION OWED: this list is authored here against §9.5 and the spike
# record's stated membership. It has NOT been diffed field-by-field against the
# spike's list v0.1 artefact, which is preserved in custody outside this tree.
# If the two differ, the spike's is the earlier statement and the difference is
# a finding, not a licence to prefer this one.
MATERIAL_PARAMETER_LIST_VERSION = "0.1"
MATERIAL_PARAMETERS: tuple[str, ...] = (
    "embedding_model",
    "distance_space",
    "hnsw_construction_ef",
    "hnsw_m",
    "hnsw_ef_search",
)

# The value recorded when a named parameter cannot be read. NEVER a documented
# default: a default recorded as though it had been read makes two environments
# that genuinely differ hash identically, which is the single failure an
# environment identity exists to prevent. UNKNOWN is a fact about the runner's
# knowledge and is hashed as such.
UNKNOWN = "UNKNOWN"

SCHEMA_DIR = Path(__file__).resolve().parent / "schema"

# Schema selection is by the spec's OWN declared version, not by a constant.
# Until v0.2 this was a single hardcoded path, which was correct while one
# schema existed and becomes a trap the moment a second does: each schema
# file pins schema_version with a const, so a v0.2 spec checked against the
# v0.1 file is rejected for the wrong reason entirely - the runner would
# report a malformed spec where the truth is a runner that cannot read that
# version. A rejection naming the wrong cause is worse than no rejection,
# because it sends the reader to fix a spec that is correct.
#
# Each schema file stays immutable; a new version is a new file and a new
# entry here, never an edit of an existing one.
#
# DUPLICATION FLAGGED, NOT REFACTORED (2026-08-17, at v0.3). This mapping
# exists twice: here, and again at tests/harness/test_scenario_spec_schema.py
# as _SCHEMA_PATHS. Adding a version means editing both in the same commit;
# editing one is a silent divergence between what the runner validates and
# what the suite believes it validates. Recorded rather than fixed because
# the fix is a shared module and that is a refactor this arc did not rule.
SCHEMA_BY_VERSION = {
    "0.1": SCHEMA_DIR / "scenario_spec_v0.1.schema.json",
    "0.2": SCHEMA_DIR / "scenario_spec_v0.2.schema.json",
    "0.3": SCHEMA_DIR / "scenario_spec_v0.3.schema.json",
}

REGIME = "COMMISSIONING"
INADMISSIBILITY = (
    "Results from this runner are permanently inadmissible as gate evidence "
    "(D2.0 commissioning frame)."
)

# Distinct per refusal class, so a caller distinguishes them without parsing
# prose. 0 is the only success; every refusal is non-zero by construction.
EXIT_OK = 0
EXIT_SPEC_INVALID = 2
EXIT_PIN_DIVERGED = 3
EXIT_INDEX_UNUSABLE = 4
# Rev C §5.4 — a spec whose top_k exceeds its own recorded absolute cap. Its
# own refusal class rather than folded into EXIT_SPEC_INVALID, because the spec
# is schema-VALID: v0.3 records the cap and JSON Schema cannot compare two
# sibling values, so this breach passes validation and is caught only here.
# Reporting it as a malformed spec would send the reader to look for a
# structural fault that does not exist.
EXIT_CAP_BREACH = 5
# Rev C §8.3 — the session was halted mid-run. Partial results are recorded,
# not discarded, and are inadmissible for any purpose but diagnosing the halt.
EXIT_HALTED = 6

# Excluded from the comparable-content hash. The timestamp varies by
# construction, and the hash cannot cover the field that carries it. Nothing
# else is excluded: scores stay raw, because normalising a float to make runs
# agree would manufacture the very reproducibility the hash exists to test.
_HASH_EXCLUDED_KEYS = ("generated_at_utc", "comparable_content_sha256")


class Refusal(Exception):
    """A refusal to run, carrying the exit code for its class."""

    def __init__(self, code: int, message: str, detail: list[str] | None = None):
        super().__init__(message)
        self.code = code
        self.detail = detail or []


class Halted(Exception):
    """The session was stopped mid-run (Rev C §8.3).

    Distinct from ``Refusal`` and the distinction is not cosmetic. A refusal
    happens BEFORE anything ran and produces no artefact, because there is
    nothing to describe. A halt happens DURING a run: work was done, and Rev C
    requires that partial work be recorded rather than discarded, marked
    inadmissible for anything but diagnosing the suspension. Collapsing the two
    would either throw away a partial result or dress a refusal up as one.
    """

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


def _git_commit(repo_hint: Path) -> str:
    """Best-effort HEAD sha for the result's provenance.

    Returns the literal string ``unknown`` when git cannot answer. Recorded
    as ``unknown`` rather than omitted: a provenance field that silently
    disappears when it cannot be determined reads, in the artefact, exactly
    like a field that was never required.
    """
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(repo_hint),
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    sha = out.stdout.strip()
    return sha if out.returncode == 0 and sha else "unknown"


def load_and_validate_spec(spec_path: Path) -> tuple[dict[str, Any], str]:
    """Parse the spec and validate against the schema the spec declares.

    Uses ``Draft202012Validator`` directly — the same validation path
    ``tests/harness/test_scenario_spec_schema.py`` exercises, so the runner
    and the test suite cannot disagree about what a valid spec is.

    Version selection has three outcomes and they stay distinct: a known
    version validates, an absent one refuses saying so, and an unknown one
    refuses naming what it does know. None of the three is allowed to
    present as another — an unreadable version reported as an invalid spec
    is the check-method failure this repository names most often.
    """
    raw = spec_path.read_bytes()
    spec_sha = hashlib.sha256(raw).hexdigest()
    try:
        spec = yaml.safe_load(raw.decode("utf-8"))
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise Refusal(EXIT_SPEC_INVALID, f"spec is not readable YAML: {exc}") from exc
    if not isinstance(spec, dict):
        raise Refusal(EXIT_SPEC_INVALID, "spec root must be a mapping")

    declared = spec.get("schema_version")
    if declared is None:
        raise Refusal(
            EXIT_SPEC_INVALID,
            "spec declares no schema_version, so no schema can be selected to "
            "judge it. Validating against a default would make the runner, "
            "not the spec, decide which rules applied.",
        )
    if declared not in SCHEMA_BY_VERSION:
        raise Refusal(
            EXIT_SPEC_INVALID,
            f"spec declares schema_version {declared!r}, for which this runner "
            f"has no schema. Known versions: "
            f"{', '.join(sorted(SCHEMA_BY_VERSION))}. This is an unreadable "
            f"version, not an invalid spec.",
        )
    schema_path = SCHEMA_BY_VERSION[declared]

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(spec), key=lambda e: str(e.json_path))
    if errors:
        detail: list[str] = []

        def walk(err: Any) -> None:
            detail.append(f"{err.json_path} :: {err.validator} :: {err.message}")
            for sub in err.context or []:
                walk(sub)

        for err in errors:
            walk(err)
        raise Refusal(
            EXIT_SPEC_INVALID,
            f"spec failed schema v{declared} validation with "
            f"{len(errors)} error(s)",
            detail,
        )

    if spec["scenario_class"] != "retrieval":
        raise Refusal(
            EXIT_SPEC_INVALID,
            f"scenario_class {spec['scenario_class']!r} is not implemented by this "
            "minimal runner; only 'retrieval' is in scope for D2.2a",
        )
    return spec, spec_sha


def verify_pins(spec: dict[str, Any], manifest_path: Path) -> dict[str, Any]:
    """Recompute the snapshot identity from the live manifest and compare.

    Returns the verified snapshot block. Raises Refusal naming every pin
    that diverged — all of them, not the first, because a caller correcting
    one at a time learns less than one shown the whole divergence.
    """
    manifest = parse_manifest(manifest_path.read_text(encoding="utf-8"))
    live = {
        "manifest_version": manifest["manifest_version"],
        "manifest_sha256": manifest_sha256(manifest),
        "retrieval_snapshot_sha256": retrieval_snapshot_sha256(manifest),
    }
    pinned = spec["corpus_snapshot"]

    diverged: list[str] = []
    for key in ("manifest_version", "manifest_sha256"):
        if pinned[key] != live[key]:
            diverged.append(f"{key}: spec pins {pinned[key]!r}, live manifest is {live[key]!r}")

    # Optional at v0.1; REQUIRED for retrieval-class at v0.2, where absence
    # is a schema rejection long before this line runs. The branch stays
    # regardless, and not merely for tidiness: v0.1 specs remain valid and
    # runnable, so the unpinned case is live for as long as any of them is.
    # Absence is reported as unpinned rather than passed over, because
    # "not checked" and "checked and matched" must not look alike.
    rss_pinned = "retrieval_snapshot_sha256" in pinned
    if rss_pinned and pinned["retrieval_snapshot_sha256"] != live["retrieval_snapshot_sha256"]:
        diverged.append(
            f"retrieval_snapshot_sha256: spec pins {pinned['retrieval_snapshot_sha256']!r}, "
            f"live manifest is {live['retrieval_snapshot_sha256']!r}"
        )

    if diverged:
        raise Refusal(
            EXIT_PIN_DIVERGED,
            f"{len(diverged)} corpus pin(s) diverged from the live manifest",
            diverged,
        )

    return {
        "manifest_version": live["manifest_version"],
        "manifest_sha256": live["manifest_sha256"],
        "retrieval_snapshot_sha256": (
            live["retrieval_snapshot_sha256"] if rss_pinned else None
        ),
        "retrieval_snapshot_pinned_by_spec": rss_pinned,
        "pins_verified_against_live_manifest": True,
        "manifest_path": str(manifest_path),
    }


def check_top_k_against_cap(spec: dict[str, Any]) -> int | None:
    """Refuse a spec whose ``top_k`` exceeds its own recorded absolute cap.

    Rev C §5.4 requires every scenario to record an absolute cap in the spec.
    v0.3 makes ``top_k_absolute_cap`` a required retrieval-block field, so the
    cap is now recorded structurally — but **JSON Schema cannot compare two
    sibling values**, so a spec whose ``top_k`` exceeds its own cap validates
    cleanly. The comparison has exactly one place it can be made, and this is
    it: at load time, before any retrieval runs.

    Returns the cap when one is recorded, ``None`` when the spec's schema
    version does not carry the field. Absent and satisfied are kept distinct in
    the result artefact for the usual reason — "not checked" and "checked and
    passed" must not look alike.

    Rev C §5.5 additionally makes a corpus expansion that pushes a scenario
    past its recorded cap a RULED VARIANCE before that scenario runs again.
    That is a governance act on the scenario, not a runtime branch, and this
    function deliberately does not try to detect it: the runner can see the
    breach, not whether it was ruled.
    """
    block = spec["retrieval"]
    cap = block.get("top_k_absolute_cap")
    if cap is None:
        return None
    top_k = block["top_k"]
    if top_k > cap:
        raise Refusal(
            EXIT_CAP_BREACH,
            f"top_k {top_k} exceeds this scenario's own recorded "
            f"top_k_absolute_cap {cap} (Rev C §5.4). The spec is schema-valid — "
            "JSON Schema cannot compare sibling values — so this is caught at "
            "load time or not at all. If a corpus expansion moved the scenario "
            "past its cap, §5.5 makes that a ruled variance before the scenario "
            "runs again.",
        )
    return cap


def material_parameter_list_sha256() -> str:
    """Hash of the NAMED LIST, not of its values.

    Rev C §9.5 element 3 requires the list to carry *its own* hash, separately
    from the environment hash over the values. The two answer different
    questions: this one moves when the definition of "material" changes, the
    environment hash moves when the environment does. Collapsing them would
    make a list amendment indistinguishable from an environment drift.
    """
    canonical = json.dumps(
        {
            "list_version": MATERIAL_PARAMETER_LIST_VERSION,
            "parameters": list(MATERIAL_PARAMETERS),
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def read_material_parameters(store: Any, embedding_model: str) -> dict[str, str]:
    """Read each named parameter's live value, or record UNKNOWN.

    Three outcomes per parameter and they stay distinct: a value read from the
    live store; a parameter the adapter does not expose; and a parameter whose
    read raised. The last two both record UNKNOWN, and correctly so — in each
    case the runner does not know the value, and the reason it does not know is
    not a property of the environment.

    **A documented default is never substituted.** Recording a default as
    though it had been read would make two environments that genuinely differ
    hash identically, which is the one failure this identity exists to prevent.

    KNOWN LIMITATION, recorded rather than worked around: the ChromaStore
    adapter exposes the embedding model and the distance space, and does not
    expose the HNSW construction, M or search-ef parameters. Those therefore
    read UNKNOWN on every run today, so the environment identity is HONEST but
    PARTIAL. Widening it means exposing the parameters on the adapter, which is
    a change to ``arcaai/platform/retrieval/`` and outside this increment's
    writable scope; it is raised as a recommendation rather than taken.
    """
    values: dict[str, str] = dict.fromkeys(MATERIAL_PARAMETERS, UNKNOWN)

    # Pinned at the adapter and imported by the caller — the one parameter the
    # runner can state without interrogating the store.
    values["embedding_model"] = embedding_model

    metadata: dict[str, Any] = {}
    for attribute in ("collection_metadata", "metadata"):
        try:
            candidate = getattr(store, attribute, None)
        except Exception:  # noqa: BLE001 - any failure here means UNKNOWN
            candidate = None
        if isinstance(candidate, dict):
            metadata = candidate
            break

    for name in MATERIAL_PARAMETERS:
        if name == "embedding_model":
            continue
        if name in metadata and metadata[name] is not None:
            values[name] = str(metadata[name])

    return values


def environment_config_sha256(values: dict[str, str], list_sha: str) -> str:
    """Hash over the material-parameter VALUES **and** the list's own hash.

    Rev C §8.1 criterion 7 specifies both inputs, and both are load-bearing.
    Over the values alone, adding or removing a parameter from the named list
    would leave the hash unchanged whenever the added parameter happened to be
    absent — a widened definition of "material" that no instrument could see.
    Including the list hash makes a definition change move the environment
    identity, which is the correct behaviour: it is a different environment
    question being asked.
    """
    canonical = json.dumps(
        {"material_parameter_list_sha256": list_sha, "values": values},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def single_chunk_expected_documents(
    manifest: dict[str, Any], expected_ids: list[str]
) -> list[str]:
    """Expected-set members whose corpus chunk count is exactly 1.

    Rev C §12.3: *a result whose expected grounding set includes a single-chunk
    document carries the attribute* ``confound: single_chunk``, validated at
    result admissibility. Rev A required the confound at prose level only, with
    no field and no check, so omission was undetectable — which is precisely
    why this is computed rather than asserted by an author.

    Returns the offending document ids rather than a bare boolean, because a
    reader asked to weigh the confound needs to know WHICH documents carry it.
    A document named in the expected set but absent from the manifest is not
    single-chunk and is not silently treated as such; it simply does not appear
    here, and the retrieval result already records the expected/matched sets.
    """
    by_id = {d["id"]: d for d in manifest.get("documents", [])}
    single: list[str] = []
    for doc_id in expected_ids:
        doc = by_id.get(doc_id)
        if doc is None:
            continue
        if (doc.get("processing") or {}).get("chunk_count") == 1:
            single.append(doc_id)
    return single


def comparable_content_sha256(result: dict[str, Any]) -> str:
    """Hash of the result with the varying fields removed.

    This is the reproducibility instrument: two runs of the same triple must
    produce the same value here. Canonicalised the same way the corpus
    manifest is (sorted keys, fixed separators, UTF-8), so formatting can
    never move the hash.
    """
    body = {k: v for k, v in result.items() if k not in _HASH_EXCLUDED_KEYS}
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def run_scenario(
    spec_path: Path,
    manifest_path: Path,
    index_path: Path,
    out_dir: Path,
    collection_name: str | None = None,
) -> tuple[dict[str, Any], Path]:
    """Execute one retrieval scenario. Returns (result, written path)."""
    spec, spec_sha = load_and_validate_spec(spec_path)
    snapshot = verify_pins(spec, manifest_path)

    # Rev C §5.4 — the sibling comparison the schema cannot make. Checked
    # before the index is touched, so a capped scenario costs nothing to refuse.
    top_k_cap = check_top_k_against_cap(spec)

    # Re-parsed rather than threaded out of verify_pins: that function's remit
    # is the pin comparison, and widening its return type to serve an unrelated
    # caller would couple two checks that should stay independently readable.
    manifest = parse_manifest(manifest_path.read_text(encoding="utf-8"))

    # Imported here, not at module scope: constructing the adapter is a
    # composition-root act, and the import warms an ONNX model. A refusal at
    # spec or pin level must not pay that cost.
    from arcaai.platform.retrieval.chroma_store import EMBEDDING_MODEL, ChromaStore

    if not index_path.exists():
        raise Refusal(EXIT_INDEX_UNUSABLE, f"index path does not exist: {index_path}")

    kwargs: dict[str, Any] = {"persist_directory": str(index_path)}
    if collection_name is not None:
        kwargs["collection_name"] = collection_name
    store = ChromaStore(**kwargs)

    # Rev C §9.5 element 3 and §8.1 criterion 7 — the environment identity.
    # Read from the live store rather than declared, and UNKNOWN wherever the
    # adapter does not expose the parameter.
    material_list_sha = material_parameter_list_sha256()
    material_values = read_material_parameters(store, EMBEDDING_MODEL)
    env_config_sha = environment_config_sha256(material_values, material_list_sha)

    indexed = store.count()
    if indexed == 0:
        raise Refusal(
            EXIT_INDEX_UNUSABLE,
            f"index at {index_path} holds 0 chunks; a scenario cannot be run against "
            "an empty index",
        )

    block = spec["retrieval"]
    top_k = block["top_k"]
    hits = store.query(block["query"], top_k=top_k)

    chunk_ids = [h.chunk.chunk_id for h in hits]
    scores = [h.score for h in hits]
    doc_ids: list[str] = []
    for h in hits:
        if h.chunk.doc_id not in doc_ids:
            doc_ids.append(h.chunk.doc_id)

    expected = list(block.get("expected_document_ids") or [])
    matched = sorted(set(doc_ids) & set(expected))
    recall = (len(matched) / len(expected)) if expected else None

    # Rev C §12.3 — computed from the manifest, never asserted by the author.
    # Rev A required this confound at prose level with no field and no check,
    # so an omission was undetectable; computing it is what makes it real.
    single_chunk_ids = single_chunk_expected_documents(manifest, expected)
    confounds = ["single_chunk"] if single_chunk_ids else []

    result: dict[str, Any] = {
        "regime": REGIME,
        "admissibility": INADMISSIBILITY,
        "runner_version": RUNNER_VERSION,
        # Rev C §6.8.1 — the fourth identity leg. Versioned independently of
        # the runner version directly above it, and neither substitutes for
        # the other.
        "evaluator_version": EVALUATOR_VERSION,
        "runner_commit": _git_commit(manifest_path.parent),
        # Rev C §8.3 — overwritten to "halted", with a reason, if the run is
        # interrupted. A result that never states its session status cannot be
        # filtered out of an evidence set by anything downstream.
        "session_status": "completed",
        # Rev C §9.8 — the D2.5 ledger field, emitted so a ledger row can carry
        # it and gate/pre-flight tooling has something to filter on.
        "invalidation_status": "none_recorded",
        "invalidation_status_note": (
            "No invalidation event has been applied to this result. The D2.5 "
            "ledger is not implemented by this runner and the controlled "
            "vocabulary for this field is D2.5's to rule; 'none_recorded' "
            "states the runner's knowledge, not a ruled ledger state."
        ),
        "scenario_id": spec["scenario_id"],
        "scenario_class": spec["scenario_class"],
        "spec_path": str(spec_path),
        "spec_sha256": spec_sha,
        "schema_version": spec["schema_version"],
        "corpus_snapshot": snapshot,
        "model_version": EMBEDDING_MODEL,
        "index_path": str(index_path),
        "indexed_chunk_count": indexed,
        "retrieval": {
            "retrieval_kind": block["retrieval_kind"],
            "query": block["query"],
            "top_k": top_k,
            # Rev C §5.4. `checked` is separate from the value because absent
            # and satisfied must not look alike: a v0.1/v0.2 spec carries no
            # cap, and "no cap recorded" is a different fact from "cap
            # recorded and honoured".
            "top_k_absolute_cap": top_k_cap,
            "top_k_cap_checked": top_k_cap is not None,
            "scoring_method": block["scoring_method"],
        },
        "retrieved_chunk_ids": chunk_ids,
        "retrieved_document_ids": doc_ids,
        "retrieved_scores": scores,
        "expected_document_ids": expected,
        "matched_document_ids": matched,
        "recall_at_k": recall,
        # Rev C §12.3 — the marker, plus which documents earned it. A reader
        # asked to weigh a confound needs to know which members carry it.
        "confound": confounds,
        "confound_single_chunk_document_ids": single_chunk_ids,
        # Rev C §8.1 criterion 7 and §9.5 element 3 — the environment identity.
        "environment_config_sha256": env_config_sha,
        "material_parameter_list_sha256": material_list_sha,
        "environment": {
            "material_parameter_list_version": MATERIAL_PARAMETER_LIST_VERSION,
            "material_parameters": list(MATERIAL_PARAMETERS),
            "material_parameter_values": material_values,
            # Named explicitly rather than left to be inferred by scanning the
            # values: a partial environment identity that does not announce
            # itself reads exactly like a complete one.
            "unknown_parameters": sorted(
                name for name, value in material_values.items() if value == UNKNOWN
            ),
        },
        "acceptance": {
            "metric": spec["acceptance"]["metric"],
            "operator": spec["acceptance"]["operator"],
            "value": spec["acceptance"]["value"],
            "evaluated": False,
            "note": (
                "Not evaluated: under the D2.0 commissioning frame a scenario's own "
                "pass/fail is not an exit criterion. The metric is recorded; the "
                "comparison is deliberately left unmade."
            ),
        },
        "generated_at_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
    }
    result["comparable_content_sha256"] = comparable_content_sha256(result)

    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = result["generated_at_utc"].replace(":", "").replace("-", "").replace(".", "")
    out_path = out_dir / f"result_{spec['scenario_id']}_{stamp}.json"
    out_path.write_text(
        json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return result, out_path


def write_halt_record(out_dir: Path, spec_path: Path, reason: str) -> Path:
    """Record a halted session instead of discarding it (Rev C §8.3).

    Rev A's §9.3 covered invalidated results and said nothing about a session
    stopped mid-flight, leaving it open whether partial work was kept, marked
    or thrown away. Rev C closes that: partial results are recorded with
    ``session_status: halted`` and the reason, and are **inadmissible for any
    purpose other than diagnosing the suspension**.

    The record deliberately carries no retrieval fields. A halt can occur
    before the store is reached, so a schema promising them would be
    half-empty on most halts — and a field present-but-null reads, to anything
    downstream, like a measurement that came back empty rather than one that
    was never taken.
    """
    record = {
        "regime": REGIME,
        "admissibility": INADMISSIBILITY,
        "runner_version": RUNNER_VERSION,
        "evaluator_version": EVALUATOR_VERSION,
        "spec_path": str(spec_path),
        "session_status": "halted",
        "halt_reason": reason,
        "invalidation_status": "none_recorded",
        "partial_result_admissibility": (
            "Inadmissible for any purpose other than diagnosing the "
            "suspension (Rev C §8.3). Re-entry is a separate session entry "
            "carrying its own pinned reproducibility identity — re-entry is "
            "not resumption, and results either side of it must not be "
            "presented as one continuous set."
        ),
        "generated_at_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = record["generated_at_utc"].replace(":", "").replace("-", "").replace(".", "")
    out_path = out_dir / f"halted_{stamp}.json"
    out_path.write_text(
        json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return out_path


def _install_halt_handlers() -> None:
    """Turn the interrupting signals into a ``Halted`` we can record.

    Best-effort by design: signal handlers can only be installed from the main
    thread, and the platforms differ on which signals exist. A failure to
    install is silently accepted because the alternative — refusing to run at
    all when a halt handler cannot be registered — would trade a recorded halt
    for no run whatsoever.
    """
    def _on_signal(signum: int, _frame: Any) -> None:
        try:
            name = signal.Signals(signum).name
        except ValueError:
            name = str(signum)
        raise Halted(f"{name} received mid-run")

    for candidate in ("SIGINT", "SIGTERM", "SIGBREAK"):
        sig = getattr(signal, candidate, None)
        if sig is None:
            continue
        try:
            signal.signal(sig, _on_signal)
        except (ValueError, OSError, RuntimeError):
            continue


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="D2.2a minimal scenario runner (COMMISSIONING). "
        "Spec in, corpus queried at a pinned snapshot, result JSON out.",
    )
    parser.add_argument("--spec", required=True, type=Path, help="scenario spec YAML")
    parser.add_argument(
        "--manifest",
        required=True,
        type=Path,
        help="corpus MANIFEST.yaml (pins recomputed from it)",
    )
    parser.add_argument(
        "--index", required=True, type=Path, help="persistent vector store directory"
    )
    parser.add_argument(
        "--out-dir", required=True, type=Path, help="result JSON output directory"
    )
    parser.add_argument(
        "--collection",
        default=None,
        help="vector store collection name (adapter default if omitted)",
    )
    args = parser.parse_args(argv)

    _install_halt_handlers()

    print(
        f"D2.2a RUNNER {RUNNER_VERSION} / evaluator {EVALUATOR_VERSION} "
        f"[{REGIME}] — {INADMISSIBILITY}"
    )
    try:
        result, out_path = run_scenario(
            args.spec, args.manifest, args.index, args.out_dir, args.collection
        )
    except Refusal as refusal:
        print(f"REFUSED: {refusal}")
        for line in refusal.detail:
            print(f"  - {line}")
        print(f"exit {refusal.code} — no result artefact written")
        return refusal.code
    except (Halted, KeyboardInterrupt) as halt:
        # Rev C §8.3. The partial record is written BEFORE the exit code is
        # returned, so a halt that happens while the operator is watching and a
        # halt that happens unattended leave the same evidence.
        reason = getattr(halt, "reason", "keyboard interrupt received mid-run")
        halt_path = write_halt_record(args.out_dir, args.spec, reason)
        print(f"HALTED: {reason}")
        print(f"  partial record : {halt_path}")
        print(
            f"exit {EXIT_HALTED} — session_status=halted; inadmissible except "
            "for diagnosing the suspension"
        )
        return EXIT_HALTED

    snap = result["corpus_snapshot"]
    print(f"  spec        : {result['scenario_id']} sha256={result['spec_sha256']}")
    print(
        f"  snapshot    : {snap['manifest_version']} / {snap['manifest_sha256']}"
        f" (pins recomputed and matched; retrieval_snapshot pinned="
        f"{snap['retrieval_snapshot_pinned_by_spec']})"
    )
    print(f"  model       : {result['model_version']}")
    print(f"  index       : {result['indexed_chunk_count']} chunks at {result['index_path']}")
    print(
        f"  retrieved   : {len(result['retrieved_chunk_ids'])} chunk(s) over "
        f"{len(result['retrieved_document_ids'])} document(s): "
        f"{result['retrieved_document_ids']}"
    )
    print(
        f"  expected    : {result['expected_document_ids']} "
        f"matched={result['matched_document_ids']}"
    )
    print(f"  recall_at_k : {result['recall_at_k']}")
    env = result["environment"]
    print(
        f"  environment : config sha256={result['environment_config_sha256']} "
        f"(list v{env['material_parameter_list_version']} "
        f"sha256={result['material_parameter_list_sha256']})"
    )
    if env["unknown_parameters"]:
        print(
            f"  env UNKNOWN : {env['unknown_parameters']} — environment identity "
            "is honest but PARTIAL; the adapter does not expose these"
        )
    cap = result["retrieval"]["top_k_absolute_cap"]
    print(
        f"  top_k cap   : {cap if cap is not None else 'NOT RECORDED (pre-v0.3 spec)'}"
        f" checked={result['retrieval']['top_k_cap_checked']}"
    )
    if result["confound"]:
        print(
            f"  confound    : {result['confound']} on "
            f"{result['confound_single_chunk_document_ids']}"
        )
    else:
        print("  confound    : none (no expected document is single-chunk)")
    print(f"  session     : {result['session_status']}")
    print("  acceptance  : NOT EVALUATED (commissioning frame)")
    print(f"  result JSON : {out_path}")
    print(f"  comparable-content sha256 : {result['comparable_content_sha256']}")
    print(
        f"COMPLETED: scenario {result['scenario_id']} ran against the pinned snapshot and one "
        f"result artefact was written [{REGIME}, inadmissible as gate evidence]"
    )
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
