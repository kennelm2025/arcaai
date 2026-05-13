# ADR-NNNN — [Short, declarative title — what was decided]

**Status:** Proposed | Accepted | Superseded by ADR-XXXX | Deprecated
**Date:** YYYY-MM-DD
**Decider:** [Name]
**Supersedes:** [ADR-XXXX, or "none"]
**Related:** [Other ADRs that bear on this decision]

---

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
- Keep ADRs short. One page is typical. Two pages is the maximum.
- ADRs are written for future readers — including bank reviewers who may not have been present when the decision was made. Assume the reader has read `PROJECT_CONTEXT.md` and the foundational ADRs (0001-0003) but no other context.
- An ADR captures a decision, not a plan. Plans live in specifications.
