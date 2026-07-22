"""CL-13(c): serve-and-score correctness for the promotion gate.

Scores a fixed reference payload through the serving code path
(FraudScorer.from_pinned_artifacts) and asserts the known answer.
The pinned model is immutable (DVC-hashed), so EXPECTED_P is stable;
any change to artefacts, features, or scoring math fails this gate.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from contracts.fraud_scoring import FraudScoreRequest  # noqa: E402
from verticals.fraud.serving.scorer import FraudScorer  # noqa: E402

REFERENCE_PAYLOAD = {
    "transaction_id": "gate-ref-001",
    "txn_count_1h": 1,
    "txn_count_24h": 4,
    "txn_count_7d": 18,
    "amount_sum_24h": 210.50,
    "amount_zscore": 0.35,
    "mins_since_last_txn": 95.0,
    "device_novelty": 0,
    "category_shift": 0,
    "category_risk": 0.20,
    "is_night": 0,
    "is_international": 0,
    "log_amount": 3.9,
}

EXPECTED_P = 0.005603496450930834  # pinned 2026-07-22 vs artefact c623c3a6
TOLERANCE = 1e-9


def main() -> None:
    scorer = FraudScorer.from_pinned_artifacts()
    resp = scorer.score(FraudScoreRequest(**REFERENCE_PAYLOAD))
    p = resp.calibrated_fraud_probability
    print(f"scored p={p!r}")
    if EXPECTED_P is None:
        print("EXPECTED_P not pinned yet - pin this value and re-run.")
        sys.exit(1)
    ok = abs(p - EXPECTED_P) <= TOLERANCE
    print(f"expected={EXPECTED_P!r} match={ok}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
