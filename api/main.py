"""ArcaAI API entry point.

B1 scope was health and version only. B5 inc2 adds the internal fraud
scoring route (no public ingress — Blueprint S16.1; see
api/routers/fraud.py). The public /v1/query endpoint arrives in B6 behind
the agent (single-agent-entry rule, Blueprint S16.1).
"""

from fastapi import FastAPI

from api.routers.fraud import router as fraud_router
from api.schemas.fraud_scoring import SCHEMA_VERSION
from api.version import VERSION

app = FastAPI(
    title="ArcaAI",
    description="The AI control layer for regulated banking decisions - reference implementation",
    version=VERSION,
)

app.include_router(fraud_router)


@app.get("/health")
def health() -> dict:
    """Liveness probe - used by docker-compose healthcheck and, later, Kubernetes."""
    return {"status": "ok"}


@app.get("/version")
def version() -> dict:
    """Build identity. Model/calibrator versions are per-response provenance
    (see FraudScoreResponse); the contract schema version is static and
    belongs here."""
    return {
        "service": "arcaai-api",
        "version": VERSION,
        "fraud_scoring_schema": SCHEMA_VERSION,
    }
