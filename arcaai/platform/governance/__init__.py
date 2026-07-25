"""ArcaAI platform governance trio (RAT-02 / ADR-0010).

Request wrapper, execution metadata, audit logging. Platform-side per
ADR-0009: nothing in this package imports from ``verticals/`` — the
boundary test in the suite is mandatory CF-1 evidence at B7.

Public surface — deliberately narrow (spec section 6):

* :func:`governed_request` — the context manager
* :class:`GovernedContext` — ``emit`` / ``emit_ref`` / ``metadata``
* the typed event models in :mod:`.events`
* :class:`AuditStore` — construction/wiring only; verticals never call it
"""

from .audit import AuditStore
from .events import (
    SCHEMA_VERSION,
    ErrorRaised,
    EventType,
    FeatureComputed,
    GovernedEvent,
    GuardrailEvaluated,
    LlmInvoked,
    ModelScored,
    RequestReceived,
    ResponseEmitted,
    RetrievalPerformed,
)
from .metadata import ExecutionMetadata, capture_execution_metadata
from .wrapper import GovernedContext, current_governed_context, governed_request

__all__ = [
    "SCHEMA_VERSION",
    "AuditStore",
    "ErrorRaised",
    "EventType",
    "ExecutionMetadata",
    "FeatureComputed",
    "GovernedContext",
    "GovernedEvent",
    "GuardrailEvaluated",
    "LlmInvoked",
    "ModelScored",
    "RequestReceived",
    "ResponseEmitted",
    "RetrievalPerformed",
    "capture_execution_metadata",
    "current_governed_context",
    "governed_request",
]
