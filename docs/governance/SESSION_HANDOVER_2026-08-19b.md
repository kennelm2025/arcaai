# SESSION HANDOVER 2026-08-19b — arc A-2026-08-19-01, "Guard integrity close-out"

**Boot line for the successor: clean tree at `3cfaea5` before this close PR;
WS-E next 76, DEC next 0018, ADR next 0011, CL next 31; divergences 0.
Regenerate the manifest yourself — a manifest found on disk is presumed
stale.**

**THE HEADLINE, PLAINLY: you inherit ZERO ruled-not-written debt.** Every
ruling made this session is written to the registers before this handover was
authored. There is no "ruled but not yet recorded" item to discover, no queue
entry deliberately lagging a decision, and nothing in section 4 of a
predecessor handover telling you the queue is correct-but-stale. That was not
true of the last two handovers and it is worth stating as the first fact
rather than the last.

---

## 1. THE ARC

**A-2026-08-19-01 — "Guard integrity close-out". Governance lane. CLOSED
CLEAN.**

Write the pre-ruled item 42 discharge, then fix and discharge WS-E 74, closing
the guard-integrity family opened by WS-E 72 and 73.

Named by the coordinator under explicit chair delegation at PROMPT 142, after
both acts had landed. Recorded that way round in
`docs/governance/ARC_RECORD_2026-08-19_guard-integrity-close-out.md` rather
than presented as though the naming preceded the work.

## 2. WHAT LANDED

**Three PRs, all merged and all verified post-merge from `main`.**

| PR | Merge | Content |
|---|---|---|
| **#142** | `f236e6f` | Item 42 OPEN→DISCHARGED with three caveats; **WS-E 75 raised**; history-rewrite refusal string baselined; 2026-08-18 cost row at basis DIRECT; correction of record for the handover's subtraction route |
| **#143** | `dc06118` | F3/F4 install record for the operator-applied guard change; 1 file, +5/−7 |
| **#144** | `3cfaea5` | WS-E 74 OPEN→DISCHARGED; WS-E 75 method upgrade; `CLAUDE.md` WS-E 74 status corrected in both places; item 8 gained the probe-spec inversion; arc record created |

**Files created (4, counting this close):**
`FOLD_IN_2026-08-18_ADDENDUM_history-rewrite-baseline_2026-08-19.md`,
`CORRECTIONS_cost-basis_2026-08-19.md`,
`ARC_RECORD_2026-08-19_guard-integrity-close-out.md`, and this handover.

**One register number consumed: WS-E 75.** Three merged PRs against one
number. DEC, ADR and CL all unchanged.

## 3. THE GUARD FAMILY IS FULLY DISCHARGED

**WS-E 72, 73 and 74 are all closed.** The family that has dominated three
sessions is done.

**Routing is positively evidenced, which bears directly on WS-E 64.** The DENY
rows returned the guard's own refusal text verbatim through the harness. That
is not composition and not inference: a refusal string can only have reached
the transcript by the PreToolUse matcher routing the call and the hook
executing. WS-E 64 recorded three days in which a guard was correct in its
patterns and unreachable in its wiring, reading as green throughout. **That
question is now answered positively for the Bash tool.**

**Boot completed through step 5 GREEN** — after `dev_up.cmd`. It was UNKNOWN
at first attempt because Postgres was unreachable; see item 47.

### The evidence tiers, and why they must stay apart

**DENY rows — proven live.** Refusal text verbatim through the harness,
twelve rows across the session.

**ASK rows — closed guard-side**, by feeding each command to the module as a
PreToolUse payload on stdin and reading its JSON answer. That exercises
`main()` and its real dispatch order rather than a reimplementation — which
matters, because dispatch order is load-bearing here: the H-11 deny runs first
and `respond()` exits, so an ask that composition would report is one the
module never reaches.

**Human surfacing is NOT proven and cannot be.** In the live transcript an
approved ask and a silent allow produce identical output. **No ask may be
cited as evidence that a human was consulted.** Three artefacts now depend on
this distinction; do not let them merge.

## 4. CARRIED FORWARD BY CHOICE

Nothing here is residue. Each was available to take and was left deliberately.

**(a) Item 27 Part B — HELD.** WS-E 74's discharge spent ground (iv) and only
ground (iv). Grounds (i) its ruling was never made, (ii) allow-pre-empts-guard
still open, and (iii) the ask tier is guard-proven-only, all stand and are
**sufficient on their own**. Needs a fresh chair ruling; the discharge of
item 42 does not license it.

**(b) DEC-0018 — numbering collision, then ruling. CHAIR-SUPPLIED, AND
UNVERIFIED IN-REPO — read this caveat before acting on it.** The chair
records that a delegation model and a dashboard both claim DEC-0018, with
"Footnote F1 reduced form" on the table for the ruling. **No repository
evidence supports or contradicts this**: the manifest regenerated at this
close reads `DEC: highest 0017 → next 0018`, unconsumed, and a repo search
finds no artefact claiming 0018 at all. It is carried verbatim as supplied
rather than dropped or elaborated. **The successor should establish the two
claimants before allocating 0018** — the collision, if real, lives outside
this repository, which is itself the item 34 M2 problem.

**(c) Item 36 — next session's build-first spine.** Runner Rev C conformance:
six unhonoured fields plus the seventh, the load-time `top_k` ≤
`top_k_absolute_cap` comparison that JSON Schema cannot make. Named as the
candidate spine by the DEC-0017 ruling at section 5.

**(d) Item 12 — the highest-leverage operator ruling available.** Fourteen
documents at `pending_review`; an inclusion decision is a **re-pinning event**
moving `retrieval_snapshot_sha256`, the eligible-set hash and the chunk count,
re-pinning all seven RQA scenarios. `RQA-106` needs re-authoring, not
re-pinning, and `RQA-104`'s Obligation D expires. Needs no build work.

**(e) WS-E 75's final link, with item 34.** Routed to the M-family, narrowed
to human surfacing only. **M3, server-side enforcement, is the natural home**
— a platform-level control does not depend on a prompt reaching anyone.

**(f) Item 40 — untested this session, no claim either way.** The full pytest
suite was never run. The two guard test files were, and passed 131/131. **Do
not read that as evidence about item 40**; different scope entirely.

## 5. RULINGS THIS SESSION, VERBATIM

**Ruling 1 — DEC-0017 disposition for A-2026-08-19-01 (chair, PROMPT 143).
EXCEPTION RECORDED, not satisfied.**

> "Session opened under a pre-ruled first act (PROMPT 133) whose discharge
> lawfully pre-empted build-first arc selection; the second act discharged the
> first's own recorded residue. No build artefact was blocked or advanced. The
> narrow directly-blocks exception is not claimed; DEC-0017's meaning stays
> tight. Next session opens build-first (item 36 named as the candidate
> spine)."

**The refusal is the load-bearing half.** The *directly-blocks* carve-out was
available and declined. An exception recorded against a tight rule costs one
queue entry; a rule loosened by a claimed exception costs the rule. Queue item
46, closed at birth.

**Ruling 2 — SO-1 trigger convention (chair, PROMPT 143). AMENDED.** The bare
trigger is blessed for SO-1 merge verification specifically, five consecutive
uses being the evidence, and the battery running identically either way.
**Numbered prompts stay mandatory for anything that INSTRUCTS; the bare form
is permitted only for what RELEASES** a fixed, pre-ruled sequence. Recorded in
`SESSION_PROTOCOLS.md` under Standing operational rules, superseding the
trigger-form paragraph of
`docs/governance/PERMISSION_CLASSES_2026-08-17_partA-applied-widening-held.md`
section 5 — which is dated and is not edited.

**Ruling 3 — handover (chair, PROMPT 143). COMMANDED, not deferred.**

## 6. CONVENTIONS AND FINDINGS

- **Check-method, first instance about a probe SPEC rather than a probe.** The
  rule *"git's own error is a BYPASS result, not a pass"* holds for deny rows
  and **inverts for ask rows**, where git's error is the expected signature of
  an approved ask. Applied mechanically it would have failed six correct rows.
  **Probe-spec expectations are stated per tier, never per table** — and on
  the ask tier no observable signature discriminates at all, so those rows
  needed a different *instrument*, not a different threshold. Queue item 8.
- **Two sign checks beat one.** The cost row is bracketed by an interim
  readout as well as a close readout, which closes the mid-session-reset
  ambiguity the 2026-08-18 row had to leave open. Taking an interim readout is
  cheap and worth repeating.
- **Arc identifiers have no register home**, exactly as versioned code
  artefacts do not. Two unrelated classes reaching the same dead end;
  queue item 41 widened.
- **A commanded edit outranks an expected file count.** This close PR changes
  **5** files where the prompt said 4 — the arc record §3 write is commanded
  by Ruling 1 and was not in the enumerated list. Reported rather than dropped.
- **PROMPT 143 arrived truncated** mid-sentence and was completed in a second
  delivery. Recorded because the transmission-truncation pattern already has
  precedent at queue item 33.

## 7. VERIFICATION BATTERY

| Check | Result |
|---|---|
| `git diff --stat` (first) | non-empty, read before commit |
| `git status` | clean; `main` == `origin/main` at `3cfaea5` pre-close |
| `python scripts/repo_manifest.py` | **0 divergences**, 13 stages, 16 open CLs |
| `python scripts/check_docs.py .` | **no findings**, exit 0 |
| `scripts\lint.cmd` | All checks passed, exit 0 |
| `python scripts/rehash_sweep.py` | **GREEN**, exit 0, both categories 0, "all pins verified" |
| Guard tests | 131 passed, exit 0 (PR #143) |
| Attribution | full bodies printed and read; zero matches at rc=1, **positive control fired at rc=0**, on every commit |

## 8. OPEN VERIFICATIONS FOR THE SUCCESSOR

1. **WS-E 75 is narrowed, not discharged.** The human-surfacing link is open.
2. **DEC-0018's claimants are unverified in-repo** — section 4(b).
3. **Item 40 status unknown this session** — no full-suite run.
4. **Item 47 is recorded, not fixed** — `/session-open` step 5 still has one
   sentence for two outcomes and an unstated dev-stack precondition.
5. **The dev stack was left UP** — Postgres healthy, MLflow started. Not torn
   down; `scripts\dev_down.cmd` if you want it clean.

## 9. COSTS

**$18.20 · API 27m 50s · wall 1h 6m 18s · +1432/−15 · dominant model
`claude-opus-5`.** Basis **DIRECT**, operator readout at the close stop.

**Two sign checks recorded:** below the 2026-08-18 anchor of $52.14, proving
the counter reset; above this session's interim readout of $6.69, proving it
is the same counter and did not reset mid-session. Reset boundary is the CC
session — **second consecutive observation, a pattern and not yet a rule**.

Row at `docs/governance/SESSION_COSTS.md`, first row to carry an arc
identifier in the Session column.

**Prompts consumed this session: 134, 135, 136, 137, 138, 139, 140, 141, 142,
143.** **PROMPT 138 is recorded as STOPPED-AT-PRECONDITION** — its
precondition read found the F3/F4 install had not landed, and the ten rows
were **not** run against an unfixed guard. That was the correct stop, and it
is why the evidence is untainted: the table at PROMPT 141 measures a fixed
guard, and the `f236e6f` pre/post comparison was constructible only because
138 refused to spend it early. The prompt is spent and is not reissued.

## 10. SUGGESTED OPENING

`/session-open`, then **build-first per Ruling 1** — item 36 is the named
candidate spine, touching `arcaai/harness/runner.py` and `tests/harness/`.

**Item 21** (`.sql` ungoverned in `.gitattributes`) is genuine shadow work
against it: touches `.gitattributes`, `sql/` and `infra/postgres-init/`, all
disjoint from the harness tree.

**Item 37** looks like shadow work and is not — its citation sweep touches
`CLAUDE.md`, so it collides with any queue edit.

**Item 12** remains the highest-leverage ruling available and needs no build
work at all. The operator resequences freely.

---

*No control mapping line is carried, for the reason
`docs/governance/SESSION_COSTS.md` states: queue item 34 M11(d) requires
per-class mapping content to be defined once in the control framework, and
that framework does not exist yet.*
