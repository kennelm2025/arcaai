"""B6 increment 3: score-node tests.

Structural tests run everywhere (CI-safe). Integration tests require the
B5 BentoML service (bentoml serve ...FraudScoringService) and self-skip
when it is absent - same local/CI split as the LLM smoke tests.
"""
import httpx
import pytest
from pydantic import ValidationError

from agent.graph import build_graph
from agent.scoring import SCORING_URL

FRAUDY_TXN = {
    "transaction_id": "inc3-test-001",
    "txn_count_1h": 2,
    "txn_count_24h": 9,
    "txn_count_7d": 41,
    "amount_sum_24h": 640.0,
    "amount_zscore": 3.1,
    "mins_since_last_txn": 4.0,
    "device_novelty": 1,
    "category_shift": 1,
    "category_risk": 0.8,
    "is_night": 1,
    "is_international": 1,
    "log_amount": 6.4,
}

def _service_available() -> bool:
    try:
        return httpx.get(f"{SCORING_URL}/healthz", timeout=2.0).status_code < 500
    except Exception:
        return False


needs_service = pytest.mark.skipif(
    not _service_available(), reason="B5 scoring service not reachable (expected in CI)"
)


def test_default_graph_still_uses_stub():
    result = build_graph().invoke({"query": "assess", "transaction": FRAUDY_TXN})
    assert result["score"] == -1.0  # sentinel: stub, not a real probability


def test_bad_transaction_rejected_before_any_network_call():
    with pytest.raises(ValidationError):
        build_graph(live_scoring=True).invoke(
            {"query": "assess", "transaction": {"nonsense": True}}
        )

@needs_service
def test_live_scoring_end_to_end():
    result = build_graph(live_scoring=True).invoke(
        {"query": "assess", "transaction": FRAUDY_TXN}
    )
    assert 0.0 <= result["score"] <= 1.0
    assert result["score"] > 0.5  # deliberately fraud-flavoured vector
    assert result["provenance"]["artifact_name"] == "xgb_mvm.ubj"
    assert result["provenance"]["schema_version"] == "fraud-scoring/1.0.0"


@needs_service
def test_provenance_carries_platt_params():
    result = build_graph(live_scoring=True).invoke(
        {"query": "assess", "transaction": FRAUDY_TXN}
    )
    prov = result["provenance"]
    assert "platt_a" in prov and "platt_b" in prov
    assert "artifact_sha256" in prov and len(prov["artifact_sha256"]) == 64
