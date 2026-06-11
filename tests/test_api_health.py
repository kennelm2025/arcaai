"""API health/version endpoint tests (httpx test client, Blueprint S9.1)."""

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health_returns_ok() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_version_reports_service_identity() -> None:
    r = client.get("/version")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "arcaai-api"
    assert body["version"]
