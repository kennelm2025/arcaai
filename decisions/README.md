# Architectural Decision Records (ADRs)

ADRs are immutable records of architecturally significant decisions. They capture **what was decided**, **why**, **what alternatives were rejected**, and **what consequences flow from the decision**.

ADRs exist to answer the question "why is the system like this?" six months or six years after the decision was made, when the people who made it may have forgotten or moved on.

## How to write an ADR

1. Copy `_template.md` to `NNNN-short-name.md` where `NNNN` is the next sequential number
2. Fill in every section
3. Open a PR
4. Discuss inline
5. Merge when accepted; the ADR's status changes from `Proposed` to `Accepted` at merge time

## Immutability

Accepted ADRs are **not edited**. Ever. If the decision changes:

1. Write a new ADR that captures the new decision
2. The new ADR's `Supersedes:` field references the old ADR
3. The old ADR's `Status:` changes to `Superseded by ADR-XXXX`
4. The old ADR's content is otherwise unchanged

This is how the system maintains a defensible audit trail. A bank reviewer can read the history of decisions and see how thinking evolved.

## What counts as "architecturally significant"?

An ADR is appropriate when:

- The decision shapes how multiple specifications are written
- Reversing the decision would require substantial rework
- The decision involves a trade-off between alternatives that future readers will want to understand
- The decision implies specific language, naming, or behaviour that must be consistent across the codebase or document set

An ADR is not needed for:

- Editorial choices (tone, formatting)
- Tactical implementation decisions inside a single specification
- Decisions that are obvious applications of an existing ADR

## Index

| ADR | Title | Status |
|---|---|---|
| [0001](0001-pretrained-model-positioning.md) | Pre-trained model positioning: reference models, not production models | Accepted |
| [0002](0002-three-stage-model-lifecycle.md) | Three-stage model lifecycle (Reference → Upskilling → Continuous Improvement) | Accepted |
| [0003](0003-pipeline-as-platform.md) | Platform positioning: pipeline-as-platform | Accepted |
