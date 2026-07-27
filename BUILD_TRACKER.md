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

> **Gate-based plan refresh (25 Jul 2026, DEC-0010 / WS-D RAT-01).**
> The replacement shape for the retired week column is now ratified.
> `Depends on` makes the build dependency explicit; `Gate doc` points
> at the per-stage gate document. **Gate criteria do not live in this
> file.** Each `docs/build/BN_GATE.md` is created at stage *entry* with
> its exit-evidence section blank, and is the single source for that
> stage's entry criteria, exit evidence, gate questions and deferrals.
> This tracker links to them and never restates them. Full text:
> `docs/governance/WS-D_RAT-01_GATE_PLAN.md`. Binding from B7.

## Phase 0 — Lockdown

| # | Item | Status | Date |
| --- | --- | --- | --- |
| 0.1 | Rulings R1–R13 decided and recorded | GATE PASSED | Jun 2026 |
| 0.2 | High-severity items applied (LB1, BA1, BA2, SA1, SA2, TI1, EB1, EB2, DP1) | GATE PASSED | Jun 2026 |
| 0.3 | Medium items applied; image round | COMPLETE (image round deferred — DEC-0000) | Jun 2026 |
| 0.4 | Suite version-bumped and frozen | GATE PASSED | Jun 2026 |
| 0.5 | GitHub monorepo created; CI skeleton; this tracker + DECISIONS.md committed | GATE PASSED | Jun 2026 |

## Build stages (Build & Quality Plan v1.0; week column retired — see variance note)

| Stage | Depends on | Scope | DevOps | MLOps | Gate | Gate doc | Date |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B1 | Phase 0 | Foundation — repo, CI, Postgres, MLflow, DVC | COMPLETE | COMPLETE | GATE PASSED | `docs/build/B1_GATE.md` | Jun 2026 |
| B2 | B1 | Synthetic data — fraud (generator, GE suite, data dictionary) | COMPLETE | COMPLETE | GATE PASSED | `docs/build/B2_GATE.md` | Jun 2026 |
| B3 | B2 | Fraud features + anti-leakage suite | COMPLETE | COMPLETE | GATE PASSED | `docs/build/B3_GATE.md` | Jun 2026 |
| B4 | B3 | Baseline + MVM + calibration (fraud) | COMPLETE | COMPLETE | GATE PASSED | `docs/build/B4_GATE.md` | Jun 2026 |
| B5 | B4 | BentoML serving + FastAPI + contracts | COMPLETE — inc1 (PR #5, `5f4e570`), inc2 (PR #11, `5f3d3d5`) | COMPLETE | GATE PASSED | `docs/build/B5_GATE.md` | Jul 2026 |
| B6 | B5 | LangGraph agent v0 + LLM (Llama 3.1 8B) | COMPLETE — 5 incs (PRs #18–#20, #22) | COMPLETE | GATE PASSED | `docs/build/B6_GATE.md` | Jul 2026 |
| B7 | B6 | Fraud RAG (ChromaDB, 50+ seed docs, RAGAS) | IN PROGRESS | IN PROGRESS | IN PROGRESS | `docs/build/B7_GATE.md` | |
| B8 | B7 | Guardrails (Presidio, OPA, grounding, injection detector selection) | NOT STARTED | NOT STARTED | NOT STARTED | *to be created at entry* | |
| B9 | B8 | Chat UI + audit-trail replay (→ WS1.4 artefact) | NOT STARTED | NOT STARTED | NOT STARTED | *to be created at entry* | |
| B9.5 | B9 | Platform Extraction (ADR-0009 / DEC-0005): extract ML lifecycle machinery to platform layer; vertical-neutral contracts; exit = 2nd vertical consumes, not copies. **Tested by B10** | NOT STARTED | NOT STARTED | NOT STARTED | *to be created at entry* | |
| B10 | B9.5 | Instantiate — Compliance + RM verticals against the platform template (restated per ADR-0009; gated by B9.5 exit) | NOT STARTED | NOT STARTED | NOT STARTED | *to be created at entry* | |
| B11 | B10 | Observability — Grafana 8 panels, Evidently, kill-switch drill | NOT STARTED | NOT STARTED | NOT STARTED | *to be created at entry* | |
| B12 | B11 | Hardening + demo pack (3 scripts, 70B demo config, deploy guide v0) | NOT STARTED | NOT STARTED | NOT STARTED | *to be created at entry* | |

**Reading the dependency column.** The chain B1→B9 is genuinely serial;
recording it as such is the honest answer, not a failure to find
parallelism. Two relationships are not simple succession and are the
reason the column exists: **B10 is the test of B9.5**, not merely its
successor — if replication cost at B10 is high, B9.5 reopens; and
**B11 has instrumentation work that can land from B7 onward**, though
its eight panels need three verticals and therefore B10.

## Gate review — checklist ownership

**The standing gate checklist lives in `WS-D_RAT-01_GATE_PLAN.md` §4**
and is not restated here (per the tracker-links-never-restates rule,
RAT-01 §2). It carries the Checkpoint 01 questions — decision capture
(CL-08 / Q-A5) and architecture conformance (CF-1) — alongside the CI,
provenance, WS-E and evidence-citation items added at RAT-01.

**This file remains canonical for the Gate Acceptance Record
specification** below, which RAT-01 §4 points at rather than duplicates.

### Gate Acceptance Record (Checkpoint 01 RAT-04) — binding from B7

Every `B*_GATE.md` from B7 onward carries a Gate Acceptance Record
section containing:

- evidence list, cited as **path @ commit SHA** (RAT-01 §3.1);
- CI results **transcribed as text** — workflow name, run number,
  conclusion, date, and the commit SHA the run was against — because
  GitHub Actions logs expire and a link will not survive to the first
  external review (RAT-01 §3.1);
- producer statement;
- approver statement (same person permitted, both statements
  mandatory);
- residual risks accepted into the next stage;
- decision: Pass / Conditional Pass / Fail;
- approval date.

## Open items / longest-lead dependencies

- [ ] G10 external domain reviewers — one per vertical (recruit now; longest lead time); brief extended to document narrative review (DEC-0003/D8)
- [ ] DEC-0000 image round — Banking Architecture figs 1.1/3.1/4.1/5.1, Learning Bank figs 1–3; deck diagram regeneration for residual source defects per DEC-0001 (NOW GATES CLIENT USE per DEC-0003/D5; + Figure 4.2 mortgage flow)
- [x] DEC-0001 — deck rasters enhanced + content-patched → Executive Presentation v2a (Jun 2026)
- [ ] WS3.1 deck design pass — start after B9 screenshots; include use-case roadmap one-pager (DEC-0003/D6)
- [ ] GPU rental plan for B12 70B demo configuration
- [x] **B2 gate-document integrity** *(raised and closed 25 Jul 2026)* —
  `docs/build/B2_GATE.md` carried every criterion unticked while this
  tracker recorded B2 as GATE PASSED. Gate confirmed passed; the
  document was never updated. Ticks applied 25 Jul with a dated
  addendum recording them as retrospective. Trail-integrity class, same
  as the 2 Jul note and CL-10; root cause is the Q-A6 finding.
  Addendum, not DEC, per RAT-01 §3.1 — the gate decision would not have
  differed.

## DEC index

See DECISIONS.md (next DEC number = tail of the DEC series there; do not duplicate it here).
