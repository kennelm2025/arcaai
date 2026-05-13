# Project Context

**Audience:** Anyone — human or AI — picking up work on ArcaAI for the first time, or returning after time away. Read this before doing anything else.

**Stability:** This document changes slowly. Major changes go through PR review like any other content. The day-to-day "what's happening now" lives in `CURRENT_STATE.md`, which changes weekly.

---

## What ArcaAI is

ArcaAI is a hybrid ML and AI platform for UK and European banks. It combines three forms of AI in one architecture:

- **Machine learning** for prediction (fraud, credit, churn, anomaly detection)
- **Agentic orchestration** for multi-step reasoning and policy enforcement
- **Open-weight large language models** for editing, summarisation, and natural-language interfaces

The whole platform runs inside the bank's perimeter — the bank's data does not leave the bank's environment.

ArcaAI wraps around the bank's existing core banking, payments, CRM, and data warehouse. It does not replace them.

## What ArcaAI delivers

The platform ships with eleven banking use cases as a starting set, spanning fraud, compliance, credit, relationship management, and payments. Each use case targets a productivity uplift in the 20-40% range, based on comparable banking deployments.

Use cases are deployed one at a time. Each engagement starts with one, proves value, then expands.

## How ArcaAI is sold and delivered

The go-to-market model is built around three productised assets, each with a distinct role:

1. **Describer Pack** — what the bank reads before engaging. Executive narrative, architecture document, business case, FAQ.
2. **Banking Demo** — what the bank drives to see the platform in action. Hosted by Arca; uses synthetic banking data. Three demo verticals (Fraud, Compliance, Relationship Management).
3. **Implementation Toolkit** — what the bank installs and operates. Reference models, the upskilling pipeline, deployment infrastructure, validation harness, monitoring. **This repository's primary purpose is to specify the Implementation Toolkit.**

A bank engagement runs: Describer Pack → Banking Demo → Implementation Toolkit deployment → first production model in 6-8 weeks → continued use cases over time.

## The three foundational decisions

Everything in this repository is shaped by three decisions captured as ADRs:

### ADR-0001 — Pre-trained model positioning: reference models, not production models

ArcaAI ships pre-trained *reference* models, trained on representative public and synthetic banking data. These are explicitly **not** production-ready. The bank upskills them on its own data before any production use.

This is non-negotiable language. We do not say "pre-trained production models." We say "reference models."

### ADR-0002 — Three-stage model lifecycle

| Stage | Owner | Output | Frequency |
|---|---|---|---|
| Reference modelling | Arca | Pre-trained reference models with Model Cards | One-time per release |
| Upskilling | Bank, using Arca's pipeline | Production-ready model, Model Risk approved | Once at deployment |
| Continuous improvement | Bank, using Arca's pipeline | Drift-triggered retraining | Ongoing |

Banks own the production model. Arca owns the pipeline that creates and maintains it.

### ADR-0003 — Pipeline-as-platform

ArcaAI is a platform centred on the upskilling and continuous improvement pipeline. Reference models are the most visible deliverable; the pipeline is the actual product. Banks adopt the pipeline as their ML operating environment for the verticals ArcaAI covers — they do not bolt Arca's models into existing MLOps and call it done.

## What we are building right now

The current phase is **design**. The goal is to produce eight canonical specifications that constitute the Implementation Toolkit's blueprints, ratified through a three-round SME review process and assembled into Implementation Pack v1.0.

Target timeline: 4-6 months from May 2026.
Working time available: approximately 3 hours per day, weekdays only.

The eight specifications are:

1. **Product Definition** — what ArcaAI is, for whom, with what outcomes
2. **Solution Architecture** — the five-layer architecture, components, interfaces
3. **Technical Architecture** — technology choices, deployment topology, infrastructure
4. **Data and ML** — pipelines, model lifecycle, feature platform
5. **Security and Compliance** — AI-specific controls, regulatory mapping
6. **Integration** — how ArcaAI connects to the bank's existing systems
7. **Operations and Support** — MLOps, observability, SLAs, support
8. **Test and Validation** — validation harness, benchmarks, Model Risk evidence

## Who works on ArcaAI

- **Mike Kennelly** — Founder. Bank CTO/CDAO/architect (35 years in banking architecture). Imperial College London AI professional graduate. Final say on everything. Three hours per day.
- **Claude (Anthropic)** — Day-to-day production partner. Drafts, challenges, integrates, maintains repository hygiene. Works in chat sessions with this repository as the persistent state.
- **SME Panel** — ChatGPT, Grok, DeepSeek, Mistral, Gemini, NotebookLM, Perplexity. Each used for specific review roles. See `governance/sme-panel.md` for full composition. No SME accepts anything; SMEs critique; Mike decides.

## The working method, in one paragraph

Mike works three hours a day in chat with Claude. Production output is committed to this repository at the end of each session. Each Friday, that week's outputs are packaged and submitted to the SME panel for review according to the round-by-round protocol in `governance/review-protocols.md`. Mike reads SME critiques the following Monday, adjudicates, and the agreed changes feed back into Tuesday-Thursday production. The whole rhythm is designed to absorb SME review latency into wall-clock time rather than make it block production.

## What this repository is not

- It is not a code repository — there is no source code here, only specifications and governance artefacts
- It is not a wiki — every document has a clear role and follows a template
- It is not shared with banks directly — banks receive Implementation Pack release artefacts, not access to this repo
- It is not a place for drafts and side-thinking — those live elsewhere; only finished and committed work lives here

## What every contributor needs to do before producing anything

1. Read this document
2. Read `CURRENT_STATE.md` for what's happening this week
3. Read the three ADRs (`decisions/0001.md`, `0002.md`, `0003.md`)
4. Read `CONTRIBUTING.md` for the working rules
5. If working on a specific spec, read `specs/_template.md` and the spec's existing `README.md`
6. If working as an SME reviewer, read your primer in `governance/sme-prompt-primers/`

If you are an AI assistant being given this file as context: do not assume capabilities beyond what is written here. Ask Mike before making decisions that aren't captured in this file or the ADRs.
