"""DEC-0014 corpus manifest suite.

Machinery tests run against FIXTURE manifests constructed in this file,
never against the live governed manifest at
verticals/fraud/corpus/MANIFEST.yaml. The first cut of this suite
asserted content facts of the live manifest (document count,
eligibility state as at a date) and broke the moment the manifest
advanced by governed process — which is what a governed artefact is
for. A test coupled to governed content is the parallel-document class
(WS-E 53) in test form. The live manifest gets exactly one test here:
shape invariants that hold for every valid version.
"""

from __future__ import annotations

import copy
import datetime
import hashlib
import pathlib
import uuid

import pytest
import sqlalchemy.exc
import yaml
from sqlalchemy import text
from sqlalchemy.orm import Session

from arcaai.platform.governance import corpus
from arcaai.platform.governance.models import CorpusVersion

LIVE_MANIFEST = (
    pathlib.Path(__file__).resolve().parents[2]
    / "verticals" / "fraud" / "corpus" / "MANIFEST.yaml"
)


def _sha(tag: str) -> str:
    return hashlib.sha256(tag.encode()).hexdigest()


def make_manifest() -> dict:
    """Two-document fixture; unique version label per call so snapshot
    tests never collide across the session."""
    return {
        "manifest_version": f"fixture-{uuid.uuid4()}",
        "documents": [
            {
                "id": "FIX-A",
                "source": "fixture document A",
                "licence": "synthetic-arcaai",
                "sa5_classification": "internal-sensitive",
                "content_sha256": _sha("fixture-a"),
                "eligibility": [
                    {"state": "pending_review", "date": "2026-07-01",
                     "reason": "fixture birth"},
                ],
                "processing": {"chunker_version": None,
                               "embedding_model": None,
                               "chunk_count": None,
                               "ingest_timestamp": None},
            },
            {
                "id": "FIX-B",
                "source": "fixture document B",
                "licence": "OGL-v3.0",
                "sa5_classification": "internal-sensitive",
                "content_sha256": _sha("fixture-b"),
                "eligibility": [
                    {"state": "pending_review", "date": "2026-07-01",
                     "reason": "fixture birth"},
                ],
                "processing": {"chunker_version": "chunker-v1",
                               "embedding_model": "embed-v1",
                               "chunk_count": 3,
                               "ingest_timestamp": "2026-07-01T00:00:00Z"},
            },
        ],
    }


@pytest.fixture()
def manifest() -> dict:
    return make_manifest()


@pytest.fixture()
def evolved(manifest) -> dict:
    """The fixture with FIX-A transitioned to included."""
    m = copy.deepcopy(manifest)
    m["manifest_version"] = f"fixture-{uuid.uuid4()}"
    m["documents"][0]["eligibility"].append(
        {"state": "included", "date": "2026-07-15", "reason": "fixture inclusion"}
    )
    return m


# -- 1. The live governed manifest: shape invariants only -----------------


def test_live_manifest_shape():
    """Invariants that hold for EVERY valid version of the governed
    manifest — never counts, states or dates, which advance by
    governed process."""
    m = corpus.parse_manifest(LIVE_MANIFEST.read_text(encoding="utf-8"))
    assert len(m["documents"]) >= 1
    assert {d["licence"] for d in m["documents"]} <= corpus.LICENCES
    # every eligibility state reachable in the file is in the enum
    for d in m["documents"]:
        for t in d["eligibility"]:
            assert t["state"] in corpus.STATES


# -- 2. Canonicalisation is reflow-invariant ------------------------------


def test_hash_survives_reserialisation(manifest):
    reflowed = yaml.safe_load(yaml.dump(manifest, default_flow_style=True))
    assert corpus.manifest_sha256(reflowed) == corpus.manifest_sha256(manifest)


def test_hash_changes_with_content(manifest, evolved):
    m2 = copy.deepcopy(manifest)
    m2["manifest_version"] = manifest["manifest_version"]  # same label
    m2["documents"][0]["eligibility"].append(
        {"state": "included", "date": "2026-07-15", "reason": "fixture inclusion"}
    )
    assert corpus.manifest_sha256(m2) != corpus.manifest_sha256(manifest)


# -- 3. Two hashes, two questions (panel Q4) ------------------------------


def test_chunker_change_moves_snapshot_hash_only(evolved):
    rechunked = copy.deepcopy(evolved)
    rechunked["documents"][0]["processing"]["chunker_version"] = "chunker-v2"
    assert corpus.eligible_set_sha256(rechunked) == corpus.eligible_set_sha256(evolved)
    assert corpus.retrieval_snapshot_sha256(rechunked) != corpus.retrieval_snapshot_sha256(
        evolved
    )


def test_eligibility_change_moves_both_hashes(manifest, evolved):
    assert corpus.eligible_set_sha256(evolved) != corpus.eligible_set_sha256(manifest)
    assert corpus.retrieval_snapshot_sha256(evolved) != corpus.retrieval_snapshot_sha256(
        manifest
    )


def test_empty_corpus_hashes_are_constant(manifest):
    # nothing eligible: both hashes are the hash of an empty list
    assert corpus.eligible_set_sha256(manifest) == corpus.retrieval_snapshot_sha256(manifest)


# -- 4. Eligibility as at a date (B7_GATE section 3) ----------------------


def test_state_as_at(evolved):
    doc = evolved["documents"][0]
    assert corpus.state_as_at(doc, datetime.date(2026, 6, 30)) is None
    assert corpus.state_as_at(doc, datetime.date(2026, 7, 1)) == "pending_review"
    assert corpus.state_as_at(doc, datetime.date(2026, 7, 14)) == "pending_review"
    assert corpus.state_as_at(doc, datetime.date(2026, 7, 15)) == "included"
    assert corpus.state_as_at(doc, datetime.date(2027, 1, 1)) == "included"


# -- 5. Mechanical append-only (DEC-0014 item 5) --------------------------


def test_appending_a_transition_is_valid(manifest, evolved):
    corpus.check_append_only(manifest, evolved)  # must not raise


def test_adding_a_document_is_valid(manifest):
    grown = copy.deepcopy(manifest)
    grown["documents"].append(copy.deepcopy(manifest["documents"][0]) | {
        "id": "FIX-C", "content_sha256": _sha("fixture-c")})
    corpus.check_append_only(manifest, grown)  # additions are legal


@pytest.mark.parametrize(
    "mutate",
    [
        pytest.param(lambda m: m["documents"][0]["eligibility"].pop(), id="deleted"),
        pytest.param(
            lambda m: m["documents"][0]["eligibility"][0].__setitem__("reason", "edited"),
            id="modified",
        ),
        pytest.param(lambda m: m["documents"].pop(0), id="document-removed"),
        pytest.param(
            lambda m: m["documents"][0].__setitem__("content_sha256", _sha("tampered")),
            id="identity-changed",
        ),
    ],
)
def test_append_only_violations_raise(evolved, mutate):
    broken = copy.deepcopy(evolved)
    mutate(broken)
    with pytest.raises(corpus.AppendOnlyViolation):
        corpus.check_append_only(evolved, broken)


# -- 6. Schema rejections -------------------------------------------------


@pytest.mark.parametrize(
    "breaker",
    [
        pytest.param(lambda m: m["documents"][0].__setitem__("licence", "MIT"), id="licence"),
        pytest.param(
            lambda m: m["documents"][0]["eligibility"][0].__setitem__("state", "live"),
            id="state",
        ),
        pytest.param(
            lambda m: m["documents"][0].__setitem__("content_sha256", "abc"), id="sha"
        ),
        pytest.param(
            lambda m: m["documents"][1].__setitem__("id", "FIX-A"), id="duplicate-id"
        ),
        pytest.param(
            lambda m: m["documents"][0]["eligibility"].insert(
                0, {"state": "included", "date": "2026-08-01", "reason": "x"}
            ),
            id="out-of-order",
        ),
    ],
)
def test_schema_violations_raise(manifest, breaker):
    broken = copy.deepcopy(manifest)
    breaker(broken)
    with pytest.raises(corpus.ManifestError):
        corpus.parse_manifest(yaml.dump(broken))


# -- 7. Snapshot: idempotent load, hash pin, denial -----------------------


def test_load_snapshot_idempotent_and_pinned(app_engine, evolved):
    with Session(app_engine) as s:
        row1 = corpus.load_snapshot(s, evolved)
        row2 = corpus.load_snapshot(s, evolved)
        assert row1.version_id == row2.version_id  # idempotent re-load
        assert row1.eligible_doc_count == 1  # FIX-A included, FIX-B pending

        tampered = copy.deepcopy(evolved)
        tampered["documents"][0]["source"] = "rewritten history"
        with pytest.raises(corpus.HashPinMismatch):
            corpus.load_snapshot(s, tampered)  # same label, new content


def test_corpus_version_update_delete_denied(app_engine, manifest):
    with Session(app_engine) as s:
        corpus.load_snapshot(s, manifest)
    for statement in (
        "UPDATE corpus_version SET manifest_sha256 = 'rewritten'",
        "DELETE FROM corpus_version",
    ):
        with (
            pytest.raises(sqlalchemy.exc.ProgrammingError) as excinfo,
            app_engine.connect() as conn,
        ):
            conn.execute(text(statement))
            conn.commit()
        assert "permission denied" in str(excinfo.value).lower()


def test_empty_string_rejected_by_store(app_engine):
    with pytest.raises(sqlalchemy.exc.IntegrityError), Session(app_engine) as s:
        s.add(
            CorpusVersion(
                version_id=uuid.uuid4(),
                manifest_version="",  # the defect under test
                manifest_sha256="ab" * 32,
                eligible_set_sha256="cd" * 32,
                retrieval_snapshot_sha256="ef" * 32,
                eligible_doc_count=0,
                loaded_at=datetime.datetime.now(datetime.timezone.utc),
            )
        )
        s.commit()
