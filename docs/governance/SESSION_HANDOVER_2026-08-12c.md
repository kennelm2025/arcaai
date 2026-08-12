# SESSION HANDOVER — ArcaAI 2026-08-12c (CL-24 residue closure arc)

*Covers one session, scoped to a single named arc: queue item 2, the CL-24
governed-store residue cleanup and closure. Landed at PR #102, merged
`545075b`. CL-24 is closed in full; open CLs fall 15 to 14. No register number
consumed. **Supersedes the boot line of**
`docs/governance/SESSION_HANDOVER_2026-08-12b.md`, retained as the record of the
pack-install arc. Authored on explicit operator command, on the close branch, so
the queue update and this file ride one PR — the fourth consecutive arc where
they do. Every queue reference below was verified against the **committed**
queue on this branch (28 items, markers at 316 and 630), not against the summary
it was drafted from.*

## Boot line (next session)

> Resume ArcaAI — B7 in progress. HEAD main to be the PR carrying this file;
> PR #102 merged at `545075b`. Boot ritual: conda arcaai → main → `git pull
> --ff-only` → `git fetch --prune` → `python scripts/repo_manifest.py --out
> D:/Downloads` → Divergences read, **expect zero** → Docker Desktop up →
> `scripts/dev_up.cmd` → `python scripts/rehash_sweep.py`.
> **The sweep now expects GREEN, exit 0, and the carve-out is RETIRED.** Expect
> `category irreproducible-pin : 0`, `category excluded-by-rule (test) : 0` and
> "all pins verified". **Any red is a plain stop** — there is no longer a shape
> of red that is acceptable, and the two `fixture-*` rows that the old carve-out
> tolerated no longer exist.
> **The governed store is empty.** All five audit tables are at zero, including
> `audit_payload`. Standing rules, permanent: the harness never elevates, never
> assumes the database owner role, and never bare-`cd`s in a persistent shell.
> **The next arc is queue item 3, D2.2a pre-flight** — unblocked by this arc and
> holding right of way under DEC-0017. A read-only session brief was prepared;
> see "Next arc" below.

## The arc

Discharge queue item 2 — delete the CL-24 test residue from the governed
`arcaai_audit` store as an operator-run owner-role act, verify independently,
and close CL-24.

## What landed

**PR #102** — merged `545075b`, 3 files, 107 insertions, 29 deletions.

**The cleanup.** The harness drafted the statements; the operator ran them. FK
order `audit_event` → `audit_run_terminal` → `audit_run` → `corpus_version`,
every delete scoped by the identities in the CL-24 baseline, each asserting its
own row count inside one transaction, with a fail-closed preflight refusing any
database but `arcaai_audit` and any role but `arcaai_owner`. **No `TRUNCATE` and
no unqualified `DELETE` anywhere.**

**Scope widened during the act, on evidence.** `audit_payload` held 3
test-written rows, first seen 2026-08-11 14:04, visible to neither the baseline
instrument nor the rehash sweep. Ruled in scope by the operator and cleared, so
five tables were emptied rather than four. Left in place, the closure artefact
would have asserted an empty store while a table its own instrument does not
enumerate was not empty.

**Figure correction.** Queue item 2 read `2 / 18 / 14 / 18` against the order
`audit_event, audit_run_terminal, audit_run, corpus_version`, transposing first
and last. Both the baseline and the live store showed `audit_event` 14 and
`corpus_version` 2. Corrected explicitly rather than silently: the wrong pair
would have had a reader expect 18 `corpus_version` rows and find 2.

**CL-24 closed** in `docs/governance/GOVERNANCE_REVIEW_CHANGELOG.md`, canonical
for CL items. **Boot carve-out retired** at queue item 1.

**Register state, read live at close:** DEC next 0018, ADR next 0011, CL next
26, WS-E next 69. 14 open CLs, down from 15. 0 divergences.

## Verification battery

`git diff --stat` first throughout; final close diff `CLAUDE.md` only, 13
insertions, 2 deletions, inside the queue markers.

All store verification was taken **non-elevated as `arcaai_app`** and
independently of the operator's terminal output:

```
rehash_sweep: category irreproducible-pin       : 0
rehash_sweep: category excluded-by-rule (test)  : 0
rehash_sweep: all pins verified
sweep exit: 0
```

Five-table count `0 / 0 / 0 / 0 / 0`. Closure read written as the AFTER-CLEANUP
section of `docs/governance/CL-24_governed-store-baseline_2026-08-12.md`, identity
digest `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` — the
SHA256 of the empty string. `audit_payload` stated separately at 0, because the
instrument cannot see it.

`check_docs.py` 121 files, no findings. Sweep re-run green from `main` after
merge, under the newly retired carve-out.

## A near-miss worth carrying

The FK graph was read from `pg_constraint`, not `information_schema`. The latter
returned **zero rows** as `arcaai_app`, because its constraint views filter by
privilege — a result that reads exactly like "this schema has no foreign keys"
and would have produced a delete order justified by an absence that was an
artefact of the reading role. The real graph has three foreign keys. Same family
as queue item 8.

## Open verifications carried forward

1. **The instrument, not the residue, is the outstanding defect.**
   `scripts/governed_store_identity.py` enumerates four tables from a hardcoded
   list and does not see `audit_payload`. The rows are gone; the blindness is
   not. Queue item 28.
2. **`${CLAUDE_PROJECT_DIR}` is still verified in this harness only** — never
   exercised in CI or another clone.
3. **Skill and subagent hook routing remain unprobed**, as do the Tier 1 rule
   strings, which queue item 27 records as verified and *wrong*.
4. **The Mobile Ruling Protocol pilot counter is still at zero.** No mobile
   ruling has yet been made through the issue template.

## Next arc — item 3, deliberately not opened

Queue item 3, the D2.2a pre-flight implementing artefact, is unblocked by this
arc: the governed store is empty and the sweep green, so Commissioning Session
Records can be written into `arcaai_audit` without the next battery erasing
them, which was the dependency that made item 2 owed before the spike. It holds
right of way under DEC-0017 as a build artefact and claims the next free CL
number, read live at the arc that opens it.

**It was deliberately not opened on 2026-08-12**, with forty minutes remaining
before the operator's hard stop, on the grounds that the arc could not be opened
and closed cleanly in the time and that a half-written ceremony is worse than an
unstarted one. A read-only session brief was prepared instead and mirrored to
the operator's drafts; it is a brief, not a beginning, and carries no register
number and no repository write.

## Return queue

Source of truth is the queue block in `CLAUDE.md` as committed at PR #103,
verified against this file. **Twenty-eight items.** Item 2 is closed; item 1's
carve-out is retired; item 3 is the next arc. Items 24 to 28 are the day's
additions, of which 24 records a disconfirmed suspicion and 28 the
instrument-blindness found during this closure.
