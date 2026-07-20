"""Fraud scoring endpoint schemas (B5 inc2).

Thin re-export of the contract models — contracts/fraud_scoring.py is the
single source of truth (contract-first, Build & Quality Plan B5). Nothing
is redefined here; the contract test asserts these names ARE the contract
objects (identity, not copies), so the API surface cannot drift.
"""

from contracts.fraud_scoring import (
    CONTRACT_FEATURES,
    SCHEMA_VERSION,
    FraudScoreRequest,
    FraudScoreResponse,
    ModelProvenance,
)

__all__ = [
    "CONTRACT_FEATURES",
    "SCHEMA_VERSION",
    "FraudScoreRequest",
    "FraudScoreResponse",
    "ModelProvenance",
]
