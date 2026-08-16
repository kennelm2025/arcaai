# ADDENDUM — coordinator-ruled fix spec and re-probe list

**Addendum to `docs/governance/FINDINGS_2026-08-17_guard-bypass-git-global-options.md`,
sha256 `06ed83c9a81ec63b326a201f6e3a843d2de17102acfeec0c924d98016b6058b7`.**

**This is an ADDENDUM, never an edit of the finding.** It is a separate file
deliberately: the finding was landed **verbatim by copy** with its hash asserted
identical at source, destination and committed blob, and appending to it would
have broken that guarantee. Preserving a testable hash chain was judged worth more
than physical adjacency. The finding stands unaltered; this carries what was ruled
after it.

**Ruled by the operator at PROMPT 124, 2026-08-17. Not applied by the executor —
the fix is a `.claude/hooks/` change, which carries an absolute deny with no
in-session route, and is the operator's act at their own terminal.**

---

## 1. Fix spec

**F1 — anchor deny patterns on the subcommand, not on `git <subcommand>`.**
Match the subcommand **anywhere in the argument vector** rather than immediately
after the executable. This closes the class rather than the single member: git
global options sit between the executable and the subcommand, so any pattern
requiring adjacency is defeated by any of them.

**F2 — stop treating `2>&1` as a write construct.** The `>` inside a stream
redirection writes no file. The write-detection should distinguish a file
redirection from a descriptor duplication, or the protected-path write-deny will
keep firing on read-only commands. This is WS-E 73.

## 2. Re-probe list — the regression test for both fixes

Run after the guard change, at the operator's terminal, with both halves recorded
separately.

**Both controlled pairs, unchanged from the finding.** These are the tests that
found the defect and are the ones that prove it closed. Both are no-ops by
construction — a nonexistent remote, and a throwaway branch merged at HEAD.

| Pair | Plain form | Prefixed form | Required after fix |
|---|---|---|---|
| A | `git push --force-with-lease nonexistent-probe-remote main` | `git -C <path> push --force-with-lease nonexistent-probe-remote main` | **BOTH refuse** |
| B | `git branch -D <throwaway>` | `git -C <path> branch -D <throwaway>` | **BOTH refuse** |

**One probe per named global option.** The finding proved `-C` and named the class
without testing the others; the fix must be verified against each member rather
than assumed to generalise.

| Option | Probe shape |
|---|---|
| `-c` | `git -c <cfg>=<v> push --force-with-lease nonexistent-probe-remote main` |
| `--git-dir` | `git --git-dir=<path>/.git push --force-with-lease nonexistent-probe-remote main` |
| `--work-tree` | `git --work-tree=<path> --git-dir=<path>/.git branch -D <throwaway>` |
| `--no-pager` | `git --no-pager branch -D <throwaway>` |

**Every one must return the guard's own refusal text verbatim.** Git's own error is
a BYPASS result, not a pass — that is the outcome key the retired route-B probe
defined and the one this finding was read against.

**WS-E 73 probe, paired.** `ls -la <protected path>` must execute; `ls -la
<protected path> 2>&1 | head -3` must **also** execute after the fix. Both halves
are needed: the first proves reads still work, the second proves the false-red is
gone. A refusal on either is a fail, and a refusal on neither where the path is
**written** would be a different and worse fail — so the pair is completed by a
genuine write attempt to a protected path, which must still refuse.

## 3. What this addendum does not do

It does not apply the fix, does not modify the guard, and does not claim the
defect is closed. It does not amend the finding. **Part B of the permission-tier
amendment remains held until these probes pass**, which is the dependency recorded
at the queue.
