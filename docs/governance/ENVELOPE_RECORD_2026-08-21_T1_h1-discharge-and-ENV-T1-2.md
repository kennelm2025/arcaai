# Envelope record — 2026-08-21, Terminal 1: H1 discharge and ENV-T1-2 disposition

**Status: RECORD OF AN ENVELOPE, appended not patched. No register number
consumed.** No WS-E, DEC, ADR, CL or arc number is claimed by this document.
Where a number would be needed it is cited as "next", per the PR #85
convention. The arc-number question is raised at section 8 and left to the
chair.

**Envelope:** PROMPT 127 (dispatched), PROMPT 127R (ruling delivery and
resume). Target Terminal 1. Class: build, trial envelope.
**Repository state:** HEAD `574cd7b`, branch `main`. Working tree carried two
untracked paths during this envelope — the M13 standards register draft, which
belongs to ENV-T1-3 and was not touched here, and this file.

---

## 1. The ruling, verbatim

Reproduced in full because a record that summarises its own authority is not a
record. Chair, 2026-08-21, resolving section 1 of the PROMPT 127 outcome:

> T1 does not extend the pre-flight under this envelope. The ownership
> assertion — fourth condition on the vector-store triple, expected-owner
> semantic, and inherited-ACE outcome class under three-outcome discipline — is
> assigned to queue item 36(b), sequenced as one pre-flight arc with the
> environment-hash ASSERT. T1 proceeds to its spine head at ENV-T1-2.
> The detection window until 36(b) lands is accepted by the Chair as a known
> trade-off; the instrument's value is recurrence protection.

**Consequence carried forward, stated so it is not lost between registers.**
Until item 36(b) lands, `scripts/d22a_preflight.py` returns GREEN on a store
whose ownership is defective, because its vector-store triple asserts
exists / readable / writable and has no ownership condition. The chair has
accepted that window knowingly. What must not happen is a later reader treating
a pre-flight GREEN as evidence that the H-6 precondition holds; it is not, and
it will not be until the fourth condition exists.

## 2. H1 — vector-store ownership repair: DISCHARGED

H-6 of `docs/governance/RULINGS_RECORD_2026-08-13_H-batch.md` ruled the repair a
confirmed hard precondition and ruled it an operator act at the operator's own
terminal, the harness never elevating and never assuming the owner role. It was
the oldest single item on the board.

**Operator act, 2026-08-21, elevated terminal:** `takeown` with recursion
followed by `icacls` `/setowner` to `MIKEK\mikek` with `/T`. Chair-reported
result: 7 items processed, 0 failed.

**Before-state**, captured non-elevated by this terminal under PROMPT 127 and
pinned at section 3a of that envelope's outcome file: directory owner
`BUILTIN\Administrators`; all six children likewise; all eight ACEs inherited,
with the only write route an inherited grant to authenticated users.

**After-state, independently verified by this terminal under PROMPT 127R**, by
a non-elevated recursive `Get-Acl` sweep — not taken on report:

```
DIR  OWNER=MIKEK\mikek
1ba9a3a7-f577-4ce0-87bb-4d53de0a30fd   OWNER=MIKEK\mikek
chroma.sqlite3                         OWNER=MIKEK\mikek
data_level0.bin                        OWNER=MIKEK\mikek
header.bin                             OWNER=MIKEK\mikek
length.bin                             OWNER=MIKEK\mikek
link_lists.bin                         OWNER=MIKEK\mikek
```

Seven items — one directory and six children — which reconciles exactly with
the chair's reported count. The recursion finding raised under PROMPT 127 was
therefore load-bearing: a non-recursive repair would have left `chroma.sqlite3`
and the four HNSW segment files Administrators-owned while reporting success.

**Two things this discharge does NOT establish, recorded so the green is not
overread.**

1. **The ACL is untouched.** The ACE set remains all-inherited, including the
   modify grant to authenticated users. Ownership was the ruled subject of H-6;
   the inherited-only ACL is a separate question and is expressly not settled
   here.
2. **Nothing in the repository can detect this repair, or its regression.**
   Verification above was performed by hand at the terminal. Until item 36(b)
   lands there is no instrument that reads a filesystem owner — confirmed by
   search across the scripts tree, where every `owner` hit is a Postgres role
   comment. Should the store be recreated by an elevated process tomorrow, no
   check in this repository would notice.

## 3. ENV-T1-2 — the two dispatch probes: NEITHER VERIFIED NOR STRUCK

The dispatch order at `docs/governance/DEC-0018_CANDIDATE_2026-08-17.md` defines
ENV-T1-2 as verify-or-strike: run the two dispatch probes and close, or strike
with recorded rationale. Both branches were assessed against the live state and
**neither is available to Terminal 1**. The reasoning is recorded in full,
because a halt whose grounds are not written is indistinguishable from a stall.

### 3a. The instruments no longer exist

The two probe instruments were staged as untracked paths under the agents and
skills directories, and are recorded as such at section 3, criterion 4 of
`docs/governance/COMMISSIONING_SESSION_RECORD_2026-08-16_d22a-runner-spike-2.md`,
which tolerated them for that session by operator ruling with **a terminus at
the earlier of the next session open or 2026-08-22**.

Read live this envelope: the agents directory holds the corpus lister and the
test author and nothing else; the probe route A2 skill directory does not
exist. Neither path appears in any commit on any branch — they were untracked
throughout their life and are now absent from disk.

*(Those two paths are deliberately written without backticks throughout this
document. The docs check enforces that a backticked repo-relative path exists,
and these do not; backticking them would fail the check that protects against
dead citations.)*

**This is compliance with a ruling, not residue and not an incident.** The
terminus was reached and the instruments went. No WS-E number is owed for their
absence and none is claimed.

### 3b. Verify is unavailable, and it is not a permission-mode question

Re-creating either instrument means writing under the agents or skills
directory. Those are two of the four paths in the never-silent DENY set, ruled
2026-08-14, whose stated cost was accepted at the time in these terms: there is
no in-session write to those paths again, including the write that would repair
the guard or roll back the deny.

A deny is not satisfiable by a permission mode, which is the entire reason the
2026-08-14 ruling chose deny over ask. So this is not a case of Terminal 1
lacking a grant it might be given; it is a case of the act being closed to
every mode.

**The repository asserts this itself.** At
`tests/governance/test_guard_protected_paths.py` the never-silent path list
includes the route B agent path as a fixture, and the parametrised test asserts
that a Write to it returns a deny carrying the never-silent prefix. The suite
states, as a standing assertion, that the instrument this envelope would need
cannot be created by the tools this envelope holds. No write was attempted;
none needed to be.

Route A2 carries a second obstacle beyond the write: its render line executes a
command carrying an absolute deny, by design, since that is what makes it a
discriminator. Arming it is a deliberate act of running the known-bypassing
path, which is an operator decision on its own merits.

### 3c. Strike is Class C, so Terminal 1 may not take it

DEC-0018 is activated — entry condition E1 is recorded satisfied at
`DECISIONS.md`, the guard fixes having landed with WS-E 72, 73 and 74
discharged. Class B self-authorisation is therefore live for reversible acts
inside an envelope. **A strike here is not one**, on three independent grounds,
any one of which is sufficient:

1. **Subject matter.** Class C reserves the guard deny set and permission tiers
   to the chair. These probes exist to establish whether the guard is invoked at
   all on two dispatch routes, which is the coverage question underneath the
   deny set rather than a question beside it.
2. **It touches the ruling itself.** DEC-0018 carries the render-route hole as a
   named standing risk of the unattended model, explicitly *until that route is
   proven governed*. Striking the disambiguation probe would convert a
   conditional risk-carry into a permanent unknown, editing the terms on which
   DEC-0018 accepted the risk. Class C reserves anything touching the ruling
   itself.
3. **It is not reversible.** Class B eligibility is conditioned on
   reversibility. Retiring the last instrument aimed at an open bypass is
   reversible on paper — an instrument can be rewritten — but not in effect,
   since the route stays unproven for as long as the strike stands, and
   `CLAUDE.md` queue item 49 makes that unproven state binding on the scoping of
   every future envelope reachable by a skill render.

**Therefore ENV-T1-2 halts to the chair.** Terminal 1 declines to strike rather
than striking by default, and the distinction matters: a strike taken because
verification was merely unavailable would record a governance decision that
nobody made.

## 4. What the probes are actually for, since a strike would be ruling on this

Stated compactly so the chair's decision does not require re-reading the failure
record at `docs/governance/GROUP1_FAILURE_route-a-bypass_2026-08-14.md`.

**Route A2 — the frontmatter disambiguation probe.** The 2026-08-14 failure is
established and is not what A2 would re-demonstrate: a skill render line
executed a command carrying an absolute deny, returning git's own error with no
prompt and no guard text. What remains unknown is **which of two defects caused
it** — skill renders never routing through the hook at all, which is
harness-level and unreachable by any change in this repository; or the probe
skill's own frontmatter grant pre-empting the deny inside a ceremony, which
would mean any skill can self-grant past the deny layer by writing its own
frontmatter. The two have entirely different fixes and the second is the worse.
A2 is the same render with the frontmatter grant removed, and it separates them.
This is the higher-value probe of the two.

**Route B — subagent dispatch.** Whether the subagent dispatch path is governed.
Its original stake is partly spent: the failure record argued it mattered because
the agents-directory narrowing rested on the premise that this path is governed,
and that narrowing was superseded when all four of those paths became DENY on
2026-08-14. Its live stake is the unattended model — an envelope that dispatches
subagents is governed only if that path is. Note beside it, from queue item 49,
that the PreToolUse matcher names the two shells and the four file-writing
tools and reaches no further, which is a coverage fact bearing on this probe's
design but not a substitute for running it.

## 5. Recommendation to the chair, offered as options rather than a preference

1. **Re-install both instruments as an operator act**, by the route every other
   change to those directories takes: drafted outside the tree, installed at the
   operator's own terminal, then branch, PR, merge — with a fresh terminus
   stated at installation, since the last one expired and that is why they are
   gone. Terminal 1 then runs them under a follow-on envelope. This is the only
   option that closes the question.
2. **Split the disposition.** Re-install A2 only, and rule route B struck on the
   narrower ground that its original premise was superseded, recording that its
   unattended-model stake passes to the envelope-guard work at queue item 48.
3. **Strike both**, which the chair may do and Terminal 1 may not, accepting
   that the render route stays unproven and that queue item 49's binding on
   envelope scoping becomes permanent rather than conditional.

Whichever is chosen, the probe-spec discipline recorded at queue item 8's
2026-08-19 instance applies: pass conditions are stated **per tier**, because an
approved ask and a live deny have opposite observable signatures, and on the ask
tier no observable signature discriminates at all.

## 6. Envelope-design findings, for the trial friction ledger

Recorded here because the chair's routing acknowledgment established a friction
ledger for the trial, and these are its natural entries.

1. **Test runs are granted but unreachable.** The envelope grants the Bash tool
   for test runs. This repository's working protocol requires the `arcaai`
   environment before any Python work; the Bash tool does not persist shell
   state between calls, so an activation cannot be carried to a following
   command, and chaining activation onto the battery command is forbidden by the
   standing convention against grant-evasion by chain. Verified live rather than
   assumed: the shell resolves to base anaconda at Python 3.13.9, not the
   required 3.11.15. **No test was run in this envelope**, and none is reported
   green or red — the environment could not be confirmed, so the protocol's own
   instruction is to stop and say so. An envelope that grants an act its tool
   discipline forecloses is a defect in the envelope, not in the terminal.
2. **A file-queue envelope cannot land its own work.** Recording acts were
   ordered and performed as working-tree writes, but the envelope's read-only
   Bash discipline excludes every git write verb, and HEAD is `main`, which is
   never committed to directly. The output of this envelope is therefore an
   uncommitted file that a later act must branch, commit and PR. That is
   correct as far as it goes, but it means envelope completion and evidence
   durability are separate events, and the second one is not scheduled by
   anything.

## 7. What this record does not establish

- It does not establish that the guard is or is not invoked on either dispatch
  route. Both probes remain unrun, and this document is the reason recorded, not
  a substitute finding.
- It does not establish anything about the ACL of the vector store beyond
  ownership.
- It reports no test result of any kind.

## 8. Owed after this envelope

1. **The chair's disposition on ENV-T1-2** from the options at section 5.
2. **Commit and PR of this record**, which cannot be done from inside the
   envelope that wrote it.
3. **An arc number question, raised and deliberately not answered.**
   `docs/governance/ARC_REGISTER.md` allocates arc identifiers and its rule is
   the highest sequence for the date plus one. No arc was opened for this
   envelope and none is claimed here, because the register's rows are
   append-only and carry PRs and a CLOSE timestamp that this envelope cannot
   supply. Beside it, a register-state observation offered without
   interpretation: the row for the runner conformance arc of 2026-08-19 still
   reads open.
4. **Queue item 36(b)** now carries the ownership assertion by the ruling at
   section 1, sequenced with the environment-hash assert as one pre-flight arc.

---

## Addendum — 2026-08-21: ENV-T1-2 disposition ruled (PROMPT 127R2)

Appended, not patched. Section 3 records ENV-T1-2 as halted to the chair, with
three options offered at section 5. The chair has ruled, adopting option (a).
The ruling is reproduced verbatim below so that this record carries the
disposition and not merely the question that preceded it.

> RULING (Chair, 2026-08-21, resolving PROMPT-127R.outcome.md section 1;
> option (a) adopted):
> Both probe instruments are re-installed by the Chair as an operator act
> at the Chair's own terminal, each with a fresh stated terminus. Route A2
> retained: it disambiguates two defects with entirely different fixes,
> and the worse (skill self-granting past the deny layer via frontmatter)
> must be found before unattended operation scales. Route B retained: its
> live stake is the unattended-model path, and that stake ceased to be
> marginal when DEC-0019 proposed largely-unattended dispatch as the
> operating default; striking it as traffic grows would convert
> DEC-0018's conditional risk-carry into a permanent unknown. Option (c)
> rejected on that same ground; option (b) rejected because it discards
> the probe whose purpose is now most relevant.
> Caveats carried: the re-install is Chair-only (CC remains barred from
> those paths); arming A2 knowingly exercises the known-bypassing path
> and happens deliberately, under a follow-on envelope, with evidence
> capture — not casually.
> Deferred by the Chair: the arc-number question goes to close-down; the
> 2026-08-19 runner-conformance row stands as it reads.

**What this settles.** ENV-T1-2 is no longer an open verify-or-strike. Both
probes survive, and the blocking condition moves from a governance question to
an operator act. Section 3c stands as the record of why Terminal 1 declined to
strike rather than striking by default, and the chair's rejection of options (b)
and (c) rests on the same ground that section gave: a strike converts DEC-0018's
conditional risk-carry into a permanent unknown.

**What it does not settle.** Section 7 is unchanged in every particular. Both
probes remain unrun and neither route is proven governed, so the standing
constraint on envelope scoping continues to bind. The chair's caveat that arming
route A2 knowingly exercises the known-bypassing path is a live condition on the
follow-on envelope rather than a formality.

**Register-hygiene note, recorded because a verbatim quotation cannot be
silently corrected.** The ruling cites DEC-0019 as a bare number. Read live at
the time of this addendum, that number appears nowhere in this repository —
absent from the decisions register and from every markdown file — so it is
unconsumed. The standing convention from the PR #85 correction is that an
unconsumed register number is written as "next 0019" and never bare in a
document under the docs tree, because the manifest scanner cannot distinguish a
bare number from a claim that the item exists and reports a spurious divergence.
The quotation above is left exactly as ruled, since editing a ruling to satisfy
a citation convention would be the worse error. This note is the alternative:
whoever runs the next manifest should expect that divergence and read its
explanation here rather than chase it.
