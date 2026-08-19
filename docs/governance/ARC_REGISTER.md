# ARC REGISTER — append-only

Authorised by **DEC-0018 A5**. One row per arc. **Append-only**: rows are
added, never edited or removed. A correction is a new row citing the row it
corrects, on the same discipline as every other register in this repository.

## What this register is for, and what it fixes

`CLAUDE.md` queue item 41 records that arc identifiers had **no register
home**: arcs have been named since the commissioning records began, but never
numbered, and a repo-wide search for the `A-YYYY-MM-DD-NN` shape returned
nothing before this file. Namings lived inside the session record of record —
a handover or a commissioning record, under a "Rulings, verbatim" section —
which is per-artefact self-description rather than a register, so nothing
enumerated the series from outside it and **nothing allocated the next
number**.

This file allocates it. The next arc number is the highest `NN` for that date
plus one, read from this register; a new date restarts at `01`.

**Scope note: this closes the arc half of item 41 only.** The other half —
versioned code-series artefacts, the scenario spec schemas — is untouched and
remains owed under item 34 M7. Two artefact classes reached the same dead end;
one of them now has a home.

## Identifier grammar

`A-YYYY-MM-DD-NN` — the date the arc **opens**, plus a two-digit sequence
within that date. The date is the arc's own, not the session-label date used by
`docs/governance/SESSION_COSTS.md`, whose rows are labelled by session and run
a day ahead of the machine clock. Where the two differ, this register uses the
clock.

## Register

| Arc | Name | Lane | OPEN (UTC) | CLOSE (UTC) | PRs | Cost | Basis |
|---|---|---|---|---|---|---|---|
| A-2026-08-19-01 | Guard integrity close-out | governance | 2026-08-19T12:44:41Z | 2026-08-19T13:43:56Z | #142–#146 | $18.20 | **RECONSTRUCTED** — see notes |
| A-2026-08-19-02 | DEC-0018 fold-in and queue commissioning | governance | 2026-08-19T16:19:15Z | 2026-08-19T16:57:12Z | #147, #148 | *(pending)* | OPEN **RECONSTRUCTED**, CLOSE **ACTUAL** — see notes |
| A-2026-08-19-03 | Runner Rev C conformance | build | 2026-08-19T17:06:20Z | *(open)* | this PR | *(pending)* | OPEN **ACTUAL** — see notes |

### Notes on A-2026-08-19-01

**Both timestamps are RECONSTRUCTED, and the marking is not a formality.** The
arc was named *after* both of its acts had merged — the arc record says so
plainly — so no OPEN timestamp was recorded at the moment of opening and none
could be. What is written here is derived from git and GitHub, and a later
reader should treat it as evidence about the arc's extent rather than as a
record of a ceremony that happened.

- **OPEN** is the author date of the first commit on
  `governance/item-42-discharge-2026-08-19`, commit `94a213f`, read this
  session. It is not the PR-open time: PR #142 was created at 12:46:12Z, 91
  seconds later, and the branch is the earlier and better witness to when work
  began.
- **CLOSE** is the `mergedAt` of PR #146, read from GitHub this session.

**Corroboration, offered because a reconstruction should be checkable.** The
reconstructed span is **59m 15s**. `docs/governance/SESSION_COSTS.md` records
the session's wall time independently as **1h 6m 18s**, supplied by the
operator's own readout rather than derived. The two agree to within seven
minutes, which is the shape one expects when the wall clock starts before the
first commit. They are independent measurements and neither was fitted to the
other.

**The PR span and the cost row's PR count disagree, and both are right.** This
row records **#142–#146**. The cost register's 2026-08-19 row records **3 PRs
merged — #142, #143, #144**. The difference is not an error in either: the cost
figure is a `/cost` readout taken at the close stop, and #145 (the session
close, carrying the cost row itself) and #146 (a citation fix clearing a
divergence introduced at #145) merged *after* that readout. This is the same
shape the register's own 2026-08-13 note already documents, where the readout
reported ten merged with #117 pending. **The readout is preserved as what the
instrument said at a moment; this register records the arc's actual extent.**

**Cost is transcribed, not recomputed.** $18.20, basis DIRECT, from
`docs/governance/SESSION_COSTS.md`. That row is DIRECT on two sign checks
rather than one — the figure sits below the previous cumulative anchor, proving
a reset, and above the session's own interim readout, proving no second reset
mid-session. It is the first row in that register that is not a lower bound.

**One cost figure remains outstanding and is not this arc's.** The `/cost` for
the CC session that executed the round-trip test (PROMPTs 144/145) was owed at
that session's close and has not been supplied. It belongs to no arc: the
round-trip test ran post-close and outside any arc, which is part of why this
fold-in was owed.

**Register numbers consumed by this arc:** WS-E 75, and nothing else. DEC, ADR
and CL were all unchanged across the arc, at next 0018, next 0011 and next 31 —
the register economy the cost register's notes record repeatedly.

**DEC-0017 disposition: EXCEPTION RECORDED, not satisfied.** No build artefact
was merged or materially advanced. The narrow *directly-blocks* exception was
available and **was not claimed**. Full ruling at
`docs/governance/ARC_RECORD_2026-08-19_guard-integrity-close-out.md` section 3
and `CLAUDE.md` queue item 46.

### Notes on A-2026-08-19-02

**This row is written while the arc is OPEN**, which is a first for this
register and is the shape A5.1 intends: the identifier is assigned at open,
not at close, and the CLOSE cell stays empty until there is something true to
put in it. An empty CLOSE here means *not yet closed*, never *not recorded*.

**OPEN is RECONSTRUCTED, and it is the fold-in's start rather than the arc's
earliest act.** The value is the release time of `ARCA-P-0146` — the draft's
last-modified stamp, `2026-08-19T16:19:15Z`, which is when the chair's rename
to `[RELEASED]` landed. Per A4.2 the draft date is corroboration and the body
`TS:` line is the timestamp of record for *authoring*; for *release* the draft
date is the better witness, because the rename is what shifts it.

**The arc's own acts begin earlier, and the register says so rather than
smoothing it.** This arc covers the `ARCA-P-0144` round trip, which is
evidenced from `2026-08-19T15:44:42Z` (the 0144 draft) and
`2026-08-19T15:53:25Z` (the `ARCA-R-0144` reply). Both precede the recorded
OPEN by roughly half an hour. The OPEN value is recorded as specified rather
than adjusted to the earliest act, and the discrepancy is stated here so a
reader reconciling this row against the arc record finds the answer instead of
the puzzle.

**Named after its acts had begun — second consecutive instance.** A5.1 says
arc IDs are assigned at OPEN. Both rows in this register were in fact named
retrospectively: `A-2026-08-19-01` after both its PRs merged, and this one
after the round trip and after PR #147. **Two in two is worth flagging as a
practice gap rather than a coincidence** — the convention is sound and has not
yet been exercised as written.

**Cost is PENDING, and the pending-ness is itself the record.** The figure
will cover the combined round-trip and fold-in CC session and is supplied at
that session's close. The standing method applies: a counter reset is proven
by **sign check against the previous cumulative anchor**, never by recollection
of whether a terminal was restarted. The previous anchor is the 2026-08-19 row
at `docs/governance/SESSION_COSTS.md`, $18.20. Note that figure belongs to the
*coordinator* session and this arc's executor cost is separate and still owed —
the outstanding item the DEC-0018 ruling already named.

**DEC-0017 disposition: DISPLACEMENT RULED, not an exception.** The 2026-08-19
close bound the next session build-first with item 36 as spine; the chair's
Q-R3 amendment of the same evening displaced that binding **for this arc
only**. Ruling verbatim, and the binding it leaves in place, at
`docs/governance/ARC_RECORD_2026-08-19_dec-0018-fold-in-and-queue-commissioning.md`.
This is a different disposition from row 01's, which recorded an exception
against a rule left tight; here the earlier binding is displaced by a later
ruling, and the build-first obligation moves to the session after this one
rather than being waived.

**CLOSED 2026-08-19.** CLOSE is `2026-08-19T16:57:12Z`, the `mergedAt` of PR
#148 read from GitHub — **actual, not reconstructed**, unlike this row's OPEN.
The row therefore carries one measured endpoint and one derived one, and the
Basis column says so rather than averaging the two into a single claim. PRs
resolve to #147 and #148; the "and this PR" placeholder written while the arc
was open is now the merged number.

**Cost stays PENDING at close, deliberately.** The CC session spans arcs 02 and
03, so a single `/cost` readout cannot be attributed to either without a split
rule. The figure is supplied at CC-session close under the standing method —
sign check against the previous cumulative anchor, never restart recollection —
and **no figure is invented here**. A pending cost on a closed arc is a
recorded gap; a guessed one would be a false entry in a register whose whole
value is that its numbers were measured.

### Notes on A-2026-08-19-03

**OPEN is ACTUAL, and that is the point of this row.** `2026-08-19T17:06:20Z`
is the release time of `ARCA-P-0148`, read from the draft's own Gmail date at
fetch. **This breaks the two-in-two late-naming pattern** the row above flagged:
arcs 01 and 02 were both named after their acts had begun, contrary to A5.1's
"assigned at arc OPEN". This arc was named at open, by the chair, before any
work began — so A5.1 is now exercised as written rather than merely stated.

**Lane is BUILD, the first in this register.** Arcs 01 and 02 were both
governance. This one takes queue item 36, the runner's unhonoured Rev C
conformance elements, which is the spine DEC-0017 has been pointing at for two
consecutive sessions. The build-first binding carried at item 46 and again at
the arc-02 record is **discharged here** rather than carried a third time.

**CLOSE and cost are open at the time of writing**, as they should be for an
arc recorded at its open.

No control mapping line is carried, for the reason
`docs/governance/SESSION_COSTS.md` states: queue item 34 M11(d) requires
per-class mapping content to be defined once in the control framework, and that
framework does not exist yet.
