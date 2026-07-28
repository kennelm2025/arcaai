"""DEC-0014 corpus manifest suite.

Pure-function coverage runs without a database; the snapshot and
denial tests run under the same two-role pattern as the trio suite.
"""

from __future__ import annotations

import copy
import datetime
import pathlib
import uuid

import pytest
import sqlalchemy.exc
import yaml
from sqlalchemy import text
from sqlalchemy.orm import Session

from arcaai.platform.governance import corpus
from arcaai.platform.governance.models import CorpusVersion

MANIFEST_PATH = (
    pathlib.Path(__file__).resolve().parents[2]
    / "verticals" / "fraud" / "corpus" / "MANIFEST.yaml"
)


@pytest.fixture()
def manifest() -> dict:
    return corpus.parse_manifest(MANIFEST_PATH.read_text(encoding="utf-8"))


@pytest.fixture()
def evolved(manifest) -> dict:
    """The seed manifest with one document transitioned to included."""
    m = copy.deepcopy(manifest)
    m["manifest_version"] = manifest["manifest_version"] + "-t"
    m["documents"][0]["eligibility"].append(
        {"state": "included", "date": "2026-07-29", "reason": "authored"}
    )
    return m


# -- 1. The committed seed manifest is valid ------------------------------


def test_seed_manifest_parses_and_nothing_is_eligible(manifest):
    assert len(manifest["documents"]) == 2
    # both seeds are pending_review: nothing retrievable until real
    # content exists (DEC-0014 / seed design)
    assert corpus.eligible_documents(manifest) == []


# -- 2. Canonicalisation is reflow-invariant ------------------------------


def test_hash_survives_reserialisation(manifest):
    reflowed = yaml.safe_load(yaml.dump(manifest, default_flow_style=True))
    assert corpus.manifest_sha256(reflowed) == corpus.manifest_sha256(manifest)


def test_hash_changes_with_content(manifest, evolved):
    assert corpus.manifest_sha256(evolved) != corpus.manifest_sha256(manifest)


# -- 3. Two hashes, two questions (panel Q4) ------------------------------


def test_chunker_change_moves_snapshot_hash_only(evolved):
    rechunked = copy.deepcopy(evolved)
    rechunked["documents"][0]["processing"]["chunker_version"] = "recursive-512-v2"
    assert corpus.eligible_set_sha256(rechunked) == corpus.eligible_set_sha256(evolved)
    assert corpus.retrieval_snapshot_sha256(rechunked) != corpus.retrieval_snapshot_sha256(evolved)


def test_eligibility_change_moves_both_hashes(manifest, evolved):
    assert corpus.eligible_set_sha256(evolved) != corpus.eligible_set_sha256(manifest)
    assert corpus.retrieval_snapshot_sha256(evolved) != corpus.retrieval_snapshot_sha256(manifest)


# -- 4. Eligibility as at a date (B7_GATE section 3) ----------------------


def test_state_as_at(evolved):
    doc = evolved["documents"][0]
    assert corpus.state_as_at(doc, datetime.date(2026, 7, 27)) is None
    assert corpus.state_as_at(doc, datetime.date(2026, 7, 28)) == "pending_review"
    assert corpus.state_as_at(doc, datetime.date(2026, 7, 29)) == "included"
    assert corpus.state_as_at(doc, datetime.date(2027, 1, 1)) == "included"


# -- 5. Mechanical append-only (DEC-0014 item 5) --------------------------


def test_appending_a_transition_is_valid(manifest, evolved):
    corpus.check_append_only(manifest, evolved)  # must not raise


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
            lambda m: m["documents"][0].__setitem__(
                "content_sha256",
                "2222222222222222222222222222222222222222222222222222222222222222",
            ),
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
            lambda m: m["documents"][1].__setitem__("id", m["documents"][0]["id"]),
            id="duplicate-id",
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
        assert row1.eligible_doc_count == 1  # derived, cached

        tampered = copy.deepcopy(evolved)
        tampered["documents"][0]["source"] = "rewritten history"
        with pytest.raises(corpus.HashPinMismatch):
            corpus.load_snapshot(s, tampered)  # same label, new content


def test_corpus_version_update_delete_denied(app_engine, evolved):
    with Session(app_engine) as s:
        corpus.load_snapshot(s, evolved)
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
