"""Internal fraud scoring route (B5 inc2).

Mounted under /internal per Blueprint S16.1 (single agent entry point):
the only public route family is /v1/query/* via the agent (B6). This route
has no public ingress — it is agent-side plumbing, and the /internal
prefix encodes that intent in the path itself. Ingress config enforces it
at deployment, exactly as the no-public-ingress rule for the BentoML
endpoint is enforced.

Platform boundary (ADR-0009, D-05..D-08): this module imports only from
contracts/. The fraud vertical's scorer is attached through the
get_scoring_backend dependency — the lazy import inside its default is the
single sanctioned crossing of the contract boundary, at the composition
seam, and tests override it with a stub.
"""

from __future__ import annotations

from typing import Annotated, Protocol

from fastapi import APIRouter, Depends

from api.schemas.fraud_scoring import FraudScoreRequest, FraudScoreResponse

router = APIRouter(prefix="/internal/v1/fraud", tags=["fraud-internal"])


class ScoringBackend(Protocol):
    """Anything that scores over the contract. The BentoML service and the
    in-process scorer both satisfy this shape."""

    def score(self, request: FraudScoreRequest) -> FraudScoreResponse: ...


_backend: ScoringBackend | None = None


def get_scoring_backend() -> ScoringBackend:
    """Default backend: the DVC-pinned in-process scorer, loaded once.

    The vertical import lives here — not at module top — so importing the
    API package never drags ML dependencies with it. Tests override this
    dependency via app.dependency_overrides.
    """
    global _backend
    if _backend is None:
        from verticals.fraud.serving.scorer import FraudScorer

        _backend = FraudScorer.from_pinned_artifacts()
    return _backend


@router.post("/score", response_model=FraudScoreResponse)
def score(
    request: FraudScoreRequest,
   backend: Annotated[ScoringBackend, Depends(get_scoring_backend)],
) -> FraudScoreResponse:
    """Score one transaction over the contract. Echoes transaction_id;
    response carries full model provenance (artefact hash + Platt params)."""
    return backend.score(request)
