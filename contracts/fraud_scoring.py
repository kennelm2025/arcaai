"""Fraud scoring contract — the request/response schema for B5 serving.

Contract-first per the Build & Quality Plan (B5): this module is the single
source of truth for the scoring interface. The BentoML service (inc1) and
the FastAPI layer (inc2) both import these models, and the contract test
verifies each side against them.

Request carries exactly the 12 MVM features (FEATURES.md, B3) in the
contract order, plus an optional ``transaction_id`` for audit correlation
only — it is echoed back, never a model input. Response carries the
calibrated fraud probability and the provenance needed to reproduce the
score: the served model artefact's content hash and the Platt parameters
that mapped its margin.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

SCHEMA_VERSION = "fraud-scoring/1.0.0"

# The 12 MVM features, in the contract order (FEATURES.md). The serving
# scorer pulls the canonical list from feature_pipeline.FEATURES; the
# contract test asserts the two are identical so they cannot drift.
CONTRACT_FEATURES: tuple[str, ...] = (
    "txn_count_1h",
    "txn_count_24h",
    "txn_count_7d",
    "amount_sum_24h",
    "amount_zscore",
    "mins_since_last_txn",
    "device_novelty",
    "category_shift",
    "category_risk",
    "is_night",
    "is_international",
    "log_amount",
)


class FraudScoreRequest(BaseModel):
    """The 12-feature MVM vector. Unknown fields are rejected — the contract
    is strict, so a caller cannot silently send the wrong shape."""

    model_config = ConfigDict(extra="forbid")

    transaction_id: str | None = Field(
        default=None,
        description="Audit correlation id. Echoed back; never a model input.",
    )

    txn_count_1h: int = Field(ge=0, description="Customer txn count in [t-1h, t)")
    txn_count_24h: int = Field(ge=0, description="Count in prior 24h")
    txn_count_7d: int = Field(ge=0, description="Count in prior 7 days")
    amount_sum_24h: float = Field(ge=0.0, description="Sum of amounts in prior 24h")
    amount_zscore: float = Field(description="Amount vs customer's own history")
    mins_since_last_txn: float = Field(ge=0.0, description="Minutes since previous txn")
    device_novelty: int = Field(ge=0, le=1, description="1 if device unseen in prior txns")
    category_shift: int = Field(ge=0, le=1, description="1 if merchant category new for customer")
    category_risk: float = Field(ge=0.0, le=1.0, description="Static MCC-style risk weight")
    is_night: int = Field(ge=0, le=1, description="1 if hour < 06:00")
    is_international: int = Field(ge=0, le=1, description="Passthrough of txn flag")
    log_amount: float = Field(ge=0.0, description="log1p(amount)")


class ModelProvenance(BaseModel):
    """Everything needed to reproduce a score: the exact model bytes (by
    hash) and the calibration that mapped its margin to a probability."""

    schema_version: str
    artifact_name: str = Field(description="e.g. xgb_mvm.ubj")
    artifact_sha256: str = Field(description="sha256 of the served model artefact")
    platt_a: float
    platt_b: float


class FraudScoreResponse(BaseModel):
    transaction_id: str | None = None
    calibrated_fraud_probability: float = Field(ge=0.0, le=1.0)
    provenance: ModelProvenance
