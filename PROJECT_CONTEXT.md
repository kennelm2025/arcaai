# PROJECT CONTEXT

**ArcaAI** — founder-led venture (Mike Kennelly): the AI control layer for regulated
banking decisions. Positioning: mid-market banks get vendor "AI-inside" as the generic
layer; ArcaAI is the bank-controlled, differentiated layer — calibrated ML + grounded
LLM + agentic orchestration under one governance regime, UK-first (PRA/FCA), everything
customer-touching on-prem.

## Operating model

Solo founder + AI-assisted engineering. Two delivery lanes (DP1/DP3): the founder-led
minimum-viable path is operative; the 4–7 FTE plan is the funded case. Current build:
**reference implementation on synthetic data** proving the full stack per vertical —
the WS1.4 demo artefact and the G1–G10 gate regime are the credibility assets.

## Non-negotiables (from the locked suite)

- 11-use-case register; Phase 1 = Fraud, Compliance, RM (R1). Mortgage orchestration is
  a documented pattern, not a register row (ADR-003).
- PostgreSQL from day 1 (R4); self-managed on-prem OpenSearch at Phase 2 (R5); GBP/UK
  regulatory frame (R6); latency ladder per R7; vocabulary rules per R9; no sum-to-one
  normalisation for independent outcomes (R10); Llama pins 3.3-70B/3.1-8B (TI7).
- Gates G1–G10 in full, every model, no exceptions. Coverage ratchet 60%→80%.
- Doc–code drift requires an ADR. Locked docs change via decision record only.
