# ADR-0010 — Platform governance instrumentation (request wrapper, execution metadata, audit logging)

**Status:** Accepted
**Decision Date:** 25 July 2026
**Recorded Date:** 25 July 2026
**Decision Type:** Contemporary
**Decider:** Mike Kennelly
**Supersedes:** none
**Related:** ADR-0003 (pipeline-as-platform), ADR-0009 (platform/vertical boundary), DEC-0010 (gate-based plan; `outcome_event` as a B9 exit item), CL-21 (data protection position), CL-08 (decision-capture gate question)
**Evidence:** `docs/governance/RAT-02_GOVERNANCE_TRIO_SPEC.md` (full specification, ratified 25 Jul 2026, with build addenda of 25 Jul and 27 Jul recording the package path, the terminal record as a fourth append-only table, and `policy_version` in execution metadata — recorded there by addendum rather than by edits to this ADR, per DEC-0013); WS-D session, one external reviewer concurring with three amendments; `docs/governance/WS-D_RAT-01_GATE_PLAN.md` §5 B7 (entry criterion this discharges on build)

> Status flips `Proposed → Accepted` at merge.

---

## Context

B5 and B6 produce governed decisions that leave no durable record. The
fraud score, its provenance, the retrieved evidence and the packaged
narrative exist in a process and then stop existing. Every governance
claim the platform makes downstream — audit-trail replay at B9, the
Article 22C right to contest under CL-21, model performance monitoring
under SS1/23 — rests on a decision record that does not yet exist.

The question is not whether to build it but when. Building it at B9,
where replay first needs it, means B7's retrieval and B8's guardrail
decisions are retrofitted into instrumentation designed after the fact.
Retrofitted instrumentation records what the author remembers to
record. Instrumentation written first records what happened, because
each stage is instrumented at the moment its author knows what matters.

This is also the first architecturally significant decision raised
prospectively under the CL-08 gate question ("what architecturally
significant decisions since the last gate?") rather than backfilled
after the fact, as ADRs 0005–0009 were.

## Decision 1 — The governance trio is platform infrastructure

Three components are built pre-B7 in `platform/governance/`:

- **Request wrapper** — mints a correlation id, captures execution
  metadata once, opens a run record before work begins, and guarantees
  a terminal record on every exit path including unhandled exception.
- **Execution metadata** — the reproducibility fingerprint of a run:
  code SHA, environment, model artefact hashes, LLM pin, and fields for
  prompt, corpus and retrieval configuration that are declared now and
  populated as B7 and B8 land.
- **Audit logging** — append-only `audit_run`, `audit_event` and
  `audit_payload` tables in PostgreSQL, ordered by a monotonic sequence
  number rather than timestamp.

These are platform-side per ADR-0009: audit logging is machinery, not
business semantics. It records that a decision was made and on what
basis without understanding what fraud is. Nothing in the trio may
import from `verticals/`. This is the first exercise of the ADR-0009
boundary against green-field rather than extracted code, and the
boundary test is mandatory evidence for the B7 CF-1 spot-check.

Provenance being entirely platform-level follows directly from
ADR-0009 Decision 1: a bank cannot tolerate provenance that differs by
business domain, and neither can it tolerate an audit record that does.

## Decision 2 — Personal data is excluded by construction, not by inspection

The emit interface accepts a **typed event object, not a free-form
dict**. Each event type has a declared payload model with named, typed
fields; a caller cannot pass a field outside the schema because there
is nowhere to put it.

This is the enforceable form of CL-21's prompt-minimisation rule. The
alternative considered and rejected — inspecting payloads at runtime
and rejecting values that look like personal data — cannot be
implemented: detection would operate on values, and no runtime check
distinguishes a name from any other short string. The result would be a
check that passes reliably and assures nothing.

Prompt and response text is stored by reference in a content-addressed
payload table, never inline in the event row. This is what makes
CL-21's crypto-shred mechanism possible: shred the payload table, keep
the decision records and their hashes intact, and the audit trail still
proves what happened without holding what was said.

`audit_run` carries an indexed `subject_ref`. This is the single item
in CL-21 with a build consequence, and it lands here rather than at B9,
because a column and an index now is a migration on a populated
append-only table later.

## Decision 3 — The audit schema and event enum are public contract

`schema_version` and the event-type enum are versioned artefacts that
later stages depend on. Adding an event type is a minor version bump.
Removing or renaming one, or changing the meaning or type of a payload
field, is a breaking change requiring a migration note and a DEC or ADR.

Without this, B9 can silently assume an event type that has since been
removed, and the failure surfaces as a replay that quietly omits a step
rather than as an error — the worst available failure mode for an
audit-trail component.

## Consequences

- **Positive.** Every governed decision from B7 onward has a durable,
  queryable, append-only record. B9's replay exhibit, nondeterminism
  register and worked trace are populated from this rather than
  reconstructed. B11's panels query these tables rather than a parallel
  metrics store.
- **CL-21 partially discharged in code.** The prompt-minimisation rule
  and the subject-retrieval requirement become enforceable platform
  properties at the moment the audit machinery is born, rather than
  paragraphs awaiting the next Banking Architecture revision. The
  retention, erasure and DPIA elements of CL-21 remain open.
- **Obligation.** Every stage from B7 emits through this interface.
  A stage that produces a governed decision without an audit event is a
  gate failure, not a style issue.
- **Platform-first discipline (ADR-0009 Decision 3).** The trio is new
  shared machinery and is therefore built platform-side from the
  outset, shrinking B9.5 when it arrives.
- **Interaction with DEC-0010.** The `outcome_event` contract and table
  remain a non-deferrable B9 exit item and are explicitly out of scope
  here. They join to these tables on correlation id.

## Alternatives considered

- **Instrument at B9, when replay first needs it** — rejected. B7 and
  B8 would be retrofitted into instrumentation designed after they were
  written, and the record would reflect what was remembered rather than
  what occurred.
- **Free-form payloads with runtime personal-data detection** —
  rejected as unimplementable (Decision 2). Detection on values cannot
  distinguish a name from any other string; the check would provide
  false assurance.
- **Per-vertical audit logging** — rejected. Follows directly from
  ADR-0009: provenance and the decision record cannot differ by
  business domain, or a bank's Model Risk function is auditing three
  different systems.
- **MLflow as the decision store** — rejected. MLflow is experiment and
  run tracking (ADR-0007 keeps it metadata-only and off the serving
  path); a decision record is a different artefact with different
  retention, query and immutability requirements.
- **File-based audit log** — rejected. B9 replay and CL-21 subject
  retrieval are both query problems; PostgreSQL has been running since
  B1.
