# ADDENDUM 2 — re-probe row amendment: two rows do not discriminate

**Addendum to `docs/governance/FINDINGS_2026-08-17_guard-bypass-ADDENDUM_fix-spec.md`,
sha256 `f83622a58adbfcb92f4f71dc9ac7f83811afff5c81927828182d4b8b03fbdab0`,
which is itself an addendum to
`docs/governance/FINDINGS_2026-08-17_guard-bypass-git-global-options.md`,
sha256 `06ed83c9a81ec63b326a201f6e3a843d2de17102acfeec0c924d98016b6058b7`.
Both hashes read live from the tree on 2026-08-18; the finding's hash matches
the value its own addendum asserts, so the chain holds at three links.**

**A SEPARATE FILE, never an edit of either.** The same reasoning that placed
Addendum 1 beside the finding rather than inside it applies again and applies
more strongly: Addendum 1 now has a hash of its own that this document pins, and
appending to it would invalidate that pin in the act of citing it. Adjacent
placement was ratified for Addendum 1; this follows the ratified shape.

**Authored 2026-08-18 under PROMPT 129. Amends the re-probe list only. It does
not amend the fix spec (F1 and F2 stand as ruled), does not apply anything, and
does not claim any defect closed.**

---

## 1. The finding

Two rows of Addendum 1 section 2 **cannot distinguish a fixed guard from an
unfixed one**. Run as written they return the correct refusal text against the
*broken* guard, so a green on those rows evidences nothing about F1.

Both rows place `--git-dir=<path>/.git` immediately before the subcommand:

| Row as written | Why it fails to discriminate |
|---|---|
| `git --git-dir=<path>/.git push --force-with-lease …` | the literal text `.git push` contains `git` followed by whitespace followed by `push` |
| `git --work-tree=<path> --git-dir=<path>/.git branch -D <throwaway>` | the literal text `.git branch` contains `git` followed by whitespace followed by `branch` |

The pre-fix patterns were `git\s+push` and `\bgit\s+branch\b`. Each matches the
`git` inside the `.git` **path component**, not the `git` executable. The row
therefore refuses on the unfixed guard for a reason that has nothing to do with
the global option it was written to test.

## 2. The evidence

Both shapes were evaluated against the installed (pre-fix) module and the
candidate (post-fix) module, offline, by importing each and searching its
`DENY_COMMAND_RES` patterns:

| Row | pre-fix | post-fix | discriminates |
|---|---|---|---|
| `--git-dir` as written | REFUSE | REFUSE | **NO** |
| `--work-tree` as written | REFUSE | REFUSE | **NO** |
| `--git-dir` amended | BYPASS | REFUSE | yes |
| `--work-tree` amended | BYPASS | REFUSE | yes |
| `-C` (push) | BYPASS | REFUSE | yes |
| `-c` (push) | BYPASS | REFUSE | yes |
| `--no-pager` (branch) | BYPASS | REFUSE | yes |

Five of the seven rows in Addendum 1 section 2 are sound as written. Only the
two carrying a `.git` path component immediately before the subcommand are
affected.

## 3. The amendment

Insert a second global option **between the `--git-dir` value and the
subcommand**, so no `.git` text is adjacent to it. The row then tests what it
was written to test.

| Option | Amended probe shape |
|---|---|
| `--git-dir` | `git --git-dir=<path>/.git --no-pager push --force-with-lease nonexistent-probe-remote main` |
| `--work-tree` | `git --git-dir=<path>/.git --work-tree=<path> branch -D <throwaway>` |

The `--work-tree` amendment is an ordering change only: the two options swap, so
`--work-tree=<path>` rather than `--git-dir=<path>/.git` is the token adjacent to
`branch`. No new option is introduced and the command's effect is unchanged.

Everything else in Addendum 1 section 2 stands unamended: both controlled pairs,
the `-c`, `-C` and `--no-pager` rows, the WS-E 73 read pair, the write probe, and
the pass condition that **every row must return the guard's own refusal text
verbatim, git's own error being a BYPASS result and not a pass.**

## 4. Why this is recorded rather than quietly fixed

A probe whose green is indistinguishable from the defect being present is the
check-method family — the most-instanced open item in the queue. This instance
is worth the file because of *where* it was found: inside the re-probe list
written to close two guard defects, in a document whose whole purpose is to
define a pass condition. The family's characteristic failure reached the
instrument built to detect it.

The counter-example is worth recording with it. The defect was found only by
running each row against **both** modules and requiring the pre-fix result to
differ from the post-fix result. Running the rows against the fixed guard alone
would have returned seven refusals and read as a clean sweep.

## 5. Status

**NOT A GREEN, AND NOTHING HERE IS EVIDENCE OF EFFICACY.** The evaluation above
is offline pattern matching against imported modules. It cannot evidence that
the PreToolUse matcher routes the call, that the hook executes, or that the
harness honours the response. Those are what the live re-probe establishes and
they remain owed.

No control mapping line is carried. Queue item 34 M11(d) requires per-class
mapping content to be defined once in the control framework, and that framework
does not exist yet; composing a mapping here is what M11(d) forbids. Same
position as `docs/governance/SESSION_COSTS.md`.
