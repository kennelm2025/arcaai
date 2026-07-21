> **RETIRED — July 2026 (WS-C).** This section was never populated; the spec regime it belongs to is superseded. See `../README.md` and /DECISIONS.md (DEC-0007).

# Integration Specification

**Spec number:** 06 of 08
**Version:** 0.0 (placeholder)
**Status:** Not started
**Owner:** Mike Kennelly
**Primary audience:** Bank-side architects, integration engineering, Arca delivery — the contracts and interfaces

---

## What this specification will contain

When complete, this specification will define:

- **What the bank's systems must expose** for ArcaAI to operate
- **The integration patterns supported** — API-based, event-driven, batch, hybrid
- **Required interfaces to:**
  - Core banking platform — read access to customer, account, transaction data
  - Payments platform — transaction streams for fraud and AML
  - CRM — customer and relationship data for RM use cases
  - Data warehouse — historical data for training and analytics
  - Identity and Access Management — authentication, authorisation, role mapping
  - Secrets management — key management, certificate management
  - Model Risk governance tooling — evidence pack delivery, approval workflow integration
  - Observability stack — log aggregation, metrics, alerting
  - Incident management — ticketing integration for AI-specific incidents
- **Data contracts** — schemas, formats, freshness requirements, completeness expectations
- **Security at the boundary** — encryption in transit, mutual TLS, network segmentation requirements
- **Operational contracts** — SLAs the bank's systems must meet for ArcaAI to operate; SLAs ArcaAI provides back
- **Reference integration patterns** for the common UK core banking platforms (Temenos T24/Transact, FIS Profile, Mambu, others as needed)

## Why this is spec 06

Integration is where Arca engagements live or die operationally. A spec that is vague here will be filled in by ad-hoc decisions during delivery, which is how engagement scope balloons and timelines slip.

This spec is rated High for both audiences — bank-side architects need to know what they're signing up for; Arca delivery engineering needs precise interfaces to build to.

## Relationship to other specs

- **Solution Architecture** defines the platform's external interfaces; this spec defines what's on the other side of them
- **Technical Architecture** defines the technologies the platform uses; this spec defines the technologies it integrates with
- **Security and Compliance** governs how integration happens securely; this spec defines the integration mechanics
- **Operations and Support** governs how integration is operated; this spec defines what is operated

## Status notes

Not started. Will begin drafting in Month 3-4 of the design phase, parallel with Security and Compliance.
