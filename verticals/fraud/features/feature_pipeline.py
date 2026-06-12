"""Fraud feature pipeline (build stage B3).

Builds the 12-feature MVM budget from the B2 synthetic dataset, applying the
anti-leakage discipline ported from the SmartDog programme:

- Every historical aggregate is computed on `shift(1)` within customer - the
  current transaction never contributes to its own features (rule 1).
- No feature reads `is_fraud`, `fraud_pattern`, or `label_available_date`
  (rule 2). Merchant/category risk is a static MCC-style map, never a
  label-derived statistic.
- `label_available_mask` is provided so downstream training (B4) can only use
  labels already confirmed at the training cut date (rule 3).
- The chronological 70/15/15 split is by timestamp with strict ordering
  assertions - no shuffled splits, ever (rule 4).

Outputs (DVC stage `feature_engineer`):
    data/fraud/features.parquet   - transaction_id + 12 features + label columns
    data/fraud/feature_report.json - pre-train filter report (VIF / missing /
                                     near-zero variance) and split boundaries

Usage:
    python -m verticals.fraud.features.feature_pipeline [--data-dir data/fraud]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]

# The locked 12-feature MVM budget (Build & Quality Plan B3 / Blueprint feature
# spec). Order is the contract - B4 trains on exactly these columns.
FEATURES = [
    "txn_count_1h",
    "txn_count_24h",
    "txn_count_7d",
    "amount_sum_24h",
    "amount_zscore",
    "mins_since_last_txn",
    "device_novelty",
    "category_shift",
    "category_risk",
    "is_night",
    "is_international",
    "log_amount",
]

LABEL_COLUMNS = ["is_fraud", "fraud_pattern", "label_available_date"]

# Static MCC-style category risk map. Mirrors public card-scheme risk tiers
# (gambling / digital goods / jewellery / electronics are classic high-risk
# MCCs). Deliberately NOT derived from observed fraud labels - that would be
# target leakage dressed up as a feature.
CATEGORY_RISK = {
    "grocery": 0.1,
    "fuel": 0.1,
    "utilities": 0.1,
    "restaurant": 0.2,
    "entertainment": 0.3,
    "fashion": 0.3,
    "travel": 0.5,
    "online_retail": 0.5,
    "electronics": 0.7,
    "jewellery": 0.8,
    "digital_goods": 0.9,
    "gambling": 1.0,
}

SPLIT_RATIOS = (0.70, 0.15, 0.15)  # train / calibration / test, chronological


# ---------------------------------------------------------------------------
# Feature construction
# ---------------------------------------------------------------------------

def _per_customer(g: pd.DataFrame) -> pd.DataFrame:
    """Historical features for one customer's chronologically ordered txns.

    Anti-leakage rule 1: the current transaction never contributes to its own
    features. Time-window aggregates use `closed="left"` - the window is
    [t - w, t), strictly before the current row. Expanding aggregates use
    `.shift(1)`. The leakage suite's source audit enforces both forms.
    """
    out = pd.DataFrame(index=g.index)
    ts = g["timestamp"]

    # Time-indexed history for windowed aggregates anchored at each txn time.
    hist = pd.DataFrame({"one": 1.0, "amt": g["amount"].values}, index=ts.values)
    out["txn_count_1h"] = hist["one"].rolling("1h", closed="left").sum().fillna(0).values
    out["txn_count_24h"] = hist["one"].rolling("24h", closed="left").sum().fillna(0).values
    out["txn_count_7d"] = hist["one"].rolling("7D", closed="left").sum().fillna(0).values
    out["amount_sum_24h"] = hist["amt"].rolling("24h", closed="left").sum().fillna(0).values

    # Amount z-score vs the customer's own history (expanding, shift(1)).
    exp_mean = g["amount"].expanding().mean().shift(1)
    exp_std = g["amount"].expanding().std().shift(1)
    z = (g["amount"] - exp_mean) / exp_std.replace(0.0, np.nan)
    out["amount_zscore"] = z.fillna(0.0).values

    # Minutes since the previous transaction (first txn -> 30-day sentinel).
    gap = (ts - ts.shift(1)).dt.total_seconds() / 60.0
    out["mins_since_last_txn"] = gap.fillna(60.0 * 24 * 30).values

    # Device novelty: 1 if this device never appeared in PRIOR rows.
    # duplicated() marks repeats of anything seen strictly above.
    out["device_novelty"] = (~g["device_id"].duplicated()).astype(float).values

    # Category shift: 1 if this merchant category is new for the customer.
    out["category_shift"] = (~g["merchant_category"].duplicated()).astype(float).values

    return out


def build_features(txns: pd.DataFrame) -> pd.DataFrame:
    """Build the 12-feature frame. Input must be the B2 transactions table."""
    df = txns.sort_values(["customer_id", "timestamp"], kind="stable").copy()

    hist_parts = []
    for _, g in df.groupby("customer_id", sort=False):
        hist_parts.append(_per_customer(g))
    hist = pd.concat(hist_parts).reindex(df.index)

    feat = pd.DataFrame(index=df.index)
    feat["transaction_id"] = df["transaction_id"]
    feat["timestamp"] = df["timestamp"]
    feat["customer_id"] = df["customer_id"]

    for c in [
        "txn_count_1h", "txn_count_24h", "txn_count_7d", "amount_sum_24h",
        "amount_zscore", "mins_since_last_txn", "device_novelty", "category_shift",
    ]:
        feat[c] = hist[c]

    feat["category_risk"] = df["merchant_category"].map(CATEGORY_RISK).astype(float)
    feat["is_night"] = (df["timestamp"].dt.hour < 6).astype(float)
    feat["is_international"] = df["is_international"].astype(float)
    feat["log_amount"] = np.log1p(df["amount"])

    # Labels travel WITH the frame but are not features - B4 consumes them
    # via the FEATURES contract and the label_available_mask.
    for c in LABEL_COLUMNS:
        feat[c] = df[c]

    # Restore global chronological order.
    feat = feat.sort_values("timestamp", kind="stable").reset_index(drop=True)
    return feat


# ---------------------------------------------------------------------------
# Splits and label availability (anti-leakage rules 3 and 4)
# ---------------------------------------------------------------------------

def chronological_split(
    feat: pd.DataFrame, ratios: tuple[float, float, float] = SPLIT_RATIOS
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Strict chronological 70/15/15 split. Never shuffles."""
    assert abs(sum(ratios) - 1.0) < 1e-9, "split ratios must sum to 1"
    f = feat.sort_values("timestamp", kind="stable").reset_index(drop=True)
    n = len(f)
    i1 = int(n * ratios[0])
    i2 = int(n * (ratios[0] + ratios[1]))
    train, cal, test = f.iloc[:i1], f.iloc[i1:i2], f.iloc[i2:]
    # Order assertions - the leakage suite re-checks these independently.
    assert train["timestamp"].max() <= cal["timestamp"].min()
    assert cal["timestamp"].max() <= test["timestamp"].min()
    return train, cal, test


def label_available_mask(df: pd.DataFrame, as_of: pd.Timestamp) -> pd.Series:
    """True where the label is legitimately known at `as_of`.

    Anti-leakage rule 3: a model trained at time T may only learn from
    outcomes confirmed by T. B4 must apply this mask to every training cut.
    """
    return df["label_available_date"] <= as_of


# ---------------------------------------------------------------------------
# Pre-train filters (gate: zero flagged features)
# ---------------------------------------------------------------------------

def vif(x: np.ndarray) -> list[float]:
    """Variance inflation factors via least squares (no statsmodels dep)."""
    xs = (x - x.mean(axis=0)) / np.where(x.std(axis=0) == 0, 1, x.std(axis=0))
    n_feat = xs.shape[1]
    out = []
    for i in range(n_feat):
        y = xs[:, i]
        others = np.delete(xs, i, axis=1)
        a = np.column_stack([others, np.ones(len(y))])
        coef, *_ = np.linalg.lstsq(a, y, rcond=None)
        resid = y - a @ coef
        ss_res = float((resid**2).sum())
        ss_tot = float(((y - y.mean()) ** 2).sum())
        r2 = 0.0 if ss_tot == 0 else 1 - ss_res / ss_tot
        out.append(float(1.0 / max(1e-9, 1.0 - r2)))
    return out


def filter_report(feat: pd.DataFrame) -> dict:
    """VIF > 8, missing > 30%, near-zero variance. Flags must be empty."""
    x = feat[FEATURES]
    missing = (x.isna().mean()).to_dict()
    variance = x.var(numeric_only=True).to_dict()
    # Sample for VIF - O(k * n) lstsq is fine but no need for all rows.
    sample = x.dropna().sample(n=min(len(x), 100_000), random_state=0)
    vifs = dict(zip(FEATURES, vif(sample.to_numpy(dtype=float)), strict=True))

    flagged = sorted(
        {f for f, v in vifs.items() if v > 8.0}
        | {f for f, m in missing.items() if m > 0.30}
        | {f for f, v in variance.items() if v < 1e-8}
    )
    return {
        "n_rows": int(len(feat)),
        "features": FEATURES,
        "vif": {k: round(v, 3) for k, v in vifs.items()},
        "missing_rate": {k: round(float(v), 5) for k, v in missing.items()},
        "variance": {k: round(float(v), 5) for k, v in variance.items()},
        "flagged": flagged,
        "thresholds": {"vif": 8.0, "missing": 0.30, "near_zero_variance": 1e-8},
    }


# ---------------------------------------------------------------------------
# Entry point (CWD-independent - B2a discipline)
# ---------------------------------------------------------------------------

def run(data_dir: Path) -> int:
    txns = pd.read_parquet(data_dir / "transactions.parquet")
    feat = build_features(txns)
    train, cal, test = chronological_split(feat)

    report = filter_report(feat)
    report["split"] = {
        "ratios": list(SPLIT_RATIOS),
        "train_rows": int(len(train)),
        "cal_rows": int(len(cal)),
        "test_rows": int(len(test)),
        "train_end": str(train["timestamp"].max()),
        "cal_end": str(cal["timestamp"].max()),
    }

    feat.to_parquet(data_dir / "features.parquet", index=False)
    (data_dir / "feature_report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report[k] for k in ("n_rows", "flagged", "split")}, indent=2))
    return 1 if report["flagged"] else 0


def main() -> None:
    """CWD-independent entry point - safe under DVC, CI, or any shell."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default="data/fraud")
    args = parser.parse_args()
    data_dir = Path(args.data_dir)
    if not data_dir.is_absolute():
        data_dir = REPO_ROOT / data_dir
    sys.exit(run(data_dir))


if __name__ == "__main__":
    main()
