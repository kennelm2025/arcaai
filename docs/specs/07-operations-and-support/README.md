> **RETIRED — July 2026 (WS-C).** This section was never populated; the spec regime it belongs to is superseded. See `../README.md` and /DECISIONS.md (DEC-0007).

# Operations and Support Specification

**Spec number:** 07 of 08
**Version:** 0.0 (placeholder)
**Status:** Not started
**Owner:** Mike Kennelly
**Primary audience:** Bank-side operations + Arca support delivery — running the platform in production

---

## What this specification will contain

When complete, this specification will define:

- **MLOps in production** — how the three-stage model lifecycle is operated day-to-day
  - Monitoring dashboards and metrics
  - Drift detection operations
  - Retraining cadences and triggers
  - Model deployment, canary, and rollback procedures
- **Platform operations** — running the platform infrastructure
  - Health checks, liveness, readiness
  - Capacity management
  - Backup, recovery, business continuity
  - Upgrade procedures (platform version, dependencies, security patches)
- **Observability** — what is observed, where it is observed
  - Logging strategy and retention
  - Metrics and SLI/SLO definitions
  - Alerting rules and escalation paths
  - Distributed tracing for end-to-end query flows
- **Incident response** — how the platform is supported when things go wrong
  - Severity definitions
  - On-call structure and rotation (initially Arca; transitions to bank or shared model over time)
  - Runbooks per incident category
  - Post-incident review process
- **SLAs** — service level commitments
  - Platform availability targets
  - Latency targets (per use case)
  - Pipeline run-time targets (upskilling cycle, retraining cycle)
  - Response and resolution targets per incident severity
- **Support model** — tiers, escalation, knowledge transfer
  - Pre-deployment support (during engagement)
  - Post-deployment support (steady-state operations)
  - Knowledge transfer to bank's own teams over time
  - Continuous improvement of runbooks based on real incidents

## Why this is spec 07

Banks who buy AI platforms and lack operational rigour end up with a black box that nobody can support. This spec is what prevents that — it makes operations explicit, runnable, and supportable.

It is also the spec that converts "ArcaAI is a platform you deploy" into "ArcaAI is a platform you operate." Without strong operations specification, the platform claim is hollow.

## Status notes

Not started. Will begin drafting in Month 4 of the design phase, after Solution Architecture, Technical Architecture, and the core of Data and ML are stable.
