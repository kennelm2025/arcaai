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
the `arcaai_audit_test` database, overridable via `ARCAAI_AUDIT_OWNER_DSN` /
`ARCAAI_AUDIT_APP_DSN`.

**Two audit databases, and the suite may only ever touch one of them** (DEC-0016).
`arcaai_audit` is the governed store — real audit events, real `corpus_version` pins, and
from D2.2a the Commissioning Session Records. `arcaai_audit_test` is disposable: the suite
drops and recreates its schema on every run, which is what made the previous single-database
arrangement destroy the governed store at the start of every battery (WS-E 65). A fail-closed
guard in `tests/governance/conftest.py` refuses the run unless the resolved DSN names the
test database, so an override pointing back at the governed store stops rather than erases.
Both databases are created by `infra/postgres-init/02-create-audit-databases.sql`, which
Postgres runs **only on a fresh `pgdata` volume** — an existing volume needs the one-off
`CREATE DATABASE` by hand, and that is an operator act at the operator's terminal, since the
harness never assumes the owner role.

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

Permissions run in three tiers, ruled 2026-08-11.
`docs/governance/HARNESS_PERMISSION_TIERS_2026-08-11.md` is **authoritative**; what
follows describes it and will drift first. Read the doc before relying on this summary,
and in particular before concluding that something is or is not gated.

**Tier 1 — auto-allow.** Read-only operations, the mandatory batteries, and git
navigation (checkout, switch, fetch, fast-forward-only pull). Auto-allow moves the gate
from before the act to the evidence after it: it removes prompts, never verification. The
batteries in "Working protocol" below are unchanged and remain mandatory. **Narrowed
2026-08-11 on evidence** — edits and git write verbs were withdrawn from Tier 1 when the
precedence test failed; see the tiers doc.

**Tier 2 — gated on every touch.** The six governed stores — `MANIFEST.yaml`,
`EDGES.yaml`, `docs/governance/WS-E_INCIDENTS.md`, `DECISIONS.md`,
`docs/governance/RULINGS_RECORD*.md`, `docs/governance/document-register.yaml` — plus
`pyproject.toml`, `.github/workflows/`, the permission and ceremony system itself
(`.claude/settings.json`, `.claude/hooks/`, `.claude/skills/`), and `decisions/`, which
is gated because `scripts/repo_manifest.py` reads register numbers off filenames there,
making any write to it register-consuming by mechanism. Gated by repository state rather
than by path: PR merge, branch deletion, and any git write while HEAD is main. Legitimate
touches are normal governed acts; the gate makes each one deliberate, not impossible.
When the prompt fires, restate which governed act the edit serves before proceeding.

**Tier 3 — operator rulings.** Arc selection, scope, merges, frame rulings, register
decisions. Not tool gates, and no mechanism grants them.

**Denied outright (no exception path — do not ask):** force push in any form (the CL-E1
incident guard), git history rewrites, recursive force deletes, and elevation — the
harness never elevates, and never assumes the database owner role. Any fix requiring
either is the operator's, at their own terminal, re-verified afterwards from a
non-elevated shell.

`.claude/hooks/governance_guard.py` enforces the denies and the Tier 2 asks, routed by
the PreToolUse matcher in `.claude/settings.json`. **Coverage is two-part and both parts
must name a tool:** the matcher routes the call, and the module's shell-tool set decides
whether the command is inspected. Either alone is a silent no-op — WS-E 64 records three
days in which the guard was wired to the Bash tool while PowerShell, this repo's primary
shell, went unguarded. Adding a shell tool means adding it in both places.

**A Tier 1 allow rule pre-empts a Tier 2 guard ask** — tested 2026-08-11, and the guard
loses. The two mechanisms are alternatives, not layers, so: **never grant in Tier 1
anything Tier 2 is relied on to gate.** An allow rule covering the same ground as a guard
ask is not belt-and-braces; it is the gate switched off silently. Whether a deny is
pre-empted the same way is untested and untestable safely, so never allow-list a command
family that carries a deny. Ceremony skills carry their own `allowed-tools` frontmatter,
which governs inside that ceremony — Tier 1 grants are not in force there.

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
- **No `Co-Authored-By` trailer on any commit in this repo**, and none in PR bodies.
  Ruled first for corpus authoring; practice then ran ahead of the rule across non-corpus
  commits, PR bodies and code for ten consecutive instances, which made it an unwritten
  rule rather than a habit. **Assert it against the full printed body, never against a
  recalled impression of it** (ruled 2026-08-12): print the complete message body with
  `git log -1 --format=%B`, and for a branch `git log main..HEAD --format=%B`, as
  in-session evidence, then assert absence case-insensitively and *anywhere in the body*,
  not only in the trailer block — and say in the success line which bodies were read.
  Two methods are specifically excluded, both found during CL-24 commit verification.
  `%(trailers)` parses only the final paragraph, so a `Co-Authored-By` line sitting
  mid-message expands to nothing and the check reports zero while the line is plainly
  visible in the text. And a count piped through a fallback — `grep -c … || true` inside
  a substitution — renders clean-absence and check-never-ran identically, because `grep`
  exits non-zero on no match and the fallback swallows it into an empty string. A check
  whose green is indistinguishable from its not having run is the check-method family
  (queue item 9), and it is worse here for appearing in the very command written to
  verify a house rule.
- **Cite an unconsumed register number as "next N", never as a bare "N"** in any document
  under `docs/`. `scripts/repo_manifest.py` cannot distinguish a bare number from a claim
  that the item exists, and reports a spurious divergence. Established by the PR #85
  correction note.
- **A DEC entry belongs in `DECISIONS.md`, never as a numbered file under `decisions/`.**
  That filesystem is the ADR register — the manifest scanner reads leading filename
  digits — so a DEC-numbered file there silently consumes ADR numbers; and because the
  DEC ledger is parsed from `DECISIONS.md` alone, such a file would not clear the very
  divergence it was written to clear. Gated mechanically since 2026-08-11, because the
  one near miss was caught by the working protocol and not by any control (WS-E 64).
- **Commit via a message file**, never an inline message string. House commit messages
  carry the reasoning and the verification battery, and inline quoting mangles multi-line
  text on Windows.
- **Every test cycle closes with a governed reporting artefact** (operator ruling,
  2026-08-11), and is not complete until the operator rules on the cycle outcome. Regime 2
  formal execution produces a TEST REPORT, specified in the Test Plan (D1.1). Regime 1
  commissioning produces a COMMISSIONING SESSION RECORD — deliberately not called a report
  and carrying no pass/fail summary, because commissioning results are permanently
  inadmissible and a report format would invite promotion by osmosis. Full text of the
  ruling lives in the handover of record.

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
1. **Boot ritual via /session-open** — STANDING. Divergences expect 0, a
   plain stop with no carve-out. **The rehash sweep now expects RED**
   until item 2 lands: exactly two `fixture-*` rows, replaced rather
   than accumulated at every governance-suite run, classified 2026-08-11
   as genuine mechanism and cause assigned to CL-24. A red sweep is no
   longer a stop; a red sweep showing anything other than two
   fixture-labelled rows is. Detail:
   `docs/governance/SESSION_HANDOVER_2026-08-11c.md` boot line and the
   2026-08-11d handover when authored.
   Sequencing note: where items encode a ruled sequence the numbering
   follows that sequence and not priority, and an in-place reduction of
   one item must not silently invert two —
   `docs/governance/SESSION_HANDOVER_2026-08-11b.md`, "Corrections
   landed this arc".
2. **CL-24, test-database isolation — LIVE next arc**, promoted
   2026-08-11 to owed-before-D2.2a. Scope as ruled: the separability
   design decision (test writes and governed writes distinguishable on
   sight, by database, schema or excluded-by-rule marker), the
   write-path guard, the residue cleanup as an operator-commanded
   owner-role act, and the sweep reporting excluded-by-rule state as a
   named category rather than as silence. **Scope enlarged at the
   2026-08-11d close by item 3, which is the same problem's sharper
   face.** Detail: `docs/governance/WS-E_INCIDENTS.md` item 61.
3. **The governance suite destroys the live audit store — NEW
   2026-08-11d, WS-E entry owed, next 65.** `tests/governance/conftest.py`
   runs `drop_all` then `create_all` against the dev `arcaai_audit`
   database as `arcaai_owner` at the start of every session, so every
   `scripts\test.cmd` run erases every audit event and corpus-version
   row present. This corrects WS-E 61's recorded mechanism, which reads
   as a failure to clean up afterwards: the suite destroys beforehand.
   The append-only property holds for the app role and is defeated at
   the owner role by the repository's own mandatory battery. Bears
   directly on D2.2a, whose Commissioning Session Records would be
   written into that store and erased by the next battery run.
4. **D2.2a pre-flight implementing artefact** — sequenced after item 2,
   not before it. Claims the next free CL number. Detail:
   `docs/governance/SESSION_HANDOVER_2026-08-11c.md` open verification 4
   and `docs/governance/FINDINGS_2026-08-11_onnx-acl-root-cause.md`.
   Reporting rule inherited: the spike closes with a Commissioning
   Session Record, not a report (operator ruling 2026-08-11).
5. **Permission-tiering follow-through — precedence RESOLVED against
   the design; three parts still open.** Tested 2026-08-11: a Tier 1
   allow rule pre-empts a Tier 2 guard ask, so the two are alternatives
   and not layers. Tier 1 narrowed the same day to read-only, batteries
   and git navigation. Open: (a) restoring edits and git writes to
   Tier 1 needs an enumeration of paths provably containing no
   protected path, which `docs/` and `verticals/` both defeat
   wholesale; (b) whether a deny is pre-empted the same way is untested
   and has no safe probe, so no command family carrying a deny may be
   allow-listed; (c) the rule strings themselves, and hook routing of
   skill and subagent calls, remain unverified. Detail:
   `docs/governance/HARNESS_PERMISSION_TIERS_2026-08-11.md`.
6. **Corpus listing owed for SG-07, SG-08 and SG-09** — OPEN;
   operator's decision whether it clears in one act or per document.
   Detail: `docs/governance/SESSION_HANDOVER_2026-08-11c.md` open
   verification 7 and
   `docs/governance/RULINGS_RECORD_2026-08-10_TOR-test-capability.md`
   amendment 9.
7. **ci-docs paths-filter gap on corpus markdown** — DECISION OWED; the
   fix is one line. Detail:
   `docs/governance/SESSION_HANDOVER_2026-08-11.md`. Push-event
   asymmetry closed as diagnosed at
   `docs/governance/SESSION_HANDOVER_2026-08-11c.md` open verification 5.
8. **Lint invocation defects, two of opposite polarity** — CARRIED,
   non-blocking. Detail:
   `docs/governance/SESSION_HANDOVER_2026-08-11.md`.
9. **Check-method defect family — PATTERN-LEVEL RULING OWED**, and the
   2026-08-11d arc added three instances: the guard whose stated
   coverage was a claim about its patterns rather than its wiring
   (WS-E 64); `Measure-Object -Line`, which counts non-blank lines while
   reading as a line count and is the prescribed `wc -l` equivalent; and
   the queue-block byte-versus-character measurement. Detail:
   `docs/governance/FINDINGS_2026-08-11_onnx-acl-root-cause.md` §5 and
   `docs/governance/SESSION_HANDOVER_2026-08-11b.md` open verification 3.
10. **Batch-2 panel circulation** — UNBLOCKED; scope decision owed on
    whether SG-03..SG-06 sit inside it. Detail:
    `docs/governance/RULINGS_RECORD_2026-08-10_TOR-test-capability.md`.
11. **Ceremony frontmatter harmonisation** — the residue of the
    conventions item, which discharged at PR #94. All five skills under
    `.claude/skills/` carry Bash-only `allowed-tools`, so Tier 1 grants
    are not in force inside a ceremony. Narrows rather than widens, so
    friction not exposure. Detail:
    `docs/governance/HARNESS_PERMISSION_TIERS_2026-08-11.md`,
    enforcement coverage.
12. **PRs #64/#65 standing tree verification** — PARTIALLY CHIPPED.
    Detail: `docs/governance/SESSION_HANDOVER_2026-08-08b.md`.
13. **Operator inclusion decision for TY-03..09** — OPEN, when ready.
    Detail: `docs/governance/SESSION_HANDOVER_2026-08-11c.md` return
    queue 10.
14. **CL-25 / inc4 pin writer** pending the agent module — OPEN. Detail:
    `docs/governance/WS-E_INCIDENTS.md` item 61.
15. **Governance-guard deny path for history rewrites** — UNEXERCISED;
    needs a throwaway clone. Detail:
    `docs/governance/SESSION_HANDOVER_2026-08-08.md`.
16. **Consistency reads owed when their targets are drafted** — SG-07
    §2.2 and §5.2, SG-08 §2.3 and §5.2 — CARRIED. Detail:
    `docs/governance/SESSION_HANDOVER_2026-08-08b.md`.
17. **`corpus_edges_check.py` design-mode false green** — DECISION OWED;
    wording, not logic, but see item 9 first. Detail:
    `docs/governance/SESSION_HANDOVER_2026-08-10c.md`.
18. **Statute-edge width** — CORPUS-DESIGN FACT for the circulation
    pack. Detail: `docs/governance/SESSION_HANDOVER_2026-08-11b.md`
    return queue 16.
19. **TOR errata** — CARRIED to the Test Plan (D1.1). Detail:
    `docs/governance/SESSION_HANDOVER_2026-08-10c.md` and the PR #83
    body.
    Reporting rule inherited: D1.1 specifies the Regime-2 Test Report
    (operator ruling 2026-08-11).
20. **Gemini architecture-review return** — CONSOLIDATION OWED before
    the Agentic Topology ADR work opens. Detail:
    `docs/governance/RULINGS_RECORD_2026-08-10_TOR-test-capability.md`.
21. **Stale local branches from past arcs** — HOUSEKEEPING,
    non-blocking. Detail:
    `docs/governance/SESSION_HANDOVER_2026-08-08.md`.
22. **Packaging declarations are unasserted** — OPEN; three findings,
    one family. Detail:
    `docs/governance/SESSION_HANDOVER_2026-08-11c.md` open verifications
    2 and 3.
<!-- QUEUE-END -->

## Orientation for a new session

Run `/session-open` first. Then: `START_HERE.md` → `DECISIONS.md` (rulings R1–R13, DEC
series, ADRs) → `BUILD_TRACKER.md` (next unpassed gate) → the newest
`docs/governance/SESSION_HANDOVER_*.md`, whose boot line is the current state of play.
`CURRENT_STATE.md` and `SESSION_PROTOCOLS.md` both lag current practice — treat the
latest handover as authoritative where they disagree.
