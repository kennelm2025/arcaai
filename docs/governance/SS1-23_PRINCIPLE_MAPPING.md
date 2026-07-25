# SS1/23 principle mapping — B8/B9 artefact set

**Status: RATIFIED 2026-07-25. Working input to B8 and B9 design.**

*WS-D item 4, the last open item in the workstream. Superseded once the
obligations below are folded into `B8_GATE.md` and `B9_GATE.md` at their
entry. Gap decisions recorded as DEC-0012.*

*Reviewed: ChatGPT and Grok, both concur. Disposition at §8.*

---

## 1. Purpose

WS-D item 4 asks which planned B8 and B9 artefacts provide evidence
against which SS1/23 principle, so the artefacts are built toward a
named expectation rather than mapped to one retrospectively. The
mapping feeds the B8 and B9 gate documents at entry, as CF-1
nominations do.

It is also the honest version of a claim the suite currently makes
loosely: "SS1/23 alignment" appears in the operative regulatory set
without a line-by-line account of what actually evidences it.

## 2. Scope precision — get this right in front of a client

SS1/23 came into force on 17 May 2024. Two facts are routinely
conflated and the platform should not conflate them:

- **Firm scope is narrow.** The expectations apply to UK-incorporated
  banks, building societies and PRA-designated investment firms **that
  hold internal model permissions for regulatory capital** (IRB, IMA or
  IMM). Firms without those permissions are not in scope; the PRA says
  they may find the principles useful and are welcome to apply them.
- **Model scope inside an in-scope firm is wide.** It is not limited to
  capital models. The Bank of England has confirmed the principles
  reach all models wherever used in the bank, explicitly including
  fraud.

So for a client bank: **if they hold IM permissions, a fraud model is
in scope of SS1/23.** If they do not, the principles are voluntary —
though widely adopted as the de facto benchmark, and firms outside
scope are choosing to apply them.

The platform's claim must be scoped accordingly. Saying "SS1/23
requires this" to a bank without IM permissions is wrong and will be
corrected in the room by someone who knows. The defensible claim is
narrower and stronger: *the platform produces the evidence a firm needs
to satisfy the principles where they apply, and the principles are
becoming the benchmark whether or not a given firm is formally in
scope.*

This language belongs in the next Banking Architecture revision, with
the CL-17/19/20 bundle.

## 3. The mapping is evidential, not declarative

**The mapping identifies which platform artefacts provide evidence
supporting a firm's compliance with the SS1/23 principles. It does not
claim that producing those artefacts alone satisfies the principles,
because governance responsibilities remain with the deploying firm.**

That sentence governs everything below, and the wording throughout §4
follows it: an artefact *provides evidence supporting* a principle. It
never *satisfies* one. Principles attach to firms; evidence is what a
platform can supply.

Same structure as CL-21, for the same reason. The obligations sit with
the bank and the platform cannot discharge them. What it can do is make
them cheap to discharge by producing artefacts a Model Risk function
would otherwise assemble by hand.

| The platform supplies | The bank owns |
|---|---|
| Per-model provenance, lineage and performance evidence | The model inventory and its maintenance |
| A risk-tiering record per model | The tiering policy and thresholds |
| Validator-ready documentation and reproducible results | The independent validation function itself |
| Monitoring signal and drift detection | Risk appetite and escalation thresholds |
| A record of every adjustment and override | Who is permitted to make them |

**Principle 4 is intentionally different from the other four.** It
depends on organisational independence rather than platform capability,
and no artefact changes that. It is treated separately at §4 and the
distinction is deliberate rather than an omission.

## 4. Principle-by-principle mapping

### Principle 1 — Model identification and model risk classification

*Firms need a clear model definition, a comprehensive inventory, and
risk-based tiering by materiality, complexity and purpose.*

- **Provides evidence supporting it:** RAT-07 model-risk tiering record
  (B8 exit, record-only per step-change candidate 3). Provenance
  manifest (CL-12) supplies per-artefact identity. Execution metadata
  (ADR-0010) records which model actually ran, which is the thing an
  inventory claims and rarely proves.
- **Gap — no model inventory artefact.** The provenance manifest is
  per-artefact and generated at build. It is not an inventory: it does
  not enumerate the models in the platform, their versions, tiers,
  lifecycle state or dependencies. SS1/23 puts the inventory first, and
  firms report it as the hardest first step. The platform is unusually
  well placed to generate one, which makes it a differentiator rather
  than a compliance chore. **Adopted — see §5, Gap 1.**

### Principle 2 — Governance

*Comprehensive governance and oversight; board and senior management
accountability; responsibility allocated to an SMF holder.*

- **Provides evidence supporting it:** the gate apparatus —
  entry-written gate documents, the Gate Acceptance Record with
  mandatory producer and approver statements, the ADR and DEC
  registers, the CL ledger, CF-1 conformance nominations.
- **Bank-side:** SMF allocation, board reporting, audit committee
  reporting on MRM effectiveness. The platform supplies evidence into
  these; it cannot hold them.
- **Note:** the Gate Acceptance Record's producer/approver split
  already anticipates a separation of duties a solo build cannot
  provide. It is honest as written — both statements mandatory,
  same-person explicitly permitted — and becomes meaningful unchanged
  the moment there are two people.

### Principle 3 — Model development, implementation and use

*Documented design, theory and logic; data sources, methodology,
performance testing, limitations; detailed enough that an independent
third party can understand the model and replicate its results.*

The strongest area, and worth being concrete about why.

- **Provides evidence supporting it:** B3 anti-leakage suite (shuffle
  test, planted-leak control, source audit, future-blindness). B4
  walk-forward validation across six folds with per-fold calibration,
  the December flag narrated rather than suppressed. Platt calibration
  with MAE recorded. CL-13 promotion gate blocking on parity, contract,
  calibration and provenance. CL-09 model card. B9 replay exhibit.
- **The replication expectation is the sharp one.** SS1/23 expects
  documentation sufficient for an independent third party to replicate
  results. For the tabular model that is met — DVC-pinned artefacts,
  seeded training, content-hash provenance. For the LLM path it is not,
  and cannot be. **The B9 nondeterminism register is the Principle 3
  replication answer** and must be labelled as such in `B9_GATE.md`, so
  a reviewer without the internal history can see what it is for. Not
  an admission: the disciplined statement of where replication holds,
  where it does not, and what bounds the difference. Bounded
  reproducibility, claimed accurately, is a stronger position than
  reproducibility claimed loosely.

### Principle 4 — Independent model validation

*Validation independent of development, with authority to escalate.*

- **Structurally different, and named as such (§3).** A solo build
  cannot supply independence. No artefact fixes this, because
  independence is an organisational property rather than a documentary
  one.
- **What the platform can do** is make independent validation cheap
  once the bank supplies the independence: reproducible pipelines,
  pinned artefacts, the validation suite as executable tests rather
  than a written report, the promotion gate as a mechanical check a
  validator can run themselves, and the replay exhibit.
- **G10 external domain reviewers** — one per vertical, the
  programme's longest-lead open item — are the nearest approximation to
  independence available before a client engagement. This mapping
  raises their priority: they are currently an open item with no date,
  and they are the only pre-client evidence against Principle 4.
- **Claim discipline, permanent:** the platform must never be described
  as satisfying Principle 4. It supplies validator-ready material. This
  statement is to be carried into the Banking Architecture and the
  model-risk artefacts, not left in this working document. It is the
  first thing a Model Risk reviewer will test.

### Principle 5 — Model risk mitigants

*Post-model adjustments, overrides, monitoring, and controls where
model risk cannot be eliminated — with adjustments justified and
recorded.*

- **Provides evidence supporting it:** B8 guardrails (Presidio, OPA,
  grounding, injection detection) with block and redaction reasons in
  the audit trail. B9 `outcome_event` table — the SS1/23 monitoring
  argument that made it non-deferrable under DEC-0010. B11 drift
  detection and the kill-switch drill. The B7 confidence threshold and
  insufficient-evidence fallback.
- **Gap — no adjustment or override record.** SS1/23 places significant
  weight on expert judgement applied to model output and requires such
  adjustments to be justified and recorded. ArcaAI has no artefact
  representing a human overriding a model decision: the audit trail
  records what the system decided, and has nowhere to record that a
  person disagreed and why. The same missing artefact is what UK GDPR
  Article 22C's human-review right needs (CL-21), and what the Learning
  Bank's overridable-decision claim assumes. **Adopted — see §5,
  Gap 2.**

## 5. The two gaps, adopted

Both recorded as **DEC-0012**. Each is a scope addition to a stage
defined in the locked Build & Quality Plan and therefore needs a DEC on
the same basis `outcome_event` did under DEC-0010.

### Gap 1 — Generated model inventory, at B8 exit

A **generated, record-only** artefact produced at B8 exit from inputs
that already exist: the provenance manifest (CL-12) and the RAT-07
tiering record. One row per model:

`model_id · version · artefact_sha256 · tier · lifecycle_state ·
last_validated · dependencies`

**Lifecycle state is part of it from the outset:** `active`,
`deprecated`, `retired`, `withdrawn`, `archived`. An inventory without
retirement states becomes wrong the first time a model is replaced, and
retiring a model is exactly the event an inventory exists to record.
This is the same discipline as B7's time-versioned corpus eligibility —
a state that changes must be recorded as a transition, not overwritten.

**Explicitly not** a maintained inventory with owners, approval
workflow or status transitions driven by people. That is bank-side.
The platform generates the table; the bank owns the register.

Placement resolves an apparent disagreement between reviewers: one
recommended deferring to B10 *unless implementation is genuinely almost
free*, the other recommended B8 exit. At B8 exit both inputs exist, so
generation is a script reading two files — the condition is met, and
B8 is the answer to the test rather than a competing view.

### Gap 2 — `adjustment_event`, non-deferrable B9 exit item

The stronger of the two. One artefact closes three things: SS1/23
Principle 5's expert-judgement expectation, UK GDPR Article 22C's
right to human review, and the Learning Bank's claim that decisions are
overridable with the override in the audit trail.

Shape only — the DEC settles the record, not the workflow:

`correlation_id · original_decision · adjusted_decision · actor_id ·
actor_role · justification · timestamp`

**`actor_role` is a controlled vocabulary, not a free field:**
`system`, `reviewer`, `approver`, `override_authority`. "Actor" alone
is too generic — banks distinguish who reviewed from who approved, and
under SM&CR accountability attaches to a named individual in a named
role. A record that cannot tell a reviewer from an approver cannot
evidence the separation the bank is claiming.

Append-only, joinable to the run on correlation id, same discipline as
`outcome_event`. Human-override UI and workflow remain deferred.

Without this the platform can show what the system decided but not that
a person disagreed and why — a visible gap against both a regulatory
expectation and a data-protection right the architecture already claims
to support.

## 6. What this changes in the gate documents

- **B8 entry:** generated model inventory added to exit evidence
  (record-only, not gate-blocking). CF-1 nominations to include a P1 or
  P5 claim. RAT-07 tiering already listed.
- **B9 entry:** `adjustment_event` contract and table as a
  non-deferrable exit item, alongside `outcome_event`. The
  nondeterminism register explicitly labelled as the Principle 3
  replication answer.
- **CL-17/19/20 bundle:** §2 scope precision and the §4 Principle 4
  claim-discipline statement both belong in the next Banking
  Architecture revision.

## 7. Standing artefact or one-time input

**One-time input, folded into the gate documents.** A standing SS1/23
matrix maintained alongside the build is exactly the kind of parallel
document that drifts from the thing it describes — the failure RAT-01
§2 exists to prevent. The gate documents carry the obligations; this
document is the working that produced them and is superseded once B8
and B9 gate documents exist.

## 8. Review disposition

- **"Serves Principle X" → "provides evidence supporting Principle X"
  (ChatGPT) — ADOPTED throughout.** Correct and cheap. Principles
  attach to firms; evidence is what a platform supplies. The original
  wording would have been read as a compliance claim.
- **Evidential-not-declarative statement (ChatGPT) — ADOPTED as
  written (§3).** Taken close to the proposed wording; it governs the
  whole document and protects it.
- **Principle 4 stated as intentionally different (ChatGPT) —
  ADOPTED (§3).** Heads off the reading that its treatment is an
  omission.
- **`actor` too generic (ChatGPT) — ADOPTED, extended (§5).** Split
  into `actor_id` plus `actor_role` from a controlled vocabulary. The
  SM&CR point makes this more than a naming preference: accountability
  attaches to a named individual in a named role.
- **Model retirement / lifecycle states (ChatGPT) — ADOPTED (§5).**
  An inventory without retirement states is wrong the first time a
  model is replaced. Noted as the same discipline as B7's
  time-versioned corpus eligibility.
- **Gap 1 placement — RESOLVED, no conflict.** ChatGPT: defer to B10
  unless almost free. Grok: B8 exit, generated and lightweight. Both
  inputs exist at B8 exit, so the condition is satisfied; B8 it is.
  Grok's constraint that it stays generated rather than maintained is
  adopted and made explicit.
- **Gap 2 as non-deferrable B9 exit item via DEC (Grok) — ADOPTED.**
  Both reviewers ranked this the stronger proposal, as did the
  coordinator.
- **Residual citation markup in Principle 1 (Grok) — FIXED.**
- **G10 priority raised (Grok) — ADOPTED (§4, P4).**
- **Claim-discipline statement made permanent (Grok) — ADOPTED
  (§4, P4).** Carried to the Banking Architecture rather than left in a
  working document.
