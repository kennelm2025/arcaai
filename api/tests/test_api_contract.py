"""API-side contract test (B5 inc2) — ci-devops half of the cross-side
API<->BentoML contract pair. The ci-mlops half is
verticals/fraud/tests/test_bento_contract.py. Both anchor on
contracts/fraud_scoring.py; contracts/** is in both workflows' paths, so a
contract change runs both sides.

No ML dependencies: the scoring backend is a stub, because this test's job
is the schema surface, not model behaviour (inc1's test_serving.py owns
parity)."""

from __future__ import annotations

from fastapi.testclient import TestClient

import contracts.fraud_scoring as contract
from api.main import app
from api.routers.fraud import get_scoring_backend, router
from api.schemas import fraud_scoring as api_schema

STUB_PROVENANCE = contract.ModelProvenance(
    schema_version=contract.SCHEMA_VERSION,
    artifact_name="stub.ubj",
    artifact_sha256="0" * 64,
    platt_a=1.0,
    platt_b=0.0,
)


class StubBackend:
    """Satisfies ScoringBackend over the contract; no model involved."""

    def score(self, request: contract.FraudScoreRequest) -> contract.FraudScoreResponse:
        return contract.FraudScoreResponse(
            transaction_id=request.transaction_id,
            calibrated_fraud_probability=0.5,
            provenance=STUB_PROVENANCE,
        )


def _payload(**overrides) -> dict:
    base = {f: 0 for f in contract.CONTRACT_FEATURES}
    base["category_risk"] = 0.5
    base.update(overrides)
    return base


# --- schema identity -------------------------------------------------------

def test_api_schemas_are_the_contract() -> None:
    """api/schemas re-exports the contract objects — identity, not copies."""
    assert api_schema.FraudScoreRequest is contract.FraudScoreRequest
    assert api_schema.FraudScoreResponse is contract.FraudScoreResponse
    assert api_schema.ModelProvenance is contract.ModelProvenance
    assert api_schema.SCHEMA_VERSION == contract.SCHEMA_VERSION
    assert api_schema.CONTRACT_FEATURES == contract.CONTRACT_FEATURES


def test_route_is_wired_to_contract_models() -> None:
    """The mounted route's response model IS the contract response model,
    and the route lives under the /internal prefix (Blueprint S16.1)."""
    score_routes = [r for r in router.routes if r.path.endswith("/score")]
    assert len(score_routes) == 1
    route = score_routes[0]
    assert route.path == "/internal/v1/fraud/score"
    assert route.response_model is contract.FraudScoreResponse
    mounted = [r.path for r in app.routes]
    assert "/internal/v1/fraud/score" in mounted


# --- round trip over HTTP --------------------------------------------------

def test_score_round_trip() -> None:
    app.dependency_overrides[get_scoring_backend] = lambda: StubBackend()
    try:
        client = TestClient(app)
        resp = client.post(
            "/internal/v1/fraud/score",
            json=_payload(transaction_id="txn-001"),
        )
        assert resp.status_code == 200
        body = contract.FraudScoreResponse.model_validate(resp.json())
        assert body.transaction_id == "txn-001"
        assert 0.0 <= body.calibrated_fraud_probability <= 1.0
        assert body.provenance.schema_version == contract.SCHEMA_VERSION
    finally:
        app.dependency_overrides.pop(get_scoring_backend, None)


def test_unknown_field_rejected_over_http() -> None:
    """extra='forbid' must survive the HTTP boundary, not just direct
    model construction."""
    app.dependency_overrides[get_scoring_backend] = lambda: StubBackend()
    try:
        client = TestClient(app)
        resp = client.post(
            "/internal/v1/fraud/score",
            json=_payload(surprise=1),
        )
        assert resp.status_code == 422
    finally:
        app.dependency_overrides.pop(get_scoring_backend, None)


def test_version_reports_contract_schema() -> None:
    client = TestClient(app)
    body = client.get("/version").json()
    assert body["fraud_scoring_schema"] == contract.SCHEMA_VERSION
