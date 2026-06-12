"""Walk-forward tests (B4 increment 4 — G5/G7 close).

CI-scale (seed-7 SMALL_CFG, which spans Jan–Dec 2025 — so the test folds
here use late-2025 months; the production FOLD_MONTHS constant targets
Dec 2025 -> May 2026 against the full 17-month dataset). Enforced here:

- Fold construction: test month isolated, training window strictly
  before the calibration slice, calibration slice strictly before the
  cut, windows expand across folds (fold k's training rows are a subset
  of fold k+1's).
- Mask discipline: every row any fit touches (model AND Platt) has its
  label confirmed at the fold cut; test months are evaluated with full
  labels (no mask), per A4.
- Determinism: same data -> identical per-fold metrics.
- Stability read: deltas computed against supplied references; the flag
  arithmetic does what the gate doc says it does.
- Report contract: per-fold keys, scaler params per fold (fold-local
  calibration, not the global inc3 scaler), stability block.

No MLflow server required (env-gated logging, never set here).
"""

from __future__ import annotations

import pytest

from verticals.fraud.features.feature_pipeline import build_features
from verticals.fraud.synthetic.generator import generate
from verticals.fraud.tests.test_leakage import SMALL_CFG
from verticals.fraud.training.walk_forward import (
    ROC_STABILITY_TOL,
    evaluate_folds,
    fold_frames,
    month_bounds,
    run_fold,
)

# SMALL_CFG ends 2025-12-31; three late months exercise the machinery.
CI_FOLD_MONTHS = ("2025-10", "2025-11", "2025-12")


@pytest.fixture(scope="module")
def feat():
    txns, _, _, _ = generate(SMALL_CFG)
    return build_features(txns)


@pytest.fixture(scope="module")
def report(feat):
    refs = {"roc_auc": 0.95, "precision_at_budget": 0.25,
            "calibration_mae": 0.001}
    return evaluate_folds(feat, CI_FOLD_MONTHS, refs)


def test_fold_windows_are_clean_and_expanding(feat) -> None:
    prev_train_max = None
    for month in CI_FOLD_MONTHS:
        cut, end = month_bounds(month)
        train, cal, test, audit = fold_frames(feat, month)
        # Test month isolated; train before cal; cal before the cut.
        assert (test["timestamp"] >= cut).all()
        assert (test["timestamp"] < end).all()
        assert train["timestamp"].max() < cal["timestamp"].min()
        assert cal["timestamp"].max() < cut
        # Expanding window: each fold trains on strictly more history.
        if prev_train_max is not None:
            assert train["timestamp"].max() > prev_train_max
        prev_train_max = train["timestamp"].max()


def test_mask_binds_every_fit_at_the_cut(feat) -> None:
    for month in CI_FOLD_MONTHS:
        cut, _ = month_bounds(month)
        train, cal, test, audit = fold_frames(feat, month)
        # Model fit and Platt fit both see only labels confirmed by cut.
        assert (train["label_available_date"] <= cut).all()
        assert (cal["label_available_date"] <= cut).all()
        # The mask's work concentrates in the cal slice: the 90-day cal
        # buffer pushes the train window past the 45-day settle, so train
        # exclusions are legitimately zero by design; cal must lose rows.
        assert audit["train_rows_masked"] <= audit["train_rows_raw"]
        assert audit["cal_rows_masked"] < audit["cal_rows_raw"]
        # ...while the test month is full and unmasked (ruling A4).
        full_month = feat[(feat["timestamp"] >= cut)
                          & (feat["timestamp"] < month_bounds(month)[1])]
        assert len(test) == len(full_month)


def test_walkforward_is_deterministic(feat) -> None:
    f1 = run_fold(feat, CI_FOLD_MONTHS[0], 1)
    f2 = run_fold(feat, CI_FOLD_MONTHS[0], 1)
    assert f1["roc_auc"] == f2["roc_auc"]
    assert f1["calibration_mae"] == f2["calibration_mae"]
    assert f1["scaler"] == f2["scaler"]


def test_calibration_is_fold_local(report) -> None:
    """Each fold fits its own scaler — the global inc3 scaler would leak
    (it saw data past the early fold cuts)."""
    scalers = [(f["scaler"]["a"], f["scaler"]["b"])
               for f in report["folds"]]
    assert len(set(scalers)) == len(scalers), (
        "identical scalers across folds - fold-local calibration broken")


def test_stability_read_arithmetic(report) -> None:
    s = report["stability"]
    refs = s["references"]
    rocs = [f["roc_auc"] for f in report["folds"]]
    assert s["roc_auc_min"] == min(rocs)
    assert s["roc_tolerance"] == ROC_STABILITY_TOL
    for f in report["folds"]:
        assert f["deltas"]["roc_auc_vs_ref"] == pytest.approx(
            f["roc_auc"] - refs["roc_auc"], abs=1e-9)
        expected_flag = f["roc_auc"] < refs["roc_auc"] - ROC_STABILITY_TOL
        assert f["flagged"] == expected_flag
        if f["flagged"]:
            assert f["test_month"] in s["flagged_folds"]
    assert s["all_within_tolerance"] == (not s["flagged_folds"])


def test_report_contract(report) -> None:
    for key in ("model", "gate", "scheme", "cal_window_days", "folds",
                "stability"):
        assert key in report, f"report missing {key}"
    assert report["model"] == "xgb_mvm_walkforward"
    assert report["gate"] == "G5"
    assert len(report["folds"]) == len(CI_FOLD_MONTHS)
    for f in report["folds"]:
        for key in ("fold", "test_month", "roc_auc", "pr_auc",
                    "precision_at_budget", "recall_at_budget",
                    "calibration_mae", "scaler", "audit", "deltas",
                    "flagged"):
            assert key in f, f"fold {f.get('test_month')} missing {key}"
        assert 0.0 <= f["calibration_mae"] <= 1.0
        assert f["audit"]["cal_fraud_masked"] > 0
