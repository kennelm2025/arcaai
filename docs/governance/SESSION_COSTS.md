# SESSION COSTS — append-only register

One row per session. **Append-only**: rows are added, never edited or removed.
A correction is a new row citing the row it corrects, on the same discipline as
every other register in this repository.

## Source and its limits, stated before the numbers

**Source.** The operator's `/cost` readout at close, **operator-supplied at the
ceremony stop**. The executor does not generate these figures and cannot verify
them — it transcribes what the operator pastes. Each row records its source so a
reader knows which.

**The figures are approximate and machine-local**, by the tool's own caveat.
They are not billing records, they are not reconciled against an invoice, and
they should never be cited as though they were. Treat them as telemetry.

**A close without a cost row records `NOT SUPPLIED` explicitly.** The absence is
written, never silent — an empty cell and a cell nobody filled are different
facts, and only one of them is checkable.

## Purpose

Cost-per-arc telemetry. Two downstream consumers:

- **Item 34 M8**, gate evidence packs — cost per arc is part of what a gate pack
  should be able to state.
- **Consolidation ITEM 13**, the consolidation cost cap, whose discipline is
  *placeholder until measured*. This register is where the measuring starts, and
  the same discipline applies to it: a number here is an observation, not a
  bound.

## Register

| Date | Session | Total cost | API duration | Lines +/- | PRs merged | Register numbers consumed | Dominant model | Context note | Cost per merged PR | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-08-13 | A | $115.78 | 2h17m | +6624/-253 | 11 (10 merged at readout, #117 pending) | CL-27 | claude-opus-5 (184.0m cache read) | 93% of usage >150k context; subagent-heavy (corpus-lister fan-out) | ~$10.53/PR | operator `/cost` readout, pasted at close |
| 2026-08-15 | NOT SUPPLIED | $41.66 | 54m 57s | +4008/-223 | 3 — #127, #128, #129 (DERIVED) | CL-28 (DERIVED) | NOT SUPPLIED | NOT SUPPLIED | NOT SUPPLIED | cost figures: operator `/cost` readout carried in `docs/governance/SESSION_HANDOVER_2026-08-17.md` §10. PRs and registers: DERIVED, see notes |
| 2026-08-16 | NOT SUPPLIED | $33.00 | 49m 27s | +2791/-41 | 5 — #130, #131, #132, #133, #134 (DERIVED) | CL-29, CL-30 (DERIVED) | NOT SUPPLIED | NOT SUPPLIED | NOT SUPPLIED | cost figures: operator `/cost` readout carried in `docs/governance/SESSION_HANDOVER_2026-08-17.md` §10. PRs and registers: DERIVED, see notes |
| 2026-08-17 | NOT SUPPLIED | $88.05 | 1h 16m 41s | +4804/-56 | 5 — #135, #136, #137, #138, #139 (DERIVED) | WS-E 72, WS-E 73 (DERIVED) | claude-opus-5 | NOT SUPPLIED | ~$17.61/PR (DERIVED) | cost figures: DERIVED BY SUBTRACTION from the cumulative `/cost` readout carried at `docs/governance/SESSION_HANDOVER_2026-08-18.md` section 9 — method stated below. PRs and registers: DERIVED |
| 2026-08-18 | NOT SUPPLIED | $52.14 | 1h 3m 12s | +1204/-31 | 2 — #140, #141 (DERIVED) | WS-E 74 (DERIVED) | NOT SUPPLIED | NOT SUPPLIED | ~$26.07/PR (DERIVED) | cost figures: operator `/cost` readout, basis **DIRECT** — single-session, reset proven by sign check against the 2026-08-17 cumulative anchor; method below. PRs and registers: DERIVED |
| 2026-08-19 | A-2026-08-19-01 "Guard integrity close-out" | $18.20 | 27m 50s | +1432/-15 | 3 — #142, #143, #144 (DERIVED) | WS-E 75 (DERIVED) | claude-opus-5 | wall 1h 6m 18s | ~$6.07/PR (DERIVED) | cost figures: operator `/cost` readout at the close stop, basis **DIRECT** — two sign checks, method below. PRs and registers: DERIVED |

### Notes on the 2026-08-13 row

**The PR count is the readout's, not the day's final.** The readout was taken
with ten merged and #117 pending; **#117 merged at 16:50:44Z**, after the
readout was given. The row preserves what the readout said rather than
correcting it, because the row's value is as a record of what the instrument
reported at a moment. The day's actual total was eleven merged, #107 through
#117. The computed cost per merged PR uses 11 and is therefore consistent with
the final count rather than the readout's parenthetical.

**Register economy is the striking figure**, and is worth recording alongside
the cost: eleven merged pull requests consumed **one** register number, CL-27.
Ten of the eleven were governance, harness or queue work that deliberately took
no number.

**The context note is the day's cost driver**, and is actionable rather than
descriptive: 93% of usage ran above 150k context. See the telemetry notes under
`CLAUDE.md` queue item 34 M8.

### Notes on the 2026-08-15 and 2026-08-16 rows

Both rows land 2026-08-17 under an operator ruling of that date, transcribed from
the `/cost` readouts carried at §10 of
`docs/governance/SESSION_HANDOVER_2026-08-17.md` rather than pasted live at a
close — the two closes they describe did not reach their cost stop.

**(i) Wall time, which this table has no column for.** 2026-08-15: **18h 7m**,
which spans an overnight gap and is not contiguous working time. 2026-08-16:
**4h 4m**. Recorded here rather than in a new column, because adding a column
would reshape the 2026-08-13 row, whose wall time is unknown — and reshaping an
existing row in an append-only register is what the register forbids. The API
durations in the table, 54m 57s and 49m 27s, are the meaningful load figures;
wall time is context.

**(ii) Two columns are DERIVED, and are not from the `/cost` readout.** The
readout supplies cost, API duration and lines changed, and nothing else. **PRs
merged** is derived from git merge history and confirmed against GitHub's own
`mergedAt`; **register numbers consumed** is derived from
`docs/governance/GOVERNANCE_REVIEW_CHANGELOG.md`. Both are marked DERIVED in the
cells so no reader takes them for readout figures. Basis: 2026-08-15 — PRs #127,
#128, #129, with CL-28 raised at #127; 2026-08-16 — PRs #130 through #134, with
CL-29 claimed at #131 and CL-30 at #134, #134 also re-pinning CL-29.

**The date basis of that derivation needs stating, because git disagrees with the
row labels.** By wall-clock, **all eight** of those PRs merged on **2026-08-15**,
between 09:47Z and 14:48Z; **no PR merged on 2026-08-16 at all**. The rows are
labelled by *session* rather than by machine date, and the governance dating used
across these artefacts runs a day ahead of the machine clock. The split between
the two sessions is not an interpretation: there is a **2h 31m gap** between #129
at 10:42Z and #130 at 13:13Z, and the two `/cost` readouts are separately
reported, so the boundary is evidenced from both sides. A reader reconciling this
register against `git log` by calendar date will find eight PRs on one day and
none on the next, and should read these rows as per-session.

**(iii) Four columns are NOT SUPPLIED**, written explicitly per this file's own
discipline rather than left blank: **Session**, **Dominant model**, **Context
note**, and **Cost per merged PR**. None was in the readouts as carried, and the
2026-08-17 ruling directed that unsupplied fields be written as such rather than
derived or estimated. An empty cell and a cell nobody could fill are different
facts, and only one of them is checkable.

### Notes on the 2026-08-17 row

**This row is DERIVED BY SUBTRACTION, and that is the one derivation this
register permits.** Everywhere else a figure is either read from a `/cost`
readout or written NOT SUPPLIED. The exception is granted here because the
subtraction is exact and checkable rather than estimated, and because the
alternative is to lose a session's telemetry entirely.

**Why a subtraction is needed at all.** The executor terminal was **not
restarted** after the 2026-08-16 session, so the readout taken at the 2026-08-17
close is cumulative over both sessions rather than a single-session figure.

**The cumulative readout, transcribed:** $121.05 · API 2h 6m 8s · wall
22h 24m 5s · 7,595 added / 97 removed · dominant model `claude-opus-5`, with
haiku negligible at $0.0011.

**The subtrahend is the already-transcribed 2026-08-16 row** — $33.00 ·
49m 27s · +2,791/−41 — which sits three rows above and was itself transcribed
rather than derived.

**All four fields subtract clean, and this was computed at authoring rather
than carried over from the source narrative:**

| Field | Cumulative | Less 2026-08-16 | Row |
|---|---|---|---|
| Total cost | $121.05 | $33.00 | **$88.05** |
| API duration | 7,568 s | 2,967 s | **4,601 s = 1h 16m 41s** |
| Lines added | 7,595 | 2,791 | **4,804** |
| Lines removed | 97 | 41 | **56** |

**A consistency check the source offers and this row keeps.** The counter cannot
also include the 2026-08-15 session: removals for 2026-08-15 and 2026-08-16
together are 264, which exceeds the cumulative 97, so the subtraction would go
negative. The counter therefore spans exactly the two sessions claimed.

**Wall time is NOT SEPARABLE and is not stated as a per-session figure.** The
counter's wall clock spans an overnight idle, so no defensible split exists. The
raw cumulative **22h 24m 5s** is recorded here in the notes with its derivation
stated, per the precedent set by the 2026-08-15 row — which this table also has
no column for.

**Dominant model is READ, not derived**, and fills a column written NOT SUPPLIED
on the two rows above it.

**Three columns remain NOT SUPPLIED** — Session, Context note, and, for
2026-08-17, no context telemetry was in the readout as carried. **Cost per
merged PR is marked DERIVED** rather than NOT SUPPLIED because it is arithmetic
over two cells of this same row, not an outside figure.

**Register numbers consumed are WS-E 72 and WS-E 73, and no CL number.** The
manifest regenerated at the 2026-08-18 boot reads CL highest 30, next 31 —
unchanged from the 2026-08-16 close at CL-30 — so the 2026-08-17 session
consumed no CL number across five merged pull requests. Same register economy
the 2026-08-13 note records.

**Date basis.** This row is labelled by *session*, on the same footing as the two
rows above and for the same reason. The label-versus-clock offset is **not a
fixed skew** and should not be reconciled by subtracting a constant; the evidence
is recorded at
`docs/governance/FOLD_IN_2026-08-18_prompts-125-126-and-guard-install.md`
section 3(b).

### Notes on the 2026-08-18 row

**This row is DIRECT, and the point of the note is how that was established
rather than asserted.** The 2026-08-17 row above is derived by subtraction
because its readout was cumulative across two sessions. The obvious move for
this row was to subtract again — and `docs/governance/SESSION_HANDOVER_2026-08-19.md`
section 9 says exactly that, directing a subtraction from the 2026-08-17 row if
the readout arrived later and the terminal had not been restarted. **That route
is wrong here, and the register's own instrument is what shows it.**

**The sign check.** The 2026-08-17 close readout was **$121.05 cumulative**. A
cumulative counter cannot read lower than it previously read. This session's
readout is **$52.14**, which is lower — by $68.91. The counter therefore
**reset** between the two readouts, and the figure is already a single-session
one. Had the subtraction of section 9 been performed as directed it would have
returned **negative** ($52.14 − $88.05 = −$35.91), which is not a cost.

**This is the same instrument the 2026-08-17 notes use, reaching the opposite
conclusion**, and that is why it is trustworthy rather than convenient: that row
argues the counter *cannot* also span 2026-08-15 because the subtraction would
go negative. The identical test applied here says the counter *cannot* span
2026-08-17. One method, two sessions, two answers, both falsifiable.

**The reset boundary is the CC session, not the terminal — and this half rests
on operator report, not on the sign check.** The operator reports the terminal
was **not restarted**. The sign check establishes *that* a reset occurred; it
cannot by itself establish *where*. Combining the two locates the boundary at
the CC session. Stated separately because the two legs have different evidential
weight, and a reader should be able to reject one without losing the other.

**The residual limit, stated because it is real.** If a reset had occurred
*partway through* the 2026-08-18 session, $52.14 would undercount it and the
sign check would look identical. Nothing available distinguishes those cases.
The figure is therefore a **lower bound that is probably exact**, and it is
recorded as DIRECT rather than EXACT for that reason.

**Method note, adopted from this row forward: a reset is proven by sign check
against the previous cumulative anchor, never by recollection of whether a
restart happened.** Restart recollection is precisely the input that produced
the wrong route in section 9 — it was correct as far as it went (the terminal
genuinely was not restarted) and still directed a subtraction that would have
gone negative, because a terminal restart is not the only thing that resets the
counter. The arithmetic is checkable; the recollection is not.

**Two columns are DERIVED**, on the same footing as the rows above. **PRs
merged**: #140 (`governance/fold-in-2026-08-18`, merged 14:11:40Z) and #141
(`governance/session-handover-2026-08-19`, merged 14:52:48Z). The boundary
against the 2026-08-17 session is evidenced from both sides: #139 merged at
09:12:32Z, leaving a **4h 59m gap** before #140, and the two sessions report
separate readouts. **Register numbers consumed**: WS-E 74, raised that session;
CL was unchanged at highest 30, so five merged PRs across two sessions consumed
no CL number — the register economy the 2026-08-13 and 2026-08-17 notes both
record.

**Dominant model is NOT SUPPLIED**, written explicitly rather than carried over
from the row above. The 2026-08-17 row reads `claude-opus-5`; assuming the same
here would be deriving a cell from an adjacent row, which this register does not
do.

**Date basis.** Labelled by *session*, as every row above it. Both PRs merged on
clock day **2026-08-16**. Per
`docs/governance/FOLD_IN_2026-08-18_prompts-125-126-and-guard-install.md`
section 3(b) the label-versus-clock offset is **not a fixed skew** and must not
be reconciled by subtracting a constant.

**Correction of record.** This row corrects
`docs/governance/SESSION_HANDOVER_2026-08-19.md` section 9, which recorded the
cost as NOT SUPPLIED and proposed the subtraction route. The handover is
hash-pinned and stays byte-frozen; the correction is at
`docs/governance/CORRECTIONS_cost-basis_2026-08-19.md`.

### Notes on the 2026-08-19 row

**First row with TWO sign checks, and the pair is what makes it DIRECT rather
than merely asserted.** The corrective adopted at the row above says a reset is
proven by sign check against the previous cumulative anchor, never by
recollection of a restart. This row exercises it twice, in opposite directions.

**Check 1 — a reset occurred.** $18.20 is **below** the 2026-08-18 anchor of
$52.14. A cumulative counter cannot read lower than it previously read, so the
counter reset between the two readouts and the figure is single-session
already. Subtraction is not merely unnecessary here; it would return
**−$33.94**, which is not a cost.

**Check 2 — it is the SAME counter, not a second reset mid-session.** $18.20 is
**above** this session's own interim readout of **$6.69**. That closes the
residual limit the 2026-08-18 note had to leave open, where a mid-session reset
would have been indistinguishable and the figure was recorded as *"a lower
bound that is probably exact"*. **Here it is not a lower bound.** A reset after
the interim readout would have put the close figure below $6.69; it is above,
so the counter ran continuously across the whole session. **Two readouts
bracketing one session are strictly better evidence than one at its end**, and
taking an interim readout is cheap — a practice worth keeping.

**Reset boundary is the CC session, second consecutive observation.** The
2026-08-18 row located the boundary at the CC session rather than the terminal
by combining a sign check with operator report. This session repeats it.
**Two observations are a pattern, not yet a rule** — recorded as such, and the
boundary is still read from evidence each time rather than assumed.

**Session column is FILLED for the first time in this register**, carrying the
arc identifier `A-2026-08-19-01`. Every row above reads NOT SUPPLIED because no
arc identifier existed to put in it. Note the identifier's own status: it has
no register home, which is queue item 41 as widened 2026-08-19.

**Wall time is IN THE CONTEXT COLUMN, not a new column.** 1h 6m 18s, supplied
directly rather than derived. It sits in the context note for the reason the
2026-08-15 row gives: adding a column would reshape rows above whose wall time
is unknown, and reshaping an existing row is what an append-only register
forbids. API duration 27m 50s is the load figure; wall time is context.

**Two columns are DERIVED.** **PRs merged**: #142 (`f236e6f`), #143
(`dc06118`), #144 (`3cfaea5`), all three verified post-merge from `main`.
**Register numbers consumed**: WS-E 75 and nothing else — three merged PRs
against one register number, the same economy the 2026-08-13 and 2026-08-17
notes record. DEC, ADR and CL were all unchanged, at next 0018, 0011 and 31.

**Cost per merged PR is the lowest this register has recorded** — ~$6.07
against ~$10.53, ~$17.61 and ~$26.07 above it. Recorded as an observation and
**not** as a trend or a target: three of the five rows compute it from a
DERIVED PR count, the arcs differ in kind, and item 34's consolidation cost-cap
discipline is *placeholder until measured*. A number here is an observation,
never a bound.

## A convention this register cannot yet follow

Queue item 34 **M11** requires new governed artefacts in named classes to carry
a `Control mapping:` line, and makes the convention prospective from its merge
at PR #117 — which is before this file. M11(d) also requires that per-class
mapping content be **defined once in the control framework**, so authors copy
rather than compose.

**That framework does not exist yet.** This register therefore carries no
mapping line: composing one here is exactly what M11(d) forbids, and inventing a
mapping to satisfy a format check would be the overclaiming M11(a) exists to
prevent. The line is added at this file's next legitimate touch once the control
framework defines the content — which is M11(c)'s selective-retrofit path,
working as intended on its first real case.
