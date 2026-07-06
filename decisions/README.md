# Architectural Decision Records (ADRs)

ADRs are immutable records of architecturally significant decisions. They capture what was
decided, why, what alternatives were rejected, and what consequences flow from the decision.

ADRs exist to answer the question "why is the system like this?" six months or six years
after the decision was made, when the people who made it may have forgotten or moved on.

## How to write an ADR

1. Copy `_template.md` to `NNNN-short-name.md` where `NNNN` is the next sequential number.
2. Fill in every section, including the front-matter fields (`Decision Date`,
   `Recorded Date`, `Decision Type`, `Evidence`).
3. Open a PR.
4. Discuss inline.
5. Merge when accepted; the ADR's status changes from `Proposed` to `Accepted` at merge time.

## Immutability

Accepted ADRs are not edited. Ever. If the decision changes:

1. Write a new ADR that captures the new decision.
2. The new ADR's `Supersedes:` field references the old ADR.
3. The old ADR's `Status:` changes to `Superseded by ADR-XXXX`.
4. The old ADR's content is otherwise unchanged.

An ADR is not immutable until it is committed. A `git mv` or an uncommitted file is not
under version control and therefore not yet part of the audit trail; commit before treating
a decision as recorded.

This is how the system maintains a defensible audit trail. A bank reviewer can read the
history of decisions and see how thinking evolved.

## Backfilled ADRs

Some decisions were made and put into operation before they were captured as ADRs. These
are recorded honestly rather than rewritten as if they were contemporaneous:

- `Decision Type: Backfilled`
- `Status: Accepted (backfilled)`
- `Evidence:` cites where the decision already lives (a commit SHA, a `DEC-` entry, a code
  comment, or a design document) so a reviewer can verify it was in operation.
- The body carries the disclosure sentence: "This ADR records a decision already in
  operation and does not imply it was made on the Recorded Date."

A backfilled ADR is still a real, binding decision; the disclosure only fixes its provenance.

## What counts as "architecturally significant"?

An ADR is appropriate when:

- The decision shapes how multiple specifications are written.
- Reversing the decision would require substantial rework.
- The decision involves a trade-off between alternatives that future readers will want to
  understand.
- The decision implies specific language, naming, or behaviour that must be consistent
  across the codebase or document set.

An ADR is not needed for:

- Editorial choices (tone, formatting).
- Tactical implementation decisions inside a single specification.
- Decisions that are obvious applications of an existing ADR.

## Numbering and namespaces

Reference ADRs in the four-digit form `ADR-0001`, not `ADR-1` or `ADR-001`.

Numbers are claimed when a decision is named (including deferred ADRs cited in planning
docs), not only when the file is written. To prevent a cited number resolving to nothing,
a reserved ADR must have a stub file present (`Status: Reserved`, with owner, reason, and
target date) - we do not reserve a number with no file behind it. Reserved-but-unwritten
ADRs are listed in the index so the next number is never double-booked.

`DECISIONS.md` is a separate lightweight ledger for build- and design-log decisions. Its
entries use the form `DEC-NNNN` and must never use `ADR-NNNN` - the four-digit `ADR-` form
belongs to this folder only, and means exactly one thing. The two instruments record
different tiers of decision at different authority levels; the identifier makes the tier
unambiguous to a reviewer running a traceability check.

## Index

| ADR | Title | Status |
| --- | --- | --- |
| 0001 | Pre-trained model positioning: reference models, not production models | Accepted |
| 0002 | Three-stage model lifecycle (Reference -> Upskilling -> Continuous Improvement) | Accepted |
| 0003 | Platform positioning: pipeline-as-platform | Accepted |
| 0004 | Target market segment (gates Spec 01 §6) | Reserved (stub) |
| 0005 | Data strategy | Reserved (stub) |
| 0006 | Serving model source: DVC-pinned artefacts, not an MLflow Registry | Accepted |
| 0007 | Artefact store: DVC as the artefact source-of-truth | Accepted (backfilled) |
| 0008 | Model-serving framework: BentoML as the platform standard | Accepted (backfilled) |
| 0009 | Platform/vertical capability boundary and the Platform Extraction gate (B9.5) | Accepted |

> **Audit note (dangling-reference sweep, June 2026 - resolved by the governance review,
> Workstream A).** The earlier sweep flagged three issues, now dispositioned:
>
> - **Namespace collision (was Critical).** Two parallel `ADR-` series collided across
>   `decisions/` and `DECISIONS.md` at 001/003/004. Resolved by convention: the
>   `DECISIONS.md` series is renamed to `DEC-NNNN`. Execution (the rename plus citation
>   updates in `generator.py`, `B3_GATE.md`, `CURRENT_STATE.md`, `BUILD_TRACKER.md`) is
>   tracked as Must-Fix CL-01.
> - **`ADR-000`.** Confirmed: it is a real, open decision in the `DECISIONS.md` series (the
>   image-round gate on client use), not a missing formal ADR. It becomes `DEC-0000` under
>   the rename above. No formal ADR is owed.
> - **`ADR-0004` / `ADR-0005`.** Legitimately reserved strategic ADRs, now backed by stub
>   files per the no-empty-reserve rule above (gating Spec 01 §6; targeted for the Month-2
>   strategic work).
