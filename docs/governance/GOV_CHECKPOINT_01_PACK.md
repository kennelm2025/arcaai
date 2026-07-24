# ArcaAI — Programme Governance Checkpoint 01 (July 2026)

**Status:** Pack drafted 2026-07-24 — for panel circulation at next session
**Chair / decider:** Mike Kennelly
**Coordinator:** Claude
**External reviewers:** ChatGPT, Grok (DeepSeek excluded — prior citation
fabrication)
**Position in plan:** run as "WS-D part 0" — programme-level review
preceding and shaping the WS-D Build & Quality Plan session
**Trigger:** none — and that is itself finding zero. The governance
system is event-driven (per-workstream, per-ADR, per-gate) with no
programme-level cadence. This checkpoint exists because the chair asked
"when was the last one?" and the honest answer was "never, as such."

---

## Part 1 — State summary (for panel context)

### 1.1 Build status

| Stage | Scope | Status | Evidence |
|---|---|---|---|
| B1–B4 | Foundation → calibrated fraud MVM | GATE PASSED (Jun 2026) | tracker + gate history |
| B5 | BentoML serving + contracts | GATE PASSED (Jul 2026) | G9: P99 ~33ms vs 200ms |
| B6 | LangGraph agent v0 + Llama 3.1 8B | **GATE PASSED (24 Jul 2026)** | docs/build/B6_GATE.md — warm max 4.10s vs 15s SLA; true cold 7.41s |
| B7 | Fraud RAG (ChromaDB, RAGAS) | NOT STARTED | — |
| B8 | Guardrails (Presidio, OPA, grounding, injection detector) | NOT STARTED | — |
| B9 | Chat UI + audit-trail replay | NOT STARTED | — |
| B9.5 | Platform Extraction (ADR-0009) | NOT STARTED | exit = 2nd vertical consumes, not copies |

Schedule honesty: the plan's week column has B6 at weeks 4–5 of the
build; the calendar says the build began early June and it is now late
July. The week model has never been re-baselined. Panel question Q2.

### 1.2 Governance state

- WS-A (decision system), WS-B (platform/vertical boundary), WS-C
  (specs currency) — CLOSED. WS-D (Build & Quality Plan; carries CL-10)
  — next, was deliberately parked behind the B6 gate, now unblocked.
- Decision registers: DEC-NNNN (build/design, DECISIONS.md, through
  DEC-0008) and ADR-NNNN (formal architecture, through ADR-0009) —
  namespace separation ratified WS-A, holding.
- WS-E process-incident ledger: in-repo, 34 items. Two rules trialled
  this week and both caught/prevented real failures: (a) ship-critical
  git one command per prompt; (b) written boarding checklist ticked
  against git status. Proposed for ratification.
- Open CL backlog: CL-06..09, CL-11, CL-16..20. CL-17/19/20 flagged as
  a bundle for the next Banking Architecture revision. CL-08
  (decision-capture gap) has an accumulating evidence pile.

### 1.3 Recent material events (since last panel round, ~2 Jul)

- B5 closed and gated; B6 built across five increments and gated.
- First live graph↔LLM↔scoring end-to-end run caught a provenance key
  mismatch invisible to unit tests on an invented canned fixture
  (WS-E 34; fixed; fixtures consolidated to mirror live shape).
  Instructive failure: three layers of green unit tests, defect on
  first contact between layers.
- WS-E ledger discovered to have never been committed to the repo
  (lived only in handover documents); now in-repo with backfill rider.
- DVC default remote switched to AWS S3 (DEC-0008) aligning artefact
  store with target-customer estates; platform-endgame decision
  (AWS as deployment target) remains PARKED.

## Part 2 — Panel prompt

*Circulate Part 1 plus repo access (or excerpts) with the following.
Three-round protocol as per house standard; Round 1 below.*

You are reviewing ArcaAI at programme level — not a single decision or
document, but whether the programme as a whole is healthy, honest with
itself, and pointed at the right next risks. ArcaAI's product claim is
a defensible, auditable governance trail a bank's Model Risk function
can read; treat this checkpoint as that reviewer would. Be adversarial
where warranted. Findings with severity (Must-Fix / Should-Fix /
Observation), each with the smallest proportionate remedy — this is a
solo-founder build and gold-plating is itself a programme risk.

**Q1 — Trajectory.** Given the state summary: is the build sequence
(B7 RAG → B8 guardrails → B9 UI → B9.5 extraction) still the right
order? Specifically: should any part of B8's guardrails be pulled
earlier now that a live LLM emits governed prose (B6), or is the
current CI-stubbed posture acceptable until B8?

**Q2 — Schedule honesty.** The week model is stale. Recommend: re-baseline
(and to what), replace with gate-cadence-only tracking, or retain as
aspiration with a recorded variance note. What would a bank reviewer
make of a plan whose calendar column is silently fictional?

**Q3 — Backlog health.** Review the open CL list (CL-06..09, 11,
16..20) with ages. Which items are quietly rotting versus legitimately
parked? Is the CL-17/19/20 → BA-revision bundle right? Should CL-08
(decision-capture) now execute rather than accumulate evidence?

**Q4 — Process-rule ratification.** WS-E items 30–34 and the two
trialled rules. Ratify, amend, or reject each. Also: the ledger itself
was never in-repo until this week — what does that say about the
handover-document-as-archive pattern, and is the backfill rider
(items 1–23) worth its cost?

**Q5 — Risk look-ahead.** B7 introduces retrieval (grounding risk),
B8 the guardrail stack, B9.5 the extraction that every future vertical
inherits. Name the top three programme risks for the next two gates
and what evidence at those gates would retire them.

**Q6 — Governance cadence (meta).** This is checkpoint 01 and it was
ad hoc. Propose a standing cadence (per-N-gates or per-N-weeks),
scope, and a trigger list for exceptional checkpoints. To be recorded
as a DEC on ratification.

**Q7 — Panel composition.** Recent rounds ran Grok + ChatGPT only; the
original charter listed a wider panel including a dedicated regulatory
reviewer (Mistral) and research tooling. Confirm the slimmed panel or
argue for reinstating seats — noting B8 (guardrails) and any future
FCA/PRA-facing artefacts are where a regulatory seat would earn keep.

**Out of scope:** individual ADR contents (reviewed at their own
gates); MyBank/PwC engagement (separate ethical wall); anything
requiring the locked suite to reopen outside the CL-17/19/20 bundle.
