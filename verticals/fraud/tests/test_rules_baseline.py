"""Rules-engine baseline tests (B4 increment 1, gate G2).

Runs at the seed-7 CI scale (same SMALL_CFG family as test_leakage.py).
What is enforced here:

- Determinism: identical input -> identical scores (the baseline is a
  reference comparator; it must never drift between runs).
- Label-blindness: scoring a frame with label columns removed must give
  identical scores — structural proof the rules never touch labels.
- Signal floor: the rules must beat chance on the real target (they encode
  the documented pattern signatures; if they don't beat chance the rule
  set or the features are broken).
- Budget arithmetic: precision/recall at budget behaves at the edges.
- Report contract: the JSON the gate doc and MLflow consume is complete.

No MLflow server is required — logging is env-gated and these tests never
set MLFLOW_TRACKING_URI.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from verticals.fraud.features.feature_pipeline import (
    FEATURES,
    LABEL_COLUMNS,
    build_features,
    chronological_split,
)
from verticals.fraud.synthetic.generator import generate
from verticals.fraud.tests.test_leakage import SMALL_CFG
from verticals.fraud.training.rules_baseline import (
    evaluate,
    precision_recall_at_budget,
    score,
)


@pytest.fixture(scope="module")
def feat() -> pd.DataFrame:
    txns, _, _, _ = generate(SMALL_CFG)
    return build_features(txns)


def test_scores_are_deterministic(feat) -> None:
    s1 = score(feat)
    s2 = score(feat)
    pd.testing.assert_series_equal(s1, s2, check_exact=True)


def test_rules_are_label_blind(feat) -> None:
    """Dropping every label column must not change a single score."""
    with_labels = score(feat)
    without_labels = score(feat.drop(columns=LABEL_COLUMNS))
    pd.testing.assert_series_equal(with_labels, without_labels,
                                   check_exact=True)


def test_rules_use_only_contract_features(feat) -> None:
    """Scoring must work on a frame containing ONLY the 12 features."""
    bare = feat[FEATURES].copy()
    s = score(bare)
    assert len(s) == len(bare)
    assert s.notna().all()


def test_rules_beat_chance_on_real_target(feat) -> None:
    from sklearn.metrics import roc_auc_score

    _, _, test = chronological_split(feat)
    auc = roc_auc_score(test["is_fraud"].to_numpy(),
                        score(test).to_numpy())
    # Floor only — G2 is a comparator, not a performance gate. The rules
    # encode the injected signatures, so material signal must be present.
    assert auc > 0.60, f"rules baseline shows no signal (AUC {auc:.4f})"


def test_precision_recall_at_budget_edges() -> None:
    y = np.array([1, 0, 0, 0, 1, 0, 0, 0, 0, 0])
    s = np.array([9.0, 8, 7, 6, 5, 4, 3, 2, 1, 0])
    p, r, k = precision_recall_at_budget(y, s, 0.10)  # top-1
    assert (p, r, k) == (1.0, 0.5, 1)
    p, r, k = precision_recall_at_budget(y, s, 0.50)  # top-5
    assert k == 5 and p == pytest.approx(0.4) and r == pytest.approx(1.0)
    # Zero-positive frame must not divide by zero
    p, r, k = precision_recall_at_budget(np.zeros(10), s, 0.2)
    assert (p, r) == (0.0, 0.0)


def test_evaluate_report_contract(feat) -> None:
    _, _, test = chronological_split(feat)
    report = evaluate(test)
    for key in ("model", "gate", "roc_auc", "pr_auc", "budgets",
                "canonical_budget", "precision_at_canonical_budget",
                "recall_at_canonical_budget",
                "pattern_recall_at_canonical_budget"):
        assert key in report, f"report missing {key}"
    assert report["model"] == "rules_baseline"
    assert report["gate"] == "G2"
    assert "0.010" in report["budgets"]
    b = report["budgets"]["0.010"]
    assert b["alerts"] == max(1, int(len(test) * 0.01))
    assert 0.0 <= b["precision"] <= 1.0
    assert 0.0 <= b["recall"] <= 1.0
