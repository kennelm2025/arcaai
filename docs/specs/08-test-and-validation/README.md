# Test and Validation Specification

**Spec number:** 08 of 08
**Version:** 0.0 (placeholder)
**Status:** Not started
**Owner:** Mike Kennelly
**Primary audience:** Bank-side Model Risk + Arca engineering — the evidence pack and CI test suite

---

## What this specification will contain

When complete, this specification will define:

- **The validation harness** — the executable test infrastructure that runs at each stage of the model lifecycle
- **Validation at Stage 1 (Reference modelling):**
  - Public benchmark performance
  - Cross-dataset generalisation tests
  - Fairness baselines on representative protected characteristics
  - Calibration checks
  - Reproducibility tests (same training data + same seed = same model)
- **Validation at Stage 2 (Upskilling):**
  - Performance on bank's held-out data
  - Fairness testing on bank's actual protected characteristics
  - Adversarial robustness tests
  - Explainability artefact generation (SHAP, LIME, counterfactuals)
  - Calibration on bank's data
  - Shadow-mode performance vs existing production model
- **Validation at Stage 3 (Continuous improvement):**
  - Drift detection accuracy
  - Delta-focused performance review
  - Fairness re-test
  - Calibration re-check
  - Canary deployment performance
- **The Model Risk evidence pack** — what the validation harness produces at each stage for the bank's Model Risk governance to consume
- **Independent validation requirements** — what the bank's independent validation team needs to do its own work (data access, model access, source code review if applicable, etc.)
- **Test infrastructure** for the platform itself — CI/CD test suites, integration tests, end-to-end tests, performance tests
- **Acceptance criteria** for each validation type — what passes, what fails, what requires investigation

## Why this is spec 08

Bank Model Risk functions read this specification first when evaluating whether to deploy an upskilled model. If the validation evidence is thin or unconvincing, the model does not deploy regardless of how well it performs.

This spec is also where engineering's test discipline is defined — the validation harness is real, executable code, and the CI pipelines must run it.

## Relationship to Data and ML

Where Data and ML (spec 04) defines what the pipelines *do*, Test and Validation (spec 08) defines how we *know* they did it correctly. The two specs are tightly coupled — changes in one will frequently imply changes in the other.

The separation is deliberate: Model Risk functions in banks read validation as a separate concern from training. Engineers also benefit from the separation — validation has its own owners, its own discipline, and its own evolution.

## Status notes

Not started. Will begin drafting in Month 4 of the design phase, parallel with Operations and Support. Both follow once the architecture, pipeline, and security/integration specs are sufficiently mature.
