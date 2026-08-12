# SESSION HANDOVER — ArcaAI 2026-08-12 (CL-24 test-database isolation arc)

*Covers one session, scoped to a single named arc: CL-24, test-database
isolation, at the scope WS-E 65 enlarged it to. Landed at PR #96, merged
`2469c2a`. Three of the four ruled scope parts are discharged; the fourth,
residue cleanup, is deliberately not done because it is an owner-role act
belonging to the operator and sequenced after the isolation merges.
**Supersedes the boot line of** `docs/governance/SESSION_HANDOVER_2026-08-11d.md`,
retained as the record of the permission tiering arc. Authored on explicit
operator command, on the close branch, so the queue update and this file
ride one PR — the second consecutive arc where they do, keeping closed the
chain-break recorded at open verification 6 of the 2026-08-11b and
2026-08-11c handovers.*

## Boot line (next session)

> Resume ArcaAI — B7 in progress. HEAD main to be the PR carrying this
> file; PR #96 merged at `2469c2a`, clean, all five checks green
> (lint-test, vertical-tests, promotion-gate, manifest-history,
> structural-checks). Boot ritual: conda arcaai → main → `git pull
> --ff-only` → `git fetch --prune` → `python scripts/repo_manifest.py
> --out D:/Downloads` → Divergences read, **expect zero**, no carve-out,
> held now across PRs #86 through #96 → Docker Desktop up →
> `scripts/dev_up.cmd` → `python scripts/rehash_sweep.py`.
> **The sweep still expects RED, but its shape has changed and the new
> shape is the check.** Expect exactly `category irreproducible-pin : 0`
> and `category excluded-by-rule (test) : 2`, naming
> `fixture-d53c6ac1-…` and `fixture-9e191dd4-…`. Those two rows are now
> **static** — since DEC-0016 the suite writes to `arcaai_audit_test`, so
> they are no longer replaced with fresh identifiers at every battery
> run, and if their identifiers change, the isolation has broken. Any
> other shape is the stop. The carve-out retires when the residue
> cleanup lands, and not before.
> **Two audit databases now, and the suite may only ever touch one** —
> `DECISIONS.md` DEC-0016 is authoritative. `arcaai_audit` is the
> governed store; `arcaai_audit_test` is disposable and is what
> `tests/governance/` targets. A fail-closed guard in
> `tests/governance/conftest.py` refuses the run unless the resolved DSN
> names the test database. A machine whose `pgdata` volume predates
> 2026-08-12 needs the one-off `CREATE DATABASE arcaai_audit_test OWNER
> arcaai_owner` by hand, because Postgres runs its init directory only at
> cluster initialisation; that is an operator act at the operator's
> terminal. **The next act on CL-24 is the residue cleanup**, owner-role,
> operator-commanded, now unblocked. Standing rule, permanent: the
> harness never elevates, and never assumes the database owner role.

## What landed

1. **PR #96 merged (`2469c2a`) — CL-24 test-database isolation.** Four
   commits, 11 files, +727 / −20. All five checks green pre-merge;
   `lint-test` 2m48s is the one that matters, because it exercised the
   new database bootstrap and the run-time `current_database()` grant
   inside a fresh CI service container rather than only on this machine.
2. **DEC-0016 — test-suite writes are separated from the governed audit
   store by database.** Separation by database, not by schema: a schema
   leaves the destructive verb running inside the governed database as
   owner, and a mis-set `search_path` is invisible in the DSN, which
   makes the failure quieter rather than rarer. Marker-only exclusion
   rejected outright — `drop_all` wipes marked and unmarked rows alike.
3. **WS-E 66 and WS-E 67 appended.** 66: the harness assumed the
   Postgres superuser account for three read-only inspections early in
   the arc, self-disclosed in-session. 67: a `CREATE DATABASE` reported
   done had not happened, and the mandatory battery is what found it.
4. **The trailer-verification convention in `CLAUDE.md` amended twice**,
   both from defects this arc's own verification surfaced. See "The
   convention that failed on its own documentation" below.
5. **Stale-branch housekeeping discharged.** 22 merged local branches
   deleted; `main` is now the only local branch and the remote head was
   pruned. This was the standing housekeeping item.

## The arc

### The defect, and why WS-E 61 had it backwards

The session-scoped `_schema` fixture in `tests/governance/conftest.py`
ran `drop_all` then `create_all` as `arcaai_owner` against the dev
`arcaai_audit` database, whose DSN defaults lived in that same file.
Every run of the mandatory battery therefore erased every audit event and
every `corpus_version` row **before the first test executed**. The
append-only property held exactly as designed for the application role —
`sql/governance_grants.sql` withholds UPDATE and DELETE, and two tests
assert the denial — while the owner role dropped the tables wholesale.
The repository's own mandatory battery defeated the guarantee its own
suite proves.

WS-E 61 had recorded the same residue as tests failing to clean up
afterwards. The inverse is true and worse: they destroy beforehand, which
is why that entry's remediation deleted rows whose cause was never
diagnosed.

### What was built

Separation by database, with the guard as the actual control. The suite
targets `arcaai_audit_test`; the governed `arcaai_audit` is never a suite
target. `_refuse_unless_disposable` refuses the run unless **the engine's
own URL** names the test database — the URL rather than the DSN constant,
because the constant records what we intended to connect to and the URL
is what will actually be dropped, and WS-E 65 is an incident in which the
two were assumed identical. It is checked at engine construction and
again at the destructive site, because WS-E 64's lesson is that stated
coverage is a claim about wiring.

Provisioning follows the precedent `infra/postgres-init/01-create-mlflow-db.sql`
already set: `infra/postgres-init/02-create-audit-databases.sql` creates
both databases at stack init. This closed a latent gap in which
`arcaai_audit` existed on the operator machine out-of-band with no
artefact in the repository creating it. `.github/workflows/ci-devops.yml`
creates both too, so the two provisioning paths cannot drift.
`sql/governance_grants.sql` now resolves its database-level GRANT through
`current_database()`, so one artefact serves both databases rather than
forking into a copy — the duplication failure DEC-0014's consequences
already fixed once here.

`scripts/rehash_sweep.py` gained two named categories, printed on every
run **including at zero**, and still exits non-zero on either. A sweep
silent about a category cannot be distinguished from one that never
checked it.

### The proof is identity, not count

`docs/governance/CL-24_governed-store-baseline_2026-08-12.md` carries
BEFORE and AFTER-BATTERY sections either side of a full `scripts\test.cmd`
run: identical digest
`5184a6d098e65c6e8408688709bbdec61bba4ebdb5e3826964957bc08fa23bd5` and
identical identity lists per table. The expectation was pre-registered in
prose before the battery ran, on operator instruction, together with the
sweep's expected non-zero exit.

The second half is what makes the first mean anything: the test store
holds 2 / 18 / 14 / 18 rows after that run. Without it, an unchanged
governed store would be equally consistent with isolation working and
with the suite writing nothing at all.

### A CREATE DATABASE that had not happened

The first battery attempt failed at fixture setup on about 27 tests with
`FATAL: database "arcaai_audit_test" does not exist`, after the create
had been reported done. A non-elevated read of `pg_database` confirmed
six databases with no near-miss spelling; `docker ps` excluded
wrong-container and wrong-instance. Cause: the command errored unnoticed
with its output unread. Re-issued with a catalogue read appended to the
same invocation so the act carried its own verification.

No harm, and the reason matters: the failure was **fail-closed**. The
suite errored at connect with no code path retrying against the governed
database, so an absent test database could not silently redirect writes.
Recorded at WS-E 67, whose class note was tightened during the arc onto
the claim that actually failed — a report that a command was issued is
not existence evidence; only output actually read, or a catalogue read,
establishes that an object exists.

### The convention that failed on its own documentation

`CLAUDE.md` required the absence of a `Co-Authored-By` trailer to be
asserted "by trailer count, never by eyeball". Two defects surfaced while
applying it. `%(trailers)` parses only the final paragraph, so a stray
line mid-message expands to nothing and the check reports zero while the
line is plainly visible. And a count piped through a fallback inside a
substitution renders clean-absence and check-never-ran identically,
because the counter exits non-zero on no match and the fallback swallows
it into an empty string — a green indistinguishable from not having run,
inside the very command written to verify a house rule.

Amended to assert against the full printed body. Applying that amendment
to this branch immediately exposed a defect in the amendment: asserting
absence of the token "anywhere in the body" flags the commit that
documents the rule, which mentions it in prose. Refined by ruling to
**attribution, not occurrence** — an attribution line is the token at
line start, a colon, and a name or address; prose mentioning the token is
not attribution.

## Registers at close

DEC next **0017** · ADR next **0011** · CL next **26** (15 open) · WS-E
next **68**. Derived from `scripts/repo_manifest.py` regenerated
in-session at boot, after each append, and again post-merge — every run
agreeing. **Three numbers consumed this arc:** DEC-0016, WS-E 66, WS-E 67.
B7 ENTERED, exit evidence open, unchanged.

**Divergences: zero**, at every regeneration.

## Open verifications

1. **Residue cleanup is not done.** The governed store still holds 2
   `corpus_version`, 18 `audit_run`, 14 `audit_event` and 18
   `audit_run_terminal` rows, all test-written. Owner-role act at the
   operator's terminal, in FK order. The boot carve-out stays live until
   it lands.
2. **The carve-out wording in the queue was repointed**, not rewritten:
   "until item 2 lands" became "until the residue cleanup at item 2
   lands", because item 2 has now largely landed and the old phrasing
   would read as expired. Flagged rather than slipped past, since the
   standing instruction was to leave item 1 alone until cleanup.
3. **The recursive `infra/` entry added to the ci-devops filter is
   unverified.** PR #96 tripped other filters anyway; an infra-only PR
   remains the untested case.
4. **`.sql` is ungoverned in `.gitattributes`** — new queue item. The
   two SQL files check out CRLF on Windows; `psql` tolerates it and the
   dollar-quoted blocks are unaffected, so this is latent, not breaking.
5. **The refined trailer test has never been exercised against a commit
   that would fail it** — only against four that pass.
6. **WS-E 66 has no mechanism behind it.** The corrective is that the
   non-elevated route was found and used, and that
   `scripts/governed_store_identity.py` hardcodes the app role and
   refuses any database but the governed one. Nothing prevents
   recurrence but discipline.
7. **CL-25 sharpens on landing.** WS-E 65 records that no harm has come
   of the destruction only because nothing of record has ever been in
   that store, every row having been written by its own tests. That is
   an accident of sequencing, not a control, and it expires the moment
   an operational writer exists.

## Return queue, in order

Enumerates the `CLAUDE.md` queue block as committed on this close branch,
item for item and in its order, read back from the committed file.
Renumbered this close: the governance-suite-destroys-the-store item and
the stale-branches item both discharged and were removed, everything
below shifted up, and the one cross-reference that moved was corrected in
place.

1. **Boot ritual via /session-open** — the sweep still expects RED, now
   in a named-category shape, and the two rows are static.
2. **CL-24 residue cleanup** — the only part left, the operator's own
   owner-role act, now unblocked.
3. **D2.2a pre-flight implementing artefact** — sequenced after item 2.
4. **Permission-tiering follow-through** — three parts still open.
5. **Corpus listing for SG-07/SG-08/SG-09.**
6. **ci-docs paths-filter gap on corpus markdown** — the sibling gap in
   ci-devops closed at PR #96; this one remains.
7. **Lint invocation defects, two of opposite polarity.**
8. **Check-method defect family** — pattern-level ruling owed, and now
   the most-instanced open item in the queue, with three more added this
   arc.
9. **Batch-2 panel circulation** — scope decision owed.
10. **Ceremony frontmatter harmonisation.**
11. **PRs #64/#65 standing tree verification.**
12. **Operator inclusion decision for TY-03..09.**
13. **CL-25 / inc4 pin writer** — sharper since this arc.
14. **Governance-guard deny path for history rewrites** — unexercised.
15. **Consistency reads owed when their targets are drafted.**
16. **`corpus_edges_check.py` design-mode false green.**
17. **Statute-edge width.**
18. **TOR errata.**
19. **Gemini architecture-review return.**
20. **Packaging declarations are unasserted.**
21. **`.sql` ungoverned in `.gitattributes`** — new this arc.
