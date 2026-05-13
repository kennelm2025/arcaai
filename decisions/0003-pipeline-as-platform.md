# ADR-0003 — Platform positioning: pipeline-as-platform, not models-as-artefacts

**Status:** Accepted
**Date:** 13 May 2026
**Decider:** Mike Kennelly
**Supersedes:** none
**Related:** ADR-0001 (pre-trained model positioning), ADR-0002 (three-stage model lifecycle)

---

## Context

ADR-0001 establishes that Arca ships reference models. ADR-0002 establishes the three-stage lifecycle that takes a reference model through upskilling to production and ongoing maintenance.

A foundational question remains: **what is ArcaAI selling?**

There are two coherent positions:

1. **Pipeline-as-platform** — Arca provides the upskilling and continuous improvement pipeline as the core product. Reference models are the most visible deliverable, but the pipeline that produces, validates, deploys, monitors, and retrains models is what banks adopt. The bank adopts Arca's pipeline as its ML operating environment for the verticals Arca covers.

2. **Models-as-artefacts** — Arca ships reference models and lets banks consume them however they wish, including bolting them into the bank's existing MLOps stack. Arca's pipeline (if any) is optional, used only by banks without existing MLOps capability.

These two positions imply radically different products, sales motions, value propositions, and competitive postures.

## Decision

ArcaAI is a **platform** centred on the upskilling and continuous improvement pipeline. Reference models are inputs to the platform, not the product. Banks adopt Arca's pipeline as their ML operating environment for the verticals ArcaAI covers — they do not bolt Arca's models into existing MLOps and call the engagement complete.

This decision is non-negotiable in product positioning. Banks who explicitly want a model marketplace without pipeline adoption are not the target customer. They will be lost to competitors and that is acceptable.

## Consequences

### Positive

- **Genuine differentiation** — the market has plenty of vendors selling individual models or AI-inside features. Few sell a complete, governed, three-stage pipeline as a platform.
- **Recurring value** — Stage 3 (continuous improvement) is ongoing, not one-time. The pipeline keeps producing value as long as models are in production.
- **Defensible moat** — once a bank's ML operations are running on Arca's pipeline, switching cost is high. This is the difference between vendor and platform.
- **Bigger deal size** — pipeline adoption is a larger commitment than model purchase.
- **The 6-8 weeks claim is achievable** — only because the pipeline does the heavy lifting. Without pipeline-as-platform, 6-8 weeks is implausible.
- **Aligns with the three-stage lifecycle** — the pipeline serves all three stages with shared infrastructure but stage-differentiated governance.

### Negative / costs

- **Harder sale** — banks with existing MLOps invested elsewhere will resist
- **Some markets are lost** — sophisticated AI-mature banks with their own pipelines won't buy this
- **More to build** — the pipeline is the largest engineering deliverable in the platform, not a side-feature
- **Pricing model implications** — recurring platform value justifies recurring fees; one-off model sales don't. Commercial model must align with the platform positioning (deferred to commercial workstream)
- **The Implementation Toolkit is bigger than "a folder of models"** — it includes the pipeline itself, infrastructure-as-code, validation harnesses, monitoring, runbooks

### Specifications affected

- **Product Definition** — the platform positioning is the core of the value proposition; must be communicated from the first paragraph
- **Solution Architecture** — the pipeline is a first-class layer of the architecture, not a hidden implementation detail
- **Technical Architecture** — the pipeline's deployment topology, infrastructure, and integration points are major components
- **Integration Specification** — the pipeline's interfaces to the bank's data warehouse, feature store, identity, secrets, Model Risk governance, and monitoring are critical surfaces
- **Operations and Support Specification** — pipeline operations are the bulk of post-deployment support
- **Implementation Toolkit packaging** — the toolkit centres on the pipeline, with reference models as inputs to it

## Alternatives considered and rejected

**Models-as-artefacts** — rejected. Reduces Arca to a commodity vendor in a market that has plenty of vendors. No moat. No recurring value. Cannot deliver the 6-8 weeks claim.

**Both supported, banks choose** — rejected. Doubles the spec surface, dilutes positioning, and means Arca is competing in two different categories at once. The market does not reward this.

**Pipeline as a paid add-on to model sales** — rejected. Misaligns commercial incentives — banks would consume the cheap option (models) and skip the expensive option (pipeline), undermining the value proposition.
