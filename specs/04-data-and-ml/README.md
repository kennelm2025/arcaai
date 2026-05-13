# Data and ML Specification

**Spec number:** 04 of 08
**Version:** 0.0 (placeholder)
**Status:** Not started
**Owner:** Mike Kennelly
**Primary audience:** Arca engineering + bank-side Data and ML reviewers — pipelines, model lifecycle, feature platform

---

## What this specification will contain

When complete, this specification will define **the three-stage model lifecycle** (ADR-0002) in full implementation detail, structured as:

### Part A — Reference modelling (Stage 1)

How Arca builds reference models:

- The reference model catalogue — what verticals are covered, what each model does
- Training data composition per model — which public datasets, which synthetic data sources, lineage
- Training infrastructure and reproducibility
- Model Card standard — what every Model Card contains, in what format
- Benchmarks — public benchmark performance, generalisation tests, fairness baselines, calibration
- Release process — how reference models are versioned, packaged, and shipped in Implementation Pack releases

### Part B — Upskilling pipeline (Stage 2)

How banks upskill reference models on their data:

- Data ingestion — interfaces to the bank's data warehouse, PII handling, lineage
- Feature platform — feature store architecture, feature definitions, computation
- Training pipeline — workflow orchestration, hyperparameter tuning, full audit logging
- Evaluation harness — held-out performance, fairness on protected characteristics, adversarial robustness, calibration, explainability artefacts
- Model Risk evidence pack — what the pipeline produces for the bank's governance process
- Approval and deployment — handoff to bank's Model Risk; shadow-mode comparison; production deployment

### Part C — Continuous improvement (Stage 3)

How upskilled models are maintained in production:

- Monitoring — drift detection (data drift, concept drift, prediction drift)
- Retraining triggers — calendar-based, drift-based, event-based
- Lighter-weight retraining cycle — refresh weights, re-evidence performance, delta-focused review
- Deployment with canary and rollback
- Long-term governance — periodic re-validation against full validation harness

## Why this is spec 04

The pipeline is the platform (ADR-0003). This is the spec where the pipeline is defined in full. Bank Model Risk teams will read this carefully; Arca engineering will build directly from it.

## Reference model and benchmark sub-specifications

The "Reference Models & Benchmarks" detail (data sources, benchmark methodology, model catalogue) lives in Part A of this spec, not as a separate document. Bank Model Risk reviewers reading this section get everything they need to assess reference model credibility.

## Predecessor documents

The current ArcaAI ML Pipeline document is the primary predecessor. Material from the v0.6 Banking Architecture document's Section 5 (MLOps from design to live) will also migrate here.

## Status notes

Not started. Will begin drafting in Month 3 of the design phase, after the core architectural specs (Solution Architecture, Technical Architecture) have established the platform structure within which the pipeline sits.
