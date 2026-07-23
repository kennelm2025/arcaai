"""B6 increment 3: fraud-scoring node - calls the B5 BentoML service.

Agent -> intelligence layer over HTTP, per the architecture's layer
separation and the ADR-0009 boundary: this module imports contract types
only, never verticals.fraud. The service URL is configurable so the same
node works against local dev (bentoml serve) and any future deployment.
"""
from __future__ import annotations

import os

import httpx

from contracts.fraud_scoring import FraudScoreRequest, FraudScoreResponse

SCORING_URL = os.environ.get("ARCAAI_FRAUD_SCORING_URL", "http://localhost:3000")
_TIMEOUT = 5.0  # seconds; generous vs the G9 P99 of ~33ms


def score_transaction(request: FraudScoreRequest) -> FraudScoreResponse:
    """One scoring call over the contract. Raises on non-2xx (fail loud)."""
    resp = httpx.post(
        f"{SCORING_URL}/score",
        json={"request": request.model_dump()},
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    return FraudScoreResponse.model_validate(resp.json())


def score_node(state: dict) -> dict:
    """LangGraph node: validates state['transaction'] against the contract,
    scores it, and returns score + provenance into state."""
    request = FraudScoreRequest.model_validate(state["transaction"])
    response = score_transaction(request)
    return {
        "score": response.calibrated_fraud_probability,
        "provenance": response.provenance.model_dump(),
    }
