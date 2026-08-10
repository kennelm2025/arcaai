# TERMS OF REFERENCE — ArcaAI Test Capability Build-Out

Covering: Test Plan | Test Operations | Test Reporting
Drafted 8 Aug 2026 (from Claude chat). Status: Rev C RULED 2026-08-10 — panel pass complete (3 reviewers, ACCEPT WITH AMENDMENTS), operator rulings recorded in RULINGS_RECORD_2026-08-10_TOR-test-capability.md. Working document; proceed per Section 9.
Rev A (8 Aug 2026): AWS sequencing annex added (Section 11); open questions updated.
Rev B (10 Aug 2026): retrieval evaluation named as scenario batch 1 (B7 exit evidence vehicle); sequencing inverted to proof-first (runner spike before Test Plan/panel); ONNX pre-flight check folded into runner (discharges parked CLAUDE.md authoring debt); dependencies refreshed post batch-2 completion; recommendations recorded against Open Questions 1 and 4.
Rev C (10 Aug 2026): Section 5A Test Governance added — two-regime model (commissioning vs formal execution), commissioning frame for the spike, admissibility rule (spike results are NOT gate evidence), governance pack contents assigned to the Test Plan. Acceptance criteria and sequencing updated to carry the frame.
Rulings (10 Aug 2026, post-panel): OQ1 ruled (DEC-0015); OQ3 ruled (preferred-primary); OQ4 ruled (formal hard gate); nine amendments accepted onto D1.1/D2.1 requirements. Section 10 annotated below; full record in the rulings record file.

## 1. PURPOSE

Establish a governed, repeatable test capability for ArcaAI comprising:
(a) an authored Test Plan interrogated by the external SME panel;
(b) a cross-platform Test Operations harness runnable via script (CLI-first) and later via dashboard;
(c) a Test Reporting layer producing citable, hash-anchored evidence for B-gate reviews and prospect demos.

The capability's FIRST cargo is B7 exit evidence: retrieval evaluation over the authored synthetic corpus, including detection of the two deliberate under-implementations (D1, D2) planted as gap-detection ground truth. Serving-side behavioural regression (scoring, latency) is the second cargo, extending the B5 gate lineage.

## 2. BACKGROUND & CONTEXT

- Builds on existing assets: B2 synthetic fraud data generator, anti-leakage test suite, BentoML serving layer, B5 latency gate precedent (P99 33ms PASS), corpus edge-check tooling, deliberate under-implementations as gap-detection ground truth.
- Corpus status at Rev B: batch 2 complete (SG-03..09, PR #80, 2026-08-10); 23 of 54 documents authored (16 pre-existing + TY-03..09 + SG-03..09). Retrieval evaluation can begin on the authored 23 and re-run as batches land — the corpus snapshot in the reproducibility triple makes each run citable against its exact corpus state.
- Extends the gate discipline from latency into retrieval quality and behavioural regression testing.
- Scenario content may be LLM-assisted (Grok/DeepSeek/Claude) at the DESIGN layer only; all volume data is produced programmatically by the in-house generator from versioned specs. External model outputs are treated as distinct provenance lines, schema-validated before pipeline entry, and hash-pinned.
- Steady-state home of the regression pack is AWS post-migration; build and baseline occur pre-migration (see Section 11).

## 3. SCOPE

IN SCOPE
- Test Plan document: coverage matrix per vertical, fraud typologies, RETRIEVAL SCENARIO CLASSES (corpus QA, citation-following, gap detection vs D1/D2 ground truth), pass/fail criteria, data provenance rules, gate linkage, and the FORMAL-EXECUTION GOVERNANCE PACK per Section 5A. Binding requirements from the 2026-08-10 rulings record (amendments 1-4, 9) apply at authoring.
- Scenario spec schema (versioned YAML/JSON): scenario class (retrieval | scoring), vertical, typology, parameter ranges, expected outcomes, acceptance thresholds. The schema MUST support corpus-snapshot-anchored retrieval scenarios from v0.1, define gap-detection scoring mathematically, carry generator_seed for scoring-class scenarios, and declare per-scenario migration-diff comparison semantics (bit-identical vs defined tolerance) — per rulings-record amendments 3, 5, 6.
- Runner core: single Python entry point (arcaai conda env, Python 3.11.15) — spec in, synthetic data materialised or corpus queried, scored/evaluated, machine-readable results out. Headless/CLI-first; CI-able via GitHub Actions.
- Runner pre-flight: environment preconditions asserted before any run — non-elevation assertion, ONNX/chromadb cache traversal check, Docker/service availability, conda env identity. Pre-flight failure exits non-zero immediately and blocks all downstream steps (rulings-record amendment 7). NOTE: this gives the ONNX cache check (currently a named procedure in CLAUDE.md and session-open/SKILL.md with NO implementing artefact) its real implementation, discharging the parked authoring debt (CL-26 candidate). The pre-flight is a standalone invocable script so ceremony skills can call the same artefact.
- Schema validation gate for any externally generated spec content.
- Results ledger: append-only, keyed by spec hash + model version + corpus snapshot (+ generator_seed where the generator is invoked).
- Reporting: human-readable run summaries; static HTML dashboard reading results JSON (read-only skin over CLI output).
- Demo scenario packs: curated spec sets for prospect demonstrations.
- Pre/post-migration regression diff (Section 11).

OUT OF SCOPE (this TOR)
- FastAPI "run-from-dashboard" wrapper (deferred until CLI stable; noted as follow-on).
- Production monitoring/observability.
- Real (non-synthetic) data of any kind.
- AWS migration itself (separate workstream; this TOR defines only the harness's touchpoints with it).

## 4. WORKSTREAMS & DELIVERABLES

WS-T1: TEST PLAN
- D1.1 Draft Test Plan authored in Claude Code session against the repo (reads actual test suite + gate history + the working runner spike per D2.2a). Carries the formal-execution governance pack (Section 5A) as a first-class section, and implements rulings-record amendments 1-4 and 9 (operational invalidation/re-test rules; D1/D2-detection vs retrieval-quality distinction; migration-diff semantics reference; the ruled B7 evidence relationship; explicit defect routing).
- D1.2 Structured for panel ruling: explicit sections, accept/reject format per batch-1 convention.
- D1.3 Optional blind-spot check: one external model produces a test-category checklist, diffed against draft (no parallel authored plan).
- D1.4 Panel circulation, rulings recorded, outcomes circulated. Circulation includes the spike's first real results, marked COMMISSIONING (panels interrogate better with a working artefact in front of them).

WS-T2: TEST OPERATIONS
- D2.0 COMMISSIONING FRAME (one page, ruled by operator before any run): session objective, entry criteria, exit criteria, records rule, and the admissibility rule per Section 5A. Held to one page by ruling (amendment 8) — it must not grow into a miniature Test Plan. Nothing executes without it.
- D2.1 Scenario spec schema v0.1 (the keystone artefact; everything else hangs off it). Must carry both scenario classes from v0.1 and the schema requirements from amendments 3, 5, 6.
- D2.2a RUNNER SPIKE: minimal runner + pre-flight + ONE retrieval scenario end-to-end (spec in, corpus queried at pinned snapshot, result JSON out). Runs under the D2.0 commissioning frame, pinned to the corpus snapshot current at spike time (amendment 9). This is the proof-first milestone and precedes the Test Plan.
- D2.2b Runner core hardened to full CLI: python -m arcaai.harness run --spec <file>.
- D2.3 Schema validation gate for any externally generated spec content.
- D2.4 GitHub Actions job running the scenario suite per PR.
- D2.5 Results ledger (append-only) wired into house ledger/manifest disciplines. Every entry carries its regime marker (commissioning | formal) per Section 5A.
- D2.6 Pre-migration baseline run: full scenario suite executed on current environment, results ledger captured and hash-pinned (migration comparison anchor). Formal-regime run; requires the ruled Test Plan. FORMAL HARD PRECONDITION to serving-layer cutover, per Ruling 4.

WS-T3: TEST REPORTING
- D3.1 Machine-readable results artefact (JSON) per run, carrying the regime marker.
- D3.2 Human summary format for session notes and gate evidence.
- D3.3 Static HTML dashboard v0.1: scenario grid, pass/fail, drill-down to run artefact. No server dependency. Commissioning-regime results visually distinguished from formal.
- D3.4 Demo pack rendering: curated scenario folder + dashboard view.
- D3.5 Migration diff report: pre vs post-AWS suite comparison at identical spec hashes and corpus snapshot, applying each scenario's declared comparison semantics (amendment 3). Formally reviewed before migration is declared complete, per Ruling 4.

## 5. GOVERNANCE & DISCIPLINES

- All artefacts enter via governed acts: authoring and listing separated; ledger/manifest append-only; SHA256 hash-pinning on transfers.
- Reproducibility triple mandatory on every result: spec hash + model version + corpus snapshot (+ generator_seed for scoring-class scenarios).
- Register linkage: decisions via DEC series, architecture choices via ADR series, work items via WS-E ledger (respect sequence-hold rule). Harness register home: DEC-0015 per Ruling 1.
- External AI usage: design-layer only; provenance logged per model; fabrication risk mitigated by schema validation (per DeepSeek CL-23 precedent).
- Compliance framing: synthetic data only; scenario narratives to avoid any real-institution identifiers.

## 5A. TEST GOVERNANCE (added Rev C)

PRINCIPLE
No run executes without a governance frame, and no run counts as evidence without the ruled one. Two regimes, and every run belongs to exactly one, marked in its ledger entry and result artefact:

REGIME 1 — COMMISSIONING (applies to D2.2a and any run before the Test Plan is ruled)
Purpose: prove the harness mechanism. Results say nothing about the system under test and are INADMISSIBLE as gate evidence — permanently, not merely until ruled. A commissioning result cannot be promoted retroactively; a scenario whose result is wanted as evidence is re-run under Regime 2. (This bars the failure class WS-E 63 records: a green read as meaning something it cannot mean.)
Frame per commissioning session (D2.0, ruled by operator before first run):
- Session objective: stated in one sentence (e.g. one retrieval scenario end-to-end at pinned snapshot).
- Entry criteria: pre-flight green (non-elevation, cache traversal, services, env identity); corpus snapshot pinned and stated; spec schema-valid; working tree state recorded.
- Exit criteria: result JSON produced and reproducible from its triple. The scenario's own pass/fail is NOT an exit criterion — commissioning proves plumbing, not the system.
- Records: run artefact ledgered with regime marker COMMISSIONING; anomalies observed-not-raised into the session record.

REGIME 2 — FORMAL EXECUTION (any run intended as evidence: B7 gate, migration baseline/diff, regression)
Precondition: the Test Plan ruled ACCEPTED by the panel process, carrying the formal-execution governance pack:
- Entry criteria per session: environment asserted via pre-flight; corpus at a LISTED snapshot (post listing-act pin); spec versions ruled; model version stated; no unconsumed suspension in force.
- Exit criteria per session: all scheduled scenarios executed or their non-execution recorded with reason; results ledgered; summary produced.
- Suspension and resumption criteria: what halts a session (pre-flight red mid-run, environment drift, corpus/model version change mid-session) and what re-entry requires (fresh pre-flight, re-pinned triple).
- Session objectives and scope: each formal session names its scenario set and purpose before execution; additions mid-session are a new session.
- Defect classification and routing: harness defects to WS-E ledger; system-under-test findings to CL register or the relevant build-stage evidence; corpus defects (a scenario failing because the corpus is wrong) to the corpus rulings process. One defect, one home.
- Evidence admissibility: only Regime 2 runs meeting their entry criteria at ruled spec versions are citable as gate evidence. Reproducibility triple mandatory. A run with a failed or skipped pre-flight is inadmissible regardless of outcome.
- Re-test and regression rules: what corpus or model movement invalidates which prior results, and what must re-run — stated operationally in the Test Plan per rulings-record amendment 1.
RULING AUTHORITY: the operator rules the commissioning frame (D2.0) directly; the formal-execution pack is ruled through the Test Plan panel process (D1.4). Amendments to either after ruling are themselves governed acts.

## 6. ROLES

- Author/Owner: Mike (solo founder) with Claude Code as build agent.
- Reviewers: external SME panel (Grok, Gemini, DeepSeek, Mistral, clean Claude session) — interrogation role, not authorship. Reviewer outputs are concurrence and recommendation only; all effective rulings are the operator's (restated after the 2026-08-10 pass, where one reviewer phrased outcomes as rulings).
- Ruling authority: Mike, recorded via panel outcome circulation. Test governance ruling split per Section 5A.

## 7. DEPENDENCIES (refreshed at Rev B, 10 Aug)

- Docker availability for any serving-layer-dependent runs. Retrieval scenarios depend on the vector store; the pre-flight (D2.2a) asserts its health before any run.
- Batch-2 authoring COMPLETE (PR #80). Remaining corpus queue items sequenced alongside, not blocking: batch-end panel circulation of SG-03..09, listing transitions (MANIFEST.yaml, eligible 16 -> 23, new corpus pin), operator inclusion decision for TY-03..09. NOTE: retrieval scenarios should pin to the corpus snapshot CURRENT at spike time; the eligible-23 pin lands with the listing act and FORMAL runs use listed snapshots only (Section 5A Regime 2 entry criteria).
- gh CLI authenticated for CI wiring.
- CLAUDE.md and harness ceremonies in place (DONE — /session-open, /pr-prep, /ledger-touch, render-abort class fixed per WS-E 63).
- AWS migration workstream (for Section 11 items only; harness build does NOT wait on it).

## 8. ACCEPTANCE CRITERIA (TOR-LEVEL)

- GOVERNANCE CRITERION (zeroth): the D2.0 commissioning frame is ruled before any run executes; every ledgered result carries its regime marker; no commissioning result appears as gate evidence anywhere.
- SPIKE CRITERION (first): one retrieval scenario runs end-to-end from spec file to results JSON at a pinned corpus snapshot, pre-flight green, under the commissioning frame, on the local environment. This precedes and informs the Test Plan.
- Test Plan ruled ACCEPTED by panel process, including the formal-execution governance pack (Section 5A Regime 2) and the rulings-record amendment requirements.
- One full scenario (each class) runs end-to-end from spec file to dashboard-rendered result on both Windows PowerShell and Linux CI.
- Gap-detection scenarios demonstrate detection (or recorded non-detection with analysis) of D1 and D2 ground truth — as Regime 2 runs, evidencing gap-detection capability distinctly from general retrieval quality (amendment 2).
- Every result reproducible from its triple (spec hash / model version / corpus snapshot, + generator_seed where applicable).
- Zero mutations to append-only stores outside sanctioned append paths (hook-enforced).
- Pre-migration baseline captured before any serving-layer redeployment to AWS.

## 9. SEQUENCING (Rev C — proof-first, governance-framed)

1. Commissioning frame D2.0 ruled (one page, operator ruling — minutes, not days).
2. Spec schema v0.1 (D2.1) — keystone, both scenario classes, amendment requirements 3/5/6 in from the start.
3. Runner spike + pre-flight + one retrieval scenario end-to-end (D2.2a) under the commissioning frame. FIRST REAL TEST RESULT LANDS HERE — days, not weeks.
4. Test Plan draft (D1.1–D1.2), informed by the working spike, carrying the formal-execution governance pack and amendments 1-4, 9.
5. Panel circulation + rulings (D1.4), spike results included in the pack marked COMMISSIONING.
6. Runner hardening + validation gate (D2.2b–D2.3).
7. Results ledger + reporting formats (D2.5, D3.1–D3.2).
8. CI job (D2.4).
9. Dashboard v0.1 + demo pack (D3.3–D3.4).
10. Pre-migration baseline run (D2.6) — Regime 2; formal hard gate before AWS serving-layer cutover per Ruling 4.
11. Post-migration re-run + diff report (D3.5) on AWS.
All of steps 1–9 execute locally / GitHub Actions and do NOT wait for AWS.

## 10. OPEN QUESTIONS — RULED 2026-08-10

Full record: RULINGS_RECORD_2026-08-10_TOR-test-capability.md (docs/governance/). Summary:
- OQ1 Register home: RULED — DEC-0015 under the existing structure; no new workstream ID. (Unanimous panel concurrence.)
- OQ2 Scenario batch 1: RESOLVED at Rev B, confirmed — retrieval over the fraud corpus (B7 exit evidence); scoring follows as batch 2. (Unanimous.)
- OQ3 B7 evidence relationship: RULED — PREFERRED-PRIMARY. Harness Regime-2 runs against the ruled Test Plan are the preferred primary evidence for retrieval quality and D1/D2 gap detection; not a hard single-point dependency where equivalent citable evidence exists by another governed route. (Panel divergent — hard-requirement vs preferred-primary; operator adopted preferred-primary; rationale in the rulings record.)
- OQ4 Migration diff gate: RULED — D2.6 baseline is a formal hard precondition to serving-layer cutover; D3.5 diff formally reviewed before migration declared complete. (Unanimous.)
- OQ5 Naming: deferred, unruled. Trivial; carries.

## 11. ANNEX A — AWS SEQUENCING

PRINCIPLE
The harness is environment-agnostic (Python CLI, spec files in, JSON out). Its steady-state home as a scheduled regression pack is AWS post-migration, but its build, baseline, and proving all occur pre-migration. Deferring the build until after migration would (a) couple two large workstreams so testing inherits every migration delay, (b) forfeit the pre-migration baseline forever, and (c) confound harness, migration, and infrastructure debugging into one pile.

MIGRATION ROLE
The regression pack is itself migration tooling: identical suite run pre- and post-cutover at the same spec hashes and corpus snapshot, results diffed per scenario under each scenario's declared comparison semantics. Comparable pass/fail at identical inputs = migration acceptance evidence (same bit-identical-comparison discipline as the MyBank v1d98b neutral-composite check, where determinism permits).

BUILT NOW (LOCAL / GITHUB ACTIONS)
- Commissioning frame, spec schema, runner spike, test plan, panel review, runner hardening, validation gate, results ledger, CI job, dashboard v0.1, demo packs, pre-migration baseline (D2.6).

WAITS FOR AWS
- IAM roles / networking / secrets handling for the runner in AWS.
- Scale and latency scenarios requiring production-shaped infrastructure.
- Scheduled (cron/EventBridge) regression runs.
- Post-migration re-run + diff report (D3.5).

GATE STATUS
RULED 2026-08-10 per Ruling 4: D2.6 baseline formal hard precondition to serving-layer cutover; D3.5 diff report formally reviewed before migration is declared complete.
