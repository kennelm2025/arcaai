# ArcaAI — Governance Checkpoint 01 — ROUND 3 (convergence)

*Identical text to both reviewers. Round 2 converged on all
substantive items; two residuals have been resolved by chair ruling
below. Round 3 task: one-line **CONCUR** or **DISSENT** per numbered
item (dissent with a one-sentence reason). Dissents are recorded in
the checkpoint outcome document; they do not block ratification.
No new findings this round unless something below is factually wrong.*

---

## Chair rulings on the two Round 2 residuals

**CR-1 — Cadence backstop.** The reviewers swapped positions in
Round 2 (ChatGPT moved to "2 gates OR 6 weeks"; Grok moved to
"2 gates, no time bound"). Ruling: **the 6-week backstop stays.**
Grounds: research-heavy stages stall silently — B6 sat at 4-of-5
increments for several days with no governance visibility. The
calendar backstop is exactly the control that catches a stalled
gate, and costs nothing when gates flow. Cadence: **every two closed
gates OR every six weeks, whichever comes first.**

**CR-2 — Safety-trio severity language.** Grok's "Observation until
B8" and ChatGPT's "Must-Fix before first external exposure" are
functionally identical. Ratified wording: the safety trio (prompt-
injection detection, PII detection/redaction, grounding verification)
is a **Must-Fix exit criterion of B8 AND a hard precondition for any
external exposure or demonstration, whichever comes first.**

## Chair findings entering the record at this round

**CF-1 — Architecture-conformance gap.** No control checks
conformance of the built system to the locked Banking Architecture
and ADRs; WS-A/B/C audited the decision system, one boundary, and
document currency respectively, and gates check functional evidence
only. WS-E 34 (contract mismatch invisible to three layers of green
unit tests) is the proof instance. Disposition: forward-looking
control, not retrospective audit — a second standing gate-checklist
question ("Does this increment conform to the BA and applicable
ADRs? → Yes / Deviation recorded as DEC / New ADR required") added in
the same edit as CL-08's question; spot-check at the B7 gate.
Retrospective B1–B6 conformance audit rejected as gold-plating.

**CF-2 — Chair actions executed this checkpoint (for confirmation):**
(a) CL-08 executed — gate checklist gains the decision-capture
question (and the CF-1 conformance question in the same edit);
(b) CL-10 double entry corrected — phantom open entry resolved;
(c) DEC-0008 gains a one-sentence reversibility note (artefact-store
move reversible; deployment-endgame decision remains PARKED).

---

## Ratification list

**RAT-01 · Must-Fix · Schedule integrity.** Week model abandoned.
Gate-based tracking becomes the official schedule: current gate,
next gate, entry/exit criteria, actual completion dates. One-time
variance note recorded against the original plan. *(R1-G-02 /
R1-CGPT-01 / R2 both)*

**RAT-02 · Should-Fix, before B7 · Governance trio.** Prompt/response
audit logging; immutable execution metadata (model, graph, prompt,
conversation IDs + versions); deterministic request-validation
wrapper. *(R2-G-01 / R2-CGPT-02)*

**RAT-03 · Per CR-2 · Safety trio.** Injection detection, PII
detection/redaction, grounding verification — B8 Must-Fix exit
criterion and hard precondition for any external exposure.
*(R1-G-01 as amended / R2-CGPT-03)*

**RAT-04 · Should-Fix · Gate Acceptance Record.** Half-page section
added to the gate document template: gate ID + date; evidence list
(links/hashes); producer statement; approver statement (same person
permitted, both statements mandatory); residual risks accepted into
next stage; dissent note; decision Pass / Conditional Pass / Fail;
approval date. Subsumes the residual-risk-statement finding.
*(R2-G-05 / R2-CGPT-04 + S5 both)*

**RAT-05 · Should-Fix, before B8 · AI threat catalogue.** One page.
Headings per Round 2: prompt manipulation, retrieval poisoning,
hallucination, provenance failure, information leakage, unsafe tool
invocation. Drives B8 guardrail test design. *(R2-CGPT-05, Grok
concurring via S2)*

**RAT-06 · B8 artefact · Guardrail precedence hierarchy.** One-page
"which control wins" decision hierarchy, written as the first
artefact of B8 once the retrieval surface exists. *(CGPT-04, Grok
timing amendment accepted)*

**RAT-07 · B8 exit criterion · Model-risk artefacts.** Model
inventory entry, validation plan skeleton, audit-trail schema —
mandatory at B8 exit, not before. *(Grok omission (c), ChatGPT
timing amendment accepted)*

**RAT-08 · Rule · Reversibility sentence.** Whenever a technical
decision executes ahead of a parked strategic decision, the DEC
records reversibility in one sentence. DEC-0008 retro-annotated per
CF-2(c). *(R2-CGPT-06)*

**RAT-09 · Rule · Ledger consistency check.** Governance ledger
consistency check (no duplicate/contradictory CL states) as part of
checkpoint preparation. *(R2-CGPT-07 / R2-G-03)*

**RAT-10 · Process rules ratified.** (a) Ship-critical git one
command per prompt; (b) written boarding checklist ticked against
git status. Ratified as written. WS-E items 30–34 closed as "trialled
and ratified". Backfill rider (items 1–23) retained. WS-E ledger is a
first-class in-repo artefact under code commit discipline. *(Q4,
unanimous)*

**RAT-11 · Backlog verdict.** Healthy; nothing rotting on real ages.
CL-08 closed (chair action, CF-2a). CL-10 phantom entry fixed
(CF-2b). CL-17/19/20 BA-revision bundle confirmed with hard trigger
at post-B8. CL-09 (Model Card) executes before any external review.
Remaining items stay parked as scheduled. *(S3/S4 both)*

**RAT-12 · Cadence DEC.** Per CR-1: standing programme checkpoint
every two closed gates OR six weeks, whichever first. Exceptional
triggers (any one fires an unscheduled checkpoint): gate failure;
new ADR changing platform/vertical boundary or model-risk surface;
any change to deployment target or artefact store; external
engagement requiring FCA/PRA-facing artefacts; WS-E incident rated
ship-critical or higher; any scheduled external exposure, demo, or
external audit request. To be recorded as a DEC on ratification.
*(S4/S5 merged lists)*

**RAT-13 · Panel composition.** Grok + ChatGPT adequate for
engineering/process checkpoints. Regulatory/Model Risk seat
reinstated from the B8 gate and for all FCA/PRA-facing artefacts.
Research-tooling seat remains parked. *(Q7, unanimous)*

**RAT-14 · Trajectory.** Build order B7 → B8 → B9 → B9.5 confirmed
unchanged. Build resumes at B7 after the WS-D Build & Quality Plan
session, which absorbs CF-1 (conformance control) and carries CL-10's
successor obligations. *(Q1, both, as amended by RAT-02/03)*

---

**Response format:** RAT-01..14 and CF-1..2, each with CONCUR or
DISSENT (+ one sentence). Anything factually wrong in this pack,
state it plainly.
