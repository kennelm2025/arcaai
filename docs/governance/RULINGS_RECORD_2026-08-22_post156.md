# Rulings record — 22 August 2026, post-156 sheet

## Provenance

| Field | Value |
| --- | --- |
| Ruled by | Chair, 22 August 2026, mobile-mode |
| Subject | The twelve-item Decision Register of `docs/governance/QDF2_DESIGN_NOTE_2026-08-22.md` |
| Carried into the tree by | PROMPT 157 (QD-F2 Step 2, lane T2) |
| Transcribed block | 12 lines, 1163 bytes, SHA256 `55c0d7d75f534866b4449be4261b1de775430db11e6e4b394558769c710ab928` |
| Register numbers consumed | None — see the note on ruling 6 below |

**Footnote — PR series is not the PROMPT series.** PR numbers cited in this
record (#163, #164) are GitHub pull requests. PROMPT numbers (155, 156, 157) are
queue envelopes. The two series are independent and neither cites the other;
their occasional numerical coincidence is not a correspondence.

**Why this consumes no register number.** Ruling 6 operates as a Chair
*interpretation* of DEC-0019's existing deletes-nothing property, not as a new
decision, so it is recorded here rather than as a new DEC. DEC-0020 remains
reserved for the withholding lift, which is expressly **not** taken by these
rulings — see ruling 8.

---

## The twelve rulings, verbatim

Transcribed byte-faithfully from the PROMPT 157 envelope §2.1, which carried the
Chair's sheet. Reproduced inside a fence so no markup transformation touches the
text.

```
1. Adopt — relabel-on-refusal as the terminal state for mechanism (a).
2. Sidecar — refusal record as bytes + sidecar (preserves independent hashability).
3. Ratify `dead\`.
4. Archive (not high-water mark).
5. Ratify `done\`.
6. Ruled: a rename within the queue root is not a deletion, provided the item's content hash is preserved and its origin path is recorded. (Deletes-nothing = no bytes leave the queue root; everything remains hash-verifiable. Moves permitted; copy-plus-marker avoided.)
7. One implementation envelope, the two mechanisms evidenced separately.
8. Adopt — lift requires both QD-F2 and lazy-auth resolved.
9. Sequencing: QD-F2 first, then lazy-auth second (paired with the lift), then F1 as convention (already largely live), then pyproject opportunistic. (If the note's 4.3 options differ materially, flag on next read; otherwise this stands.)
10. Conditional adoption of the acceptance criteria at 5.1 — "adopted as drafted, subject to Chair read-back before the lift is ruled."
11. Defer retention (question remains on record); urgency removed by ruling 6.
12. Settled: ERROR page + log row + dead-letter record; no new channel.
```

---

## Open Chair items carried by these rulings

**Ruling 9's caveat and ruling 10's read-back both remain open Chair items:**
ruling 9 stands only if the design note's section 4.3 options do not differ
materially from the sequencing it states, and ruling 10 adopts the section 5.1
acceptance criteria subject to Chair read-back before the lift is ruled.
Neither is discharged by this record or by the implementation it accompanies.
