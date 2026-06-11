# Design Phase Charter

**Status:** Draft v0.1 — awaiting first SME review round
**Owner:** Mike Kennelly
**Last updated:** 13 May 2026

This document is the constitution of the ArcaAI design phase. It defines what the design phase produces, how it is governed, who participates, and how long it takes.

It is deliberately lean. The full Design Phase Plan (formal Word document) is produced from this Charter at the end of Month 1 once the working method has proven itself.

---

## 1. Purpose

The design phase produces the **canonical specifications** that constitute the ArcaAI Implementation Toolkit. These specifications serve two audiences in the same document set:

- **Bank-side reviewers** — CTOs, CDAOs, Model Risk, InfoSec, Procurement — who read for assurance
- **Arca engineering** — who read for buildability

Each specification is **implementation-ready** at v1.0 — a developer can pick up a spec and build the component from it; a bank reviewer can pick up a spec and assess whether they would buy it.

## 2. Scope

In scope for the design phase:

- Eight canonical specifications (listed in section 3)
- Three foundational ADRs (already ratified)
- The governance infrastructure that maintains spec quality over time
- The Implementation Pack release model
- Specifications standards (template, diagram conventions, glossary, naming)

Out of scope for the design phase:

- Building the demo (separate workstream, starts Month 5-6)
- Building the toolkit (specifications-led; build follows ratification)
- Commercial terms, pricing, contracts (separate workstream)
- Sales material beyond the Describer Pack (separate workstream)
- The pre-trained reference models themselves (data and model build is its own workstream; this phase specifies the architecture they sit within)

## 3. The eight canonical specifications

| # | Specification | Primary role |
|---|---|---|
| 1 | Product Definition | What ArcaAI is, who it's for, what it delivers. The bank's first read. |
| 2 | Solution Architecture | The five-layer architecture, components, interfaces, data flows. The reference architecture. |
| 3 | Technical Architecture | Technology choices, deployment topology, infrastructure, scaling characteristics. |
| 4 | Data and ML | The three-stage model lifecycle, feature platform, pipelines, training infrastructure. |
| 5 | Security and Compliance | AI-specific controls, regulatory mapping (PRA SS1/23, FCA, GDPR, EU AI Act, DORA). |
| 6 | Integration | How ArcaAI connects to core banking, payments, CRM, data warehouse, IAM. |
| 7 | Operations and Support | MLOps, observability, incident response, SLAs, support model. |
| 8 | Test and Validation | Validation harness, benchmarks, Model Risk evidence pack, fairness testing. |

Every specification follows `specs/_template.md`. None has been ratified yet.

## 4. The four governance pillars

The design phase rests on four governance pillars. None is optional.

### Pillar 1 — The canonical specification set

The eight specs above, each with one clear role and audience weighting. No duplication, no drift, no rogue documents.

### Pillar 2 — Specification governance

- Document register (`governance/document-register.yaml`) — machine-readable status per spec
- RFC process — proposals before changes
- ADR process — decisions captured immutably
- Versioning — semantic versioning per spec, plus Implementation Pack versioning at release
- Quarterly review cadence post-ratification

### Pillar 3 — Repository and release engineering

- Private GitHub repository as source of truth
- Branch protection on `main`
- PR-based change flow
- Implementation Pack release artefact built from tagged commits
- Distribution to banks via signed-URL release artefacts or deploy keys, not raw repo access

### Pillar 4 — Specification standards

- One spec template, all eight follow it
- One ADR template
- One RFC template
- Diagrams as source files (Mermaid/PlantUML), never as images in `main`
- Shared glossary, no spec redefines terms
- Consistent component naming across all specs

## 5. The SME review panel

The SME panel is the quality filter that catches what a single author misses. Full composition in `governance/sme-panel.md`. In summary:

| Role | Who |
|---|---|
| Bank CTO/CDAO/architect — **final say** | Mike Kennelly |
| AI engineering critique | DeepSeek (primary), ChatGPT (secondary) |
| Structural critique | Grok |
| Regulatory reviewer | Mistral Le Chat |
| Regulatory currency check | Perplexity Pro (research, not review) |
| Cross-document consistency | NotebookLM |
| Fresh-eyes pass | Claude (clean session) |
| Day-to-day production | Claude (this working session) |

The panel reviews each specification through **three rounds**:

- **Round 1 — Structural review** (3-4 days wall-clock)
- **Round 2 — Content review** (3-4 days wall-clock)
- **Round 3 — Adversarial review** (3-4 days wall-clock)

After Round 3, Mike decides whether to accept v1.0. Full protocol in `governance/review-protocols.md`.

**Honest framing:** AI SMEs are well-read amateurs, not domain specialists. They catch structural gaps, logical inconsistencies, and shallow errors brilliantly. They do not give legal opinions, predict regulator behaviour, or replace a Big Four compliance review when one is eventually needed. The panel is a quality filter, not a fitness-for-purpose certificate.

## 6. Working method

Three hours per day, weekdays, with Claude as production partner.

### Daily shape

| Block | Duration | Activity |
|---|---|---|
| Production | 60 min | New content drafted with Claude |
| Review integration | 45 min | SME critiques adjudicated; agreed changes merged |
| Governance | 30 min | Repo hygiene; register updates; review queue prep |
| Flexible | 45 min | Whatever the day needs |

### Weekly rhythm

- **Monday** — Read SME critiques from prior week; produce review verdicts; merge agreed changes
- **Tuesday-Thursday** — Production-heavy; new spec content
- **Friday** — Submit the week's outputs to the SME panel; tag any releases; commit weekly state update

### Context preservation across chats

The repository is the source of truth. Every chat session ends by committing outputs back to the repo. Every chat session starts by reading `PROJECT_CONTEXT.md` and `CURRENT_STATE.md`. Chats are transient; the repo is persistent.

## 7. Timeline

| Month | Focus | Key deliverables |
|---|---|---|
| 1 | Foundations | Scaffold ratified; rationalisation map; first spec to ~50%; ADR-0004, 0005 on target market and data |
| 2 | Core specs round 1 | Product Definition, Solution Architecture, Technical Architecture at v0.9 |
| 3 | Core specs to v1.0; detail specs draft | Specs 1-3 ratified. Specs 4, 5, 6 drafted. |
| 4 | Detail specs to v1.0; final specs draft | Specs 4, 5, 6 ratified. Specs 7, 8 drafted. |
| 5 | Final specs to v1.0; Pack v1.0 release | All eight specs at v1.0. Implementation Pack v1.0 released. Demo build scope locked. |
| 6 | Demo build; Pack v1.1 polish | Working demo. Pack v1.1 with feedback from demo build. |

## 8. Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Process-over-product trap | Medium | High | Charter time-boxed; spec production starts Week 2 |
| SME review latency exceeds plan | Medium | Medium | Specs in parallel; review batched; flexible round count |
| Strategic questions stay open too long | Medium | High | Target market and data strategy ADRs ratified by end of Month 2 |
| Existing-doc rationalisation drags | Low | Medium | Scoped as 2-day exercise; archive aggressively |
| Mike's hours interrupted by other work | Medium | High | 3 hours per day target; weekly status flags if at risk |
| Spec template wrong, propagates errors | Low | High | Template reviewed by SME panel before first spec uses it |
| Context loss between Claude chats | Low | Medium | PROJECT_CONTEXT + CURRENT_STATE + repo as state |

## 9. Definition of done for the design phase

The design phase is complete when:

1. All eight canonical specifications are at version 1.0 (three SME rounds complete, accepted by Mike)
2. Implementation Pack v1.0 has been released as a tagged GitHub Release with full manifest
3. The Banking Demo has been built and reflects the ratified specifications
4. The Describer Pack has been assembled from the ratified Product Definition, Solution Architecture, executive presentation, and business case
5. At least one bank prospect has received an Implementation Pack and provided a structured response

This Charter is itself subject to revision. If the working method proves wrong, this document changes — but only through a normal PR with stated reasons.
