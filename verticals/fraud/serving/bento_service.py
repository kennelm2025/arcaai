"""BentoML serving for the fraud MVM (B5 inc1).

Thin wrapper over ``FraudScorer``: loads the DVC-pinned B4 calibrated model
at startup and exposes a single typed ``/score`` endpoint over the contract.
BentoML 1.2+ service API.

Run locally:
    bentoml serve verticals.fraud.serving.bento_service:FraudScoringService
"""

from __future__ import annotations

import bentoml

from contracts.fraud_scoring import FraudScoreRequest, FraudScoreResponse
from verticals.fraud.serving.scorer import FraudScorer


@bentoml.service
class FraudScoringService:
    def __init__(self) -> None:
        # Loaded once at service startup, not per request.
        self.scorer = FraudScorer.from_pinned_artifacts()

    @bentoml.api
    def score(self, request: FraudScoreRequest) -> FraudScoreResponse:
        return self.scorer.score(request)
