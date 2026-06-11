"""ArcaAI API entry point.

B1 scope: health and version endpoints only. The /v1/query endpoint
arrives in B5/B6 behind the agent (single-agent-entry rule, Blueprint S16.1).
"""

from fastapi import FastAPI

from api.version import VERSION

app = FastAPI(
    title="ArcaAI",
    description="The AI control layer for regulated banking decisions - reference implementation",
    version=VERSION,
)


@app.get("/health")
def health() -> dict:
    """Liveness probe - used by docker-compose healthcheck and, later, Kubernetes."""
    return {"status": "ok"}


@app.get("/version")
def version() -> dict:
    """Build identity. Model/calibrator versions join this payload from B5."""
    return {"service": "arcaai-api", "version": VERSION}
