"""Serving tests (B5 inc1) — contract, parity, latency.

CI-scale (SMALL_CFG, no MLflow, no pinned artefacts): generate small data,
fit a model and Platt scaler exactly as B4 does, build a FraudScorer from
those in-memory objects, and verify:

- Contract: the request schema is the 12 FEATURES in the canonical order,
  unknown fields are rejected, flag ranges are enforced; the response
  carries a calibrated probability in [0, 1] and full provenance.
- Parity: the serving path reproduces calibrate_mvm's calibrated
  probabilities byte-for-byte (margin -> sigmoid(a*margin + b)), and a
  single-row request equals its in-batch value (R10 independence + proof
  the request->frame->score path matches the batch path).
- Latency (G9 sanity): single-row scoring is comfortably under the 200ms
  SLA. The authoritative G9 measurement is on the pinned model on reference
  hardware, recorded in the B5 gate doc.
"""

from __future__ import annotations

import time

import numpy as np
import pytest
from pydantic import ValidationError

from contracts.fraud_scoring import (
    CONTRACT_FEATURES,
    FraudScoreRequest,
    FraudScoreResponse,
)
from verticals.fraud.features.feature_pipeline import (
    FEATURES,
    build_features,
    chronological_split,
)
from verticals.fraud.serving.scorer import FraudScorer
from verticals.fraud.synthetic.generator import generate
from verticals.fraud.tests.test_leakage import SMALL_CFG
from verticals.fraud.training.calibrate_mvm import (
    apply_platt,
    fit_platt,
    masked_cal_frame,
)
from verticals.fraud.training.train_mvm import fit


def _request_from_row(row) -> FraudScoreRequest:
    # .item() -> native Python scalar so Pydantic sees int/float, not numpy.
    return FraudScoreRequest(**{f: row[f].item() for f in CONTRACT_FEATURES})


@pytest.fixture(scope="module")
def splits():
    txns, _, _, _ = generate(SMALL_CFG)
    feat = build_features(txns)
    return chronological_split(feat)


@pytest.fixture(scope="module")
def scorer_and_offline(splits):
    train, cal, test = splits
    model, _ = fit(train)
    cal_masked, _ = masked_cal_frame(cal)
    margins_cal = model.predict(cal_masked[FEATURES], output_margin=True)
    scaler = fit_platt(margins_cal, cal_masked["is_fraud"].to_numpy())
    # Offline calibrated probabilities on test — the reference the serving
    # path must reproduce exactly.
    margins_test = model.predict(test[FEATURES], output_margin=True)
    offline = apply_platt(scaler, margins_test)
    return FraudScorer(model, scaler), offline, test


# --- contract --------------------------------------------------------------

def test_contract_features_match_model() -> None:
    """The contract's feature list is exactly the model's, in order."""
    assert tuple(FEATURES) == CONTRACT_FEATURES
    declared = tuple(f for f in FraudScoreRequest.model_fields if f != "transaction_id")
    assert declared == CONTRACT_FEATURES


def test_request_rejects_unknown_field() -> None:
    payload = {f: 0 for f in CONTRACT_FEATURES}
    payload["category_risk"] = 0.5
    payload["surprise"] = 1
    with pytest.raises(ValidationError):
        FraudScoreRequest(**payload)


def test_request_enforces_flag_range() -> None:
    payload = {f: 0 for f in CONTRACT_FEATURES}
    payload["category_risk"] = 0.5
    payload["is_night"] = 2  # flag must be 0 or 1
    with pytest.raises(ValidationError):
        FraudScoreRequest(**payload)


# --- parity ----------------------------------------------------------------

def test_serving_matches_offline_calibration(scorer_and_offline) -> None:
    """Batch path is byte-identical to calibrate_mvm's calibrated probs."""
    scorer, offline, test = scorer_and_offline
    served = scorer.calibrated_proba(test)
    np.testing.assert_array_equal(served, offline)


def test_single_request_equals_in_batch_value(scorer_and_offline) -> None:
    """A row scored alone equals its batch value (R10), and the
    request->frame->score path matches the batch path exactly."""
    scorer, offline, test = scorer_and_offline
    for i in (0, len(test) // 2, len(test) - 1):
        resp = scorer.score(_request_from_row(test.iloc[i]))
        assert isinstance(resp, FraudScoreResponse)
        assert resp.calibrated_fraud_probability == float(offline[i])


def test_response_provenance_complete(scorer_and_offline) -> None:
    scorer, _, test = scorer_and_offline
    resp = scorer.score(_request_from_row(test.iloc[0]))
    prov = resp.provenance
    assert prov.schema_version
    assert prov.artifact_name == "xgb_mvm.ubj"
    assert (prov.platt_a, prov.platt_b) == (scorer.scaler["a"], scorer.scaler["b"])
    assert 0.0 <= resp.calibrated_fraud_probability <= 1.0


# --- latency (G9 sanity) ---------------------------------------------------

def test_single_score_latency(scorer_and_offline) -> None:
    scorer, _, test = scorer_and_offline
    req = _request_from_row(test.iloc[0])
    scorer.score(req)  # warm
    times = []
    for _ in range(50):
        t0 = time.perf_counter()
        scorer.score(req)
        times.append((time.perf_counter() - t0) * 1000.0)
    median_ms = float(np.median(times))
    # Generous CI sanity bound; authoritative G9 (<200ms P99 on the pinned
    # model / reference hardware) is recorded in the B5 gate doc.
    assert median_ms < 100.0, f"median single-score latency {median_ms:.1f}ms"
