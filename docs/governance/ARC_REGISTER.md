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

No control mapping line is carried, for the reason
`docs/governance/SESSION_COSTS.md` states: queue item 34 M11(d) requires
per-class mapping content to be defined once in the control framework, and that
framework does not exist yet.
