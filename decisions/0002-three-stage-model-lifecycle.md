# ADR-0002 — Three-stage model lifecycle

**Status:** Accepted
**Date:** 13 May 2026
**Decider:** Mike Kennelly
**Supersedes:** none
**Related:** ADR-0001 (pre-trained model positioning), ADR-0003 (pipeline-as-platform)

---

## Context

Given ADR-0001's decision that ArcaAI ships reference models that banks upskill before production use, the model lifecycle has multiple distinct stages with different owners, governance weights, and infrastructure needs.

An incomplete framing of this lifecycle leaves critical questions unanswered:

- Where does the reference model come from?
- What happens when a bank takes a reference model and applies it to its data?
- What happens to the resulting model in production over time as data and conditions drift?

Without an explicit lifecycle structure, the specifications would conflate these stages or address them partially, leading to gaps that bank Model Risk teams would identify in review.

## Decision

The ArcaAI model lifecycle has three explicit stages, each with distinct ownership, output, and governance:

### Stage 1 — Reference modelling

- **Owner:** Arca
- **Output:** Pre-trained reference models with Model Cards
- **Frequency:** One-time per model release; updated when underlying architecture, training data, or benchmark methodology changes
- **Governance:** Arca's internal model release process; published benchmarks; Model Card includes lineage and reproducibility information
- **Data:** Public banking datasets (Lending Club, Freddie Mac, IEEE-CIS Fraud, BAF, others to be specified) plus synthetic banking data generated within Arca's environment
- **Validation:** Public benchmark performance, generalisation tests across datasets, fairness baselines, calibration

### Stage 2 — Upskilling

- **Owner:** Bank, using Arca's pipeline
- **Output:** Production-ready upskilled model, approved by the bank's Model Risk governance
- **Frequency:** Once at deployment per use case; full re-runs are rare events triggered by architectural change or data regime shift
- **Governance:** The bank's Model Risk lifecycle (development → independent validation → approval → deployment). Arca's pipeline produces the evidence pack; the bank's process makes the decision.
- **Data:** The bank's own customer and operational data, accessed within the bank's perimeter
- **Validation:** Performance on bank's held-out data, fairness on bank's protected characteristics, explainability artefacts, adversarial robustness, calibration on bank's data, shadow-mode comparison to existing production if any

### Stage 3 — Continuous improvement

- **Owner:** Bank, using Arca's pipeline
- **Output:** Drift-triggered retraining; ongoing maintenance of the production model
- **Frequency:** Continuous monitoring; retraining triggered by drift detection, calendar policy, or significant data regime change
- **Governance:** Lighter-touch than Stage 2 because architecture is already validated; refresh weights and re-evidence performance against held-out data; approval threshold defined by the bank's Model Risk policy
- **Data:** Recent bank data, accumulated since previous training cycle
- **Validation:** Drift metrics, delta-focused performance review, fairness re-test, calibration re-check, deployment with canary/rollback

## Consequences

### Positive

- **Each stage has a clear owner and clear governance weight** — avoiding the trap of "who's responsible for the production model?" being ambiguous
- **The specifications can be structured around the lifecycle** — Data and ML Spec has three clearly-bounded sections; Security and Compliance Spec addresses three distinct risk profiles
- **The MLOps loop (Stage 3) gets first-class treatment** — banks who think they bought "an AI" and discover six months later that they bought "an AI maintenance liability" are the ones who never buy again; treating Stage 3 as a peer of Stages 1 and 2 forces the platform to earn long-term trust
- **The pipeline architecture must support all three with shared infrastructure** but stage-differentiated governance weights — this is a concrete engineering requirement, not vague

### Negative / costs

- **Banks must accept that they own Stages 2 and 3** — some banks will want Arca to take more responsibility; the position must hold
- **The pipeline is more complex than a "training script"** — full lifecycle support is significantly more engineering than minimum-viable ML training
- **Monitoring and drift detection (Stage 3) is a hard problem** that's easy to get wrong — must be specified carefully

### Specifications affected

- **Data and ML Specification** — restructured around the three stages
- **Security and Compliance Specification** — each stage has its own regulatory profile (Stage 1: data provenance, synthetic data governance; Stage 2: PII handling, Model Risk integration; Stage 3: drift accuracy, change management to live production model)
- **Operations and Support Specification** — Stage 3 is operations, not development; sits primarily in this spec
- **Test and Validation Specification** — validation harness behaviour differs by stage
- **Integration Specification** — pipeline must integrate with bank's data warehouse, feature store, Model Risk governance tooling at Stage 2 and Stage 3

## Alternatives considered and rejected

**Two-stage lifecycle (Reference + Upskilling only)** — rejected. Treats post-deployment as out of scope. Banks need ongoing maintenance and Arca's pipeline must provide it.

**Single-stage lifecycle (Reference, banks do everything else themselves)** — rejected. Incompatible with ADR-0003 (pipeline-as-platform). Reduces Arca to model marketplace.

**Four or more stages** (e.g. splitting upskilling into "initial training" and "first deployment") — rejected. The pipeline runs as one logical process at Stage 2; sub-dividing it artificially complicates governance without adding clarity.
