"""Rules-engine baseline (build stage B4, gate G2).

The transparent, deterministic floor every model must beat. This is the
reference implementation of what a bank's existing rules engine looks like:
hand-set thresholds over the same 12 signals the MVM sees, weighted by
domain judgement, never fitted to labels. It exists so that B4's XGBoost
MVM has an honest comparator and so the canonical business metric (R9:
precision uplift at fixed alert budget) has a denominator.

Anti-leakage position: the rules read ONLY the 12 contract features
(FEATURES.md). No label column is consulted — weights are static domain
priors mirroring publicly known fraud signatures (velocity bursts,
card-testing micro-amounts, new-device + amount-shift takeover, night/
international/high-risk-category risk stacking). The shuffle test in
ci-mlops covers this module's inputs by construction.

Evaluation protocol (chronological 70/15/15 per FEATURES.md):
- Scores are computed for ALL rows (the rules are stateless per-row).
- Headline metrics are reported on the TEST split only — the same split
  the MVM will be judged on. Retrospective evaluation uses full labels;
  the label_available_mask discipline binds TRAINING cuts (the MVM, not
  this unfitted baseline).

MLflow: logs a run to experiment `arcaai-fraud` when MLFLOW_TRACKING_URI
is set in the environment; otherwise prints a notice and skips — so DVC
repro and CI stay green without a tracking server.

Usage:
    python -m verticals.fraud.training.rules_baseline [--data-dir data/fraud]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from verticals.fraud.features.feature_pipeline import (
    FEATURES,
    chronological_split,
)

REPO_ROOT = Path(__file__).resolve().parents[3]

MLFLOW_EXPERIMENT = "arcaai-fraud"

# Alert budgets: fraction of transactions an ops team can review. The
# canonical R9 metric is precision uplift at the 1.0% budget (ASSUMPTION
# A2 in docs/build/B4_GATE.md — ratify or amend there).
ALERT_BUDGETS = (0.005, 0.01)
CANONICAL_BUDGET = 0.01

# ---------------------------------------------------------------------------
# The rules. Static domain priors — tuned by judgement, NEVER fitted.
# Each rule: (name, predicate over the feature frame, points).
# Signatures mirror the four public card-fraud archetypes; thresholds are
# round numbers a fraud-ops analyst would recognise.
# ---------------------------------------------------------------------------

def _amount(f: pd.DataFrame) -> pd.Series:
    """Recover GBP amount from the contract's log_amount."""
    return np.expm1(f["log_amount"])


def rule_table(f: pd.DataFrame) -> list[tuple[str, pd.Series, float]]:
    amount = _amount(f)
    return [
        # Velocity (spree / testing)
        ("velocity_1h_ge3", f["txn_count_1h"] >= 3, 3.0),
        ("velocity_24h_ge8", f["txn_count_24h"] >= 8, 2.0),
        ("rapid_fire_lt2min", f["mins_since_last_txn"] < 2.0, 2.0),
        # Card-testing: micro-amount in an active burst
        ("micro_amount_burst", (amount < 2.0) & (f["txn_count_1h"] >= 2), 3.0),
        # Account takeover: new device, especially with an amount shift
        ("new_device", f["device_novelty"] >= 1.0, 2.0),
        ("new_device_amount_shift",
         (f["device_novelty"] >= 1.0) & (f["amount_zscore"] > 3.0), 3.0),
        # Amount anomaly on its own
        ("amount_zscore_gt3", f["amount_zscore"] > 3.0, 2.0),
        # Context risk stack
        ("night", f["is_night"] >= 1.0, 1.0),
        ("international", f["is_international"] >= 1.0, 1.0),
        ("high_risk_category", f["category_risk"] >= 0.7, 1.0),
        ("category_shift_high_value",
         (f["category_shift"] >= 1.0) & (f["amount_zscore"] > 2.0), 1.0),
    ]


def score(f: pd.DataFrame) -> pd.Series:
    """Deterministic rule score per row. Higher = more suspicious."""
    s = pd.Series(0.0, index=f.index)
    for _, hit, points in rule_table(f):
        s = s + hit.astype(float) * points
    return s


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def precision_recall_at_budget(
    y: np.ndarray, s: np.ndarray, budget: float
) -> tuple[float, float, int]:
    """Precision/recall when alerting the top `budget` fraction by score.

    Ties at the threshold are broken deterministically by stable sort order
    so the alert count is exactly floor(n * budget).
    """
    n = len(y)
    k = max(1, int(n * budget))
    order = np.argsort(-s, kind="stable")[:k]
    hits = int(y[order].sum())
    total_pos = int(y.sum())
    precision = hits / k
    recall = hits / total_pos if total_pos else 0.0
    return float(precision), float(recall), k


def evaluate(test: pd.DataFrame) -> dict:
    from sklearn.metrics import average_precision_score, roc_auc_score

    y = test["is_fraud"].to_numpy()
    s = score(test).to_numpy()

    out: dict = {
        "model": "rules_baseline",
        "gate": "G2",
        "split": "test",
        "n_rows": int(len(test)),
        "n_fraud": int(y.sum()),
        "fraud_rate": round(float(y.mean()), 6),
        "roc_auc": round(float(roc_auc_score(y, s)), 4),
        "pr_auc": round(float(average_precision_score(y, s)), 4),
        "budgets": {},
    }
    for b in ALERT_BUDGETS:
        p, r, k = precision_recall_at_budget(y, s, b)
        out["budgets"][f"{b:.3f}"] = {
            "alerts": k, "precision": round(p, 4), "recall": round(r, 4),
        }
    cb = out["budgets"][f"{CANONICAL_BUDGET:.3f}"]
    out["canonical_budget"] = CANONICAL_BUDGET
    out["precision_at_canonical_budget"] = cb["precision"]
    out["recall_at_canonical_budget"] = cb["recall"]

    # Per-pattern recall at the canonical budget — which archetypes do the
    # rules actually catch? (first_party is designed to be near-invisible.)
    k = cb["alerts"]
    order = np.argsort(-s, kind="stable")[:k]
    alerted = test.iloc[order]
    pat: dict[str, dict] = {}
    for p_name, g in test[test["is_fraud"] == 1].groupby("fraud_pattern"):
        caught = int((alerted["fraud_pattern"] == p_name).sum())
        pat[str(p_name)] = {"fraud_rows": int(len(g)),
                            "caught": caught,
                            "recall": round(caught / len(g), 4)}
    out["pattern_recall_at_canonical_budget"] = pat
    return out


# ---------------------------------------------------------------------------
# MLflow (conditional — env-gated so CI/DVC never need a server)
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
    with mlflow.start_run(run_name="rules_baseline_g2") as run:
        mlflow.set_tags({
            "stage": "B4", "gate": "G2", "model_type": "rules_engine",
            "vertical": "fraud", "split": "test",
        })
        mlflow.log_params({
            "n_rules": len(rule_table(pd.DataFrame(
                {c: pd.Series(dtype=float) for c in FEATURES}))),
            "canonical_budget": CANONICAL_BUDGET,
            "fitted": False,
        })
        mlflow.log_metrics({
            "roc_auc": report["roc_auc"],
            "pr_auc": report["pr_auc"],
            "precision_at_budget": report["precision_at_canonical_budget"],
            "recall_at_budget": report["recall_at_canonical_budget"],
            "test_rows": report["n_rows"],
        })
        mlflow.log_dict(report, "baseline_report.json")
        print(f"MLflow run logged: {run.info.run_id} "
              f"(experiment {MLFLOW_EXPERIMENT})")
        return run.info.run_id


# ---------------------------------------------------------------------------
# Entry point (CWD-independent — B2a discipline)
# ---------------------------------------------------------------------------

def run(data_dir: Path) -> int:
    feat = pd.read_parquet(data_dir / "features.parquet")
    _, _, test = chronological_split(feat)
    report = evaluate(test)
    run_id = log_to_mlflow(report)
    if run_id:
        report["mlflow_run_id"] = run_id
    (data_dir / "baseline_report.json").write_text(
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
