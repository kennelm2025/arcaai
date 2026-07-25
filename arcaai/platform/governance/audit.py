"""Audit persistence (RAT-02 spec section 5) — INSERT and SELECT only.

Application code contains no UPDATE and no DELETE; the runtime role's
grant excludes them (``sql/governance_grants.sql``), so the property is
enforced by the database, not by review. Each write commits in its own
transaction: an audit record that waits for the request to finish is a
record that vanishes when the process does.

The one apparent exception, ``ON CONFLICT DO NOTHING`` on the
content-addressed payload table, is still an INSERT: identical content
hashes to an identical key, and re-inserting the same bytes under the
same hash is a no-op by construction, not a mutation.
"""

from __future__ import annotations

import hashlib
import uuid
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any

from sqlalchemy import Engine, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from .metadata import ExecutionMetadata, utcnow
from .models import AuditEvent, AuditPayload, AuditRun, AuditRunTerminal


class AuditStore:
    """Thin persistence layer over the four audit tables.

    Constructed with an Engine bound to the *runtime* role
    (``arcaai_app``): SELECT + INSERT only. Schema creation is the
    owner role's job and does not happen here.
    """

    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    # -- run lifecycle ----------------------------------------------------

    def open_run(
        self,
        *,
        correlation_id: uuid.UUID,
        started_at: datetime,
        metadata: ExecutionMetadata,
        subject_ref: str | None,
        source: str | None,
        metadata_extra: Mapping[str, Any] | None = None,
    ) -> None:
        """Write the run record — once, at entry, before any work happens."""
        with Session(self._engine) as session:
            session.add(
                AuditRun(
                    correlation_id=correlation_id,
                    started_at=started_at,
                    subject_ref=subject_ref,
                    source=source,
                    code_sha=metadata.code_sha,
                    code_sha_source=metadata.code_sha_source,
                    env_id=metadata.env_id,
                    schema_version=metadata.schema_version,
                    model_artifacts=(
                        dict(metadata.model_artifacts)
                        if metadata.model_artifacts is not None
                        else None
                    ),
                    llm_pin=metadata.llm_pin,
                    prompt_version=metadata.prompt_version,
                    corpus_version=metadata.corpus_version,
                    retrieval_config=(
                        dict(metadata.retrieval_config)
                        if metadata.retrieval_config is not None
                        else None
                    ),
                    metadata_extra=(
                        dict(metadata_extra) if metadata_extra is not None else None
                    ),
                )
            )
            session.commit()

    def close_run(
        self,
        *,
        correlation_id: uuid.UUID,
        started_at: datetime,
        outcome: str,
        error_type: str | None = None,
        error_message: str | None = None,
        ended_at: datetime | None = None,
    ) -> None:
        """Write the terminal record — once, from the wrapper's ``finally``.

        An INSERT into ``audit_run_terminal``, not an UPDATE on
        ``audit_run`` — see models.py module docstring.
        """
        ended = ended_at if ended_at is not None else utcnow()
        duration_ms = max(
            0, int((ended - started_at).total_seconds() * 1000)
        )
        with Session(self._engine) as session:
            session.add(
                AuditRunTerminal(
                    correlation_id=correlation_id,
                    ended_at=ended,
                    outcome=outcome,
                    error_type=error_type,
                    error_message=error_message,
                    duration_ms=duration_ms,
                )
            )
            session.commit()

    # -- events and payloads ----------------------------------------------

    def record_event(
        self,
        *,
        correlation_id: uuid.UUID,
        sequence_number: int,
        event_type: str,
        actor: str | None,
        span_id: uuid.UUID | None,
        parent_span_id: uuid.UUID | None,
        payload: Mapping[str, Any] | None,
        payload_ref: str | None,
    ) -> None:
        with Session(self._engine) as session:
            session.add(
                AuditEvent(
                    correlation_id=correlation_id,
                    sequence_number=sequence_number,
                    event_type=event_type,
                    actor=actor,
                    span_id=span_id,
                    parent_span_id=parent_span_id,
                    payload=dict(payload) if payload is not None else None,
                    payload_ref=payload_ref,
                    created_at=utcnow(),
                )
            )
            session.commit()

    def store_payload(self, text: str) -> str:
        """Store free text content-addressed; return its sha256 hex.

        Idempotent by construction: identical text, identical key,
        ``ON CONFLICT DO NOTHING``.
        """
        raw = text.encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        stmt = (
            pg_insert(AuditPayload)
            .values(
                payload_sha256=digest,
                content=text,
                byte_length=len(raw),
                first_seen_at=utcnow(),
            )
            .on_conflict_do_nothing(index_elements=["payload_sha256"])
        )
        with Session(self._engine) as session:
            session.execute(stmt)
            session.commit()
        return digest

    # -- reads (B9 replay / subject retrieval) ----------------------------

    def events_for_run(self, correlation_id: uuid.UUID) -> Sequence[AuditEvent]:
        """Replay order: sequence number, nothing else (spec section 5)."""
        with Session(self._engine) as session:
            rows = session.scalars(
                select(AuditEvent)
                .where(AuditEvent.correlation_id == correlation_id)
                .order_by(AuditEvent.sequence_number)
            ).all()
            session.expunge_all()
            return rows

    def runs_for_subject(self, subject_ref: str) -> Sequence[AuditRun]:
        """Every run for one subject — the CL-21 gap-2 query, via the index."""
        with Session(self._engine) as session:
            rows = session.scalars(
                select(AuditRun)
                .where(AuditRun.subject_ref == subject_ref)
                .order_by(AuditRun.started_at)
            ).all()
            session.expunge_all()
            return rows
