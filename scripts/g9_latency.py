"""G9 latency harness: P99 < 200ms against the served pinned model.

Sequential single-client measurement on reference hardware. Run with the
BentoML server already up on localhost:3000.
"""
import statistics
import time

import httpx

PAYLOAD = {
    "request": {
        "txn_count_1h": 2,
        "txn_count_24h": 9,
        "txn_count_7d": 41,
        "amount_sum_24h": 350.75,
        "amount_zscore": 1.8,
        "mins_since_last_txn": 14.5,
        "device_novelty": 0,
        "category_shift": 0,
        "category_risk": 0.35,
        "is_night": 0,
        "is_international": 0,
        "log_amount": 4.32,
    }
}
URL = "http://localhost:3000/score"
WARMUP = 20
RUNS = 1000

with httpx.Client(timeout=10.0) as client:
    for _ in range(WARMUP):
        client.post(URL, json=PAYLOAD).raise_for_status()

    samples_ms = []
    for _ in range(RUNS):
        t0 = time.perf_counter()
        r = client.post(URL, json=PAYLOAD)
        elapsed = (time.perf_counter() - t0) * 1000.0
        r.raise_for_status()
        samples_ms.append(elapsed)

samples_ms.sort()
p50 = statistics.quantiles(samples_ms, n=100)[49]
p95 = statistics.quantiles(samples_ms, n=100)[94]
p99 = statistics.quantiles(samples_ms, n=100)[98]
print(f"runs={RUNS}  min={samples_ms[0]:.2f}ms  p50={p50:.2f}ms  "
      f"p95={p95:.2f}ms  p99={p99:.2f}ms  max={samples_ms[-1]:.2f}ms")
print(f"G9 (<200ms P99): {'PASS' if p99 < 200.0 else 'FAIL'}")
