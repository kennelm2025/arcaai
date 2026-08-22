# PROMPT series reconciliation — 22 August 2026

**What this file is.** The reconciliation directed by the post-sitting same-day
addendum of 22 August 2026, recording a fork in the PROMPT numbering series, the
rule by which forked references resolve, the consumed set as grepped, the point
of resumption, and the live evidence the reconciliation rests on.

**Authority.** Chair ruling of 22 August 2026. Ruling and reasons:
`docs/governance/RULINGS_RECORD_2026-08-22_sitting.md`, post-sitting same-day
addendum. **Transcribed under PROMPT 154**, lane T1. No register numbers
consumed.

**Standing flexibility principle applies** per envelope §0 as incorporated into
the sitting record: binding for current direction, not irreversible
architecture.

---

## 1. The fork

The PROMPT series **forked between the 19 August session family and the
21 August session family**. Numbers in the range **132–153 were attested on both
sides**. Two different prompts therefore bear the same number in several cases,
and neither attestation is an error in its own frame.

**How the fork was discovered.** On 22 August 2026 the staged transcription
envelope — staged as PROMPT 141 — was **refused at release**. The refusal rested
on two valid grounds: main-worktree rooting, and a D3 target-quote mismatch. In
the course of that refusal the numbering collision surfaced: the committed
record already attests **141–143 consumed on 19 August**, at
`docs/governance/ARC_RECORD_2026-08-19_guard-integrity-close-out.md` lines 3,
56, 104, 129 and 154.

**Corroborated live, not accepted from the envelope.** Those five line
references were re-read in the lane worktree at transcription time and resolve
as: line 3 PROMPT 142, line 56 PROMPT 142, line 104 PROMPT 143, line 129
PROMPT 141, line 154 PROMPT 141. The citation is accurate.

**The refusal was itself the control working.** The fork was not found by an
audit of the register; it was found because a release was refused on unrelated
grounds and the refusal forced a re-read. That is worth recording, because
nothing in the numbering machinery would have surfaced it otherwise — the same
shape as the queue-staleness pattern the boot readback exists to catch.

## 2. Disambiguation rule (ruled 22 August 2026)

> Every PROMPT reference in the range **132–153** resolves by the **date and PR
> context of the document citing it**. All attestations on both sides **stand as
> written** — recorded rather than renumbered.

This extends the precedent already set at
`docs/governance/ARC_RECORD_2026-08-19_guard-integrity-close-out.md` line 154,
which recorded rather than renumbered in a comparable case.

**Why recorded rather than renumbered.** Renumbering would require rewriting
committed governance artefacts to make a numbering scheme tidy, which is a
history rewrite in substance if not in mechanism, and it would invalidate every
external citation of the affected documents. Recording costs one lookup at read
time and leaves the trail intact.

**Practical consequence for a reader.** A bare "PROMPT 137" is ambiguous in the
same way a bare "A4" is ambiguous — see the label-collision note in `CLAUDE.md`.
Cite the date or the PR alongside the number whenever the number falls in
132–153.

## 3. Consumed set

**As grepped on 22 August 2026 from the whole tree**, pattern `PROMPT (1[0-9][0-9])`:

**100, 115, 116, 123, 124, 127–144, 146, 147, 149, 150, 152, 153.**

**Gaps preserved as gaps, forward-only, no backfill:** 101–114, 117–122,
125–126, 145, 148, 151.

**Verification note.** The set above was re-derived live in the lane worktree at
transcription time and matched the ruled set exactly, element for element, with
no additions and no omissions. After this envelope's own artefacts landed in the
working tree the same grep additionally returns **154**, which is this envelope
and is expected; no other value changed. Both readings are recorded because a
set stated without saying when it was taken is the kind of claim that goes stale
silently.

## 4. Resumption

The series **resumes single-threaded at PROMPT 154** — the envelope transcribed
by this act.

The staged QD-F2 pair renumber to **155 (Step 0)** and **156 (Step 1)**.

## 5. Evidence appendix

### 5.1 Method

Run live in the lane worktree `arcaai-t1` on `lane/t1-spine`, read-only, at
transcription time. Two greps, both stated so the result is reproducible rather
than asserted:

- **Primary** — every file and line number attesting a PROMPT number in the
  range 132–153:
  `grep -rnoE "PROMPTs? ?(13[2-9]|14[0-9]|15[0-3])" . --exclude-dir=.git --exclude-dir=.ruff_cache | sort`
- **Supplementary** — range and pair forms, where an in-range number appears as
  the second element and the primary pattern's leading token does not sit
  immediately before it:
  `grep -rnoE "PROMPTs? ?1[0-9][0-9][^0-9]{1,6}1[0-9][0-9]" . --exclude-dir=.git --exclude-dir=.ruff_cache | sort`

**Scope stated precisely, because a partial appendix that reads as complete is
worse than none.** The output below was taken **after** the four preceding
artefacts of this envelope were written (the sitting record, the lapse note, the
`CLAUDE.md` amendment and the dossier correction) and **before this file
existed**. It therefore reflects the tree as committed **except for this file**,
whose own in-range references are excluded by construction. Those references are
citations of the fork, not attestations of consumption. A later re-run will
return more lines than appear here, and that is expected rather than a
discrepancy.

**Line numbers moved during this envelope.** The `CLAUDE.md` amendment is a net
+34 lines above the queue block, so `CLAUDE.md` line numbers in this appendix
are **post-amendment** and are 34 higher than the same references would have
been at 24ef117.

### 5.2 Primary output, verbatim (81 lines)

```
CLAUDE.md:1650:PROMPT 133
CLAUDE.md:1681:PROMPT 141
CLAUDE.md:1760:PROMPT 133
CLAUDE.md:1899:PROMPT 153
CLAUDE.md:36:PROMPT 136
CLAUDE.md:648:PROMPT 141
DECISIONS.md:75:PROMPT 144
docs/governance/ARCA-R-0152_2026-08-19.md:396:PROMPT 132
docs/governance/ARCA-R-0152_2026-08-19.md:405:PROMPT 152
docs/governance/ARCA-R-0152_2026-08-19.md:405:PROMPT 153
docs/governance/ARCA-R-0152_2026-08-19.md:410:PROMPT 152
docs/governance/ARCA-R-0152_2026-08-19.md:411:PROMPT 153
docs/governance/ARCA-R-0152_2026-08-19.md:49:PROMPT 152
docs/governance/ARCA-R-0152_2026-08-19.md:6:PROMPT 132
docs/governance/ARCA-R-0153_2026-08-19.md:171:PROMPT 149
docs/governance/ARCA-R-0153_2026-08-19.md:225:PROMPT 150
docs/governance/ARCA-R-0153_2026-08-19.md:264:PROMPT 153
docs/governance/ARCA-R-0153_2026-08-19.md:299:PROMPT 132
docs/governance/ARCA-R-0153_2026-08-19.md:307:PROMPT 152
docs/governance/ARCA-R-0153_2026-08-19.md:307:PROMPT 153
docs/governance/ARCA-R-0153_2026-08-19.md:312:PROMPT 152
docs/governance/ARCA-R-0153_2026-08-19.md:313:PROMPT 153
docs/governance/ARCA-R-0153_2026-08-19.md:55:PROMPT 153
docs/governance/ARCA-R-0153_2026-08-19.md:6:PROMPT 132
docs/governance/ARC_RECORD_2026-08-19_dec-0018-fold-in-and-queue-commissioning.md:30:PROMPT 147
docs/governance/ARC_RECORD_2026-08-19_dec-0018-fold-in-and-queue-commissioning.md:3:PROMPT 147
docs/governance/ARC_RECORD_2026-08-19_guard-integrity-close-out.md:104:PROMPT 143
docs/governance/ARC_RECORD_2026-08-19_guard-integrity-close-out.md:109:PROMPT 133
docs/governance/ARC_RECORD_2026-08-19_guard-integrity-close-out.md:129:PROMPT 141
docs/governance/ARC_RECORD_2026-08-19_guard-integrity-close-out.md:151:PROMPT 138
docs/governance/ARC_RECORD_2026-08-19_guard-integrity-close-out.md:154:PROMPT 141
docs/governance/ARC_RECORD_2026-08-19_guard-integrity-close-out.md:37:PROMPT 134
docs/governance/ARC_RECORD_2026-08-19_guard-integrity-close-out.md:3:PROMPT 142
docs/governance/ARC_RECORD_2026-08-19_guard-integrity-close-out.md:56:PROMPT 142
docs/governance/ARC_RECORD_2026-08-19_guard-integrity-close-out.md:61:PROMPT 133
docs/governance/ARC_RECORD_2026-08-19_guard-integrity-close-out.md:83:PROMPT 133
docs/governance/ARC_REGISTER.md:83:PROMPTs 144
docs/governance/CORRECTIONS_cost-basis_2026-08-19.md:17:PROMPT 134
docs/governance/CORRECTIONS_cost-basis_2026-08-19.md:5:PROMPT 135
docs/governance/DEC-0018_A6_CORRECTION_2026-08-19.md:28:PROMPT 144
docs/governance/DEC-0018_RIDER_R2_2026-08-19.md:72:PROMPT 144
docs/governance/F5_DESIGN_BRIEF_2026-08-21.md:16:PROMPT 139
docs/governance/F5_DESIGN_BRIEF_2026-08-21.md:420:PROMPT 141
docs/governance/F5_DESIGN_BRIEF_2026-08-21.md:629:PROMPT 139
docs/governance/FOLD_IN_2026-08-18_ADDENDUM_history-rewrite-baseline_2026-08-19.md:3:PROMPT 135
docs/governance/GOVERNANCE_REVIEW_CHANGELOG.md:384:PROMPT 136
docs/governance/GOVERNANCE_REVIEW_CHANGELOG.md:394:PROMPT 136
docs/governance/QUEUE_CYCLE_2026-08-19.md:148:PROMPT 143
docs/governance/QUEUE_CYCLE_2026-08-19.md:51:PROMPT 144
docs/governance/QUEUE_CYCLE_2026-08-19.md:5:PROMPT 146
docs/governance/QUEUE_CYCLE_2026-08-21.md:108:PROMPT 152
docs/governance/QUEUE_CYCLE_2026-08-21.md:108:PROMPT 153
docs/governance/QUEUE_CYCLE_2026-08-21.md:113:PROMPT 152
docs/governance/QUEUE_CYCLE_2026-08-21.md:114:PROMPT 153
docs/governance/QUEUE_CYCLE_2026-08-21.md:118:PROMPT 152
docs/governance/QUEUE_CYCLE_2026-08-21.md:124:PROMPT 153
docs/governance/QUEUE_CYCLE_2026-08-21.md:179:PROMPT 132
docs/governance/QUEUE_CYCLE_2026-08-21.md:181:PROMPTs 152
docs/governance/QUEUE_CYCLE_2026-08-21.md:189:PROMPT 132
docs/governance/QUEUE_CYCLE_2026-08-21.md:5:PROMPT 132
docs/governance/RB_RULING_DOSSIER_2026-08-21.md:36:PROMPT 132
docs/governance/RB_RULING_DOSSIER_2026-08-21.md:5:PROMPT 140
docs/governance/RB_RULING_DOSSIER_2026-08-21.md:91:PROMPT 137
docs/governance/RULINGS_RECORD_2026-08-22_sitting.md:31:PROMPT 137
docs/governance/RULINGS_RECORD_2026-08-22_sitting.md:31:PROMPT 139
docs/governance/RULINGS_RECORD_2026-08-22_sitting.md:52:PROMPT 141
docs/governance/SESSION_HANDOVER_2026-08-19.md:147:PROMPT 133
docs/governance/SESSION_HANDOVER_2026-08-19b.md:131:PROMPT 143
docs/governance/SESSION_HANDOVER_2026-08-19b.md:134:PROMPT 133
docs/governance/SESSION_HANDOVER_2026-08-19b.md:146:PROMPT 143
docs/governance/SESSION_HANDOVER_2026-08-19b.md:156:PROMPT 143
docs/governance/SESSION_HANDOVER_2026-08-19b.md:177:PROMPT 143
docs/governance/SESSION_HANDOVER_2026-08-19b.md:235:PROMPT 138
docs/governance/SESSION_HANDOVER_2026-08-19b.md:238:PROMPT 141
docs/governance/SESSION_HANDOVER_2026-08-19b.md:26:PROMPT 142
docs/governance/WS-E_INCIDENTS.md:1131:PROMPT 141
docs/governance/WS-E_INCIDENTS.md:1251:PROMPT 141
docs/governance/WS-E_INCIDENTS.md:1371:PROMPT 150
docs/governance/WS-E_INCIDENTS.md:1469:PROMPT 132
docs/governance/WS-E_INCIDENTS.md:1500:PROMPT 132
docs/governance/WS-E_INCIDENTS.md:1501:PROMPT 132
```

Three of those lines are this envelope's own sitting record, at
RULINGS\_RECORD\_2026-08-22\_sitting.md lines 31 and 52. They are in-range
references carried inside the verbatim §3 text (PROMPT 137, PROMPT 139 and the
staged-as-141 reference) and are attestations of the fork's subject matter, not
new consumptions.

### 5.3 Supplementary output, verbatim (range and pair forms)

```
CLAUDE.md:1654:PROMPTs 130–132
DECISIONS.md:75:PROMPT 144/145
docs/governance/ARC_REGISTER.md:83:PROMPTs 144/145
docs/governance/DEC-0018_A6_CORRECTION_2026-08-19.md:28:PROMPT 144/145
docs/governance/DEC-0018_RIDER_R2_2026-08-19.md:72:PROMPT 144/145
docs/governance/QUEUE_CYCLE_2026-08-21.md:180:PROMPTs 127R, 127
docs/governance/QUEUE_CYCLE_2026-08-21.md:181:PROMPTs 152 and 153
scripts/queue_driver.py:4:PROMPT 129/129
tests/harness/test_queue_driver.py:1:PROMPT 129/129
```

The supplementary grep surfaces exactly **one** in-range attestation the primary
grep does not reach: `CLAUDE.md` line 1654, the form "PROMPTs 130–132", where
132 is in range but sits as the second element of an en-dash range. The
remaining rows are either already in the primary output (the 144/145 pairs) or
out of range (127, 129).

### 5.4 Disposition — `CLAUDE.md` line 1616, surfaced by the 22 August filename-level grep

**Where it is now.** Post-amendment the line is **1650** (the +34 shift noted at
5.1). At 24ef117 it was 1616.

**What it references.** It is the opening of **queue item 42**, the guard repair
for WS-E 72 and 73: *"DISCHARGED 2026-08-19. CLOSED. Ruled at PROMPT 133
(2026-08-18 session clock)"*. The reference is to **PROMPT 133**, which falls in
the 132–153 fork range.

**Does it need the disambiguation touch? Assessed: NO.** The citation already
satisfies the §2 rule on its face. It carries an explicit date qualifier in the
same clause — "(2026-08-18 session clock)" — and it sits inside a queue item
dated 2026-08-19 whose PR context is stated in the surrounding text (#142 to
#144). Date and PR context are both present, so the reference resolves to the
19 August family without amendment.

**Same disposition for its neighbour.** Line **1654** ("PROMPTs 130–132") sits
in the same 2026-08-19 discharge block and inherits the same date and PR
context. Only 132 is in range, and it resolves identically. No touch needed.

**If the Chair assesses otherwise, the touch is OWED, not performed.** It is
outside this envelope's D3 grant, which is scoped to the lines 106–117 passage
only. This section states an assessment; it does not perform an amendment, and
nothing at 1650 or 1654 was edited.

### 5.5 Method defect recorded — a false-negative in the first supplementary grep

Recorded because the check-method family (queue item 8) turns on exactly this
shape, and a defect found while building an evidence appendix belongs in the
appendix rather than in a memory.

The first attempt at the supplementary grep used a bracket expression to match
either dash form. The en-dash is **multibyte UTF-8** (bytes E2 80 93), and a
bracket-expression range containing it is not valid in the C locale, so the
pattern **matched nothing at all and returned clean**. Had it been trusted, the
appendix would have omitted `CLAUDE.md` line 1654 while appearing complete.

**Shape:** a check whose empty result is indistinguishable from its not having
run — the same failure mode as `grep -c … || true` recorded in the house
conventions. It was caught only because the missing row was already known from
reading the file, which is luck rather than method. **Corrective applied here:**
the supplementary pattern avoids bracket expressions over multibyte characters
entirely, matching any one-to-six non-digit bytes between the two numbers
instead. No claim is made that this generalises; it is stated so the next author
of a dash-matching grep in this tree does not rediscover it.

## Related

- `docs/governance/RULINGS_RECORD_2026-08-22_sitting.md` — the sitting record
  and its post-sitting same-day addendum, the ruling this file transcribes.
- `docs/governance/ARC_RECORD_2026-08-19_guard-integrity-close-out.md` — the
  committed attestation of 141–143 on 19 August, and the recorded-rather-than-
  renumbered precedent at its line 154.
- `docs/governance/ARC_REGISTER.md` — the arc register, whose allocation rule is
  the nearest existing analogue to the numbering question this file answers.
- `CLAUDE.md` queue item 41 — no live register home for code-series artefacts.
  The PROMPT series is a third artefact class reaching the same dead end, and
  this file is per-artefact self-description rather than a register.

No control mapping line is carried, for the reason
`docs/governance/QUEUE_CYCLE_2026-08-19.md` states: queue item 34 M11(d)
requires per-class mapping content to be defined once in the control framework,
and that framework does not exist yet.
