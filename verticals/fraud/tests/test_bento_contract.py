"""Bento-side contract test (B5 inc2) — ci-mlops half of the cross-side
API<->BentoML contract pair (the ci-devops half is
api/tests/test_api_contract.py).

inc1's test_serving.py exercises FraudScorer but never imports
bento_service; this closes that gap by asserting the Bento service
registers score as an API endpoint whose signature resolves to the
contract models.

Two wrinkles, both empirically verified against the 1.2+ SDK:
- @bentoml.service replaces the class with a Service wrapper, so the
  original function is reached through the service's ``apis`` registry —
  which also makes this assert endpoint registration, not just method
  shape.
- bento_service.py uses ``from __future__ import annotations`` (PEP 563),
  so raw ``__annotations__`` are strings; ``typing.get_type_hints``
  resolves them to the actual contract classes.
"""

from __future__ import annotations

import typing

from contracts.fraud_scoring import FraudScoreRequest, FraudScoreResponse
from verticals.fraud.serving.bento_service import FraudScoringService


def test_bento_score_is_a_registered_api_on_the_contract() -> None:
    assert "score" in FraudScoringService.apis
    func = FraudScoringService.apis["score"].func
    hints = typing.get_type_hints(func)
    assert hints["request"] is FraudScoreRequest
    assert hints["return"] is FraudScoreResponse
