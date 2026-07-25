"""Audit store schema (RAT-02 spec section 5) — SQLAlchemy table definitions.

All tables are append-only: application code performs INSERT and SELECT
only, and the runtime role's grant excludes UPDATE and DELETE
(``sql/governance_grants.sql``; enforced by test, not convention).

**One deliberate deviation from the spec letter, recorded here and in
the delivery note.** Spec section 5 names three tables, but also
requires (a) a run record opened *before any work happens*, (b) a
terminal record on every exit path, and (c) no UPDATE grant. Those
three cannot coexist in a single ``audit_run`` row: closing a run that
was opened earlier is an UPDATE. Granting UPDATE on outcome columns
alone was considered and rejected — column-scoped UPDATE still breaches
"no UPDATE in application code" as written, and any UPDATE path on
``audit_run`` weakens section 4's "immutable thereafter" guarantee on
execution metadata. Resolution: the spec's own two nouns are two rows.
``audit_run`` holds the *run record* (written once, at entry);
``audit_run_terminal`` holds the *terminal record* (written once, in the
wrapper's ``finally``). Every stated invariant survives except the
table count, which becomes four. Needs a line in ADR-0010's evidence
trail; drafted in the delivery note for ratification.
"""

from __future__ import annotations

import uuid

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class AuditBase(DeclarativeBase):
    pass


class AuditRun(AuditBase):
    """One row per governed request — written once, at wrapper entry.

    Execution metadata as typed columns plus a JSONB overflow
    (spec section 5). Immutable after insert.
    """

    __tablename__ = "audit_run"

    correlation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True
    )
    started_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    # Subject reference — CL-21 gap 2 lands here (spec section 5.2).
    # Indexed from the outset: without it, "retrieve every record
    # relating to one individual" is a full table scan.
    subject_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # Execution metadata, typed (spec section 4). Nullable columns carry
    # NULL when the owning stage has not landed — never "" or a sentinel.
    code_sha: Mapped[str] = mapped_column(String(64), nullable=False)
    code_sha_source: Mapped[str] = mapped_column(String(16), nullable=False)
    env_id: Mapped[str] = mapped_column(String(128), nullable=False)
    schema_version: Mapped[str] = mapped_column(String(16), nullable=False)
    # none_as_null on every JSONB column: SQLAlchemy's default converts a
    # Python None into a JSON `null` *value*, which is precisely the
    # sentinel-masquerading-as-NULL that spec section 4 prohibits — it
    # passes `IS NOT NULL` while meaning "not populated". Caught by
    # test_unpopulated_metadata_fields_are_null on first run.
    model_artifacts: Mapped[dict | None] = mapped_column(
        JSONB(none_as_null=True), nullable=True
    )
    llm_pin: Mapped[str | None] = mapped_column(String(256), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    corpus_version: Mapped[str | None] = mapped_column(String(128), nullable=True)
    retrieval_config: Mapped[dict | None] = mapped_column(
        JSONB(none_as_null=True), nullable=True
    )

    # JSONB overflow for metadata that has no typed column yet.
    metadata_extra: Mapped[dict | None] = mapped_column(
        JSONB(none_as_null=True), nullable=True
    )

    __table_args__ = (
        Index("ix_audit_run_subject_ref", "subject_ref"),
        CheckConstraint(
            "code_sha_source IN ('build', 'fallback')",
            name="ck_audit_run_code_sha_source",
        ),
        # NULL-not-sentinel discipline, enforced at the store as well as
        # in application code: an empty string in a nullable metadata
        # column is a defect wherever it came from.
        CheckConstraint("llm_pin <> ''", name="ck_audit_run_llm_pin_not_empty"),
        CheckConstraint(
            "prompt_version <> ''", name="ck_audit_run_prompt_version_not_empty"
        ),
        CheckConstraint(
            "corpus_version <> ''", name="ck_audit_run_corpus_version_not_empty"
        ),
    )


class AuditRunTerminal(AuditBase):
    """Terminal record — one row per run, written once, in ``finally``.

    See the module docstring for why this is a separate append-once
    table rather than an UPDATE on ``audit_run``.
    """

    __tablename__ = "audit_run_terminal"

    correlation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("audit_run.correlation_id"),
        primary_key=True,
    )
    ended_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    outcome: Mapped[str] = mapped_column(String(16), nullable=False)
    # On failure/abort: exception type and message, never the traceback
    # (spec section 3.4 — tracebacks can carry payload into the record).
    error_type: Mapped[str | None] = mapped_column(String(256), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "outcome IN ('completed', 'failed', 'aborted')",
            name="ck_audit_run_terminal_outcome",
        ),
    )


class AuditEvent(AuditBase):
    """One row per step within a run (spec section 5).

    **Sequence number, not timestamp, is the ordering key** — the primary
    key is (correlation_id, sequence_number), so B9 replay order is
    deterministic even for two events in the same microsecond. The
    wrapper owns the monotonic counter.

    ``span_id``/``parent_span_id`` carry wrapper nesting (spec
    section 3, nesting): a child wrapper reuses the parent correlation
    id and records a child span rather than minting a new run.
    """

    __tablename__ = "audit_event"

    correlation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("audit_run.correlation_id"),
        primary_key=True,
    )
    sequence_number: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    actor: Mapped[str | None] = mapped_column(String(128), nullable=True)
    span_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    parent_span_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    payload_ref: Mapped[str | None] = mapped_column(
        String(64), ForeignKey("audit_payload.payload_sha256"), nullable=True
    )
    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    __table_args__ = (
        Index("ix_audit_event_event_type", "event_type"),
    )


class AuditPayload(AuditBase):
    """Content-addressed text store (spec section 5.1).

    Prompt and response text lives here, keyed by its sha256; the event
    row carries only the hash. This is what makes CL-21's crypto-shred
    possible later — shred this table, keep the decision record and its
    hashes intact. Content addressing also deduplicates identical
    prompts across runs.
    """

    __tablename__ = "audit_payload"

    payload_sha256: Mapped[str] = mapped_column(String(64), primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    byte_length: Mapped[int] = mapped_column(Integer, nullable=False)
    first_seen_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
