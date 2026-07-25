"""Request wrapper (RAT-02 spec section 3) — the governed context.

One object, three calls (spec section 6)::

    with governed_request(store, subject_ref=..., source=...) as ctx:
        ctx.emit(ModelScored(probability=..., artifact_sha256=...))
        ctx.emit_ref("llm_invoked", text=prompt)   # hashed, stored by reference
        meta = ctx.metadata                        # read-only

Exit-path mapping (spec section 3.4):

* normal exit                       -> ``completed``
* ``ctx.mark_failed(...)`` + exit   -> ``failed``   (handled failure)
* exception propagating out         -> ``aborted``  (unhandled), with
  exception type and message recorded — never the traceback, which can
  carry payload data into the record.

The terminal record is written in a ``finally``; an audit trail that
records only successes cannot answer the question a contested decision
actually raises.

Nesting: a ``governed_request`` opened inside an active one reuses the
parent correlation id and sequence counter and records a child span
rather than minting a new run. Only the root wrapper opens the run
record and writes the terminal record.
"""

from __future__ import annotations

import threading
import uuid
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any

import uuid6

from .audit import AuditStore
from .events import EventType, GovernedEvent
from .metadata import ExecutionMetadata, capture_execution_metadata, utcnow

_current_context: ContextVar[GovernedContext | None] = ContextVar(
    "arcaai_governed_context", default=None
)


class GovernedContext:
    """Handle passed to everything running inside the wrapper.

    Nodes call ``emit``/``emit_ref``; they do not know about tables,
    sessions or transactions (spec section 6). Deliberately narrow:
    three methods is the whole surface.
    """

    def __init__(
        self,
        *,
        store: AuditStore,
        correlation_id: uuid.UUID,
        metadata: ExecutionMetadata,
        span_id: uuid.UUID,
        parent_span_id: uuid.UUID | None,
        _counter: _SequenceCounter,
    ) -> None:
        self._store = store
        self._correlation_id = correlation_id
        self._metadata = metadata
        self._span_id = span_id
        self._parent_span_id = parent_span_id
        self._counter = _counter
        self._failure: tuple[str, str | None] | None = None

    # -- read-only views ---------------------------------------------------

    @property
    def correlation_id(self) -> uuid.UUID:
        return self._correlation_id

    @property
    def metadata(self) -> ExecutionMetadata:
        """Captured once at root entry; frozen (spec section 4)."""
        return self._metadata

    # -- the emit contract -------------------------------------------------

    def emit(self, event: GovernedEvent, *, actor: str | None = None) -> int:
        """Record a typed event. Free-form dicts are rejected by signature:
        the argument must be a ``GovernedEvent`` subclass instance
        (allowlist by construction, spec section 6.1)."""
        if not isinstance(event, GovernedEvent):
            raise TypeError(
                "emit takes a typed GovernedEvent, not "
                f"{type(event).__name__}; free-form payloads have nowhere "
                "to go by design (RAT-02 spec section 6.1)."
            )
        seq = self._counter.next()
        self._store.record_event(
            correlation_id=self._correlation_id,
            sequence_number=seq,
            event_type=event.event_type.value,
            actor=actor,
            span_id=self._span_id,
            parent_span_id=self._parent_span_id,
            payload=event.model_dump(mode="json"),
            payload_ref=None,
        )
        return seq

    def emit_ref(
        self, event_type: str | EventType, *, text: str, actor: str | None = None
    ) -> str:
        """The only route for text that may contain personal data.

        Stores ``text`` content-addressed in ``audit_payload``; the event
        row carries the hash and byte length, never the text
        (spec sections 5.1, 6.1). Returns the sha256 so callers can
        cross-reference (e.g. ``LlmInvoked.prompt_sha256``).
        """
        etype = EventType(event_type)
        digest = self._store.store_payload(text)
        seq = self._counter.next()
        self._store.record_event(
            correlation_id=self._correlation_id,
            sequence_number=seq,
            event_type=etype.value,
            actor=actor,
            span_id=self._span_id,
            parent_span_id=self._parent_span_id,
            payload={
                "payload_sha256": digest,
                "byte_length": len(text.encode("utf-8")),
            },
            payload_ref=digest,
        )
        return digest

    # -- handled failure ---------------------------------------------------

    def mark_failed(self, error_type: str, error_message: str | None = None) -> None:
        """Declare a handled failure: the run terminates ``failed`` on a
        normal exit instead of ``completed``. Root context only."""
        self._failure = (error_type, error_message)


class _SequenceCounter:
    """Monotonic per-run counter owned by the root wrapper (spec section 5).

    Thread-locked: LangGraph nodes may emit from worker threads, and a
    gap or duplicate in the sequence breaks B9 replay determinism.
    """

    def __init__(self) -> None:
        self._value = 0
        self._lock = threading.Lock()

    def next(self) -> int:
        with self._lock:
            self._value += 1
            return self._value


def current_governed_context() -> GovernedContext | None:
    """The active context, if any — how LangGraph nodes reach ``ctx``
    when it is not threaded through state explicitly."""
    return _current_context.get()


@contextmanager
def governed_request(
    store: AuditStore,
    *,
    subject_ref: str | None = None,
    source: str | None = None,
    model_artifacts: Mapping[str, Any] | None = None,
    llm_pin: str | None = None,
    prompt_version: str | None = None,
    corpus_version: str | None = None,
    retrieval_config: Mapping[str, Any] | None = None,
    metadata_extra: Mapping[str, Any] | None = None,
    _environ: Mapping[str, str] | None = None,
) -> Iterator[GovernedContext]:
    """Wrap a governed inbound request — FastAPI, batch job, or test harness.

    Root invocation: mints a UUIDv7 correlation id (time-ordered, so
    records sort naturally without a separate timestamp index), captures
    execution metadata once, opens the run record before any work
    happens, and guarantees a terminal record on every exit path.

    Nested invocation: reuses the parent correlation id, metadata and
    counter; records a child span; writes no run or terminal record.
    """
    parent = _current_context.get()

    if parent is not None:
        # Child span (spec section 3, nesting). subject/source/metadata
        # arguments are ignored: the run's identity was fixed at root.
        child = GovernedContext(
            store=parent._store,
            correlation_id=parent._correlation_id,
            metadata=parent._metadata,
            span_id=uuid6.uuid7(),
            parent_span_id=parent._span_id,
            _counter=parent._counter,
        )
        token = _current_context.set(child)
        try:
            yield child
        finally:
            _current_context.reset(token)
        return

    # Root invocation.
    correlation_id = uuid6.uuid7()
    started_at = utcnow()
    metadata = capture_execution_metadata(
        model_artifacts=model_artifacts,
        llm_pin=llm_pin,
        prompt_version=prompt_version,
        corpus_version=corpus_version,
        retrieval_config=retrieval_config,
        environ=_environ,
    )
    ctx = GovernedContext(
        store=store,
        correlation_id=correlation_id,
        metadata=metadata,
        span_id=uuid6.uuid7(),
        parent_span_id=None,
        _counter=_SequenceCounter(),
    )

    # Open the run record before any work happens (spec section 3.3).
    store.open_run(
        correlation_id=correlation_id,
        started_at=started_at,
        metadata=metadata,
        subject_ref=subject_ref,
        source=source,
        metadata_extra=metadata_extra,
    )

    token = _current_context.set(ctx)
    outcome = "completed"
    error_type: str | None = None
    error_message: str | None = None
    try:
        yield ctx
        if ctx._failure is not None:
            outcome = "failed"
            error_type, error_message = ctx._failure
    except BaseException as exc:
        outcome = "aborted"
        error_type = type(exc).__name__
        # Message only, never the traceback (spec section 3.4).
        error_message = str(exc) or None
        raise
    finally:
        _current_context.reset(token)
        store.close_run(
            correlation_id=correlation_id,
            started_at=started_at,
            outcome=outcome,
            error_type=error_type,
            error_message=error_message,
        )
