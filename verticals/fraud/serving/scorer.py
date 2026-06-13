"""Fraud scorer — loads the B4 calibrated model and reproduces its scoring
path for serving (B5 inc1).

Scoring composition is identical to ``calibrate_mvm.py``: the XGBoost raw
margin is mapped through the Platt scaler, ``p = sigmoid(a*margin + b)``.
This module deliberately does NOT import ``calibrate_mvm`` — a serving unit
must not drag the trainer with it into a Bento — so the two-line map is
re-stated here, and the parity test (``test_serving.py``) is what guarantees
it stays byte-identical to the offline pipeline.

Model source is the DVC-pinned B4 artefacts, not MLflow: B4 logs the model
to MLflow only as a loose run artefact (no Model Registry), so the
reproducible source of truth is the DVC outputs:
    data/fraud/models/xgb_mvm.ubj        - XGBoost booster
    data/fraud/models/platt_scaler.json  - {a, b}
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb

from contracts.fraud_scoring import (
    SCHEMA_VERSION,
    FraudScoreRequest,
    FraudScoreResponse,
    ModelProvenance,
)
from verticals.fraud.features.feature_pipeline import FEATURES

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATA_DIR = REPO_ROOT / "data" / "fraud"


def _sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-z))


class FraudScorer:
    """Calibrated fraud scorer: XGBoost margin -> Platt -> probability."""

    def __init__(
        self,
        model: xgb.XGBClassifier,
        scaler: dict,
        *,
        artifact_name: str = "xgb_mvm.ubj",
        artifact_sha256: str = "in-memory",
    ) -> None:
        if set(scaler) != {"a", "b"}:
            raise ValueError(f"scaler must have keys {{'a','b'}}, got {set(scaler)}")
        self.model = model
        self.scaler = {"a": float(scaler["a"]), "b": float(scaler["b"])}
        self.artifact_name = artifact_name
        self.artifact_sha256 = artifact_sha256

    @classmethod
    def from_pinned_artifacts(cls, data_dir: Path | None = None) -> "FraudScorer":
        """Load the DVC-pinned B4 model + Platt scaler. Hashes the model
        bytes so the served artefact is identifiable in the response."""
        base = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
        model_path = base / "models" / "xgb_mvm.ubj"
        scaler_path = base / "models" / "platt_scaler.json"
        if not model_path.exists():
            raise FileNotFoundError(
                f"{model_path} not found — pull the DVC-pinned B4 artefacts "
                "(dvc pull / dvc repro) before serving."
            )
        if not scaler_path.exists():
            raise FileNotFoundError(
                f"{scaler_path} not found — pull the DVC-pinned B4 artefacts."
            )
        model = xgb.XGBClassifier()
        model.load_model(model_path)
        scaler = json.loads(scaler_path.read_text(encoding="utf-8"))
        sha = hashlib.sha256(model_path.read_bytes()).hexdigest()
        return cls(model, scaler, artifact_name=model_path.name, artifact_sha256=sha)

    def calibrated_proba(self, frame: pd.DataFrame) -> np.ndarray:
        """Calibrated fraud probability per row. Row-wise monotone map; no
        batch statistics, no normalisation (R10)."""
        margins = self.model.predict(frame[list(FEATURES)], output_margin=True)
        return _sigmoid(self.scaler["a"] * margins + self.scaler["b"])

    def _provenance(self) -> ModelProvenance:
        return ModelProvenance(
            schema_version=SCHEMA_VERSION,
            artifact_name=self.artifact_name,
            artifact_sha256=self.artifact_sha256,
            platt_a=self.scaler["a"],
            platt_b=self.scaler["b"],
        )

    def score(self, request: FraudScoreRequest) -> FraudScoreResponse:
        row = {f: getattr(request, f) for f in FEATURES}
        frame = pd.DataFrame([row], columns=list(FEATURES))
        p = float(self.calibrated_proba(frame)[0])
        return FraudScoreResponse(
            transaction_id=request.transaction_id,
            calibrated_fraud_probability=p,
            provenance=self._provenance(),
        )
