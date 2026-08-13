# ADR — Orchestrator-Worker Separation, Tiered Versioned Memory, and Governed Memory Consolidation (skeleton)

# DRAFT — NOT RULED — NUMBER RESERVED, NOT CONSUMED

**Circulation.** This skeleton circulates to the SME panel under the panel-round
convention (`CLAUDE.md` queue item 33, CANDIDATE), so it is pinned as the inputs
are. It carries a circulation pin only and no fidelity pin: a fidelity pin
attests a received text against its original, and this document was authored
here rather than received.

Pin method (ruled 2026-08-13): sha256 over the complete committed file with the
single line beginning 'Circulation pin' excluded; canonicalised as the file's
raw bytes minus that line including its newline.

Circulation pin (file sha256): 1a745e66496d7f8cacced5c058ccc2bec610e7989c290e07bc6a0ac9ae957a95

Title formulation is **ruled**, at ITEM 21 of the rulings record. The reservation
is **ADR 0011**, confirmed next-free against the register anchor of 2026-08-13
(`decisions/` holds 0001–0010). **This draft consumes nothing**; the number is
allocated at ruling, read live from the register.

Every input names "ADR-0012". That is stale self-numbering throughout, corrected
in each pinned input's header and read as 0011.

Two markers remain in use, and one has been retired:

- **[BACKFILL: source]** — content exists, not yet read in. Mechanical.
- **[RULING NEEDED]** — the governing text is **SILENT**. No convention substituted.
- **[PENDING RECORD RECOVERY]** — **RETIRED.** The parked rulings record was
  recovered and pinned on 2026-08-13. Every citation that carried this marker is
  now a live citation. **Count: zero.**

---

## 0. Input set — COMPLETE, four pinned artefacts

All four committed to `docs/governance/` on 2026-08-13, body byte-for-byte, each
under the ruled pin method (circulation pin excludes its own line).

| Input | File (`docs/governance/`) | Circulation pin |
|---|---|---|
| **Seed** — Brain/Hands v0.2 | `ADR-candidate-input_brain-hands_2026-08-13.md` | `7755a5076f7c…` |
| **Consolidation** — 20 items | `ADR-candidate-input_panel-consolidation_2026-08-13.md` | `6d7a188c111c…` |
| **Rulings record** — 21 rulings | `ADR-candidate-input_rulings-record_2026-08-13.md` | `a25963414ddc…` |
| **Reviewed document** — 2026-08-09 | `ADR-candidate-input_reviewed-document_2026-08-13.md` | `b20ee2bec188…` |

**Precedence, ruled and load-bearing.** The consolidation states
RECOMMENDATIONS; the rulings record states RULINGS. **On any divergence the
rulings record governs.** Citations below are to the rulings record by item.

### 0.1 The rulings record — recovered, not reconstructed

Searched exhaustively in-repo on 2026-08-13 and found nowhere: working-tree
content search across all file types, history pickaxe `-S` across all refs, a
second pass with `-G -i` after establishing that `git log -S` is case-sensitive
while `grep -i` is not, and a filename search. Zero commits on any ref had ever
contained it. It was never in this repository.

It was **parked 2026-08-10 to ride this ADR's PR**, by that session's own plan —
its §5 item 6 says so: *"This record and the consolidation document enter
docs/governance/ via a repo PR at the next appropriate session (hash-pinned
transfer per house rule)."* The pinning act of 2026-08-13 discharges the parking,
and the transfer was hash-pinned exactly as that plan required.

### 0.2 The seed — provenance is weaker than the others, and says so

The Brain/Hands original is **no longer locatable in the operator's Gmail
drafts**. The pinned text was preserved by the coordinator's read earlier on
2026-08-13. Provenance is **coordinator-transcribed, operator-confirmed**; the
operator's confirmation at PR review is the fidelity attestation.

Recorded here as well as in the input's own header because it bears on what the
fidelity pin means: it fixes the text against later drift, and **cannot evidence
faithfulness to a draft that no longer exists.** §C and §D rest on this input,
so they rest on that attestation.

## A. Statement and lineage

**Statement.** [BACKFILL: one-paragraph statement, authored from §B–§D once the
graph inventory is enumerated.]

**Lineage.** Extends, and does not reopen:

- **ADR-0009** — platform supplies machinery, vertical supplies business
  semantics; nothing in `arcaai/platform/` imports from `verticals/`; the B9.5
  extraction gate. The seed is explicit that the scoring/agentic firebreak is
  *"the existing ADR-0009 platform/vertical boundary applied, not a new ruling"*.
- **ADR-0010** — typed events, personal data excluded by construction; payload
  by reference; the event enum as **public contract** where renaming a type is a
  breaking change requiring a DEC or ADR. Binds §D and §J.
- **RAT-02** — the governance trio the seed aligns the broker to at its §2.

**Canonical vocabulary — RULED, ITEM 21.** The three principles take these names
and the working terminology is retired:

- **ORCHESTRATOR-WORKER SEPARATION** — *"execution and shared-memory proposal
  authority are structurally separated: workers execute; workers have read-only
  access to shared memory; the orchestrator is the sole proposer of
  shared-memory changes; proposals cannot self-apply."* "Single-Proposer
  Topology" declined as primary name.
- **TIERED VERSIONED MEMORY** — *"shared context is held in authoritative,
  versioned memory tiers (PLATFORM, TENANT/PROJECT, CASE) with hash-pinning,
  authority semantics and explicit release boundaries."* "Governed Memory Tiers"
  declined.
- **GOVERNED MEMORY CONSOLIDATION** — *"memory changes are produced out-of-band
  from bounded evidence as proposed, validated and gated diffs."* Ruled the
  strongest rename: the "Dreaming" metaphor *"is unsuitable as the formal name of
  a bank architecture control and misleadingly implies autonomous offline
  learning."*

**"Dreaming" is RETIRED from formal vocabulary, not retained parenthetically.**
Historical documents stand as written under the immutability convention; the
canonical names bind from this ADR forward, with ITEM 21 as the mapping of
record.

## B. Graph inventory, and two boundaries that must not be conflated

**The structural instruction, ruled at ITEM 21's drafting guidance:**

> "Orchestrator-Worker Separation (shared-memory proposal authority) and the
> Brain/Hands spine (execution and credential authority, Item 18) are distinct
> boundaries that compose - the brain is the orchestrator, hands are workers -
> but govern different properties (who may change shared memory vs who may act
> on the world). ADR-0012 states both boundaries explicitly and does not
> conflate them."

This ADR therefore carries **two** boundary statements, not one:

| Boundary | Governs | Source |
|---|---|---|
| Orchestrator-Worker Separation | who may **change shared memory** | ITEM 21 |
| Brain/Hands | who may **act on the world**, and who holds credentials | ITEM 18(a), seed |

They compose — brain *is* orchestrator, hands *are* workers — and collapsing them
into one boundary loses a property. Stated because the composition makes the
collapse the natural drafting error.

- Orchestrator graph(s): [BACKFILL: enumerate against `agent/graph.py` as built]
- Subordinate graphs: [BACKFILL]
- **[RULING NEEDED: whether worker-to-worker invocation is permitted, or all
  fan-out routes through the orchestrator.** ITEM 21 fixes proposal authority
  over shared memory and is SILENT on invocation topology.**]**

**The scoring path is explicitly OUT of scope.** Seed: *"The scoring path
(BentoML) is explicitly OUT of scope — it remains a synchronous, hot,
non-agentic service. The firebreak between scoring and agentic paths is
preserved."* ADR-0009 is applied here, not re-ruled.

## C. Brain/Hands separation

**Source: pinned seed, circulation pin `7755a5076f7c…`. Ruled ACCEPTED as the
structural spine at ITEM 18(a).**

**Statement, from the seed:** the orchestration loop ("brain") and tool/task
execution ("hands") are separate services with distinct lifecycles. The brain is
durable and long-lived, holds session state, conversation context and the
reasoning loop, and **holds no execution credentials and performs no
side-effecting work**. Hands are execution environments provisioned on demand
only when a tool invocation requires one, receive credentials scoped to the
single task at the moment of use, and are destroyed or reset afterwards.

**Rationale carried:** latency (the hot path never touches sandbox
provisioning); credential isolation (§D); resilience (session state in the
brain's durable store — a crashed sandbox loses only the in-flight task, not the
investigation); scalability (one orchestration service multiplexes many
sessions); auditability (the seam is a natural audit boundary, every crossing a
typed event).

**Seam cost — stated honestly, not assumed away.** The crossing adds a hop
inside the agentic path: event serialisation, broker round-trip, sandbox
dispatch.

**Seam P95 budget: [BACKFILL: Domain-1 pilot measurement].** A placeholder, and
**not a claim.** The measurement point is **ruled and CONFIRMED at ITEM 18(c):
the Domain-1 pilot.** The seed states the same discipline: *"placeholder until
measured, not a claim."*

**Light-worker class — a named design decision, not a default.** The seed
permits the ADR to define a class reusing a warm environment for trivial
stateless calls, and insists the trade — warmth versus isolation — be named.
**[RULING NEEDED: whether the light-worker class is adopted, and its bounds.**
The seed offers it; no consolidation item disposes of it.**]**

**Design vocabulary, adopted from the seed:** Agent (model + system prompt +
tools, declarative and versioned), Environment (sandbox image, packages, egress
rules, declarative and versioned), Session (a running binding of agent +
environment owned by the brain, durable across execution failures), Event (the
**sole** communication protocol — *"no request/response coupling; the event
stream IS the audit log"*).

**Phase 1 refactor implied:** B6's LangGraph agent runs loop and tool execution
in-process; this principle requires extracting the loop into an orchestration
service and moving tool execution behind a worker/sandbox interface.

## D. Credential broker

**Source: pinned seed §2a, circulation pin `7755a5076f7c…`.**

**Home: RULED at ITEM 18(b) — a SECTION OF THIS ADR**, not a standalone DEC,
*"with promotion to a standalone DEC only if the broker's design decisions later
outgrow the ADR (register economy)."* The seed left this open; the ruling closes
it, and this section is where it lands.

**The broker is a new trust root and is treated as one.** The seed owns the
consequence rather than hiding it: moving credential risk out of the loop
concentrates it in the broker. Minimum posture, carried:

- Its **own isolated service** — not co-resident with brain or hands.
- A **policy table** mapping agent + session + tool to a scoped credential and TTL.
- A **typed audit event for every issuance AND every denial** — which must
  conform to ADR-0010's emit contract; denials are events, not silence.
- **Immediate revocation** supported.
- **Subject to the same admission and hash-pin discipline as any platform
  artefact** — so the broker is itself mandated (§G).
- **Brain-only issuance.** *"The broker never accepts capability requests
  originating from hands — issuance requests flow from the brain only, so a
  compromised sandbox cannot mint its own credentials."*

**Failure semantics — ruled at ITEM 10**, and they attach here: behaviour on
mid-flight mandate revocation and on mandate-store unavailability must be
specified, with **fail-closed the default posture**; any degraded mode *"must be
explicitly argued in the ADR with evidence."*

**Least privilege — ruled at ITEM 16.** The broker and the hands-cannot-mint
rule *"implement the credential half"* of that item.

## E. Memory — tiers, authority, budgets, consolidation

**TIERED VERSIONED MEMORY**, tiers named at ITEM 21: **PLATFORM, TENANT/PROJECT,
CASE**, with hash-pinning, authority semantics and explicit release boundaries.

- **Authority boundary — RULED, ITEM 8.** The ADR defines who is authoritative
  when tiers conflict, and staleness rules when a lower-tier artefact is newer
  than a higher-tier one. It states plainly that **context assembly is an
  AUTHORISATION boundary — what an agent may see and act on — not a content
  loader.** The ACL matrix and release-boundary semantics are designed to that
  standard.
- **ACL matrix** — [BACKFILL: undesigned; the standard it must meet is ITEM 8]
- **Per-tier context budgets and summarisation discipline — RULED, ITEM 7**, and
  required **before context assembly is built**. The excluded failure mode is
  named: *silent degradation of case content under load.* [BACKFILL: the numbers]
- **Decision-record semantics — RULED, ITEM 9.** The audit record distinguishes
  memory **loaded** into the session from memory merely available or authorised,
  establishing what context governed the decision. Vehicle: the Brain/Hands typed
  event stream (session assembly events).
- **GOVERNED MEMORY CONSOLIDATION** — out-of-band from bounded evidence, as
  proposed, validated and gated diffs. **Consolidation cost cap RULED at ITEM
  13**: a maximum cost per run per tenant with an enforcement mechanism (token
  budget, model-size cap, or fallback to a smaller model), *"placeholder until
  measured at the Domain-1 pilot; if the pilot exceeds the bound, the task
  narrows before production commitment."*
- **Memory-pattern DEC — RULED, ITEM 19**: drafted **alongside** this ADR, as
  DEC-0014 generalised to memory artefacts. Number taken at authoring. Not this
  document's content, but its sibling.

**Sequencing constraint from queue item 33's P2:** no consolidation or memory
code lands before the mandate design note is ruled.

## F. Release boundaries

- **Policy Fast Lane — RULED IN FULL, ITEM 4.** A first-class release class
  carrying: a fixed list of allowable change types; pre-approved ranges per type;
  **automatic re-review of every fast-lane change at the next standard cadence**;
  the bounds themselves as mandated artefacts under slow governance; a named
  owner and versioning for the bounds; and an audit trail distinguishing
  fast-lane deployments. *No longer an open ruling.*
- **Transactional rollback — RULED, ITEM 11** (dissent leg 2, discharged).
  Rollback is transactional across the release unit — model, thresholds and
  dependent artefacts revert together; is itself a mandated, logged, auditable
  event; and targets are hash-pinned and deployable without rebuild.
- **Statistical parity — RULED, ITEM 14.** Acceptable divergence per model type;
  a statistical parity test (e.g. bootstrap CI) in the promotion gate; failure
  rejects the promotion and logs the incident. **One definition of statistical
  comparison serves both this and the test-capability schema's migration-diff
  semantics** (TOR rulings-record amendment 3) — *"stated once and referenced."*
- **Governed-batch loop** — [BACKFILL: undesigned]

## G. Mandate and admission — placement principle, pointer for the design

Specification is **queue item 33's P2 design note** and is **not duplicated
here.** What this ADR states, ruled at **ITEM 2**:

- **Enforcement at PLATFORM level**: the loader and orchestrator *"refuse any
  unmandated artefact regardless of caller."*
- A **`MANDATE_ENFORCEMENT` interpreter-startup flag that fails hard when unset.**
- A **CI negative test proving an unmandated artefact hard-fails.**
- **Composition-root checks are defence in depth only, never the enforcement
  point.**
- Schema, versioning, revocation path and three-way hash reconciliation are
  specified **before any platform code**.

## H. Two-zone Domain 1

**RULED, ITEM 5**, with DeepSeek's hardening adopted:

- The **Frontier / Bank-Data Training** split adopted.
- **Data minimisation by a separate non-AI redaction pipeline** before anything
  crosses to the frontier zone.
- **The redaction pipeline is itself a mandated, separately audited artefact.**
- Cross-zone flows logged under **production-grade egress controls**.

**[RULING NEEDED: whether the zone boundary is enforced by deployment topology,
by credential scope through §D's broker, or by both.** ITEM 5 fixes the split and
the pipeline and is SILENT on the enforcement mechanism.**]**

Related, **ITEM 16**: developer workstations are excluded from production data
and artefacts *"except within the bank-data training zone under separate
credentials and logging."*

## I. Spec-blindness mechanism (H-1)

**Not addressed by the architecture review.** This requirement comes from H-1 in
`docs/governance/RULINGS_RECORD_2026-08-13_H-batch.md`, which ruled blindness
**mechanically verified** and placed the mechanism **in this ADR**.

**The requirement.** The test-author must be **provably unable** to read builder
output — not instructed not to, and not merely unable to write outside the test
tree.

**Candidates, with their weaknesses; the choice is [RULING NEEDED]:**

1. **Protected paths** — the guard denies reads of implementation paths for the
   test-author identity. Precedent exists (`.claude/agents/`, the governed
   stores). Weakness: the guard gates writes and commands; a read-deny scoped to
   an agent identity is not a shape it currently has.
2. **Scoped context** — spawn with only the ruled spec artefacts reachable.
   Weakness: a subagent holding a Read tool can reach the filesystem.
3. **Worktree isolation** — spec and test tree only, nothing else present.
   Strongest, since absence is not a rule that can be misapplied. Weakness: cost,
   and the spec must be genuinely separable.

**[RULING NEEDED: what artefact evidences that blindness held for a given lane.**
A mechanism leaving no evidence it held is indistinguishable at review from an
instruction that was followed.**]**

## J. Event schema as a governed artefact

ADR-0010 Decision 3 already governs status: `schema_version` and the event-type
enum are **public contract**; adding a type is a minor bump; removing or renaming
one, or changing a payload field's meaning or type, is a **breaking change
requiring a migration note and a DEC or ADR.** RAT-02 §6.2 carries the same.

**A divergence between two inputs, resolved by precedence.** The seed proposes
*"Event schema becomes a governed artefact in the corpus (candidate B-series
doc)."* **ITEM 19 rules otherwise: "no corpus placement yet (register first;
corpus only when a later SG document is deliberately scoped to agent-memory
governance)."** The rulings record governs. **The event schema is registered, not
corpus-placed, at this stage** — the seed's B-series candidacy is deferred, not
adopted.

Recorded explicitly because it is the first case where a pinned input and the
ruling that governs it disagree, and the precedence rule at §0 decides it.

## K. Open rulings register — reconciled against the ruled record

Every item marked open in the previous draft has been rechecked against the
rulings record. **Five of the eight were already ruled on 2026-08-10** and are
struck.

| # | Ruling | Section | State |
|---|---|---|---|
| **K-1** | Worker-to-worker invocation, or all fan-out via orchestrator | B | **OPEN** — ITEM 21 fixes proposal authority, SILENT on invocation topology |
| **K-5** | Zone boundary enforcement — topology, credential scope, or both | H | **OPEN** — ITEM 5 SILENT on mechanism |
| **K-6** | **Spec-blindness mechanism — three candidates** | I | **OPEN** — from H-1; absent from the architecture review |
| **K-7** | What artefact evidences blindness held | I | **OPEN** — from H-1 |
| **K-9** | Light-worker class — adopted, and its bounds | C | **OPEN, NEW** — seed offers it; no item disposes of it |
| ~~K-2~~ | Seam / admission failure semantics | D | **RULED — ITEM 10**, fail-closed default |
| ~~K-3~~ | Memory tier versioning | E | **RULED — ITEM 19**, memory-pattern DEC generalising DEC-0014 |
| ~~K-4~~ | Policy Fast Lane bounds, validators, re-review | F | **RULED — ITEM 4**, in full |
| ~~K-8~~ | Event schema placement | J | **RULED — ITEM 19**, no corpus placement yet |

**Net: 8 open → 5 open**, one of them new. **K-6 still gates the arc** — H-2
sequenced this ADR before lane one hardens, and H-1 put the mechanism here.

## L. Requirements carried from the ruled consolidation — coverage map

ITEM 19 requires this ADR to carry *"the mandate schema outline, ACL matrix,
per-tier budgets, fast lane, two-zone Domain 1, and the Items 2-16
requirements."* This map exists so no ruled item is silently dropped.

| Item | Requirement | Home |
|---|---|---|
| 2 | Mandate/admission, platform-level enforcement | §G |
| **3** | **Attestation — staged** | **§M, below** |
| 4 | Policy fast lane | §F |
| 5 | Two-zone Domain 1 | §H |
| 6 | Tenant isolation as a formal gate criterion | §M |
| 7 | Per-tier budgets, summarisation | §E |
| 8 | Memory authority boundary | §E |
| 9 | Decision-record semantics | §E |
| 10 | Admission-check failure semantics | §D |
| 11 | Transactional rollback | §F |
| 12 | Canary — hybrid | §M |
| 13 | Consolidation cost cap | §E |
| 14 | Statistical parity | §F |
| 15 | Operational burden | §M |
| 16 | Least privilege | §D, §H, §M |
| 17 | S16 rulings as production-critical-path | §M |

## M. Assurance posture, and requirements without another home

### M.1 Attestation — the interim/production distinction, ON THE ADR'S FACE

**RULED, ITEM 3 — staged.** This is the consolidation's central ruling and the
dissent's first leg. The ADR must state **on its face** that *"procedural
controls are not equivalent to cryptographic/hardware-rooted assurance."*

- **Production requirement:** signed component attestation chained to a hardware
  root, **AWS Nitro named**, landing with the AWS migration workstream.
- **Until then:** logs, reconciliation and canary are **explicitly labelled
  interim evidence and never represented as equivalent.**

**The dissent is PARTIALLY SUSTAINED (ITEM 20)**, and the record says why: *"the
interim/production distinction exists precisely because procedural and
cryptographic assurance are not equivalent."* This ADR does not soften that.

### M.2 Canary — hybrid, ruled at ITEM 12 (dissent leg 3, discharged)

Production-resident canary **retained** for positive evidence of live
containment, with DeepSeek's hardening adopted in full: separate alerting
channel; independent second-process verification of the canary's own logs;
**missed report window treated as suspected breach**, triggering incident
response. Scope widened to all execution routes including credential-bearing and
indirect-dependency paths. ITEM 2's CI negative test covers the pre-production
route. The ADR states the canary is **attempt-only, with no live-traffic
interaction.**

### M.3 Tenant isolation — ITEM 6

Elevated to a **formal gate criterion preceding AWS infrastructure build**,
recorded in the build tracker, with memory's tenant-scoping named as the reason
it is *"a correctness precondition, not merely infrastructure."*

### M.4 Operational burden — ITEM 15

Minimum-viable operations manual (a checklist a non-expert can follow) plus a
mock-bank trial measuring time-to-competence. **Initial ceiling: 2 person-days
setup**; above it, the architecture simplifies or automates further.

### M.5 S16 — ITEM 17

The pending S16 chair rulings are recorded as **production-critical-path**
(evidence base and fine-tuning data for the consolidator), stated in the build
tracker. The rulings themselves remain a separate act for the chair.

## N. Sections deliberately absent

- **Statement paragraph** (§A) — authored once §B's graph inventory is enumerated.
- **Consequences** and **Alternatives considered** — required by
  `decisions/_template.md`; the alternatives are largely the declined options
  recorded in the consolidation and ITEM 21, and are assembled at authoring.
- **Front matter** (Status, Decision Date, Decider, Supersedes, Related,
  Evidence) — omitted so this reads as a skeleton rather than a draft ADR. The
  `Evidence:` field will cite all four pinned inputs by circulation pin.
- **Mandate schema itself** — queue item 33's P2, pointed at from §G, not
  duplicated.
