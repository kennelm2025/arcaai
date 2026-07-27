# RAT-02 — Governance trio specification

**Status: RATIFIED 2026-07-25 (ADR-0010). Build target: pre-B7.**

*WS-D item 3. On build, discharges the B7 entry criterion "RAT-02
governance trio landed as pre-B7 work". Formal decision record:
`decisions/0010-platform-governance-instrumentation.md`.*

*Reviewed: one external reviewer, concur with three amendments — two
adopted as written, one adopted with the mechanism replaced (§11).*

---

## 1. Why this is pre-B7, not part of B7

The trio is infrastructure the build has been running without. B5 and
B6 produce decisions that leave no durable record: the fraud score, the
retrieved provenance, the packaged narrative all exist in a process and
then stop existing.

The reason it must land *before* B7 rather than alongside it is
ordering. B7 adds a retrieval step; B8 adds guardrail decisions; B9
replays the lot. If the wrapper arrives after those, each has to be
retrofitted into it, and retrofitted instrumentation records what the
author remembers to record rather than what happened. Landing the trio
first means B7 and B8 are instrumented at the moment they are written,
which is the only time the author knows what matters.

Three components, in dependency order: the **request wrapper** creates
the context, **execution metadata** describes it, **audit logging**
persists what happens inside it.

## 2. Boundary — platform, not vertical

All three are platform-side per ADR-0009. Audit logging is machinery:
it records that a decision was made and on what basis, without
understanding what fraud is. Nothing in the trio may import from
`verticals/`.

Location: `platform/governance/` — `wrapper.py`, `metadata.py`,
`audit.py`, `events.py`, `models.py`. The fraud vertical and the agent
consume it through the narrow interface at §6; they do not reach into
its internals.

This is the first test of the ADR-0009 boundary against green-field
code rather than extracted code, and therefore the first meaningful
CF-1 spot-check subject. The boundary test at §7 is mandatory evidence
for that spot-check.

## 3. Component 1 — Request wrapper

A context manager wrapping any governed inbound request, whether from
FastAPI, a batch job, or a test harness.

Responsibilities:

1. **Mint a correlation id** — UUIDv7 (time-ordered, so records sort
   naturally without a separate index on timestamp). One per request,
   propagated through LangGraph state to every node.
2. **Capture execution metadata** once, at entry (§4), and bind it to
   the correlation id.
3. **Open a run record** in the audit store before any work happens.
4. **Guarantee a terminal record** on every exit path — success,
   handled failure, and unhandled exception. This is the requirement
   most easily lost: an audit trail that records only successes cannot
   answer the question a contested decision actually raises, which is
   what happened when it went wrong. The wrapper closes the run in a
   `finally`, with outcome `completed | failed | aborted` and, on
   failure, the exception type and message but **not** the traceback,
   which can carry payload data into the record.
5. **Provide the emit interface** (§6) to everything running inside it.

Nesting: a wrapper opened inside an active wrapper reuses the parent
correlation id and records a child span rather than minting a new run.
Sub-agents at later stages will need this and it is far cheaper to
build now than to introduce once records exist.

## 4. Component 2 — Execution metadata

The reproducibility fingerprint of a run. Captured once at wrapper
entry, immutable thereafter, written to the run record, and consumed
directly by the B9 nondeterminism register.

| Field | Source | Why |
|---|---|---|
| `correlation_id` | wrapper | joins everything |
| `started_at`, `ended_at` | wrapper | UTC, microsecond |
| `code_sha` | build-time injection | which code ran |
| `env_id` | conda env name + Python version | which environment |
| `model_artifacts` | provenance from the scoring service | sha256, Platt a/b — already emitted by B5 |
| `llm_pin` | Ollama model tag + digest | TI7 pin, actual not intended |
| `prompt_version` | prompt registry (B8 `prompts/` decision) | null until B8 |
| `corpus_version` | corpus manifest hash | null until B7 |
| `retrieval_config` | top-k, threshold | null until B7 |
| `schema_version` | constant | audit record schema, versioned from day one |

Nullable-until-available is deliberate: the fields are declared now and
populated as stages land, so the schema does not change under B7 and
B8. Declaring the shape early is the cheap half; migrating a populated
audit table is the expensive half.

**Unpopulated fields are `NULL`, never an empty string and never a
sentinel such as `"none"` or `"n/a"`.** Downstream code must be able to
distinguish "this stage had not landed when the run executed" from "a
value was recorded and it was blank". A sentinel silently becomes a
real version string to anything reading the column later.

`model_artifacts` deserves note — B5 already emits exactly this
provenance and B6 already threads it through agent state. The trio does
not invent it; it gives it somewhere to be written down.

`code_sha` is injected at build time into an environment variable. Where
it cannot be resolved — a container built outside CI, a bare dev run —
the value is `unknown` **and the fact that the fallback was taken is
itself recorded** in a `code_sha_source` field (`build | fallback`).
Never a silent blank: a run whose provenance is unknown must be
identifiable as such rather than indistinguishable from one that was
never asked.

## 5. Component 3 — Audit logging

Three tables, all append-only. No `UPDATE`, no `DELETE` in application
code; the database grant does not include them.

**`audit_run`** — one row per governed request. Correlation id (primary
key), execution metadata as typed columns plus a JSONB overflow,
`subject_ref`, outcome, timings.

**`audit_event`** — one row per step within a run. Correlation id,
sequence number, event type, actor (which node), typed payload,
optional payload reference, timestamp.

**`audit_payload`** — content-addressed text store, keyed by hash
(§5.1).

**Sequence number, not timestamp, is the ordering key.** Two events in
the same microsecond need a deterministic order for replay, and clock
resolution will not always provide one. The wrapper owns a monotonic
counter per run.

### 5.1 What is stored, and what is referenced

The tension: replay needs enough to reconstruct the decision; CL-21
requires that prompts not carry personal data; and storing full prompts
and responses inline would make the audit table the largest
personal-data store in the system.

Position: **derived signals and references are stored inline in the
event row; prompt and response text is stored under a payload
reference.** The event carries a hash and a pointer; the text lives in
`audit_payload` keyed by that hash.

This is what makes CL-21's crypto-shred mechanism possible later —
shred the payload table, keep the decision record and its hashes
intact, and the audit trail still proves what happened without holding
what was said. Content-addressing also deduplicates identical prompts
across runs, which at volume is not a minor saving.

### 5.2 Subject reference

`audit_run` carries a `subject_ref` column, indexed, holding whatever
pseudonymous customer identifier the vertical supplies.

This is the one item in CL-21 with a build consequence, and this is
where it lands. Without it, "retrieve every record relating to one
individual" is a full table scan, and both subject access requests and
erasure become operationally impossible at any real volume. A column
and an index now; a migration on a populated append-only table later.

### 5.3 Storage

**PostgreSQL**, running since B1. Not MLflow — that is experiment
tracking and the wrong tool for a decision record. Not files — B9
replay and subject retrieval are both query problems.

## 6. Interfaces

Everything inside a wrapper sees one object and three calls:

```python
with governed_request(subject_ref=..., source=...) as ctx:
    ctx.emit(ModelScored(probability=..., artifact_sha256=...))
    ctx.emit_ref("llm_invoked", text=prompt)   # hashed, stored by reference
    meta = ctx.metadata                        # read-only
```

The agent passes `ctx` through LangGraph state. Nodes call `emit`; they
do not know about tables, sessions or transactions.

Deliberately narrow: three methods is the whole surface. A wide
governance interface gets used inconsistently, and inconsistent audit
records are worse than none because they imply a completeness they do
not have.

### 6.1 The emit contract — allowlist by construction

**`emit` accepts a typed event object, not a free-form dict.** Each
event type has a declared payload model in `platform/governance/
events.py` with named, typed fields. A caller cannot pass a field that
is not in the schema, because there is nowhere to put it.

This is the enforceable form of CL-21's prompt-minimisation rule. The
alternative — inspecting a free-form dict and rejecting values that
look like personal data — cannot work: a name is a string, and no
runtime check distinguishes `"Michael Kennelly"` from `"card_present"`.
A denylist over values would give false assurance, which is worse than
no check at all. An allowlist over *fields* holds, because the schema
is written once, reviewed once, and cannot be circumvented at a call
site.

Two backstops against schema drift:

- **Key-name denylist** applied when event models are defined, not at
  call time: a payload model declaring a field named `name`,
  `account_number`, `sort_code`, `address`, `email`, `postcode`, or
  `full_name` fails a test. This catches the case where someone adds a
  well-intentioned field to a model months from now.
- **String-length ceiling** of 256 characters on any payload field.
  Anything longer is free text and belongs in `emit_ref`. Enforced in
  the base model.

`emit_ref` is the only route for text that may contain personal data,
and it stores by reference (§5.1) precisely so that text can later be
shredded independently of the decision record.

### 6.2 Public contract and versioning

**`schema_version` and the event-type enum are public contract.** Later
stages depend on them — B9's replay reads event types by name, B11's
panels query them.

- Event types at B7 entry: `request_received`, `feature_computed`,
  `model_scored`, `retrieval_performed`, `llm_invoked`,
  `guardrail_evaluated`, `response_emitted`, `error_raised`.
- The enum is extensible. **Adding** an event type is a minor version
  bump and needs a note in the ADR's evidence trail.
- **Removing or renaming** an event type, or changing the meaning or
  type of an existing payload field, is a breaking change: it requires
  a migration note and a DEC or ADR, and cannot land without one.

Without this, B9 can silently assume an event type that has since
disappeared, and the failure surfaces as a replay that quietly omits a
step rather than as an error.

## 7. Tests

- Wrapper emits a terminal run record on success, handled failure, and
  unhandled exception — three tests, and the third is the one that
  catches regressions.
- Sequence numbers strictly increasing, no gaps, within a run.
- Nested wrapper reuses parent correlation id.
- Execution metadata captured once and not mutated by later emits.
- Unpopulated metadata fields are `NULL`, not `""` or a sentinel.
- `code_sha_source` records `fallback` when injection is absent.
- No `UPDATE`/`DELETE` path: attempt one, assert it fails.
- Payload text is not present in `audit_event`; only the hash is.
- `subject_ref` index exists and a lookup by subject returns all runs.
- **Negative test — prohibited field:** an event payload model
  declaring a denylisted key name fails the suite.
- **Negative test — free text:** a payload field exceeding 256
  characters is rejected at construction.
- **Boundary test:** `platform/governance/` imports nothing from
  `verticals/`. Machine-checked, and the seed for the B9.5 CI check.

## 8. What consumes this downstream

- **B7** — `retrieval_performed` events with chunk ids and manifest
  version; the corpus eligibility state at decision time comes from
  here.
- **B8** — `guardrail_evaluated` events carrying block/redaction
  reasons and the precedence resolution.
- **B9** — the entire replay exhibit, the nondeterminism register
  (populated from execution metadata), the worked trace, and the
  `outcome_event` table, which joins on correlation id.
- **B11** — panels query these tables rather than a parallel metrics
  store.

B9 is the point at which the trio's design either holds or is exposed.
Everything above is chosen with that in mind.

## 9. Deferrals

**In scope now:** the three components, three tables, schema version
and event enum as public contract, subject reference and its index, the
typed emit interface with both backstops, the tests.

**Explicitly out:** retention and purge implementation (CL-21, and it
needs the bank's policy); crypto-shred implementation (the *mechanism*
is enabled by §5.1, the operation is later); any UI; log shipping or
external SIEM integration; the `outcome_event` table itself, which is a
B9 exit item under DEC-0010.

## 10. Resolved decisions

1. **Payload retention default in the reference build** — store
   indefinitely, with the expiry mechanism present and disabled. The
   reference build is synthetic so nothing turns on it technically; the
   point is that the mechanism is demonstrable to a bank's DPO rather
   than described.
2. **`code_sha` in a non-git environment** — build-time injection,
   fallback to `unknown` with `code_sha_source` recording that the
   fallback was taken (§4).
3. **ADR or DEC** — **ADR-0010**, per §11. This establishes a platform
   component and an interface every subsequent stage depends on, which
   is architecturally significant under the CL-08 test. It is the first
   ADR raised prospectively under that gate question rather than
   backfilled.

## 11. Review disposition

- **A1, strengthen the no-personal-data rule — ADOPTED, mechanism
  replaced (§6.1).** The intent is right and the amendment is the most
  valuable of the three: without it, CL-21's minimisation rule stays a
  future Banking Architecture paragraph instead of becoming an
  enforceable platform property. But the proposed mechanism — rejecting
  payload fields "that match the prohibited set" — cannot be
  implemented. Detection would have to operate on values, and no
  runtime check distinguishes a name from any other short string; the
  result would be a check that passes reliably and assures nothing.
  Replaced with an allowlist by construction: `emit` takes a typed
  event object, so a field outside the schema has nowhere to go.
  Backstopped by a denylist on *field names* at model-definition time
  and a 256-character ceiling pushing free text to `emit_ref`. Same
  objective, enforceable form.
- **A2, schema version and event enum as public contract — ADOPTED as
  written (§6.2).** Extended slightly: additions are a minor bump,
  removals and renames require a DEC or ADR plus a migration note. The
  failure mode named in the review is the right one — B9 assuming an
  event type that has since gone, surfacing as a replay that quietly
  omits a step rather than as an error.
- **A3, resolve open decision 3 as an ADR — ADOPTED.** Raised as
  ADR-0010.
- **Minor clean-ups — ADOPTED, all four.** Nullable fields stay `NULL`
  (§4); negative test for prohibited fields, adapted to the §6.1
  mechanism and split into two tests (§7); both open-decision
  recommendations accepted (§10).

---

## Addendum — 2026-07-25 (build; ratified text above unchanged)

Two implementation records, entered at build per RAT-01 section 3.1
(addendum, not DEC/re-ratification — the ratified decisions would not
have differed):

1. **Package path.** Section 2's location `platform/governance/` reads
   as `arcaai/platform/governance/` (import path
   `arcaai.platform.governance`) per DEC-0013: top-level `platform`
   collides with the Python standard library module of that name, in
   both directions, verified before build. The ADR-0009 boundary is
   unchanged; only its filesystem address moves. All path references in
   sections 2, 6.1 and 7, and in ADR-0010, read accordingly.

2. **Terminal record is a fourth append-only table.** Section 5's
   "three tables" is implemented as four: `audit_run` (run record,
   written once at entry) plus `audit_run_terminal` (terminal record,
   written once in the wrapper's `finally`), because a single-row
   open-then-close design requires UPDATE, which the append-only grant
   deliberately excludes, and a column-scoped UPDATE grant would weaken
   section 4's immutability of execution metadata. The spec's own two
   nouns ("run record", "terminal record") are two rows. Every other
   section 5 invariant is unchanged and enforced by test, including the
   database-level denial of UPDATE and DELETE to the runtime role.

## Addendum — 2026-07-27 (build; ratified text above unchanged)

Two further implementation records, entered per RAT-01 section 3.1 on
the same test as the 2026-07-25 items — the ratified decisions would
not have differed had these been known at ratification:

3. **`policy_version` declared in execution metadata.** Section 4's
   field table gains `policy_version` (source: policy bundle
   content-address; null until B8), declared now and populated when B8
   lands. This is section 4's own nullable-until-available rule applied
   to a field that did not exist when the section was written:
   `prompt_version` is the identical case — a B8 field declared at
   build — and is the precedent. CL-23 gap 2 proposed an interim route
   through `metadata_extra` with a typed column at B8; that is
   superseded here, because it would change the schema under B8 which
   section 4 exists to prevent. Implemented as `String(128)` matching
   `corpus_version`, with a `<> ''` CHECK constraint per the
   NULL-not-sentinel discipline. **No `schema_version` bump.** Section
   6.2's versioning rule addresses the event-type enum; this is an
   additive nullable metadata column declared before any row exists, so
   there is no before-and-after for a consumer to distinguish. Entered
   while the tables are empty deliberately: after B7 writes its first
   run this stops being free, which is section 4's stated reasoning.
   Independent of CL-23's panel review — if the three-tier framing is
   rejected, an unused nullable column costs nothing.

4. **`metadata_extra` JSONB overflow column.** `audit_run` carries a
   `metadata_extra` JSONB column, present in the build since 25 Jul but
   named in neither section 4's field table nor the first addendum.
   Recorded here for completeness: it is overflow for metadata with no
   typed column yet, subject to the same `none_as_null=True` treatment
   as every other JSONB column. It is **not** the route for fields that
   are known in advance — those are declared per section 4, as item 3
   above does.
