# SESSION HANDOVER — ArcaAI (close of 2026-07-24, PM)

*Supersedes SESSION_HANDOVER_2026-07-24. This session: **Governance
Checkpoint 01 RUN AND CLOSED** — three-round panel protocol (ChatGPT +
Grok), converged same day, unanimous, zero dissents, sixteen items
ratified (CF-1..2, RAT-01..14). Pack landed via PR #23 (`c528478`);
closure PR PR #24 (merge `ee0c916`) carries the outcome document,
working papers, all four circulation packs, DEC-0009, and the chair
actions. WS-E candidates 35–36 drafted, not yet in ledger.*

## Boot line (paste to resume)
> Resume ArcaAI — Checkpoint 01 CLOSED (PR #24, `ee0c916`;
> outcome docs/governance/GOVERNANCE_CHECKPOINT_01_outcome.md).
> **NEXT: WS-D — Build & Quality Plan session.** WS-D absorbs:
> (a) CF-1 conformance spot-check design for the B7 gate; (b) plan
> refresh to gate-based schedule per RAT-01; (c) RAT-02 governance
> trio (audit logging, execution metadata, request wrapper) planned as
> pre-B7 work; (d) SS1/23 principle mapping for the B8/B9 artefact set
> (see Regulatory watchlist); (e) disposition of the five step-change
> candidates (section below — outcome-capture-in-B9 is the one needing
> a real decision). First micro-action before WS-D: commit
> WS-E items 35–36 (drafts below) + this handover. Build resumes at
> B7 (Fraud RAG) after WS-D. Boot ritual: conda activate `arcaai` →
> git switch main → git pull --ff-only → git fetch --prune. No live
> services needed for WS-D.

## What was done (24 Jul PM)

### Governance Checkpoint 01 — full cycle in one day
- Pack committed (PR #23, `c528478`, both pipelines green).
- Round 1 circulated; independent reviews received. Capture incident:
  Grok's output pasted twice unlabelled, nearly entered record as
  ChatGPT concurrence; caught by coordinator text comparison (WS-E 36
  candidate).
- Round 2: chair corrections (CL ledger ages; CL-08 actual content —
  Grok's R1 remedy had misread it; CL-10 double entry discovered
  during extraction; exposure statement). Grok withdrew its safety
  Must-Fix precondition; ChatGPT adopted threat catalogue,
  residual-risk statement, and the six-week cadence backstop.
- Round 3: convergence pack, 16 items, both reviewers full CONCUR,
  no factual objections. ChatGPT explicitly authorised B7 progression
  subject to RAT-02 + chair actions.
- Chair rulings: CR-1 six-week cadence backstop retained; CR-2 safety
  trio = B8 Must-Fix exit criterion AND precondition for any external
  exposure, whichever first.
- Chair findings: CF-1 architecture-conformance gap (standing gate
  question established; spot-check design → WS-D; retrospective audit
  rejected); CF-2 chair actions executed.

### Closure PR PR #24 — nine files
- New: outcome doc (with obligations register + next checkpoint due
  **B8 gate or 2026-09-04**), working papers (Grok verbatim; ChatGPT
  R2/R3 condensed with capture notes — verbatim swap remains an open
  offer), four circulation packs.
- BUILD_TRACKER.md: RAT-01 executed — week column removed, variance
  note; standing Gate review checklist (CL-08 decision-capture +
  CF-1 conformance questions); Gate Acceptance Record required in
  every B*_GATE.md from B7; stale B6 "this PR" reference fixed.
- DECISIONS.md: DEC-0009 (cadence: 2 gates OR 6 weeks + trigger
  list); DEC-0008 reversibility sentence (RAT-08).
- GOVERNANCE_REVIEW_CHANGELOG.md: CL-08 closed (CF-2a, executed as
  the BUILD_TRACKER checklist); CL-10 phantom open entry corrected
  (CF-2b).
- Edits ran via guarded PowerShell script (anchor-count checks),
  removed before commit.

## WS-E candidates 35–36 (commit next session; full drafts)

**35 — Script-delivery encoding + CWD class (24 Jul).** A BOM-less
UTF-8 .ps1 was parsed by Windows PowerShell 5.1 as ANSI: each em-dash
(E2 80 94) decoded via Windows-1252, whose 0x94 is a curly closing
double-quote — silently terminating string literals and producing
misleading parser errors. Second clause, same script: `[IO.File]`
static methods resolve relative paths against the .NET process CWD
(unchanged by Set-Location) — first run looked for DECISIONS.md in
C:\Users\mikek. Third clause: downloaded scripts carry Mark-of-the-Web
and need Unblock-File under RemoteSigned. All three caught before any
write (guards held; nothing corrupted). **Rules:** (a) .ps1 delivered
for PS 5.1 execution = UTF-8 WITH BOM (repo .md stays no-BOM — the
two rules coexist for different consumers); (b) any script using
[IO.File] pins `[Environment]::CurrentDirectory = (Get-Location).Path`
or uses absolute paths; (c) Unblock-File step in the delivery sequence.

**36 — Panel-capture labelling (24 Jul).** Round 1 outputs returned
unlabelled; a duplicate of Grok's review was initially presented as
ChatGPT's, and byte-identical text nearly entered the record as two
independent concurring reviews. Caught by coordinator comparison
before analysis. **Rule:** panel outputs labelled reviewer + round at
the moment of capture; coordinator runs a distinctness check before
cross-round analysis.

## Regulatory watchlist (established this session; UK position July 2026)

- UK regulators (FCA/PRA/BoE) continue overseeing AI through existing
  frameworks — no bespoke AI statute; BoE/PRA reaffirmed the
  technology-agnostic approach 1 Apr 2026. Operative set for target
  customers: SS1/23 MRM, SM&CR, Consumer Duty, operational resilience.
- **FCA guidance on audit trails + human-in-the-loop expected during
  2026** (Treasury Committee pressing for comprehensive guidance by
  end-2026 incl. SM&CR accountability for AI harm). When published:
  fires a RAT-12 exceptional-checkpoint trigger; design input to B9
  audit-trail replay and RAT-02 logging. Market tailwind — regulator
  about to require what B9 builds.
- CTP designations expected from HM Treasury during 2026; UK bank
  customers will push SS2/21 outsourcing requirements onto vendors.
  DORA applies vendor-side only if selling into EU-supervised banks.
- **WS-D scope notes (carry in):** SS1/23 principle mapping for the
  B8/B9 artefact set; B9 to track the FCA audit-trail guidance.
- **CL-17/19/20 bundle candidate:** vendor-side regulatory posture
  paragraph (SS2/21 readiness, CTP awareness, DORA-if-EU) in BA
  positioning. Raise as CL at bundle time, not before.

## Step-change candidates (Grok, post-checkpoint aside — WS-D input, NOT ratified)

Arrived outside panel protocol after Round 3; no bearing on B7 start
(RAT-14 stands). WS-D disposes of each — adopt (with DEC where scope
changes a locked plan stage, per the DEC-0005 pattern), park, or
reject:

1. **Outcome capture as architecture (strongest).** Minimal
   `outcome_event` contract + append-only table into B9 alongside
   audit-trail replay; synthetic labels acceptable in reference
   build. Directly evidences the Learning Bank L3/L4 claim — same
   claim-vs-evidence gap class DEC-0006 governs. Scope change to
   locked B9 → needs DEC if adopted.
2. **Proactive OPA-before-LLM** (high-stakes rules consulted before
   generation, not filtering after). This is B8 done well, not new
   scope; feed the three example rules (no binary credit decision;
   no uncited regulatory clause; HITL above risk band X) into the
   RAT-05 threat catalogue as seed cases; RAT-06 precedence hierarchy
   settles ordering.
3. **Model-risk tiering:** record framework only (Tier 1 = challenger
   + independent validation required at production promotion, NOT in
   reference build) inside RAT-07 artefacts at B8 exit. Full
   challenger build rejected as gold-plating.
4. **Retrieval confidence as live signal:** cheap half only —
   confidence thresholds + "insufficient evidence" fallback path in
   B7. Full per-query RAGAS-in-the-loop conflicts with the R7
   retrieval rung; offline RAGAS stays as planned.
5. **Process-intelligence metrics as product surface:** B11 design
   note only; reframing, not capability.

## Findings / riders (carried)
- WS-E 1–23 backfill rider (source material 07-20..07-23 in
  D:\Downloads; delete stale unsuffixed 07-22b — repo copy is
  reference).
- decisions/ → adrs/ rename: NAMED BACKLOG (two strikes).
- Locked-suite disk sprawl purge (D:\ArcaAI-locked\, Downloads strays,
  superseded BA v1.0 in SmartDog_V4\docs\CURRENT\).
- CL-17/19/20 bundle → next BA revision; **hard trigger ratified:
  post-B8** (RAT-11); + regulatory-posture candidate above.
- CL-09 (Model Card) executes before any external review (RAT-11).
- prompts/ scaffold decision deferred to B8 (unchanged).
- Working papers verbatim swap (ChatGPT R2/R3) — open offer, optional
  hygiene.
- Obligations register lives in the outcome doc — WS-D and the B7/B8
  gates consume it; do not restate obligations elsewhere (point at it).

## Environment
- Unchanged. arcaai conda env (Python 3.11.15). Nothing live needed
  for WS-D. B7 will bring ChromaDB into scope.

## Governance state
- **CHECKPOINT 01 CLOSED (unanimous)** · B1–B6 gated · WS-A/B/C
  CLOSED · **NEXT: WS-D → B7** · DEC through **0009** · ADR through
  0009 · CL open backlog: CL-06, 07, 09, 11, 16, 17, 18, 19, 20
  (CL-08 and CL-10 state resolved this session) · WS-E in-repo at 34
  + candidates 35–36 pending commit · Standing gate checklist + Gate
  Acceptance Record binding from B7 · Next checkpoint: B8 gate or
  2026-09-04, whichever first (DEC-0009).
