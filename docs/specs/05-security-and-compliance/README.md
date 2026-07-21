> **RETIRED — July 2026 (WS-C).** This section was never populated; the spec regime it belongs to is superseded. See `../README.md` and /DECISIONS.md (DEC-0007).

# Security and Compliance Specification

**Spec number:** 05 of 08
**Version:** 0.0 (placeholder)
**Status:** Not started
**Owner:** Mike Kennelly
**Primary audience:** Bank-side InfoSec, Model Risk, Compliance — the evidence pack

---

## What this specification will contain

When complete, this specification will define:

- **AI-specific security controls** layered on top of the bank's existing security architecture — the platform inherits the bank's existing controls and adds AI-specific ones
- **Three-stage governance profiles** (per ADR-0002):
  - Stage 1 controls — data provenance for Arca's training data, synthetic data governance, Model Card standards
  - Stage 2 controls — PII handling during upskilling, audit logging, Model Risk integration
  - Stage 3 controls — drift detection accuracy, change management to a live production model
- **Regulatory mapping** to:
  - PRA SS1/23 (Model Risk Management)
  - FCA Handbook relevant sections (SYSC, SUP, GENPRU)
  - GDPR (data protection)
  - EU AI Act (high-risk AI system requirements)
  - DORA (operational resilience for ICT)
  - Future-state: relevant UK AI regulation as it emerges
- **Liability split** between Arca and the bank — clear, contractable
- **Audit trail requirements** — what the platform must log, retain, and produce on demand
- **Identity, access, and secrets management** — integration with the bank's IAM
- **Incident response** for AI-specific events — model failure, drift triggering false outputs, adversarial input detection

## Why this is spec 05

Bank InfoSec and Model Risk read this first when evaluating ArcaAI. If this specification is thin, the engagement does not proceed regardless of how good the rest of the platform is.

This spec is also the most regulation-touching, which is why it gets the heaviest review weighting from the regulatory reviewer (Mistral Le Chat) and currency check (Perplexity Pro).

## Cross-cutting nature

This specification touches every other specification:

- **Product Definition** — the platform's regulatory positioning
- **Solution Architecture** — security controls as architectural elements
- **Technical Architecture** — security infrastructure (secrets, encryption, network segmentation)
- **Data and ML** — data governance through the three stages
- **Integration** — secure integration with bank systems
- **Operations and Support** — security operations, incident response
- **Test and Validation** — security testing, adversarial robustness, fairness

It will be reviewed alongside every other spec, not just on its own.

## Status notes

Not started. Will begin drafting in Month 3-4 of the design phase, when the architecture and pipeline are stable enough for security overlays to be specified concretely.

This spec needs the most up-to-date regulatory reading. Perplexity Pro will be used during drafting to verify current state of key regulations (which clauses are in force, which are under consultation, which have been amended).
