# Governance Review — Change Log

Running log of changes the review requires. Tick as done. Spans all workstreams;
seeded with Workstream A. **Must-Fix items blocked resumption of build (B5/inc2);
that gate was discharged at the WS-A close and B5/B6 have since gated. The
Must-Fix / Backlog distinction is retained below as the historical record of
that ruling.** House rules apply when executing: plain Notepad only, PowerShell
`.Replace()` for tracker edits (but NOT for ID renames near 4-digit refs —
prefix collision; use `-replace` with `\b`), `git add <explicit paths>` — never
`git add -A` (WS-E 38) — → `git status -s` eyeball before every commit.

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
- [x] **CL-08** *(closed 24 Jul 2026 — Checkpoint 01 chair action CF-2a; executed as the standing Gate review checklist section in BUILD_TRACKER.md, which also carries the CF-1 architecture-conformance question)* Add the decision-capture question to the gate checklist +
  BUILD_TRACKER: "What architecturally significant decisions since the last gate?
  → None | Existing ADR | DEC log only | New ADR required." *(Q-A5)*
- [ ] **CL-09** Fold XGBoost + Platt rationale into the fraud Model Card. *(Q-A2)*
- [x] **CL-10** *(new, 2 Jul; duplicate-state corrected 24 Jul 2026 — Checkpoint 01 CF-2b; closure was already recorded in the later ticked entry)* BUILD_TRACKER B5 row is wrong, not merely
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
- [x] **CL-12** Build the B4 sidecar provenance manifest
  (`data/fraud/models/provenance.json`; ADR-0006 decision 3). **Gates B5 gate
  close** (not resume).
- [x] **CL-13** Build the promotion-gate CI check — instantiate scorer from
  proposed pinned artefacts; parity + schema contract + calibration invariants +
  latency budget; fail merge on violation (ADR-0006 decision 5). **Gates B5 gate
  close** (not resume).

### Closure - CL-12/CL-13 (22 Jul 2026)
CL-12 and CL-13 closed jointly. Evidence: PR #14 (merge a8fe650) + PR #15 (merge 1179abe);
promotion-gate GREEN on ci-mlops #41 (branch) / #42 (main). Manifest is generated
platform-side in CI (scripts/generate_provenance_manifest.py, same serving code path)
and uploaded as a build artefact, not committed at the ADR-0006 literal path.
Gate = sha256 identity check + known-answer score check (scripts/gate_score_check.py).
Latency not gated per B5_GATE.md section 5.

### Trail-integrity note (2 Jul 2026)
The repo copies of this changelog, the WS-A outcome, and the session handover were
found stale on 2 Jul — recording WS-A as open/unticked with the four-entry rename
scope, while the repo itself carried the executed five-entry rename and the
close-out commit. This file and `GOVERNANCE_REVIEW_WS-A_outcome.md` are patched to
match what was executed; the stale handover is superseded by
`SESSION_HANDOVER_2026-07-02.md`. Logged here as a live instance of the Q-A6
process-vs-practice finding: the fix (update trail docs in the same commit as the
work they record) applies to the review itself.

### Header currency note (25 Jul 2026)
Two defects corrected in this file's own header this date, both instances of the
Q-A6 finding above. First, the house-rule line instructed `git add -A`, which is
the practice that caused WS-E 38 (three handover copies staged; 4 files / 522
insertions where 2 / 45 intended). The canonical CL ledger was instructing the
behaviour its own incident ledger had ruled against; corrected to explicit paths.
Second, the Must-Fix framing referred to a resume-build gate discharged at the
WS-A close, with B5 and B6 gated since; reworded as historical record rather
than live instruction.

## Workstream B — Architecture & design coherence — **CLOSED 2 Jul 2026**
Pack v0.3 sent; Grok + ChatGPT responses consolidated (unanimous) in
`GOVERNANCE_REVIEW_WS-B_outcome.md`; D-05–D-08 ratified same day. Findings
F-011–F-014 registered. Key rulings: machinery-vs-semantics capability boundary;
B9.5 Platform Extraction gate before B10; wording rule; Stage-2/3 design
workstream commissioned; extraction at B9.5 with platform-first discipline from
B5/inc2.

### WS-B remediation
- [x] **CL-14** ADR-0009 written (boundary + B9.5 gate). Accepted at merge.
- [x] **CL-15** B9.5 stage inserted: BUILD_TRACKER row added; deviation from the
  locked Build & Quality Plan recorded as DEC-0005 (tracker is truth per EB8).
- [ ] **CL-16** Generalise `contracts/` to vertical-neutral. Latest B9.5;
  earlier if touched at B5/inc2.
- [ ] **CL-17** Apply the DEC-0006 wording rule to external material at next
  revision of each document.
- [ ] **CL-18** Stage-2/3 minimum design brief (D-07). Named workstream,
  post-review.
- [x] **CL-10** (from 2 Jul list) BUILD_TRACKER B5 row restated with this
  commit.

## Workstream C — Specifications currency
**Run 21 Jul 2026. Outcome: GOVERNANCE_REVIEW_WS-C_outcome.md (F-C01..F-C06); retirements recorded in DEC-0007. This changelog is the canonical CL ledger per DEC-0007.** First exhibit identified (2 Jul): `spec-01-working-brief-v0_2.md`
is dated 13 May, pre-lockdown — harvest map targets Banking Architecture **v0.4**
and exec deck v12, both superseded by the locked v1.0b suite. Its open questions
7b (9-vs-11 use cases) and the §3 tagline candidate are already settled by rulings
R1 and R3 respectively; ADR-0004 stub now exists for its §7a dependency. Re-base
before any drafting. **Done: retired with tombstone and content disposition, this date.**
- [ ] **CL-19** *(new, 21 Jul)* Sharpen the two-kinds-of-pre-trained-models distinction in Banking Architecture (open-weight LLMs inherited as-is vs reference predictive models the bank upskills); canonical language already exists in the glossary ("Reference model"). Apply at next BA revision, alongside CL-17. *(Source: working brief 6a, dispositioned at retirement; F-C02)*
- [ ] **CL-20** *(new, 21 Jul)* Add the fourth competitive category (consulting/services firms: platform with consulting-enabled delivery, not a services engagement) to Banking Architecture positioning and the next deck design pass (WS3.1). *(Source: working brief 6d, dispositioned at retirement; F-C02)*


## Workstream D — Build & Quality Plan
**Opened 25 Jul 2026. RAT-01 gate-based plan refresh CLOSED — ratified as
DEC-0010, merged PR #26 (`fc125e8`); ci-mlops #54 and ci-devops #50 success,
25 Jul 2026. Outcome: `docs/governance/WS-D_RAT-01_GATE_PLAN.md`, binding from
B7.** The week column is replaced by an explicit dependency column; per-stage
gate criteria move out of BUILD_TRACKER.md into `docs/build/BN_GATE.md`, written
at stage **entry** with exit evidence blank rather than retrospectively at close.
Ten sub-decisions ratified, including evidence immutability (path @ SHA, CI
results transcribed), the not-allowed deferral list serving as the
required-evidence list, and an external-dependency flag on entry criteria.
Reviewed by Grok (R1, R2) and ChatGPT (R1); two independent concurrences on the
shape. Carries CL-10 evidence (tracker accuracy is a §4 D task).

WS-D items 2–4 open: CF-1 conformance spot-check design, RAT-02 governance trio
specification (audit logging, execution metadata, request wrapper), SS1/23
principle mapping for the B8/B9 artefact set.

- [ ] **CL-21** *(new, 25 Jul)* Data protection and record retention position for
  decision records, prompts and outcomes. The suite states none, while describing
  an append-only audit trail and `outcome_event` table that will hold personal
  data in any real deployment. Six gaps: immutability vs erasure across competing
  obligations (UK GDPR, AML/fraud retention, audit and model-risk evidence);
  subject retrieval as an indexing requirement — the only build consequence, and
  it lands in B9; prompt minimisation, proposed as an addition to the Architecture
  Principles set; purpose limitation; controller/processor default and the DPIA
  position; UK GDPR Art 22A–22D safeguards mapping, which the architecture should
  claim in its favour rather than leave implicit. Resolution is paragraph-level
  additions at the next BA revision plus one principles-set addition. Apply
  alongside CL-17/19/20; hard trigger post-B8 (RAT-11), pulled forward if a client
  pilot is scheduled sooner. **Not a B7 blocker** — the reference build is
  synthetic throughout. Full text: `docs/governance/CL-21_data-protection.md`.
  *(Source: WS-D session, arising from B7 corpus licensing / DEC-0011; reviewed
  ChatGPT + Grok, both concur)*
- [ ] **CL-22** *(new, 25 Jul)* Board-level KPIs in the Executive Presentation are
  not anchored to any build artefact. Document-currency defect, deliberately kept
  out of the B11 gate so the standing gate checklist does not carry a deck's
  obligations. Apply at next BA revision alongside CL-17/19/20. *(Source: WS-D
  RAT-01 §7, dispositioned from a reviewer amendment)*

## Workstream E — Engineering process & protocols
- [ ] **CL-E1** (carried in) Record the force-push-to-main incident + add a guard
  (branch protection / documented exception). *(F-007)*
- Q-A6 root-cause fix lands here: trail docs update in the same commit as the work
  they record (see trail-integrity note above).

## Workstream F — Regulatory / bank-reviewer lens
*(applied throughout; synthesised at end)*
