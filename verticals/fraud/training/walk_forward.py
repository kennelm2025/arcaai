"""Walk-forward evaluation (build stage B4, increment 4 — G5/G7 close).

Six monthly test folds Dec 2025 -> May 2026, expanding training window
from 2025-01, label_available_mask applied at each training cut (ruling
A3). Per fold: a fresh XGBoost is trained on the masked expanding window,
a fresh Platt scaler is fitted on a masked calibration slice, and the
fold's test month is evaluated retrospectively with full labels (A4) on
ROC-AUC, precision/recall at the canonical 1% budget (A2), and
calibration MAE per A1.

Implementation notes (A3 sub-judgements — ratify at gate review):
- Per-fold calibration slice = the 90 days immediately before the fold
  cut, masked at the cut; the model trains on everything earlier, masked
  at the cut. 90 days is chosen so that after the 45-day nonfraud label
  settle, roughly 45 days of confirmed mixed-class data remain — enough
  for a two-parameter Platt fit. Reusing the global inc3 scaler would
  leak (it was fitted on data through the global cal window, which
  post-dates the early fold cuts).
- "Materially below" for the stability read = fold ROC-AUC more than
  0.02 under the full-test reference. The threshold is reported, not
  hidden; flagged folds need narrative at gate review, not auto-failure.
  The December fold is expected to move (seasonality lift by design).

References for the deltas are read from the committed inc2/inc3 reports
(mvm_report.json, calibration_report.json) — declared as DVC deps, so if
the reference numbers ever change, the stability read correctly re-runs.

Outputs (DVC stage `walk_forward`):
    data/fraud/walkforward_report.json - per-fold metrics + stability read

MLflow: env-gated on MLFLOW_TRACKING_URI. One parent run
(walk_forward_g5) with six nested fold runs, per the gate doc.

Usage:
    python -m verticals.fraud.training.walk_forward [--data-dir data/fraud]
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
    label_available_mask,
)
from verticals.fraud.training.calibrate_mvm import (
    apply_platt,
    calibration_mae,
    fit_platt,
)
from verticals.fraud.training.rules_baseline import (
    CANONICAL_BUDGET,
    MLFLOW_EXPERIMENT,
    precision_recall_at_budget,
)
from verticals.fraud.training.train_mvm import PARAMS

REPO_ROOT = Path(__file__).resolve().parents[3]

# Ruling A3: six monthly test periods, expanding window from 2025-01.
FOLD_MONTHS = ("2025-12", "2026-01", "2026-02", "2026-03", "2026-04",
               "2026-05")
CAL_WINDOW_DAYS = 90        # per-fold Platt slice (implementation note)
ROC_STABILITY_TOL = 0.02    # "materially below" threshold (reported)


# ---------------------------------------------------------------------------
# Fold construction — all mask discipline lives here
# ---------------------------------------------------------------------------

def month_bounds(month: str) -> tuple[pd.Timestamp, pd.Timestamp]:
    """[start, end) bounds of a YYYY-MM month."""
    start = pd.Timestamp(month + "-01")
    return start, start + pd.offsets.MonthBegin(1)


def fold_frames(feat: pd.DataFrame, month: str) -> tuple[
        pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    """Build one fold: (masked train, masked cal, test month, audit).

    cut = start of the test month. Calibration slice = the CAL_WINDOW_DAYS
    immediately before the cut; training window = everything earlier;
    both masked as_of the cut (the fit happens at the cut — anti-leakage
    rule 3 binds the model fit and the Platt fit identically). The test
    month is evaluated retrospectively with full labels (ruling A4).
    """
    cut, end = month_bounds(month)
    cal_start = cut - pd.Timedelta(days=CAL_WINDOW_DAYS)

    test = feat[(feat["timestamp"] >= cut) & (feat["timestamp"] < end)]
    train_raw = feat[feat["timestamp"] < cal_start]
    cal_raw = feat[(feat["timestamp"] >= cal_start)
                   & (feat["timestamp"] < cut)]

    train = train_raw.loc[label_available_mask(train_raw, cut)]
    cal = cal_raw.loc[label_available_mask(cal_raw, cut)]

    audit = {
        "cut": str(cut), "cal_window_start": str(cal_start),
        "train_rows_raw": int(len(train_raw)),
        "train_rows_masked": int(len(train)),
        "cal_rows_raw": int(len(cal_raw)),
        "cal_rows_masked": int(len(cal)),
        "cal_fraud_masked": int(cal["is_fraud"].sum()),
        "n_test": int(len(test)),
        "n_test_fraud": int(test["is_fraud"].sum()),
    }
    return train, cal, test, audit


def run_fold(feat: pd.DataFrame, month: str, fold_no: int) -> dict:
    """Train, calibrate, and evaluate one fold."""
    from sklearn.metrics import average_precision_score, roc_auc_score

    train, cal, test, audit = fold_frames(feat, month)
    for name, frame in (("train", train), ("cal", cal)):
        if frame["is_fraud"].nunique() < 2:
            raise ValueError(
                f"fold {month}: masked {name} slice has a single class - "
                f"cannot fit; widen the window or revisit fold scheme")

    y_train = train["is_fraud"].to_numpy()
    n_pos = int(y_train.sum())
    spw = float((len(y_train) - n_pos) / max(1, n_pos))
    model = xgb.XGBClassifier(**PARAMS, scale_pos_weight=spw)
    model.fit(train[FEATURES], y_train)

    scaler = fit_platt(model.predict(cal[FEATURES], output_margin=True),
                       cal["is_fraud"].to_numpy())

    y = test["is_fraud"].to_numpy()
    p = apply_platt(scaler,
                    model.predict(test[FEATURES], output_margin=True))
    prec, rec, k = precision_recall_at_budget(y, p, CANONICAL_BUDGET)
    mae, _ = calibration_mae(y, p)

    audit["scale_pos_weight"] = round(spw, 3)
    return {
        "fold": fold_no,
        "test_month": month,
        "roc_auc": round(float(roc_auc_score(y, p)), 4),
        "pr_auc": round(float(average_precision_score(y, p)), 4),
        "alerts_at_budget": k,
        "precision_at_budget": round(prec, 4),
        "recall_at_budget": round(rec, 4),
        "calibration_mae": round(mae, 6),
        "scaler": scaler,
        "audit": audit,
    }


# ---------------------------------------------------------------------------
# Stability read (gate-doc requirement)
# ---------------------------------------------------------------------------

def stability_read(folds: list[dict], refs: dict | None) -> dict:
    """Per-fold deltas vs the full-test references + flagged folds.

    A fold is flagged when its ROC-AUC sits more than ROC_STABILITY_TOL
    below the reference — "materially below" made explicit. Flags demand
    narrative at gate review, they do not auto-fail the gate.
    """
    rocs = [f["roc_auc"] for f in folds]
    maes = [f["calibration_mae"] for f in folds]
    out = {
        "roc_auc_min": min(rocs),
        "roc_auc_median": round(float(np.median(rocs)), 4),
        "calibration_mae_max": max(maes),
        "roc_tolerance": ROC_STABILITY_TOL,
        "references": refs,
        "flagged_folds": [],
    }
    if refs:
        for f in folds:
            f["deltas"] = {
                "roc_auc_vs_ref": round(f["roc_auc"] - refs["roc_auc"], 4),
                "precision_at_budget_vs_ref": round(
                    f["precision_at_budget"] - refs["precision_at_budget"],
                    4),
                "calibration_mae_vs_ref": round(
                    f["calibration_mae"] - refs["calibration_mae"], 6),
            }
            f["flagged"] = bool(
                f["roc_auc"] < refs["roc_auc"] - ROC_STABILITY_TOL)
            if f["flagged"]:
                out["flagged_folds"].append(f["test_month"])
    out["all_within_tolerance"] = not out["flagged_folds"]
    return out


def evaluate_folds(feat: pd.DataFrame, months=FOLD_MONTHS,
                   refs: dict | None = None) -> dict:
    folds = [run_fold(feat, m, i + 1) for i, m in enumerate(months)]
    return {
        "model": "xgb_mvm_walkforward",
        "gate": "G5",
        "scheme": ("A3: monthly test folds, expanding training window "
                   "from 2025-01, label_available_mask at each cut; "
                   f"per-fold Platt on the {CAL_WINDOW_DAYS}-day slice "
                   "before the cut"),
        "cal_window_days": CAL_WINDOW_DAYS,
        "folds": folds,
        "stability": stability_read(folds, refs),
    }


# ---------------------------------------------------------------------------
# MLflow (env-gated) — parent run + nested fold runs
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
    s = report["stability"]
    with mlflow.start_run(run_name="walk_forward_g5") as parent:
        mlflow.set_tags({
            "stage": "B4", "gate": "G5", "model_type": "xgboost+platt",
            "vertical": "fraud", "scheme": "A3-6fold",
        })
        mlflow.log_params({
            "n_folds": len(report["folds"]),
            "cal_window_days": report["cal_window_days"],
            "roc_tolerance": s["roc_tolerance"],
        })
        mlflow.log_metrics({
            "roc_auc_min": s["roc_auc_min"],
            "roc_auc_median": s["roc_auc_median"],
            "calibration_mae_max": s["calibration_mae_max"],
            "n_flagged_folds": len(s["flagged_folds"]),
        })
        mlflow.log_dict(report, "walkforward_report.json")
        for f in report["folds"]:
            with mlflow.start_run(run_name=f"fold_{f['fold']}_"
                                  f"{f['test_month']}", nested=True):
                mlflow.set_tags({
                    "stage": "B4", "gate": "G5", "vertical": "fraud",
                    "fold": str(f["fold"]),
                    "test_month": f["test_month"],
                })
                mlflow.log_metrics({
                    "roc_auc": f["roc_auc"],
                    "pr_auc": f["pr_auc"],
                    "precision_at_budget": f["precision_at_budget"],
                    "recall_at_budget": f["recall_at_budget"],
                    "calibration_mae": f["calibration_mae"],
                    "n_test": f["audit"]["n_test"],
                    "n_test_fraud": f["audit"]["n_test_fraud"],
                })
        print(f"MLflow parent run logged: {parent.info.run_id} "
              f"(experiment {MLFLOW_EXPERIMENT}, "
              f"{len(report['folds'])} nested fold runs)")
        return parent.info.run_id


# ---------------------------------------------------------------------------
# Entry point (CWD-independent — B2a discipline)
# ---------------------------------------------------------------------------

def load_references(data_dir: Path) -> dict | None:
    """Full-test reference numbers from the committed inc2/inc3 reports."""
    mvm_path = data_dir / "mvm_report.json"
    cal_path = data_dir / "calibration_report.json"
    if not (mvm_path.exists() and cal_path.exists()):
        return None
    mvm = json.loads(mvm_path.read_text(encoding="utf-8"))
    cal = json.loads(cal_path.read_text(encoding="utf-8"))
    return {
        "roc_auc": mvm["roc_auc"],
        "precision_at_budget": mvm["precision_at_canonical_budget"],
        "calibration_mae": cal["calibration_mae"],
        "sources": {
            "mvm_mlflow_run": mvm.get("mlflow_run_id"),
            "calibration_mlflow_run": cal.get("mlflow_run_id"),
        },
    }


def run(data_dir: Path) -> int:
    refs = load_references(data_dir)
    if refs is None:
        print("ERROR: mvm_report.json / calibration_report.json not found "
              "- run increments 2 and 3 first; the stability read has no "
              "reference.")
        return 1

    feat = pd.read_parquet(data_dir / "features.parquet")
    report = evaluate_folds(feat, FOLD_MONTHS, refs)

    run_id = log_to_mlflow(report)
    if run_id:
        report["mlflow_run_id"] = run_id
    (data_dir / "walkforward_report.json").write_text(
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
