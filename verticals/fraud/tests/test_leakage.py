"""Anti-leakage test suite (B3, gates G3/G4).

Ported from the proven SmartDog discipline. Four independent lines of defence:

1. SHUFFLE TEST - train a real model on the engineered features with the
   target randomly shuffled. If the features leak the label, the model will
   "learn" the shuffled target anyway. Gate: AUC < 0.55.
2. SOURCE AUDIT - static scan of feature_pipeline.py: every `.rolling(` must
   exclude the current row (closed="left" or .shift(1)); every `.expanding(`
   must carry `.shift(1)`; label columns must not appear in feature code.
3. FUTURE-BLINDNESS TEST - features computed on the full dataset must be
   identical, row for row, to features computed with all future data removed.
   If deleting the future changes the past, something is looking ahead.
4. SPLIT-ORDER ASSERTIONS - the chronological split must be strictly ordered
   and the label-availability mask must behave (rules 3 and 4).

Runs at small scale (seed-7 CI config) inside ci-mlops via `pytest verticals`.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score

from verticals.fraud.features.feature_pipeline import (
    FEATURES,
    LABEL_COLUMNS,
    build_features,
    chronological_split,
    filter_report,
    label_available_mask,
)
from verticals.fraud.synthetic.generator import generate

SHUFFLE_AUC_GATE = 0.55  # Blueprint G3

SMALL_CFG = {
    "seed": 7,
    "population": {"customers": 300, "merchants": 100},
    "window": {"start_date": "2025-01-01", "end_date": "2025-12-31"},
    "behaviour": {
        "base_txn_rate_per_day": 0.8,
        "december_rate_multiplier": 1.35,
        "december_amount_multiplier": 1.2,
    },
    "fraud": {
        "spree_incidents": 40,
        "testing_incidents": 20,
        "takeover_incidents": 15,
        "first_party_rate": 0.0004,
    },
    "label_lag": {"fraud_mean_days": 18, "nonfraud_settle_days": 45},
    "out_dir": "unused",
}


@pytest.fixture(scope="module")
def feat() -> pd.DataFrame:
    txns, _, _, _ = generate(SMALL_CFG)
    return build_features(txns)


# ---------------------------------------------------------------------------
# 1. Shuffle test (G3 headline)
# ---------------------------------------------------------------------------

def _shuffle_then_featurise() -> pd.DataFrame:
    """Shuffle the label in the RAW data, then run feature engineering.

    The shuffle happens BEFORE the pipeline so that any feature which
    consumes the label - now or added later (target encoding, merchant
    fraud rates, label-aware filters) - encodes the shuffled target and
    inflates AUC. Shuffling after featurisation would test nothing.
    """
    txns, _, _, _ = generate(SMALL_CFG)
    rng = np.random.default_rng(0)
    txns = txns.copy()
    txns["is_fraud"] = rng.permutation(txns["is_fraud"].to_numpy())
    return build_features(txns)


def test_shuffle_target_auc_below_gate() -> None:
    """A model trained through the full pipeline on a SHUFFLED target must
    not beat chance on held-out data. This is the decisive gate (G3)."""
    f = _shuffle_then_featurise()
    x = f[FEATURES].to_numpy(dtype=float)
    y = f["is_fraud"].to_numpy()
    n = len(f)
    split = int(n * 0.7)
    model = HistGradientBoostingClassifier(max_iter=60, random_state=0)
    model.fit(x[:split], y[:split])
    auc = roc_auc_score(y[split:], model.predict_proba(x[split:])[:, 1])

    assert auc < SHUFFLE_AUC_GATE, (
        f"Shuffle test FAILED: AUC {auc:.4f} >= {SHUFFLE_AUC_GATE} - "
        "features carry label information"
    )


def test_shuffle_detector_catches_planted_leak() -> None:
    """Negative control: plant a deliberate leak and require the detector to
    fire. Proves the shuffle test has teeth and is not passing vacuously."""
    f = _shuffle_then_featurise()
    leaky = f.copy()
    rng = np.random.default_rng(1)
    # A 'feature' contaminated with the (shuffled) label - the classic
    # target-encoding failure mode in miniature.
    leaky["planted"] = leaky["is_fraud"] * 1.0 + rng.normal(0, 0.1, len(leaky))
    cols = [*FEATURES, "planted"]
    x = leaky[cols].to_numpy(dtype=float)
    y = leaky["is_fraud"].to_numpy()
    split = int(len(leaky) * 0.7)
    model = HistGradientBoostingClassifier(max_iter=60, random_state=0)
    model.fit(x[:split], y[:split])
    auc = roc_auc_score(y[split:], model.predict_proba(x[split:])[:, 1])
    assert auc >= SHUFFLE_AUC_GATE, (
        "detector failed to flag a planted leak - shuffle test has no power"
    )


def test_real_target_beats_chance(feat) -> None:
    """Power check: the same model on the REAL target must find signal.

    Guards against an inert feature set. Not a performance gate (that is
    B4) - just proof the features carry information at all.
    """
    x = feat[FEATURES].to_numpy(dtype=float)
    y = feat["is_fraud"].to_numpy()
    n = len(feat)
    split = int(n * 0.7)
    model = HistGradientBoostingClassifier(max_iter=60, random_state=0)
    model.fit(x[:split], y[:split])
    auc = roc_auc_score(y[split:], model.predict_proba(x[split:])[:, 1])
    assert auc > 0.60, f"features show no signal at all (AUC {auc:.4f})"


# ---------------------------------------------------------------------------
# 2. Source audit
# ---------------------------------------------------------------------------

def _pipeline_source() -> str:
    path = (
        Path(__file__).resolve().parents[1] / "features" / "feature_pipeline.py"
    )
    return path.read_text()


def test_source_audit_rolling_excludes_current_row() -> None:
    """Every .rolling( must exclude the current row at the call site."""
    for line in _pipeline_source().splitlines():
        if ".rolling(" in line:
            assert 'closed="left"' in line or ".shift(1)" in line, (
                f"rolling window without current-row exclusion: {line.strip()}"
            )


def test_source_audit_expanding_is_shifted() -> None:
    """Every .expanding( aggregation must be lagged with .shift(1)."""
    for line in _pipeline_source().splitlines():
        if ".expanding(" in line:
            assert ".shift(1)" in line, (
                f"expanding aggregate without shift(1): {line.strip()}"
            )


def test_source_audit_no_label_columns_in_feature_code() -> None:
    """Label columns may appear only in the explicit label pass-through."""
    src = _pipeline_source()
    feature_funcs = re.findall(
        r"def _per_customer.*?(?=\ndef )", src, flags=re.DOTALL
    )
    assert feature_funcs, "could not locate _per_customer for audit"
    for col in ("is_fraud", "fraud_pattern", "label_available_date"):
        assert col not in feature_funcs[0], (
            f"label column '{col}' referenced inside feature construction"
        )


# ---------------------------------------------------------------------------
# 3. Future-blindness (date-filter audit)
# ---------------------------------------------------------------------------

def test_features_unchanged_when_future_removed(feat) -> None:
    """Deleting all future rows must not change features for the past.

    The strongest causality check: recompute features on data truncated at
    a mid-window cut and require bit-identical values for every surviving
    transaction.
    """
    txns, _, _, _ = generate(SMALL_CFG)
    cut = txns["timestamp"].quantile(0.6)

    truncated = txns[txns["timestamp"] <= cut].copy()
    feat_truncated = build_features(truncated)

    full_past = (
        feat[feat["timestamp"] <= cut]
        .sort_values("transaction_id", kind="stable")
        .reset_index(drop=True)
    )
    trunc_past = (
        feat_truncated.sort_values("transaction_id", kind="stable")
        .reset_index(drop=True)
    )

    assert len(full_past) == len(trunc_past)
    pd.testing.assert_frame_equal(
        full_past[["transaction_id", *FEATURES]],
        trunc_past[["transaction_id", *FEATURES]],
        check_exact=True,
    )


# ---------------------------------------------------------------------------
# 4. Split order and label availability (rules 3 and 4)
# ---------------------------------------------------------------------------

def test_chronological_split_order_and_sizes(feat) -> None:
    train, cal, test = chronological_split(feat)
    assert train["timestamp"].max() <= cal["timestamp"].min()
    assert cal["timestamp"].max() <= test["timestamp"].min()
    n = len(feat)
    assert len(train) + len(cal) + len(test) == n
    assert abs(len(train) / n - 0.70) < 0.01
    assert abs(len(cal) / n - 0.15) < 0.01


def test_label_available_mask_blocks_unconfirmed_labels(feat) -> None:
    """At the train-end cut, recent labels must be masked out (rule 3)."""
    train, _, _ = chronological_split(feat)
    as_of = train["timestamp"].max()
    mask = label_available_mask(train, as_of)
    assert mask.dtype == bool
    # Labels lag events; near the cut the mask must exclude a real share.
    assert 0 < (~mask).sum() < len(train)
    # And everything the mask admits really is known by the cut.
    assert (train.loc[mask, "label_available_date"] <= as_of).all()


def test_feature_frame_contract(feat) -> None:
    """The frame B4 consumes: 12 features, labels carried, no NaNs, no flags."""
    assert list(feat[FEATURES].columns) == FEATURES
    assert len(FEATURES) == 12
    for col in LABEL_COLUMNS:
        assert col in feat.columns
    assert not feat[FEATURES].isna().any().any()
    report = filter_report(feat)
    assert report["flagged"] == [], f"pre-train filters flagged: {report['flagged']}"
