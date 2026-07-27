# SESSION HANDOVER — ArcaAI (close of 2026-07-25, evening session)

*Supersedes SESSION_HANDOVER_2026-07-25. That handover opened this
session; this one closes the day. **RAT-02 trio BUILT and MERGED; all
five B7 entry criteria MET.** Four PRs merged (#35 hotfix, #36 trio,
#37 addendum repair, #38 chromadb pin). Next session opens with B7
entry sign-off — the first stage entered under the full RAT-01 regime.*

## Boot line (paste to resume)

> Resume ArcaAI — trio landed (PR #36, `b07eba0`), chromadb==1.5.9
> pinned (PR #38, `8a5696a`), all five B7 entry criteria met.
> **NEXT: confirm the closeout-pack edits to B7_GATE.md and
> WS-E_INCIDENTS.md are aboard, fix `repo_manifest.py` gate-state
> logic, sign B7 entry in `docs/build/B7_GATE.md`, then open the
> stage: corpus manifest schema first (time-versioned eligibility is
> the hard part), then retrieval adapter behind an interface
> (CF-1/B7-a: chromadb imported in ONE module only).** Boot ritual:
> conda activate `arcaai` → git switch main → git pull --ff-only →
> git fetch --prune → `python scripts/repo_manifest.py` and attach
> REPO_MANIFEST.md → check `D:\Downloads\_staging` exists before any
> capture (WS-E 52). Docker Desktop must be started by hand before
> `dev_up.cmd` — the script cannot start the daemon itself.
> **PENDING COMMIT from the late-evening session:** CL-23 draft
> (`docs/governance/CL-23_policy-as-code.md`, new) and the updated
> `GOVERNANCE_REVIEW_CHANGELOG.md` — land them with the sign-off PR.

## What was done (25 Jul, evening)

- **PR #35** — hotfix: unused `sys` import in `scripts/repo_manifest.py`
  (F401) left by the `--out` change; found because ci-devops #58 failed
  on main post-merge. Root cause: the scripts tree was absent from
  ci-devops PR triggers — WS-E 45's class, second exhibit; trigger
  fixed in #36.
- **PR #36 — RAT-02 governance trio, the session's substance.**
  `arcaai/platform/governance/` (wrapper.py, metadata.py, audit.py,
  events.py, models.py); four append-only Postgres tables; runtime
  role SELECT+INSERT only via `sql/governance_grants.sql` (grant
  enforced by test, in CI, against a service Postgres); typed emit
  contract — allowlist by construction, definition-time field-name
  denylist, 256-char ceiling, `emit_ref` content-addressed payload
  store (CL-21 crypto-shred enabler); UUIDv7 correlation ids;
  sequence-number ordering; terminal record in `finally` on all three
  exit paths; span-based nesting. 24-test suite (spec section 7 in
  full) green locally and in CI, and verified from outside the repo
  root per the B5 precedent. Rode with: **DEC-0013** (package path
  `arcaai/platform/` — top-level `platform/` collides with the stdlib
  in both directions, verified empirically; NOT an ADR-0009 boundary
  change, only its address); the spec addendum (path correction +
  four-table terminal record — a single-row open-then-close design
  needs UPDATE, which the append-only grant deliberately excludes);
  and the **ci-devops hardening** — postgres:16 service with
  in-pipeline role bootstrap mirroring local dev, plus trigger paths for the
  arcaai, sql and scripts trees.
- **PR #37** — spec addendum markdown repair. The Notepad paste of the
  addendum carried rendered text, not source: heading, list numbering,
  bold and separator stripped, leaving it reading as ratified
  Review-disposition text. Wording unchanged; structure restored.
  Noted in the PR: ci-docs bold-parity passed the malformed version
  because the markers were wholly absent rather than half-terminated —
  a check_docs candidate (structural integrity of addendum sections),
  observed, not raised as a CL.
- **PR #38** — `chromadb==1.5.9` hard-pinned; import verified from
  outside the repo root (prints 1.5.9 from `D:\`). Hard pin over the
  house floor, deliberately: retrieval latency is CF-1/B7-d evidence
  and must not move under a silent version bump.
- **Defect caught pre-delivery by the suite's own raw-SQL assertion:**
  SQLAlchemy JSONB serialises Python `None` as JSON `null` — a
  sentinel passing `IS NOT NULL`. Fixed with `none_as_null=True`;
  WS-E 49.
- **Late evening — Executive Presentation v12** built: v11 design
  preserved; two new slides (Auditability Delivered; Built for the
  Regulatory Ground) translating the trio and regulatory posture into
  executive language; status slide rewritten to July 2026 reality
  (six gates, 33ms scoring, audit machinery live); dates and appendix
  corrected (SQLite→PostgreSQL 16, ChromaDB pinned→OpenSearch path).
  Marketing asset, not a repo artefact — register per CL-22's
  document-currency lens when circulated.
- **CL-23 drafted** (policy-as-code extended to the governance layer;
  three-tier framing; sole pre-B8 build consequence is
  `policy_version` in execution metadata). DRAFT pending panel
  review; changelog entry written; **both files uncommitted** — see
  boot line.
- **WS-E 49–52 entered** (ORM/SQL divergence; truncated-paste class
  with the per-block length-check rule; unexecuted verification
  numbers, generalising item 37; `_staging` browser-default
  recurrence). Standing-principle derivations extended accordingly.

## Environment changes

- `pyproject.toml`: added `uuid6>=2024.7.10` (UUIDv7 backport until
  py3.14 — one-line swap to stdlib then) and `chromadb==1.5.9`;
  `[tool.setuptools] packages` gained `arcaai`, `arcaai.platform`,
  `arcaai.platform.governance`.
- Postgres (docker dev stack): roles `arcaai_owner` / `arcaai_app` and
  database `arcaai_audit` created. Governance-suite conftest DSNs
  default to the dev passwords; overridable via
  `ARCAAI_AUDIT_OWNER_DSN` / `ARCAAI_AUDIT_APP_DSN`.
- CI: ci-devops now runs a postgres:16 service with role bootstrap
  identical to local dev; the governance suite (including the
  grant-denial tests) executes pre-merge on every PR touching the
  arcaai, sql, scripts or tests trees, or pyproject.toml.

## Carried to next session

1. **Fix `repo_manifest.py` gate-state logic before or with entry
   sign-off.** Flagged at this morning's boot and still open: it
   derives state from BUILD_TRACKER alone and will report B7 as
   "NOT STARTED — to be created at entry" while `docs/build/B7_GATE.md`
   exists with 5/5 criteria met. The boot artefact must not
   contradict the gate regime it serves. Fix: check gate-doc file
   existence and emit three states (passed / entered, gate doc open /
   not started).
2. **Sign B7 entry** in `docs/build/B7_GATE.md` (sign-off deliberately
   left as the opening act of the stage, per DEC-0010's
   entry-not-retrospective principle).
3. **B7 build order suggestion:** corpus manifest schema (dated
   eligibility transitions — the section 3 item hardest to retrofit) →
   retrieval interface with a single-module chromadb adapter
   (CF-1/B7-a) → `retrieval_performed` emits via the trio (CF-1/B7-c)
   → grounding and negative tests → confidence threshold + fallback →
   RAGAS baseline. **Explicit pinned embedding function from the first
   line — never chromadb's default** (silent ONNX download at first
   `add()`; recorded at B7_GATE section 2.1).
4. **CL-23 follow-through:** commit the two files (boot line); panel
   review before B8 entry; `policy_version` metadata note any time
   before B8 (nullable-until-available, no schema change); scope
   statement into the B8 design brief with CL-18; principle addition
   joins the CL-21 principle in the BA revision bundle.
5. **Open riders, unchanged:** WS-E 1–23 backfill; `decisions/` →
   `adrs/` rename (named backlog); locked-suite disk sprawl purge;
   CL-17/19/20/21/22 bundle → next Banking Architecture revision
   (hard trigger post-B8, RAT-11; CL-21 pulled forward if a pilot is
   scheduled); CL-09 before any external review; G10 external
   reviewers (priority raised, still no date); prompts/ scaffold
   decision → B8; coverage sources exclude `arcaai/` — parked as a
   deliberate open question, revisit at B7 close.
6. **Minor:** `docs/governance/~$caAI_Banking_Architecture_v1_0b.docx`
   Word lock file still committed — the `~$*` gitignore line and
   `git rm --cached` never landed this session; the
   `reviews/2026-06-arch-review/1739140963936 (1).gif` download-suffix
   duplicate remains.

## Regulatory watchlist

Unchanged from the morning handover: UK GDPR Articles 22A–22D
(in force 5 Feb 2026, favours the platform, claim to be made explicit
via CL-21); SS1/23 scope precision; FCA audit-trail /
human-in-the-loop guidance expected during 2026 (RAT-12 trigger on
publication); CTP designations expected from HM Treasury during 2026.

## Environment

`arcaai` conda env (py3.11.15). Docker Desktop manual start →
`dev_up.cmd` (Postgres 16 + MLflow). `gh` CLI still not installed;
GitHub web/Desktop remains the PR route. Governance suite:
`pytest tests\governance -q` (24 tests; needs the dev stack up).

## Governance state

**WS-A/B/C/D CLOSED** · B1–B6 gated · **B7 entry criteria 5/5 MET —
sign-off next session** · DEC through **0013** · ADR through 0010 ·
CL open backlog: 06, 07, 09, 11, 16, 17, 18, 19, 20, 21, 22, 23 (draft) ·
**WS-E in-repo at 52** (items 1–23 backfill rider open) · Two standing
principles, derivations extended by items 50–52 · Next checkpoint:
B8 gate or 2026-09-04, whichever first (DEC-0009).
