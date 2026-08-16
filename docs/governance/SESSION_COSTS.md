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
