# CURRENT STATE

_Last updated: 11 June 2026_

## Where we are

- **Phase 0 (lockdown): CLOSED.** Suite locked June 2026 — Banking Architecture v1.0b,
  System Architecture v1.1, Technical Infrastructure v1.1, Engineering Blueprint v1.1
  (ML Pipeline Sister Document), Learning Bank v2.1, Delivery Plan v1.1, Executive
  Presentation v2a. Rulings R1–R13 + ADR-000–003 in DECISIONS.md. Repo is the single
  source of truth (baseline commit 986afd3; Phase 0.5 GATE PASSED).
- **B1 (foundation): IN PROGRESS.** Skeleton per Blueprint §4, CI (ci-devops/ci-mlops),
  Postgres+MLflow dev stack, DVC init, smoke tests. Gate: CI green on PR, MLflow UI
  reachable, services healthy.
- **Next: B2** — fraud synthetic data generator + Great Expectations suite + data dictionary.

## Open items

- **ADR-000 image round — GATES CLIENT USE.** BA figs 1.1/3.1/4.1/5.1 + new 4.2 (mortgage
  flow), Learning Bank figs 1–3, deck diagram regeneration (ADR-001 residuals).
  Inputs staged in `diagrams/image-round-inputs/` incl. the Grok regeneration brief.
- **G10 external domain reviewers** — one per vertical; longest lead; brief includes
  document narrative (ADR-003/D8). Recruit now.
- **ML_Pipeline_v0.2 harvest check** — archived April doc vs Blueprint §19 (R13 follow-up).
- Manual: logo artwork spelling; identify REVIEW_unknown-1/-2 in diagrams; inspect
  D:\ArcaAI_legacy.
- WS3.1 deck design pass after B9 (incl. use-case roadmap one-pager).
- GPU rental plan for the B12 70B demo configuration.
