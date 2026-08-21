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
  post-review. *(2026-07-27: CL-23 gap 1's policy-plane scope statement is
  due in this brief at B8 entry; cross-referenced here because the
  dependency ran one way only.)*
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
- [ ] **CL-23** *(new, 25 Jul, DRAFT pending panel review)* Policy-as-code extended
  to the governance layer: the bank's data, security and AI policy expressed as
  versioned, tested, declarative bundles the platform deploys and enforces, with
  every decision recording which policy governed it. Three-tier framing extends
  the CL-21 mechanism/policy table: structural audit invariants (Tier 1) are
  explicitly **not policy-addressable**, including by the bank; bank policy as
  code (Tier 2) lands on existing enforcement points — the disabled retention
  mechanism, the emit denylist as a one-way ratchet, promotion-gate appetite,
  replay/subject authorisation and Art 22C human-routing; human judgement
  (Tier 3) stays outside the engine. Seven gaps; the sole pre-B8 build
  consequence is `policy_version` in execution metadata (nullable-until-
  available, the `subject_ref` pattern repeated — cheap now, a migration on a
  populated append-only table later). One principles-set addition proposed
  ("Bank policy is code"), bundled with CL-21's at the same review. Scope
  statement due in the B8 design brief (with CL-18); no policy evaluation in the
  retrieval hot path; **not a B7 blocker**. Full text:
  `docs/governance/CL-23_policy-as-code.md`. *(Source: evening session 25 Jul,
  arising from Executive Presentation v12 and the CL-21 framing; numbering note
  in full text — the morning's withdrawn checker-bug draft never entered this
  register)*

- [x] **CL-24** *(new, 6 Aug; CLOSED 2026-08-12)* Governance test suite must not
  default into the dev database: isolate `conftest.py` DSN defaults to a scratch
  database or schema, and/or roll back rather than commit fixture
  `corpus_version` rows. Until then, running the governance tests locally
  recreates the WS-E 61 condition. *(Source: WS-E 61 — rehash_sweep first run,
  6 Aug; fixture rows found in the dev `corpus_version` table from the 30 Jul
  test run)*
  **CLOSURE.** Parts (a) separability, (b) write-path guard and (d)
  excluded-by-rule as a named sweep category discharged at PR #96, ruled at
  DEC-0016: separation by database, the suite on `arcaai_audit_test`, the
  governed `arcaai_audit` never a test target. Part (c), residue cleanup,
  discharged 2026-08-12 as an owner-role act at the operator's terminal —
  identity-scoped deletes in FK order, each asserting its own row count inside
  one transaction, no `TRUNCATE` and no unqualified `DELETE`. Evidence, all
  taken non-elevated as `arcaai_app`: `rehash_sweep.py` GREEN at **exit 0**
  with `irreproducible-pin : 0` and `excluded-by-rule (test) : 0`, reporting
  "all pins verified"; five-table count **0/0/0/0/0**; and the AFTER-CLEANUP
  section of `docs/governance/CL-24_governed-store-baseline_2026-08-12.md`
  carrying identity digest
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, the
  SHA256 of the empty string. **Scope was widened during the act on evidence:**
  `audit_payload` held 3 test-written rows visible to neither the baseline
  instrument nor the sweep, and was ruled in and cleared rather than left as
  residue no monitored instrument could report. Instrument extension to five
  tables is carried at `CLAUDE.md` queue item 28.
- [ ] **CL-25** *(new, 6 Aug)* Operational ingest must write the
  `corpus_version` evidence row: wire `corpus.load_snapshot` into the ingest
  path so real loads produce real pins (DEC-0014 intent; the row is currently
  written only by tests — the `.6` run of record was never row-recorded).
  Candidate home: inc4 governance wiring; rule scope at inc4 entry.
  *(Source: WS-E 61)*
- [ ] **CL-26** *(new, 12 Aug)* D2.2a pre-flight implementing artefact:
  `scripts/d22a_preflight.py`, asserting the four D2.0 entry-criteria
  assertions as one standalone invocable script — non-elevation first and
  gating, ONNX/chromadb cache traversal by read rather than existence, services
  including the vector store's exists/readable/writable triple, and conda
  environment identity. Three outcomes per assertion (GREEN/RED/UNKNOWN);
  UNKNOWN and SKIPPED both exit non-zero and never collapse into green.
  Discharges the authoring debt at which the traversal check existed only as
  prose in `CLAUDE.md` and `.claude/skills/session-open/SKILL.md` with no
  script behind it and no non-elevation assertion at all. **Open at authoring:**
  the ceremony skills still describe the procedure rather than calling this
  script, which is the remaining half of the debt and is an edit to ruled
  ceremony artefacts, held for operator ruling. *(Source: DEC-0015 proof-first
  sequencing; `docs/governance/D2.0_COMMISSIONING_FRAME_2026-08-11.md`;
  `docs/governance/FINDINGS_2026-08-11_onnx-acl-root-cause.md` sections 4-6)*
- [x] **CL-27** *(new, 13 Aug; CLOSED 2026-08-13)* D2.2a runner spike: the
  minimal scenario runner at `arcaai/harness/runner.py` — spec in, corpus queried
  at a pinned snapshot, result JSON out — built from nothing, the harness package
  having held only its `arcaai/harness/__init__.py` and the v0.1 schema. Runs
  under the D2.0 commissioning frame, COMMISSIONING-labelled throughout, results
  permanently inadmissible as gate evidence. *(Source: `CLAUDE.md` queue item 30;
  `docs/governance/D2.0_COMMISSIONING_FRAME_2026-08-11.md`;
  `docs/governance/TOR_test-capability_RevC_RULED_2026-08-10.md` section 5A)*
  **CLOSURE.** Discharged 2026-08-13 on branch `commissioning/d22a-spike-cl27`,
  runner commit `7bad3b7`. Exit criterion met: **REPRODUCIBLE: YES** — two runs of
  scenario RQA-001 at the same triple produced comparable-content sha256
  `4124f3359b584be1ba92397526e74828af79becd64302f0b437bdd3cc881b1a3` on both,
  verified by a recompute external to the runner, with the generated timestamp the
  only differing key across the two complete artefacts. The scenario's own
  pass/fail is **not** an exit criterion and none is recorded: RQA-001 scored
  recall_at_k 0.0, carried as finding F1 and routed to the Test Plan (D1.1), not
  chased in-spike and nothing tuned to produce a match. Refusals proved rather
  than assumed: four deny-shaped probes refused at **exit 2, 3, 3 and 4**, each
  naming what failed, the two pin probes isolated to one wrong pin each so they
  evidence that the runner names the correct pin; result-artefact count 2 before
  and 2 after, so refusals write nothing. Boundaries held: chromadb reaches the
  runner only through ChromaStore (CF-1/B7-a), and nothing imports from the
  verticals tree with no vertical-shaped default anywhere (ADR-0009). Full record:
  `docs/governance/COMMISSIONING_SESSION_RECORD_2026-08-13_d22a-runner-spike.md`,
  the first instance of the Commissioning Session Record form. F2 and F7 opened as
  queue items, F6 attached to the Arc 2 combined pull request, and F8 — where a
  Commissioning Session Record lives is ruled only in part — raised for a future
  ruling.
- [x] **CL-29** *(new, 16 Aug; CLOSED 2026-08-16)* D2.2a runner spike, arc 2: the
  spike proper, of which CL-27 built the runner. Scenario **RQA-107** — the Rev C
  Appendix A.1 Statute slot — authored, validated against scenario spec schema
  **v0.2**, and executed end-to-end against the pinned corpus snapshot
  `2026-08-13.8`. COMMISSIONING throughout, results **permanently inadmissible as
  gate evidence**. *(Source: `CLAUDE.md` queue item 30; operator rulings of
  2026-08-16 at arc open, entry-gate ordering, scenario approval, execution and
  closure)*
  **CLOSURE.** Discharged 2026-08-16 on branch `build/d22a-spike-2-2026-08-16`,
  the runner unmodified at `0.1.0-commissioning`. Exit criterion met:
  **REPRODUCIBLE: YES** — four runs at the same triple produced comparable-content
  sha256 `aeed275708bd4b67900d37c763479beb19fe96644ac58bf72aba371624a209ef` on
  every one, verified by a recompute external to the runner, with **exactly one
  field differing** across the complete artefacts — `generated_at_utc`, classified
  run-metadata — and the raw float scores comparing exactly equal with no rounding
  applied. The scenario's own pass/fail is **not** an exit criterion and none is
  recorded: RQA-107 scored recall_at_k 0.0, acceptance NOT EVALUATED, nothing
  tuned. Validation was both-halves: four deny-shaped mutations refused at exit 2
  each naming the fault, of which **D1 is the schema discriminator** — dropping
  `retrieval_snapshot_sha256` yields a spec that passes under v0.1, so its refusal
  is positive evidence that v0.2 was the schema applied, which no allow-shaped
  pass could establish. Rev C section 5.2 criterion 4 takes its **first live
  discharge**: E was fixed at authoring and stated before any retrieval ran.
  **Finding yield: ELEVEN unhonoured items**, six runner-side and five spec-side,
  each with a fix route, recorded as findings for the Rev C acceptance stop rather
  than as defects in Rev C, which is UNACCEPTED with a delta round in flight. The
  first material-parameter list is authored as a runner-build artefact carrying
  **two** hashes, the definition's and the observed values', so a narrowing of what
  counts as material is itself detectable. Two instrument defects are recorded,
  both the harness's own, including an abort probe INDETERMINATE twice whose first
  summary line is retracted verbatim. Full record:
  `docs/governance/COMMISSIONING_SESSION_RECORD_2026-08-16_d22a-runner-spike-2.md`,
  sha256 `84738dc44ab2a3a46f8ca90359175f3fdebcff56fd4d7091e5c4d88d08d19a0a`, the
  second instance of the Commissioning Session Record form. *(Hash note,
  RE-PINNED 2026-08-16. The record has carried three values and all three are
  named so the trail is followable: `f0236cd3…a307b150` at first commit
  (`c7ae90d`); `67a401a1…89ab7dec` once this CL-29 claim was written into it,
  which is the value this entry cited at merge; and `84738dc4…08d19a0a` after the
  section-15 custody correction merged at `c02147a`, which is the value cited
  above. Re-pinned on the operator's ruling rather than left to resolve by path
  alone: a ledger entry whose hash no longer matches its subject is a pin that
  has stopped pinning, and the correction it missed was itself a hash defect.)*
  Artefact preservation is **DISCHARGED 2026-08-16 by read-back**: the spec, the
  environment-identity artefact and the four result artefacts were copied to
  `D:\ArcaAI-artefact-custody\2026-08-16-spike-2\` and re-hashed **at the
  destination**, six of six matching the corrected section 15, whose expected
  values were parsed from the committed record rather than restated.
- [x] **CL-30** *(new, 16 Aug; CLOSED 2026-08-16)* **D1.1 Test Plan ACCEPTED at
  Rev C.** The panel process closes. Rev C, sha256
  `9d6ab3b0da21d5e6603f7fa505d48a892da9acf11dba60725b83e5a8c590e88c`, is ruled
  ACCEPTED by the chair on 2026-08-16 under the acceptance rule at
  `docs/governance/D1.1_PANEL_ROUND2_CIRCULATION_PACK_2026-08-15.md` §2.1: the
  round returned no finding rated BLOCKING or MATERIAL and sustained at that
  severity. *(Source: chair ruling 2026-08-16; `CLAUDE.md` queue item 18;
  `docs/governance/TOR_test-capability_RevC_RULED_2026-08-10.md` section 5A)*
  **CLOSURE.** Discharged by a light delta round to the same four reviewers,
  scope confined to the nine residual MATERIAL findings, each reviewer verifying
  only its own. **Nine of nine returned DISCHARGED** — Grok 2, ChatGPT 1,
  DeepSeek 2, Gemini 4 — with **zero dissents and zero defects-in-fix**. Full
  return, so the non-response machinery was never engaged and **no finding
  carries a chair-adjudicated-unverified marking**. The `F-DS-11` +
  `F-GEM-REG-04` composite was verified from both sides independently and both
  returned DISCHARGED, so the anticipated divergence adjudication was not needed.
  The round's only chair severity movement, `F-GEM-REG-01` from BLOCKING to
  MATERIAL with a remedy the reviewer did not propose, was verified and
  discharged by that reviewer against the **adopted** remedy. Custody checked
  rather than assumed: all four reviewers received Rev C at the governing hash
  and the **post-amendment** same-day delta pack `765eedaf…dc4e8378`, verified by
  hashing the per-reviewer outbound copies. Two matters recorded rather than
  smoothed: Gemini's verdicts came on a third prompt after two non-responsive
  summaries were rejected on form and not landed, and Gemini's return did not
  restate the reviewed hash as the pack's return conditions require.
  **Consequences:** D1.1 exits DRAFT at Rev C, the filename rename being a
  separate owed act; the `TOR §5A` precondition for Regime 2 is SATISFIED; and
  the `TOR §5A:101` post-acceptance amendment route is now OPEN, its first
  customer the TOR-side three-leg identity statements deferred at `F-GROK-08`.
  Acceptance does not make Regime 1 results admissible and does not lift the §2.4
  external-reliance bar. Full record:
  `docs/governance/D1.1_REVC_ACCEPTANCE_2026-08-16.md`, with the four returns
  committed verbatim as
  `docs/governance/DELTA_RETURN_D1.1_RevC_from_GROK_2026-08-16.md` and its three
  siblings.

## Workstream E — Engineering process & protocols
- [ ] **CL-E1** (carried in) Record the force-push-to-main incident + add a guard
  (branch protection / documented exception). *(F-007)*
- [ ] **CL-28** *(new, 15 Aug)* `docs/governance/review-protocols.md` uses one
  word for two different round outcomes. Its "When a round fails" section
  prescribes that the failed round is "**re-run** with the same reviewers — not
  the next round", and reads as governing every negative outcome, because nothing
  distinguishes a round that **did not complete** from a round that **completed
  and returned a negative verdict**. Define both. **Process-incomplete** — the
  round did not finish, so it is re-run with the same reviewers and the next round
  does not open. **Verdict-negative** — the round completed, every finding and
  dissenting position was disposed, and the document was not accepted, so the
  round closes and the next round proceeds under a fresh disposition. Wording tidy
  only: no change to protocol substance is intended or authorised by this item,
  and the three-round structure, bench lists and acceptance route are untouched.
  *(Source: operator ruling 2026-08-15 on D1.1 round identity — Reading B. Round 1
  of the D1.1 Test Plan **completed with a negative verdict and did not fail**:
  four reviews received; 26 findings and four dissenting positions all disposed
  through a committed per-finding disposition table; and the round's single
  BLOCKING finding, `F-DS-04`, converted at the chair's stop into bounded Rev B
  obligations, since discharged. The re-run clause governs process-incomplete
  rounds and does not bite here. Ambiguity surfaced at the Rev B round-2 readiness
  assessment. **Count note:** the disposition's own factual note corrects its chair
  statement's "2 dissents" to four — two unnumbered ChatGPT dissents plus DeepSeek
  D-001 and D-002 — and the corrected figure is used here rather than the
  superseded one. Detail:
  `docs/governance/D1.1_PANEL_ROUND1_DISPOSITION_2026-08-14.md`.)*
- Q-A6 root-cause fix lands here: trail docs update in the same commit as the work
  they record (see trail-integrity note above).
- [x] **CL-31** *(new, 21 Aug; CLOSED 2026-08-21)* **Harness uplift disposition
  (Chair ruling 21 Aug 2026).** **Item 1** (root `CLAUDE.md`) executed
  **append-only**, scoped to the seven gaps in the PROMPT 136 audit list (b); the
  brief skeleton is **discarded as superseded by the live file**. **Item 2**
  (settings-side `permissions.deny`) is **PARKED into the F5 design brief, not
  struck**: there is **no DEC-0018 conflict**, the struck mechanism having been the
  *allow* half, but it is blocked on (i) deny-versus-hook firing order being
  unprovable from inside the harness and (ii) **observability polarity** — a deny
  firing before `PreToolUse` may widen the WS-E 75 gap. Revisit in F5 with an
  externally designed probe. **Closed as a disposition, not as completed work:**
  the parked half is carried at `CLAUDE.md` queue item 48, and no
  `.claude/settings.json` change was made under this item or is authorised by it.
  *(Source: chair ruling 2026-08-21, R-a and R-b; the PROMPT 136 read-only gap
  audit; `DECISIONS.md` DEC-0018 for the struck mechanism, with the operative
  sentences at `docs/governance/DEC-0018_A6_CORRECTION_2026-08-19.md` section 3(a);
  `DECISIONS.md` DEC-0019 and `docs/governance/WS-E_INCIDENTS.md` item 77 for the
  transcribed sources of the seven appends.)*

## Workstream F — Regulatory / bank-reviewer lens
*(applied throughout; synthesised at end)*
