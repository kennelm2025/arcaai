"""Great Expectations validation for the fraud synthetic dataset (B2, gate G1).

Defines the expectation suite and runs it against the generated parquet.
Pass condition (Blueprint G1): anomaly rate < 5% on row-level expectations,
zero schema violations, zero impossible values. Writes validation_report.json
next to the data and exits non-zero on failure so DVC/CI can gate on it.

Usage:
    python -m verticals.fraud.validation.run_validation [--data-dir data/fraud]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import great_expectations as gx
import pandas as pd

EXPECTED_COLUMNS = [
    "transaction_id", "timestamp", "customer_id", "merchant_id",
    "merchant_category", "merchant_country", "amount", "currency", "channel",
    "device_id", "is_international", "customer_home_region",
    "is_fraud", "fraud_pattern", "label_available_date",
]

CATEGORIES = [
    "grocery", "fuel", "restaurant", "fashion", "online_retail", "electronics",
    "travel", "entertainment", "utilities", "digital_goods", "gambling", "jewellery",
]
CHANNELS = ["pos", "contactless", "online", "atm"]
PATTERNS = ["none", "spree", "testing", "takeover", "first_party"]

ANOMALY_GATE = 0.05  # Blueprint G1: anomaly rate < 5%
FRAUD_RATE_BAND = (0.001, 0.01)  # documented synthetic design band


def build_suite() -> gx.ExpectationSuite:
    e = gx.expectations
    suite = gx.ExpectationSuite(name="fraud_transactions_v1")
    add = suite.add_expectation

    # Schema
    add(e.ExpectTableColumnsToMatchSet(column_set=EXPECTED_COLUMNS, exact_match=True))

    # Keys
    add(e.ExpectColumnValuesToNotBeNull(column="transaction_id"))
    add(e.ExpectColumnValuesToBeUnique(column="transaction_id"))
    add(e.ExpectColumnValuesToNotBeNull(column="customer_id"))
    add(e.ExpectColumnValuesToNotBeNull(column="merchant_id"))
    add(e.ExpectColumnValuesToNotBeNull(column="timestamp"))

    # Impossible values
    add(e.ExpectColumnValuesToBeBetween(column="amount", min_value=0.01, max_value=20000))
    add(e.ExpectColumnValuesToBeInSet(column="currency", value_set=["GBP"]))
    add(e.ExpectColumnValuesToBeInSet(column="channel", value_set=CHANNELS))
    add(e.ExpectColumnValuesToBeInSet(column="merchant_category", value_set=CATEGORIES))
    add(e.ExpectColumnValuesToBeInSet(column="is_fraud", value_set=[0, 1]))
    add(e.ExpectColumnValuesToBeInSet(column="fraud_pattern", value_set=PATTERNS))

    # Distributional sanity
    add(e.ExpectColumnMeanToBeBetween(
        column="is_fraud", min_value=FRAUD_RATE_BAND[0], max_value=FRAUD_RATE_BAND[1]
    ))
    add(e.ExpectColumnValuesToBeBetween(
        column="timestamp",
        min_value="2025-01-01T00:00:00",
        max_value="2026-06-02T00:00:00",
    ))
    return suite


def label_integrity_checks(df: pd.DataFrame) -> list[dict]:
    """Checks GE can't express cleanly - run as explicit assertions."""
    checks = []

    lag_ok = (df["label_available_date"] > df["timestamp"]).all()
    checks.append({
        "check": "label_available_date strictly after timestamp (no time travel)",
        "success": bool(lag_ok),
    })

    fraud = df[df["is_fraud"] == 1]
    pattern_ok = (fraud["fraud_pattern"] != "none").all()
    checks.append({
        "check": "every fraud row carries a named pattern",
        "success": bool(pattern_ok),
    })

    legit = df[df["is_fraud"] == 0]
    legit_ok = (legit["fraud_pattern"] == "none").all()
    checks.append({
        "check": "no legit row carries a fraud pattern",
        "success": bool(legit_ok),
    })

    sorted_ok = df["timestamp"].is_monotonic_increasing
    checks.append({
        "check": "dataset sorted chronologically (split discipline, rule 4)",
        "success": bool(sorted_ok),
    })
    return checks


def run(data_dir: Path) -> int:
    df = pd.read_parquet(data_dir / "transactions.parquet")

    context = gx.get_context(mode="ephemeral")
    batch = (
        context.data_sources.add_pandas("pandas")
        .add_dataframe_asset("transactions")
        .add_batch_definition_whole_dataframe("batch")
        .get_batch(batch_parameters={"dataframe": df})
    )
    result = batch.validate(build_suite())

    rows = len(df)
    worst_anomaly = 0.0
    expectation_results = []
    for r in result.results:
        unexpected = r.result.get("unexpected_count", 0) if r.result else 0
        frac = (unexpected / rows) if rows else 0.0
        worst_anomaly = max(worst_anomaly, frac)
        expectation_results.append({
            "expectation": r.expectation_config.type,
            "column": r.expectation_config.kwargs.get("column", "<table>"),
            "success": bool(r.success),
            "unexpected_fraction": round(frac, 6),
        })

    integrity = label_integrity_checks(df)

    ge_pass = bool(result.success)
    integrity_pass = all(c["success"] for c in integrity)
    anomaly_pass = worst_anomaly < ANOMALY_GATE
    overall = ge_pass and integrity_pass and anomaly_pass

    report = {
        "dataset": str(data_dir / "transactions.parquet"),
        "rows": rows,
        "gate": "G1 - Data Foundation",
        "overall_success": overall,
        "ge_suite_success": ge_pass,
        "worst_anomaly_fraction": round(worst_anomaly, 6),
        "anomaly_gate": ANOMALY_GATE,
        "expectations": expectation_results,
        "integrity_checks": integrity,
    }
    out = data_dir / "validation_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"GE suite: {'PASS' if ge_pass else 'FAIL'} | "
          f"integrity: {'PASS' if integrity_pass else 'FAIL'} | "
          f"worst anomaly {worst_anomaly:.4%} (gate {ANOMALY_GATE:.0%}) | "
          f"report: {out}")
    return 0 if overall else 1


REPO_ROOT = Path(__file__).resolve().parents[3]


def main() -> None:
    """CWD-independent entry point - safe under DVC, CI, or any shell."""
    parser = argparse.ArgumentParser(description="Validate fraud synthetic data (G1)")
    parser.add_argument("--data-dir", default="data/fraud")
    args = parser.parse_args()
    data_dir = Path(args.data_dir)
    if not data_dir.is_absolute():
        data_dir = REPO_ROOT / data_dir
    sys.exit(run(data_dir))


if __name__ == "__main__":
    main()
