# CURRENT STATE

*Last updated: 12 June 2026*

## Where we are

\- \*\*Phase 0 (lockdown): CLOSED.\*\* Suite locked June 2026 — Banking Architecture v1.0b,

&#x20; System Architecture v1.1, Technical Infrastructure v1.1, Engineering Blueprint v1.1

&#x20; (ML Pipeline Sister Document), Learning Bank v2.1, Delivery Plan v1.1, Executive

&#x20; Presentation v2a. Rulings R1–R13 + ADR-000–004 in DECISIONS.md. Repo is the single

&#x20; source of truth (Phase 0.5 GATE PASSED).

\- \*\*B1 (foundation): GATE PASSED (June 2026).\*\* Skeleton per Blueprint §4, CI green

&#x20; (ci-devops/ci-mlops), Docker Desktop installed (WSL 2, disk image on D:\\Docker),

&#x20; Postgres 16 :5432 + MLflow 2.14.1 :5000 healthy, experiment `arcaai-fraud` created,

&#x20; DVC init committed.

\- \*\*B2 (fraud synthetic data): GATE PASSED (June 2026).\*\* 956,684 txns, 2,000 customers,

&#x20; 600 merchants, 17 months, fraud 0.535% across four patterns. Content hash

&#x20; `6db7d6b191a9c929` (ns-pinned per ADR-004, pandas-version-stable). GE suite + integrity

&#x20; PASS; DVC pipeline pinned; leakage-honest `label\_available\_date` on every row.

\- \*\*B3 (fraud features + anti-leakage): GATE PASSED (June 2026).\*\* 12-feature MVM budget

&#x20; (contract in verticals/fraud/features/FEATURES.md); 956,684 rows featurised, zero

&#x20; pre-train filter flags; chronological 70/15/15 split. Anti-leakage suite in ci-mlops:

&#x20; shuffle test (shuffled-before-featurisation, AUC < 0.55), planted-leak power control,

&#x20; source audit, future-blindness test, split/label-mask assertions. feature\_engineer DVC

&#x20; stage pinned.

\- \*\*Next: B4\*\* — rules-engine baseline (G2) + 12-feature XGBoost MVM + Platt calibration

&#x20; (MAE < 0.05) + 6-period walk-forward (G5/G7). First AUC numbers. Logs to MLflow

&#x20; `arcaai-fraud`.

## Open items

* Domain registration (arcaai.com/.co.uk) + email + AWS account hygiene — short session this week.
* **ADR-000 image round — GATES CLIENT USE.** BA figs 1.1/3.1/4.1/5.1 + new 4.2 (mortgage
flow), Learning Bank figs 1–3, deck diagram regeneration (ADR-001 residuals).
Inputs staged in `diagrams/image-round-inputs/` incl. the Grok regeneration brief.
* **G10 external domain reviewers** — one per vertical; longest lead; brief includes
document narrative (ADR-003/D8). Recruit now.
* **ML\_Pipeline\_v0.2 harvest check** — archived April doc vs Blueprint §19 (R13 follow-up).
* Manual: logo artwork spelling; identify REVIEW\_unknown-1/-2 in diagrams; inspect
D:\\ArcaAI\_legacy.
* WS3.1 deck design pass after B9 (incl. use-case roadmap one-pager).
* GPU rental plan for the B12 70B demo configuration.

