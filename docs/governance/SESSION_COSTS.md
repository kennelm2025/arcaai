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
