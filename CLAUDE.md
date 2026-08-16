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
`pyproject.toml`, `.github/workflows/`, and `decisions/`, which
is gated because `scripts/repo_manifest.py` reads register numbers off filenames there,
making any write to it register-consuming by mechanism. Gated by repository state rather
than by path: PR merge, branch deletion, and any git write while HEAD is main. Legitimate
touches are normal governed acts; the gate makes each one deliberate, not impossible.
When the prompt fires, restate which governed act the edit serves before proceeding.

**Tier 3 — operator rulings.** Arc selection, scope, merges, frame rulings, register
decisions. Not tool gates, and no mechanism grants them.

**Denied outright (no exception path — do not ask):** force push in any form (the CL-E1
incident guard), git history rewrites, recursive force deletes, force branch deletion
(`git branch -D` and the long form), the write forms of the read-class grants (`find`
with its delete or exec flags, `sort` with its output flag), **writes to the permission
and ceremony system — `.claude/settings.json`, `.claude/hooks/`, `.claude/skills/`,
`.claude/agents/`** — and elevation; the harness never elevates, and never assumes the
database owner role. Any fix requiring one of these is the operator's, at their own
terminal, re-verified afterwards from a non-elevated shell.

**The never-silent set, ruled 2026-08-14 (WS-E 69 fix item 1).** Those four `.claude/`
paths drew a Tier 2 ask until that date. An ask is a gate only while it reaches a
person, and it does not: a bypassing permission mode auto-approves asks without
surfacing them, so the absence of a prompt evidences nothing. Deny is the only response
no mode and no approval overrides. **The cost is accepted rather than overlooked: there
is no in-session write to those paths again — including the write that would repair the
guard or roll back this deny.** Harness changes are drafted outside the tree, installed
by the operator at their own terminal, then branch → PR → merge. Reads are untouched,
so every ceremony that inspects `.claude/` is unaffected. The deny covers the
file-writing tools by path alone; it covers shell commands only through the same verb
list the ask used, which is narrower, and widening that list is a separate act.

`.claude/hooks/governance_guard.py` enforces the denies and the Tier 2 asks, routed by
the PreToolUse matcher in `.claude/settings.json`. **Coverage is two-part and both parts
must name a tool:** the matcher routes the call, and the module's shell-tool set decides
whether the command is inspected. Either alone is a silent no-op — WS-E 64 records three
days in which the guard was wired to the Bash tool while PowerShell, this repo's primary
shell, went unguarded. Adding a shell tool means adding it in both places.

**A Tier 1 allow rule pre-empts a Tier 2 guard ask** — tested 2026-08-11, and the guard
loses. The two mechanisms are alternatives, not layers, so: **never grant in Tier 1
anything Tier 2 is relied on to gate.** An allow rule covering the same ground as a guard
ask is not belt-and-braces; it is the gate switched off silently. **Whether a deny is
pre-empted the same way was tested 2026-08-14 under `bypassPermissions`, and the deny
FIRED** — a matching allow rule for the force-push family did not stop the guard's own
refusal coming back verbatim
(`docs/governance/PRECEDENCE_DISCRIMINATOR_OUTCOME_2026-08-14.md`). **Read the mode
qualifier before relying on it:** that session auto-approved asks without surfacing them,
so the absence of a prompt evidences nothing, and **deny-precedence in default mode is
UNPROVEN** — a re-run in an ask-tier session is owed at WS-E 69. That is one family, deny
only, under one mode; it leaves the allow-pre-empts-ask finding above untouched. **Never allow-list a
command family that carries a deny** stands regardless, on the narrower ground that such an
overlap buys nothing. Ceremony skills carry their own `allowed-tools` frontmatter,
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

Any session touching retrieval starts with the standing first act, and the act is to
**call `python scripts/d22a_preflight.py`**, not to re-perform the check from prose.
Exit 0 with 4/4 GREEN is the only pass; UNKNOWN and SKIPPED both exit non-zero. The
prose ONNX-cache-traversal description this line used to carry asserted no
non-elevation and returned green under an elevated shell — the artefact supersedes it
(CL-26), and describing a procedure the repository already implements is how the two
drift apart.

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
5. **Corpus listing owed for SG-07, SG-08 and SG-09 — DISCHARGED.
   CLOSED 2026-08-17.** The listing act is complete: `MANIFEST.yaml` at
   `2026-08-13.8` carries **30 documents**, including SYN-SG-03 through
   SYN-SG-09 and SYN-TY-03 through SYN-TY-09, all fourteen at
   `pending_review`. Read live from the manifest via the DEC-0014
   machinery at the 2026-08-17 boot, not from a report. **What remains
   is not listing but the inclusion decision**, which is item 12 and is
   the operator's. Recorded rather than deleted because this item was
   carried as open for several sessions after the act that discharged
   it had already landed, which is the queue-staleness pattern the boot
   readback exists to catch. Detail:
   `docs/governance/SESSION_HANDOVER_2026-08-11c.md` open
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
12. **Operator inclusion decision — WIDENED 2026-08-17, and it is
    FOURTEEN documents, not seven.** OPEN, when ready. The item read
    "TY-03..09"; the live manifest shows **SYN-SG-03..09 AND
    SYN-TY-03..09**, all fourteen sitting at `pending_review`, eligible
    count 16 of 30. An inclusion decision would move the eligible set
    from 16 toward 23 or 30 and would therefore **change
    `retrieval_snapshot_sha256`, the eligible-set hash and the indexed
    chunk count**, which are pinned by every retrieval scenario spec —
    so it is a re-pinning event for the scenario set, not only a corpus
    act. Sequence it against scenario authoring deliberately rather
    than letting it land mid-flight. Detail:
    `docs/governance/SESSION_HANDOVER_2026-08-11c.md` return
    queue 10; `docs/governance/SESSION_HANDOVER_2026-08-17.md` §7.
    **GUARD 2 — SEVEN SCENARIOS NOW CARRY RE-PIN DEBT AGAINST THIS
    DECISION, appended 2026-08-17.** `RQA-101`, `RQA-102`, `RQA-103`,
    `RQA-104`, `RQA-105`, `RQA-106` and `RQA-107`, authored this date
    against the 16-document eligible set and all pinning one corpus
    state — `2026-08-13.8` / `2d5f2fb5…3809c` / rss `878b3439…ab928`.
    An inclusion ruling moves all three values and every one of the
    seven is re-pinned. **Two of the seven need more than a re-pin, and
    the difference is load-bearing.** `RQA-106` carries a **RE-AUTHORING
    trigger**: `SYN-TY-03` and `SYN-TY-04` are near-duplicates of its
    expected set by subject, and sufficiency is a property of the
    eligible set rather than of a document in isolation, so if either
    becomes eligible the claim that its E members are necessary may
    cease to be true and criterion 2 fails by construction — re-pinning
    alone would carry forward a sufficiency argument that no longer
    holds, and the re-author must fix E before any retrieval against
    the new snapshot. `RQA-104` carries an **Obligation D EXPIRY**: its
    series grows from two documents to nine, the `\|E\| >= 5` route
    becomes constructible, and its justification stops holding, so
    Obligation D is re-discharged by a graded scenario against the
    enlarged set rather than by re-citing the existing one. Weaker
    cases at `RQA-105` and `RQA-101` are recorded in their own
    authoring records. Detail:
    `verticals/fraud/scenarios/RQA-BATCH1.set-record.md`.
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
18. **TOR errata — DISCHARGED. CLOSED 2026-08-17.** Carried to the Test
    Plan (D1.1), which is **ACCEPTED at Rev C** (CL-30, PR #134,
    2026-08-16). The errata are carried in the accepted text. Detail:
    `docs/governance/SESSION_HANDOVER_2026-08-10c.md`, the PR #83 body,
    and `docs/governance/D1.1_REVC_ACCEPTANCE_2026-08-16.md`.
    Reporting rule inherited: D1.1 specifies the Regime-2 Test Report
    (operator ruling 2026-08-11).
    **Residue, tracked separately and NOT closed by this:** the
    `TOR §5A:101` post-acceptance amendment route is now OPEN, and its
    first customer is the TOR-side three-leg identity statements at
    `TOR §5:74` and `TOR §8:124`, deferred by name at `F-GROK-08`. That
    is TOR text, not Test Plan text, and it remains owed.
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
    not decide. **NARROWED 2026-08-17: the listing debt this item was
    scoped against is DISCHARGED** — all thirty documents are listed
    (see item 5), so there is no outstanding fan-out to scale and the
    urgency is gone. The three design questions survive on their own
    merits, for the next time a fan-out is proposed; the count in this
    item's closing paragraph — "seven documents wide" — is spent and
    should not be read as live debt. (a) Whether the agent should hold an execution tool at
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
27. **Permission-tier review — HELD 2026-08-17. NOT DISCHARGED.**
    **Status by component:** the rule-string restatement and the
    `.claude/agents/` narrowing discharged earlier at `678f46a`, the
    latter superseded entirely when all four `.claude/` paths became
    DENY on 2026-08-14. **Part A, the READ/VERIFY widening, is APPLIED**
    at the operator's terminal 2026-08-17 and is probe-supported.
    **Part B, the REVERSIBLE-MUTATION widening, is HELD** and the reason
    is evidence rather than caution. It was drafted with a blocker
    already stated — an allow rule pre-empts a guard ask, the
    HEAD-is-main protection lives in the guard, and the branch condition
    cannot be a rule string, so settings-allowing the git write verbs
    would remove the gate on main rather than widen it off main. The
    probe set then found worse: **WS-E 72**, the guard's git denies can
    fail to match at all. Widening the git write verbs against a deny
    surface with a known bypass compounds two defects. **Part B unblocks
    when item 42's guard repair and re-probe list pass**, not before.
    The item cannot be discharged while its principal component is held;
    saying otherwise would be the overclaim the together-in-one-PR
    condition existed to prevent. Detail:
    `docs/governance/PERMISSION_CLASSES_2026-08-17_partA-applied-widening-held.md`.
    Original candidate text follows.
    Occasion: tonight's pilot ran three subagents cleanly
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
    **COORDINATOR EXPANSION (2026-08-13, ruled).** The item above states
    the defect; this states how it is discharged.
    *Verify-first obligations, which the implementing session performs and
    this item does not:* (1) enumerate the five tables from the LIVE schema
    as `arcaai_app`, non-elevated, noting that `information_schema` is
    privilege-filtered and can return false-complete listings (item 8
    dossier) — corroborate by a second method, the in-tree migrations or
    DDL, before treating the list as the coverage target; (2) read the
    instrument and the sweep and enumerate their ACTUAL table coverage from
    the code, not from this item's claim about it.
    *Required change:* identity reporting extended to `audit_payload` and to
    any divergence the read reveals — row counts plus identity-scoped counts
    per table, in the existing output discipline. **The sweep's GREEN names
    all five tables explicitly**, because a scope-naming output is checkable
    and "all tables" is not. Three-outcome discipline per table; an
    unreadable table is UNKNOWN and exits non-zero. No elevation and no
    owner-role assumption (WS-E 66): owner-only readability is a named
    UNKNOWN, never an elevation prompt.
    *Verification:* D-1, a revoked or absent grant resolves to UNKNOWN at
    non-zero exit, so a false-complete listing cannot recur silently; D-2, a
    four-table GREEN must be impossible to emit — probe by scope-list
    injection if the design permits it, and state the limit plainly if it
    does not; A-1, a full run as `arcaai_app` reports five named tables,
    GREEN.
    *Out of scope:* schema changes, data acts, and the definition of
    "identity-scoped". *Open at implementation:* whether the extended sweep
    supersedes the ceremony's or runs alongside it until parity is shown.
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
30. **D2.2a runner spike — DISCHARGED at CL-29, PR #131. CLOSED
    2026-08-16.** Exit criterion met: **REPRODUCIBLE YES** — four runs
    of RQA-107 at one triple, comparable-content sha256
    `aeed2757…a209ef` on every one, with `generated_at_utc` the only
    differing field and raw scores exactly equal. The scenario's own
    pass/fail was not an exit criterion and none is recorded
    (`recall_at_k` 0.0, acceptance NOT EVALUATED, nothing tuned).
    **Finding yield: eleven unhonoured Rev C requirements**, six
    runner-side and five spec-side, now carried at items 35 and 36.
    Ruled at close: the **D3.1 golden-baseline door keys on the
    comparable-content hash, not the raw artefact hash**; run 1
    (`56ab9ac5…`) is the candidate baseline. Preservation discharged by
    read-back, 6/6 at
    `D:\ArcaAI-artefact-custody\2026-08-16-spike-2\`. Record:
    `docs/governance/COMMISSIONING_SESSION_RECORD_2026-08-16_d22a-runner-spike-2.md`.
    Historical scope below, retained for the reasoning it carries: the
    spike
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
    spec schema v0.2 — DISCHARGED. CLOSED 2026-08-17.** The v0.2 schema
    exists in the tree at
    `arcaai/harness/schema/scenario_spec_v0.2.schema.json` and makes the
    field **required inside the retrieval-class branch**, conditional
    rather than unconditional so it does not bind scoring-class
    scenarios that pin a snapshot without querying an index. The runner
    selects a schema from the spec's declared version. Verified live at
    the 2026-08-16 spike, which validated RQA-107 against v0.2 and
    proved by deny-shaped probe D1 that dropping the field is refused —
    the same spec passing under v0.1, so the refusal evidences that
    v0.2 was the schema applied. **This item was carried as OPEN after
    the artefact discharging it had already merged**; recorded rather
    than deleted, as the queue-staleness pattern at item 5. Original
    text follows. The field is optional at
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
33. **Pre-B7-exit ruling pack** — NEW 2026-08-13, RULED IN as an item.
    B7 exit (plan step 10) opens B8/B9, and three architecture decisions
    recorded in the operator's drafts of 28 Jul, 9 Aug and 10 Aug 2026 are
    owed BEFORE that door opens. Those drafts live in Gmail, **outside this
    repository**, which is itself the reason the item exists: if the door
    opens first, code decides these implicitly and the record is written
    backwards. **Premise to verify at implementation, not now:** check the
    SME panel's 21 ruled items before treating any amendment below as
    homeless.
    **P1 — Integration-modes ADR.** *Panel: ADVISABLE.* Three decision
    classes — inline authorisation with explicit fail-open or fail-closed on
    timeout; post-event pre-settlement; retrospective batch. The
    feature-availability fork (platform-owned pre-computed store versus
    enrich-at-call) is named the binding constraint. The audit-write fork
    (durable-write-before-response on the authorisation path, async
    elsewhere) is decided explicitly under SM&CR reasoning. The integration
    surface is adapter-shaped to protect ADR-0009, with the B9.5 consequence
    noted. Commercial sequencing — build real-time, pilot deferred — is
    recorded as context only.
    **P2 — Mandate/admission-check design note.** *Panel: ADVISABLE,
    strongly.* Panel-convergent finding: the mandate artefact does not exist
    and is the most important new control surface. The note covers schema;
    versioning; the revocation path and its failure semantics, including a
    running component holding a revoked mandate and an unavailable mandate
    store; three-way hash reconciliation across artefact, mandate and
    promotion record; and platform-level enforcement with a negative CI test
    in which an unmandated artefact hard-fails. **No consolidation or memory
    code before this note is ruled.**
    **P3 — Panel amendment disposition table.** *Panel: COURTESY
    re-circulation.* Enumerate the four reviews' required amendments against
    the 21 ruled items as ADOPTED (cite), REJECTED (cite), or HOMELESS
    (owner plus vehicle). Check-set at minimum: tenant isolation as a named
    gate criterion pre-AWS; per-tier context budgets with summarisation
    discipline; Policy Fast Lane as a release class with bounds, validators
    and re-review; two-zone Domain 1 with a redaction pipeline as a mandated
    artefact; a memory-pattern DEC generalising DEC-0014; transactional
    hash-pinned rollback; canary isolation with independent verification;
    statistical parity for promotion gates; attestation signing, carrying
    the DeepSeek dissent verbatim; a single audited loader with
    least-privilege egress; a consolidation cost cap; a minimum-viable ops
    manual plus mock-bank trial; and the S16 Domain-1 pilot rulings as
    production-critical-path.
    **PANEL-ROUND CONVENTION — CANDIDATE.** Documents circulate only as
    committed, hash-pinned drafts, with the hash stated in the circulation
    pack. Every panel response returns verbatim as a committed file pinned
    to the reviewed hash, and dissents are never summarised. The chair's
    ruling closes each round with a per-finding disposition table: adopted /
    rejected-with-reason / deferred-with-owner. Marked CANDIDATE
    deliberately — whether it earns a DEC number is ruled when it is first
    exercised, not before.
    **Feeder notes.** The Brain/Hands Decoupling seed enters ADR-0011's
    input set. Its "ADR 0012" numbering lives in the operator's Gmail draft
    outside this repository and no repo file carries it — verified by a
    repo-wide search on 2026-08-13, where `0012` resolves only to DEC-0012.
    The correction is therefore scoped to the **seed's commit header at ADR
    input assembly**, against the register anchor live at that moment, and
    to no existing file.
    *Transmission note:* the brief conveying this item truncated at the
    feeder-notes line. The Brain/Hands note above is reconstructed from the
    same brief's preamble and the 2026-08-13 ruling, both of which state it
    explicitly. **If further feeder notes were intended they are missing**;
    confirm before treating this list as complete.
34. **Audit-readiness: SDLC control framework + evidence map** — NEW
    2026-08-13, RULED IN as an item. **Rationale:** ArcaAI's proposition
    makes the development lifecycle itself part of the product — internal
    engineering discipline IS the customer's regulatory evidence pack. A
    prospect bank's skilled person will audit the build process and the
    governance around it, and **that audit cannot be failed**. This item
    converts existing practice into a named, testable control set;
    practice that is real but unnamed is not a control an auditor can
    test.
    **Deliverable:** one document, the SDLC control framework,
    enumerating the controls already in force — register discipline; the
    two-regime model; hash-pinned custody including review documents;
    the panel-round convention with recorded dissent; deny-probe
    verification; the Option B merge gate; three-outcome checks — and
    mapping each to SS1/23 model-risk expectations. Item 33's P3
    disposition table is its seed.
    **Mechanisms to build under this item, each its own arc:**
    **M1 — Intelligent CI reviewer.** An agent in CI reading every PR
    diff against the standing rules — attribution, regime labels,
    protected paths, register discipline — and commenting before human
    review. Converts the written rulebook into a control an auditor can
    test rather than a document an auditor must take on trust.
    **M2 — Coordination-layer session records.** The judgment layer's
    numbered prompts and operator rulings committed per session as
    governed artefacts, closing the gap where the deliberative trail
    lives outside the evidence perimeter. Evidence that the gap is real
    and not theoretical: the 2026-08-10 rulings record survived only on
    the operator's Downloads folder, was searched for exhaustively
    in-repo and found nowhere, and entered the tree on 2026-08-13 at
    `docs/governance/ADR-candidate-input_rulings-record_2026-08-13.md`
    only because it was supplied from disk.
    **M3 — Server-side enforcement.** Client-side guards under
    `.claude/` bind only the executor's tool calls; **any other git client
    bypasses them entirely.** Enable GitHub branch protection on `main`:
    required checks, required review, force-push and branch-deletion
    disabled at platform level. The client guards then become defence in
    depth over an environment-independent control, rather than the
    control itself. *Near-term candidate: high evidence per hour.*
    **M4 — Cryptographic signing and external anchoring.** SSH-signed
    commits, and signed tags per gate or record, convert **asserted**
    attribution into **key-bound** attribution and give tamper-evident
    anchors. Pushing signed tags to GitHub anchors `main`'s history
    outside the operator's machine. *Near-term candidate.*
    **M5 — AI-authorship policy, stated.** The no-`Co-Authored-By` rule
    strips per-line provenance **by design**, and the policy that makes
    that defensible has never been written down. It must be: all code is
    executor-drafted and operator-reviewed under the two-regime model;
    review is evidenced by the PR trail; authorship provenance is **by
    process, not by per-line labels**. Without the written policy, the
    attribution-stripping reads as concealment — which is precisely how a
    skilled person would read it.
    **M6 — Evidence-store custody split.** CL-24 demonstrated that the
    owner role can empty the audit store. That was correct under
    commissioning and would be fatal in production. Production requires
    WORM-class retention, or writer/deleter role separation with deletion
    as an alarmed event. Named now so the CL-24 precedent is **explained
    rather than discovered** by whoever reads the register next.
    **M7 — Traceability matrix.** One artefact walking requirement →
    decision (DEC/ADR) → code (PR) → test (probe or record) → evidence
    (pack), navigable in **both** directions. Candidate: generated from
    the registers by script rather than maintained by hand. This is the
    document an audit starts from.
    **AMENDED 2026-08-13.** The control framework and the traceability
    matrix map **primarily to SS1/23 principles and the ISO/IEC 42001
    clause structure**, with **ISO 27001 and SOC 2 trust criteria as
    secondary maps**. External attestation is named as a **STAGED**
    target, not a present claim: **SOC 2 Type II at the first serious
    prospect** — its observation period means the clock starts early, so
    the decision to begin is itself time-sensitive — and **ISO 42001 when
    revenue justifies it**. Any interim external review is by a
    **specialist independent firm, non-channel** per the external-party
    boundary recorded below.
    **M8 — Gate evidence packs and retention policy.** Each gate emits a
    standard pack — hashes, probe tables, run records, approvals — to a
    defined retention location, under a stated policy: what is kept,
    where, for how long, and immutable by what mechanism. The 2026-08-13
    manual scratchpad preservation (42 files copied to a durable
    location, 6 of 6 custody hashes verified against the committed
    record) is the manual instance proving the need.
    **Telemetry notes appended 2026-08-13**, from the first session-cost
    row at `docs/governance/SESSION_COSTS.md`. Both are candidate acts,
    not rulings.
    (i) **Context hygiene.** Use `/clear` at arc boundaries once M2
    session records make reconstruction cheap. **93% of 2026-08-13 usage
    ran above 150k context**, and that was the day's dominant cost
    driver. The dependency runs the right way round and matters: clearing
    is only safe once the deliberative trail is recoverable from the
    repository, which is precisely what M2 builds — so this note waits on
    M2 rather than racing it.
    (ii) **Subagent model tiering.** Trial a cheaper-model
    `corpus-lister` on the next fan-out. The evidence is from the same
    day: the lead **recomputed every hash regardless**, and all seven
    agents reported failure mode 2 on `content_sha256` because they hold
    no execution tool. The verification burden therefore already sits
    above the subagent tier, so a cheaper tier loses nothing that was
    being relied on.
    **M9 — Restore evidence and recovery guide in-repo.** The recovery
    guide currently lives in a Gmail draft, which is itself a finding of
    the same shape as M2; commit it. Add a periodic **evidenced restore
    drill**, answering the auditor's question "when did you last test
    restore?" — for which the current honest answer is **never**.
    **M10 — Actor identity, independent validation, dependency
    provenance.** (a) Distinguish **operator-decided** from
    **executor-performed** acts, by commit trailer or session record —
    applying the Brain/Hands who-decided-versus-who-executed doctrine to
    the build process itself. (b) Name lane one's spec-blind test-author
    explicitly as the **SS1/23 independent-validation function** in the
    control framework: one paragraph converting an architecture choice
    into a named regulatory control. (c) Full dependency lockfile with
    hashes, plus a basic SBOM stance, for the supply-chain question.
    **M11 — Standards-mapping convention for governed artefacts.** Every
    governed artefact of the classes below carries a standards-mapping
    line in its header or footer, in one controlled form:
    `Control mapping: <framework> <ref>[; <framework> <ref>...]`
    Controlled vocabulary, closed: SS1/23, ISO42001, ISO27001, SOC2,
    NIST-AI-RMF, EU-AI-Act.
    (a) **The line is a MAPPING, never a compliance claim.** The words
    *compliant*, *certified* and *conformant* are **FORBIDDEN** in the
    line absent an actual certificate. `scripts/check_docs.py` gains an
    assertion enforcing both the line format AND the forbidden-words
    rule — a mechanism, not a convention, because a convention against
    overclaiming is exactly the kind that erodes under sales pressure.
    (b) **Prospective** for new artefacts in these classes: DEC and ADR
    entries, rulings records, session and gate records, the TOR and Test
    Plan, evidence packs, and the control framework itself.
    (c) **Retrofit is selective** — key existing artefacts gain the line
    at their next legitimate touch, **never as a history rewrite**.
    (d) **Per-class mapping content is defined once in the control
    framework**, so authors copy rather than compose and two artefacts of
    a class cannot map the same obligation differently. First exercised
    on the control framework itself.
    **Known findings the framework must STATE HONESTLY rather than
    hide** — a framework that omits its own weaknesses fails the audit
    it was written for:
    (a) **Single-operator segregation-of-duties limit.** Mitigations:
    the panel convention as independent challenge, with sustained
    dissents as the evidence it is real; a future customer-bank SMF in
    the loop; and any external attestation via an INDEPENDENT third
    party only.
    (b) **Process-versus-outcome evidence gap.** The Test Plan and lane
    one are the answer, and are sequenced already.
    **External-party boundary — RULED 2026-08-13.** PwC is
    **channel-only and build-excluded**: no PwC personnel, systems,
    credentials or engagement materials touch the repository,
    governance, infrastructure or evidence pack, and there is no
    cross-contamination of work product in either direction. A
    cross-reference scan in the `scripts/check_docs.py` style, asserting
    zero PwC engagement references in the repo, is a **candidate
    mechanical control** — candidate, because the ruling is the control
    and the scan would only evidence it. Channel use, if ever, flows
    only through an explicit conflict-management arrangement with PwC
    compliance — the ethical-wall conversation, owner Mike, before any
    live sales activity.
    **Sequencing:** after item 33's ruling pack, since P3 feeds the map;
    and **before any live sales conversation**. Within the mechanisms:
    **M3 and M4 are immediately buildable** and are candidate filler for
    the next sessions; **M6 is production-phase**, named early so the
    CL-24 precedent carries its explanation; the rest ride the
    control-framework deliverable.
35. **Scenario spec schema v0.3 — NEW 2026-08-17, OPEN. The critical
    path's likely first authoring act.** The D2.2a spike found **five
    Rev C requirements v0.2 cannot hold**, because v0.2 is
    `additionalProperties: false` at every level and predates every
    round-2 fix. Four are carried in the spec's `description` under the
    machine-findable prefix `CARRIED-NO-FIELD:` so a migration can find
    every affected spec by grep: the **absolute `top_k` cap**, which
    Rev C §5.4 says every scenario records *in the spec*; the
    **binary-probe justification** (§5.3); the **Obligation D
    justification** (§2.1); and the **density-stratified note** (§5.2).
    The fifth is the **typology identifier**, used with an
    `unverifiable-pending-vocabulary:` prefix because §2.4 requires a
    stable identifier and no controlled vocabulary exists to draw one
    from (Appendix B item 16) — and a schema can require a field but
    cannot require that the field mean something, so this half needs the
    corpus-side vocabulary and not only v0.3. **Fix route is a new
    versioned file**; v0.2 is immutable once merged and is never
    edited. **Every scenario authored against v0.2 carries
    `CARRIED-NO-FIELD` baggage until this lands**, which is the argument
    for taking it before scenario authoring rather than after. Detail:
    `docs/governance/COMMISSIONING_SESSION_RECORD_2026-08-16_d22a-runner-spike-2.md`
    §12 and `docs/governance/SESSION_HANDOVER_2026-08-17.md` §5.
36. **Runner Rev C conformance — six unhonoured fields. NEW
    2026-08-17, OPEN.** Confirmed ABSENT from the emitted result
    artefact by reading its keys, not by reading the code alone:
    **`evaluator_version`** (§6.8.1, the fourth identity leg — the
    runner predates it); **`environment_config_sha256`** (§8.1
    criterion 7); **`material_parameter_list_sha256`** (§9.5
    element 3); **`confound: single_chunk`** (§12.3 — **it should have
    fired**, both RQA-107 expected documents being single-chunk);
    **`session_status: halted`** (§8.3 — no abort path exists in
    `arcaai/harness/runner.py`: no signal handling, no `finally`);
    **`invalidation_status`** (§9.8 — D2.5 ledger, the runner writes no
    rows). Two of the six are the sharpest: the values for
    `environment_config_sha256` and `material_parameter_list_sha256`
    **already exist**, computed at the spike and preserved in custody,
    and the runner simply does not carry them into the result — so the
    artefact's environment identity is incomplete on its face while the
    information needed to complete it sits beside it. Carries
    DeepSeek's runner-build note from the delta round: the named
    material-parameter list must include **search-time** parameters
    such as `ef_search`, not only index-build parameters —
    independently corroborated, the spike's list v0.1 having included
    `hnsw_ef_search` without sight of that return. Detail:
    `docs/governance/D1.1_REVC_ACCEPTANCE_2026-08-16.md` §7.
    **EXTENDED 2026-08-17 — a SEVENTH item, the load-time comparison
    schema v0.3 cannot hold.** v0.3 adds `top_k_absolute_cap` as a
    required retrieval-block field, so the cap is now recorded
    structurally on every scenario. **JSON Schema cannot compare two
    sibling values**, so the schema records the cap and does not assert
    `top_k <= top_k_absolute_cap`; a spec whose `top_k` exceeds its own
    cap validates cleanly today, and a test asserts that so the limit
    is found by whoever changes it rather than by whoever trusts it.
    **The runner must make that comparison at load time** and refuse on
    breach, which is the only place it can be made. Rev C §5.4 also
    makes a corpus expansion pushing a scenario past its recorded cap a
    **ruled variance under §5.5** before that scenario runs again — a
    second assertion the runner is the natural home for, and one that
    bites the moment the item 12 inclusion decision lands. Detail:
    `arcaai/harness/schema/scenario_spec_v0.3.schema.json`, the
    `top_k_absolute_cap` description.
37. **Rev C filename still says DRAFT — NEW 2026-08-17, OPEN,
    cosmetic but not nothing.** The accepted text lives at
    `docs/governance/D1.1_TEST_PLAN_DRAFT_RevC_2026-08-15.md`. D1.1
    exited DRAFT status at acceptance on 2026-08-16, so the filename now
    contradicts the document's own status and every future citation
    inherits the contradiction. The rename **touches every citation of
    the path** across the governance tree, which is why it is a
    deliberate act rather than a tidy-up: `scripts/check_docs.py`
    enforces that a backticked repo-relative path exists, so a rename
    without a sweep breaks the docs check. Detail:
    `docs/governance/D1.1_REVC_ACCEPTANCE_2026-08-16.md` §8 item 1.
38. **Delta pack send-time record act — NEW 2026-08-17, OPEN, one
    line.** `docs/governance/D1.1_ROUND2_DELTA_CIRCULATION_2026-08-16.md`
    §3 carries an empty send-time row. It is **record-only** and gates
    nothing: the 2026-08-16 same-day ruling made the deadline absolute,
    so nothing computes from it and §10 item 1 is SPENT rather than
    closed. The value was asked for twice and not supplied; **no time
    was invented**, because a fabricated timestamp in the circulation
    instrument of an accepted document is exactly the failure the empty
    slot was protecting against. Fill it from the operator's actual send
    time whenever convenient, or rule it permanently unrecorded — both
    are fine, and only silence is not.
39. **Governance guard denies a READ-ONLY command that names a
    protected path — RAISED AS WS-E 73, 2026-08-17. MECHANISM
    CORRECTED; the original diagnosis below was WRONG.** Observed
    in-session 2026-08-16: a command composed only of `ls`, `git status`
    and `git check-ignore`, naming `.claude/agents/` and
    `.claude/skills/`, was refused with the guard's **write**-deny text.
    **CORRECTION 2026-08-17, on evidence from the PROMPT 123 probe
    set.** This item stated the trigger as the path string — *"The guard
    matched the path string, not the verb"* — and that is
    **DISCONFIRMED**. Four commands, one variable:
    `ls -la <path>/.claude/agents/` EXECUTED;
    `git check-ignore -v .claude/agents/corpus-lister.md` EXECUTED;
    `ls -la <path>/.claude/skills/` EXECUTED; and
    `ls -la <path>/.claude/agents/ 2>&1 | head -3` REFUSED. **The
    trigger is the `>` inside `2>&1`**, a descriptor duplication that
    writes no file, which the guard's write-detection reads as a write
    construct. The original instance carried `2>&1` twice, which
    explains it exactly. Corrected rather than deleted, because a wrong
    diagnosis that survived on a compound command in which the true
    variable was never isolated is itself the lesson. Full record at WS-E
    73; fix spec at
    `docs/governance/FINDINGS_2026-08-17_guard-bypass-ADDENDUM_fix-spec.md`.
    The original text follows for the trail. **This contradicts
    the enforcement section of this file**, which states that the
    `.claude/` deny covers writes and that "Reads are untouched" — and
    a guidance-versus-hook disagreement is by this file's own rule a
    WS-E item. Polarity is worth naming: this is a **false-RED**, the
    opposite of the family's usual false-green, and it is the safer
    direction to fail — but it defeats exactly the read-only inspection
    that verifying a `.claude/` change depends on, so it has teeth. The
    workaround used was the file-read tools, which the deny does not
    cover; that is a workaround and not a fix, and it means the two
    surfaces disagree about what a read is. **WS-E next 72 is free and
    is NOT consumed by this queue entry** — raising it is a governed act
    and a separate one. Related: item 25's false-red in
    `check_docs.py`, and the item 8 check-method family.
40. **Pre-existing pytest failure blocks full-suite green as evidence
    — NEW 2026-08-17, OPEN.**
    `api/tests/test_api_contract.py::test_route_is_wired_to_contract_models`
    fails with `AttributeError: '_IncludedRouter' object has no
    attribute 'path'`. It is FastAPI/Starlette dependency drift: the
    test iterates `app.routes` expecting route objects and the
    installed version yields an `_IncludedRouter` wrapper. **Verified
    pre-existing** by running the same test at pristine `main` in a
    throwaway git worktree on 2026-08-17 — it failed identically there,
    so it is not caused by any change of that date. **The consequence
    is what makes this a queue item rather than a nuisance: a full
    `pytest` run exits 1 for a reason unrelated to whatever is being
    tested, so "full suite green" is unavailable as evidence until it
    is fixed.** Every session must instead report the failure as itself
    and distinguish it from new failures, which is a manual
    discrimination and therefore exactly the kind that eventually gets
    skipped. Note CI does not catch it: `ci-devops` passed on the v0.3
    PR, so the workflow's own scope differs from a local full run —
    worth establishing which is right before fixing the test. Same
    family as item 8.
41. **No live register home for code-series artefacts — NEW
    2026-08-17, PLACEMENT OWED.** Surfaced when ruling D5 of the v0.3
    arc directed the scenario spec schema series into
    `docs/governance/document-register.yaml`. That file is a **six-line
    RETIRED tombstone** — `status: retired`, `superseded_by:
    ../../DECISIONS.md`, retained so stale links fail loudly rather
    than silently — so writing entries into it would resurrect a
    retired register against its own text, in one of the six Tier 2
    governed stores. The canonical alternative it names, `DECISIONS.md`
    **Locked suite**, registers the June 2026 business-document suite
    and not code artefacts, so schema files there are a second category
    error. **Net: versioned code artefacts have nowhere to be
    registered.** Today the schema series carries its own provenance in
    each file's description block, which is the v0.1/v0.2/v0.3
    convention and works — but it is per-artefact self-description, not
    a register, and nothing enumerates the series from outside it.
    **Placement to be ruled under item 34's audit-readiness work**,
    where M7's traceability matrix needs exactly this: an artefact an
    auditor can start from that lists what exists. Detail: the v0.3
    stop report of 2026-08-17 §5.
42. **Guard repair for WS-E 72 and 73, plus the re-probe list — NEW
    2026-08-17, OPEN. BLOCKS item 27 Part B.** Two pattern defects,
    both operator acts at the operator's terminal because the fix is a
    `.claude/hooks/` change carrying an absolute deny. **F1:** anchor
    the deny patterns on the subcommand **anywhere in the argument
    vector** rather than immediately after `git`, which closes the class
    rather than the single tested member — git global options sit
    between executable and subcommand, so any adjacency-requiring
    pattern is defeated by any of them. **F2:** stop treating `2>&1` as
    a write construct; distinguish a file redirection from a descriptor
    duplication, or the protected-path write-deny keeps firing on
    read-only commands. **Re-probe, and a green is only a green when
    every row passes:** both controlled pairs from WS-E 72 — force-push
    and `branch -D`, each in plain and prefixed form, all four required
    to REFUSE — plus **one probe per named global option**, `-c`,
    `--git-dir`, `--work-tree` and `--no-pager`, because the finding
    proved `-C` and named the class without testing the others. Every
    probe must return the guard's own refusal text verbatim; **git's own
    error is a BYPASS result, not a pass.** Plus the WS-E 73 pair: a
    read with `2>&1` must execute, and a genuine write to a protected
    path must still refuse. Detail:
    `docs/governance/FINDINGS_2026-08-17_guard-bypass-ADDENDUM_fix-spec.md`.
43. **Reconcile the no-bare-`cd` convention with the guard's command
    patterns — NEW 2026-08-17, OPEN, and it is to be TESTED rather than
    reasoned about.** WS-E 72's reach comes from two individually
    correct conventions combining into a hole: the corrective written
    after WS-E 68 requires addressing by absolute path, and for git that
    is `git -C <path>`, which is exactly the form the deny patterns
    cannot see. **Neither convention is to be reversed on argument.**
    The reconciliation is a decision about which form the harness uses
    for git and what the guard must therefore match, and it is settled
    by running the pairs under each candidate form rather than by
    deciding which reading is more natural. Interim practice adopted
    2026-08-17 without waiting for the ruling: plain `git …` from the
    repo-root working directory, which involves no `cd`, satisfies the
    convention, and is the form the guard can see. Recorded as interim
    practice, not as the answer. Related: WS-E 68, WS-E 72, item 42.
<!-- QUEUE-END -->

## Orientation for a new session

Run `/session-open` first. Then: `START_HERE.md` → `DECISIONS.md` (rulings R1–R13, DEC
series, ADRs) → `BUILD_TRACKER.md` (next unpassed gate) → the newest
`docs/governance/SESSION_HANDOVER_*.md`, whose boot line is the current state of play.
`CURRENT_STATE.md` and `SESSION_PROTOCOLS.md` both lag current practice — treat the
latest handover as authoritative where they disagree.
