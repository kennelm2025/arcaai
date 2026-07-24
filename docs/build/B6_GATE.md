# B6 GATE — LangGraph agent v0 + LLM (Llama 3.1 8B)

Status: GATE PASSED — July 2026
Evidence increment: inc5 (this PR). Prior increments: inc1 (LLM smoke,
TI7 pin), inc2 (hello-graph), inc3 (score node, HTTP to B5 service),
inc4 (packaging node) — PRs #18, #19, #20 (+ #21 tracker fix).

## Gate test — end-to-end latency vs R7

Reference: Banking Architecture v1.0b §5.5 (Inference latency), applying
cross-document ruling R7 (latency ladder). Harness:
`scripts/b6_inc5_latency.py`. Full graph, live_scoring=True +
live_packaging=True, INTAKE_FIXTURE (inc3 fraud-flavoured vector,
scores 0.9865). Reference hardware: RTX 3070 8GB (LLM), same machine
as B5 G9 host.

| R7 rung | Target | Result | Status |
|---|---|---|---|
| Conversational query SLA | < 15 s | warm max 4.10 s (n=20) | **PASS** |
| Synchronous API | < 10 s | warm max 4.10 s (same run) | **PASS** |
| Conversational typical band | 5–10 s | median 3.64 s — below band | noted |
| ML scoring | P99 < 200 ms | P99 ~33 ms — cited from B5 G9, not re-measured | PASS (B5) |
| Retrieval | < 100 ms | no RAG until B7 | deferred (deliberate) |

Warm distribution (n=20): min 3.58 s / median 3.64 s / mean 3.68 s /
max 4.10 s. Gate statistic is warm max — a conservative stand-in for
P99 at this sample size; no P99 claim is made from n=20.

True cold start (model evicted via `ollama stop`, load from disk +
first generation): **7.41 s** — reported separately, outside gate
scope, though it also meets both SLA lines. Post-reload warm runs
(3.37–3.85 s, n=3) confirm the main set is representative.

Note on prior estimate: inc4 measured 1.82 s for short probe prose;
the full governed note (~250 chars) plus graph orchestration and the
HTTP scoring hop lands at ~3.6 s. The difference is output length and
end-to-end scope, not regression.

## Finding fixed at this gate — provenance key mismatch

The first live end-to-end run (this increment) failed immediately:
`agent/packaging.py` read `provenance["sha256"]` and
`provenance["platt_params"]`, while the score node emits
`artifact_sha256` and `platt_a`/`platt_b` (as asserted by
tests/test_score_node.py). All prior packaging tests passed against an
invented canned fixture carrying the wrong keys — the mismatch was
structurally invisible to unit tests. The `platt_params` variant was
the worse defect: no exception, just a governed note stating
calibration parameters were absent when present.

Remediation in this PR: packaging.py conformed to the live keys;
fixtures consolidated into `agent/fixtures.py` (INTAKE_FIXTURE,
SCORED_FIXTURE) with SCORED_FIXTURE mirroring live score-node output
shape and the real B5 artifact sha256. Logged as WS-E 34.

## Rider closed

Prompt relabel ("sha256 (prefix)" → "artifact prefix") folded into the
packaging.py fix; live test re-verified verbatim prefix emission under
the new label.

## Out of scope, carried forward

- Retrieval rung of R7 → B7 gate.
- prompts/ scaffold decision unchanged (deferred to B8, per inc4).
- B6 remains agent v0: single vertical, single query shape. Multi-turn
  and query classification are later-stage concerns.
