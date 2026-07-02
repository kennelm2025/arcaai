# Governance Review — Workstream A: consolidated outcome

**Date:** 14 June 2026 · **Panel:** Mike (chair), Claude (coordinator), Grok, ChatGPT
**Re-run needed?** No. Both reviews answered the understated (pre-update) pack, but the
three findings they lacked (parallel series, ADR-000 resolution, F-010 uncommitted ADRs)
**reinforce** their positions rather than overturning them. Proceed to consolidation.

## Consolidated rulings

**Q-A1 — Two ledgers, hard separation.** Unanimous: keep two instruments, rename the
lightweight tier out of the `ADR-` namespace. ChatGPT sharpened the *why* — it's a
governance **classification** defect (one identifier implying two authority levels),
not merely a naming clash. Notation: **`DEC-NNNN`** for the log (not Grok's
headings-only), because the log entries are *cited from code* (`generator.py` cites
"ADR-004") and citations need a stable target. `ADR-NNNN` (four-digit, `decisions/`)
means exactly one thing henceforth.
→ This covers the whole DECISIONS.md series — **five** entries,
ADR-000/001/002/003/004 → DEC-0000..DEC-0004. (The original scope said four;
ADR-002 (PwC scrub) was missed and caught during CL-01 execution, 14 Jun PM.)

**Q-A2 — Triage.** Unanimous: **DVC-as-store → backfill ADR (0007)**; **XGBoost →
Model Card**; **Platt → Model Card**. **BentoML → depends on intent** (both flagged
this): vertical-local → fold into ADR-0006; platform serving standard → standalone ADR.
*Mike's ruling needed* — Claude's lean: platform-standard, because B10 replicates the
fraud serving component across every vertical, so the framework choice is de facto
cross-vertical.

**Q-A3 — Stop reserving; stub the existing two now.** ChatGPT improved Claude's
position: don't leave 0004/0005 unwritten (a cited number must resolve to a file).
Create **stub ADRs immediately** — `Status: Reserved`, owner, reason, target — and fill
when the strategic work is done. Never reserve again; number at creation; planning docs
refer to unwritten ADRs by title.

**Q-A4 — Disclosed backfill (union of both reviews).** `_template.md` gains:
`Decision Date`, `Recorded Date`, `Decision Type: Contemporary | Backfilled`,
`Evidence:` (commit SHA / DEC entry / code comment), and a mandatory disclosure
sentence: *"This ADR records a decision already in operation and does not imply it was
made on the Recorded Date."* Backfilled ADRs carry `Status: Accepted (backfilled)`.
Plus (F-010): an ADR is not immutable until committed — enforce a commit check.

**Q-A5 — One gate-capture question.** Unanimous. Add to every gate review:
*"What architecturally significant decisions were made since the last gate?"* with
outcomes `None | Existing ADR covers it | DEC log only | New ADR required`. No
ADR-first mandate. Capture at the gate, since the gate already exists.

**Q-A6 — Worst finding (the one split, resolved).** Grok: namespace collision. ChatGPT:
process-vs-practice. They are two levels of one problem. **Process-vs-practice is the
root cause** (it implies unknown unknowns — "where else wasn't this followed?"), now
compounded by F-010. **The namespace collision is the most visible symptom** — what a
reviewer's first traceability check fails on. Ranking: (1) process-vs-practice, (2)
namespace collision [Critical], (3) undocumented decisions, (4) reserved-unwritten, (5)
ADR-000, (6) citation drift. Fix order: Q-A1 stops the bleeding; Q-A5 + commit
discipline cures the cause.

## Findings register — updates

| ID | Sev | Status | Note |
|---|---|---|---|
| F-001 | **Critical** | Open | Parallel `ADR-` series collide at 001/003/004 (three decisions double-booked), not one |
| F-002 | — | **Closed** | ADR-000 is a real, open Series-2 decision (image round, gates client use) |
| F-003 | Low | Reframed | Three- vs four-digit is the series boundary, not format drift; resolved by Q-A1 |
| F-005 | Med | Open | Re-triaged (Q-A2): DVC=ADR, XGBoost/Platt=Model Card, BentoML=Mike's ruling |
| F-006 | Med | Open | 0004/0005 → immediate stub ADRs (Q-A3) |
| F-010 | Med | Open | **New** — ADRs not under version control; immutability unenforced until committed |

## Remediation

**Must-Fix (block resume to B5/inc2):**
1. Rename DECISIONS.md series `ADR-` → `DEC-`; update citations (`generator.py`,
   `B3_GATE.md`, `CURRENT_STATE.md`, `BUILD_TRACKER.md`). [F-001]
2. Commit ADR-0006 + README; confirm `decisions/` + `DECISIONS.md` tracked. [F-010]
3. Update `_template.md` with the Q-A4 backfill fields + disclosure. [Q-A4]
4. Stub ADR-0004 / ADR-0005 (`Status: Reserved`). [F-006]
5. Backfill ADR-0007 (DVC-as-artefact-store) using the backfill fields. [F-005]

**Backlog (don't block):**
6. Standardise citations to four-digit. [F-003]
7. Triage DECISIONS.md entries for promotion — the mortgage-orchestration decision
   (S2 "ADR-003") reads architecturally significant → candidate formal ADR. [Q-A1]
8. Add the gate-capture question to the gate checklist + BUILD_TRACKER. [Q-A5]
9. Fold XGBoost / Platt rationale into the fraud Model Card. [Q-A2]

## Decisions — ruled by Mike, 14 Jun 2026 (PM)
- **D-01 BentoML: platform serving standard** → recorded as ADR-0008 (backfilled).
  Settled by Banking Architecture v1.0b (L4 technology components; infra-split
  table "All ML models (BentoML)"). Boundary captured in 0008: BentoML serves
  models (L4); FastAPI is the system-integration API (L1); the agent (L2) is the
  single caller.
- **D-02 `DEC-NNNN` ratified** as the log notation; rename-not-renumber.
- **D-03 Must-Fix #1–#5 (+ ADR-0008 + README) ratified** as the resume-build gate.

## WS-A exit status
**CLOSED — 14 Jun 2026 (PM).** Must-Fix #1–#5 executed; rulings ratified; merged to
`main` via PR #6 at commit `1b86764` (ci-devops #21, ci-mlops #25 green). Files
landed: ADR-0004/0005 stubs (Reserved), ADR-0007 + ADR-0008 (backfilled, Accepted),
reconciled `decisions/README.md` + `_template.md`, DECISIONS.md renamed, four citers
updated. → Next: WS-B (architecture coherence), then WS-C (specs).

*Patched 2 Jul 2026: rename scope corrected to five entries and close-out recorded —
the repo copy had not been updated when WS-A closed (see changelog trail-integrity
note).*
