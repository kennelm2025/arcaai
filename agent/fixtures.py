"""Shared test/evidence fixtures - single source of truth.

INTAKE_FIXTURE: raw fraud-flavoured transaction (inc3 probe vector;
scores 0.9865 against the B5 service). Feed to full graph runs.

SCORED_FIXTURE: post-scoring state for packaging-layer tests. Provenance
keys mirror the LIVE score-node output shape (artifact_sha256, platt_a,
platt_b) - asserted by tests/test_score_node.py - and the sha256 is the
real B5 artifact hash. Do not invent canned shapes: the inc5 live run
caught a key mismatch (sha256 vs artifact_sha256, platt_params vs
platt_a/platt_b) that unit tests on an invented fixture could not see.
"""

INTAKE_FIXTURE = {
    "query": "assess",
    "transaction": {
        "transaction_id": "inc3-test-001",
        "txn_count_1h": 2,
        "txn_count_24h": 9,
        "txn_count_7d": 41,
        "amount_sum_24h": 640.0,
        "amount_zscore": 3.1,
        "mins_since_last_txn": 4.0,
        "device_novelty": 1,
        "category_shift": 1,
        "category_risk": 0.8,
        "is_night": 1,
        "is_international": 1,
        "log_amount": 6.4,
    },
}

SCORED_FIXTURE = {
    "query": "assess this transaction",
    "score": 0.9865,
    "provenance": {
        "artifact_sha256": (
            "c623c3a604193ee4636fcb4da90caf298e5302c6509e6d35b7883eea625728c0"
        ),
        "platt_a": -1.0,
        "platt_b": 0.5,
    },
}
