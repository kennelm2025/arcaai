# ArcaAI

**The AI control layer for regulated banking decisions.**

ArcaAI is a hybrid AI platform — calibrated predictive ML, grounded LLM narrative, and
agentic orchestration — built UK-first (PRA/FCA) with full data sovereignty: all customer
data, ML inference, and LLM serving on-premises. This repository is the single monorepo
for everything: application code, ML code, IaC, prompt templates, and governance
(Engineering Blueprint §4).

## State

The document suite was **locked June 2026** (rulings R1–R13, ADR-000–003 — see
[DECISIONS.md](DECISIONS.md)). The build is the **reference implementation on synthetic
data**: 12 gated stages B1–B12 ([BUILD_TRACKER.md](BUILD_TRACKER.md)), founder-led,
gate-not-date discipline. Phase 1 scope: **Fraud, Compliance, Relationship Management** —
3 of an 11-use-case catalogue, 9 by Phase 2.

## Repo map

| Path | Contents |
|---|---|
| `agent/` | LangGraph agent + tools + versioned prompt templates (B6) |
| `api/` | FastAPI application — health/version live; query endpoint from B5/B6 |
| `verticals/` | Per-vertical ML: features, training, serving, evaluation, tests (fraud first) |
| `ingest/` | Document ingest pipeline (B7) |
| `contracts/` | Contract-first specs — API schemas, BentoML endpoint specs |
| `infra/` | docker-compose dev stack now; Terraform/k8s as infra hardens |
| `monitoring/` | Grafana dashboards + Evidently drift configs (B11) |
| `data/` | DVC pointers only — raw data never enters git |
| `docs/` | Locked governance suite, specs, reviews, build gate records |
| `decisions/` | Per-ADR files; indexed by DECISIONS.md |
| `diagrams/` | Diagram sources incl. ADR-000 image-round inputs |

## Quickstart (dev)

```
pip install -e ".[dev]"
scripts\dev_up.cmd      # Postgres :5432 + MLflow UI :5000 (Docker required)
scripts\test.cmd        # pytest + coverage gate
scripts\dvc_init.cmd    # one-time DVC init, local remote
```

## Governance

Locked documents live in `docs/governance/` and change **via decision record only**.
The build tracker is the living status. Doc–code drift = ADR, or it didn't happen.
