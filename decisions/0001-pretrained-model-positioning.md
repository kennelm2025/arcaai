# ADR-0001 — Pre-trained model positioning: reference models, not production models

**Status:** Accepted
**Date:** 13 May 2026
**Decider:** Mike Kennelly
**Supersedes:** none

---

## Context

ArcaAI's go-to-market promise includes "first production model live in 6-8 weeks" from engagement start. This is economically possible only if the platform ships with pre-trained ML capability that the bank does not have to build from scratch.

There are three plausible positionings for what "pre-trained" means in this context:

1. **Pre-trained production-ready models** — a bank installs them and they make production decisions on the bank's data from day one
2. **Pre-trained reference models** — Arca trains models on representative data that demonstrate the architecture and approach; the bank upskills them on its own data through Arca's pipeline before production use
3. **Trained-on-synthetic-data demonstrators** — models that prove platform capability but are not represented as suitable for any production use

These three options have radically different implications for liability, data strategy, regulatory accountability, and the credibility of the 6-8 weeks claim.

Option 1 is not achievable on a solo-founder build timeline, would expose Arca to direct model risk liability, and is not in fact what any current banking AI vendor honestly delivers (the appearance of pre-trained production models in vendor pitches is almost always option 2 with looser language).

Option 3 is sufficient for a demo but cannot be sold as part of an Implementation Toolkit. Banks will inspect what they receive.

## Decision

ArcaAI ships pre-trained **reference models**, not production-ready models.

Reference models are:

- Trained by Arca on representative public and synthetic banking data
- Documented with full Model Cards stating intended use, out-of-scope use, training data composition, benchmark performance, and known limitations
- Explicitly positioned as starting points, not endpoints
- Not suitable for, and not authorised for, production decisioning on a bank's customer data

Banks take reference models and upskill them on their own data through ArcaAI's governed training pipeline. The upskilled model — produced inside the bank's perimeter, validated against the bank's data, and approved by the bank's Model Risk governance — is what goes into production.

This decision is non-negotiable language. Marketing, specifications, contracts, and Model Cards must consistently use "reference model" and not "pre-trained production model" or equivalent phrasing.

## Consequences

### Positive

- **Regulatory accountability sits in the right place** — the bank owns the production model; Arca provides the pipeline. This is the difference between being a model vendor (heavy liability, regulated relationship) and being a platform vendor (clean platform liability).
- **The 6-8 weeks claim becomes defensible** — it refers to the time from pipeline deployment to first upskilled production model, with the pipeline doing the work.
- **Reference model benchmarks are public proof points** — Arca can publish them without restrictions because they involve no real bank data.
- **The bank's upskilled model performance is the bank's IP** — never Arca's.
- **Honesty as a moat** — competitors who blur this line are exposed to liability and reputational risk; Arca's clarity becomes a trust signal.

### Negative / costs

- **Sales conversations must lead with reference models, not production models** — sales motion needs to land this distinction early
- **The "we ship you AI" pitch is more nuanced** — buyer education required
- **Every reference model requires a Model Card** — adds production overhead to model development
- **The upskilling pipeline becomes the most important thing to build well** — see ADR-0002 and ADR-0003 for related decisions

### Specifications affected

- **Product Definition** — must use reference-model language consistently
- **Data and ML Specification** — structured around the three-stage lifecycle (see ADR-0002)
- **Security and Compliance Specification** — must address the liability split between Arca and bank
- **Test and Validation Specification** — defines what Model Cards contain and how benchmarks are reported
- **Integration Specification** — defines pipeline integration points with bank's data warehouse and Model Risk tooling

## Alternatives considered and rejected

**Pre-trained production-ready models** — rejected. Not achievable on the build timeline. Exposes Arca to direct model risk liability. Not honestly deliverable for any banking ML use case without bank-specific data.

**Trained-on-synthetic-data demonstrators only** — rejected. Sufficient for demo but insufficient for the Implementation Toolkit. Banks expect to receive starting weights, not just architecture.

**Both production and reference, banks choose** — rejected. Doubles the spec surface, dilutes positioning, and the production option still doesn't work for the underlying reasons above.
