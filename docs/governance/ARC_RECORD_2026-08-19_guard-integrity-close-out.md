# ARC RECORD 2026-08-19 — A-2026-08-19-01, "Guard integrity close-out"

Governance lane. Authored under PROMPT 142 on branch
`governance/ws-e-74-discharge-2026-08-19`.

**This is an arc record, not a session close.** `/session-close` has not run,
the queue pointer has not been rewritten by ceremony, and no cost row for this
session exists. Those remain owed.

## 0. Two conventions read rather than assumed, and where they landed

**(a) Where arc namings live.** Read from prior instances, not from
recollection: `docs/governance/COMMISSIONING_SESSION_RECORD_2026-08-16_d22a-runner-spike-2.md`
section 2 and `docs/governance/COMMISSIONING_SESSION_RECORD_2026-08-13_d22a-runner-spike.md`
section 2 both carry the naming as **"Ruling 1 — arc naming"** inside a
**"Rulings, verbatim"** section of the session record of record, quoted
verbatim in a blockquote, and stating that it discharges the `/session-open`
arc-selection task and the DEC-0017 arc-selection step.
`.claude/skills/session-close/SKILL.md` step 3 places the arc summary in the
handover. **Arc namings therefore live in the session record of record** —
`SESSION_HANDOVER_*.md` for an ordinary session, `COMMISSIONING_SESSION_RECORD_*.md`
for a commissioning arc. Section 2 below follows that shape.

**(b) The identifier `A-2026-08-19-01` has no precedent in this repository.**
A repo-wide search for the `A-YYYY-MM-DD-NN` shape returns nothing, and no arc
register exists — arcs have been named, but never numbered. The identifier is
recorded here **as supplied, and as a first use**, not as continuation of a
series. Two consequences a later reader should not have to derive: there is no
`A-2026-08-19-00` or earlier sibling that has gone missing, and nothing yet
allocates the next one. **Whether the scheme becomes a register is a decision
nobody has taken**; if it does, it wants a home, and queue item 41 already
records that versioned code-series artefacts have nowhere to be registered —
the same gap, arriving from a different direction.

**Why this file rather than a handover.** The `SESSION_HANDOVER_2026-08-19.md`
slot is occupied by the **predecessor's** handover, written for this session,
hash-pinned and verified byte-frozen at PROMPT 134. Writing into it would break
its pin. A same-day suffixed handover would assert a close that has not
happened. So the arc record stands as its own artefact and carries the
convention internally.

## 1. Arc

**A-2026-08-19-01 — "Guard integrity close-out". Governance lane.**

Covers two acts:

| Act | Vehicle |
|---|---|
| Item 42 discharge write, WS-E 75 raised, history-rewrite string baselined, cost row and correction | **PR #142**, merged `f236e6f` |
| F3/F4 fix install record, and the WS-E 74 discharge | **PR #143** merged `dc06118`, and this PR |

## 2. Rulings, verbatim

**Ruling 1 — arc naming (coordinator, under explicit chair delegation,
2026-08-19, PROMPT 142).** Discharges the `/session-open` arc-selection task
and the DEC-0017 arc-selection step.

> "A-2026-08-19-01 — 'Guard integrity close-out', governance lane. Covers: item
> 42 discharge write (PR #142), F3/F4 fix + WS-E 74 discharge (PRs #143, this
> PR). DEC-0017 note: first act pre-ruled PROMPT 133, lawfully pre-empting
> build-first arc selection; second act completes the same integrity family
> (WS-E 72/73/74). Arc named by coordinator under explicit chair delegation,
> 2026-08-19. D2.2a pre-flight not run — arc touches no retrieval."

**The delegation is recorded because the default is the opposite.**
`.claude/skills/session-open/SKILL.md` makes arc naming operator-only and never
delegable, and `docs/governance/SESSION_HANDOVER_2026-08-19.md` section 6
confirms it. This naming was made **coordinator-side under explicit chair
delegation given in the prompt**, which is a different thing from an executor
inferring an arc from the queue — the failure that rule exists to prevent. The
distinction is the whole reason this paragraph is here: a delegated ruling is
still a ruling, and it is traceable to the chair act that delegated it.

**Arc named after the acts, not before.** Both PRs merged before the naming was
issued. Recorded plainly rather than presented as though the sequence ran the
other way. The first act carried its own pre-ruling (below); the second did
not, and this record is where that is visible.

## 3. DEC-0017 disposition

**First act — lawfully pre-empting build-first selection.** The item 42
discharge write was **pre-ruled at PROMPT 133** (2026-08-18 session clock),
before this session opened. It was ruled work carried forward, not an arc
chosen this session in preference to the build lane, so DEC-0017's
arc-selection step was not the gate it had to pass.

**Second act — same integrity family.** The F3/F4 fix and the WS-E 74 discharge
complete the guard-integrity family opened by WS-E 72 and 73. Item 42's own
caveat (c) named WS-E 74 as the adjacent unfixed hole, so the second act
discharges a debt the first act recorded.

**Stated honestly, because DEC-0017 is a standing obligation and this arc did
not satisfy it in the ordinary way: no build-queue artefact was merged or
materially advanced this session.** Both PRs are governance. DEC-0017's
exception is narrow — the item must *directly block* a merge — and **that
exception is not claimed here**, because the guard defects blocked no build
artefact. What is claimed is narrower and different: the first act was ruled
before the session began, and the second discharged the first's own recorded
residue. **Whether that satisfies DEC-0017 or requires a recorded exception is
the chair's call, and it is owed at close.** It is written this way so the
question is put rather than quietly answered.

## 4. Evidence, and the tiers kept apart

The re-probe returned **11 / 11** (PROMPT 141). The two halves of that table
are not the same kind of fact and this record will not let them merge:

- **DENY rows — proven live.** The guard's own refusal text returned verbatim
  through the harness. This additionally evidences that the PreToolUse matcher
  **routes** Bash calls to the hook, which is a positive result against WS-E 64.
- **ASK rows — closed guard-side**, by stdin PreToolUse payload against
  `main()`, exercising the real dispatch order. **Human surfacing remains
  unprovable (WS-E 75)** and is not claimed anywhere in this arc.

**What the arc did NOT establish:** that a human sees a surfaced ask. Every
ask-class claim in both PRs stops short of that line deliberately.

## 5. Prompt numbers consumed

**134, 135, 136, 137, 138, 139, 140, 141, 142.** Per the interim practice
adopted at
`docs/governance/FOLD_IN_2026-08-18_prompts-125-126-and-guard-install.md`
section 5(a), pending queue item 34 M2.

PROMPT 138 is recorded as **issued and correctly refused**: its precondition
read found the F3/F4 install had not landed, and the ten rows were not run
against an unfixed guard. The prompt is spent, and the run it specified
happened at PROMPT 141 after the install. Recorded rather than renumbered.

## 6. Not done this arc

- **`/session-close` has not run.** Queue pointer, cost row and handover owed.
- **`/cost` for this session was requested and not supplied.**
- **D2.2a pre-flight not run** — conditional on the arc touching retrieval, and
  it does not.
- **Item 27 Part B remains HELD.** WS-E 74's discharge spends ground (iv) only;
  grounds (i) to (iii) stand and are sufficient. A fresh chair ruling is still
  required and this arc does not supply one.

## 7. Disposition

No control mapping line is carried, for the reason
`docs/governance/SESSION_COSTS.md` states: queue item 34 M11(d) requires
per-class mapping content to be defined once in the control framework, and that
framework does not exist yet.
