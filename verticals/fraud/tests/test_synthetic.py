"""Synthetic generator tests (B2) - run at small scale so CI stays fast."""

import pandas as pd
import pytest

from verticals.fraud.synthetic.generator import COLUMNS, generate

SMALL_CFG = {
    "seed": 7,
    "population": {"customers": 150, "merchants": 80},
    "window": {"start_date": "2025-06-01", "end_date": "2025-09-30"},
    "behaviour": {
        "base_txn_rate_per_day": 0.8,
        "december_rate_multiplier": 1.35,
        "december_amount_multiplier": 1.2,
    },
    "fraud": {
        "spree_incidents": 20,
        "testing_incidents": 10,
        "takeover_incidents": 8,
        "first_party_rate": 0.0004,
    },
    "label_lag": {"fraud_mean_days": 18, "nonfraud_settle_days": 45},
    "out_dir": "unused",
}


@pytest.fixture(scope="module")
def dataset():
    txns, customers, merchants, prof = generate(SMALL_CFG)
    return txns, customers, merchants, prof


def test_schema(dataset) -> None:
    txns, _, _, _ = dataset
    assert list(txns.columns) == COLUMNS
    assert txns["transaction_id"].is_unique
    assert txns["amount"].min() > 0
    assert set(txns["currency"]) == {"GBP"}


def test_determinism_same_seed_same_hash(dataset) -> None:
    _, _, _, prof1 = dataset
    _, _, _, prof2 = generate(SMALL_CFG)
    assert prof1["content_hash"] == prof2["content_hash"]
    assert prof1["rows"] == prof2["rows"]


def test_different_seed_different_data() -> None:
    cfg = dict(SMALL_CFG, seed=8)
    _, _, _, prof = generate(cfg)
    base = generate(SMALL_CFG)[3]
    assert prof["content_hash"] != base["content_hash"]


def test_fraud_labelling_integrity(dataset) -> None:
    txns, _, _, _ = dataset
    fraud = txns[txns["is_fraud"] == 1]
    legit = txns[txns["is_fraud"] == 0]
    assert (fraud["fraud_pattern"] != "none").all()
    assert (legit["fraud_pattern"] == "none").all()
    assert set(fraud["fraud_pattern"]).issubset({"spree", "testing", "takeover", "first_party"})


def test_no_label_time_travel(dataset) -> None:
    txns, _, _, _ = dataset
    assert (txns["label_available_date"] > txns["timestamp"]).all()


def test_chronological_order_and_window(dataset) -> None:
    txns, _, _, _ = dataset
    assert txns["timestamp"].is_monotonic_increasing
    assert txns["timestamp"].min() >= pd.Timestamp("2025-06-01")
    assert txns["timestamp"].max() <= pd.Timestamp("2025-10-02")


def test_fraud_rate_in_design_band(dataset) -> None:
    txns, _, _, prof = dataset
    # Small-scale band is wider than production config but must stay plausible
    assert 0.001 < prof["fraud_rate"] < 0.03
    assert prof["fraud_rows"] == int(txns["is_fraud"].sum())


def test_spree_is_burst_shaped(dataset) -> None:
    txns, _, _, _ = dataset
    spree = txns[txns["fraud_pattern"] == "spree"]
    # at least one victim has 5+ spree txns inside a 6-hour window
    found = False
    for _, g in spree.groupby("customer_id"):
        if len(g) >= 5 and (g["timestamp"].max() - g["timestamp"].min()) < pd.Timedelta(hours=6):
            found = True
            break
    assert found, "spree pattern lost its burst shape"


def test_attacker_devices_differ_from_customer_device(dataset) -> None:
    txns, customers, _, _ = dataset
    fraud_online = txns[(txns["is_fraud"] == 1) & (txns["fraud_pattern"] != "first_party")]
    primary = dict(zip(customers["customer_id"], customers["primary_device"], strict=True))
    mismatch = (
        fraud_online["device_id"]
        != fraud_online["customer_id"].map(primary)
    ).mean()
    assert mismatch > 0.9  # injected fraud overwhelmingly uses unfamiliar devices


def test_first_party_looks_legit() -> None:
    """The hard cases: first-party rows are drawn from genuine behaviour."""
    txns, _, _, _ = generate(SMALL_CFG)
    fp = txns[txns["fraud_pattern"] == "first_party"]
    if len(fp) == 0:
        pytest.skip("no first-party rows at this scale")
    assert (fp["channel"] == "online").all()
    assert fp["amount"].median() > txns["amount"].median()
