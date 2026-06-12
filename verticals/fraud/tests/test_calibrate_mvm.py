"""Platt calibration tests (B4 increment 3 — G7).

CI-scale (seed-7 SMALL_CFG). Enforced here:

- Mask discipline: the Platt fit consumes only cal rows whose labels are
  confirmed at the cal-end cut (anti-leakage rule 3 binds fits, per A4).
- A1 definition: equal-frequency binning is genuinely equal-frequency,
  and the MAE arithmetic matches a hand-computed case exactly.
- Monotonicity: Platt is rank-preserving, so ROC-AUC is unchanged and
  the budget metrics from increment 2 stand untouched.
- R10: probabilities are independent per row — batch composition cannot
  change any row's value; no sum-to-one anywhere.
- The point of the exercise: calibrated MAE beats uncalibrated MAE (the
  scale_pos_weight inflation is corrected), probabilities stay valid.
- Report contract: scaler params, reliability table, audit, G7 verdict.

No MLflow server required (env-gated logging, never set here).
"""

from __future__ import annotations

import numpy as np
import pytest

from verticals.fraud.features.feature_pipeline import (
    FEATURES,
    build_features,
    chronological_split,
)
from verticals.fraud.synthetic.generator import generate
from verticals.fraud.tests.test_leakage import SMALL_CFG
from verticals.fraud.training.calibrate_mvm import (
    N_BINS,
    apply_platt,
    calibrate,
    calibration_mae,
    equal_frequency_bins,
    fit_platt,
    masked_cal_frame,
)
from verticals.fraud.training.train_mvm import fit


@pytest.fixture(scope="module")
def splits():
    txns, _, _, _ = generate(SMALL_CFG)
    feat = build_features(txns)
    return chronological_split(feat)


@pytest.fixture(scope="module")
def model(splits):
    train, _, _ = splits
    m, _ = fit(train)
    return m


@pytest.fixture(scope="module")
def report(model, splits):
    _, cal, test = splits
    return calibrate(model, cal, test)


def test_platt_fits_on_masked_cal_only(splits) -> None:
    _, cal, _ = splits
    masked, audit = masked_cal_frame(cal)
    as_of = cal["timestamp"].max()
    # Everything the fit can see is genuinely confirmed by the cut...
    assert (masked["label_available_date"] <= as_of).all()
    # ...and a real share near the cut was excluded (labels lag events).
    assert audit["rows_excluded_unconfirmed_label"] > 0
    assert audit["cal_rows_masked"] + audit[
        "rows_excluded_unconfirmed_label"] == audit["cal_rows_raw"]


def test_a1_binning_and_mae_arithmetic() -> None:
    """The A1 definition, checked against a hand-computed case."""
    # Equal-frequency property: bin sizes differ by at most one row,
    # even with heavy ties (the realistic fraud-score shape).
    p = np.concatenate([np.zeros(95), np.linspace(0.5, 1.0, 25)])
    bins = equal_frequency_bins(p, N_BINS)
    sizes = [len(b) for b in bins]
    assert len(bins) == N_BINS
    assert sum(sizes) == len(p)
    assert max(sizes) - min(sizes) <= 1
    # Hand-computed MAE: 20 rows, 2 bins. Low bin predicts 0.1, observes
    # 0.0 (gap 0.1); high bin predicts 0.8, observes 0.6 (gap 0.2).
    # Unweighted mean = 0.15.
    p2 = np.array([0.1] * 10 + [0.8] * 10)
    y2 = np.array([0] * 10 + [1, 1, 1, 1, 1, 1, 0, 0, 0, 0])
    mae, table = calibration_mae(y2, p2, n_bins=2)
    assert mae == pytest.approx(0.15, abs=1e-9)
    assert [row["n"] for row in table] == [10, 10]


def test_calibration_is_monotone_rank_preserving(report) -> None:
    """Platt must not move the ranking: ROC-AUC unchanged, so the R8/R9
    numbers recorded at increment 2 stand."""
    assert report["roc_auc_calibrated"] == pytest.approx(
        report["roc_auc_uncalibrated"], abs=1e-6)
    assert report["r10_independence"]["monotone_in_margin"]


def test_r10_independence_no_normalisation(model, splits) -> None:
    """A row's probability depends on its score alone — never the batch."""
    _, cal, test = splits
    cal_masked, _ = masked_cal_frame(cal)
    margins_cal = model.predict(cal_masked[FEATURES], output_margin=True)
    scaler = fit_platt(margins_cal, cal_masked["is_fraud"].to_numpy())
    margins = model.predict(test[FEATURES], output_margin=True)
    p_full = apply_platt(scaler, margins)
    # Same rows in a different batch: identical values.
    half = apply_platt(scaler, margins[: len(margins) // 2])
    np.testing.assert_array_equal(half, p_full[: len(margins) // 2])
    # A batch of one: identical value.
    np.testing.assert_array_equal(apply_platt(scaler, margins[:1]),
                                  p_full[:1])
    # No sum-to-one: total probability mass is whatever it is.
    assert p_full.sum() != pytest.approx(1.0)


def test_calibration_improves_mae(report) -> None:
    """The reason inc3 exists: scale_pos_weight inflates raw probabilities;
    Platt must bring the MAE down, with valid probabilities throughout."""
    assert report["calibration_mae"] < report["calibration_mae_uncalibrated"]
    for row in report["reliability_table"]:
        assert 0.0 <= row["mean_predicted"] <= 1.0


def test_report_contract(report) -> None:
    for key in ("model", "gate", "scaler", "calibration_audit",
                "calibration_mae", "calibration_mae_uncalibrated",
                "reliability_table", "r10_independence", "g7"):
        assert key in report, f"report missing {key}"
    assert report["model"] == "xgb_mvm_platt"
    assert report["gate"] == "G7"
    assert set(report["scaler"]) == {"a", "b"}
    assert len(report["reliability_table"]) == N_BINS
    assert report["r10_independence"]["pass"]
    assert set(report["g7"]) == {"gate_mae_lt_0.05",
                                 "improved_vs_uncalibrated"}
    # MAE arithmetic is internally consistent with its own table.
    gaps = [row["abs_gap"] for row in report["reliability_table"]]
    assert report["calibration_mae"] == pytest.approx(
        float(np.mean(gaps)), abs=1e-4)
