# ADR-0008: BentoML as the platform model-serving framework

* **Status:** Accepted (backfilled)
* **Decision Date:** May 2026 (architecture design phase)
* **Recorded Date:** 2026-06-14
* **Decision Type:** Backfilled
* **Deciders:** Mike Kennelly
* **Relates to:** ADR-0003 (pipeline-as-platform), ADR-0006 (serving model source)
* **Evidence:**

  * ArcaAI Banking Architecture v1.0b, L4 Intelligence Layer, technology components:
BentoML named as the model-serving framework that "standardises the endpoint
pattern across all use cases."
  * Same document, infrastructure-split table: the sensitive-workload column lists
"All ML models (BentoML)" — i.e. every vertical's model, not the fraud model alone.
  * `verticals/fraud/serving/bento\_service.py` at commit `5f4e570` (PR #5, B5/inc1) —
the first concrete implementation of the pattern; the decision is in operation.

> This ADR records a decision already in operation and does not imply it was made on
> the Recorded Date.

## Context

Every ArcaAI use case is built on a tabular model (XGBoost / LightGBM) that must be
served to the agent (L2) as a REST scoring endpoint: one endpoint per use case, returning
a risk band or classification, top contributing features, and a confidence estimate. The
serving layer must provide pre-loaded inference (no cold-load cost), health checks,
metrics, and horizontal scalability, and must present an identical endpoint shape for
every use case so the agent's tool registry can invoke any model the same way.

The architecture (ADR-0003, pipeline-as-platform) treats the upskilling and serving
pipeline — not the individual models — as the product. B10 replicates the fraud vertical
across all other verticals. A serving framework chosen per-vertical would therefore be
re-chosen and re-implemented N times, producing endpoint-shape drift across verticals and
defeating the single-pattern requirement the agent depends on.

The choice of serving framework was made during the May architecture design phase and is
documented in the architecture specification, but was never captured as an ADR. WS-A of
the governance review flagged it (F-005) and the panel ruled (Q-A2) that whether it
warranted a standalone ADR turned on intent: vertical-local would fold into ADR-0006;
platform-standard earns its own ADR. The architecture document resolves the intent
question directly — BentoML is specified as a platform-wide standard ("across all use
cases", "All ML models") — so it earns this ADR.

## Decision

BentoML is the platform model-serving framework for ArcaAI. Every use-case model in every
vertical is served as a BentoML service exposing the standard ML-scoring endpoint contract.
The framework choice is platform-level: a vertical does not select its own serving
framework; it consumes the platform standard.

## Boundary with FastAPI and the agent

BentoML serves *models*. It is not the platform's system-integration API and must not be
conflated with it:

* **FastAPI** is the system-facing REST front door — the stable, schema-validated API
through which integrated banking systems reach the platform (L1).
* **The agent (L2, LangGraph)** is the single entry point and orchestrator; it is the only
caller of the model endpoints. No channel or integrated system calls a BentoML endpoint
directly.
* **BentoML (L4)** sits below both: it is how each model is exposed for the agent to call,
standardised across use cases.

This separation is recorded explicitly because the three were conflated during this
decision's review; the integration API (FastAPI) and the model-serving framework (BentoML)
are distinct platform components at different layers.

## Alternatives considered

* **Per-vertical serving choice** — rejected: defeats the single-endpoint-pattern the
agent's tool registry requires and is re-implemented at every B10 replication.
* **FastAPI-only model serving** (hand-rolled endpoints) — rejected: no pre-loaded
inference, health-check, metrics, or scaling story out of the box; re-implements per model
what BentoML standardises.
* **KServe / Seldon Core** — heavier Kubernetes-native serving meshes; deferred as
disproportionate to the initial deployment, though compatible with the BentoML service
unit if a future scale tier needs them. Not adopted now.

## Consequences

* **Positive.** One endpoint contract across all verticals; the agent invokes any model
identically. B10 replication instantiates the standard rather than re-deciding it.
Pre-loaded inference, health checks, and metrics come from the framework, not per-model
code. Serves the ADR-0003 platform claim with a concrete, shared serving capability.
* **Platform/vertical line.** Confirms the serving framework as a platform-level capability
the vertical consumes (the WS-B P-B3 question, for the serving slice, is answered:
platform). The remaining P-B3 questions — anti-leakage, calibration, provenance — are
still open and decided separately.
* **Obligations. The standard ML-scoring endpoint contract must be defined once at the platform** 

&#x09;**level (request/response schema, feature-contribution and confidence fields, health and metrics surface)**

&#x09;**and inherited by every vertical, not re-specified per vertical. The B5/inc1 fraud bento\_service.py is** 

&#x09;**the reference implementation, and the contract it embodies already sits in the top-level contracts/ directory**

&#x09;**as fraud\_scoring.py — but as a fraud-specific contract. The obligation before vertical #2 is to** 

&#x09;**generalise it into a vertical-neutral scoring contract within that existing contracts/ directory, which each vertical then instantiates.**

* **Interaction with ADR-0006.** ADR-0006 governs *what* the service loads (DVC-pinned,
content-hash-verified, parity-tested model artefacts). ADR-0008 governs *how* it is
served (the BentoML framework and endpoint standard). The two are complementary and
should be read together for the serving design.
* **Open follow-up (not blocking).** Whether the BentoML service unit and the standard
endpoint contract are physically extracted to a `platform/` location, or remain in
`verticals/fraud/` until the platform-extraction step, is a WS-B architecture question
(Q-B4) — recorded there, not resolved here.

