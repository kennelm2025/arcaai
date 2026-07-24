# Governance Checkpoint 01 — Working Papers

*Verbatim reviewer outputs, all rounds, captured 24 Jul 2026 by the
coordinator. Circulation packs are the ROUND1/ROUND2/ROUND3 documents
in this folder. Outcome: GOVERNANCE_CHECKPOINT_01_outcome.md.*

*Capture note: Round 1 outputs were initially pasted unlabelled and a
duplicate of Grok's Round 1 nearly entered the record as ChatGPT's
independent review; caught by coordinator text comparison before any
cross-analysis ran. Logged as a WS-E candidate (labelling rule for
panel captures).*

---

# 1. GROK — ROUND 1

**1. Answers to Q1–Q7**

**Q1 — Trajectory.**
The sequence B7 (Fraud RAG) → B8 (Guardrails) → B9 (Chat UI + audit-trail replay) → B9.5 (Platform Extraction) remains directionally correct for a solo-founder build, but is no longer fully acceptable once B6 has placed a live LLM in the path that emits governed prose.

A bank Model Risk function will treat any live LLM emission as a model-output risk surface. CI-stubbed posture is acceptable for pure unit/integration tests; it is not acceptable for any end-to-end path that leaves the developer's machine or is shown to stakeholders. Minimum viable guardrails that must be pulled forward before further B6 work or any external demonstration:
- prompt-injection / jailbreak detector on every inbound user message,
- Presidio-style PII detection + redaction on every outbound prose response,
- basic grounding check (even if only "response must cite a scored feature or decision key").

Full OPA policy engine, RAGAS evaluation suite and comprehensive injection corpus can stay in B8. Pulling the three minimal controls now is low-cost and directly protects the product claim of a defensible audit trail. Deferring them creates a period in which the system can generate ungoverned text that later has to be retrospectively justified.

**Q2 — Schedule honesty.**
A bank reviewer will treat a calendar column that is silently fictional as a control failure. Model Risk and Internal Audit expect either (a) an honest re-baseline or (b) explicit abandonment of time-based tracking in favour of the event-driven gate model already in use. Silent variance is worse than admitted slip because it destroys the ability to demonstrate controlled delivery.

Recommendation: replace the week model with gate-cadence-only tracking effective immediately. Record a one-time variance note against the original plan (B6 landed ~6–7 weeks later than the week column implied) and close the week model. Retain the gate artefacts (G9, B6_GATE.md etc.) as the sole schedule evidence. This is the lowest-cost, highest-credibility posture for a solo founder and aligns with the already event-driven governance system.

**Q3 — Backlog health.**
Without explicit age or last-touched dates the list cannot be fully aged, but the numbering and the statement that CL-08 is "accumulating evidence" allow a clear triage:
- Quietly rotting risk: CL-06, CL-07, CL-09, CL-11 (lower numbers, no mention of recent activity). These should be either closed with a one-line rationale or given an explicit next action and owner date.
- Legitimately parked: CL-16 and the CL-17/19/20 Banking Architecture bundle — the decision to hold them for a single BA revision is sound provided the revision itself has a hard trigger (post-B8 or post-B9.5).
- Must execute now: CL-08 (decision-capture gap). An accumulating evidence pile for a gap in the decision system itself is self-defeating. The product claim is "defensible, auditable governance trail". Leaving the capture mechanism incomplete while the trail is being written is the highest-priority backlog item. Execute a minimal decision-capture remediation (template + mandatory fields + single source of truth) before or in parallel with the next gate.

**Q4 — Process-rule ratification.**
- Rule (a) "ship-critical git one command per prompt": ratify as written. It caught a real failure; cost is near zero.
- Rule (b) "written boarding checklist ticked against `git status`": ratify as written. Same evidence of value.
WS-E items 30–34 (the ones that produced the two rules) should be closed as "rules trialled and ratified".

The fact that the entire WS-E ledger lived only in handover documents until this week is a material process finding. Handover-as-archive is fragile under solo-founder conditions and creates an un-auditable gap. The backfill rider for items 1–23 is worth the modest documentation cost; it restores a continuous evidence chain. Going forward, the ledger must be treated as a first-class in-repo artefact with the same commit discipline as code.

**Q5 — Risk look-ahead.**
Top three programme risks for the next two gates (B7 and B8):

1. **Grounding / retrieval integrity (B7).** Fraud RAG can surface incorrect, incomplete or adversarial context that the agent then presents as authoritative.
   Gate evidence that retires the risk: RAGAS faithfulness + context-precision scores above a pre-declared threshold on a held-out adversarial set; explicit demonstration that every agent claim is traceable to a retrieved chunk + score key.

2. **Guardrail completeness and bypass (B8).** Incomplete coverage of injection, PII leakage, policy violation or ungrounded prose allows the system to emit outputs that cannot be defended to Model Risk.
   Gate evidence: red-team corpus (injection, PII, policy-violation cases) with zero escapes; OPA policy coverage metrics; Presidio false-negative rate on banking-style PII.

3. **Platform extraction inheritance lock-in (B9.5, but the design decisions that will be frozen are taken in B7/B8).** Any structural debt or missing control introduced now becomes the baseline every future vertical inherits.
   Gate evidence: a written "consumption contract" that the second vertical must satisfy without copying code; explicit list of what is platform vs vertical-specific, reviewed at the B8 gate.

**Q6 — Governance cadence (meta).**
Standing cadence: every two closed gates or every six calendar weeks, whichever comes first. Scope identical to this checkpoint (state summary + Q1–Q7 style questions + findings).

Exceptional triggers (any one fires an unscheduled checkpoint):
- any gate failure,
- any new ADR that changes platform/vertical boundary or model-risk surface,
- schedule variance that would have moved a gate by more than one cadence interval,
- external engagement that requires FCA/PRA-facing artefacts,
- any WS-E incident rated "ship-critical" or higher.

Record the cadence and trigger list as a formal DEC on ratification of this checkpoint.

**Q7 — Panel composition.**
The slimmed panel (Grok + ChatGPT) is adequate for pure engineering and process checkpoints while the work remains internal. It is not adequate once B8 (guardrails) and any future FCA/PRA-facing artefacts appear. A dedicated regulatory / Model Risk seat (originally Mistral or equivalent) should be reinstated for B8 gate and all subsequent checkpoints that touch policy, audit trail or regulatory narrative. Research-tooling seat can remain parked. The cost of a single additional reviewer on the two or three highest-stakes gates is trivial compared with the credibility gain when a bank Model Risk function examines the governance trail.

**2. Findings list**

**R1-G-01** — Severity: Must-Fix
Finding: Live LLM (B6) can emit governed prose with only CI-stubbed guardrails. This creates an ungoverned output surface that is inconsistent with the product claim of a defensible audit trail readable by a bank Model Risk function.
Smallest proportionate remedy: Implement the three minimal controls listed in Q1 (injection detector, Presidio PII redaction, basic grounding citation check) as a pre-condition for any further B6 demonstration or external exposure. Full B8 stack remains as planned.

**R1-G-02** — Severity: Must-Fix
Finding: The week-based schedule column is silently fictional. A bank reviewer will treat this as a control failure.
Smallest proportionate remedy: Issue a one-time variance note, abandon the week model, and switch permanently to gate-cadence-only tracking (see Q2).

**R1-G-03** — Severity: Must-Fix
Finding: CL-08 (decision-capture gap) is allowed to accumulate evidence while the decision system itself is incomplete. This directly undermines the core product claim.
Smallest proportionate remedy: Execute a minimal remediation (mandatory decision template + single source of truth) before or in parallel with the next gate; close the "accumulate evidence" posture.

**R1-G-04** — Severity: Should-Fix
Finding: WS-E process-incident ledger lived only in handover documents until this week, creating an un-auditable historical gap.
Smallest proportionate remedy: Complete the backfill rider already started; treat the ledger as a first-class in-repo artefact with the same commit rules as code going forward. Ratify the two trialled rules (Q4).

**R1-G-05** — Severity: Should-Fix
Finding: No standing programme-level governance cadence exists; checkpoints are ad-hoc. This is the root cause of "finding zero".
Smallest proportionate remedy: Adopt the cadence and exceptional-trigger list in Q6; record as a DEC.

**R1-G-06** — Severity: Observation
Finding: Lower-numbered open CLs (06, 07, 09, 11) have no visible recent activity or explicit parking rationale.
Smallest proportionate remedy: One-line close-or-park decision for each before the next gate; no further work required if the rationale is recorded.

**R1-G-07** — Severity: Observation
Finding: Panel composition is currently under-weight for the regulatory/Model Risk scrutiny that B8 and later artefacts will attract.
Smallest proportionate remedy: Reinstate a regulatory seat for the B8 gate and any subsequent FCA/PRA-facing work (Q7). No change required for pure engineering gates.

**3. Material omissions or obscurities in the state summary**

- No ages, last-touched dates or explicit "parked until" statements are given for the open CL list. Without them a bank reviewer cannot distinguish rotting items from deliberately deferred ones.
- Gate evidence is cited only by filename (B6_GATE.md, G9). No summary of residual risks, test coverage, or known limitations is provided; a Model Risk function will expect that residual-risk statement.
- No mention of whether any threat model, abuse-case catalogue or model-risk taxonomy has been started for the LLM agent. The first live end-to-end failure (provenance key mismatch) is exactly the class of defect a threat model would have been expected to surface earlier.
- The platform-endgame decision (AWS deployment target) remains PARKED while the DVC remote has already been moved to S3. The summary does not state whether this creates any reversible or irreversible coupling.
- No statement of current model-risk artefact readiness (e.g., whether a model inventory entry, validation plan skeleton or audit-trail schema exists). These are the artefacts a bank Model Risk function will ask for first.

---

# 2. CHATGPT — ROUND 1

Understood. I will review this as if I were sitting on a Tier 1 bank's Architecture Review Board, Model Risk Committee, and Internal Audit function—not as a general AI reviewer.

That means I will assess against principles such as:

* PRA/FCA expectations (or equivalent ECB/OCC governance principles)
* SR 11-7 model risk management concepts
* Enterprise Architecture governance
* SDLC governance
* Auditability and evidence
* Change management
* Operational resilience
* Three Lines of Defence
* Proportionality (avoiding unnecessary process for a solo founder while ensuring the design can survive scrutiny in a large bank)

Importantly, I will **not** try to make the project "more enterprise" for its own sake. Banks reject programmes just as often because they are over-engineered as because they are under-governed.

# Overall assessment

**Governance maturity: 8.8/10**

This checkpoint reads like something between an engineering governance review and a lightweight programme assurance review. It is significantly stronger than most startup AI governance documentation.

The biggest positive is that the programme has evolved into an **evidence-based governance system** rather than a document-based governance system. That distinction matters enormously inside banks. What banks eventually trust is evidence that decisions were made deliberately, tested, and recorded—not beautifully formatted documents. The checkpoint demonstrates that philosophy consistently.

# Q1 — Build trajectory

**Retain the overall sequence.** B7 → B8 → B9 → B9.5 remains correct. I would **not** reorder the major work packages. However, I would pull **three B8 controls forward immediately.** These are not "guardrails" in the LLM sense. They are governance controls. Those are different things.

### Pull forward immediately

1. **Prompt/Response audit logging.** Every prompt and response should already be captured. Not because of security. Because future investigations depend on reconstructing behaviour. Without this, reproducing defects becomes extremely difficult.

2. **Immutable conversation identifiers.** Each conversation should already carry conversation_id, model version, prompt version, graph version, retrieval version (later). Those become part of audit evidence.

3. **Basic safety policy wrapper.** Not sophisticated guardrails. Just deterministic pre/post processing: reject malformed requests, reject oversized prompts, reject unsupported agent states, standard error responses. Those reduce operational risk immediately.

Everything else in B8 (Presidio, grounding verification, OPA etc.) can remain where planned.

**Conclusion:** No stage re-ordering. Pull only lightweight governance controls forward.

# Q2 — Schedule honesty

This is the strongest finding in the paper. A bank reviewer will immediately notice this. The issue is **not schedule slippage.** Large programmes slip constantly. The issue is: the published plan knowingly contains inaccurate information. That is a governance issue. Not a planning issue.

My recommendation: **Remove week numbers entirely.** Replace with Current Gate, Next Gate, Planned Entry Criteria, Planned Exit Criteria, Actual completion dates. This aligns much better with iterative delivery. Trying to estimate "Week 11" for research-heavy AI work is largely fiction. Banks increasingly recognise this. The gates are already the real governance mechanism. Let them become the official schedule.

**Finding severity:** Must Fix.

# Q3 — Backlog health

Overall health appears good. Nothing suggests uncontrolled governance debt.

- **CL-17/19/20:** Bundling into one Banking Architecture revision is correct. Reopening architecture repeatedly is expensive. One controlled revision is preferable.
- **CL-08:** Decision capture has crossed the threshold. The evidence has accumulated sufficiently. At this point continuing to gather evidence produces diminishing returns. Execute.
- **Other CL items:** Without their contents I cannot assess technical urgency. Nothing in the summary suggests hidden governance failures.

# Q4 — Process-rule ratification

- **Rule 1 (one git command per prompt): Ratify.** Not because Git requires it. Because human error scales non-linearly under cognitive load. Excellent example of operational learning.
- **Rule 2 (written boarding checklist): Ratify.** This is classic aviation practice. Banks increasingly use similar operational checklists. Very low cost. High value.
- **WS-E ledger:** The fact that it lived in handover documents reveals an architectural smell. Knowledge existed. Repository evidence did not. That creates audit risk. The move into the repository is absolutely correct.
- **Backfill rider:** I would retain it. Future auditors often ask "When was this governance process introduced?" The rider preserves historical continuity. Low maintenance cost. High audit value.

# Q5 — Top programme risks

1. **Retrieval provenance.** This becomes the single largest technical risk after B7. Evidence required: citation accuracy, retrieval determinism, provenance completeness, hallucination measurement.
2. **Policy inconsistency.** Multiple guardrail layers can disagree (LLM → OPA → Grounding → Prompt policy → Business rules). Need a clear precedence hierarchy. Evidence: decision tree showing which policy wins.
3. **Platform extraction.** B9.5 risks creating accidental coupling. Evidence required: second vertical should consume platform services without modification. That is the true exit criterion. Not simply "code moved into another folder."

# Q6 — Governance cadence

Current approach: event-driven. Good. Missing: strategic rhythm. Recommendation: major checkpoint every two gates (B6, B8, B9.5...). Exception checkpoint triggers immediately if: architecture rewritten, governance process changed, model class changes, external regulation changes, major incident, security issue, deployment target changes. Those are governance events. Not engineering events.

# Q7 — Panel composition

Current panel (ChatGPT + Grok) is adequate today. However, by B8 I recommend reinstating an explicit regulatory perspective. Not because another model is "smarter." Because different review personas identify different classes of defect. The value comes from diversity of review lenses: Architecture, Engineering, Model Risk, Regulatory Compliance. Those are genuinely different disciplines. I do **not** think you need a large panel. Four perspectives is sufficient.

# Additional findings

**R1-CGPT-01 — Must Fix.** Replace fictional week-based schedule with gate-based programme tracking. Proportionate remedy: remove week numbering and publish gate progress with actual completion dates.

**R1-CGPT-02 — Should Fix.** Introduce immutable conversation metadata immediately. Remedy: every execution records model version, graph version, prompt version, conversation id. No additional governance process required.

**R1-CGPT-03 — Should Fix.** Move prompt/response audit logging into B6 baseline. Remedy: persist interactions before B7 begins.

**R1-CGPT-04 — Should Fix.** Define guardrail precedence before implementation. Remedy: one-page decision hierarchy showing which control has authority in conflict scenarios.

**R1-CGPT-05 — Observation.** Evidence-driven governance has become one of the programme's strengths. Protect this. Avoid replacing it with documentation-heavy governance.

# What the state summary omits

The checkpoint discusses governance decisions extensively, but says almost nothing about **acceptance authority**. A bank reviewer will eventually ask: Who is authorised to approve a gate? What evidence is mandatory? Can the same individual both produce and approve evidence? What constitutes a failed gate versus a conditional pass? How are dissenting reviewer opinions recorded?

For a solo-founder project this does not require introducing artificial bureaucracy. However, it does require making the governance mechanics explicit. Even if the chair performs multiple roles, the documentation should clearly distinguish when you are acting as builder, reviewer, or approver. That separation of roles, even if held by one person, strengthens the audit trail and makes the process easier for a future bank or independent reviewer to trust.

## Overall conclusion

I would classify this checkpoint as **ready to proceed**, subject to the single Must-Fix on schedule integrity. The governance approach is notably mature for a solo-built AI platform: it favours measurable evidence over process theatre, records lessons learned, and demonstrates that governance is influencing engineering decisions rather than documenting them after the fact. The next phase (B7/B8) is where the scrutiny will increase substantially, because that is where claims about explainability, provenance, safety, and regulatory defensibility begin to crystallise into capabilities that a Model Risk function or Internal Audit team would evaluate directly. If those stages are executed with the same discipline shown here, the programme will have a governance narrative that is credible to large-bank reviewers.

---

# 3. CHATGPT — ROUND 2

[Full text as captured 24 Jul: revised position that the safety and
governance control sets are complements gated by exposure — governance
trio (execution metadata, audit logging, request wrapper) Should-Fix
before B7; safety trio (injection, PII, grounding) Must-Fix before
first external exposure. Adopted the threat catalogue (one page,
before B8, R2-CGPT-05), the residual-risk statement per gate
(R2-CGPT-04), and Grok's six-week cadence backstop with a merged
trigger list. Pushed model-risk artefacts to a B8 exit criterion.
Ruled the S3-while-PARKED move consistent but requiring a recorded
reversibility sentence (R2-CGPT-06). Re-triaged the backlog on real
ages: nothing rotting; CL-08 chair action "exactly right, no
residue". Reframed the CL-10 duplicate as an evidence-integrity issue
warranting a pre-checkpoint ledger consistency check (R2-CGPT-07).
Acceptance authority sized as one Gate Authority section per gate
document, no new artefact. Findings R2-CGPT-01..07. Closing: one
Must-Fix remaining before continuing (schedule integrity), one
Must-Fix before any external exposure (basic AI safety controls);
everything else incremental hardening.]

---

# 4. GROK — ROUND 2

**S1 — The Q1 clash (safety vs governance controls)**
Given A4 (zero external users, zero demos, pure local Ollama), my original Must-Fix precondition on the three safety controls was overstated. Withdraw the "precondition for any further B6 work" framing.

The two sets are complements, not substitutes:
- ChatGPT's governance trio (prompt/response audit logging, immutable version metadata, deterministic request-validation wrapper) protects the *audit trail claim* and should be done now.
- My safety trio (injection detector, Presidio redaction, basic grounding citation) protects the *output surface* and remains correctly scoped to B8, except for the lightest possible logging of any unguarded emission so the trail remains complete.

Minimal combined set with honest severities:
1. Prompt/response audit logging + immutable version metadata + deterministic request-validation wrapper → **Should-Fix**, execute before B7.
2. Full injection / Presidio / grounding stack → remains **Observation** until B8 (or until any external exposure is scheduled).
No Must-Fix remains on the safety side while the system stays air-gapped to the developer machine.

**S2 — Precedence hierarchy (CGPT-04)**
Right in principle, premature in timing. A one-page "which control wins" hierarchy is useful, but writing it before B7 retrieval exists means inventing conflict cases that do not yet exist. Do it as the first artefact of B8, after the RAG surface is real. Ranking it higher now is gold-plating.

**S3 — Acceptance authority**
Concur fully. Even when one person holds every role, the mechanics must be explicit or the "defensible trail" claim is theatre.

Smallest artefact: a ½-page "Gate Acceptance Record" template containing only: Gate ID + date; Evidence list (links or hashes); Producer statement ("I built and tested"); Approver statement ("I accept / conditional / reject") — same person allowed, but the two statements must both be present; Residual risks + any dissent note; Decision (Pass / Conditional Pass / Fail). Add it to the existing gate checklist. One template, one mandatory fill-in. Nothing more.

**S4 — Q3 re-triage on real ages**
All open CLs are 3 days to ~3.5 weeks old. Nothing is rotting.
- CL-06 / CL-07 / CL-09 / CL-11 / CL-16 / CL-17 / CL-18: legitimately young, leave parked or scheduled as already planned.
- CL-08: now confirmed as a one-line checklist edit; chair will close it this checkpoint → closed.
- CL-19 / CL-20: brand-new, correctly bundled with the next BA revision.
- New defect from A3: CL-10 appears both open and closed. This is a ledger hygiene failure. Anyone grepping sees a phantom open item.
Triage conclusion: backlog is healthy; the only action required is a one-line ledger clean-up of the CL-10 double entry.

**S5 — Cadence merge**
Merged proposal for the Round 3 DEC:
Standing cadence: every two closed gates. No calendar backstop (ChatGPT's version is cleaner; a solo founder does not need the extra 6-week rule).
Exceptional triggers (any one fires an unscheduled checkpoint): gate failure; new ADR that changes platform/vertical boundary or model-risk surface; any change to deployment target or artefact store (explicitly includes the S3 move already made under DEC-0008 while the AWS endgame remains PARKED); external engagement requiring FCA/PRA-facing artefacts; WS-E incident rated ship-critical or higher; any scheduled external exposure or demo.
This is the single list to ratify.

**Revised / new findings (R2)**

**R2-G-01** (replaces R1-G-01) — Should-Fix. Governance controls on the live (local) LLM path are still missing: prompt/response audit logging, immutable version metadata, deterministic request-validation wrapper. Safety controls stay in B8. Remedy: implement the three governance controls before B7 starts. No safety Must-Fix while exposure remains zero.

**R2-G-02** (replaces R1-G-03) — Closed. CL-08 is a one-file checklist edit; templates and single source of truth already exist. Chair will execute during this checkpoint. Remedy: none further. Confirm closed at Round 3.

**R2-G-03** (new) — Should-Fix. CL-10 appears both open-unticked and closed-ticked in the ledger. Grep produces a false open item. Remedy: one-line ledger edit to remove the phantom open entry. Done.

**R2-G-04** (refined from R1-G-05) — Should-Fix. No standing cadence exists. Remedy: adopt the merged cadence + trigger list in S5; record as DEC at Round 3.

**R2-G-05** (refined from R1-G-07 / ChatGPT acceptance point) — Should-Fix. Gate acceptance mechanics (producer vs approver statements, residual risks, pass/conditional/fail) are not explicit. Remedy: add the ½-page Gate Acceptance Record template described in S3 to the existing checklist.

All other R1 findings stand or are superseded as above. No new Must-Fix items remain under the corrected exposure and CL data.

---

# 5. GROK — ROUND 3 (concurrence)

CF-1 CONCUR · CF-2 CONCUR · RAT-01 CONCUR · RAT-02 CONCUR ·
RAT-03 CONCUR · RAT-04 CONCUR · RAT-05 CONCUR · RAT-06 CONCUR ·
RAT-07 CONCUR · RAT-08 CONCUR · RAT-09 CONCUR · RAT-10 CONCUR ·
RAT-11 CONCUR · RAT-12 CONCUR · RAT-13 CONCUR · RAT-14 CONCUR ·
"Nothing factually wrong in the pack."

---

# 6. CHATGPT — ROUND 3 (concurrence)

CONCUR on all sixteen items (CF-1, CF-2, RAT-01..14) with commentary;
no dissents, no factual inaccuracies identified. Selected statements
for the record:

- CF-1: "the strongest addition made during convergence… closes the
  only governance gap that had the potential to become significant as
  the platform matures."
- RAT-12: "the best outcome reached during all three rounds. The
  six-week backstop protects governance during research-heavy periods
  without creating unnecessary overhead."
- Final: "CONCUR with the complete Round 3 convergence package… If
  this were a real bank governance board, I would be comfortable
  signing these ratifications and authorising progression to B7,
  subject to execution of the agreed pre-B7 actions (RAT-02 and
  associated chair actions)."
