# ARC RECORD 2026-08-19 — A-2026-08-19-02, "DEC-0018 fold-in and queue commissioning"

Governance lane. Authored under PROMPT 147 on branch
`governance/dec-0018-sources-and-arc-record`.

**This is an arc record, not a session close.** The arc is OPEN at the time of
writing: `/session-close` has not run, no cost row exists, and the CLOSE cell
in `docs/governance/ARC_REGISTER.md` is deliberately empty. Those remain owed.

## 1. Arc

**A-2026-08-19-02 — "DEC-0018 fold-in and queue commissioning". Governance
lane. OPEN 2026-08-19T16:19:15Z (reconstructed).**

| Act | Vehicle |
|---|---|
| Queue round trip: `ARCA-P-0144` staged, released, executed; `ARCA-R-0144` returned and verified both ends | No PR — pre-repo, recorded at `docs/governance/QUEUE_CYCLE_2026-08-19.md` |
| DEC-0018 fold-in: register entry, A6 correction, arc register created, queue-cycle record | **PR #147**, merged `012fb33` |
| Source documents into tree, this arc record, DEC-0017 displacement | **This PR** |

**The first act produced no PR, and that is the point of the third.** The
round trip ran post-close and outside any arc, so its only durable trace until
PR #147 was a pair of Gmail drafts. An arc whose first act lives only in
transport is precisely the M2 gap; this arc's later acts are what pull it into
the tree.

## 2. Rulings, verbatim

**Ruling 1 — arc naming (chair, under the standing "today" delegation,
2026-08-19, carried by PROMPT 147).**

> A-2026-08-19-02, "DEC-0018 fold-in and queue commissioning", governance
> lane, named under the chair's standing "today" delegation (same delegation
> note as A-2026-08-19-01).

**The delegation is recorded because the default is the opposite.**
`.claude/skills/session-open/SKILL.md` makes arc naming operator-only and
never delegable. This naming was made under an explicit standing delegation
from the chair, which is a different thing from an executor inferring an arc
from the queue — the failure that rule exists to prevent. Same footing, and
same paragraph, as the naming of `A-2026-08-19-01`.

**Ruling 2 — DEC-0017 displacement (chair, 2026-08-19, verbatim).**

> "The 08-19 close bound the next session build-first (item 36); the chair's
> Q-R3 amendment of the same evening displaced that binding for this arc only
> — a later ruling displaces an earlier one, and this records the
> displacement. Build-first with item 36 as spine now binds the session AFTER
> this one."

**Ruling 3 — `.claude/settings.json.e2-before` residue (chair, 2026-08-19,
verbatim).**

> "e2-before residue: confirmed operator act — the chair removed
> .claude/settings.json.e2-before mid-session on coordinator advice; no
> unexplained actor."

## 3. DEC-0017 disposition — DISPLACEMENT, not exception

**This is a different disposition from the previous arc's, and the difference
matters.** `A-2026-08-19-01` closed with an **exception recorded against a
rule left tight**: the narrow *directly-blocks* carve-out was available and was
declined, so DEC-0017's meaning did not move. This arc closes on
**displacement**: an earlier binding is superseded by a later ruling from the
same authority, and the obligation it created does not disappear — it moves.

**What the displacement does not do.** It does not weaken DEC-0017, does not
claim the *directly-blocks* exception, and does not create a precedent that
governance may generally precede build. It is scoped by its own words to *this
arc only*, and it re-attaches the build-first obligation to the next session
explicitly rather than leaving it to lapse.

**Binding forward, stated so it cannot be lost:** the session after this one
opens **build-first**, with queue item 36 — the runner's six unhonoured Rev C
fields — named as the candidate spine. That is the second consecutive session
to carry this binding forward, item 46 having recorded it first, and a third
consecutive deferral should be read as a pattern rather than a schedule.

**Stated honestly:** no build-queue artefact was merged or materially advanced
in this arc either. Both of its PRs are governance.

## 4. The e2-before residue — open note closed

`docs/governance/DEC-0018_A6_CORRECTION_2026-08-19.md` section 3(b) recorded
an untracked `.claude/settings.json.e2-before` present at the arc's opening
state check and in the 16:21 UTC manifest snapshot, absent when re-checked
before commit, and it left the actor unstated because the executor could not
know.

**Ruling 3 above closes that note: it was an operator act, made on coordinator
advice, and there is no unexplained actor.**

**The note is closed, not deleted, and the correction file is not edited.**
Two reasons, and the second is the load-bearing one. First, this PR's scope
does not include that file. Second, the file's own value is that it recorded an
observation faithfully at a moment when the explanation was unavailable —
retro-fitting the answer into it would erase the very thing that made it worth
writing. The answer is recorded here, where the reader who follows the
citation will find it.

**Worth keeping as method:** an executor observed a state change it could not
explain, refused to guess at the cause, and named it as owed. The explanation
arrived one prompt later. That sequence is what the discipline is for.

## 5. Queue commissioning — what this arc established, and what it did not

**Commissioned here: A4.4, the mandatory R-leg.** Every future ARCA-P item
concludes with its ARCA-R twin, staged by the executor, carrying the PR number
and URL, the files-changed list, battery results, any stops or conflicts, and
a STATUS line. **The terminal readback becomes corroboration; the R-draft is
the return leg of record.** First applied at `ARCA-R-0147`, staged at this
PR's open. The reasoning is the M2 reasoning: a readback that exists only in a
terminal transcript is not evidence anybody can retrieve later.

**Established by this arc:** the queue format round-trips (P staged, released,
polled, executed, R returned, verified at both ends); the release gate works,
since a `[STAGED]` subject is not executable and only the chair's rename makes
it so; and the duplicate gate works where a reply artefact exists.

**NOT established, and none of it should be inferred from the above:**

- **That an unattended poll works.** Every act in this arc was attended, and
  the first poll of the first item was declined at the permission gate and
  needed an explicit re-approval. That stall is the concrete case A3.2 cites.
- **That the queue is governed.** The MCP tools the queue uses sit outside the
  PreToolUse matcher entirely, so no guard was exercised at any point in any
  queue act. This is what makes the queue leg safe to unattend without a
  widening, and equally what means no guard probe evidences anything about it.
- **That staging is tamper-evident.** An item is mutable until release —
  `ARCA-P-0146` rewrote its own `TS:` in place and said so. Nothing pins a
  staged body against its released form, so the chair's release attests to the
  text at release time and to nothing earlier.
- **That idempotency generalises.** `ARCA-P-0147` has an R-leg, so its
  duplicate check has a target. Items ending at PR-open do not, and their
  markers are the branch and the PR. A4.4 incidentally fixes this by giving
  every P-item an R-twin to check against.

## 6. Prompt numbers consumed

**144, 145, 146, 147.** Per the interim practice at
`docs/governance/FOLD_IN_2026-08-18_prompts-125-126-and-guard-install.md`
section 5(a), pending queue item 34 M2. No next number is predicted: a prompt
exists when it arrives and not before.

`ARCA-P-0127` is **RETIRED UNRELEASED** for tally collision, 127 having been
consumed in the 2026-08-18 session. Nothing was executed under it. Recorded at
`docs/governance/QUEUE_CYCLE_2026-08-19.md` section 4.

## 7. Not done this arc

- **`/session-open` did not run.** Ceremonies are user-invoked and the
  executor did not self-invoke. Live register derivation, which
  working-protocol rule 4 requires regardless, was performed directly at both
  PRs.
- **The rehash sweep did not run.** This arc touches no corpus and no
  retrieval. Queue item 47 records that the sweep's Postgres precondition is
  unstated in the boot sequence.
- **`/session-close` has not run.** Queue pointer, cost row and CLOSE
  timestamp are owed, and the arc register's CLOSE cell is empty until then.
- **`/cost` has not been supplied** for this CC session, which covers both the
  round trip and the fold-in.
- **The F5 envelope-guard amendment is not started** (queue item 48), and the
  render-route disambiguation probe has not run (queue item 49).

No control mapping line is carried, for the reason
`docs/governance/SESSION_COSTS.md` states: queue item 34 M11(d) requires
per-class mapping content to be defined once in the control framework, and that
framework does not exist yet.
