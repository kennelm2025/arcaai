"""XGBoost MVM trainer (build stage B4, increment 2 — G5 entry).

The minimum viable model: XGBoost over exactly the 12 contract features
(FEATURES.md), trained on the chronological 70 split with the
label_available_mask applied at the train-end cut (anti-leakage rule 3),
seed-pinned, no tuning loop. Evaluated on the test split against R8
(ROC-AUC > 0.85 gate / 0.90 indicative) and R9 (precision uplift at the
1% alert budget vs the rules-engine baseline — gate-doc ruling A2).

Honesty notes carried from the gate doc:
- The unfitted rules baseline already clears R8 on this synthetic data
  (injected patterns are cleaner than reality). The meaningful number is
  the R9 uplift and, in increment 3, calibration quality — not the R8
  pass itself.
- class imbalance: scale_pos_weight = n_neg/n_pos on the MASKED train
  split. Dataset fraud rate (~0.5% by count) is above real-world ~0.1%
  per the data dictionary; the weight is recorded in MLflow params.
- Evaluation labels are retrospective/full on the test split (ruling A4);
  the mask binds the training cut only.

Outputs (DVC stage `train_mvm`):
    data/fraud/models/xgb_mvm.ubj  - the model artefact (also logged to MLflow)
    data/fraud/mvm_report.json     - metrics, R8/R9 verdicts, uplift table

MLflow: env-gated on MLFLOW_TRACKING_URI, same as the baseline.

Usage:
    python -m verticals.fraud.training.train_mvm [--data-dir data/fraud]
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
from verticals.fraud.training.rules_baseline import (
    ALERT_BUDGETS,
    CANONICAL_BUDGET,
    MLFLOW_EXPERIMENT,
    precision_recall_at_budget,
)

REPO_ROOT = Path(__file__).resolve().parents[3]

SEED = 42
R8_GATE = 0.85          # ROC-AUC sign-off gate (R8)
R8_INDICATIVE = 0.90    # indicative target (R8)

# MVM hyperparameters — fixed by judgement, no tuning loop at B4. Modest
# depth/shrinkage; recorded in MLflow so any future tuning has a pinned
# starting point. scale_pos_weight is computed from the masked train split
# at run time, not hard-coded.
PARAMS = {
    "n_estimators": 400,
    "max_depth": 6,
    "learning_rate": 0.08,
    "subsample": 0.9,
    "colsample_bytree": 0.9,
    "min_child_weight": 5,
    "tree_method": "hist",
    "eval_metric": "aucpr",
    "random_state": SEED,
    "n_jobs": -1,
}


# ---------------------------------------------------------------------------
# Training (mask discipline lives here)
# ---------------------------------------------------------------------------

def masked_train_frame(train: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Apply the label-availability mask at the train-end cut.

    A model trained at time T may only learn from outcomes confirmed by T
    (anti-leakage rule 3). Returns the masked frame and an audit dict.
    """
    as_of = train["timestamp"].max()
    mask = label_available_mask(train, as_of)
    audit = {
        "train_rows_raw": int(len(train)),
        "train_rows_masked": int(mask.sum()),
        "rows_excluded_unconfirmed_label": int((~mask).sum()),
        "as_of": str(as_of),
    }
    return train.loc[mask], audit


def fit(train: pd.DataFrame) -> tuple[xgb.XGBClassifier, dict]:
    masked, audit = masked_train_frame(train)
    y = masked["is_fraud"].to_numpy()
    n_pos = int(y.sum())
    spw = float((len(y) - n_pos) / max(1, n_pos))
    model = xgb.XGBClassifier(**PARAMS, scale_pos_weight=spw)
    model.fit(masked[FEATURES], y)
    audit["scale_pos_weight"] = round(spw, 3)
    audit["train_fraud_rows"] = n_pos
    return model, audit


# ---------------------------------------------------------------------------
# Evaluation — R8 + R9 against the committed baseline report
# ---------------------------------------------------------------------------

def evaluate(model: xgb.XGBClassifier, test: pd.DataFrame,
             baseline_report: dict) -> dict:
    from sklearn.metrics import average_precision_score, roc_auc_score

    y = test["is_fraud"].to_numpy()
    p = model.predict_proba(test[FEATURES])[:, 1]

    out: dict = {
        "model": "xgb_mvm",
        "gate": "G5-entry",
        "split": "test",
        "n_rows": int(len(test)),
        "n_fraud": int(y.sum()),
        "roc_auc": round(float(roc_auc_score(y, p)), 4),
        "pr_auc": round(float(average_precision_score(y, p)), 4),
        "budgets": {},
    }
    for b in ALERT_BUDGETS:
        prec, rec, k = precision_recall_at_budget(y, p, b)
        out["budgets"][f"{b:.3f}"] = {
            "alerts": k, "precision": round(prec, 4), "recall": round(rec, 4),
        }
    cb = out["budgets"][f"{CANONICAL_BUDGET:.3f}"]
    out["canonical_budget"] = CANONICAL_BUDGET
    out["precision_at_canonical_budget"] = cb["precision"]
    out["recall_at_canonical_budget"] = cb["recall"]

    # Per-pattern recall at the canonical budget — where did the uplift
    # come from? (Expectation: takeover; first_party stays near-invisible.)
    k = cb["alerts"]
    order = np.argsort(-p, kind="stable")[:k]
    alerted = test.iloc[order]
    pat: dict[str, dict] = {}
    for name, g in test[test["is_fraud"] == 1].groupby("fraud_pattern"):
        caught = int((alerted["fraud_pattern"] == name).sum())
        pat[str(name)] = {"fraud_rows": int(len(g)), "caught": caught,
                          "recall": round(caught / len(g), 4)}
    out["pattern_recall_at_canonical_budget"] = pat

    # R8 verdict
    out["r8"] = {
        "gate_0.85": bool(out["roc_auc"] > R8_GATE),
        "indicative_0.90": bool(out["roc_auc"] > R8_INDICATIVE),
        "context": ("synthetic data: unfitted rules baseline also clears "
                    "0.85 - see B4_GATE.md context note"),
    }

    # R9 verdict — uplift vs the baseline report produced by increment 1
    bkey = f"{CANONICAL_BUDGET:.3f}"
    b_prec = baseline_report["budgets"][bkey]["precision"]
    b_rec = baseline_report["budgets"][bkey]["recall"]
    out["r9_uplift_at_canonical_budget"] = {
        "baseline_precision": b_prec,
        "mvm_precision": cb["precision"],
        "precision_uplift_pp": round((cb["precision"] - b_prec) * 100, 2),
        "baseline_recall": b_rec,
        "mvm_recall": cb["recall"],
        "recall_uplift_pp": round((cb["recall"] - b_rec) * 100, 2),
        "baseline_mlflow_run": baseline_report.get("mlflow_run_id"),
    }
    return out


# ---------------------------------------------------------------------------
# MLflow (env-gated)
# ---------------------------------------------------------------------------

def log_to_mlflow(report: dict, audit: dict, model_path: Path) -> str | None:
    uri = os.environ.get("MLFLOW_TRACKING_URI")
    if not uri:
        print("MLFLOW_TRACKING_URI not set - skipping MLflow logging "
              "(set it and re-run to record the run).")
        return None
    import mlflow

    mlflow.set_tracking_uri(uri)
    mlflow.set_experiment(MLFLOW_EXPERIMENT)
    with mlflow.start_run(run_name="xgb_mvm_uncalibrated") as run:
        mlflow.set_tags({
            "stage": "B4", "gate": "G5-entry", "model_type": "xgboost",
            "vertical": "fraud", "split": "test", "calibrated": "false",
        })
        mlflow.log_params({**PARAMS, **{k: audit[k] for k in
                          ("scale_pos_weight", "train_rows_masked",
                           "rows_excluded_unconfirmed_label")}})
        u = report["r9_uplift_at_canonical_budget"]
        mlflow.log_metrics({
            "roc_auc": report["roc_auc"],
            "pr_auc": report["pr_auc"],
            "precision_at_budget": report["precision_at_canonical_budget"],
            "recall_at_budget": report["recall_at_canonical_budget"],
            "r9_precision_uplift_pp": u["precision_uplift_pp"],
            "r9_recall_uplift_pp": u["recall_uplift_pp"],
            "test_rows": report["n_rows"],
        })
        mlflow.log_dict(report, "mvm_report.json")
        mlflow.log_artifact(str(model_path))
        print(f"MLflow run logged: {run.info.run_id} "
              f"(experiment {MLFLOW_EXPERIMENT})")
        return run.info.run_id


# ---------------------------------------------------------------------------
# Entry point (CWD-independent — B2a discipline)
# ---------------------------------------------------------------------------

def run(data_dir: Path) -> int:
    feat = pd.read_parquet(data_dir / "features.parquet")
    train, _, test = chronological_split(feat)

    baseline_path = data_dir / "baseline_report.json"
    if not baseline_path.exists():
        print("ERROR: baseline_report.json not found - run the rules "
              "baseline (increment 1) first; R9 has no denominator.")
        return 1
    baseline_report = json.loads(baseline_path.read_text(encoding="utf-8"))

    model, audit = fit(train)
    report = evaluate(model, test, baseline_report)
    report["training_audit"] = audit
    report["params"] = PARAMS

    models_dir = data_dir / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / "xgb_mvm.ubj"
    model.save_model(model_path)

    run_id = log_to_mlflow(report, audit, model_path)
    if run_id:
        report["mlflow_run_id"] = run_id
    (data_dir / "mvm_report.json").write_text(
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
