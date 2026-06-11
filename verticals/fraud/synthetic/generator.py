"""Fraud synthetic data generator (build stage B2).

Generates a deterministic, seeded synthetic card-transaction dataset for the
fraud vertical reference implementation: customers, merchants, and ~1M
transactions over 17 months with four injected fraud patterns and honest
label-availability dates.

Design rules honoured:
- Deterministic for a given seed (DVC-pinned, reproducible - Blueprint S8.2).
- Labels carry `label_available_date` so downstream stages cannot train on
  outcomes before they would be known in production (anti-leakage rule 3).
- Fraud events are independent binary outcomes - no group normalisation (R10).
- Currency GBP, UK-first frame (R6).

Usage:
    python -m verticals.fraud.synthetic.generator [--config path] [--out dir]
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

UK_REGIONS = [
    "London", "South East", "North West", "West Midlands", "Yorkshire",
    "Scotland", "Wales", "East of England", "South West", "North East",
]
INTL_COUNTRIES = ["IE", "FR", "ES", "US", "DE", "NL", "IT", "PT"]

CATEGORIES = [
    # (name, amount multiplier, merchant risk weight, online share)
    ("grocery", 0.6, 0.2, 0.10),
    ("fuel", 0.7, 0.2, 0.02),
    ("restaurant", 0.8, 0.3, 0.08),
    ("fashion", 1.0, 0.4, 0.45),
    ("online_retail", 1.0, 0.6, 1.00),
    ("electronics", 2.2, 0.8, 0.70),
    ("travel", 3.0, 0.6, 0.80),
    ("entertainment", 0.9, 0.4, 0.55),
    ("utilities", 1.2, 0.1, 0.90),
    ("digital_goods", 0.5, 0.9, 1.00),
    ("gambling", 1.1, 1.0, 0.95),
    ("jewellery", 3.5, 0.9, 0.35),
]
CAT_NAMES = [c[0] for c in CATEGORIES]
CAT_AMT_MULT = {c[0]: c[1] for c in CATEGORIES}
CAT_ONLINE = {c[0]: c[3] for c in CATEGORIES}
HIGH_RISK_CATS = ["electronics", "jewellery", "digital_goods", "gambling", "online_retail"]

CHANNELS = ["pos", "contactless", "online", "atm"]

COLUMNS = [
    "transaction_id", "timestamp", "customer_id", "merchant_id",
    "merchant_category", "merchant_country", "amount", "currency", "channel",
    "device_id", "is_international", "customer_home_region",
    "is_fraud", "fraud_pattern", "label_available_date",
]


# --------------------------------------------------------------------------- #
# Entities
# --------------------------------------------------------------------------- #

def build_customers(rng: np.random.Generator, n: int) -> pd.DataFrame:
    risk = rng.choice(["low", "medium", "high"], size=n, p=[0.6, 0.3, 0.1])
    return pd.DataFrame({
        "customer_id": [f"C{i:05d}" for i in range(n)],
        "home_region": rng.choice(UK_REGIONS, size=n),
        "risk_segment": risk,
        "mean_amount": np.round(rng.lognormal(mean=3.2, sigma=0.5, size=n), 2),  # ~ GBP 25 median
        "txn_rate": np.clip(rng.gamma(shape=4.0, scale=0.25, size=n), 0.15, 4.0),
        "online_propensity": np.clip(rng.beta(2.5, 4.0, size=n), 0.02, 0.95),
        "night_propensity": np.clip(rng.beta(1.2, 12.0, size=n), 0.005, 0.4),
        "intl_propensity": np.clip(rng.beta(1.2, 20.0, size=n), 0.0, 0.5),
        "primary_device": [f"D{i:05d}a" for i in range(n)],
    })


def build_merchants(rng: np.random.Generator, n: int) -> pd.DataFrame:
    cats = rng.choice(CAT_NAMES, size=n)
    intl = rng.random(n) < 0.12
    countries = np.where(intl, rng.choice(INTL_COUNTRIES, size=n), "GB")
    cat_risk = dict(zip(CAT_NAMES, [c[2] for c in CATEGORIES], strict=True))
    risk_w = np.array([cat_risk[c] for c in cats])
    return pd.DataFrame({
        "merchant_id": [f"M{i:05d}" for i in range(n)],
        "category": cats,
        "country": countries,
        "risk_score": np.round(np.clip(risk_w + rng.normal(0, 0.1, n), 0.05, 1.0), 3),
    })


# --------------------------------------------------------------------------- #
# Legitimate traffic
# --------------------------------------------------------------------------- #

def _hours_for(rng: np.random.Generator, n: int, night_prop: float) -> np.ndarray:
    """Hour-of-day mixture: daytime hump, evening hump, thin night tail."""
    pick = rng.random(n)
    day = np.clip(rng.normal(13.5, 3.0, n), 6, 21)
    eve = np.clip(rng.normal(19.5, 1.8, n), 17, 23)
    night = rng.choice([0, 1, 2, 3, 4, 23], size=n)
    hours = np.where(pick < night_prop, night, np.where(pick < night_prop + 0.35, eve, day))
    return hours.astype(int)


def generate_legit(
    rng: np.random.Generator,
    customers: pd.DataFrame,
    merchants: pd.DataFrame,
    cfg: dict,
) -> pd.DataFrame:
    start = datetime.fromisoformat(cfg["window"]["start_date"])
    end = datetime.fromisoformat(cfg["window"]["end_date"])
    n_days = (end - start).days + 1
    base_rate = cfg["behaviour"]["base_txn_rate_per_day"]
    dec_rate = cfg["behaviour"]["december_rate_multiplier"]
    dec_amt = cfg["behaviour"]["december_amount_multiplier"]

    merch_by_cat = {c: merchants.index[merchants["category"] == c].to_numpy() for c in CAT_NAMES}
    frames: list[pd.DataFrame] = []

    for cust in customers.itertuples(index=False):
        n_txn = rng.poisson(base_rate * cust.txn_rate * n_days)
        if n_txn == 0:
            continue
        day_idx = rng.integers(0, n_days, size=n_txn)
        months = pd.DatetimeIndex(pd.to_datetime(start) + pd.to_timedelta(day_idx, unit="D"))
        is_dec = np.asarray(months.month == 12)
        # December volume lift: duplicate a fraction of December rows
        extra = int(is_dec.sum() * (dec_rate - 1.0))
        if extra > 0:
            dec_days = day_idx[is_dec]
            day_idx = np.concatenate([day_idx, rng.choice(dec_days, size=extra)])
            n_txn += extra
            months = pd.DatetimeIndex(pd.to_datetime(start) + pd.to_timedelta(day_idx, unit="D"))
            is_dec = np.asarray(months.month == 12)

        hours = _hours_for(rng, n_txn, cust.night_propensity)
        minutes = rng.integers(0, 60, n_txn)
        seconds = rng.integers(0, 60, n_txn)
        ts = (
            pd.to_datetime(start)
            + pd.to_timedelta(day_idx, unit="D")
            + pd.to_timedelta(hours, unit="h")
            + pd.to_timedelta(minutes, unit="m")
            + pd.to_timedelta(seconds, unit="s")
        )

        # Category preference: stable per customer
        pref = rng.dirichlet(np.ones(len(CAT_NAMES)) * 1.6)
        cats = rng.choice(CAT_NAMES, size=n_txn, p=pref)
        m_idx = np.array([rng.choice(merch_by_cat[c]) for c in cats])
        m_country = merchants["country"].to_numpy()[m_idx]

        amt_mult = np.array([CAT_AMT_MULT[c] for c in cats])
        amounts = rng.lognormal(np.log(cust.mean_amount), 0.65, n_txn) * amt_mult
        amounts = np.where(is_dec, amounts * dec_amt, amounts)
        amounts = np.round(np.clip(amounts, 0.5, 20000.0), 2)

        online_p = np.array([CAT_ONLINE[c] for c in cats]) * 0.5 + cust.online_propensity * 0.5
        is_online = rng.random(n_txn) < online_p
        channel = np.where(
            is_online, "online",
            rng.choice(["pos", "contactless", "atm"], size=n_txn, p=[0.45, 0.50, 0.05]),
        )
        intl = (m_country != "GB") | (rng.random(n_txn) < cust.intl_propensity * 0.1)

        frames.append(pd.DataFrame({
            "timestamp": ts,
            "customer_id": cust.customer_id,
            "merchant_id": merchants["merchant_id"].to_numpy()[m_idx],
            "merchant_category": cats,
            "merchant_country": m_country,
            "amount": amounts,
            "channel": channel,
            "device_id": np.where(
                channel == "online", cust.primary_device, "POS-TERMINAL"
            ),
            "is_international": intl,
            "customer_home_region": cust.home_region,
            "is_fraud": 0,
            "fraud_pattern": "none",
        }))

    return pd.concat(frames, ignore_index=True)


# --------------------------------------------------------------------------- #
# Fraud pattern injection
# --------------------------------------------------------------------------- #

def _fraud_frame(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    df["is_fraud"] = 1
    return df


def inject_spree(rng, customers, merchants, cfg, start, end) -> pd.DataFrame:
    """Stolen-card burst: rapid escalating transactions at high-risk merchants."""
    rows = []
    hi_risk = merchants[merchants["category"].isin(HIGH_RISK_CATS)]
    horizon = (end - start).days - 1
    for _ in range(cfg["fraud"]["spree_incidents"]):
        cust = customers.iloc[rng.integers(0, len(customers))]
        t0 = start + timedelta(
            days=int(rng.integers(0, horizon)),
            hours=int(rng.choice([0, 1, 2, 3, 22, 23, 11, 15])),
            minutes=int(rng.integers(0, 60)),
        )
        n = int(rng.integers(5, 16))
        gaps = np.cumsum(rng.exponential(scale=8.0, size=n))  # minutes
        base = float(rng.uniform(15, 60))
        for k in range(n):
            m = hi_risk.iloc[rng.integers(0, len(hi_risk))]
            rows.append({
                "timestamp": t0 + timedelta(minutes=float(gaps[k])),
                "customer_id": cust["customer_id"],
                "merchant_id": m["merchant_id"],
                "merchant_category": m["category"],
                "merchant_country": m["country"],
                "amount": round(min(base * (1.45 ** k) * rng.uniform(0.8, 1.3), 9500.0), 2),
                "channel": "online" if rng.random() < 0.7 else "pos",
                "device_id": f"DX{rng.integers(0, 99999):05d}",  # attacker device
                "is_international": bool(rng.random() < 0.45),
                "customer_home_region": cust["home_region"],
                "fraud_pattern": "spree",
            })
    return _fraud_frame(rows)


def inject_testing(rng, customers, merchants, cfg, start, end) -> pd.DataFrame:
    """Card testing: micro-amounts in quick succession online, often a final strike."""
    rows = []
    online = merchants[merchants["category"].isin(["online_retail", "digital_goods"])]
    horizon = (end - start).days - 1
    for _ in range(cfg["fraud"]["testing_incidents"]):
        cust = customers.iloc[rng.integers(0, len(customers))]
        t0 = start + timedelta(
            days=int(rng.integers(0, horizon)),
            hours=int(rng.choice([1, 2, 3, 4, 5, 14, 20])),
            minutes=int(rng.integers(0, 60)),
        )
        n = int(rng.integers(6, 21))
        gaps = np.cumsum(rng.exponential(scale=1.5, size=n))
        device = f"DX{rng.integers(0, 99999):05d}"
        for k in range(n):
            m = online.iloc[rng.integers(0, len(online))]
            rows.append({
                "timestamp": t0 + timedelta(minutes=float(gaps[k])),
                "customer_id": cust["customer_id"],
                "merchant_id": m["merchant_id"],
                "merchant_category": m["category"],
                "merchant_country": m["country"],
                "amount": round(float(rng.uniform(0.5, 2.0)), 2),
                "channel": "online",
                "device_id": device,
                "is_international": bool(rng.random() < 0.35),
                "customer_home_region": cust["home_region"],
                "fraud_pattern": "testing",
            })
        if rng.random() < 0.7:  # the strike
            m = online.iloc[rng.integers(0, len(online))]
            rows.append({
                "timestamp": t0 + timedelta(minutes=float(gaps[-1]) + float(rng.uniform(3, 25))),
                "customer_id": cust["customer_id"],
                "merchant_id": m["merchant_id"],
                "merchant_category": m["category"],
                "merchant_country": m["country"],
                "amount": round(float(rng.uniform(200, 900)), 2),
                "channel": "online",
                "device_id": device,
                "is_international": bool(rng.random() < 0.35),
                "customer_home_region": cust["home_region"],
                "fraud_pattern": "testing",
            })
    return _fraud_frame(rows)


def inject_takeover(rng, customers, merchants, cfg, start, end) -> pd.DataFrame:
    """Account takeover: new device, elevated amounts, spread over days."""
    rows = []
    horizon = (end - start).days - 5
    for _ in range(cfg["fraud"]["takeover_incidents"]):
        cust = customers.iloc[rng.integers(0, len(customers))]
        t0 = start + timedelta(days=int(rng.integers(0, horizon)), hours=int(rng.integers(0, 24)))
        n = int(rng.integers(3, 10))
        device = f"DX{rng.integers(0, 99999):05d}"
        offsets_h = np.sort(rng.uniform(0, 24 * rng.integers(1, 5), size=n))
        for k in range(n):
            m = merchants.iloc[rng.integers(0, len(merchants))]
            rows.append({
                "timestamp": t0 + timedelta(hours=float(offsets_h[k])),
                "customer_id": cust["customer_id"],
                "merchant_id": m["merchant_id"],
                "merchant_category": m["category"],
                "merchant_country": m["country"],
                "amount": round(float(cust["mean_amount"]) * float(rng.uniform(1.5, 4.0)), 2),
                "channel": "online",
                "device_id": device,
                "is_international": bool(rng.random() < 0.3),
                "customer_home_region": cust["home_region"],
                "fraud_pattern": "takeover",
            })
    return _fraud_frame(rows)


def inject_first_party(rng, legit: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Relabel a thin slice of high-amount online legit txns - the hard cases."""
    candidates = legit.index[
        (legit["channel"] == "online")
        & (legit["amount"] > legit["amount"].quantile(0.75))
    ].to_numpy()
    n = int(len(legit) * cfg["fraud"]["first_party_rate"])
    chosen = rng.choice(candidates, size=min(n, len(candidates)), replace=False)
    legit.loc[chosen, "is_fraud"] = 1
    legit.loc[chosen, "fraud_pattern"] = "first_party"
    return legit


# --------------------------------------------------------------------------- #
# Assembly
# --------------------------------------------------------------------------- #

def add_labels_and_ids(rng, df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    df = df.sort_values("timestamp", kind="mergesort").reset_index(drop=True)
    df["transaction_id"] = [f"T{i:08d}" for i in range(len(df))]
    fraud_lag = rng.gamma(shape=3.0, scale=cfg["label_lag"]["fraud_mean_days"] / 3.0, size=len(df))
    fraud_lag = np.clip(fraud_lag, 1.0, 90.0)
    settle = float(cfg["label_lag"]["nonfraud_settle_days"])
    lag_days = np.where(df["is_fraud"] == 1, fraud_lag, settle)
    df["label_available_date"] = df["timestamp"] + pd.to_timedelta(lag_days, unit="D")
    df["currency"] = "GBP"
    df["is_international"] = df["is_international"].astype(bool)
    df["amount"] = df["amount"].astype(float)
    return df[COLUMNS]


def profile(df: pd.DataFrame) -> dict:
    by_pattern = df[df["is_fraud"] == 1]["fraud_pattern"].value_counts().to_dict()
    content = pd.util.hash_pandas_object(
        df[["timestamp", "customer_id", "amount", "is_fraud"]], index=False
    ).to_numpy()
    digest = hashlib.sha256(content.tobytes()).hexdigest()[:16]
    return {
        "rows": int(len(df)),
        "customers": int(df["customer_id"].nunique()),
        "merchants": int(df["merchant_id"].nunique()),
        "date_min": str(df["timestamp"].min()),
        "date_max": str(df["timestamp"].max()),
        "fraud_rows": int(df["is_fraud"].sum()),
        "fraud_rate": round(float(df["is_fraud"].mean()), 6),
        "fraud_by_pattern": {k: int(v) for k, v in by_pattern.items()},
        "content_hash": digest,
    }


def generate(cfg: dict) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    rng = np.random.default_rng(cfg["seed"])
    start = datetime.fromisoformat(cfg["window"]["start_date"])
    end = datetime.fromisoformat(cfg["window"]["end_date"])

    customers = build_customers(rng, cfg["population"]["customers"])
    merchants = build_merchants(rng, cfg["population"]["merchants"])

    legit = generate_legit(rng, customers, merchants, cfg)
    legit = inject_first_party(rng, legit, cfg)
    fraud = pd.concat(
        [
            inject_spree(rng, customers, merchants, cfg, start, end),
            inject_testing(rng, customers, merchants, cfg, start, end),
            inject_takeover(rng, customers, merchants, cfg, start, end),
        ],
        ignore_index=True,
    )
    txns = pd.concat([legit, fraud], ignore_index=True)
    txns = txns[txns["timestamp"] <= pd.Timestamp(end) + pd.Timedelta(days=1)]
    txns = add_labels_and_ids(rng, txns, cfg)
    return txns, customers, merchants, profile(txns)


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG = Path(__file__).with_name("config.yaml")


def main() -> None:
    """CWD-independent entry point - safe under DVC, CI, or any shell."""
    parser = argparse.ArgumentParser(description="ArcaAI fraud synthetic data generator (B2)")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--out", default=None, help="Override out_dir from config")
    args = parser.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    out_dir = Path(args.out or cfg["out_dir"])
    if not out_dir.is_absolute():
        out_dir = REPO_ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    txns, customers, merchants, prof = generate(cfg)
    txns.to_parquet(out_dir / "transactions.parquet", index=False)
    customers.to_parquet(out_dir / "customers.parquet", index=False)
    merchants.to_parquet(out_dir / "merchants.parquet", index=False)
    (out_dir / "data_profile.json").write_text(json.dumps(prof, indent=2), encoding="utf-8")

    print(json.dumps(prof, indent=2))


if __name__ == "__main__":
    main()
