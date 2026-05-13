# Contributing to ArcaAI

This document defines how work is done in this repository. The discipline is not for show — it is what makes the specifications defensible to bank reviewers, auditors, and regulators six months after they were written.

## The cardinal rule

**The repository is the source of truth. Chats, drafts, emails, and side documents are not.** If a decision was made but is not in the repo, it did not happen.

## Branching model

- `main` is protected. Never commit directly.
- All changes happen on feature branches: `branch-name` describes the change in kebab-case (e.g. `spec-04-data-ml-draft`, `adr-0004-vector-db`, `rfc-0002-fairness-testing`).
- Branches are merged via Pull Request, never rebased or force-pushed onto `main`.
- Delete branches after merge.

## What requires what

| Change | Mechanism | Reviewers |
|---|---|---|
| Typo, link fix, formatting | Direct PR | Owner of the file |
| Section rewrite within an existing spec | Direct PR | Spec owner + 1 SME review |
| New ADR | Direct PR with ADR drafted | Mike (final say) |
| Substantive change to a spec's structure or claims | RFC first, then PR | RFC: SME panel (3 rounds); PR: Mike |
| New spec | RFC + ADR + PR | All three rounds of SME review |
| Implementation Pack release | Tag on `main` + GitHub Release | Mike only |

## The RFC process

RFCs (Request for Comments) are how non-trivial proposals are made *before* anyone writes the change.

1. Create a new file in `rfcs/` using `rfcs/_template.md`
2. Number it sequentially: `rfcs/0001-name.md`
3. Open a PR with the RFC alone (no implementation changes)
4. Circulate to relevant SME panel members
5. Discuss inline on the PR; revise the RFC
6. Merge when accepted, withdraw when rejected
7. Implementation happens in a separate PR that references the RFC number

## The ADR process

ADRs (Architectural Decision Records) capture decisions immutably.

1. Create a new file in `decisions/` using `decisions/_template.md`
2. Number it sequentially: `decisions/0001-name.md`
3. State the decision, status, context, consequences
4. Once merged, an ADR is **never edited** — superseded by a newer ADR if the decision changes
5. New ADRs that supersede older ones must reference them explicitly

Status values:
- **Proposed** — under discussion
- **Accepted** — decision is binding
- **Superseded by ADR-NNNN** — no longer in force
- **Deprecated** — context has shifted; new ADR not yet written

## Specifications

All eight canonical specifications live under `specs/` and follow `specs/_template.md`.

### Spec versioning

Each spec has its own semantic version:
- `0.x` — draft, not yet ratified
- `1.0` — first ratified version (all three SME rounds complete, accepted by Mike)
- `1.x` — additive change post-ratification
- `2.0` — breaking change (re-ratification required)

### Spec lifecycle states

Each spec is in one of these states, tracked in `governance/document-register.yaml`:

1. **Not started**
2. **Drafting** — content being written
3. **Round 1 review** — structural review with SME panel
4. **Round 2 review** — content review
5. **Round 3 review** — adversarial review
6. **Ratified** — version 1.0 reached
7. **Maintenance** — versioned changes against ratified base

## Diagrams

Diagrams are committed as **source files** (Mermaid `.mmd` or PlantUML `.puml`), never as image files in the repository.

Rationale: source diagrams can be edited, version-controlled, and rendered consistently. Image files drift and cannot be reviewed.

Rendered images for Implementation Pack releases are produced at release time, not committed to `main`.

See `diagrams/README.md`.

## Glossary

Terms used across multiple specifications live in `glossary/`. No specification re-defines a term that exists in the glossary. If a term is needed and missing, add it to the glossary as part of the same PR.

## Implementation Pack releases

The Implementation Pack is the bank-distributable artefact. It is produced by:

1. Tagging a commit on `main` with `pack-vX.Y.Z`
2. A GitHub Release is created at that tag
3. A zipped artefact is built containing:
   - Rendered PDFs of all ratified specs at their current versions
   - Rendered diagrams (PNG and SVG)
   - Templates and reference artefacts
   - A signed manifest listing each file with its SHA-256 hash and spec version
4. The release notes in `CHANGELOG.md` are updated

Distribution to a specific bank is by:
- **Default:** signed URL to the GitHub Release artefact, time-limited
- **For deeper engagement:** GitHub deploy key giving read-only repo access at a specific tag
- **For air-gapped banks:** physical media handed over with the manifest separately signed

In all cases, the receiving bank knows exactly which Implementation Pack version they have. There is no "latest" — only versioned releases.

## SME panel and review

See `governance/sme-panel.md` and `governance/review-protocols.md` for who reviews what and how.

SME reviews leave a trace in the repository. The reviewing SME's response is committed under the spec's folder as `reviews/round-N-sme-name.md`. Reconciliation decisions are committed alongside as `reviews/round-N-reconciliation.md`. Reviews are part of the audit trail and are not deleted after the round closes.

## Day-one rules of thumb

- If you are about to commit to `main`, you are wrong. Use a branch.
- If you are about to edit an ADR, you are wrong. Write a new one.
- If you are about to "just quickly add a paragraph" to a ratified spec, write an RFC first.
- If a diagram is a `.png`, it cannot be reviewed. Find or write the source.
- If a term is unclear, the answer is in `glossary/`. If it isn't, add it there.
- If you change a spec's sister list, you must change every named sister's sister list to match. Bidirectional integrity is not optional.
