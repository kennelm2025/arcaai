# Phase 2 group (i) — FAILED on route A: skill renders are ungoverned

**Status: RECORD OF A FAILED GATE. No register number consumed.** A WS-E number
is claimed only at the operator's word; until then this cites "next 69" and
nothing else. The finding itself is not provisional — the probe ran and returned.

**Date:** 2026-08-14. **Repository state at probe time:** HEAD
`b9423dff193c578caca2c31330f38d42dc42f740`, the merge commit of PR #120; probe
run from a throwaway branch off that commit; working tree clean apart from the
probe skill, which was untracked throughout and has since been removed.

**Verdict in one line: skill render lines execute shell commands that the
governance guard never sees, including commands carrying an absolute deny.**

---

## 1. The probe, and both halves of its result

The probe was a skill whose single render line attempted the established
discriminator command, safe by construction because the remote does not exist
(verified immediately beforehand by reading `.git/config`, which lists `origin`
alone). The instrument, now deleted, and its render line:

```
.claude/skills/probe-route-a/SKILL.md   (removed 2026-08-14)
sha256 4095bca1069f9338d37367474404b6fe5b29144a831c3bf167359f1468702758
render line: !`git push --force-with-lease nonexistent-probe-remote main`
```

**Executor's half — the render output, verbatim, in-harness:**

```
Shell command failed for pattern "!`git push --force-with-lease nonexistent-probe-remote main`": [stderr]
fatal: 'nonexistent-probe-remote' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

**Operator's half — observed at the terminal, stated by the operator:**

> no prompt, no deny, nothing at his terminal.

The two are attributed separately and deliberately. The executor cannot see a
prompt; the operator cannot see the tool result. Neither half alone decides this,
and that division is the same one that made the morning's discriminator work.

**Classification: outcome 2 of the probe's own three-outcome key — BYPASS.** The
command executed, and no gate interaction occurred at either end.

## 2. The elimination step

The pair could in principle be explained by an allow rule silently pre-empting
the guard on a path the guard did see. **It cannot be, and that is settled
evidence rather than reasoning.** This morning's discriminator proved at the
operator's terminal that the guard's deny survives a matching Tier 1 allow: no
prompt fired and the refusal returned. See
`docs/governance/PRECEDENCE_DISCRIMINATOR_OUTCOME_2026-08-14.md`.

So an allow cannot explain a *silent execution* on a guard-seen path. The only
reading consistent with execution plus terminal silence is that the guard was
never invoked on this path at all.

## 3. The confound, honestly bounded

One ambiguity survives, and the operator's half does not resolve it because both
readings produce exactly the same pair — execution, no prompt, no deny:

1. **Hook never invoked.** Skill renders do not route through PreToolUse. The
   defect is harness-level and no hook or settings change can reach it.
2. **Frontmatter pre-emption.** The probe skill declared a Tier-1-shaped grant
   for the command family in its own `allowed-tools` — deliberately, so that
   frontmatter could not be the thing *blocking* and any refusal would be
   attributable to the guard. If that grant instead pre-empted the deny inside a
   ceremony, the defect is that **any skill can self-grant past the deny layer**
   by writing its own frontmatter.

**Both are governance failures, and the second is the worse of the two.** It
would mean the deny layer is bypassable by an artefact any skill author controls,
and that deny-precedence is context-dependent — proven for the main-loop path,
false inside a ceremony.

**The disambiguating probe is OWED and was not run:** the identical render with
the frontmatter grant removed. If it still executes, reading 1 holds independent
of the grant. If it is refused, reading 2 holds and the finding changes shape
entirely. Not run because the operator ruled stop-everything on a bypass, which
is the correct order — the exposure is closed first and the diagnosis follows.

## 4. Exposure — this is not hypothetical

**Skill renders are an ungoverned execution path, and the ceremonies use them.**
`.claude/skills/session-open/SKILL.md` carries five render lines that fire at
every boot, before a word of the task text is read. Their commands are benign —
git status, git log, git diff, the manifest script, a gh read — but the path they
run on has no gate.

**Every session this repository has ever opened has opened through this hole.**

The authoritative tiers document recorded the question as UNVERIFIED and added
that it was moot in practice because background subagents are disabled
repository-wide. That mootness argument covered **subagents only**. Skill renders
were never moot, and the sentence's reassurance did not apply to them.

## 5. Second finding: the registry wall

The first attempt at this probe did not fire. The skill was authored mid-session
and the invocation returned `Unknown skill: probe-route-a`, because the skill
registry is populated at process start.

This is the same structural wall the discriminator hit with `.claude/settings.json`:
**load-at-start surfaces cannot be introduced into the running process that needs
them, so they are testable only across a restart boundary.** Settings then, skills
now. Any future probe of a load-at-start surface must budget a restart, and a probe
that "returns nothing" in its authoring process has not failed — it has not run,
which is a third outcome and not a red.

## 6. Third finding: deletion is not a write, per the ask layer

Found while disposing of the probe instrument. The protected-path **ask** fires
when a command matches a protected path *and* a write-shaped construct. The
write-shaped set names redirection, tee, in-place sed, move and copy verbs, and
the PowerShell content-setting cmdlets. **It does not name any deletion verb.**

So removing a file under a protected path does not raise the ask, while writing
one does. Only the recursive-force spellings are caught, and those are caught by
the deny layer rather than by this one. This is a third instance in the
already-carried write-detection family and is recorded with the other two rather
than raised separately.

## 7. Register position — WS-E candidate at next 69

This belongs in the incident register as a **candidate at next 69**, cited as
"next 69" and not as a bare number until consumed at the operator's word.

**Family: WS-E 64.** That incident recorded a guard wired to one shell of two,
correct and unreachable for three days. This is the same shape one layer out —
**coverage believed present, absent in fact** — and it is worse in one respect:
WS-E 64's gap was in a mechanism nobody had exercised, while this gap sits on the
path every session takes to open.

## 8. The rollback this record lands with

Ruled NARROW on evidence, against a full revert of the merge.

**Done:** the 55 widened allow entries are removed; allow entries return from 122
to 67, the pre-widening count. The standing note carries an amendment recording
the rollback and its reason, and amendment 3 is marked superseded rather than
rewritten.

**Retained deliberately, because this failure does not implicate them:** the three
deny regexes in `.claude/hooks/governance_guard.py`; their 37 assertions at
`tests/governance/test_guard_deny_patterns.py`, the first test coverage that
module has ever had; and the deny-precedence amendments, which rest on a proof
this failure leaves untouched. A full revert would have re-inserted the
now-superseded claim that deny-precedence is untested — re-landing a documented
falsehood to remove an unrelated grant.

**What the rollback does NOT do, stated so the green is not overread.** Allow
rules only ever permit; they never block. Removing them does not constrain a
render that bypasses the guard entirely. **This closes the exposure it can reach —
fail-closed on the main-loop path — and records the one it cannot.**

## 9. Owed, and not discharged here

1. **Frontmatter disambiguation probe** — same render, grant removed. Section 3.
2. **Route B, subagent dispatch — still unprobed.** It matters more than it did
   before: the agents narrowing landed on the premise that the subagent path is
   governed. If route B also bypasses, that narrowing gates a path nothing
   enforces, and the gate is decorative.
3. **Groups (ii), (iii) and (iv): NOT STARTED**, blocked on this gate by ruling
   R2, which declined to carve an exception for exactly this blind spot. The
   widened families were never exercised, for any purpose, at any point.
