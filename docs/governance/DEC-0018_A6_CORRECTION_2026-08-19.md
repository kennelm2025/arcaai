# DEC-0018 A6 — correction of record, 2026-08-19

**Status: LANDED with DEC-0018.** This file carries two things the register
entry cites and cannot hold at its own length: the chair's ruling of record
verbatim, and the corrected authorisation architecture that replaces A6 as
drafted.

**Why a correction rather than an amended draft.** A6 was ruled on a premise
that a read of the tree, performed the same evening, found already answered.
The ruling is not wrong about what it decided; it is wrong about the mechanism
available to implement it. The ruling therefore stands as delivered and is
reproduced unaltered below, and the correction sits beside it — the discipline
`docs/governance/CORRECTIONS_cost-basis_2026-08-19.md` states, where a
narrative artefact is corrected beside itself rather than edited.

---

## 1. The ruling of record, verbatim

Delivered by the chair in one sitting, 2026-08-19, and preserved at transport
as `ARCA-D-DEC-0018 [ANSWERED]` pending this write. Reproduced here in full so
the register entry cites a document rather than a mailbox.

> **Q-R1.** DEC number: the delegation/envelope model (17 Aug candidate + Rider
> R1 + Rider R2) takes DEC-0018. The dashboard claim is reassigned to the next
> free number at the moment it is formally advanced. Rationale: number follows
> the work — the envelope mechanism is the live collision, has consumed the
> round-trip test (PROMPT 144/145), and is the prerequisite for unattended
> operation.
>
> **Q-R2.** Full form adopted — candidate + R1 + R2, subject only to blocking
> Entry Condition E2 (A6.2). A3 adopted as written (ARCA-\* namespace lock
> mandatory: no send, nothing outside the series). A4 adopted as written
> (subject grammar, ID/TS/RE body header, Q→D ruling-by-queue flow now
> standing). A5 adopted as written (arc ID grammar, OPEN/CLOSE timestamps,
> ARC_REGISTER.md authorised; A-2026-08-19-01 recognised as first use,
> timestamps reconstructed at next touch). A6 adopted as written (Part B's
> three grounds resolved contingent on E2 green; merge-to-main permanently
> outside every allow-list, backed by M3 branch protection). Footnote F1
> reductions NOT applied.
>
> **Q-R3.** E2 probe authorised as the next session's first act. No other work
> may precede the two-row probe proving the PreToolUse hook still fires under
> an allow-listed tool.

Consequential state, as delivered with the ruling:

> - Item 27 Part B: resolution path ruled; widening applies only on E2 green,
>   at the operator terminal, scoped to the R1 A1 + R2 A3 toolset.
> - Observability dashboard candidate: renumbered to next-free-at-advancement
>   (currently would be next 0019; cite as "next", never bare, per the PR #85
>   convention).
> - Prompt tally: 144/145 consumed by the round-trip test (post-close, outside
>   any arc — fold-in owed). Next is 146.
> - Cost note: the 08-19 coordinator-session row ($18.20 DIRECT) is WRITTEN
>   (PR #145). What remains outstanding is the /cost for the CC session that
>   executed the round-trip test — supply at that session's close per standing
>   method (sign check, not recollection).

## 2. The chair's amendment ruling, 2026-08-19

Delivered the same evening, after the settings read at section 3:

> Q-R3 is amended. The E2 probe is cancelled unrun — its premise is superseded
> by the tree. This fold-in replaces the probe as the arc's ruled first act.

**E2 is therefore SUPERSEDED, not satisfied.** It never went green, and the
difference decides what A6 can claim. A6 as drafted resolved item 27 Part B's
grounds *contingent on E2 green*. A condition that never occurred cannot be
read as met, and treating a cancelled gate as a passed one is the
blocker-cleared-therefore-proceed step that item 27's together-in-one-PR
condition exists to prevent.

## 3. Three findings from the settings read, verbatim

Read from `.claude/settings.json` this session. The file's own `_tier1_note`
is the source; the quotations are exact.

### (a) Allow pre-empts ask — so a settings widening cannot implement A2

Constraint (1), verbatim:

> "(1) A Tier 1 allow rule PRE-EMPTS a Tier 2 guard ask (tested 2026-08-11).
> The two are alternatives, not layers, so never grant here anything the
> governance guard is relied on to gate."

**Consequence, and it is fatal to the drafted mechanism.** A2's ALLOW-AND-LOG
requires a call to be permitted *and* observed. A settings allow rule permits
by pre-empting the guard, which is the only component positioned to log. The
widening would therefore purchase permission at the exact cost of the
observation that made it acceptable. **A settings.json widening is struck as
the mechanism for A2.** This was not a new probe result — it was proven
2026-08-11 and had been sitting in the file since.

### (b) The deny-overlap prohibition stands

Constraint (2), verbatim:

> "(2) Never allow-list a command family carrying a DENY. AMENDED 2026-08-14:
> the premise has changed but the rule has not. Deny precedence was UNTESTED
> when this was written; it is now PROVEN - a matching Tier 1 allow rule did
> NOT pre-empt the force-push deny, no prompt fired, and the guard's own
> refusal returned. […] The rule stands anyway, on narrower grounds: the proof
> is one observation on ONE command family, and an allow rule overlapping a
> deny buys nothing while risking everything if a second family behaves
> differently."

**The cancelled E2 probe entry is recorded as prohibited-and-never-applied.**
The entry the probe would have added is `Bash(git branch:*)`. Bare `git branch`
reaches `-D`, which carries an absolute deny, so the entry is prohibited by
constraint (2) on its face and would have been prohibited whatever the probe
returned.

**Never-applied is evidenced, not assumed.** `git status` this session shows
`.claude/settings.json` unmodified against HEAD, and the allow list read at
section 3 contains no `git branch` wildcard — only `Bash(git branch -d:*)` and
its PowerShell twin, both lowercase-only and pre-existing.

**One residue was observed and then disposed of mid-session, and the sequence
is recorded rather than tidied into a single tense.** At the opening state
check an untracked `.claude/settings.json.e2-before` sat in the working tree —
a backup taken in preparation for the probe that was then cancelled. Two
independent instruments caught it: the opening `git status`, and the manifest
regenerated at 16:21 UTC, which recorded the working tree as DIRTY with that
one entry. It was flagged as an operator act, because writes to that directory
are denied outright with no exception path and the executor could not remove
it. **It was then removed during this session**; a later check returns absent,
and `.claude/` shows clean.

**Why the disappearance is written down rather than quietly reflected.** A
file that exists at the start of a record and not at its end is exactly the
kind of state an auditor cannot reconstruct later, and the register's own
discipline is that an absence is written explicitly. Note also that the backup
was never the load-bearing evidence for *never-applied*: that rests on
`.claude/settings.json` being unmodified against HEAD, which is checkable at
any point in the future from git alone, whereas the residue was checkable only
while it existed.

### (c) The corrected mechanism: envelope resolution moves into the guard

Ask-tier envelope resolution moves **into** `.claude/hooks/governance_guard.py`
as an **F5-class amendment**: the guard consults an envelope manifest — a
frozen-format file naming the active envelope's scope — and resolves an
in-envelope ask-tier call to allow-and-log, **with the guard itself writing the
log row**.

**Layered with the hook, never alternative to it.** That phrasing is the whole
correction. The drafted mechanism sat *beside* the guard and pre-empted it; the
corrected one sits *inside* it, so the component that grants is the component
that records, and no call is permitted by a path that cannot observe it.

**This amendment is owed as its own governed act and is not started here.** It
is a `.claude/hooks/` change, which is drafted outside the tree, installed by
the operator at their own terminal, then branch, PR, merge — the F1 to F4
route. A design brief, panel-reviewable, then a chair ruling, then install.

### (d) The Gmail and MCP leg of A3 survives unchanged

The PreToolUse matcher, read from the file:

> `"matcher": "Bash|PowerShell|Edit|Write|MultiEdit|NotebookEdit"`

MCP tools are not named, so the guard does not gate them. **Unattending the
prompt queue therefore carries zero deny overlap** — the queue leg of A3 needs
no widening at all, because nothing gates it today.

**Stated as a fact about coverage, not as reassurance.** The same read that
makes the queue leg safe to unattend also says the guard does not see MCP
calls, which is a coverage gap of the WS-E 64 shape rather than a design
feature. It is recorded here so a later reader who widens MCP use finds the
observation already made.

### (e) The render-route hole is a named standing risk of the unattended model

Recorded at `docs/governance/GROUP1_FAILURE_route-a-bypass_2026-08-14.md` and
summarised in the rollback note of `_tier1_note` Amendment 4, verbatim:

> "A skill render line executed a command carrying an absolute DENY - the
> force-push discriminator, aimed at a nonexistent remote - and returned git's
> own error rather than the guard's refusal, with no prompt and no deny at the
> operator's terminal. The guard was never invoked on that path."

And on what the rollback did not do:

> "It does NOT close the hole the probe found: allow rules only ever permit,
> never block, so removing them does not constrain a render that bypasses the
> guard entirely. Closing that is harness-level, or a frontmatter rule, and
> which of the two is owed to a disambiguation probe that has not run."

**Carried forward as a NAMED STANDING RISK until the route is proven
governed.** The reasoning is specific to unattended operation rather than
general caution: the envelope model's whole purpose is to run acts without a
person at the prompt, and the render route is a path on which the guard is
never invoked and no prompt fires. Attended operation has a human as the
backstop for exactly that case. Unattended operation removes the backstop and
multiplies the traffic on the path that has already failed once.

## 4. What this correction does not do

- **It does not widen anything.** No settings entry is added, removed or
  changed by this PR; the file is untouched.
- **It does not discharge the F5 amendment.** The mechanism is specified, not
  built. Queue item 48 carries the design brief.
- **It does not close the render-route hole**, nor decide between the
  harness-level and frontmatter fixes. Queue item 49 carries the
  disambiguation probe.
- **It does not make E2 green.** E2 is superseded and stays superseded; if the
  question it was to answer ever matters again, it needs a fresh probe with a
  fresh premise.

## 5. A limitation this file states rather than inherits

The 17 August candidate, Rider R1 and Rider R2 — the documents DEC-0018 adopts
"in full form" — **are not in this repository.** They exist in coordinator chat
and in Gmail transport. Section 1 preserves the ruling *about* them, which is
what makes the decision citable at all, but a reader cannot presently read A1
through A6 in their own words, and the labels used throughout this file are
therefore references to text held outside the evidence perimeter.

That is a live instance of the `CLAUDE.md` queue item 34 M2 gap, and it is the
second recorded one: the 2026-08-10 rulings record survived only on the
operator's Downloads folder and entered the tree on 2026-08-13 only because it
was supplied from disk. **Committing the candidate is owed.** It is not done
here because this PR's scope is five named edits and authoring a sixth document
from transport is a separate governed act.

No control mapping line is carried, for the reason
`docs/governance/SESSION_COSTS.md` states: queue item 34 M11(d) requires
per-class mapping content to be defined once in the control framework, and that
framework does not exist yet.
