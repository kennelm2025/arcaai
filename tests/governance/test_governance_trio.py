"""RAT-02 spec section 7 test list, in spec order, plus supporting checks.

Every test that touches the database runs under the *runtime* role
(``arcaai_app``) so that what passes here is what holds in production.
"""

from __future__ import annotations

import ast
import pathlib
import uuid

import pytest
import sqlalchemy.exc
from pydantic import ValidationError
from sqlalchemy import inspect, select, text
from sqlalchemy.orm import Session

import arcaai.platform.governance as _governance_pkg
from arcaai.platform.governance import (
    EventType,
    GovernedEvent,
    ModelScored,
    RequestReceived,
    governed_request,
)
from arcaai.platform.governance.events import ProhibitedFieldName
from arcaai.platform.governance.models import (
    AuditEvent,
    AuditRun,
    AuditRunTerminal,
)

# Resolved from the package's own import, not from this file's position:
# the test must survive relocation (e.g. into tests/governance/) without
# silently pointing at an empty directory and passing vacuously.
GOVERNANCE_PKG = pathlib.Path(_governance_pkg.__file__).resolve().parent


def _terminal(app_engine, correlation_id) -> AuditRunTerminal:
    with Session(app_engine) as s:
        row = s.scalars(
            select(AuditRunTerminal).where(
                AuditRunTerminal.correlation_id == correlation_id
            )
        ).one()
        s.expunge_all()
        return row


# -- 1. Terminal record on all three exit paths ---------------------------


def test_terminal_record_on_success(store, app_engine):
    with governed_request(store, source="test") as ctx:
        ctx.emit(RequestReceived(channel="test"))
        cid = ctx.correlation_id
    row = _terminal(app_engine, cid)
    assert row.outcome == "completed"
    assert row.error_type is None and row.error_message is None


def test_terminal_record_on_handled_failure(store, app_engine):
    with governed_request(store, source="test") as ctx:
        cid = ctx.correlation_id
        ctx.mark_failed("UpstreamTimeout", "scoring service did not respond")
    row = _terminal(app_engine, cid)
    assert row.outcome == "failed"
    assert row.error_type == "UpstreamTimeout"


def test_terminal_record_on_unhandled_exception(store, app_engine):
    """The one that catches regressions (spec section 7)."""
    cid = None
    with (
        pytest.raises(RuntimeError, match="boom"),
        governed_request(store, source="test") as ctx,
    ):
        cid = ctx.correlation_id
        raise RuntimeError("boom")
    row = _terminal(app_engine, cid)
    assert row.outcome == "aborted"
    assert row.error_type == "RuntimeError"
    assert row.error_message == "boom"
    # Message, never the traceback (spec section 3.4).
    assert "Traceback" not in (row.error_message or "")
    assert "test_governance_trio" not in (row.error_message or "")


# -- 2. Sequence numbers strictly increasing, no gaps ---------------------


def test_sequence_numbers_strictly_increasing_no_gaps(store, app_engine):
    with governed_request(store) as ctx:
        cid = ctx.correlation_id
        for i in range(5):
            ctx.emit(ModelScored(probability=0.1 * i, artifact_sha256="ab" * 32))
        ctx.emit_ref(EventType.LLM_INVOKED, text="prompt text")
    with Session(app_engine) as s:
        seqs = s.scalars(
            select(AuditEvent.sequence_number)
            .where(AuditEvent.correlation_id == cid)
            .order_by(AuditEvent.sequence_number)
        ).all()
    assert seqs == list(range(1, 7))


# -- 3. Nested wrapper reuses parent correlation id -----------------------


def test_nested_wrapper_reuses_correlation_id(store, app_engine):
    with governed_request(store) as root:
        with governed_request(store) as child:
            assert child.correlation_id == root.correlation_id
            child.emit(RequestReceived(channel="sub-agent"), actor="child_node")
        root.emit(RequestReceived(channel="root"), actor="root_node")
        cid = root.correlation_id
    # One run, one terminal — the child minted neither.
    with Session(app_engine) as s:
        runs = s.scalars(
            select(AuditRun).where(AuditRun.correlation_id == cid)
        ).all()
        terms = s.scalars(
            select(AuditRunTerminal).where(
                AuditRunTerminal.correlation_id == cid
            )
        ).all()
        events = s.scalars(
            select(AuditEvent)
            .where(AuditEvent.correlation_id == cid)
            .order_by(AuditEvent.sequence_number)
        ).all()
        assert len(runs) == 1 and len(terms) == 1
        # Child span recorded: differing span ids, child's parent = root's span.
        child_evt, root_evt = events
        assert child_evt.span_id != root_evt.span_id
        assert child_evt.parent_span_id == root_evt.span_id
        assert root_evt.parent_span_id is None
        # Shared counter: no sequence collision across spans.
        assert [e.sequence_number for e in events] == [1, 2]


# -- 4. Metadata captured once, not mutated by later emits ----------------


def test_metadata_captured_once_and_immutable(store):
    with governed_request(store, llm_pin="llama3.1:8b@sha256:feed") as ctx:
        before = ctx.metadata
        ctx.emit(ModelScored(probability=0.5, artifact_sha256="cd" * 32))
        after = ctx.metadata
        assert before is after  # same frozen object, not re-captured
        with pytest.raises(ValidationError):
            ctx.metadata.llm_pin = "tampered"  # type: ignore[misc]


# -- 5. Unpopulated metadata fields are NULL, not "" or sentinel ----------


def test_unpopulated_metadata_fields_are_null(store, app_engine):
    with governed_request(store) as ctx:  # no B7/B8 fields supplied
        cid = ctx.correlation_id
    with app_engine.connect() as conn:
        row = conn.execute(
            text(
                "SELECT prompt_version IS NULL, corpus_version IS NULL, "
                "retrieval_config IS NULL, llm_pin IS NULL, "
                "model_artifacts IS NULL, metadata_extra IS NULL "
                "FROM audit_run WHERE correlation_id = :cid"
            ),
            {"cid": str(cid)},
        ).one()
    assert all(row), "unpopulated metadata columns must be SQL NULL"


def test_empty_string_metadata_rejected_by_store(app_engine):
    """The CHECK constraints back the discipline at the database."""
    with pytest.raises(sqlalchemy.exc.IntegrityError), Session(app_engine) as s:
        s.add(
            AuditRun(
                correlation_id=uuid.uuid4(),
                started_at=__import__(
                    "arcaai.platform.governance.metadata",
                    fromlist=["utcnow"],
                ).utcnow(),
                code_sha="unknown",
                code_sha_source="fallback",
                env_id="t/py",
                schema_version="1.0.0",
                llm_pin="",  # the defect under test
            )
        )
        s.commit()


# -- 6. code_sha_source records fallback ----------------------------------


def test_code_sha_fallback_recorded(store, app_engine):
    with governed_request(store, _environ={}) as ctx:  # no ARCAAI_CODE_SHA
        cid = ctx.correlation_id
        assert ctx.metadata.code_sha == "unknown"
        assert ctx.metadata.code_sha_source == "fallback"
    with Session(app_engine) as s:
        run = s.get(AuditRun, cid)
        assert run is not None
        assert (run.code_sha, run.code_sha_source) == ("unknown", "fallback")


def test_code_sha_build_injection(store):
    env = {"ARCAAI_CODE_SHA": "f11ff0a"}
    with governed_request(store, _environ=env) as ctx:
        assert ctx.metadata.code_sha == "f11ff0a"
        assert ctx.metadata.code_sha_source == "build"


# -- 7. No UPDATE/DELETE path: attempt one, assert it fails ---------------


@pytest.mark.parametrize(
    "statement",
    [
        "UPDATE audit_run SET code_sha = 'rewritten'",
        "DELETE FROM audit_event",
        "UPDATE audit_run_terminal SET outcome = 'completed'",
        "DELETE FROM audit_payload",
    ],
)
def test_update_and_delete_denied_to_app_role(app_engine, statement):
    with (
        pytest.raises(sqlalchemy.exc.ProgrammingError) as excinfo,
        app_engine.connect() as conn,
    ):
        conn.execute(text(statement))
        conn.commit()
    assert "permission denied" in str(excinfo.value).lower()


# -- 8. Payload text absent from audit_event; only the hash ---------------


def test_payload_text_stored_by_reference_only(store, app_engine):
    secret = "Customer narrative that must never sit in the event row 42."
    with governed_request(store) as ctx:
        cid = ctx.correlation_id
        digest = ctx.emit_ref(EventType.LLM_INVOKED, text=secret)
    with app_engine.connect() as conn:
        evt = conn.execute(
            text(
                "SELECT event_type, payload::text, payload_ref FROM audit_event "
                "WHERE correlation_id = :cid"
            ),
            {"cid": str(cid)},
        ).one()
        stored = conn.execute(
            text(
                "SELECT content FROM audit_payload "
                "WHERE payload_sha256 = :h"
            ),
            {"h": digest},
        ).scalar_one()
    assert secret not in evt.payload
    assert evt.payload_ref == digest
    assert stored == secret


def test_payload_dedup_across_runs(store, app_engine):
    prompt = "identical prompt across two runs"
    with governed_request(store) as ctx:
        h1 = ctx.emit_ref("llm_invoked", text=prompt)
    with governed_request(store) as ctx:
        h2 = ctx.emit_ref("llm_invoked", text=prompt)
    assert h1 == h2
    with app_engine.connect() as conn:
        n = conn.execute(
            text("SELECT count(*) FROM audit_payload WHERE payload_sha256 = :h"),
            {"h": h1},
        ).scalar_one()
    assert n == 1  # content-addressed: one row, two references


# -- 9. subject_ref index exists; lookup returns all runs -----------------


def test_subject_ref_index_exists(app_engine):
    indexes = inspect(app_engine).get_indexes("audit_run")
    assert any(
        ix["column_names"] == ["subject_ref"] for ix in indexes
    ), "subject_ref must be indexed from the outset (spec section 5.2 / CL-21 gap 2)"


def test_subject_lookup_returns_all_runs(store):
    subject = f"subj-{uuid.uuid4().hex[:12]}"
    cids = []
    for _ in range(3):
        with governed_request(store, subject_ref=subject) as ctx:
            cids.append(ctx.correlation_id)
    with governed_request(store, subject_ref="someone-else"):
        pass
    found = store.runs_for_subject(subject)
    assert sorted(r.correlation_id for r in found) == sorted(cids)


# -- 10. Negative test — prohibited field name fails at definition --------


def test_prohibited_field_name_fails_at_model_definition():
    with pytest.raises(ProhibitedFieldName, match="account_number"):

        class WellIntentioned(GovernedEvent):
            event_type = EventType.REQUEST_RECEIVED
            account_number: str  # the mistake, months from now


# -- 11. Negative test — free text rejected at construction ---------------


def test_free_text_field_rejected_at_construction():
    with pytest.raises(ValidationError, match="256"):
        RequestReceived(channel="x" * 300)


def test_free_text_in_list_field_rejected():
    with pytest.raises(ValidationError, match="256"):
        __import__(
            "arcaai.platform.governance.events", fromlist=["RetrievalPerformed"]
        ).RetrievalPerformed(
            chunk_ids=["ok", "y" * 300], manifest_version="v1", top_k=5
        )


def test_undeclared_field_rejected():
    """Allowlist by construction: nowhere to put an unknown field."""
    with pytest.raises(ValidationError):
        ModelScored(
            probability=0.5, artifact_sha256="ab" * 32, customer_note="hello"
        )


def test_emit_rejects_free_form_dict(store):
    with (
        governed_request(store) as ctx,
        pytest.raises(TypeError, match="typed GovernedEvent"),
    ):
        ctx.emit({"event": "model_scored", "probability": 0.5})  # type: ignore[arg-type]


# -- 12. Boundary test — platform imports nothing from verticals ----------


def test_platform_governance_imports_nothing_from_verticals():
    """Machine-checked ADR-0009 boundary; seed for the B9.5 CI check and
    mandatory CF-1 evidence at B7."""
    offenders: list[str] = []
    scanned = 0
    for path in GOVERNANCE_PKG.rglob("*.py"):
        scanned += 1
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            for name in names:
                root = name.split(".")[0]
                if root == "verticals" or ".verticals" in name:
                    offenders.append(f"{path.name}: {name}")
    assert scanned >= 6, (
        f"boundary scan saw only {scanned} files at {GOVERNANCE_PKG}; "
        "an empty scan is a vacuous pass, not a clean one"
    )
    assert not offenders, f"platform->verticals imports found: {offenders}"
