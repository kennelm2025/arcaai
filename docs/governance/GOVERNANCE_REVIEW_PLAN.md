# ArcaAI — Governance & Foundations Review Plan

**Status:** Proposed (v0.1) — for ratification before kickoff
**Date:** 14 June 2026
**Chair / decider:** Mike Kennelly
**Coordinator:** Claude
**External reviewers:** ChatGPT, Grok *(DeepSeek excluded — prior citation fabrication)*
**Trigger:** ADR governance audit (June 2026) surfaced systemic gaps
**Build status during review:** net-new build paused at the B5/inc1 boundary

---

## 1. Why now

A routine ADR review surfaced that the decision-governance system had drifted in ways that were invisible in isolation: a numbering **collision across two ledgers** (`decisions/` vs `DECISIONS.md`, both using `ADR-NNN`), a **dangling `ADR-000`** reference, **reserved-but-unwritten** strategic ADRs (0004 Target Market, 0005 Data Strategy), an index that lagged the files, and several **architecturally-significant engineering decisions never captured as ADRs** (XGBoost, BentoML, Platt, DVC-as-artefact-store). Each piece looked fine on its own; the gaps only appeared on a cross-cutting sweep — which is precisely the failure mode that survives undetected.

We are about to enter **B10**, where the fraud vertical becomes the template every other vertical inherits. Any loose foundation now is replicated N times. This review confirms architecture, design/specs, the quality plan, and the decision system are coherent, current, and externally defensible **before** that replication and before B5/inc2.

**Reframe:** ArcaAI's core value proposition (ADR-0001, `decisions/README.md`) is a defensible, auditable governance trail a bank's Model Risk function can read. This review is the first real exercise of that claim, run against our own repo. It is dogfooding, not overhead.

## 2. Operating principles (keep it proportionate)

- **Triage, don't gold-plate.** Every finding gets a severity. Only **Must-Fix** items block resumption; the rest go to a backlog fixed in normal flow.
- **Time-boxed.** Estimate ~5–7 focused review passes. Success = "confident and defensible enough to proceed," not perfection. **Named failure mode to avoid: the review becomes an open-ended stall the build never resumes from.**
- **Evidence over memory.** Findings are grounded in the repo — greps, file inventories, traceability matrices — not recollection. Memory is exactly what missed the collision.
- **Decisions are Mike's.** The panel surfaces, challenges, and recommends; Mike ratifies. Anything rising to an architecturally-significant decision is written as an ADR via the existing `decisions/` process.

## 3. Scope — Mike's four pillars + two additions

| Pillar (as stated) | Workstream | Primary artefacts |
|---|---|---|
| Decisions | **A — Decision-system integrity** | `decisions/`, `DECISIONS.md`, `_template.md`, README index, citations across repo |
| Architecture | **B — Architecture & design coherence** | Solution/Technical Architecture specs, ADR-0001/0002/0003/0006, fraud vertical code, serving design |
| Design | **C — Specifications currency** | `docs/specs/01,02,04,05,07`, working-briefs, glossary, deferred strategic ADRs |
| Quality Plan | **D — Build & Quality Plan** | Build & Quality Plan (docx), gate docs (`docs/build/`), `BUILD_TRACKER.md`, CI/test/leakage suites |
| *(added)* | **E — Engineering process & protocols** | `SESSION_PROTOCOLS.md`, `CONTRIBUTING`, `CHANGELOG.md`, `CURRENT_STATE.md`, branching/PR, DVC/MLflow ops, SME-panel method |
| *(added, cross-cutting)* | **F — Regulatory / bank-reviewer lens** | Security & Compliance spec, liability split (0001), Model Risk integration (0002 Stage 2/3) |

**Out of scope:** net-new feature build (paused above inc1); commercial/GTM workstream except where it gates a deferred ADR.

## 4. Workstreams

### A — Decision-system integrity *(acute; do first)*
**Answers:** Is the decision record complete, unambiguous, and free of namespace collisions? Are all significant decisions captured at the right tier?
**Tasks:** reconcile `decisions/` vs `DECISIONS.md` namespaces; resolve `ADR-000`; fix citation format (4-digit standard); confirm reserved 0004/0005 handling; triage undocumented significant decisions → backfill ADRs; settle the "Blueprint" terminology (no such file exists — references are wrong); confirm immutability/Proposed→Accepted discipline is actually followed.

### B — Architecture & design coherence
**Answers:** Does the system *as built* match ADR-0001/0002/0003 and the architecture specs? Is the fraud vertical a sound B10 template?
**Tasks:** trace pipeline-as-platform and the three-stage lifecycle from ADR → spec → code; validate the serving design (0006) and its inc2 plan; review the feature/anti-leakage architecture; identify architecture-vs-ADR drift; assess vertical-replication readiness.

### C — Specifications currency
**Answers:** Are the specs current with build reality, internally consistent, and complete?
**Tasks:** spec inventory (note the visible set is 01/02/04/05/07 — confirm whether 03/06 exist or are gaps); check spec↔ADR traceability; resolve the Spec 01 §6 dependency on the deferred Target-Market ADR; confirm the 01/02 boundary; flag stale sections.

### D — Build & Quality Plan
**Answers:** Is the quality plan still right, and are its gates actually being honoured?
**Tasks:** validate the B0–B10 gate model and G/L quality gates against current build; verify gate evidence (e.g. `B3_GATE.md`) and `BUILD_TRACKER.md` accuracy (B5 row); test the "docs are the spec" discipline; confirm CI/leakage-suite coverage; check ADR-0006's commitments (provenance manifest, promotion gate) are built or logged, not just described.

### E — Engineering process & protocols
**Answers:** Do the working protocols hold under pressure, and did incidents get properly recorded?
**Tasks:** review `SESSION_PROTOCOLS`/`CONTRIBUTING`; close out the **force-push-to-main incident** (CONTRIBUTING forbids it; the eol recovery did it) — decision record + guard; confirm house rules; assess DVC/MLflow operational hygiene; review the SME-panel method itself and refresh `docs/governance/sme-prompt-primers`.

### F — Regulatory / bank-reviewer lens *(applied throughout, synthesised at end)*
**Answers:** Would this survive a bank Model Risk review?
**Tasks:** apply the external-reviewer lens to A–E outputs; check the liability split (0001) and Stage-2/3 Model Risk integration story hold; sanity-check the Security & Compliance spec against the deferred Target-Market regulatory frame (UK-only vs UK+EU/DORA/EU AI Act).

## 5. Panel & operating method

| Role | Who | Responsibility |
|---|---|---|
| Chair / decider | Mike | Domain authority; ratifies findings; owns go/no-go |
| Coordinator + reviewer | Claude | Repo-aware analysis (sweeps, traceability, drafting); prepares per-workstream briefs; consolidates; maintains the findings register |
| Independent reviewers | ChatGPT, Grok | Receive the prepared brief; return *forced positions*, not approval; red-team |

**Per-workstream cycle** (the pattern proven in the ADR rounds):
1. Claude prepares a review brief: context the external models lack + specific questions + Claude's own pre-assessment stated as *positions to challenge*.
2. ChatGPT and Grok review independently and return positions.
3. Claude consolidates — convergence / unique catches / resolve the splits — plus own view.
4. Mike decides. Decisions logged to the findings register; any that rise to ADR level are written per the `decisions/` process.

## 6. Sequence & cadence

A first (acute, and mostly already surfaced — a short pass to ratify and clear). Then B and C (can overlap). Then D, then E. F runs as a lens across all and is synthesised into the final go/no-go. Estimate one focused pass per workstream; A and E are light, B/C/D heavier.

## 7. Outputs

- **Findings register** — `GOVERNANCE_REVIEW_FINDINGS.md` (id, area, severity, finding, recommendation, owner, status). Seeded below.
- **Remediation backlog** — prioritised; Must-Fix vs Deferred.
- **New / backfilled ADRs** — for the undocumented significant decisions.
- **Reconciled governance docs** — README, `DECISIONS.md` namespace, conventions, refreshed primers.
- **Go/No-Go to resume build** — explicit decision against the exit criteria.

## 8. Exit criteria (the resume-build gate)

Build resumes at B5/inc2 when:
1. **Decisions** reconciled — no dangling refs, namespaces separated, conventions documented, undocumented-decision backlog triaged (each: backfill / log / no-ADR-needed).
2. **Architecture** confirmed ADR-aligned, or every drift logged with a remediation owner.
3. **Specs** triaged for currency; Spec-01 §6 dependency resolved or explicitly provisional.
4. **Quality Plan** validated; `BUILD_TRACKER` accurate; ADR-0006 commitments built or logged.
5. **Process** incidents closed (force-push recorded + guarded).
6. **Bank-reviewer lens** sign-off from the panel + Mike that the trail is defensible.
7. All open Must-Fix findings closed; everything else explicitly deferred to backlog (Must-Fix is the *only* class that blocks).

## 9. Seed findings register

| ID | Area | Sev | Finding | Recommendation |
|---|---|---|---|---|
| F-001 | A | High | `ADR-NNN` namespace collides across `decisions/` and `DECISIONS.md` (two decisions, same string) | Rename `DECISIONS.md` entries out of `ADR-` form; update citations in `generator.py`, `B3_GATE.md`, `CURRENT_STATE.md` |
| F-002 | A | Med | `ADR-000` cited with no file | Locate (`git grep -n "ADR-000"`); backfill or correct references |
| F-003 | A | Low | Citation format inconsistent (`ADR-001` vs `ADR-0001`) | Standardise on 4-digit repo-wide |
| F-004 | A | Low | README index lagged files (missed 0006; reserved 0004/0005 untracked) | Resolved in updated README; confirm process so index can't drift again |
| F-005 | A/B | Med | Significant engineering decisions never captured as ADRs (XGBoost, BentoML, Platt, DVC-as-store) | Triage each vs the README significance test; backfill those that qualify |
| F-006 | C | Med | Strategic ADRs 0004 (Target Market) / 0005 (Data Strategy) deferred since May, gating Spec 01 §6 | Decide whether to resolve now or keep Spec 01 §6 provisional; they're at/near their Month-2 trigger |
| F-007 | E | Med | Force-push to `main` (eol recovery) violated CONTRIBUTING | Record the incident decision; add a guard (branch protection / documented exception process) |
| F-008 | A | Low | "Blueprint" referenced (incl. in review briefs) but no such file exists | Correct terminology; ADRs are standalone in `decisions/` |
| F-009 | B/D | Med | ADR-0006 (Proposed) commits to a B4 provenance manifest + promotion-gate CI not yet built | Build before B5 gate close, or downgrade those clauses to logged follow-ups |

## 10. Immediate next actions

1. **Mike:** ratify or amend this plan (scope, principles, panel roster, time-box).
2. **Claude:** on ratification, prepare the **Workstream A** review brief first — it's acute, and most of its findings are already on the table, so it's a fast, momentum-building pass.
3. **Panel:** run A through the four-step cycle; ratify the reconciled decision system; then proceed to B/C.
4. Resume build only on meeting the §8 exit criteria.
