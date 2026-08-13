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
  in-session evidence, then assert against that full printed body that **no line asserts
  co-authorship**. An attribution line is the token at line start, a colon, and a name or
  address; prose mentioning the token — this bullet, or a commit message discussing the
  rule — is not attribution. Case-insensitive, and anywhere in the body rather than only
  in the trailer block. Say in the success line which bodies were read.
  Two methods are specifically excluded, both found during CL-24 commit verification.
  `%(trailers)` parses only the final paragraph, so a `Co-Authored-By` line sitting
  mid-message expands to nothing and the check reports zero while the line is plainly
  visible in the text. And a count piped through a fallback — `grep -c … || true` inside
  a substitution — renders clean-absence and check-never-ran identically, because `grep`
  exits non-zero on no match and the fallback swallows it into an empty string. A check
  whose green is indistinguishable from its not having run is the check-method family
  (queue item 8), and it is worse here for appearing in the very command written to
  verify a house rule.
- **The harness never bare-`cd`s in a persistent shell.** Commands address files by
  absolute path, or wrap a directory change in `Push-Location` / `Pop-Location` with a
  guaranteed restore. A persisted working directory is ambient state that outlives the
  command that set it, and on 2026-08-12 a single `cd .claude` broke the governance
  hook's relative invocation path and deadlocked every tool fail-closed (WS-E 68).
- **A hook or permission change is verified by re-reading the loaded file AND a
  deny-shaped probe** — never by the editor's word, and never by a command that would
  have been allowed anyway. The probe must return the guard's own refusal text verbatim;
  a refusal arising from a broken invocation is indistinguishable from a genuine denial
  at the blocked level, and an allow-shaped probe cannot tell a live guard from a dead
  one at all. Pair it with one allow-shaped call to prove the guard discriminates rather
  than merely blocks. Apply config fixes by shell string-replace with the read-back
  appended to the same act: an editor can report a save while a stale buffer is what
  lands, which is what defeated two successive fixes (WS-E 68).
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
   plain stop with no carve-out. **The rehash sweep now expects GREEN,
   exit 0, with no carve-out of any kind** — CARVE-OUT RETIRED
   2026-08-12 when the residue cleanup at item 2 landed. Expect
   `category irreproducible-pin : 0`, `category excluded-by-rule
   (test) : 0` and "all pins verified". **Any red is a plain stop.**
   The two `fixture-*` rows the previous carve-out tolerated are gone,
   and there is no longer a shape of red that is acceptable. Detail:
   `DECISIONS.md` DEC-0016, `docs/governance/WS-E_INCIDENTS.md` item 65
   and `docs/governance/CL-24_governed-store-baseline_2026-08-12.md`.
   Sequencing note: where items encode a ruled sequence the numbering
   follows that sequence and not priority, and an in-place reduction of
   one item must not silently invert two —
   `docs/governance/SESSION_HANDOVER_2026-08-11b.md`, "Corrections
   landed this arc".
2. **CL-24 — DISCHARGED IN FULL 2026-08-12. CLOSED.** Parts (a), (b)
   and (d) discharged at PR #96 under DEC-0016. Part (c), residue
   cleanup, discharged as an owner-role act at the operator's terminal:
   identity-scoped deletes in FK order (`audit_event`,
   `audit_run_terminal`, `audit_run`, then `corpus_version`) — **14 /
   18 / 18 / 2** rows, each delete asserting its own count inside one
   transaction, no `TRUNCATE` and no unqualified `DELETE`.
   **Figure correction:** this item previously read "2 / 18 / 14 / 18"
   against that same table order, transposing the first and last
   values; the baseline file and the live store both showed
   `audit_event` 14 and `corpus_version` 2. Corrected here rather than
   silently, because the wrong pair would have had a reader expect 18
   `corpus_version` rows and find 2.
   **Scope widened during the act, on evidence:** `audit_payload` held
   3 test-written rows visible to neither the baseline instrument nor
   the sweep; ruled in and cleared, so 5 tables were emptied, not 4.
   Verification, non-elevated as `arcaai_app`: sweep GREEN at exit 0
   with both categories 0; five-table count 0/0/0/0/0; AFTER-CLEANUP
   identity digest `e3b0c442…`, the SHA256 of the empty string.
   Item 1's carve-out retired in the same act. Instrument extension
   carried at item 28. Detail: `DECISIONS.md` DEC-0016,
   `docs/governance/GOVERNANCE_REVIEW_CHANGELOG.md` CL-24, and
   `docs/governance/CL-24_governed-store-baseline_2026-08-12.md`.
3. **D2.2a pre-flight implementing artefact — DISCHARGED at PR #104
   (`b1fc7f3`), CL-26. CLOSED.** `scripts/d22a_preflight.py` asserts the
   four D2.0 entry-criteria assertions as one standalone invocable
   script: non-elevation first and gating, cache traversal by read
   rather than existence, services including the vector store's
   exists/readable/writable triple, and conda environment identity.
   Three outcomes throughout; UNKNOWN and SKIPPED both exit non-zero
   and never collapse into green. Verified post-merge from `main` at
   4/4 GREEN, exit 0. The prose-only authoring debt, which carried no
   non-elevation assertion at all, is discharged. **Entry-criteria
   note, because a green now exists to point at:** pre-flight green is
   ONE of four D2.0 entry criteria; the other three are run-record
   obligations — corpus snapshot pinned and stated, scenario spec
   schema-valid against v0.1, working tree state recorded. A green
   pre-flight alone does not satisfy entry. Residue at item 29.
   Historical: its blocker, item 2, discharged at PR #102
   (`545075b`); the governed store is empty and the sweep green with no
   carve-out, so Commissioning Session Records can now be written into
   `arcaai_audit` without the next battery erasing them — which was the
   dependency that made item 2 owed before this spike. Holds right of
   way under DEC-0017 as a build artefact. Claims the next free CL
   number, read live at the arc that opens it and not before. **Not
   opened 2026-08-12:** ruled deliberately unstarted with 40 minutes
   left, on the grounds that the arc could not be opened and closed
   cleanly in the time and a half-written ceremony is worse than an
   unstarted one. A read-only session brief was prepared instead.
   Detail:
   `docs/governance/SESSION_HANDOVER_2026-08-11c.md` open verification 4
   and `docs/governance/FINDINGS_2026-08-11_onnx-acl-root-cause.md`.
   Reporting rule inherited: the spike closes with a Commissioning
   Session Record, not a report (operator ruling 2026-08-11).
4. **Permission-tiering follow-through — precedence RESOLVED against
   the design; three parts still open.** Tested 2026-08-11: a Tier 1
   allow rule pre-empts a Tier 2 guard ask, so the two are alternatives
   and not layers. Tier 1 narrowed the same day to read-only, batteries
   and git navigation. Open: (a) restoring edits and git writes to
   Tier 1 needs an enumeration of paths provably containing no
   protected path, which `docs/` and `verticals/` both defeat
   wholesale; (b) whether a deny is pre-empted the same way is untested
   and has no safe probe, so no command family carrying a deny may be
   allow-listed; (c) the rule strings themselves, and hook routing of
   skill and subagent calls, remain unverified — NARROWED 2026-08-12:
   hook routing for the PowerShell tool is now positively evidenced, a
   deny-shaped probe having returned the guard's own refusal text and
   an allow-shaped probe having succeeded, repeatedly and across
   changes to both the invocation and the guard's own code. Skill and
   subagent routing remain unprobed, as do the rule strings. Detail:
   `docs/governance/HARNESS_PERMISSION_TIERS_2026-08-11.md` and
   `docs/governance/WS-E_INCIDENTS.md` item 68.
5. **Corpus listing owed for SG-07, SG-08 and SG-09** — OPEN;
   operator's decision whether it clears in one act or per document.
   Detail: `docs/governance/SESSION_HANDOVER_2026-08-11c.md` open
   verification 7 and
   `docs/governance/RULINGS_RECORD_2026-08-10_TOR-test-capability.md`
   amendment 9.
6. **ci-docs paths-filter gap on corpus markdown** — DECISION OWED; the
   fix is one line. Detail:
   `docs/governance/SESSION_HANDOVER_2026-08-11.md`. Push-event
   asymmetry closed as diagnosed at
   `docs/governance/SESSION_HANDOVER_2026-08-11c.md` open verification 5.
   Note 2026-08-12: the sibling gap in `ci-devops` closed at PR #96,
   which added a recursive `infra/` entry after the same family bit a
   fourth time. This item is the corpus-markdown one and remains open.
7. **Lint invocation defects, two of opposite polarity** — CARRIED,
   non-blocking. Detail:
   `docs/governance/SESSION_HANDOVER_2026-08-11.md`.
8. **Check-method defect family — PATTERN-LEVEL RULING OWED**, now the
   most-instanced open item in this queue. The 2026-08-11d arc added
   three: the guard whose stated coverage was a claim about its patterns
   rather than its wiring (WS-E 64); `Measure-Object -Line`, which
   counts non-blank lines while reading as a line count and is the
   prescribed `wc -l` equivalent; and the queue-block
   byte-versus-character measurement. The 2026-08-12 arc added three
   more: the `ci-devops` paths filter, whose coverage was a claim about
   what was remembered as added rather than about what it names;
   `%(trailers)`, which parses only the final paragraph so a
   mid-message line counts as zero while plainly visible; and
   `grep -c … || true` inside a substitution, which renders
   clean-absence and check-never-ran identically. The last two were
   found in commands written to verify a house rule, and the trailer
   convention in "Conventions that will bite you" was amended twice on
   2026-08-12 as a result. The pack-install arc of 2026-08-12 added two
   further instances and one counter-example. Instances: the
   reported-done-not-done class at its fourth and fifth appearances,
   twice in one session, a configuration fix reported applied while the
   loaded file was unchanged; and `.claude/` CI coverage, where two
   passing checks may not have covered the changed files at all, now
   carried separately at item 24. Counter-example worth keeping,
   because this item has accumulated failures and no method: the guard
   was certified only by a DENY-shaped probe returning its own refusal
   text verbatim, paired with an ALLOW-shaped probe. A dead hook and a
   working hook are indistinguishable from any command that was going
   to be allowed anyway, so the allow-shaped probe alone would have
   passed a dead guard silently three times over. That pairing is the
   first positive discriminator this family has produced and is a
   candidate for the pattern-level ruling. Detail:
   `docs/governance/FINDINGS_2026-08-11_onnx-acl-root-cause.md` §5,
   `docs/governance/SESSION_HANDOVER_2026-08-11b.md` open verification 3,
   and `docs/governance/WS-E_INCIDENTS.md` item 68.
9. **Batch-2 panel circulation** — UNBLOCKED; scope decision owed on
   whether SG-03..SG-06 sit inside it. Detail:
   `docs/governance/RULINGS_RECORD_2026-08-10_TOR-test-capability.md`.
10. **Ceremony frontmatter harmonisation** — the residue of the
    conventions item, which discharged at PR #94. The five ceremony
    skills under `.claude/skills/` carry Bash-only `allowed-tools`, so
    Tier 1 grants are not in force inside a ceremony. WIDENED
    2026-08-12: PR #98 added three reference skills (`check-method`,
    `commit-hygiene`, `harness-discipline`), taking the directory to
    eight. The three new ones declare no `allowed-tools` at all, which
    is a different shape from the five and unassessed — whether an
    absent declaration inherits, denies or is simply inert has not been
    established, and the count in this item should not be read as
    covering them. Narrows rather than widens, so
    friction not exposure. Detail:
    `docs/governance/HARNESS_PERMISSION_TIERS_2026-08-11.md`,
    enforcement coverage.
11. **PRs #64/#65 standing tree verification** — PARTIALLY CHIPPED.
    Detail: `docs/governance/SESSION_HANDOVER_2026-08-08b.md`.
12. **Operator inclusion decision for TY-03..09** — OPEN, when ready.
    Detail: `docs/governance/SESSION_HANDOVER_2026-08-11c.md` return
    queue 10.
13. **CL-25 / inc4 pin writer** pending the agent module — OPEN, and
    sharper since 2026-08-12: WS-E 65 recorded that no harm has yet come
    of the audit store being destroyed only because nothing of record
    has ever been in it, every row having been written by its own tests.
    That is an accident of sequencing, not a control, and it expires the
    moment this item lands. Detail:
    `docs/governance/WS-E_INCIDENTS.md` item 61.
14. **Governance-guard deny path for history rewrites** — UNEXERCISED;
    needs a throwaway clone. Detail:
    `docs/governance/SESSION_HANDOVER_2026-08-08.md`.
15. **Consistency reads owed when their targets are drafted** — SG-07
    §2.2 and §5.2, SG-08 §2.3 and §5.2 — CARRIED. Detail:
    `docs/governance/SESSION_HANDOVER_2026-08-08b.md`.
16. **`corpus_edges_check.py` design-mode false green** — DECISION OWED;
    wording, not logic, but see item 8 first. Detail:
    `docs/governance/SESSION_HANDOVER_2026-08-10c.md`.
17. **Statute-edge width** — CORPUS-DESIGN FACT for the circulation
    pack. Detail: `docs/governance/SESSION_HANDOVER_2026-08-11b.md`
    return queue 16.
18. **TOR errata** — CARRIED to the Test Plan (D1.1). Detail:
    `docs/governance/SESSION_HANDOVER_2026-08-10c.md` and the PR #83
    body.
    Reporting rule inherited: D1.1 specifies the Regime-2 Test Report
    (operator ruling 2026-08-11).
19. **Gemini architecture-review return** — CONSOLIDATION OWED before
    the Agentic Topology ADR work opens. Detail:
    `docs/governance/RULINGS_RECORD_2026-08-10_TOR-test-capability.md`.
20. **Packaging declarations are unasserted** — OPEN; three findings,
    one family. Detail:
    `docs/governance/SESSION_HANDOVER_2026-08-11c.md` open verifications
    2 and 3.
21. **`.sql` is ungoverned in `.gitattributes`** — NEW 2026-08-12,
    DECISION OWED, one line. The file sets `* text=auto` and then names
    `.py .yaml .md .txt .sh`, the DVC metadata and the CRLF-keeping
    Windows scripts; `.sql` appears nowhere, so
    `infra/postgres-init/02-create-audit-databases.sql` and
    `sql/governance_grants.sql` check out CRLF on Windows. `psql` treats
    `\r` as whitespace and the `DO $$` blocks are unaffected, so this is
    latent rather than breaking. Fixing it means the one-line addition
    plus a re-normalisation of two files. Detail: PR #96 body, "Known
    and not addressed here".
22. **Mobile Ruling Protocol pilot review** — NEW 2026-08-12, ADOPTED
    AS PILOT at PR #98, not a permanent rule. The review clause fires
    after the first **five** mobile rulings have been made and
    transcribed; until it returns, no document may cite the protocol
    as settled practice. The review is the operator's and its outcome
    is a decision entry. Counter starts at zero: no mobile ruling has
    yet been made through the issue template. Detail:
    `docs/governance/ruling-briefs/README.md`.
23. **DEC-0017 build-first right of way is now STANDING and binds arc
    selection** — NEW 2026-08-12. Every session merges, or materially
    advances toward merge, at least one build-queue artefact before any
    governance refinement item is taken up; the exception is narrow
    (*directly blocks* a merge) and carries an evidential obligation,
    the blocking relationship being stated in the session record. Binds
    at the arc-selection step of `/session-open` and is discharged or
    excepted at `/session-close`. Note against this queue: items 1, 2
    and 3 are the near-term build lane; most of the remainder are
    refinement and now yield to them. Detail: `DECISIONS.md` DEC-0017.
24. **`.claude/` CI paths-filter coverage — SETTLED 2026-08-12, and
    the concern was DISCONFIRMED.** `.github/workflows/ci-devops.yml`
    line 33 names a recursive `.claude/` entry explicitly, and has
    since `402e698`
    ("Close the CI paths-filter gap: WS-E 62"). The `lint-test` pass on
    PR #98 was therefore genuinely triggered by, and did cover, the
    `.claude/` changes; that green meant what it appeared to mean.
    Recorded rather than deleted because the item was raised as a
    suspected false green and the check that settled it is the same
    read that found item 25 — a disconfirmed suspicion is evidence, and
    a queue that only records confirmed defects teaches the wrong
    lesson about which checks were worth running.
25. **`scripts/check_docs.py` does not scan `.claude/`** — NEW
    2026-08-12, FINDING RECORDED, fix is a future session's work. The
    script's scope is `ROOTS = ("docs", "decisions")` plus a root-level
    `*.md` glob, so the **ten** markdown files under `.claude/` — five
    ceremony skills, three reference skills, two agent definitions —
    are never structurally checked, by CI or by `scripts\test.cmd`. No
    paths filter can reach this; the scope is in the script. It matters
    because those files cite repo-relative paths in backticks and the
    house rule is that a cited path must exist: a skill citing a moved
    file would fail silently and surface only when an agent followed
    the dead path. Same family as item 6.
    **A second defect in the same script, found while writing this
    item and of the opposite polarity — a FALSE-RED (check-method
    failure mode 3).** The bold-parity check counts doubled-asterisk
    markers without excluding code spans, so a backticked glob ending
    in a doublestar — the exact string `ci-devops.yml` line 33 uses —
    is counted as an unterminated bold marker and the document is
    failed while being correct. It fired twice on this very queue
    edit, and the wording above is phrased around it rather than
    triggering it, which is a workaround and not a fix. Note the shape:
    the checker cannot express the one path expression this repository
    most needs to cite in prose. Detail:
    `docs/governance/PILOT_2026-08-12_corpus-lister-fan-out.md` and the
    settling read at item 24.
26. **`corpus-lister` scaling decisions owed before any wider fan-out**
    — NEW 2026-08-12, three design questions the pilot raised and did
    not decide. (a) Whether the agent should hold an execution tool at
    all, a permissions decision deliberately not taken as part of the
    transcription repair; (b) whether fan-out is the right instrument,
    given `scripts/corpus_manifest_entries.py` already emits a complete
    entry with hash for every unlisted document in one pass and writes
    nothing — the mechanical fields want a script, and the agents' real
    contribution was governance judgment; (c) the divergent shapes need
    pre-ruling, `processing` as `null` versus placeholder and the
    eligibility date as authoring act versus listing act, both of which
    validate against the parser. Note also that the listing debt is
    **seven documents wide, not three** — SG-03 through SG-09 are all
    unlisted — and that SG-03..06 stay excluded pending the item 9
    scope decision. Detail:
    `docs/governance/PILOT_2026-08-12_corpus-lister-fan-out.md`.
27. **Permission-tier review — CANDIDATE DRAFTED, awaiting ruling; not
    a change.** Occasion: tonight's pilot ran three subagents cleanly
    and concurrently inside their own tool grants while the lead
    needed operator approval for read-only inspection, scratchpad
    writes and pull-request waiting mechanics. The candidate
    classifies every prompting act of the session into deny (correct,
    unchanged), operator-only ask (correct, unchanged) and arc
    mechanics (proposed auto-allow while HEAD is not main). Merge,
    main, the registers, the corpus tree, settings and elevation stay
    operator-only without exception, and `gh pr merge` is explicitly
    excluded from the widening. **Two findings outrank the widening.**
    First, the Tier 1 rule strings are written for relative invocation
    and tonight's own no-bare-`cd` convention broke them — an absolute
    invocation does not match a relative rule, so the grants for the
    mandatory batteries stopped matching the way those batteries must
    now be invoked; lines 49-50 of `.claude/settings.json` already
    carry absolute duplicates for two scripts, so the pattern was
    evidenced in the tree before tonight. That closes the open half of
    item 4(c): the rule strings are no longer unverified, they are
    verified and wrong. Second, the review proposes a **narrowing** as
    well — `.claude/agents/` is absent from the guard's protected
    patterns, so agent definitions edit ungated while skills prompt,
    though an agent definition states what a subagent may do and is at
    least as load-bearing. Evidence basis is stated honestly in the
    candidate: there is no literal prompt log, and inferred rows are
    marked as such.
    **Extended 2026-08-12 with a merge-delegation clause**, for
    ruling: `gh pr merge` moves from unconditional ask to CONDITIONAL,
    permitted only when the PR carries the operator's own GitHub review
    approval **against the current head SHA** and all checks are green,
    both read by the guard from live GitHub state rather than from a
    rule string. The approval is the ruling record; the merge is then
    mechanics, and re-asking makes the operator rule twice for one
    decision. Every other Class B row stays operator-only unchanged.
    Three mechanics are specified because without them the clause does
    not hold: approval pinned to head SHA, so approve-push-merge cannot
    launder an unreviewed change; approval matched by operator
    identity, so a future collaborator does not inherit the delegation;
    and unreachable or unparseable GitHub is UNKNOWN, which asks — a
    delegation that failed open would be the register's oldest failure
    shape with merge rights attached.
    **Ruling condition, a condition and not a preference: the
    widening, the rule-string restatement and the `.claude/agents/`
    narrowing land TOGETHER, in ONE PR, each tested by probe.** They
    cannot be separated. Widening while the rule strings still assume
    relative invocation grants latitude that silently fails to apply
    where it is needed and may apply where it is not; narrowing later
    leaves agent definitions ungated through the very window in which
    the widening makes agent work easier. Probe-tested means what it
    meant tonight — a deny-shaped call returning the guard's own
    refusal text, paired with an allow-shaped call that succeeds —
    never a reading of the rule that finds it plausible. Detail:
    `docs/governance/TIER_AMENDMENT_CANDIDATE_2026-08-12.md` and
    `docs/governance/HARNESS_PERMISSION_TIERS_2026-08-11.md`.
28. **Extend the governed-store instrument to five tables** — NEW
    2026-08-12, FINDING RECORDED during the CL-24 closure.
    `scripts/governed_store_identity.py` snapshots four tables
    (`corpus_version`, `audit_run`, `audit_event`,
    `audit_run_terminal`) and does not see `audit_payload`, which held
    3 test-written rows throughout the CL-24 arc — invisible to the
    baseline file, invisible to `rehash_sweep.py`, and absent from
    every count the register carried. They were found only because the
    delete draft required reading the schema rather than the baseline.
    The rows are now cleared, so this is not outstanding residue; the
    outstanding defect is the **instrument**, which reported a store
    "empty" while a table it does not enumerate was not. Check-method
    family: a check whose stated subject is narrower than the subject
    it names. Fix is to enumerate tables from the metadata rather than
    a hardcoded list, so a table added later is covered by
    construction. Detail:
    `docs/governance/GOVERNANCE_REVIEW_CHANGELOG.md` CL-24 closure and
    `docs/governance/CL-24_governed-store-baseline_2026-08-12.md`.
29. **Ceremony-skills rewiring: describe → call
    `scripts/d22a_preflight.py`** — NEW 2026-08-12, **RULED IN** as
    transcription-in-spirit, execution deferred. `CLAUDE.md` and
    `.claude/skills/session-open/SKILL.md` still describe the ONNX
    cache traversal procedure in prose; they should call the artefact
    instead, which is the residue of the item 3 authoring debt. Not
    done at authoring because it is a **Tier 2** edit to ruled ceremony
    artefacts and build holds right of way under DEC-0017. Executes at
    the next governance-eligible window, **ideally riding the same PR
    as the item 27 tier-amendment work**, since both touch `.claude/`
    and both want one probe-tested landing. **+ F6 candidate rider:
    align session-open manifest invocation with documented `--out`
    (CL-27 record F6).** **Until then the prose descriptions stand** —
    and anyone who touches them carries a known-superseded note
    pointing at the script rather than editing the prose as though it
    were current. Detail:
    `docs/governance/GOVERNANCE_REVIEW_CHANGELOG.md` CL-26.
30. **D2.2a runner spike — the next arc under DEC-0017.** The spike
    proper, of which the pre-flight at item 3 was one part: minimal
    runner plus one retrieval scenario end-to-end — spec in, corpus
    queried at a pinned snapshot, result JSON out. Runs under the D2.0
    commissioning frame, pinned to the corpus snapshot **current at
    spike time**, which does not wait on the listing act and need not
    be a listed snapshot, so item 5's corpus debt does not block it.
    **COMMISSIONING-labelled throughout**, results permanently
    inadmissible as gate evidence, anomalies observed-not-raised.
    Exit criteria are a result JSON reproducible from its triple; the
    scenario's own pass/fail is **not** an exit criterion. **Closes
    with a Commissioning Session Record, not a report** — no pass/fail
    summary, because a report format invites promotion by osmosis.
    Claims the next free CL number, read live at the arc that opens
    it. Detail: `docs/governance/D2.0_COMMISSIONING_FRAME_2026-08-11.md`
    and `docs/governance/TOR_test-capability_RevC_RULED_2026-08-10.md`
    section 5A.
31. **`retrieval_snapshot_sha256` mandatory for retrieval-class at
    spec schema v0.2** — NEW 2026-08-13, OPEN. The field is optional at
    v0.1 and the schema's own comment defers the question to the D2.2a
    spike; the spike pinned it, ruled in as spike-scoped only, and did
    not settle it. Substance: the manifest hash excludes the processing
    facts — chunker version, embedding model, chunk counts — that
    decide what the retriever actually sees, so a retrieval scenario
    pinning only the manifest pair records a reproducibility claim
    narrower than it appears. A change is a **new versioned file**;
    v0.1 is immutable once merged and is never edited. Source: CL-27
    record F2,
    `docs/governance/COMMISSIONING_SESSION_RECORD_2026-08-13_d22a-runner-spike.md`.
32. **Harness shell cp1252 encoding corrupts transcript rendering** —
    NEW 2026-08-13, OPEN, LOW PRIORITY. The shell resolves to the
    Windows ANSI code page, so printing any repository artefact
    containing an em-dash or arrow raises a Unicode encode error until
    UTF-8 is forced, and the runner's own stdout rendered its regime
    banner's em-dash as a replacement character in every captured run.
    Fix is to force UTF-8 at harness entry. Affects transcript
    fidelity, not artefact content. Source: CL-27 record F7,
    `docs/governance/COMMISSIONING_SESSION_RECORD_2026-08-13_d22a-runner-spike.md`.
<!-- QUEUE-END -->

## Orientation for a new session

Run `/session-open` first. Then: `START_HERE.md` → `DECISIONS.md` (rulings R1–R13, DEC
series, ADRs) → `BUILD_TRACKER.md` (next unpassed gate) → the newest
`docs/governance/SESSION_HANDOVER_*.md`, whose boot line is the current state of play.
`CURRENT_STATE.md` and `SESSION_PROTOCOLS.md` both lag current practice — treat the
latest handover as authoritative where they disagree.
