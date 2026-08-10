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
2. **Parked elevated-session findings — blocking for retrieval.**
   - ONNX cache ACL fault, confirmed live. Repair before any `--live` retrieval
     act; a stub-flag run is unaffected.
   - Elevated-harness-shell breach, recorded.
   - The ONNX cache traversal check returns green under an elevated shell — a
     false-green defect. Its result is not to be trusted as the standing first
     act until it asserts non-elevation. **Restated 2026-08-10: this is an
     authoring job, not a fix.** The check has no implementing artefact — it
     exists only as a named procedure in this file and in
     `.claude/skills/session-open/SKILL.md`, with no script behind it, so there
     is nothing to add the assertion to. Operator decision owed on whether it
     warrants a CL.
3. **Batch-2 authoring — COMPLETE at 7/7.** SG-03/SG-04 (PR #67), SG-05/SG-06
   (PR #68, AO-2 discharged in SG-05), SG-07 (PR #74), SG-08 (PR #80), SG-09
   (PR #81, 2026-08-10). No SG authoring remains; the downstream acts are the
   listing at item 4 and the circulation at item 6.
4. **Corpus listing owed for SG-07, SG-08 and SG-09.** All three are authored
   and none is listed: listing in `verticals/fraud/corpus/MANIFEST.yaml` is a
   separate governed act and was deliberately not chained to any of the three
   authoring arcs. The corpus pin is unmoved and eligible remains 16 until it
   happens. The debt has now grown once per authoring arc for three consecutive
   arcs — worth deciding whether it clears in one act or per document.
5. **ci-docs paths-filter gap — decision owed.** `ci-docs` cannot fire on corpus
   markdown: its `pull_request` paths are `docs/**`, `decisions/**`, `*.md`,
   `scripts/check_docs.py` and `.github/workflows/ci-docs.yml`, and `*.md`
   matches root-level files only. Structural checks on corpus documents
   therefore run post-merge or not at all on a PR — the condition WS-E 45
   created ci-docs to abolish. Fourth recurrence of that family (`docs/`, then
   `scripts/`, then `.claude/`, now corpus markdown). **Evidence is now as
   complete as it will get: three instances, the third predicted in advance.**
   PR #74 carried the gap unnoticed; PR #80 evidenced it after the fact; PR #81
   was called in the PR body before the run and confirmed — ci-docs did not fire
   on the PR and ran green post-merge on main. `gh run list` shows the only
   ci-docs runs for both corpus PRs are `push` events on main, never
   `pull_request`. The 2026-08-08b handover's statement that both workflows
   cover a corpus document is wrong as to ci-docs. Fix is one line; whether it
   also warrants WS-E 64 or CL-26 is an operator decision.
   Carried alongside it: a lint false-red observed 2026-08-10 — `cmd /c
   scripts\lint.cmd` by relative path exits 1 ("system cannot find the path
   specified") while the same script by absolute path and a bare `ruff check .`
   both exit 0, cwd confirmed as the repo root. Undiagnosed, non-blocking.
6. **Batch-2 panel circulation — now unblocked; scope decision owed.** Ruled
   2026-08-10: circulation is not a per-document precondition for batch-2
   authoring, on the evidence of the SG-05/SG-06 and SG-07 arcs. It is a
   batch-level act at batch end, and batch end has arrived — all of
   SG-03..SG-09 is authored as of PR #81. Open: whether SG-03..SG-06 — authored
   under the batch-1 rulings of 2026-08-06 — sit inside that circulation or are
   treated as already covered. Ruled into the pack as a stated condition: SG-09
   lands as a **leaf in the authored subgraph** — its only design inbound is
   `DL-05: [SG-09, SG-06]` and DL-05 is unauthored, so no authored document
   cites SG-09. Not a check failure (closure runs against the design file, not
   prose), but it is the condition the v0.2.1 closure repair exists to prevent
   at design level.
7. PRs #64/#65 standing tree verification — **partially chipped, not
   discharged.** EDGES v0.2.2 was read in full during the SG-07 arc and the
   manifest-history job ran live on PR #74; the MANIFEST.yaml side of #64 and
   the rest of #65 are still owed a look. Untouched by the SG-08 and SG-09 arcs.
8. Operator inclusion decision for TY-03..09 when ready (separate act; next ingest
   then populates processing fields at a .8 version).
9. CL-25 / inc4 (pin writer) pending agent module; CL-24 when convenient.
10. Governance-guard deny path for history rewrites (`filter-branch` / `filter-repo`)
    is the one documented category still unexercised; test needs a throwaway clone,
    not this working tree.
11. Consistency reads owed when their targets are drafted — SG-07 §2.2 (TR-05)
    and §5.2 (DL-06), both characterised by series role only per the SG-05
    precedent for CV-03 and DP-04; and SG-08 §2.3 (TR-03) and §5.2 (CV-05),
    where TR-03 was characterised from SG-04 §2.1's committed wording rather
    than bare series role and CV-05 by series role only. **Unchanged by the
    SG-09 arc, and deliberately so:** all three of SG-09's minimum targets
    (DP-01, SG-06, OGL-0003) were already authored, so every citation landed by
    pinpoint and the ruled-in extra (TY-04) was read in full before drafting to
    keep it that way. SG-09 is the first batch-2 document to add nothing here.
12. Commit-trailer convention — ruled: no `Co-Authored-By` trailer on corpus
    authoring commits. Owed as a standing rule in this file at its next revision.
    Two corpus-authoring instances now: `59fb216` (SG-08) and `66041e5` (SG-09),
    both asserted by trailer count 0 rather than by eyeball. Open for that
    revision: whether the rule extends to PR bodies — the generated-with footer
    was omitted from PR #80 and again from PR #81 on the ruling's spirit, but
    its terms reach commit trailers only, so the practice is now two instances
    ahead of the rule.
13. **`corpus_edges_check.py` design-mode false green — decision owed.** Run
    without `--docs`, it prints `OK: closure, asymmetry, immutability, and
    authored-doc checks pass` having read no authored document at all: `--docs`
    defaults to `None` and the authored-document loop never runs. Observed live
    during the SG-09 arc — a bare run reported that line, and the docs-mode
    re-run was what actually evidenced SG-09. Same false-green shape as the ONNX
    cache traversal check at item 2: a check whose success message claims more
    than it verified. Whether it warrants a CL is an operator decision; the
    minimum fix is wording, not logic.
14. **Statute-edge width — corpus-design fact for the circulation pack.** The
    corpus holds POCA s.327 (OGL-0003) and s.330 (OGL-0004) and no text of
    s.338, s.339A, MLR 2017 reg 28, or the tipping-off provisions — all of which
    s.327 depends on by reference. SG-09 §1.2 states the boundary on the face of
    the document rather than papering it, per the operator ruling and the SG-08
    §1.2 pattern, but the underlying gap is a property of the corpus rather than
    of SG-09 and will recur for any document reaching into the disclosure
    regime.
<!-- QUEUE-END -->

## Orientation for a new session

Run `/session-open` first. Then: `START_HERE.md` → `DECISIONS.md` (rulings R1–R13, DEC
series, ADRs) → `BUILD_TRACKER.md` (next unpassed gate) → the newest
`docs/governance/SESSION_HANDOVER_*.md`, whose boot line is the current state of play.
`CURRENT_STATE.md` and `SESSION_PROTOCOLS.md` both lag current practice — treat the
latest handover as authoritative where they disagree.
