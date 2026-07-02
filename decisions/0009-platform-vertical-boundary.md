# ADR-0009 — Platform/vertical capability boundary and the Platform Extraction gate (B9.5)

**Status:** Proposed
**Decision Date:** 2 July 2026
**Recorded Date:** 2 July 2026
**Decision Type:** Contemporary
**Decider:** Mike Kennelly
**Supersedes:** none
**Related:** ADR-0003 (pipeline-as-platform), ADR-0007 (DVC artefact store), ADR-0008 (BentoML platform serving standard)
**Evidence:** Governance review WS-B — `docs/governance/WS-B_review_pack.md` (v0.3, source tree §2b), `docs/governance/GOVERNANCE_REVIEW_WS-B_outcome.md` (unanimous panel consolidation, 2 Jul 2026)

> Status flips `Proposed → Accepted` at merge.

---

## Context

The WS-B governance review examined whether the system as built substantiates
ADR-0003's pipeline-as-platform claim. The panel (Grok, ChatGPT, Claude;
chaired by Mike) was unanimous: the build is a well-engineered fraud vertical
inside a monorepo shaped for a platform, but no extracted platform layer exists.
The decisive evidence is location, not quality — the entire ML lifecycle
(features, training, evaluation, validation, calibration, anti-leakage, serving)
lives inside `verticals/fraud/`; there is no `platform/` or `core/` directory;
`verticals/compliance/` and `verticals/rm_support/` are empty placeholders with
nothing platform-shaped to consume; the one contract on the platform shelf
(`contracts/fraud_scoring.py`) is vertical-named.

Both reviewers applied the same test — *delete `verticals/fraud/`; what reusable
ML platform remains?* — and got the same answer: infrastructure and wrappers,
not the ML lifecycle. Both independently described the failure mode if B10
("replicate the fraud vertical") proceeds without extraction: N copies of
fraud-specific machinery, quality controls diverging within months, and no
defensible answer to a bank architect's question *"show me where your reusable
platform begins and the fraud solution ends."*

The panel's verdict on ADR-0003 is adopted verbatim: **pipeline-as-platform is
architecturally specified but only partially evidenced in the current
implementation.** This ADR converts that finding into two binding decisions.

## Decision 1 — The capability boundary: platform supplies machinery, vertical supplies business semantics

The following boundary governs where every capability is implemented, now and at
extraction:

| Capability | Platform | Vertical |
|---|---|---|
| Serving (BentoML, ADR-0008) | framework, parity harness | endpoint configuration |
| Artefact provenance (DVC, ADR-0007) | entirely | — |
| Anti-leakage | framework: time windows, look-ahead detection, train/test validation | domain leakage rules (e.g. transaction timing, merchant hierarchy) |
| Calibration | framework: Platt and isotonic support | method choice and thresholds |
| Validation | framework | thresholds |
| Feature pipeline | framework: transforms, dependency graph, execution, caching | feature definitions (e.g. merchant velocity, country entropy, device reuse) |
| Provenance manifest, promotion gate | mechanism | vertical-supplied configuration |
| Model architecture, business rules, synthetic generators, evaluation metrics | — | entirely |

Provenance is entirely platform-level: a bank cannot tolerate provenance that
differs by business domain.

## Decision 2 — The Platform Extraction gate (B9.5)

A new build stage **B9.5 — Platform Extraction** is inserted between B9 and B10
in the Build & Quality Plan sequence (recorded as a deviation from the locked
plan via `DECISIONS.md`; `BUILD_TRACKER.md` is the living truth per ruling EB8).

**Scope:** extract the platform-side capabilities in the Decision 1 table from
`verticals/fraud/` into a top-level platform layer; generalise `contracts/` to
vertical-neutral objects; fraud becomes the first consumer of the platform it
previously embedded.

**Exit criterion (gates B10):** a second vertical consumes shared ML lifecycle
components — training, validation, provenance, calibration, feature framework,
serving, governance — rather than copying them. Operational test: a new vertical
can be bootstrapped from platform primitives plus contracts alone, without
copying fraud code, in the order of days not weeks. Target reuse on vertical #2:
80–90% platform, 10–20% new code.

**B10 is restated accordingly:** from "replicate the fraud vertical" to
"instantiate verticals against the platform template."

## Timing (Decision 3)

Extraction happens **at B9.5, not now**. B6–B9 (agent, RAG, guardrails, UI) are
not vertical-ML machinery; halting at B5 to extract would design abstractions
against a sample of one vertical. From B5/inc2 onward, however, **platform-first
discipline applies to anything new and shared**: the promotion-gate CI (CL-13)
is built as a platform mechanism with fraud-supplied configuration; the
provenance manifest schema (CL-12) is vertical-neutral. This shrinks B9.5 when
it arrives.

## Consequences

- B10 cannot open until the B9.5 exit criterion is met.
- Until then, all client-facing and locked-document language describes the
  platform as "architecturally specified, partially evidenced" — never "the
  platform exists" (wording ruling recorded as a `DECISIONS.md` entry).
- The Stage-2/3 minimum design (data adapters, Model Risk gateway, registry
  reconciliation closing ADR-0006's deferred ADR, drift/retrain loop,
  bank-perimeter deployment blueprints) is commissioned as a named design
  workstream after the governance review; it is a prerequisite for claiming
  pipeline-as-platform to a bank, and independent of B9.5.
- `contracts/fraud_scoring.py` is generalised no later than B9.5; earlier if
  touched at B5/inc2.

## Alternatives considered

**Extract now (halt at B5).** Rejected: abstractions designed against one
vertical over-fit it; B6–B9 do not compound the extraction debt.

**Proceed to B10 as written and refactor later.** Rejected unanimously by the
panel: duplicated quality machinery diverges within months, and the divergence
is precisely what a bank Model Risk review would find; retrofitting a platform
under N live verticals is strictly more expensive than extracting under one.

**Treat the platform claim as satisfied by the monorepo skeleton.** Rejected:
the skeleton demonstrates intent, not capability; the delete-fraud test fails.
