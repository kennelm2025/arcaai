"""B6 inc5 — end-to-end graph latency vs R7.

Measures full graph runs (live_scoring=True, live_packaging=True) against
the R7 latency ladder (Banking Architecture v1.0b §5.5, Inference latency;
ruling R7 in the cross-document rulings register):

    ML scoring            P99 < 200 ms   (proven at B5 G9: ~33 ms — cited, not re-measured)
    Retrieval             < 100 ms       (B7 rung — no RAG yet; explicitly deferred)
    Conversational query  typ 5-10 s, SLA < 15 s   <-- THIS GATE
    Synchronous API       < 10 s         (reported against; same measurement)

Gate statistic: WARM max (conservative stand-in for P99 at small n).
Cold start (first invocation after service start) reported separately,
outside gate scope.

Prerequisites (both live simultaneously):
    - Ollama serving llama3.1:8b
    - bentoml serve verticals.fraud.serving.bento_service:FraudScoringService

Usage:
    python scripts/b6_inc5_latency.py [--runs 20]

Not part of the test suite — evidence generator for the B6 gate doc.
"""

from __future__ import annotations

import argparse
import json
import statistics
import time

from agent.fixtures import INTAKE_FIXTURE as QUERY_STATE

# --- adjust these two imports to match repo names if they differ ----------
from agent.graph import build_graph

# --------------------------------------------------------------------------

R7_SLA_CONVERSATIONAL_S = 15.0
R7_SLA_API_SYNC_S = 10.0
R7_TYPICAL_LOW_S, R7_TYPICAL_HIGH_S = 5.0, 10.0


def timed_invoke(graph, state) -> tuple[float, dict]:
    t0 = time.perf_counter()
    result = graph.invoke(state)
    return time.perf_counter() - t0, result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=20, help="warm runs (default 20)")
    args = parser.parse_args()

    graph = build_graph(live_scoring=True, live_packaging=True)

    # --- cold start: first invocation after service start ---
    cold_s, cold_result = timed_invoke(graph, QUERY_STATE)
    narrative = cold_result.get("narrative", "")
    print(f"cold-start: {cold_s:.2f}s  (narrative {len(narrative)} chars)")
    if not narrative:
        print("FAIL: cold run produced no narrative — aborting before warm runs")
        return 1

    # --- warm runs ---
    warm: list[float] = []
    for i in range(args.runs):
        dt, result = timed_invoke(graph, QUERY_STATE)
        warm.append(dt)
        ok = "ok" if result.get("narrative") else "NO NARRATIVE"
        print(f"warm {i + 1:>3}/{args.runs}: {dt:.2f}s  {ok}")

    w_min, w_max = min(warm), max(warm)
    w_med = statistics.median(warm)
    w_mean = statistics.fmean(warm)

    summary = {
        "runs_warm": args.runs,
        "cold_start_s": round(cold_s, 2),
        "warm_min_s": round(w_min, 2),
        "warm_median_s": round(w_med, 2),
        "warm_mean_s": round(w_mean, 2),
        "warm_max_s": round(w_max, 2),
        "r7_sla_conversational_s": R7_SLA_CONVERSATIONAL_S,
        "r7_sla_api_sync_s": R7_SLA_API_SYNC_S,
    }
    print("\n=== R7 evidence summary ===")
    print(json.dumps(summary, indent=2))

    gate_pass = w_max < R7_SLA_CONVERSATIONAL_S
    api_pass = w_max < R7_SLA_API_SYNC_S
    in_typical = R7_TYPICAL_LOW_S <= w_med <= R7_TYPICAL_HIGH_S
    below_typical = w_med < R7_TYPICAL_LOW_S

    print(f"\nGATE  (warm max {w_max:.2f}s < {R7_SLA_CONVERSATIONAL_S:.0f}s SLA): "
          f"{'PASS' if gate_pass else 'FAIL'}")
    print(f"API   (warm max {w_max:.2f}s < {R7_SLA_API_SYNC_S:.0f}s):     "
          f"{'PASS' if api_pass else 'FAIL'}")
    print(f"Typical band (median {w_med:.2f}s vs 5-10s): "
          f"{'within' if in_typical else ('below (fine)' if below_typical else 'ABOVE')}")
    print(f"Cold start {cold_s:.2f}s — reported, not gated.")

    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
