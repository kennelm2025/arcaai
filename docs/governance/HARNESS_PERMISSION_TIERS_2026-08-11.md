# Harness permission tiers — ArcaAI

**Operator ruling: 2026-08-11.** Autonomy granted by written policy on
the record. This document is authoritative for the tiers; `CLAUDE.md`
describes them and points here. Where the two disagree, this document
governs and the discrepancy is a WS-E item.

Landed alongside WS-E 64, which records that the enforcement layer had
been wired to one shell of two since installation. The sequencing was
ruled absolute: no allow-list widens anything while the deny layer has
a blind spot, so the guard was extended to the PowerShell tool and
verified end to end in the same PR that grants Tier 1.

## Tier 1 — auto-allow, no prompt

Read-only operations (git status, diff, log, show, branch listing,
blame, rev-parse, fetch; file reads; directory listings; `Get-Acl`;
`Test-NetConnection`). The mandatory batteries (`scripts/check_docs.py`,
lint, tests, pytest, `scripts/repo_manifest.py`,
`scripts/rehash_sweep.py`). Non-gated git navigation (checkout, switch,
fetch, fast-forward-only pull).

*Rationale:* every one of these is reversible, branch-isolated, and
verified by batteries that run regardless of whether a prompt preceded
them. The prompt was never the control; the evidence after the act is.

**NARROWED 2026-08-11, same day, on evidence.** Tier 1 as first merged
also granted bare `Edit` and `Write` and the git write verbs (add,
commit, push, branch). All of those are withdrawn. The precedence
question recorded below as UNVERIFIED was tested and **failed**: a
settings allow rule pre-empts the guard's ask, so every allow rule
silently disabled the Tier 2 gate covering the same ground. Bare
`Edit` and `Write` neutralised every protected-path gate; the git
write verbs neutralised the branch-deletion and HEAD-on-main gates.
Restoring those grants safely requires enumerating paths that provably
contain no protected path — `docs/` and `verticals/` each contain
several, so neither subtree can be granted wholesale — and that
enumeration is deliberately not attempted here. Until it exists, Tier 1
is read-only operations, the batteries, and git navigation. Edits and
git writes prompt as they did before the tiering.

**READ-CLASS WIDENING: LANDED AND ROLLED BACK, 2026-08-14. DEFERRED
AGAIN, and this time with a named reason rather than an open question.**
The families deferred when precedence was unproven — git-family reads
beyond those present, filesystem reads, text search, text slicing — were
restored once deny-precedence was proven at the operator's terminal, then
removed the same day when the gating probe failed. Their activation had
been made conditional on that probe, and the probe found that skill
renders run ungoverned; see the soft-enforced section below and
`docs/governance/GROUP1_FAILURE_route-a-bypass_2026-08-14.md`.
Allow entries returned from 122 to 67, the pre-widening count.
**The list was not found wrong. The gate failed.** Nothing in the
enumeration is withdrawn on its merits, and it stands ready for the day
the render route is fixed or proven governed — which is the condition of
its return, and the only one.
**Why removed rather than annotated as inactive:** "inactive" was a note
in a commit body and a JSON comment, and no mechanism enforced it. A
grant that is live in every fresh process is granted, whatever the
surrounding prose says.

## Tier 2 — gated, every touch

The six governed stores, unchanged: `verticals/fraud/corpus/MANIFEST.yaml`,
the corpus edges file, `docs/governance/WS-E_INCIDENTS.md`,
`DECISIONS.md`, the rulings records, and the document register. Added
2026-08-11: `pyproject.toml`; `.github/workflows/`; and `decisions/`. Plus, by
repository state rather than by path: PR merge, branch deletion, and any
git write while HEAD is main.

**REMOVED FROM THIS TIER ON 2026-08-14 — the four `.claude/` paths are
now DENIED, not asked.** `.claude/settings.json`, `.claude/hooks/` and
`.claude/skills/` were added here on 2026-08-11, and `.claude/agents/`
on 2026-08-13 at `678f46a`. All four left Tier 2 on 2026-08-14 under
WS-E 69 fix item 1; the amendment is below. The narrowing paragraph that
follows is retained rather than deleted, because it is the record of why
`.claude/agents/` was gated at all, and that reasoning is what the deny
now carries forward.

**The `.claude/agents/` addition is a NARROWING**, and is recorded here
because a review commissioned to reduce friction returned it. Agent
definitions were ungated while skills prompted, so a subagent's tool
grants and instructions could be rewritten with no gate at all. An agent
definition states what a subagent **may do** and is at least as
load-bearing as a skill, which only teaches. The gap was latitude nobody
ruled rather than a decision anybody took.

*Rationale, per group.* `pyproject.toml` and the workflows change what
every future run means, so a silent edit rewrites the meaning of every
later green. The permission and ceremony system is gated against
itself because the harness must never widen its own latitude
unprompted — `.claude/settings.json` guards the file these tiers
live in, which is the point rather than an accident. **That reasoning is
retained; its RESPONSE is superseded by the 2026-08-14 amendment below,
where the gate becomes a deny rather than an ask.** `decisions/` is
gated on a mechanism, not a convention: `scripts/repo_manifest.py`
reads the leading four digits off each filename there, so that
filesystem **is** the ADR register and any write to it consumes
register numbers silently. It is register-consuming by mechanism and
therefore gated by consequence. WS-E 64 records that the one near miss
of this kind was caught by the working protocol and not by any gate;
this is the gate that was missing.

### AMENDMENT 2026-08-14 — the never-silent set: ask becomes deny

**Ruled by the operator on 2026-08-14, discharging WS-E 69 fix item 1.**
`.claude/settings.json`, `.claude/hooks/`, `.claude/skills/` and
`.claude/agents/` no longer draw a Tier 2 ask. They draw a **deny**, on
both the file-writing-tool branch and the shell branch of
`.claude/hooks/governance_guard.py`.

**Why the ask was not a gate.** The reasoning above — gate the system
against itself, make each touch deliberate rather than impossible — held
only while an ask was guaranteed to reach a person. It was not. A
bypassing permission mode auto-approves asks without ever surfacing
them, which WS-E 69 records for a session's full duration, so the
absence of a prompt evidenced nothing. An ask that a MODE can satisfy is
a gate whose green is indistinguishable from its never having been put.
The deny/ask asymmetry recorded at WS-E 69 is the whole argument: denies
survive bypass, asks vanish into silent approval.

**Why deny, and why there is no middle.** There is no stronger ask. Deny
is the only response this guard returns that no mode and no approval
overrides.

**What it costs, stated rather than discovered.** There is no in-session
write to these four paths again, with or without live operator approval,
**including the write that would repair the guard or roll back this very
deny**. That is the same route every other denied verb already takes.
Harness changes are drafted outside the tree — the scratchpad is
unmatched by these patterns — installed by the operator at the
operator's own terminal, then branch, PR, merge. Drafting is unaffected;
only installing is denied, and installing is the act that changes what
every future run means. The cost was demonstrated within the hour: the
message-wording refinement ruled in the same package could not be
applied by the executor and was installed by the operator — this
posture's first live exercise.

**Installer-design note from that first exercise.** The install script's
final assertion — that the superseded wording no longer appears in the
file — reported a STOP while the change was in fact correct. The sole
surviving occurrence was the patch's own new comment, quoting the old
wording as history. A phrase search cannot separate **use** from
**mention**, so the check failed the file for explaining itself. False
red, in the safe direction, resolved by reading the surviving line. The
design correction for the next installer is one line: **assert absence
in the message strings, not across the whole file** — comments quoting
superseded text are evidence the change was understood, not evidence it
was missed.

**What is NOT changed: reads.** Every ceremony in this repository reads
`.claude/` and none of them prompts. The deny covers the file-writing
tools by path alone, and shell commands only through the same verb list
the ask used — so the shell branch remains exactly as porous as that
list, and widening it is a separate act with its own ruling.

**The other eight protected paths keep their ask**, deliberately. They
are stores the executor must be able to append to as ordinary governed
acts; denying them would stop the register discipline rather than
protect it.

**Fail-degraded by construction.** The four patterns remain spliced into
the guard's protected-path list as well as into their own, so that if
the never-silent check were ever reordered behind the ask or lost, these
paths degrade to the ask they drew before this amendment rather than to
a silent allow. That duplication is asserted by a test and must not be
tidied away as redundancy.

**Evidence.** Landed at `c406932`, verified by a paired probe: a
deny-shaped call returned the guard's own refusal text verbatim through
the PowerShell tool, and an allow-shaped read of the same path
succeeded, which is what shows the guard discriminates rather than
merely blocks. Unit coverage is
`tests/governance/test_guard_protected_paths.py`, which drives the hook
end to end rather than asserting its patterns, because the failure mode
of this change is ordering rather than matching. **Not closed by this
amendment:** the session that ran those probes could not confirm its own
permission mode from inside itself, so the default-mode deny-precedence
probe owed at WS-E 69 stands untouched.

**"PR merge" above understates what is now built, and is corrected
here.** As of `25d71b3` the merge gate is Option B: the guard reads live
GitHub state and spends it on **refusing early** rather than on
proceeding automatically. No approval, an approval not pinned to the
current head SHA, any check failing or still pending, or state that
cannot be read at all — each is a **deny**, the last one fail-closed,
because an UNKNOWN rendered as a green is the shape every false green in
this repository has taken. Only an approval on the current head with all
checks green reaches **ask**. The guard never returns allow, by design:
a guard that could allow would be a granting mechanism, and every future
defect in it would confer merge rights rather than merely fail to block.
So merging remains an operator act under Tier 3; what changed is that the
confirmation can now only be reached by a pull request that genuinely
carries approval and green checks. This is strictly stronger than the
unconditional ask it replaced, which asked identically on every PR
regardless of its state.

### First live exercise of the Option B gate — 2026-08-14, refusal direction

Exercised deliberately on PR #123, the pull request that hardens the
guard itself. With no review on the PR, `gh pr merge 123` returned the
gate's own refusal verbatim: **"MERGE DENIED (no approval): the PR
carries no APPROVED review. The operator's approval IS the ruling
record; without it there is nothing for a merge to execute."** The gate
reads live GitHub state, finds no approval, and refuses. That path is
now evidenced rather than reasoned about.

**The satisfied path is structurally unreachable on this topology, and
that is the more important finding.** Reaching **ask** requires an
APPROVED review pinned to the current head SHA. GitHub does not permit
the author of a pull request to approve it, and this repository has one
operator who authors every commit and opens every pull request. There is
therefore no state this repository can currently produce in which the
gate returns ask. The delegation clause is sound; the topology cannot
supply its precondition.

**Consequences, recorded so the gate is not later read as broken.**
(1) **Browser merge is the designed route for this repository**, not a
fallback — the operator merges at GitHub, where the author-approval bar
does not apply because no approval is being claimed. (2) **The gate
retains its whole value in the refusing direction**: it is the
executor-self-merge guard, and it refuses every merge the executor could
attempt through the harness, on every PR, unconditionally, for as long
as this topology holds. It was never the operator's gate; it is the
executor's. (3) The satisfied path becomes reachable the moment a second
reviewer exists, and needs no change to the guard when that happens.

**Evidence for the single-operator segregation-of-duties limit** named
at `CLAUDE.md` current-queue item 34, finding (a). That limit has until
now been stated as a policy caveat. This is the first instance of it
appearing as a **mechanical** fact: a control that is correctly built,
correctly wired, and unreachable in one direction because one person
cannot be two parties. The SDLC control framework must state it in that
form — an auditor who reads the gate's specification and then finds it
has never returned ask is owed the reason in the document rather than in
a reconstruction.

**Absolute denies, unchanged and with no exception path:** force push
in any form, git history rewrites, recursive force deletes, force branch
deletion, the write forms of the read-class grants, **writes to the four
never-silent `.claude/` paths (2026-08-14, amendment above)**, and the
standing rule that the harness never elevates — extended 2026-08-11 to
database roles: the harness runs as the application role and never
assumes owner.

## Tier 3 — operator rulings

Arc selection, scope, merges, frame rulings, register decisions. These
are not tool gates and are unaffected by anything in this document. No
mechanism grants or withholds them.

## Safeguard 1 — batteries remain mandatory

Auto-allow moves the gate from *before* the act to the evidence
*after* it. It removes prompts, not verification. Unchanged: `git diff
--stat` comes first in every battery and an empty diff means the act
did not happen; success is asserted on the substance a check returns
and on the assertions it names, never on an exit code alone; one act
at a time, with state checked before mutation and effect verified
after it.

## Safeguard 2 — rollback is one revert

Every change implementing these tiers rides a single PR. Reverting
that PR restores the prior enforcement state in one act, with no
partial condition to reason about.

## Enforcement coverage

"Gated" must not be able to quietly mean "gated on one tool". Three
mechanisms exist, and they do not cover the same ground.

1. **The PreToolUse guard** (`.claude/hooks/governance_guard.py`,
   routed by the matcher in `.claude/settings.json`). Covers the Bash
   and PowerShell tools for command inspection, and the file-writing
   tools for path inspection. Coverage is two-part: the matcher must
   route the call *and* the module's shell-tool set must name the
   tool. Either alone is a silent no-op — the WS-E 64 defect exactly.
   Adding a shell tool means adding it in both places.
2. **Permission rules** in `.claude/settings.json`. These match
   command text only. They cannot read repository state, which is why
   the branch condition is not expressible here and lives in the guard
   instead.
3. **Skill frontmatter `allowed-tools`**, per ceremony under
   `.claude/skills/`. **Tier 1 grants are not in force inside a
   ceremony**; that ceremony's own frontmatter governs, and all five
   are currently Bash-only. This narrows rather than widens, which is
   the safe direction — a ceremony that prompts more than the tiers
   promise is friction, not exposure — but it means the boot battery
   may prompt where Tier 1 says it will not. Harmonising the
   frontmatter is a follow-up, deliberately not folded into this arc.

**The guard may only ever restrict** — it returns deny or ask and never
allow, so it cannot widen a granted permission. **But it cannot narrow
one either, and that is not what this document first claimed.** Tested
2026-08-11: an allow rule in `.claude/settings.json` pre-empts the
guard's ask for the same command, so the two mechanisms do not compose
as allow-narrowed-by-guard. They are alternatives, and the allow rule
wins. The practical rule that follows is blunt and load-bearing:
**never grant in Tier 1 anything Tier 2 is relied on to gate.** An
allow rule and a guard ask covering the same ground is not
belt-and-braces; it is the gate silently switched off. Whether the
guard's *deny* is likewise pre-empted has NOT been tested, because
every deny in this repository is destructive and no harmless probe
exists on that path — treat deny coverage as unverified rather than
assumed, and never rely on a deny to catch an allow-listed command.

## Soft-enforced — named, not implied covered

Real content, because a policy that implies coverage it lacks is the
false-green shape this repository catalogues.

- **The never-elevate rule.** Not mechanically enforced at all.
  Partially detectable through the obvious invocations, but elevation
  can arrive by means no pattern sees. Guidance only.
- **The never-assume-owner-role rule** (2026-08-11). Same status:
  partially detectable through the owner DSN and role name, never
  completely. Guidance only.
- **"Branch deletion other than the just-merged branch."** The guard
  gates all branch deletion because it cannot know which branch was
  just merged. The qualifier is soft; the gate is deliberately
  broader than the rule.
- **"Any register-consuming act."** Consumption is semantic, not
  textual. Three registers are gated by path and `decisions/` is now
  gated by mechanism, but no mechanism can recognise a number being
  claimed in prose.
- **Skill renders: TESTED 2026-08-14, and they are UNGOVERNED.** A skill
  whose render line attempted the force-push discriminator, aimed at a
  nonexistent remote, **executed it** — returning git's own error rather
  than the guard's refusal, with no prompt and no deny at the operator's
  terminal. The guard was never invoked on that path. Full record at
  `docs/governance/GROUP1_FAILURE_route-a-bypass_2026-08-14.md`.
  **This is not hypothetical and it is not new.** The boot ceremony
  carries five render lines that fire before a word of its task text is
  read, so every session this repository has ever opened has opened
  through this path. The commands themselves are benign; the path is
  ungoverned.
  **One ambiguity is unresolved and is owed a probe:** whether renders
  bypass the hook entirely, or whether the probe skill's own
  `allowed-tools` grant pre-empted the deny inside a ceremony. Both fit
  the evidence and both are governance failures — the second would mean
  any skill can self-grant past the deny layer.
  **This bullet previously said the question was moot because background
  subagents are disabled. That mootness covered subagents only.** Skill
  renders were never moot, and the reassurance did not apply to them.
- **Whether subagent tool calls route through PreToolUse is still
  UNVERIFIED.** Not observed, and not claimed in either direction. It
  now matters more than it did: `.claude/agents/` was added to Tier 2 on
  the premise that the subagent path is governed. If it is not, that gate
  is decorative.
- **The permission rule strings themselves are unverified.** Rules
  governing a session cannot be tested from inside that session, and
  declaring them working on merge would be exactly the false green
  this repository keeps cataloguing. The PowerShell rule forms in
  particular are asserted by construction, not by observation.
- **Precedence between a Tier 1 allow rule and a Tier 2 guard ask:
  TESTED 2026-08-11, and it FAILED.** The allow rule wins; the guard's
  ask does not reach the operator. Tier 1 was narrowed the same day.
  See the narrowing note under Tier 1 and the amended coverage rule
  above.
- **Whether an allow rule also pre-empts a guard DENY: TESTED
  2026-08-14 UNDER `bypassPermissions`, and the deny FIRED. Default-mode
  precedence is UNPROVEN.** A matching Tier 1 allow rule for the
  force-push family was applied, the session restarted so the settings
  provably loaded, and the probe issued: **no prompt fired and the
  command was denied**, returning the guard's own refusal text. Branch A
  of the discriminator — deny wins. Full record, including the two
  verbatim strings and the preconditions with their evidence, at
  `docs/governance/PRECEDENCE_DISCRIMINATOR_OUTCOME_2026-08-14.md`.
  **Scope, stated so the result is not overread.** It is one observation
  on one command family, the CL-E1 force-push guard. It settles
  precedence for a **deny** only and leaves the 2026-08-11
  allow-pre-empts-**ask** finding entirely untouched — the two mechanisms
  remain alternatives at the ask level, and the rule directly above still
  governs there.
  **This bullet previously claimed the question could not be tested
  safely. That claim was wrong, and the way it was wrong is the lesson.**
  Every deny here is destructive, so the reasoning went, therefore no
  harmless probe exists. But a force push aimed at a remote that does not
  exist is harmless by construction, and that probe was available the
  whole time. An untested control was recorded as untestable, which is a
  stronger claim than the evidence supported and one that removed the
  question from the queue of things anyone would attempt.
  **The practical rule is unchanged: never allow-list a command family
  that carries a deny.** Its basis is now narrower — one family proven,
  not the class — and an allow rule overlapping a deny still buys nothing.
  The historical interval in which `git push` sat in the allow-list is
  recorded rather than papered over: it began when the tiering merged and
  ended with the same-day narrowing. On this evidence the guard was
  probably in force throughout it, which is reassurance and not proof.
  **Mode qualifier, added 2026-08-14, and it narrows this bullet.** The
  probe ran in a session later established to have been in
  `bypassPermissions` mode, under which an ask is auto-approved without
  ever surfacing at the operator's terminal. **The "no prompt fired" half
  of the observation is therefore uninformative**: no prompt would have
  appeared whatever the rules said, so that half evidences nothing and
  must not be cited as though it did. The deny half is untouched — denies
  are not auto-approved, the command was refused, and the refusal came
  back in the guard's own words. What survives without qualification is
  that **the deny fired while a matching allow rule was in force, in
  bypass mode**. What does not survive is the unqualified claim that deny
  beats allow, because the ask layer that would compete with the deny in
  default mode was inert throughout.
  **This bullet previously read "TESTED 2026-08-14, and the guard HELD"
  and cited the absent prompt as part of the result.** The change is
  recorded rather than made quietly: the mode was not known when the
  bullet was written, and a reader should be able to see that the
  qualifier arrived afterwards.
  **OPEN QUESTION WITH A LIVE ROUTE, not a permanent gap.** The successor
  session of the same day attested ask-tier by behaviour, so a
  default-mode re-run of the discriminator is available: same rule, same
  deny-carrying family, in a session where asks surface and both halves of
  the observation therefore carry information. Owed at WS-E 69 fix item 5,
  not run. Until it runs, the practical rule **never allow-list a command
  family that carries a deny** stands on ground narrower still than the
  paragraph above already concedes. Full record and the live-route reframe
  at `docs/governance/PRECEDENCE_DISCRIMINATOR_OUTCOME_2026-08-14.md`.

## Post-merge verification — required

The first session after merge is the evidence, not the session that
wrote this.

1. **Expect prompts that have never appeared before.** Protected-path
   asks will fire on the PowerShell tool for the first time in this
   repository's history. A new prompt is the matcher fix working. The
   first such prompt is its live confirmation, and must not be read as
   a failure of the tiering.
2. **Resolve the precedence UNKNOWN — DONE 2026-08-11, and it failed.**
   The test as first written turned on observing an *ask*, which the
   harness cannot observe from inside a session; that flaw is why the
   question survived the arc that created it. The working form inverts
   the signal: run an allow-listed command that also carries a guard
   ask, and have the operator **decline** if prompted. A refusal is
   visible in the tool result where an approved ask is not, so both
   outcomes are observable. The probe — `git branch -d` on a throwaway
   branch — executed with no prompt, while the guard returned `ask` for
   that exact string when fed the payload directly. Tier 1 narrowed the
   same day. **Design lesson worth more than the result: a verification
   whose only signal is a prompt cannot be self-verified, and must be
   rebuilt around a signal the harness can see.**
   **Confirmed after the narrowing, which makes this a controlled pair
   rather than a single observation.** One alternative explanation
   survived the probe: that the session was auto-approving at the
   permission-mode level, in which case Tier 2 had never gated anything
   and the narrowing addressed the wrong cause. The two are
   indistinguishable from inside the harness and demand different
   fixes. What separates them is what happened next. With the allow
   entries removed and nothing else changed — same session, same guard,
   same operator — a protected-path edit and a `git push` both
   prompted, minutes after an allow-listed command had executed
   silently. The allow rule is the only variable between the two
   observations. Mode-level auto-approval is excluded; precedence is
   the cause; and the narrowing addressed it rather than a symptom.
3. **Confirm Tier 1 actually reduces prompts.** If routine git and
   battery calls still prompt, the rule strings do not match and are
   to be corrected against observed behaviour rather than reasoned
   about further.

## Machine-local settings

`.claude/settings.local.json` is gitignored and remains legitimate for
machine-local experimentation. It is never policy: a permission
configuration that no reviewer can see is the opposite of a governed
artefact, which is why Tier 1 lands in the tracked file. Its two prior
entries are disposed of as follows — the docs-check rule migrates into
tracked Tier 1, generalised to its argument forms; the exit-code echo
rule is **dropped**, because it is tooling for reading an exit status
in isolation and tracked policy must not enshrine a check method this
repository's own findings discredit. Clearing the stale local entries
is an operator act on their own machine.
