# CL-23 — Policy-as-code extended to the governance layer: bank policy as versioned, executable, recorded input

*Raised: 2026-07-25 (evening session), arising from the Executive
Presentation v12 refresh and the CL-21 mechanism/policy framing.
Class: architecture gap / design input to B8 — not a build defect.
Status: DRAFT, not yet panel-reviewed; circulate with the next
governance round per house process.*

*Numbering note: an earlier draft handover entry styled "CL-23"
(2026-07-25, morning) was withdrawn before filing as a check_docs
resolution bug — "no CL is raised" — and never entered the register.
This is the first filed CL-23; the register's next-free counter was 23
at the time of filing.*

---

## Framing — three tiers, and the CL-21 table made executable

CL-21 established the governing split: *the architecture states the
mechanism; the deploying bank decides the policy*. This CL is that
split made executable — the bank's data, security and AI policy
expressed as versioned code the platform deploys and enforces
automatically. Three tiers, and the boundaries between them carry the
design:

| Tier | What it holds | How it is enforced |
|---|---|---|
| 1 — Structural invariants | Append-only grants, typed emit allowlist, sequence ordering, payload-by-reference | Compiled in and database-enforced. **Not policy-addressable, including by the bank** — see Non-goals |
| 2 — Bank policy as code | Retention schedules, erasure triggers, field prohibitions, model-risk appetite, replay authorisation, human-routing rules | Declarative bundles (OPA/Rego and configuration), versioned, tested, deployed through the platform, enforced at existing control points |
| 3 — Human judgement | Lawful basis, DPIA sign-off, risk-appetite ratification | Outside the engine; the engine records and enforces the consequences of these decisions, never makes them |

The load-bearing rule: **a policy engine must not be able to weaken the
recording substrate that makes policy enforcement demonstrable.** If
"allow UPDATE on audit" were expressible as policy, the audit trail's
evidentiary value — the platform's central claim — would be gone.
Tier 1 is the floor beneath Tier 2, and its non-negotiability
(including to the deploying bank) is a selling point, not a
limitation.

## Finding

Policy currently exists in the suite as prose and as scheduled
components. OPA arrives at B8 scoped to the control plane
(request-time authorisation and content policy). The governance layer,
meanwhile, has accumulated enforcement points that take no policy
input and record no policy provenance: the retention/expiry mechanism
ships present-and-disabled with nothing to enable it against
(RAT-02 section 10.1); the emit field denylist is fixed at platform
build; promotion gates check platform thresholds, not bank appetite;
the B9 replay and subject-retrieval capabilities have no authorisation
model; and no decision records which policy was in force when it was
made. A bank asked "what retention rule applied to this record" would
answer from documents, not from the record — the archaeology the
platform exists to eliminate.

Seven gaps.

### 1. Policy-plane scope at B8 — the framing decision

B8's scheduled policy work (OPA, precedence hierarchy, threat
catalogue) should be framed as a **policy plane spanning the control
plane (request-time) and the governance layer (record-time)**, not as
control-plane-only. This is a scope statement for the B8 design brief,
not new components: the same OPA instance, the same precedence
hierarchy work, extended targets. The precedence hierarchy already
scheduled resolves Tier 2 policy conflict for free.

### 2. `policy_version` in execution metadata — the build consequence

The one item with immediate build implication, and it is cheap now and
expensive later, exactly as `subject_ref` was in CL-21. Execution
metadata already records `corpus_version` and `prompt_version` per
decision; `policy_version` joins them under the same
nullable-until-available pattern (NULL until B8), carrying the
content-address (hash) of the policy bundle in force. Policy bundles
are stored content-addressed, reusing the payload-store pattern.
Policy *deployments* run through the governed-request wrapper: who
deployed which bundle, when — append-only, replayable. Interim: rides
`metadata_extra` from B7 if needed; typed column at B8.

*Note added 2026-07-27, ahead of panel review: the interim
`metadata_extra` route above is superseded and the column has been
declared. RAT-02 section 4 already rules that fields known in advance
are declared at build and populated as stages land, expressly so that
the schema does not change under B7 and B8 — `prompt_version` is the
same case and was declared at build. Riding the overflow column and
adding a typed column at B8 is the migration that rule exists to avoid.
`policy_version` is therefore in `audit_run` from 2026-07-27, NULL
until B8, recorded as spec addendum item 3. The gap stands as written
in every other respect; only its interim mechanism changes.*

The payoff is the differentiating sentence: **every decision
permanently records which policy governed it**, and "what rule applied
to this 2027 record" is answered by replay, not argument.

### 3. Retention and erasure as policy input

The disabled expiry mechanism gains its enabling input: per-record-
class retention schedules, legal-hold rules, and crypto-shred triggers
as declarative policy, with competing-obligation precedence (AML
retention defeats minimisation) expressed as ordinary rule ordering.
Batch evaluation — nothing enters any request path.

### 4. Field denylist as a one-way ratchet

The emit-model field denylist becomes bank-extensible in one direction
only: a bank may add prohibited field names; neither the bank nor a
later platform change may remove platform-defined ones through policy.
CL-21's prompt-minimisation rule thereby becomes bank-tightenable.
Evaluated at model-definition/build time, as now — never at call time.

### 5. Model-risk appetite as code at the promotion gates

Calibration bounds, drift thresholds, minimum sample sizes, sign-off
prerequisites — the bank's risk appetite expressed as a versioned
bundle evaluated at model promotion. This is the SS1/23 division of
labour made executable: the platform supplies evidence, the bank
supplies appetite, and the appetite is code with a version history
rather than a document with a review date.

### 6. Replay authorisation and human-routing

Who may replay decisions, who may query by subject, and which decision
classes must route to a human before taking effect — the last being
the DUAA Article 22C human-review safeguard expressed as a rule rather
than a procedure. OPA in front of the B9 replay API; routing rules
evaluated in the agent path (outside the R7 retrieval rung — see
Non-goals).

### 7. Policy bundles are tested artefacts

A rule that cannot fail is not a control (WS-E standing observation).
Every policy bundle ships with executable tests, in the same
discipline as the B8 threat catalogue: a retention rule has a test
that would fire if it stopped holding; a routing rule has a test case
that must route. The Implementation Toolkit gains a **policy starter
library** — reference bundles for retention, minimisation, appetite
and routing — so a bank starts from tested defaults rather than a
blank Rego file. GTM consequence: this strengthens the Toolkit asset
and gives the AI-governance audience in the Describer Pack something
executable to probe.

## Proposed Architecture Principle

> **Bank policy is code.** Data, security and AI policy are expressed
> as versioned, tested, declarative bundles; the platform enforces
> them at every layer; and every decision records which policy
> governed it. Structural audit invariants sit beneath policy and are
> not policy-addressable.

**As with CL-21 gap 3, a principles-set addition is a heavier change
than paragraph edits** and takes the same scrutiny as the original
entries. Bundle with the CL-21 principle at the same review.

## Non-goals — stated as hard rules

- **Tier 1 invariants are not policy-addressable.** No bundle may
  grant UPDATE/DELETE on audit tables, widen the emit contract, alter
  sequence ordering, or inline payload text.
- **No policy evaluation in the retrieval hot path.** Retention is
  batch; denylist extension is build-time; only replay authorisation
  and human-routing are runtime, and neither sits inside the R7
  latency rung (CF-1/B7-d unaffected).
- **The engine does not make Tier 3 judgements.** Lawful basis, DPIA
  conclusions and appetite ratification are human decisions the engine
  records and enforces, never produces.

## Proposed resolution

Scope statement into the B8 design brief (gap 1); `policy_version`
metadata addition per gap 2 (interim `metadata_extra` acceptable at
B7; typed column and content-addressed bundle store at B8); gaps 3–6
as B8 policy-plane work items alongside the already-scheduled OPA and
precedence hierarchy; gap 7 into the Implementation Toolkit backlog;
the Architecture Principle into the next Banking Architecture revision
with the CL-17/19/20/21/22 bundle.

## Sizing and trigger

Design input due at B8 entry (hard trigger: B8 design brief, with
CL-18). Principle addition rides the post-B8 BA revision bundle
(RAT-11). Gap 2's metadata note is the only pre-B8 touchpoint and can
land any time before B8 without a schema change, per the
nullable-until-available design. Not a B7 blocker: no change to B7
entry criteria or gate items; the reference build is synthetic and no
bank policy exists yet to enforce.

## Limitation

Coordinator's design position, not yet panel-reviewed. The claim that
OPA/Rego is the right expression vehicle for all of gaps 3–6 is an
assumption the B8 selection work should test — retention scheduling in
particular may be better served by configuration plus the existing
mechanism than by a rules engine, and the CL stands either way: the
finding is the missing policy input and provenance, not the choice of
engine.
