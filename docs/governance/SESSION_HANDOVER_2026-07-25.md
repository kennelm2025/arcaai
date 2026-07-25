# SESSION HANDOVER — ArcaAI (close of 2026-07-25)

*Supersedes SESSION_HANDOVER_2026-07-24c. This session: **WS-D opened
and CLOSED in full** — all four items ratified. Nine PRs merged (#26
through #33). B7 entry criteria reduced from five open to two, both
self-resolvable. Docs CI now runs pre-merge, closing WS-E 45 two days
inside its own deadline.*

## Boot line (paste to resume)

> Resume ArcaAI — WS-D CLOSED (RAT-01/DEC-0010, CF-1 method, RAT-02 +
> ADR-0010, SS1/23 mapping + DEC-0012). **NEXT: build the RAT-02
> governance trio, then pin ChromaDB — the last two B7 entry criteria,
> both self-resolvable.** Then sign B7 entry and open the stage. Boot
> ritual: conda activate `arcaai` → git switch main → git pull
> --ff-only → git fetch --prune → **`python scripts/repo_manifest.py`
> and attach REPO_MANIFEST.md** (new this session — structure,
> register numbering, gate state, open CLs, generated not recalled).
> Postgres needed for the trio; ChromaDB from B7.

## What was done (25 Jul)

### WS-D — Build & Quality Plan, all four items

**Item 1 — RAT-01 gate-based plan refresh. Ratified as DEC-0010,
PR #26 (`fc125e8`).** Full text
`docs/governance/WS-D_RAT-01_GATE_PLAN.md`. The load-bearing change is
not the schedule shape but the timing: **gate documents are created at
stage entry with exit evidence blank**, not written retrospectively at
close. A gate doc written at close is a report whose criteria are
inferred backwards from whatever evidence exists. Ten sub-decisions,
including: `Depends on` replaces `Wk`; the tracker links to gate docs
and never restates criteria; five-section gate schema; the not-allowed
deferral list **is** the required-evidence list and must be exhaustive
at entry; evidence immutability with path-@-SHA citation and CI results
transcribed as text because Actions logs expire at 90 days;
external-dependency flag on entry criteria; `outcome_event` as a
non-deferrable B9 exit item on SS1/23 monitoring grounds.

**Item 2 — CF-1 conformance spot-check method. Ratified, PR #30
(`10ade6c`).** `docs/governance/CF-1_SPOT_CHECK_METHOD.md`. Claims are
nominated at stage *entry*, before the code exists — a spot-check
chosen at gate close is contaminated by already knowing what is fine.
At least one nomination must be one the author expects to be awkward,
or the gate record must state why none could be found. Four B7
nominations recorded in `B7_GATE.md` §1.1.

**Item 3 — RAT-02 governance trio specification + ADR-0010, PR #29
(`c528e54`).** `docs/governance/RAT-02_GOVERNANCE_TRIO_SPEC.md`,
`decisions/0010-platform-governance-instrumentation.md`. Specified, not
built — see Next session.

**Item 4 — SS1/23 principle mapping + DEC-0012, PR #31 (`7965adb`).**
`docs/governance/SS1-23_PRINCIPLE_MAPPING.md`. Evidential, not
declarative: artefacts provide evidence supporting a firm's compliance;
they do not satisfy principles, which attach to firms.

### Other decisions and artefacts

- **DEC-0011 — B7 corpus is synthetic plus a named OGL subset**
  (PR #28, `e5025a0`). FCA Handbook terms prohibit inclusion in any
  public *or private* electronic retrieval system without prior written
  permission; a ChromaDB index is one on the plain reading. Local-only
  ingest outside the repo was considered and **rejected** — it fixes
  publication, not the retrieval-system prohibition, because the local
  index is itself the restricted artefact. Recorded as rejected because
  it is the intuitive answer and will be proposed again.
- **CL-21 (data protection and record retention) and CL-22 (board-level
  KPIs unanchored)** filed, PR #27. CL-21 full text at
  `docs/governance/CL-21_data-protection.md`.
- **`docs/build/B7_GATE.md` created at entry** — first artefact under
  the new regime. Two of five entry criteria met.
- **B2 trail-integrity defect** — `B2_GATE.md` carried every criterion
  unticked while the tracker recorded GATE PASSED. Gate confirmed
  passed; ticks applied with a dated addendum stating they are
  retrospective, plus corroborating evidence from B3_GATE.md that does
  not depend on B2's own document.
- **BUILD_TRACKER** implements the RAT-01 shape: `Depends on` and
  `Gate doc` columns, checklist ownership split with the plan (tracker
  owns the Gate Acceptance Record spec; plan §4 owns the standing
  checklist).
- **WS-E 41–48 + two standing principles**, PR #32 (`eec9d58`).
- **Docs CI + structural checks + boot manifest**, PR #33 (`ab913b9`).

## Carried to next session

### 1. Build the RAT-02 trio (largest item)

Spec is ratified; the code is not written. `platform/governance/` —
`wrapper.py`, `metadata.py`, `audit.py`, `events.py`, `models.py`.
Three Postgres tables, append-only. Key design points that are easy to
lose in implementation:

- Terminal run record on **every** exit path including unhandled
  exception, in a `finally`; exception type and message but **not** the
  traceback, which can carry payload into the record.
- **Sequence number, not timestamp**, is the ordering key — two events
  in the same microsecond need deterministic order for B9 replay.
- `emit` takes a **typed event object, not a free-form dict**.
  Personal data is excluded by construction; runtime detection on
  values cannot distinguish a name from any other string.
- Prompt/response text stored **by reference** in a content-addressed
  table, never inline — this is what makes CL-21 crypto-shred possible.
- Indexed `subject_ref` on `audit_run` from the outset.
- Unpopulated metadata fields are `NULL`, never `""` or a sentinel.
- Boundary test (`platform/` imports nothing from `verticals/`) is
  mandatory evidence for the B7 CF-1 spot-check.

### 2. Pin ChromaDB

`pyproject.toml`, pinned, import verified from outside the repo root
per the B5 packaging precedent. **Local install, not AWS** — DEC-0008
moved the DVC artefact store to S3 and explicitly left the
deployment-target question PARKED; nothing points compute at AWS. A
remote store would also put a network hop inside the R7 <100 ms
retrieval rung, making CF-1/B7-d meaningless.

### 3. CL-23 — WITHDRAWN, was a checker bug

An earlier draft of this handover carried CL-23: that DEC-0007 retired
`docs/specs/`, `docs/rfcs/` and the review-protocol scaffold but left
`CONTRIBUTING.md` and `SESSION_PROTOCOLS.md` still pointing at them.

**It was wrong, and no CL is raised.** The ten baselined findings behind
it were artefacts of a resolution bug in `check_docs.py`, which resolved
cited paths only from the repository root. Three conventions are in use
and all are legitimate: root-relative; relative to the citing file's own
directory (`docs/DESIGN_PHASE_CHARTER.md` citing
`governance/sme-panel.md`); and relative to `docs/` (root-level
`CONTRIBUTING.md` citing `specs/_template.md`). Every one of the ten
resolves under one of the latter two. The directories are all present in
the tree — the manifest shows them.

Fixed the same day; the baseline is now empty. The lesson is the one
worth keeping: **a new check's first findings are as likely to indict
the check as the repository**, and CL-23 came within a session of being
written against a retirement that had been carried out correctly.

### 4. Transcribe today's CI results

Per RAT-01 §3.1, evidence is transcribed as text because Actions logs
expire at 90 days. Not yet done for this session's runs. The gate-
relevant one is `ci-docs #2 · success · 2026-07-25 · 11s` on the
`wse-45-docs-ci` head — the first pre-merge check in the programme.

### 5. Minor

- **`docs/governance/~$caAI_Banking_Architecture_v1_0b.docx` is
  committed** — a Word lock file. B5_GATE's residuals list flagged the
  `~$*` gitignore line as housekeeping and it never landed. Add the
  ignore and `git rm --cached`.
- **`SESSION_HANDOVER_2026-07-24c.md` is not in the repo** — the
  handovers run 07-24 → 07-24b → 07-25. The document that opened this
  session was never committed, so this one's supersession line points
  at nothing in the tree. Commit it from the Downloads copy or reword
  to supersede 07-24b.
- `reviews/2026-06-arch-review/1739140963936 (1).gif` — a
  download-suffix duplicate committed before WS-E 38 existed.
- `REPO_MANIFEST.md` is gitignored and generated on demand. A manifest
  generated Monday and pasted Thursday is the stale artefact it exists
  to prevent — regenerate at boot.

## B7 entry status

| Criterion | State |
|---|---|
| B6 gate passed | **met** |
| RAT-02 trio landed | open — specified, not built |
| ChromaDB pinned | open |
| Corpus sourcing DEC | **met** — DEC-0011 |
| CF-1 spot-check design | **met** — method ratified |

Nothing external outstanding. Entry sign-off happens in `B7_GATE.md`
when the two remaining criteria close.

## New this session — tooling

- **`scripts/check_docs.py`** — bold parity, backtick parity, cited-path
  existence, LF endings. Each check exists because something broke. Ten
  pre-existing findings baselined with reasons.
- **`scripts/repo_manifest.py`** — generates `REPO_MANIFEST.md`:
  structure, next free DEC/ADR/CL/WS-E numbers, gate state, open CLs,
  git state. **Run at boot and attach.** Five path failures this
  session came from asserting structure from memory.
- **`.github/workflows/ci-docs.yml`** — fires on `pull_request` for
  `docs/**`, `decisions/**`, root markdown. Both existing workflows
  filtered docs out of their `pull_request` paths while running
  unfiltered on push to main, so no governance PR had ever reported
  before merge.

## Findings / riders (carried)

- WS-E 1–23 backfill rider — source material 07-20..07-23; Downloads
  was cleared 24 Jul, confirm sources survived or use repo handover
  copies.
- `decisions/` → `adrs/` rename: NAMED BACKLOG (two strikes).
- Locked-suite disk sprawl purge.
- CL-17/19/20/21/22 bundle → next BA revision; hard trigger post-B8
  (RAT-11). CL-21 adds the §2 SS1/23 scope-precision text and the
  Principle 4 claim-discipline statement.
- CL-09 (Model Card) executes before any external review (RAT-11).
- **G10 external domain reviewers — priority raised.** The SS1/23
  mapping makes them the only pre-client approximation of Principle 4
  independence. Still no date.
- prompts/ scaffold decision deferred to B8.
- Obligations register in the Checkpoint 01 outcome doc — point at it,
  do not restate.

## Regulatory watchlist

- **UK GDPR Article 22 was replaced by Articles 22A–22D on 5 February
  2026** (Data (Use and Access) Act 2025). Default moved from
  prohibition to permission-with-safeguards: transparency before the
  decision, right to human review, right to contest. Special category
  data restricted under 22B. This *favours* the platform and the
  safeguards map onto B9 artefacts already planned — the architecture
  should make that claim explicitly (CL-21).
- **SS1/23 scope precision**: applies to UK banks with internal model
  permissions for regulatory capital; within an in-scope firm it covers
  all models including fraud. Saying "SS1/23 requires this" to a bank
  without IM permissions is wrong and will be corrected in the room.
- FCA guidance on audit trails + human-in-the-loop expected during
  2026 — fires a RAT-12 exceptional-checkpoint trigger on publication;
  design input to B9.
- CTP designations expected from HM Treasury during 2026.

## Environment

Unchanged. `arcaai` conda env (Python 3.11.15). Postgres needed for the
trio build. ChromaDB enters scope at B7. `gh` CLI still not installed;
GitHub Desktop remains the PR route (web form 500s persisted).

## Governance state

**WS-A/B/C/D CLOSED** · B1–B6 gated · **NEXT: build trio → pin
ChromaDB → sign B7 entry → B7** · DEC through **0012** · ADR through
**0010** · CL open backlog: 06, 07, 09, 11, 16, 17, 18, 19, 20, 21, 22 · **WS-E in-repo at 48**, items 1–23
backfill rider open · Two standing principles established (Verify state
before mutating it; A caveat is not a gate) · Standing gate checklist +
Gate Acceptance Record binding from B7 · Next checkpoint: B8 gate or
2026-09-04, whichever first (DEC-0009).
