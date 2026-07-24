# ArcaAI — BUILD_TRACKER.md

*Living build tracker (ruling EB8 — the Blueprint §18 table is frozen; this file is the truth).*

Status: NOT STARTED / IN PROGRESS / COMPLETE / GATE PASSED. Update at every gate review.

> **Schedule variance note (24 Jul 2026, Checkpoint 01 RAT-01).** The
> week column from Build & Quality Plan v1.0 has been removed. The
> build began early June 2026; B6 gated 24 Jul at roughly plan-week 7
> against a planned week 4–5, and the week model was never
> re-baselined. Per Checkpoint 01 (unanimous), gates are the official
> schedule: current gate, next gate, entry/exit criteria, and the
> actual-date column below. This note is the one-time variance record;
> the week model is closed, not restated.

## Phase 0 — Lockdown

| # | Item | Status | Date |
| --- | --- | --- | --- |
| 0.1 | Rulings R1–R13 decided and recorded | GATE PASSED | Jun 2026 |
| 0.2 | High-severity items applied (LB1, BA1, BA2, SA1, SA2, TI1, EB1, EB2, DP1) | GATE PASSED | Jun 2026 |
| 0.3 | Medium items applied; image round | COMPLETE (image round deferred — DEC-0000) | Jun 2026 |
| 0.4 | Suite version-bumped and frozen | GATE PASSED | Jun 2026 |
| 0.5 | GitHub monorepo created; CI skeleton; this tracker + DECISIONS.md committed | GATE PASSED | Jun 2026 |

## Build stages (Build & Quality Plan v1.0; week column retired — see variance note)

| Stage | Scope | DevOps | MLOps | Gate | Date |
| --- | --- | --- | --- | --- | --- |
| B1 | Foundation — repo, CI, Postgres, MLflow, DVC | COMPLETE | COMPLETE | GATE PASSED | Jun 2026 |
| B2 | Synthetic data — fraud (generator, GE suite, data dictionary) | COMPLETE | COMPLETE | GATE PASSED | Jun 2026 |
| B3 | Fraud features + anti-leakage suite | COMPLETE | COMPLETE | GATE PASSED | Jun 2026 |
| B4 | Baseline + MVM + calibration (fraud) | COMPLETE | COMPLETE | GATE PASSED | Jun 2026 |
| B5 | BentoML serving + FastAPI + contracts | COMPLETE — inc1 (PR #5, `5f4e570`), inc2 (PR #11, `5f3d3d5`) | COMPLETE | GATE PASSED | Jul 2026 |
| B6 | LangGraph agent v0 + LLM (Llama 3.1 8B) | COMPLETE — 5 incs (PRs #18–#20, #22); gate evidence docs/build/B6_GATE.md | COMPLETE | GATE PASSED | Jul 2026 |
| B7 | Fraud RAG (ChromaDB, 50+ seed docs, RAGAS) | NOT STARTED | NOT STARTED | NOT STARTED | |
| B8 | Guardrails (Presidio, OPA, grounding, injection detector selection) | NOT STARTED | NOT STARTED | NOT STARTED | |
| B9 | Chat UI + audit-trail replay (→ WS1.4 artefact) | NOT STARTED | NOT STARTED | NOT STARTED | |
| B9.5 | Platform Extraction (ADR-0009 / DEC-0005): extract ML lifecycle machinery to platform layer; vertical-neutral contracts; exit = 2nd vertical consumes, not copies | NOT STARTED | NOT STARTED | NOT STARTED | |
| B10 | Instantiate — Compliance + RM verticals against the platform template (restated per ADR-0009; gated by B9.5 exit) | NOT STARTED | NOT STARTED | NOT STARTED | |
| B11 | Observability — Grafana 8 panels, Evidently, kill-switch drill | NOT STARTED | NOT STARTED | NOT STARTED | |
| B12 | Hardening + demo pack (3 scripts, 70B demo config, deploy guide v0) | NOT STARTED | NOT STARTED | NOT STARTED | |

## Gate review checklist (standing — Checkpoint 01)

Every `B*_GATE.md` from B7 onward answers both standing questions:

1. **Decision capture (CL-08 / Q-A5):** What architecturally
   significant decisions were taken since the last gate?
   → None | Existing ADR covers | DEC log only | New ADR required.
2. **Architecture conformance (Checkpoint 01 CF-1):** Does this
   increment conform to the Banking Architecture and applicable ADRs?
   → Yes | Deviation recorded as DEC | New ADR required.

Every `B*_GATE.md` from B7 onward also carries a **Gate Acceptance
Record** section (Checkpoint 01 RAT-04): evidence list (links/hashes);
producer statement; approver statement (same person permitted, both
statements mandatory); residual risks accepted into next stage;
decision Pass / Conditional Pass / Fail; approval date.

## Open items / longest-lead dependencies

- [ ] G10 external domain reviewers — one per vertical (recruit now; longest lead time); brief extended to document narrative review (DEC-0003/D8)
- [ ] DEC-0000 image round — Banking Architecture figs 1.1/3.1/4.1/5.1, Learning Bank figs 1–3; deck diagram regeneration for residual source defects per DEC-0001 (NOW GATES CLIENT USE per DEC-0003/D5; + Figure 4.2 mortgage flow)
- [x] DEC-0001 — deck rasters enhanced + content-patched → Executive Presentation v2a (Jun 2026)
- [ ] WS3.1 deck design pass — start after B9 screenshots; include use-case roadmap one-pager (DEC-0003/D6)
- [ ] GPU rental plan for B12 70B demo configuration

## DEC index

See DECISIONS.md (next DEC number = tail of the DEC series there; do not duplicate it here).
