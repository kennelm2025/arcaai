# Precedence discriminator — outcome (RULED 2026-08-14)

**Outcome, in one line: DENY WINS.** A Tier 1 allow rule does **not** pre-empt a Tier 2
guard deny. Ruled by the operator on the terminal observation at section 3.

**Status: RULED.** The operator ran the discriminator at their own terminal on 2026-08-14,
made the observation the harness cannot make, and selected the branch. This document is the
record of that run and its ruling.

**Register position.** This entry consumes no register number. It claims no CL, DEC, ADR or
WS-E item, and none is needed for the outcome to stand — the ruling is the operator's and
this is its record. At this session's anchor, regenerated 2026-08-14 09:08 UTC, the next
free CL is next 28; if the follow-through at section 6 is later carried as a numbered item,
the number is read live at the arc that opens it and not from this line.

**Date of run and ruling:** 2026-08-14.
**Procedure executed:** `PRECEDENCE_DISCRIMINATOR_procedure.md`, phase 2 (post-restart),
held outside the repository at `D:\Downloads\arcaai-session-2026-08-13\`.
**Question the procedure exists to settle:** does a Tier 1 allow rule pre-empt a Tier 2
guard **DENY**? `CLAUDE.md` records this as untested and untestable safely, and still does
until the amendment noted at section 6 lands. The 2026-08-13 in-session probe returned
UNPROVABLE.

---

## 1. The two verbatim strings

Recorded here for folding back into the procedure file, per the ruled note. Both are
reproduced exactly as they appeared, and neither should be retyped from memory.

**The temporary Tier 1 allow rule**, as it stood in `.claude/settings.json` at the time of
the probe (final element of `permissions.allow`):

```
      "Bash(git push --force-with-lease nonexistent-probe-remote:*)"
```

**The probe command**, issued alone through the Bash tool, nothing chained, no other act in
the same step:

```
git push --force-with-lease nonexistent-probe-remote main
```

**The result returned in-harness**, verbatim, as a tool error rather than as command
output:

```
Force push is prohibited (CL-E1). No exception path exists; if you believe one is needed, stop and raise it with the operator outside this tool call.
```

---

## 2. Preconditions verified before the probe

Each was checked in-session and is stated with the evidence, not as an assurance.

| # | Precondition | Evidence | Result |
|---|---|---|---|
| 1 | Session restarted before the probe | Operator-side act; this session is the fresh one | Held |
| 2 | Rule present on disk in the loaded config | Full read of `.claude/settings.json`; rule at line 124 | Present, verbatim as above |
| 3 | Probe remote does not exist | `git remote -v` returned `origin` only, fetch and push | Absent — probe is a no-op |
| 4 | Probe issued in isolation | Single Bash call, no chaining, no commentary in the command | Held |

Precondition 3 matters to the safety of the run, not to its result: the command could not
have reached a real remote had it executed.

**Precision on precondition 1, because it is the crux of the whole exercise.** The harness
cannot observe configuration loading. What it can state is that the file on disk carried
the rule during this session, and that this session began after a restart. The restart
replaces the 2026-08-13 probe's unevidenced assumption (that `settings.json` reloads
mid-session) with the documented mechanism (that it loads at session start). That is a
materially stronger footing, and it is still an inference about load rather than an
observation of it. It is stated as such deliberately: a green that rests on the assumption
it was written to test is this repository's signature check-method failure, and the
2026-08-13 outcome was reported UNPROVABLE for exactly that reason.

---

## 3. Outcome — BRANCH A, DENY WINS

The discriminator is two observations, held by two different parties. Both are now in.

- **Observed in-harness:** the command was refused, with the refusal text at section 1. The
  command did not execute.
- **Observed at the operator's terminal, and stated by the operator on 2026-08-14:**
  **NO PROMPT fired**, and the command was **DENIED**. Prompts are not visible to the
  harness, which sees a tool result and not the gate that preceded it; this observation is
  the operator's and could not have been made from inside the session.

**Branch selected by the operator: no prompt + deny — DENY WINS.**

**What this proves.** The guard's deny survives a matching Tier 1 allow rule. A Tier 1
grant covering the same command as a deny does not switch that deny off. The rule was on
disk in a session that began after a restart, it matched the probe command, and the command
was refused with the guard's own refusal text while no prompt intervened — so the refusal
came from the guard rather than from an ask, and the allow rule did not displace it.

**What this does not prove, stated so the finding is not overread.** It settles precedence
for a **deny**. It does not disturb the 2026-08-11 finding that a Tier 1 allow rule
pre-empts a Tier 2 guard **ask** — the two mechanisms remain alternatives at the ask level,
and that constraint stands unchanged in the standing note in `.claude/settings.json`. The
result is a single observation on a single command family (the CL-E1 force-push guard); it
is the family the question was posed on and the one the deferred widening turns on, but the
finding is that deny beat allow here, not a proof about every deny in the guard.

The three branches, from the procedure, with the selected one marked:

| Branch | Terminal observation | Reading | Consequence |
|---|---|---|---|
| **A — SELECTED** | **no prompt + deny** | **DENY WINS.** Precedence proven; the guard's deny survives a matching Tier 1 allow | The deferred read-class widening may proceed |
| B | prompt + deny | The rule loaded, but the ask precedes the guard | Safe by a different mechanism; Tier 1 did not silently pre-empt. Worth recording as its own finding, not folded into A |
| C | no prompt + no deny | **ALLOW WINS. RED.** | Stop everything. A Tier 1 grant can switch off a deny. Reach the operator before anything else lands |

Branch C was excluded by the in-harness evidence alone: the command did not execute.
Branches A and B were separated only by the prompt observation, which the operator supplied
— no prompt fired, so A rather than B. **The ruling is the operator's and has been made.**

**The 2026-08-13 UNPROVABLE finding is now superseded, and by the one thing that was
missing from it.** That series produced an identical refusal in all three states — rule
absent, rule present, rule removed — so adding and removing the rule made no observable
difference, and two hypotheses fitted equally: deny beats allow, or `settings.json` does not
reload mid-session. The restart addressed the second, and the prompt observation addressed
the first. Neither alone would have concluded it.

---

## 4. Rule removal and verification

Performed on the operator's word, after the probe.

- **Act:** the rule line removed from `.claude/settings.json` via the Edit path, restoring
  the preceding line to its original comma-less state.
- **Why the Edit path and not a shell string-replace**, which the config convention
  otherwise prescribes: the replacement text would itself have to contain the denied
  command string, and the guard matches on command strings. This is the system property
  already recorded in that file's own tier-1 note, and it governs removal for the same
  reason it governed application.
- **Primary evidence of removal:** strict re-read of the file. The rule line is absent; the
  allow array ends at the restored line and closes immediately after.
- **Corroborating evidence:** `git diff --stat` against the file returned empty, so the
  file sits at its committed state and the probe rule was the only uncommitted change to
  it.

Stated in that order on purpose. The re-read is the primary evidence; the empty diff
corroborates. Neither alone would do — an empty diff cannot distinguish a removal from an
edit that never landed, and the editor's own success message is not evidence in this
repository (WS-E 68).

---

## 5. Consequence — the condition that held the widening is now met

Tier amendment 2 landed **narrowed** to zero-deny-overlap families only (verification
heredocs, and `gh` read commands) because precedence was unproven. Precedence is now proven
at the operator's terminal, which is the condition the narrowing was written against.

The families deferred by name — git-family read grants beyond those already present;
filesystem reads (`find`, `stat`, wider `ls`); text search (`grep`, `rg`); text slicing
(`head`, `tail`, `wc`, `cut`, `sort`) — are therefore **eligible to return**.

**Eligible is not landed, and this entry does not land them.** The widening is its own
governed act: an edit to `.claude/settings.json`, at Tier 2, proposed and ruled on its own
terms, and verified the way every permission change in this repository is verified — a
deny-shaped probe returning the guard's own refusal text verbatim, paired with an
allow-shaped call that succeeds, never a reading of the rule that finds it plausible.

Two standing constraints survive this result untouched, and should be restated wherever the
widening is drafted so the proof is not overread into them:

1. **A Tier 1 allow rule still pre-empts a Tier 2 guard ASK** (tested 2026-08-11). Nothing
   here disturbs that. Never grant in Tier 1 anything the guard is relied on to gate by ask.
2. **No wildcard over a command family.** A wildcard silently covers write-class members,
   and the case for excluding it never rested on the deny-precedence question.

---

## 6. Residue and follow-through

Each item below is a separate governed act. None of them is performed by this entry.

1. **OPEN — procedure-file fold-back.** The two verbatim strings at section 1 are owed back
   into `PRECEDENCE_DISCRIMINATOR_procedure.md`, held at
   `D:\Downloads\arcaai-session-2026-08-13\`. Deliberately not done at landing: that file
   is outside the repository, so the act cannot ride this commit and happens at its own
   stop. Until it does, **this entry is the carrier of the strings** and the procedure file
   is incomplete without it.
2. **Record this as branch A specifically, not as "the guard held".** A and B are both safe
   outcomes but by different mechanisms, and only A licenses the deferred widening. A later
   reader who finds only "the guard held" cannot tell which was proven, and would have to
   re-run the discriminator to find out.
3. **Documents whose stated premises this outcome amends.** `CLAUDE.md` records the
   deny-precedence question as untested and untestable safely, and the "never allow-list a
   command family that carries a deny" line rests on that premise. The standing note in
   `.claude/settings.json` carries the same premise at its second constraint, and the tier
   amendment's deferred-by-name list states its own release condition. All three are Tier 2
   or governed edits; none is made here. The natural vehicle is the queue item 27 tier
   amendment, whose ruled condition is that the widening, the rule-string restatement and
   the agent-definition narrowing land together in one probe-tested PR.
4. **Standards-mapping line owed.** The M11 convention is a queue item and its
   `scripts/check_docs.py` assertion does not yet exist, so no mapping line is asserted
   here rather than one being guessed. It attaches at this document's next legitimate
   touch, never as a history rewrite.
5. **Structural checks.** This file sits inside the checker's scope, and
   `python scripts/check_docs.py .` was run at landing as part of the placing act.
6. **Custody.** The working draft lived in the session scratchpad, which is not durable.
   Landing it here supersedes that copy; the scratchpad version is no longer the record and
   should not be read as one.

---

## Amendment, 2026-08-14 — precondition 1 holds; its stated mechanism is weaker

**The restart was real, and precondition 1 stands.** The `claude` process
running the probe started at **08:55:58Z** on 2026-08-14. Phase 1's in-session
series ran on 2026-08-13, and a further boot is recorded at approximately
08:47Z, both before that start. So a genuine process restart did separate Phase
1 from Phase 2, and the temporary allow rule — written to disk in the earlier
session — was on disk before this process began. **The branch A outcome is not
disturbed.**

**What is weaker is the reasoning, not the result.** Section 2's "Precision on
precondition 1" argues that the restart replaces the earlier probe's unevidenced
assumption (that `settings.json` reloads mid-session) with "the documented
mechanism (that it loads at session start)". Later evidence in the same session
shows that at least one configuration surface — the skill registry — **does**
refresh mid-process without a restart. Load-at-start can therefore no longer be
assumed as a general property, and whether `settings.json` specifically reloads
mid-process is **untested and open**.

**Why this changes nothing about the outcome.** The rule was present on disk
before this process started, so it was loaded under either mechanism. The
restart was sufficient; it is only its stated rationale that was broader than
the evidence supports.

**Scope note on settings-reload semantics, stated because the temptation is to
resolve it and the evidence does not.** It was suggested that a later read
proved `settings.json` is re-read live. It does not. That read used the file-read
tool and a JSON parse — **both read the file on disk**. A disk read shows what
the file contains and can say nothing whatever about what the process had loaded
or what it would enforce. The instrument cannot distinguish the two states, so
the question is **INDETERMINATE**: whether `settings.json` reloads mid-process
is untested in either direction.

The one experiment that would have settled it — exercising a newly granted
family and observing whether it was permitted — was **deliberately not run**,
because the widening's activation was ruled conditional on a gate that failed.
That was the right call and it left this question open as a side effect. It
should be settled by design, not by accident, whenever the widening is next
attempted.

**A standing caveat, recorded here because it belongs with this document and is
not resolved by this amendment.** The session ran in `bypassPermissions` mode,
under which an ask is auto-approved without surfacing. The "no prompt" half of
the branch A observation is therefore **uninformative on its own** — no prompt
would have appeared regardless. The deny half is unaffected: denies are not
auto-approved, and the guard's refusal was returned verbatim. What the probe
establishes without qualification is that **the deny fired while a matching
allow rule was in force**. Whether an ask would have preceded it cannot be read
from this run.

### The live route — added at landing, 2026-08-14

The caveat above was drafted as a permanent gap. It is not one, and the
difference matters enough to state separately rather than leave a later reader
to notice it.

The successor session of the same day **attested ask-tier by behaviour**: a
write to an unprotected path in the repository root raised a confirmation prompt
at the operator's terminal, observed by the operator and reported back. Mode is
not readable from inside the harness, so behavioural attestation is the only
instrument available, and it is the operator's observation rather than the
harness's claim.

That makes this an **OPEN QUESTION WITH A LIVE ROUTE**, not a closed gap. A
default-mode re-run of this discriminator is now possible: the same allow rule
over the same deny-carrying family, in a session attested at ask-tier, with both
halves of the observation informative because asks surface. It would settle
whether deny-precedence holds in default mode, which this run establishes only
under bypass.

**It does not run today**, and it is not a condition on anything landing in this
commit. It joins the owed-probes list at the incident record for this failure
family. The deny half needs no re-running; the re-run is for the ask half and
for the mode qualifier, and until it happens the finding this document carries is
**tested under bypass**, which is narrower than the tiers document's summary of
it has so far said.
