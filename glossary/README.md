# Glossary

The shared canonical glossary for ArcaAI. Every term defined here is referenced across multiple specifications. **No specification re-defines a term that exists in the glossary.**

## How to use the glossary

- When writing a specification, look here first before defining a term
- If the term you need is missing, add it here in the same PR as the specification change that needs it
- Definitions are kept short — one or two sentences. The specification can elaborate; the glossary anchors the term.

## Initial terms

This is a starting set. The glossary grows as specifications are written.

---

**ArcaAI** — The hybrid ML and AI platform that this repository specifies. Combines machine learning, agentic orchestration, and open-weight LLMs into a single platform that runs inside a bank's perimeter.

**Reference model** — A pre-trained ML model produced by Arca, trained on representative public and synthetic banking data. Shipped with a Model Card. Not for production decisioning. Starting point for the bank's upskilling process.

**Upskilled model** — A model produced by a bank from a reference model, by training on the bank's own data through Arca's upskilling pipeline. Goes through the bank's Model Risk governance before production use.

**Upskilling** — The process of taking a reference model and training it further on a bank's own data, producing a production-ready model owned by the bank. Stage 2 of the three-stage model lifecycle.

**Continuous improvement** — Ongoing maintenance of upskilled models in production. Includes drift detection, periodic retraining, fairness re-testing. Stage 3 of the three-stage model lifecycle.

**Pipeline** — The end-to-end ML workflow infrastructure that ArcaAI provides. Operates across all three stages of the model lifecycle. The pipeline is the core product (see ADR-0003).

**Implementation Toolkit** — The bank-distributable package containing reference models, the pipeline, supporting infrastructure, runbooks, and the specifications. Released as versioned `pack-vX.Y.Z` artefacts.

**Implementation Pack** — Same as Implementation Toolkit. The terms are interchangeable; "Pack" is used for release versioning, "Toolkit" is used for the artefact in commercial conversations.

**Describer Pack** — The pre-engagement read-only artefact a bank consumes before agreeing to engage. Contains executive narrative, architecture overview, business case, and FAQ.

**Banking Demo** — The Arca-hosted environment a bank uses to see the platform in action before committing. Runs on synthetic data, with three demo verticals (Fraud, Compliance, Relationship Management).

**Model Card** — Standardised documentation describing a model's intended use, training data, performance, limitations, and fairness characteristics. Every reference model ships with one. Every upskilled model produces a new one.

**Model Risk** — The discipline within a bank that governs ML and statistical models in production. Operates under PRA SS1/23 in the UK. Owns the decision on whether an upskilled model can enter production.

**Use case** — A discrete business problem ArcaAI addresses (e.g. transaction fraud detection, AML transaction monitoring, credit decisioning). The platform supports eleven use cases as its starting set.

**Vertical** — A grouping of use cases by business domain (e.g. "Fraud" vertical contains transaction fraud and account takeover; "Compliance" contains AML monitoring and KYC). The Banking Demo features three verticals.

**The perimeter** — The bank's own infrastructure boundary. ArcaAI runs inside the perimeter; the bank's data does not leave it. This is non-negotiable to the platform's positioning.

---

## Terms expected to be added as specifications develop

- Feature store
- Evaluation harness
- Drift detection / data drift / concept drift / prediction drift
- Shadow mode / canary deployment
- Fairness baselines / protected characteristics
- Calibration
- Adversarial robustness
- The five architectural layers (L1 through L5) once Solution Architecture is drafted
- The eleven use cases by name
- Specific regulations (PRA SS1/23, DORA, EU AI Act, etc.) as they're referenced

Add terms to the glossary as they're needed in specifications.
