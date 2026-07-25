"""Typed governance events — the emit contract (RAT-02 spec section 6.1/6.2).

Public contract: ``SCHEMA_VERSION`` and ``EventType`` are depended on by
B9 replay and B11 panels. Adding an event type is a minor version bump
recorded in ADR-0010's evidence trail; removing or renaming one, or
changing the meaning or type of an existing payload field, is a breaking
change requiring a DEC or ADR plus a migration note (spec section 6.2).

Allowlist by construction: ``emit`` accepts only subclasses of
``GovernedEvent``. Fields are declared, typed and closed
(``extra="forbid"``) — a caller cannot pass a field that is not in the
schema because there is nowhere to put it. Two backstops against schema
drift, both enforced here rather than at call time:

* a denylist over *field names*, applied when an event model class is
  **defined** — a payload model declaring ``name``, ``account_number``
  etc. raises at import, so the mistake cannot reach a call site;
* a 256-character ceiling on any string payload value — anything longer
  is free text and belongs in ``emit_ref``, which stores by reference.
"""

from __future__ import annotations

import enum
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, model_validator

#: Audit record schema version (RAT-02 spec section 4, section 6.2).
SCHEMA_VERSION = "1.0.0"

#: Ceiling on any string payload field (spec section 6.1). Longer text is
#: free text and must go through ``emit_ref``.
MAX_PAYLOAD_FIELD_CHARS = 256

#: Field names an event payload model may never declare (spec section 6.1).
#: Checked at model-definition time, not call time.
DENYLISTED_FIELD_NAMES = frozenset(
    {
        "name",
        "account_number",
        "sort_code",
        "address",
        "email",
        "postcode",
        "full_name",
    }
)


class EventType(str, enum.Enum):
    """Event types at B7 entry (spec section 6.2). Extensible; see module docstring."""

    REQUEST_RECEIVED = "request_received"
    FEATURE_COMPUTED = "feature_computed"
    MODEL_SCORED = "model_scored"
    RETRIEVAL_PERFORMED = "retrieval_performed"
    LLM_INVOKED = "llm_invoked"
    GUARDRAIL_EVALUATED = "guardrail_evaluated"
    RESPONSE_EMITTED = "response_emitted"
    ERROR_RAISED = "error_raised"


class ProhibitedFieldName(TypeError):
    """An event model declared a denylisted field name (spec section 6.1 backstop)."""


class GovernedEvent(BaseModel):
    """Base class for all emit payloads.

    Frozen (events are records, not workspaces), closed to undeclared
    fields, and string-bounded. Subclasses set ``event_type``.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    #: Set by each concrete subclass; not a payload field.
    event_type: ClassVar[EventType]

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: object) -> None:
        """Definition-time denylist (spec section 6.1): fail at import, not at call."""
        super().__pydantic_init_subclass__(**kwargs)
        bad = DENYLISTED_FIELD_NAMES.intersection(cls.model_fields)
        if bad:
            raise ProhibitedFieldName(
                f"{cls.__name__} declares prohibited payload field(s) "
                f"{sorted(bad)}; personal-data-shaped fields may not enter "
                f"event payloads (RAT-02 spec section 6.1). Free text goes "
                f"through emit_ref."
            )

    @model_validator(mode="after")
    def _enforce_string_ceiling(self) -> GovernedEvent:
        """Runtime backstop (spec section 6.1): free text cannot ride in a payload field."""
        for field_name in type(self).model_fields:
            value = getattr(self, field_name)
            candidates = (
                value if isinstance(value, (list, tuple)) else (value,)
            )
            for item in candidates:
                if isinstance(item, str) and len(item) > MAX_PAYLOAD_FIELD_CHARS:
                    raise ValueError(
                        f"{type(self).__name__}.{field_name} exceeds "
                        f"{MAX_PAYLOAD_FIELD_CHARS} characters; free text "
                        f"belongs in emit_ref, not an event payload "
                        f"(RAT-02 spec section 6.1)."
                    )
        return self


# --------------------------------------------------------------------------
# Concrete event payload models — one per EventType. Field sets are the
# minimum the consuming stage needs (spec section 8); additions are minor
# version bumps per section 6.2.
# --------------------------------------------------------------------------


class RequestReceived(GovernedEvent):
    event_type: ClassVar[EventType] = EventType.REQUEST_RECEIVED

    channel: str | None = None
    request_kind: str | None = None


class FeatureComputed(GovernedEvent):
    event_type: ClassVar[EventType] = EventType.FEATURE_COMPUTED

    feature_set: str
    feature_count: int
    feature_suite_sha256: str | None = None


class ModelScored(GovernedEvent):
    event_type: ClassVar[EventType] = EventType.MODEL_SCORED

    probability: float
    artifact_sha256: str
    platt_a: float | None = None
    platt_b: float | None = None
    threshold: float | None = None
    decision: str | None = None


class RetrievalPerformed(GovernedEvent):
    """B7 consumer: chunk ids + manifest version give eligibility-at-decision."""

    event_type: ClassVar[EventType] = EventType.RETRIEVAL_PERFORMED

    chunk_ids: list[str]
    manifest_version: str
    top_k: int
    score_threshold: float | None = None
    result_count: int | None = None


class LlmInvoked(GovernedEvent):
    """Prompt/response text never appears here — emit_ref only (spec section 5.1)."""

    event_type: ClassVar[EventType] = EventType.LLM_INVOKED

    model_tag: str
    model_digest: str | None = None
    prompt_sha256: str | None = None
    response_sha256: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None


class GuardrailEvaluated(GovernedEvent):
    """B8 consumer: block/redaction reasons and precedence resolution."""

    event_type: ClassVar[EventType] = EventType.GUARDRAIL_EVALUATED

    guardrail: str
    outcome: str
    reason_code: str | None = None
    precedence_rule: str | None = None


class ResponseEmitted(GovernedEvent):
    event_type: ClassVar[EventType] = EventType.RESPONSE_EMITTED

    response_kind: str
    response_sha256: str | None = None


class ErrorRaised(GovernedEvent):
    """Handled-failure marker. Exception message capped at the field
    ceiling by the base validator; tracebacks never enter the record
    (spec section 3.4)."""

    event_type: ClassVar[EventType] = EventType.ERROR_RAISED

    error_type: str
    error_message: str | None = None
    handled: bool = True
