# Solution Architecture Specification

**Spec number:** 02 of 08
**Version:** 0.0 (placeholder)
**Status:** Not started
**Owner:** Mike Kennelly
**Primary audience:** Bank-side architects + Arca engineering — the shared reference architecture

---

## What this specification will contain

When complete, this specification will define:

- **The five-layer architecture** — the canonical structure of the platform (drawing from v0.5/v0.6 of the predecessor Banking Architecture document)
- **The components within each layer** — named, scoped, and bounded
- **The interfaces between layers** — what crosses each boundary
- **The data flows** — how a query, a model training run, a monitoring event move through the architecture
- **The agentic orchestration model** — how the agent layer drives the platform
- **The three-stage model lifecycle** in architectural terms (ADR-0002) — how Reference, Upskilling, and Continuous Improvement are reflected in the architecture

## Why this is spec 02

This is the reference architecture both sides work from. Bank-side architects use it to assess fit; Arca engineering uses it as the framework within which Technical Architecture is fleshed out.

It is **technology-agnostic where possible** — naming components by role, not by product. Specific technology choices live in Technical Architecture (spec 03).

## Predecessor documents

The current v0.6 Banking Architecture document and the ArcaAI System Architecture document both contain material that will be rationalised into this specification during the design phase. The rationalisation map (Week 2 deliverable) will establish what migrates from where.

## Status notes

Not started. Will begin drafting in Month 2 of the design phase, after Product Definition is sufficiently developed to provide canonical positioning.
