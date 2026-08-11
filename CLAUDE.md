# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. Guidance here is the soft layer; hard rules are also enforced by hooks in `.claude/settings.json` (see "Enforcement layer" below). If guidance and a hook disagree, the hook wins and the discrepancy is a WS-E item.

## What this repo is

ArcaAI — "the AI control layer for regulated banking decisions". A single monorepo
holding application code, ML code, IaC, prompt templates **and** the governance suite.
The build is a reference implementation on synthetic data, delivered through 12 gated
stages (B1–B12) plus B9.5. Currently **B7 (fraud RAG)**.

This is a governance-heavy repository. The document trail is a deliverable, not
overhead — several conventions below exist because a bank reviewer or auditor has to be
able to reconstruct a decision months later.

**Current state lives in the newest session handover.** The most recent
SESSION_HANDOVER file under `docs/governance/` is the single source of truth for the
state of play; `CURRENT_STATE.md` and `SESSION_PROTOCOLS.md` lag it. Read the newest
handover's boot line before trusting either.

**Register state is derived, never quoted from memory or from a found file.** This
document deliberately carries no register numbers, no corpus snapshot hash, no HEAD
sha — every static pinning of them has gone stale within a session (the CL-26
stale-origin pattern). Register numbering (WS-E / DEC / ADR / CL), build-stage state
and divergences come from `python scripts/repo_manifest.py` run **in this session**
(`/session-open` does this). A `REPO_MANIFEST.md` found on disk or pasted into
context is presumed stale until regenerated — its own header says so. Corpus
identity comes from `MANIFEST.yaml`; citation-edge minimums from `EDGES.yaml` at its
current version.

## Commands

```
pip install -e ".[dev]"        # Python 3.11+
scripts\dev_up.cmd             # Postgres :5432 + MLflow UI :5000 (needs Docker Desktop running)
scripts\dev_down.cmd
scripts\lint.cmd               # ruff check . — MUST be clean before every push (standing rule)
scripts\test.cmd               # ruff, then pytest --cov (fails under 60% coverage)
```

Targeted runs:

```
pytest tests/test_agent_graph.py -q                  # one file
pytest verticals -q                                  # vertical suites only (what ci-mlops runs)
pytest tests/governance -q                           # needs the dev Postgres stack up
pytest -k test_score_node -q                         # one test
python scripts/check_docs.py .                       # what ci-docs runs (markdown structural checks)
dvc repro verticals/fraud/dvc.yaml                   # regenerate the fraud pipeline
python scripts/b7_run.py                             # governed end-to-end agent run (dry-run; --live executes)
python scripts/rehash_sweep.py                       # standing boot act (corpus pin sweep; expect 0 pins)
python scripts/repo_manifest.py --out D:/Downloads   # session boot snapshot; write OUTSIDE the tree
```

`scripts\test.cmd` lints before testing deliberately — local/CI parity. Running bare
`pytest` skips the lint step that CI will fail on.

`tests/governance/*` and `tests/retrieval/*` need the dev stack; the governance suite
connects as two Postgres roles (`arcaai_owner` for DDL, `arcaai_app` for runtime) against
the `arcaai_audit` database, overridable via `ARCAAI_AUDIT_OWNER_DSN` /
`ARCAAI_AUDIT_APP_DSN`.

Three CI workflows, each with `paths` filters — check that a new directory is covered by
the right filter or PRs will report nothing and fail only after merge (this has happened):
`ci-devops` (lint + tests + coverage, with a Postgres service), `ci-mlops` (vertical
tests, corpus manifest verification, DVC promotion gate, manifest history sweep),
`ci-docs` (`scripts/check_docs.py`).

## Architecture

**Platform / vertical boundary (ADR-0009 — the load-bearing rule).**
`arcaai/platform/` holds *machinery*; `verticals/<name>/` holds *business semantics*.
Nothing in `arcaai/platform/` may import from `verticals/` — paths and config arrive as
arguments. Platform-side today: governance instrumentation and retrieval. The rest of the
ML lifecycle still lives in `verticals/fraud/` and gets extracted at stage B9.5; until
that gate passes, describe pipeline-as-platform as "architecturally specified, partially
evidenced" (DEC-0006), never "the platform exists".

**Request flow.** `api/` (FastAPI) → `agent/graph.py` (LangGraph:
`intake → score → retrieve → package`) → `verticals/fraud/serving/` (BentoML + the
calibrated scorer). Every live leg of the graph is behind a flag (`live_scoring`,
`live_retrieval`, `live_packaging`) that defaults to a deterministic stub, so CI runs
fully offline. Real dependencies are constructed at a composition root
(`scripts/b7_run.py`), never inside the graph — `build_graph` raises rather than guess a
store or a manifest version.

**Governance trio (`arcaai/platform/governance/`, ADR-0010 / RAT-02 spec).**
`governed_request(...)` mints a correlation id, captures execution metadata, and
guarantees a terminal record on every exit path (completed / failed / aborted). Nodes only
call `ctx.emit(TypedEvent(...))` or `ctx.emit_ref(...)`. Events are closed pydantic models
(`extra="forbid"`, 256-char string ceiling, PII field-name denylist enforced at class
definition). The audit store is **INSERT/SELECT only** — the `arcaai_app` grant in
`sql/governance_grants.sql` excludes UPDATE and DELETE, so append-only is a database fact
the test suite asserts, not a review convention. Adding an event type is a minor bump;
renaming or retyping one is a breaking change needing a DEC/ADR.

**Retrieval (`arcaai/platform/retrieval/`).** `interface.py` is store-agnostic;
`chroma_store.py` is the only module in the repo permitted to import `chromadb`, enforced
by a test. The embedding function is pinned explicitly and warmed at adapter construction —
never let Chroma's default embedding function run (it silently downloads an unpinned model
mid-query).

**Corpus manifest (DEC-0014).** `verticals/fraud/corpus/MANIFEST.yaml` is the sole
governing artefact for corpus identity, licence, classification and retrieval eligibility.
`arcaai/platform/governance/corpus.py` provides hashing and the append-only check; the
`corpus_version` Postgres row is *evidence a version loaded* and must never be used to
regenerate the manifest.

**Model artefacts.** DVC-pinned, not MLflow-registered: `data/fraud/models/xgb_mvm.ubj`
plus `platt_scaler.json` are the reproducible source of truth (MLflow holds loose run
artefacts). `verticals/fraud/serving/scorer.py` re-states the two-line margin→Platt map
rather than importing the trainer; `verticals/fraud/tests/test_serving.py` parity-checks
it against the offline pipeline. Data itself never enters git.

## Enforcement layer — hooks and protected files

`.claude/hooks/governance_guard.py` runs as a PreToolUse hook on every Bash/Edit/Write
call. It is deterministic and cannot be skipped or talked around.

**Denied outright (no exception path — do not ask):** `git push --force` in any form
(the CL-E1 incident guard), git history rewrites (`filter-branch` / `filter-repo`),
recursive force deletes (`rm -rf`, `Remove-Item -Recurse -Force`).

**Operator confirmation required (every touch, by design):** any edit or writing shell
command reaching `MANIFEST.yaml`, `EDGES.yaml`, `docs/governance/WS-E_INCIDENTS.md`,
`DECISIONS.md`, `docs/governance/RULINGS_RECORD*.md`,
`docs/governance/document-register.yaml`. Legitimate appends to these are normal
governed acts; the gate exists to make every touch deliberate, not to prevent them.
When the confirmation prompt fires, restate which governed act the edit serves before
proceeding.

Background subagent tasks are disabled project-wide
(`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` in `.claude/settings.json`). Sessions are
attended, single-arc. Do not suggest detached (`/bg`) sessions on this repo.

## Ceremonies (slash skills, user-invoked only)

- `/session-open` — boot ritual: clean-tree check, env check, live register
  regeneration, rehash sweep, queue readback, arc selection. Run before substantive
  work in every session.
- `/session-close` — regenerate manifest snapshot, update the queue section below,
  draft the arc summary in handover style.
- `/ledger-touch` — WS-E append with the sequence-hold check enforced.
- `/hash-verify` — SHA256 pinned-transfer verification (the only skill Claude may
  invoke unprompted).
- `/pr-prep` — pre-PR battery (diff-stat first) and house-style PR body draft.

Any session touching retrieval starts with the standing first act: the normal-shell
ONNX cache traversal check, before other work.

## Conventions that will bite you

- **Never commit to `main`.** Feature branch → PR → merge. Delete the local branch after
  merge and `git fetch --prune` (GitHub auto-deletes the remote head).
- **ADRs in `decisions/` are immutable once merged** — supersede with a new one, never
  edit. Deviations from a locked document need a DECISIONS.md entry *before* the code
  merges. Locked `.docx` files in `docs/governance/` change by decision record only.
- **Gate criteria live in `docs/build/BN_GATE.md`, never in BUILD_TRACKER.md.** The
  tracker links; it does not restate. Same rule for the CL ledger
  (`docs/governance/GOVERNANCE_REVIEW_CHANGELOG.md` is canonical for CL items).
- **`.gitattributes` forces LF** on `.py/.yaml/.md/dvc.lock/*.dvc` etc. because DVC hashes
  working-tree bytes and a CRLF checkout drifts `dvc.lock`. `.cmd/.bat/.ps1` stay CRLF.
- **Markdown structural checks are enforced** (`scripts/check_docs.py`): balanced bold and
  backtick spans, no dead repo-relative path references in backticks, LF endings. A path
  you cite in a governance doc must exist.
- Operator scripts default to **dry-run**; `--live` executes.
- Docstrings here carry decision history (which increment, which ruling, why the shape).
  Match that when adding modules — a comment explaining *why* the constraint exists is the
  house style, and several of them are the only record of an incident.
- Governance artefacts change by explicit full-file replacement or scripted writes, never
  through a markdown-aware editor that reformats on save. Prototype/experiment files are
  each their own file (v0a, v0b, …); no overwrites of prior versions.

## Working protocol (non-negotiable)

1. **Environment.** `conda activate arcaai` (Python 3.11) before any Python work. Every
   script in this repo assumes that environment; a bare system interpreter will resolve
   the wrong dependency set. If the env cannot be confirmed, stop and say so.
2. **One act at a time.** Propose a single command or edit, wait for approval, read the
   output before the next act. Verification precedes mutation: check state first
   (`git status`, `git diff --stat`, or read the file) before changing it, and after any
   act verify its effect before proceeding. **`git diff --stat` comes FIRST in any
   verification battery** — an empty diff after a supposed change means the change did
   not happen, whatever else is green; say so rather than assuming it landed.
3. **Corpus governance.** Never edit anything under `verticals/fraud/corpus/` outside a
   governed act. `verticals/fraud/corpus/MANIFEST.yaml` changes only as appended
   eligibility transitions in a new manifest version — DEC-0014 item 5 enforces this
   mechanically. Authored corpus documents are immutable once committed: a correction is a
   new entry with a new hash, never an edit. `verticals/fraud/corpus/EDGES.yaml` changes
   are versioned acts and carry a version note. **Authoring and listing are separate
   governed acts** — writing a corpus document and listing it in MANIFEST.yaml never
   happen in the same uncommanded flow; ask before each act, never chain them.
4. **Registers are append-only.** DEC, ADR, CL and WS-E numbers come from a
   REPO_MANIFEST regenerated **this session** — never guessed, never reused, never read
   from a stale snapshot. Sequence-hold rule (WS-E 58): next number is highest+1, only.
5. **Docs discipline.** Run `python scripts/check_docs.py .` before any push containing
   markdown. `scripts\lint.cmd` is narrower than CI's docs check; passing lint does not
   imply docs will pass.
6. **Hash-pinned transfers.** Any artefact crossing a machine or session boundary gets a
   SHA256, verified in full on arrival (`/hash-verify`). On mismatch: stop, do not open
   or act on the artefact.
7. **External AI panel.** Panel composition and primers are governed by
   `docs/governance/sme-panel.md` and `docs/governance/sme-prompt-primers/` — never
   enumerate members from memory (Mistral sits on the roster primarily for European
   regulation cross-checking). Every circulation records its ACTUAL composition in the
   circulation/rulings artefact: which members were fielded, any substitutions (and for
   whom), and any member unavailable (down, token-limited, etc.) with the reason. A
   panel outcome without its composition record is incomplete. Panel members act as
   interrogators, never authors; panel material leaves and returns hash-pinned; rulings
   are the operator's alone.

## Current queue

Maintained by `/session-close` at end of each session. Queue source of truth is the
latest committed session handover (plus addendum if any) under `docs/governance/`;
this section is a working pointer, not the record.

<!-- QUEUE-START -->
1. Boot ritual via /session-open (incl. rehash_sweep; expect 0 pins).
   **Expect 0 divergences.** The DEC-0015 divergence that stood by
   construction across the 10c and 11 arcs cleared at PR #86 when the ledger
   entry landed, and 0 has held since across PRs #88, #89, #90 and #91. There
   is no longer an expected divergence: **any** divergence is now a genuine
   stop. **Queue-maintenance note:** where items encode a ruled sequence their
   numbering follows that sequence and not priority, and an in-place reduction
   of one item must not silently invert two — which is how the ordering
   corrected at the 2026-08-11b arc went wrong. Meaning that lives in a slot
   rather than in the text is the general hazard.
2. **D2.2a pre-flight implementing artefact — now the live next step**, D2.1
   having discharged at PR #91. It is the residue of the parked
   elevated-session findings, most of which discharged at PR #88.
   Discharged: the ONNX cache ACL fault is repaired. The operator deleted the
   locked directory from their own elevated terminal; chromadb then re-extracted
   locally from the existing archive under the normal identity (archive size,
   mtime and SHA256 all unchanged, so no network fetch), and traversal plus a
   full model read now pass from a shell corroborated as non-elevated. Root
   cause, the false-green mechanism and the constraints they place on the
   artefact are recorded at
   `docs/governance/FINDINGS_2026-08-11_onnx-acl-root-cause.md`: the ACL fault
   and the elevated-harness-shell breach were **one incident, cause and
   effect**, not two findings. Still owed:
   - The pre-flight has **no implementing artefact**. It exists only as a named
     procedure in this file and in `.claude/skills/session-open/SKILL.md`, and
     has been run ad-hoc in every session that needed it. It arrives at D2.2a
     and claims the next free CL number there — next 26.
   - It must carry the three-state constraint: an assertion is GREEN, RED or
     **UNKNOWN**, and UNKNOWN exits non-zero and never renders as green. Every
     false green catalogued so far is an UNKNOWN rendered as a GREEN.
     Non-elevation is asserted first and, if it fails, the artefact refuses to
     report the remaining assertions at all rather than reporting them passing.
   - **Latent hazard, recorded not repaired.** The corpus index directory is
     still owned by `BUILTIN\Administrators` from the same elevated interlude,
     usable only through an inherited grant to authenticated users. Repair
     needs elevation and is therefore the operator's.
   - **Standing rule, permanent (operator, 2026-08-11): the harness never
     elevates.** Any fix requiring elevation is the operator's, at their own
     terminal, and the assertion it repairs is re-verified afterwards from a
     non-elevated shell.
3. **Corpus listing owed for SG-07, SG-08 and SG-09.** All three authored, none
   listed: listing in `verticals/fraud/corpus/MANIFEST.yaml` is a separate
   governed act and was deliberately not chained to any authoring arc. The
   corpus pin is unmoved and eligible remains 16. Debt has grown once per
   authoring arc for three consecutive arcs — worth deciding whether it clears
   in one act or per document. The ruled frame settles the interaction rather
   than leaving it open: commissioning runs pin the snapshot current at spike
   time and do **not** wait on this act, but Regime-2 formal runs use listed
   snapshots only.
4. **ci-docs paths-filter gap — decision owed; evidence now complete.**
   `ci-docs` cannot fire on corpus markdown: its `pull_request` paths are
   `docs/**`, `decisions/**`, `*.md`, `scripts/check_docs.py` and
   `.github/workflows/ci-docs.yml`, and `*.md` matches root-level files only.
   Fourth recurrence of that family (`docs/`, then `scripts/`, then `.claude/`,
   now corpus markdown). PR #74 carried the gap unnoticed; PR #80 evidenced it
   after the fact; PR #81 called it in the PR body before the run and confirmed
   it. **Second control case, PR #86 (2026-08-11), and it is the decisive one:**
   that PR changed a root-level `*.md` (`DECISIONS.md`) and a file under `docs/` in
   the same diff, and ci-docs fired on the `pull_request` event and passed in
   7s. Both covered path classes work in a single run, which isolates the defect
   conclusively to the root-only `*.md` glob failing to reach corpus markdown.
   Fix is one line; whether it also warrants a WS-E ledger entry or a CL item is
   an operator decision. PR #88 (2026-08-11) is a third confirming case for the
   covered classes — two files under `docs/`, ci-docs fired and passed in 7s —
   and adds nothing on corpus markdown, which no run can reach and so no run can
   evidence. **Push-event asymmetry diagnosed 2026-08-11c, and it is not a
   defect:** all three workflows carry `push: branches: [main]` with no paths
   filter at all, the paths list appearing only under `pull_request`. Every
   merge to main therefore runs all three regardless of content — evidenced both
   ways, a docs-only merge running ci-devops and ci-mlops, and PR #91's
   code-only merge running ci-docs in 10s. That is an unconditional post-merge
   sweep, and ci-devops' own header records it catching a repo-wide `ruff` I001
   failure that PR-time filtering had missed. The open verification parked on
   this in `docs/governance/SESSION_HANDOVER_2026-08-11.md` can be closed as
   diagnosed. It is a different thing from the corpus-markdown gap above, which
   is a PR-time defect.
5. **Lint invocation defects — two now, with opposite polarity.** Carried:
   `cmd /c scripts\lint.cmd` by relative path exits 1 ("system cannot find the
   path specified") while the same script by absolute path and a bare
   `ruff check .` both exit 0, cwd confirmed as the repo root. Undiagnosed,
   non-blocking; the absolute-path invocation is the working practice.
   **New 2026-08-11 and more dangerous:** invoking the absolute path via
   `cmd /c` *from the Bash tool* printed a cmd banner and exited **0 without
   running ruff at all** — a false green, where the carried defect is a false
   red. The absolute-path practice holds only under PowerShell. Exit code alone
   does not evidence that the check ran; the "All checks passed!" line does.
6. **Check-method defect family — six instances now, and a pattern-level
   decision is owed rather than six separate fixes.** The shape is constant: a
   check whose success message claims more than it verified, or an exit status
   evidencing neither success nor failure. Instances: the ONNX traversal check
   green under elevation (diagnosed and constrained at PR #88, item 2); both
   lint invocation defects at item 5; `scripts/corpus_edges_check.py` at item
   14; and two observed during the PR #88 arc and written up in §5 of
   `docs/governance/FINDINGS_2026-08-11_onnx-acl-root-cause.md` — a structured
   exception handler wrapped around a native command, which can never fire
   because native commands set an exit code rather than raising, and a git
   invocation piped into a first-item selector returning exit 255 while
   succeeding completely. The generalisation to rule on: **an exit code alone
   evidences nothing.** A check must assert on the substance of what it returns,
   must name the assertions it actually evaluated, and where it does rely on an
   exit code must invoke the command in a form that lets that code mean what it
   appears to mean. Bears directly on item 2 — the D2.2a pre-flight is the first
   artefact that would encode the rule. **Applied once already, at the D2.1 arc:**
   the spec schema first expressed forbidden fields as false subschemas, which
   reject correctly but report only that a value is disallowed without naming
   the field; a negative test caught it and the schema now uses `not`/`required`,
   which names what it rejected.
7. **Batch-2 panel circulation — unblocked; scope decision owed.** Ruled
   2026-08-10: circulation is a batch-level act at batch end, not a
   per-document precondition, and batch end has arrived (SG-03..SG-09 authored
   as of PR #81). Open: whether SG-03..SG-06 — authored under the batch-1
   rulings of 2026-08-06 — sit inside that circulation or are treated as
   already covered. Ruled into the pack as a stated condition: SG-09 lands as a
   leaf in the authored subgraph, its only design inbound being `DL-05` which is
   unauthored, so no authored document cites SG-09.
8. **Conventions owed in this file at its next revision — three, and they
   should be written once, together, rather than accreting.**
   - **Commit trailers.** No `Co-Authored-By` on corpus authoring commits
     (ruled). Practice now runs ahead of the rule on three axes: non-corpus
     commits, PR bodies, and now code. Ten instances, all asserted by trailer
     count 0 rather than by eyeball: `59fb216` (SG-08), `66041e5` (SG-09),
     `99b63cd` (TOR panel-pass artefacts), both commits of PR #86 (`cffafe0`,
     `7b07dbd`), both of PR #88 (`8cc66b8`, `a20a03b`), both of PR #90
     (`54360ac`, `e110b08`), and `d93760a` (PR #91, the D2.1 schema — the first
     code commit in the set). Ten instances is no longer practice running ahead
     of the rule; it is an unwritten rule, and writing it down is overdue.
   - **Register-number citation.** In any document under `docs/`, cite an
     unconsumed register number as "next N" or not at all, never as a bare "N":
     the manifest scanner cannot distinguish a bare number from a claim the item
     exists, and it produces a spurious divergence. Established by the PR #85
     correction note.
   - **DEC placement.** A DEC entry belongs in `DECISIONS.md`, never as a
     numbered file under `decisions/`. `scripts/repo_manifest.py` treats that
     filesystem as the ADR register and reads leading filename digits, so a
     DEC-numbered file there silently consumes ADR numbers; and because the DEC
     ledger is parsed from `DECISIONS.md` alone, it would not clear the very
     divergence it was written to clear. Caught live at the 2026-08-11 arc
     before mutation; recorded in the DEC-0015 entry, but it is a general hazard
     for every future DEC and belongs here too.
9. PRs #64/#65 standing tree verification — **partially chipped, not
   discharged.** EDGES v0.2.2 read in full during the SG-07 arc and the
   manifest-history job ran live on PR #74; the MANIFEST.yaml side of #64 and
   the rest of #65 are still owed a look. Untouched since.
10. Operator inclusion decision for TY-03..09 when ready (separate act; next
    ingest then populates processing fields at a .8 version).
11. CL-25 / inc4 (pin writer) pending agent module; CL-24 when convenient.
12. Governance-guard deny path for history rewrites (`filter-branch` /
    `filter-repo`) is the one documented category still unexercised; test needs
    a throwaway clone, not this working tree.
13. Consistency reads owed when their targets are drafted — SG-07 §2.2 (TR-05)
    and §5.2 (DL-06), both characterised by series role only per the SG-05
    precedent for CV-03 and DP-04; and SG-08 §2.3 (TR-03) and §5.2 (CV-05),
    where TR-03 was characterised from SG-04 §2.1's committed wording rather
    than bare series role and CV-05 by series role only. Unchanged by the SG-09
    arc, deliberately: all three of SG-09's minimum targets were already
    authored.
14. **`corpus_edges_check.py` design-mode false green — decision owed.** Run
    without `--docs`, it prints `OK: closure, asymmetry, immutability, and
    authored-doc checks pass` having read no authored document at all: `--docs`
    defaults to `None` and the authored-document loop never runs. A member of
    the check-method defect family now consolidated at item 6 — a check whose
    success message claims more than it verified. Minimum fix is wording, not
    logic, but see item 6 before fixing it in isolation.
15. **Statute-edge width — corpus-design fact for the circulation pack.** The
    corpus holds POCA s.327 (OGL-0003) and s.330 (OGL-0004) and no text of
    s.338, s.339A, MLR 2017 reg 28, or the tipping-off provisions — all of which
    s.327 depends on by reference. SG-09 §1.2 states the boundary on the face of
    the document rather than papering it, but the gap is a property of the
    corpus and will recur for any document reaching into the disclosure regime.
16. **TOR errata — carry to the Test Plan (D1.1) and any future TOR revision.**
    The TOR entered the repo at Rev C RULED (PR #83) and is immutable as
    committed, so both are recorded rather than amended, and both are stated in
    the PR #83 body.
    - §2 and §7 cite PR #80 for batch-2 completion; batch 2 completed at PR #81.
      The claim was wrong at the moment of writing, not merely stale — batch 2
      stood at 6/7 when Rev B was drafted and SG-09 did not yet exist.
    - §2's authored count should read **30 of 54** — the parenthetical
      enumeration (16 + TY-03..09 + SG-03..09) is the correct one. 23 belongs to
      the listing pipeline, not to authoring. The conflation propagated outward:
      Reviewer B's "23-document corpus" phrasing derives from it, making this a
      correction owed to the panel record and not only to the TOR.
17. **Gemini architecture-review return — consolidation owed.** Gemini's
    assessment of the orchestration / memory / dreaming document arrived in the
    same circulation as the TOR pass but reviews a different document; it is
    recorded as out of scope in the rulings record and forms no part of it. It
    stands as an unconsolidated two-reviewer return with Grok's. **Consolidate
    before the Agentic Topology ADR work opens** — ADR-0011 is the next free ADR
    number and that work would consume it. Note that ADR-0011 was nearly
    consumed by accident at the 2026-08-11 arc (item 8, DEC placement).
18. Housekeeping, non-blocking: 19 stale local branches from past arcs remain
    after their merges. The delete-after-merge convention has held for recent
    arcs; these predate it.
19. **Packaging declarations are unasserted — three findings, one family,
    surfaced at the D2.1 arc.**
    - `arcaai/harness/schema/scenario_spec_v0.1.schema.json` is **not** declared
      as package data. `arcaai.harness` now ships; the schema file it exists to
      carry does not. Harmless today because the test resolves it by path, and
      it bites the moment a runner loads the schema from an installed
      distribution — which is the D2.2a/D2.2b arc.
    - `arcaai.platform.retrieval` is still absent from `[tool.setuptools]
      packages`. Retrieval works only by grace of the editable install. Left
      untouched by ruling at the D2.1 arc, with the pyproject evidence carried
      here.
    - **Nothing in the repo asserts that list.** `tests/test_packaging.py` tests
      the agent packaging node, not setuptools — the name misleads, and that is
      how the retrieval omission survived unnoticed. A test over the packages
      list is the one fix that would have caught both findings above.
<!-- QUEUE-END -->

## Orientation for a new session

Run `/session-open` first. Then: `START_HERE.md` → `DECISIONS.md` (rulings R1–R13, DEC
series, ADRs) → `BUILD_TRACKER.md` (next unpassed gate) → the newest
`docs/governance/SESSION_HANDOVER_*.md`, whose boot line is the current state of play.
`CURRENT_STATE.md` and `SESSION_PROTOCOLS.md` both lag current practice — treat the
latest handover as authoritative where they disagree.
