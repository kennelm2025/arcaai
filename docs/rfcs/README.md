# Request for Comments (RFC)

RFCs are how non-trivial proposals are shared, discussed, and resolved **before** implementation begins.

## Why RFCs?

Without an RFC process, every substantive change starts as a PR with code or content already written. By the time it's reviewed, the author has invested effort and is committed; reviewers feel pressure to accept rather than ask for fundamental rethinks.

The RFC process inverts this. Substantive changes are proposed as a written argument first. Implementation happens only after the argument is accepted.

## When to write an RFC

Write an RFC when:

- The change affects more than one specification
- The change implies a new architectural decision (an ADR will follow)
- The change introduces new structure, tooling, or process
- The change reverses or significantly modifies an existing approach

Do not write an RFC for:

- Minor edits within a single specification
- Typos, formatting, or link fixes
- Implementation of a previously-accepted RFC
- Changes that are obvious applications of an existing ADR

## RFC lifecycle

1. **Draft** — Author creates `NNNN-name.md` from `_template.md` and opens a PR
2. **Under review** — Reviewers (SME panel and Mike) discuss inline
3. **Accepted** — RFC merges to `main`; implementation work begins as separate PRs that reference the RFC
4. **Rejected** — RFC merges to `main` with status `Rejected` and a note on why; this is part of the audit trail
5. **Withdrawn** — Author withdraws before resolution; RFC merges with status `Withdrawn`

Accepted and rejected RFCs both stay in the repository. They are part of the project's decision history.

## Numbering

Sequential, padded to four digits: `0001`, `0002`, `0003`, etc. Numbers are never reused.

## Index

No RFCs yet.
