# ArcaAI

A hybrid ML and AI platform for UK and European banks. Reference models, governed upskilling pipeline, continuous improvement — all running inside the bank's perimeter.

This repository is the canonical source of truth for the ArcaAI platform design and specifications. It is the build system from which Implementation Pack releases are produced for bank distribution.

---

> ### 🧭 New here? → **[Start at `START_HERE.md`](START_HERE.md)**
>
> That document is a navigation map. It tells you, by your role and purpose, exactly which documents to open first, in what order, and what you can skip. Reading it takes 5 minutes and saves you an hour of guessing.

---

## Status

**Current phase:** Design — scaffolding complete, specifications in progress.
**Current Implementation Pack version:** none released.
**See:** [`CURRENT_STATE.md`](CURRENT_STATE.md) for the up-to-date weekly snapshot.

## How this repository is organised

```
arcaai/
├── README.md                    You are here
├── START_HERE.md                Navigation map — read this first
├── CONTRIBUTING.md              How to work in this repo
├── CHANGELOG.md                 Release notes per Implementation Pack version
├── PROJECT_CONTEXT.md           Stable context primer for new contributors and AI SMEs
├── CURRENT_STATE.md             Weekly-updated state file — what's happening now
├── SESSION_NOTES.md             Append-only reasoning trail across chat sessions
├── SESSION_PROTOCOLS.md         The opening and closure rituals for every chat session
├── DESIGN_PHASE_CHARTER.md      The constitution of the design phase
│
├── decisions/                   Architectural Decision Records (ADRs)
├── rfcs/                        Request for Comments — proposals before changes
├── specs/                       The eight canonical specifications
├── diagrams/                    Mermaid/PlantUML source for all diagrams
├── glossary/                    Shared canonical glossary
├── governance/                  Document register, SME panel, review protocols
├── archive/                     Legacy ArcaAI documents, retired with provenance
└── .github/                     GitHub configuration
```

## The eight canonical specifications

Every specification follows the same template and goes through the same governance. None has yet been ratified.

| # | Specification | Audience weight | Status |
|---|---|---|---|
| 1 | Product Definition | Bank-side high, engineering low | Not started |
| 2 | Solution Architecture | Bank-side high, engineering medium | Not started |
| 3 | Technical Architecture | Bank-side medium, engineering high | Not started |
| 4 | Data and ML | Bank-side medium, engineering high | Not started |
| 5 | Security and Compliance | Bank-side high, engineering medium | Not started |
| 6 | Integration | Bank-side high, engineering high | Not started |
| 7 | Operations and Support | Bank-side high, engineering high | Not started |
| 8 | Test and Validation | Bank-side high, engineering high | Not started |

See [`specs/README.md`](specs/README.md) for full details.

## Foundational decisions

Three ADRs anchor everything in this repository:

- [**ADR-0001**](decisions/0001-pretrained-model-positioning.md) — Pre-trained model positioning: reference models, not production models
- [**ADR-0002**](decisions/0002-three-stage-model-lifecycle.md) — Three-stage model lifecycle: Reference → Upskilling → Continuous Improvement
- [**ADR-0003**](decisions/0003-pipeline-as-platform.md) — Platform positioning: pipeline-as-platform, not models-as-artefacts

If you read nothing else in this repo, read those three. They constrain everything else.

## How to contribute

See [`CONTRIBUTING.md`](CONTRIBUTING.md). In short:

- Branch off `main`, never commit to it directly
- Significant changes go through an RFC first
- Architectural decisions are recorded as ADRs
- All specifications follow [`specs/_template.md`](specs/_template.md)
- All changes are reviewed before merge

## Confidentiality

This repository is private. Its contents are commercial in confidence. Releases to bank prospects are issued as **Implementation Pack** versioned artefacts, not by granting repository access.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for release mechanics.
