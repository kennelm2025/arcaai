# WS-E — Process Incident Ledger

Append-only register of process incidents (tooling traps, workflow
failures, discipline gaps) and the rules they produced. Numbering is
continuous and reserved. Authoritative home of WS-E as of this file's
creation (2026-07-23, PR #20); prior items lived only in session
handover documents.

**Backfill rider:** items 1-23 to be transcribed from the handover
archive in a hygiene session (same bucket as the locked-suite disk
sprawl purge). Items 24-27 are entered as summaries pending the same
backfill. Discovery that no WS-E item had ever been committed to the
repo is itself CL-08 evidence.

## Items

1-23. *Reserved — backfill from handover archive.*

24. PowerShell path resolution trap. (Summary; full text in
    handover 2026-07-22. Backfill.)
25. Local tidy-up sequencing. (Summary; full text in handover
    2026-07-22. Backfill.) See also footnote under 29.
26. Boot ritual gaps. (Summary; full text in handover 2026-07-22.
    Backfill.)
27. Backtick paste handling. (Summary; full text in handover
    2026-07-22. Backfill.)

28. **DEC misfiled into ADR register.** DEC/ADR namespace separation
    held on paper, failed at filesystem level — the ADR folder is
    named `decisions/`, inviting it. Guard paragraph added to
    decisions/README.md. Candidate: rename folder `adrs/` someday.

29. **Here-string writes omit trailing newline → ruff W292 in CI.**
    RULE: run `ruff check --fix` locally before any Python-touching
    commit (joins the git-diff eyeball). Amend-and-force-with-lease
    is the fix pattern pre-merge on own PR branch; never post-merge.

## Footnotes

- To 14/25: git log decoration reflects LOCAL refs; a prune racing a
  just-deleted remote branch leaves ghost decoration. Stale pasted
  scrollback bit twice more this session. `git log` / `Select-String`
  are the truth-tellers, not terminal history or decoration.
- pytest `-v` is overridden by pyproject config (dots print
  regardless); use `-vv` or `--durations=0` when per-test visibility
  matters.