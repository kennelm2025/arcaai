# ADR candidate (unnumbered) — Agentic Topology: Engine Team, App Teams, and the Contract Gate

**Status:** DRAFT candidate for Mike's ruling. ADR-0011 is reserved for Agentic Topology; the
number is allocated only at ruling, read from the live register. This seed is drafted from the
Strategic Staging Note in the Accelerator Pack v3 install brief (11 Aug 2026), which is itself
not yet ruled. May alternatively land as an ADR-0009 extension — that is part of the ruling.

## Context

ADR-0009 established the platform/vertical boundary architecturally. The Brain/Hands Decoupling
candidate (unnumbered, v0.2, not yet ruled) proposes the structural spine. Neither yet extends
the boundary into the
**operating model** — how teams organise around it as the venture scales beyond one builder.

## Proposal

One engine team hardens the technical AI engine. Business-app teams build verticals that deploy
onto it through a conformance gate. Sequencing to prove the process before replicating it:

1. **Contract first.** The engine team's first deliverable is the contract: a versioned engine
   interface plus the conformance gate — the scenario schema and test runner, generalised.
2. **One app team, deliberately distant.** Exactly one app team builds against the contract, in a
   vertical far from fraud (e.g. complaints or onboarding), touching only the published interface.
   This brings the vertical-two boundary test forward on purpose.
3. **One full cycle.** Build → deploy → integrate through the gate, end to end.
4. **Rule the corrections.** The interface corrections that cycle forces are ruled. That
   correction moment is when the platform becomes real.
5. **Only then replicate.** A set of app teams, with batched ruling sessions and per-team draft
   queues in place before team three exists — the register (Mike) is the scaling bottleneck.

**Coordination rule:** inter-team communication happens only through the contract, spec gaps, and
the ruling queue. The coordination trail IS the governance record.

## Consequences

- The engine interface is extracted from accumulated precedent (`contract-seed.md`), not invented.
- Vertical independence is proven with one consumer before it is assumed for many.
- Ruling throughput becomes an explicit scaling constraint with a named mitigation (batched
  sessions, draft queues, Mobile Ruling Protocol) rather than a discovered one.

## Open questions for the ruling

1. ADR-0011 in its own right, or an ADR-0009 extension?
2. Which distant vertical for the boundary test — complaints, onboarding, other?
3. Does the conformance gate's Formal Execution follow the D2.0 two-regime model verbatim, or
   does a multi-team context need its own regime wording?
