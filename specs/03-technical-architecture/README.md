# Technical Architecture Specification

**Spec number:** 03 of 08
**Version:** 0.0 (placeholder)
**Status:** Not started
**Owner:** Mike Kennelly
**Primary audience:** Arca engineering + bank-side technical reviewers — the build-level spec

---

## What this specification will contain

When complete, this specification will define:

- **Technology choices** — for each component named in Solution Architecture, the specific technology used and the rationale (e.g. "vector database: ChromaDB at pilot scale, OpenSearch at production scale")
- **Deployment topology** — what runs where, how it scales, what the deployment substrate looks like (Kubernetes, on-prem vs cloud postures)
- **Infrastructure** — compute (CPU/GPU profiles), storage, networking, observability stack
- **Scaling characteristics** — what load patterns the platform handles, where the bottlenecks are, how scaling works
- **Sizing guidance** — for an early-stage pilot vs a full-scale deployment, what infrastructure footprint is needed
- **Technology decision rationale** — every significant technology choice has a stated rationale; alternatives considered briefly stated

## Why this is spec 03

This is the spec that Arca engineering builds from. It is also what a bank's CTO/architect uses to assess whether ArcaAI fits their operational environment.

The two-tier reading model is particularly important here:
- Bank-side reviewers want to know what they need to operate (high-level topology, dependencies on their existing stack)
- Engineering wants implementation-grade specifics (exact versions, configuration parameters, deployment artefacts)

## Relationship to Solution Architecture

Solution Architecture (spec 02) defines what the components are and how they relate. Technical Architecture (this spec) defines what they are built with and how they are deployed. Components are named identically across both specs.

## Predecessor documents

The current ArcaAI Technical Infrastructure document and Engineering Blueprint contain material that will rationalise into this specification.

## Status notes

Not started. Will begin drafting in Month 2-3 of the design phase, behind Solution Architecture.
