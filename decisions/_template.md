# ADR-NNNN — [Short, declarative title — what was decided]

**Status:** Proposed | Accepted | Accepted (backfilled) | Superseded by ADR-XXXX | Deprecated
**Decision Date:** YYYY-MM-DD  *(when the decision was actually made)*
**Recorded Date:** YYYY-MM-DD  *(when this ADR was written; equals Decision Date for a contemporary ADR)*
**Decision Type:** Contemporary | Backfilled
**Decider:** [Name]
**Evidence:** [Backfilled ADRs: cite where the decision already lives — a commit SHA, a DEC-NNNN entry, a code comment, or a design document — so a reviewer can verify it was in operation. Contemporary ADRs: "n/a".]
**Supersedes:** [ADR-XXXX, or "none"]
**Related:** [Other ADRs that bear on this decision]

---

> **Backfilled ADRs only — include this line verbatim, then delete this quote block:**
> This ADR records a decision already in operation and does not imply it was made on the Recorded Date.

## Context

What is the situation that requires a decision? What forces are at play? What is the question being answered?

Keep this focused. Two or three paragraphs. The reader should be able to understand why a decision is needed without reading any other document.

## Decision

State the decision in plain, declarative language. "We will do X" — not "we should consider X."

If the decision has non-obvious nuances or specific language requirements (e.g. "must always be phrased as Y, never as Z"), state them here.

## Consequences

### Positive

What this decision enables, unlocks, or improves. Be specific — "easier to maintain" is weak; "reduces the number of integration points from 4 to 1" is strong.

### Negative / costs

What this decision costs, blocks, or constrains. Honest framing — every decision has trade-offs. If you can't name a downside, you haven't thought hard enough about the decision.

### Specifications affected

Which of the eight canonical specifications are touched by this decision, and how.

## Alternatives considered and rejected

For each plausible alternative, state what it was and why it was rejected. Two to four alternatives is the right range — fewer means the decision space wasn't explored; more means alternatives are being padded.

---

## Notes for authors

- ADRs are **immutable once accepted**. If a decision changes, write a new ADR that supersedes this one. Never edit an accepted ADR.
- An ADR is not immutable until it is **committed** — an uncommitted file is not yet part of the audit trail.
- Most ADRs are **Contemporary** (decided now, recorded now — set both dates the same, Evidence "n/a"). Use **Backfilled** only when recording a decision already in operation; then set the two dates honestly, fill Evidence, use `Status: Accepted (backfilled)`, and keep the disclosure line.
- `ADR-NNNN` (four-digit) is this folder only. Build- and design-log decisions live in `DECISIONS.md` as `DEC-NNNN` — do not use `ADR-` for those.
- Keep ADRs short. One page is typical. Two pages is the maximum.
- ADRs are written for future readers — including bank reviewers who may not have been present when the decision was made. Assume the reader has read `PROJECT_CONTEXT.md` and the foundational ADRs (0001-0003) but no other context.
- An ADR captures a decision, not a plan. Plans live in specifications.
