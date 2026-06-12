"""Platt calibration for the XGBoost MVM (build stage B4, increment 3 — G7).

Fits a two-parameter Platt scaler — p = sigmoid(a * margin + b) over the
MVM's raw margin — on the 15% CALIBRATION split only, with the
label_available_mask applied at the cal-end cut (the Platt fit is a fit;
ruling A4's mask discipline binds it exactly as it binds the trainer).
The scaler is then applied to the TEST split, where evaluation is
retrospective with full labels (A4).

Gate criteria (docs/build/B4_GATE.md):
- G7: calibration MAE < 0.05 on the test split, where MAE is defined per
  ruling A1 — 10 equal-frequency probability bins, mean
  |observed fraud rate - mean predicted probability| per bin, unweighted.
- R10: calibrated probabilities are INDEPENDENT per row. The scaler is a
  fixed monotone map applied row-wise; there is no group normalisation,
  no sum-to-one, anywhere. The report records a structural verification
  (same row -> same probability regardless of batch composition).

Why calibration matters here specifically: the MVM trains with
scale_pos_weight ~176, which deliberately inflates raw probabilities to
buy recall. Ranking (ROC-AUC, the budget metrics) is unaffected — Platt
is monotone — but the raw numbers are not usable as probabilities until
this remap. The report records before/after MAE so the improvement is
auditable, not asserted.

Outputs (DVC stage `calibrate_mvm`):
    data/fraud/models/platt_scaler.json  - {a, b} (transparent, no pickle)
    data/fraud/calibration_report.json   - MAE, reliability table, verdicts

MLflow: env-gated on MLFLOW_TRACKING_URI, same as baseline and trainer.
Reliability table is logged as a run artefact (gate-doc requirement).

Usage:
    python -m verticals.fraud.training.calibrate_mvm [--data-dir data/fraud]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb

from verticals.fraud.features.feature_pipeline import (
    FEATURES,
    chronological_split,
    label_available_mask,
)
from verticals.fraud.training.rules_baseline import MLFLOW_EXPERIMENT

REPO_ROOT = Path(__file__).resolve().parents[3]

G7_MAE_GATE = 0.05   # calibration MAE gate (G7, definition per ruling A1)
N_BINS = 10          # equal-frequency bins (ruling A1)


# ---------------------------------------------------------------------------
# Platt scaler — two parameters, fitted on the masked cal split only
# ---------------------------------------------------------------------------

def fit_platt(margins: np.ndarray, y: np.ndarray) -> dict:
    """Fit p = sigmoid(a * margin + b) by logistic regression.

    Textbook Platt scaling over the model's raw margin. Effectively
    unregularised (C large): two parameters on thousands of rows need no
    shrinkage, and regularising would bias `a` toward 0 — miscalibration
    by construction.
    """
    from sklearn.linear_model import LogisticRegression

    lr = LogisticRegression(C=1e6, solver="lbfgs", max_iter=1000)
    lr.fit(margins.reshape(-1, 1), y)
    return {"a": float(lr.coef_[0][0]), "b": float(lr.intercept_[0])}


def apply_platt(scaler: dict, margins: np.ndarray) -> np.ndarray:
    """Row-wise monotone map. No batch statistics, no normalisation (R10)."""
    z = scaler["a"] * margins + scaler["b"]
    return 1.0 / (1.0 + np.exp(-z))


# ---------------------------------------------------------------------------
# Calibration MAE per ruling A1
# ---------------------------------------------------------------------------

def equal_frequency_bins(p: np.ndarray, n_bins: int = N_BINS) -> list[np.ndarray]:
    """Split row indices into `n_bins` contiguous rank chunks of p.

    Rank-based rather than quantile-edge-based so heavy ties at low
    probabilities (most of a fraud score distribution) cannot collapse
    bins. Bin sizes differ by at most one row. Sort is stable, so the
    binning is deterministic.
    """
    order = np.argsort(p, kind="stable")
    return [b for b in np.array_split(order, n_bins) if len(b) > 0]


def calibration_mae(y: np.ndarray, p: np.ndarray,
                    n_bins: int = N_BINS) -> tuple[float, list[dict]]:
    """MAE per A1: unweighted mean over equal-frequency bins of
    |observed fraud rate - mean predicted probability|.

    Returns (mae, reliability_table) — the table is the gate-doc artefact.
    """
    table = []
    for i, idx in enumerate(equal_frequency_bins(p, n_bins)):
        obs = float(y[idx].mean())
        pred = float(p[idx].mean())
        table.append({
            "bin": i + 1,
            "n": int(len(idx)),
            "mean_predicted": round(pred, 6),
            "observed_fraud_rate": round(obs, 6),
            "abs_gap": round(abs(obs - pred), 6),
        })
    mae = float(np.mean([row["abs_gap"] for row in table]))
    return mae, table


# ---------------------------------------------------------------------------
# R10 structural verification — independence, no normalisation
# ---------------------------------------------------------------------------

def verify_independence(scaler: dict, margins: np.ndarray) -> dict:
    """Calibrated probabilities must be a per-row function of the score.

    Checks: (1) calibrating a shuffled batch returns the same values
    per row — batch composition cannot matter; (2) calibrating any single
    row alone equals its in-batch value; (3) monotone in the margin, so
    ranking metrics are untouched. Sum-to-one is structurally impossible
    in a per-row map, but its absence is asserted explicitly anyway.
    """
    p_full = apply_platt(scaler, margins)
    rng = np.random.default_rng(0)
    perm = rng.permutation(len(margins))
    p_perm = apply_platt(scaler, margins[perm])
    batch_independent = bool(np.array_equal(p_full[perm], p_perm))
    solo = apply_platt(scaler, margins[:1])
    row_independent = bool(np.array_equal(solo, p_full[:1]))
    order = np.argsort(margins, kind="stable")
    monotone = bool((np.diff(p_full[order]) >= 0).all())
    return {
        "batch_independent": batch_independent,
        "row_independent": row_independent,
        "monotone_in_margin": monotone,
        "sum_to_one_normalisation": False,
        "pass": batch_independent and row_independent and monotone,
    }


# ---------------------------------------------------------------------------
# Calibration run — mask discipline lives here
# ---------------------------------------------------------------------------

def masked_cal_frame(cal: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Apply the label-availability mask at the cal-end cut.

    The Platt fit consumes labels, so anti-leakage rule 3 binds it: only
    outcomes confirmed by the end of the calibration window may be used.
    """
    as_of = cal["timestamp"].max()
    mask = label_available_mask(cal, as_of)
    audit = {
        "cal_rows_raw": int(len(cal)),
        "cal_rows_masked": int(mask.sum()),
        "rows_excluded_unconfirmed_label": int((~mask).sum()),
        "as_of": str(as_of),
    }
    return cal.loc[mask], audit


def calibrate(model: xgb.XGBClassifier, cal: pd.DataFrame,
              test: pd.DataFrame) -> dict:
    """Fit on masked cal, evaluate on test. Returns the full report."""
    from sklearn.metrics import roc_auc_score

    cal_masked, audit = masked_cal_frame(cal)
    m_cal = model.predict(cal_masked[FEATURES], output_margin=True)
    scaler = fit_platt(m_cal, cal_masked["is_fraud"].to_numpy())

    y = test["is_fraud"].to_numpy()
    m_test = model.predict(test[FEATURES], output_margin=True)
    p_raw = model.predict_proba(test[FEATURES])[:, 1]
    p_cal = apply_platt(scaler, m_test)

    mae_raw, table_raw = calibration_mae(y, p_raw)
    mae_cal, table_cal = calibration_mae(y, p_cal)

    return {
        "model": "xgb_mvm_platt",
        "gate": "G7",
        "split": "test",
        "n_rows": int(len(test)),
        "n_fraud": int(y.sum()),
        "scaler": scaler,
        "calibration_audit": audit,
        "mae_definition": ("A1: 10 equal-frequency bins, unweighted mean of "
                           "|observed fraud rate - mean predicted| per bin"),
        "calibration_mae_uncalibrated": round(mae_raw, 6),
        "calibration_mae": round(mae_cal, 6),
        "reliability_table": table_cal,
        "reliability_table_uncalibrated": table_raw,
        "roc_auc_uncalibrated": round(float(roc_auc_score(y, p_raw)), 6),
        "roc_auc_calibrated": round(float(roc_auc_score(y, p_cal)), 6),
        "r10_independence": verify_independence(scaler, m_test),
        "g7": {
            "gate_mae_lt_0.05": bool(mae_cal < G7_MAE_GATE),
            "improved_vs_uncalibrated": bool(mae_cal < mae_raw),
        },
    }


# ---------------------------------------------------------------------------
# MLflow (env-gated)
# ---------------------------------------------------------------------------

def log_to_mlflow(report: dict) -> str | None:
    uri = os.environ.get("MLFLOW_TRACKING_URI")
    if not uri:
        print("MLFLOW_TRACKING_URI not set - skipping MLflow logging "
              "(set it and re-run to record the run).")
        return None
    import mlflow

    mlflow.set_tracking_uri(uri)
    mlflow.set_experiment(MLFLOW_EXPERIMENT)
    with mlflow.start_run(run_name="xgb_mvm_platt_calibration") as run:
        mlflow.set_tags({
            "stage": "B4", "gate": "G7", "model_type": "xgboost+platt",
            "vertical": "fraud", "split": "test", "calibrated": "true",
        })
        mlflow.log_params({
            "platt_a": report["scaler"]["a"],
            "platt_b": report["scaler"]["b"],
            "n_bins": N_BINS,
            "cal_rows_masked": report["calibration_audit"]["cal_rows_masked"],
            "rows_excluded_unconfirmed_label":
                report["calibration_audit"]["rows_excluded_unconfirmed_label"],
        })
        mlflow.log_metrics({
            "calibration_mae": report["calibration_mae"],
            "calibration_mae_uncalibrated":
                report["calibration_mae_uncalibrated"],
            "roc_auc_calibrated": report["roc_auc_calibrated"],
            "test_rows": report["n_rows"],
        })
        mlflow.log_dict({"reliability_table": report["reliability_table"]},
                        "reliability_table.json")
        mlflow.log_dict(report, "calibration_report.json")
        print(f"MLflow run logged: {run.info.run_id} "
              f"(experiment {MLFLOW_EXPERIMENT})")
        return run.info.run_id


# ---------------------------------------------------------------------------
# Entry point (CWD-independent — B2a discipline)
# ---------------------------------------------------------------------------

def run(data_dir: Path) -> int:
    model_path = data_dir / "models" / "xgb_mvm.ubj"
    if not model_path.exists():
        print("ERROR: models/xgb_mvm.ubj not found - run the MVM trainer "
              "(increment 2) first; there is nothing to calibrate.")
        return 1
    model = xgb.XGBClassifier()
    model.load_model(model_path)

    feat = pd.read_parquet(data_dir / "features.parquet")
    _, cal, test = chronological_split(feat)

    report = calibrate(model, cal, test)

    scaler_path = data_dir / "models" / "platt_scaler.json"
    scaler_path.write_text(json.dumps(report["scaler"], indent=2),
                           encoding="utf-8")

    run_id = log_to_mlflow(report)
    if run_id:
        report["mlflow_run_id"] = run_id
    (data_dir / "calibration_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default="data/fraud")
    args = parser.parse_args()
    data_dir = Path(args.data_dir)
    if not data_dir.is_absolute():
        data_dir = REPO_ROOT / data_dir
    sys.exit(run(data_dir))


if __name__ == "__main__":
    main()
