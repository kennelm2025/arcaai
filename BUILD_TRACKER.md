# ArcaAI — BUILD_TRACKER.md

Living build tracker (ruling EB8 — the Blueprint §18 table is frozen; this file is the truth).
Status: NOT STARTED / IN PROGRESS / COMPLETE / GATE PASSED. Update at every gate review.

## Phase 0 — Lockdown

| # | Item | Status | Date |
|---|------|--------|------|
| 0.1 | Rulings R1–R13 decided and recorded | GATE PASSED | Jun 2026 |
| 0.2 | High-severity items applied (LB1, BA1, BA2, SA1, SA2, TI1, EB1, EB2, DP1) | GATE PASSED | Jun 2026 |
| 0.3 | Medium items applied; image round | COMPLETE (image round deferred — ADR-000) | Jun 2026 |
| 0.4 | Suite version-bumped and frozen | GATE PASSED | Jun 2026 |
| 0.5 | GitHub monorepo created; CI skeleton; this tracker + DECISIONS.md committed | GATE PASSED | Jun 2026 |

## Build stages (Build & Quality Plan v1.0)

| Stage | Wk | Scope | DevOps | MLOps | Gate | Date |
|-------|----|-------|--------|-------|------|------|
| B1 | 1 | Foundation — repo, CI, Postgres, MLflow, DVC | COMPLETE | COMPLETE | GATE PASSED | Jun 2026 |
| B2 | 1–2 | Synthetic data — fraud (generator, GE suite, data dictionary) | COMPLETE | COMPLETE | GATE PASSED | Jun 2026 |
| B3 | 2–3 | Fraud features + anti-leakage suite | COMPLETE | COMPLETE | GATE PASSED | Jun 2026 |
| B4 | 3 | Baseline + MVM + calibration (fraud) | IN PROGRESS | IN PROGRESS | NOT STARTED | |
| B5 | 4 | BentoML serving + FastAPI + contracts | NOT STARTED | NOT STARTED | NOT STARTED | |
| B6 | 4–5 | LangGraph agent v0 + LLM (Llama 3.1 8B) | NOT STARTED | NOT STARTED | NOT STARTED | |
| B7 | 5–6 | Fraud RAG (ChromaDB, 50+ seed docs, RAGAS) | NOT STARTED | NOT STARTED | NOT STARTED | |
| B8 | 6–7 | Guardrails (Presidio, OPA, grounding, injection detector selection) | NOT STARTED | NOT STARTED | NOT STARTED | |
| B9 | 7–8 | Chat UI + audit-trail replay (→ WS1.4 artefact) | NOT STARTED | NOT STARTED | NOT STARTED | |
| B10 | 8–10 | Replicate — Compliance + RM verticals | NOT STARTED | NOT STARTED | NOT STARTED | |
| B11 | 10–11 | Observability — Grafana 8 panels, Evidently, kill-switch drill | NOT STARTED | NOT STARTED | NOT STARTED | |
| B12 | 11–12 | Hardening + demo pack (3 scripts, 70B demo config, deploy guide v0) | NOT STARTED | NOT STARTED | NOT STARTED | |

## Open items / longest-lead dependencies

- [ ] G10 external domain reviewers — one per vertical (recruit now; longest lead time); brief extended to document narrative review (ADR-003/D8)
- [ ] ADR-000 image round — Banking Architecture figs 1.1/3.1/4.1/5.1, Learning Bank figs 1–3; deck diagram regeneration for residual source defects per ADR-001 (NOW GATES CLIENT USE per ADR-003/D5; + Figure 4.2 mortgage flow)
- [x] ADR-001 — deck rasters enhanced + content-patched → Executive Presentation v2a (Jun 2026)
- [ ] WS3.1 deck design pass — start after B9 screenshots; include use-case roadmap one-pager (ADR-003/D6)
- [ ] GPU rental plan for B12 70B demo configuration

## ADR index

See DECISIONS.md. Next ADR number: ADR-001.
