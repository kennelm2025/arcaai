# PERMISSION-TIER AMENDMENT CANDIDATE — 2026-08-12

**Status: CANDIDATE for operator ruling. Not a change.** Nothing in
`.claude/settings.json` or `.claude/hooks/governance_guard.py` was modified to
produce this document, and nothing should be until it is ruled. It amends the
tiering ruled and sealed at PR #95 and described at
`docs/governance/HARNESS_PERMISSION_TIERS_2026-08-11.md`, which remains
authoritative until this is ruled in.

## Evidence basis, and its limit

**There is no literal prompt log, and this document does not claim one.** The
classification below is reconstructed from the tool calls this session actually
made and from the two mechanisms that decide them — the `permissions.allow` list
in `.claude/settings.json` and the `PROTECTED_PATTERNS` / `DENY_COMMAND_RES` /
`ASK_COMMAND_RES` sets in `.claude/hooks/governance_guard.py`. Where a
classification is inferred from the rule text rather than observed firing, it is
marked INFERRED. A reader should treat the inferred rows as the weaker evidence
they are.

The occasion was the corpus-lister pilot: three subagents ran cleanly and
concurrently within their own tool grants, while the lead needed operator
approval for read-only inspection, scratchpad writes, and pull-request waiting
mechanics. The asymmetry is what prompted this review.

## Classification

### Class A — DENIED, and correctly so. No change proposed.

| Act | Mechanism | Observed |
| --- | --- | --- |
| `Remove-Item -Recurse -Force` | `DENY_COMMAND_RES` | Fired 5+ times as deliberate guard probes; returned the guard's own refusal text every time |

The deny path is the only part of the system exercised repeatedly tonight, and it
behaved identically under every condition including a broken invocation. No
amendment.

### Class B — ASK, and correctly operator-only. No change proposed.

| Act | Mechanism | Observed |
| --- | --- | --- |
| Edit `.claude/settings.json` | `PROTECTED_PATTERNS` | Yes |
| Edit `.claude/hooks/` | `PROTECTED_PATTERNS` | Yes |
| Edit `.claude/skills/` | `PROTECTED_PATTERNS` | Yes |
| Edit `DECISIONS.md` | `PROTECTED_PATTERNS` | Yes |
| Edit `docs/governance/WS-E_INCIDENTS.md` | `PROTECTED_PATTERNS` | Yes |
| `git branch -d` | `ASK_COMMAND_RES` | Yes |
| `gh pr merge` | `ASK_COMMAND_RES` | Yes |
| Any git write while HEAD is main | `GIT_WRITE_RE` + branch check | INFERRED — avoided all session by branching first |

These are the acts the operator must keep. Merge, main, the registers, the corpus
tree, the settings and ceremony system, and elevation stay operator-only under
this candidate, without exception.

### Class C — prompted, and arguably arc mechanics. The amendment's subject.

Every row below was a prompt this session for an act that changes nothing
governed, on a feature branch, with the operator present.

| Act | Why it prompted |
| --- | --- |
| `Get-FileHash` | Absent from the allow list, though `Get-ChildItem`, `Get-Content`, `Get-Acl` and `Test-Path` are present. Pure read |
| `Expand-Archive` | Absent. Wrote only to scratchpad |
| `New-Item`, `Copy-Item` | Absent |
| Scratchpad file writes | The `Write` tool is not allow-listed; only `Read`, `Glob`, `Grep` are |
| `Start-Sleep` | Absent. Used solely to wait for CI |
| `gh pr create`, `gh pr edit`, `gh pr view`, `gh pr checks` | Absent. None of them merges anything |
| `gh label list` | Absent. Pure read |
| `git add`, `git commit`, `git push` on a feature branch | `GIT_WRITE_RE` asks; the branch check distinguishes main, but the ask fires regardless |

**Proposed:** auto-allow these as arc mechanics **while HEAD is not main**, with
the branch condition enforced in the guard rather than in a rule string, since
rule strings cannot read repository state. `gh pr merge` is explicitly excluded
and stays Class B.

## The finding that matters most, and it is not a widening

**The Tier 1 allow rules are written for relative invocation, and this session's
own new convention broke them.**

The allow list carries entries of the form
`PowerShell(python scripts/repo_manifest.py:*)`. The no-bare-`cd` convention
ruled tonight (WS-E 68) requires commands to address files by absolute path.
An absolute invocation does not match a relative rule string, so the Tier 1
grants for the mandatory batteries stopped matching the way those batteries are
now required to be invoked.

This is corroborated in the file itself: lines 49-50 already carry absolute-path
duplicates for `lint.cmd` and `test.cmd` alone. Someone met this problem before,
patched the two cases in front of them, and did not generalise it — so the
evidence for the pattern was already in the tree.

Consequence for the register: this is direct evidence on **queue item 4(c)**,
which records the rule strings as unverified. They are now verified, and they are
wrong. Any amendment must state each rule in a form that matches absolute
invocation, or the widening will silently fail to apply.

## A counter-finding — this review also proposes a NARROWING

`.claude/agents/` is **not** in `PROTECTED_PATTERNS`. The guard gates
`settings.json`, `hooks/` and `skills/`, and stops there.

Tonight's four repairs to `.claude/agents/corpus-lister.md` were therefore
ungated, while the three edits to `.claude/skills/` in the same arc each
prompted. An agent definition states what a subagent may do and which tools it
holds; it is at least as load-bearing as a skill, which only teaches. The
asymmetry is an accident of the pattern list rather than a decision.

**Proposed:** add `.claude/agents/` to `PROTECTED_PATTERNS`, Class B. A review
commissioned to reduce friction should not return only widenings, and this one
does not.

## What must be true before this is ruled in

1. **Rule strings must be tested, not written.** The lesson of WS-E 68's
   corrective, and of the two absolute-path duplicates already in the file, is
   that a permission or hook rule is verified by a deny-shaped probe returning
   the guard's own text plus an allow-shaped call that succeeds — never by
   reading the rule and finding it plausible.
2. **Never grant in Tier 1 anything Tier 2 is relied on to gate.** Tested
   2026-08-11: a Tier 1 allow rule pre-empts a Tier 2 guard ask. Every Class C
   row must be checked against `PROTECTED_PATTERNS` before it is allow-listed,
   and no command family carrying a deny may be allow-listed at all, since
   whether a deny is pre-empted the same way remains untested and has no safe
   probe.
3. **The branch condition belongs in the guard.** "While HEAD is not main"
   cannot be expressed as a rule string, which matches command text and cannot
   read repository state.
