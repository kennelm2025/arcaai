# Governance Review — Change Log

Running log of changes the review requires. Tick as done. Spans all workstreams;
seeded with Workstream A. **Must-Fix items block resumption of build (B5/inc2);
Backlog items do not.** House rules apply when executing: plain Notepad only,
PowerShell `.Replace()` for tracker edits (but NOT for ID renames near 4-digit
refs — prefix collision; use `-replace` with `\b`), `git add -A` →
`git status -s` eyeball before every commit.

## Workstream A — Decision-system integrity — **CLOSED 14 Jun 2026 (PM)**

Remediation merged to `main` via PR #6, commit `1b86764` (ci-devops #21,
ci-mlops #25 green).

### Must-Fix (blocked resume — all done)
- [x] **CL-01** Rename the `DECISIONS.md` `ADR-NNN` series → `DEC-NNNN`. Scope was
  **five** entries — DEC-0000..DEC-0004 (the original scope said four; ADR-002
  PwC-scrub was missed and caught mid-execution). Citations updated:
  `verticals/fraud/synthetic/generator.py`, `docs/build/B3_GATE.md`,
  `CURRENT_STATE.md`, `BUILD_TRACKER.md`. DECISIONS.md "## ADRs" header and
  BUILD_TRACKER "ADR index / Next ADR number" relabelled to DEC. After this,
  `ADR-NNNN` (four-digit, `decisions/`) means exactly one thing. *(F-001, Critical)*
- [x] **CL-02** `decisions/0006-serving-model-source.md` + `decisions/README.md`
  committed (pre-break); the full `decisions/` tree and `DECISIONS.md` tracked;
  remaining WS-A files landed in the close-out commit. *(F-010)*
- [x] **CL-03** `decisions/_template.md` updated: front-matter `Decision Date`,
  `Recorded Date`, `Decision Type: Contemporary | Backfilled`, `Evidence:`;
  mandatory backfill disclosure sentence; Status enum gained
  "Accepted (backfilled)". *(Q-A4)*
- [x] **CL-04** Stubs created: `decisions/0004-target-market-segment.md`,
  `decisions/0005-data-strategy.md` — `Status: Reserved`. *(F-006)*
- [x] **CL-05** `decisions/0007-artefact-store-dvc.md` backfilled (DVC as artefact
  source-of-truth) using the CL-03 backfill fields. *(F-005)*

### Decisions ratified by Mike (14 Jun 2026)
- [x] **D-01** BentoML ruled **platform serving standard** — recorded as
  **ADR-0008 (backfilled)**. Boundary captured: BentoML serves models (L4);
  FastAPI is the system-integration API (L1); the agent (L2) is the single caller.
- [x] **D-02** `DEC-NNNN` log notation ratified; rename-not-renumber.
- [x] **D-03** CL-01–CL-05 (+ ADR-0008 + README) ratified as the resume-build gate.

### Backlog (non-blocking — carried forward)
- [ ] **CL-06** Standardise all ADR citations to four-digit repo-wide. *(F-003)*
- [ ] **CL-07** Triage `DECISIONS.md` entries for promotion to formal ADRs; the
  mortgage process-orchestration decision (DEC-0003) looks architecturally
  significant — candidate. *(Q-A1 triage)*
- [ ] **CL-08** Add the decision-capture question to the gate checklist +
  BUILD_TRACKER: "What architecturally significant decisions since the last gate?
  → None | Existing ADR | DEC log only | New ADR required." *(Q-A5)*
- [ ] **CL-09** Fold XGBoost + Platt rationale into the fraud Model Card. *(Q-A2)*
- [ ] **CL-10** *(new, 2 Jul)* BUILD_TRACKER B5 row is wrong, not merely
  conservative — inc1 is **merged to main** (PR #5, commit `5f4e570`, per
  ADR-0008 Evidence) but the row reads NOT STARTED across all columns. Restate
  as "inc1 COMPLETE (PR #5, `5f4e570`); inc2 + gate blocked on governance
  resume." *(trail integrity)*
- [ ] **CL-11** *(new, 2 Jul)* `Decider` (template) vs `Deciders` (0007/0008)
  field-name mismatch — cosmetic, align. `CURRENT_STATE.md` "Last updated" stamp
  — bump at next commit.

### Ruling — D-04 (2 Jul 2026): ADR-0006 status
ADR-0006 flipped **Proposed → Accepted**, executing the merge-time rule (stated
in both the README and 0006's own numbering note) that was never actioned at the
14 Jun merge. The two commitments 0006 makes that are not yet built (F-009) are
downgraded to tracked follow-ups per the F-009 disposition options:
- [ ] **CL-12** Build the B4 sidecar provenance manifest
  (`data/fraud/models/provenance.json`; ADR-0006 decision 3). **Gates B5 gate
  close** (not resume).
- [ ] **CL-13** Build the promotion-gate CI check — instantiate scorer from
  proposed pinned artefacts; parity + schema contract + calibration invariants +
  latency budget; fail merge on violation (ADR-0006 decision 5). **Gates B5 gate
  close** (not resume).

### Trail-integrity note (2 Jul 2026)
The repo copies of this changelog, the WS-A outcome, and the session handover were
found stale on 2 Jul — recording WS-A as open/unticked with the four-entry rename
scope, while the repo itself carried the executed five-entry rename and the
close-out commit. This file and `GOVERNANCE_REVIEW_WS-A_outcome.md` are patched to
match what was executed; the stale handover is superseded by
`SESSION_HANDOVER_2026-07-02.md`. Logged here as a live instance of the Q-A6
process-vs-practice finding: the fix (update trail docs in the same commit as the
work they record) applies to the review itself.

## Workstream B — Architecture & design coherence — **IN PROGRESS**
Pack at v0.2 (`WS-B_review_pack.md`) with the WS-A head-start evidence folded in
(contracts/ dir; ADR-0007/0008 pre-answering two P-B3 slices). Blocked on one
input: the source tree pull (§5 of the pack). Then send to Grok + ChatGPT.

## Workstream C — Specifications currency
*(not started)* First exhibit identified (2 Jul): `spec-01-working-brief-v0_2.md`
is dated 13 May, pre-lockdown — harvest map targets Banking Architecture **v0.4**
and exec deck v12, both superseded by the locked v1.0b suite. Its open questions
7b (9-vs-11 use cases) and the §3 tagline candidate are already settled by rulings
R1 and R3 respectively; ADR-0004 stub now exists for its §7a dependency. Re-base
before any drafting.

## Workstream D — Build & Quality Plan
*(not started)* Carries CL-10 evidence (tracker accuracy is a §4 D task).

## Workstream E — Engineering process & protocols
- [ ] **CL-E1** (carried in) Record the force-push-to-main incident + add a guard
  (branch protection / documented exception). *(F-007)*
- Q-A6 root-cause fix lands here: trail docs update in the same commit as the work
  they record (see trail-integrity note above).

## Workstream F — Regulatory / bank-reviewer lens
*(applied throughout; synthesised at end)*
