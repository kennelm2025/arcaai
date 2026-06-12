"""XGBoost MVM trainer tests (B4 increment 2).

CI-scale (seed-7 SMALL_CFG). Enforced here:

- Mask discipline: training rows with labels unconfirmed at the train-end
  cut are excluded, and the audit reports it (anti-leakage rule 3).
- Contract: the model is fitted on exactly the 12 FEATURES columns.
- Determinism: same data + pinned seed -> identical predictions.
- Sanity: probabilities in [0,1]; AUC beats both chance and the rules
  baseline at CI scale (the whole point of the MVM).
- Report contract: R8 verdict, R9 uplift table, training audit present.

No MLflow server required (env-gated logging, never set here).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from verticals.fraud.features.feature_pipeline import (
    FEATURES,
    build_features,
    chronological_split,
)
from verticals.fraud.synthetic.generator import generate
from verticals.fraud.tests.test_leakage import SMALL_CFG
from verticals.fraud.training.rules_baseline import evaluate as baseline_evaluate
from verticals.fraud.training.rules_baseline import score as baseline_score
from verticals.fraud.training.train_mvm import (
    evaluate,
    fit,
    masked_train_frame,
)


@pytest.fixture(scope="module")
def splits():
    txns, _, _, _ = generate(SMALL_CFG)
    feat = build_features(txns)
    return chronological_split(feat)


@pytest.fixture(scope="module")
def fitted(splits):
    train, _, _ = splits
    return fit(train)


def test_mask_excludes_unconfirmed_labels(splits) -> None:
    train, _, _ = splits
    masked, audit = masked_train_frame(train)
    as_of = train["timestamp"].max()
    # Everything kept is genuinely confirmed by the cut...
    assert (masked["label_available_date"] <= as_of).all()
    # ...and a real share near the cut was excluded (labels lag events).
    assert audit["rows_excluded_unconfirmed_label"] > 0
    assert audit["train_rows_masked"] + audit[
        "rows_excluded_unconfirmed_label"] == audit["train_rows_raw"]


def test_model_sees_exactly_the_contract_features(fitted) -> None:
    model, _ = fitted
    booster_feats = model.get_booster().feature_names
    assert booster_feats == FEATURES


def test_training_is_deterministic(splits) -> None:
    train, _, test = splits
    m1, _ = fit(train)
    m2, _ = fit(train)
    p1 = m1.predict_proba(test[FEATURES])[:, 1]
    p2 = m2.predict_proba(test[FEATURES])[:, 1]
    np.testing.assert_array_equal(p1, p2)


def test_probabilities_are_valid(fitted, splits) -> None:
    model, _ = fitted
    _, _, test = splits
    p = model.predict_proba(test[FEATURES])[:, 1]
    assert np.isfinite(p).all()
    assert (p >= 0).all() and (p <= 1).all()


def test_mvm_beats_baseline_auc(fitted, splits) -> None:
    """The MVM must beat the rules engine on ROC-AUC at CI scale - the
    minimum justification for its existence (R9 precedes calibration)."""
    from sklearn.metrics import roc_auc_score

    model, _ = fitted
    _, _, test = splits
    y = test["is_fraud"].to_numpy()
    auc_mvm = roc_auc_score(y, model.predict_proba(test[FEATURES])[:, 1])
    auc_rules = roc_auc_score(y, baseline_score(test).to_numpy())
    assert auc_mvm > auc_rules, (
        f"MVM ({auc_mvm:.4f}) does not beat rules baseline "
        f"({auc_rules:.4f}) at CI scale"
    )


def test_report_contract(fitted, splits) -> None:
    model, _ = fitted
    _, _, test = splits
    baseline_report = baseline_evaluate(test)
    report = evaluate(model, test, baseline_report)
    for key in ("model", "roc_auc", "pr_auc", "budgets", "r8",
                "r9_uplift_at_canonical_budget",
                "pattern_recall_at_canonical_budget"):
        assert key in report, f"report missing {key}"
    assert report["model"] == "xgb_mvm"
    assert set(report["r8"]) >= {"gate_0.85", "indicative_0.90"}
    u = report["r9_uplift_at_canonical_budget"]
    for key in ("baseline_precision", "mvm_precision",
                "precision_uplift_pp", "recall_uplift_pp"):
        assert key in u
    # Uplift arithmetic is internally consistent.
    assert u["precision_uplift_pp"] == pytest.approx(
        (u["mvm_precision"] - u["baseline_precision"]) * 100, abs=0.01)
