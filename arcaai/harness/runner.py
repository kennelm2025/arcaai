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
SCHEMA_BY_VERSION = {
    "0.1": SCHEMA_DIR / "scenario_spec_v0.1.schema.json",
    "0.2": SCHEMA_DIR / "scenario_spec_v0.2.schema.json",
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

    result: dict[str, Any] = {
        "regime": REGIME,
        "admissibility": INADMISSIBILITY,
        "runner_version": RUNNER_VERSION,
        "runner_commit": _git_commit(manifest_path.parent),
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
            "scoring_method": block["scoring_method"],
        },
        "retrieved_chunk_ids": chunk_ids,
        "retrieved_document_ids": doc_ids,
        "retrieved_scores": scores,
        "expected_document_ids": expected,
        "matched_document_ids": matched,
        "recall_at_k": recall,
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

    print(f"D2.2a RUNNER {RUNNER_VERSION} [{REGIME}] — {INADMISSIBILITY}")
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
