# SESSION HANDOVER — ArcaAI 2026-08-08b (SG-07 arc)

*Second handover of 2026-08-08. **Supersedes the boot line of
`docs/governance/SESSION_HANDOVER_2026-08-08.md`**, which is retained
as the record of the morning's harness work; this file carries the
full day, PRs #70-#74. The rehash sweep that handover recorded as OWED
was run this session and is discharged. Commit via handover PR per the
30 Jul pattern.*

## Boot line (next session)

> Resume ArcaAI — B7 in progress. HEAD main `26f57ef` (PR #74 merge),
> clean, identical to origin/main; the handover PR carrying this file
> advances it. Boot ritual: conda arcaai → main → `git pull --ff-only`
> → `git fetch --prune` → `python scripts/repo_manifest.py --out
> D:/Downloads` (writes outside the tree; the file is gitignored,
> there is no committed snapshot) → Divergences read → Docker Desktop
> up → `scripts/dev_up.cmd` → `python scripts/rehash_sweep.py` —
> expected green at "0 pins" until CL-25 lands a writer. **Retrieval is
> blocked**: the ONNX cache ACL fault is confirmed live and must be
> repaired before any `--live` retrieval act, and the ONNX cache
> traversal check cannot be trusted to tell you otherwise until it
> asserts non-elevation. Stub-flag runs are unaffected. No open CI
> verifications carry in; CI on PR #74 was not read before merge.

## What landed today (all on main)

The morning's four items are recorded in full in the superseded
handover and are summarised here only to carry the day.

1. **Guard verification — all four documented deny/confirm categories
   exercised.** Two findings: the PowerShell recursive-delete rule is
   separate from the POSIX one, and the guard matches the inner command
   string through a `powershell -Command` wrapper, so wrapping does not
   evade it.
2. **PR #71 merged (`ed5f8b0`) — harness repair, 4 commits, 7 files,
   +83/-20.** Ruff I001 autofix in the governance guard, the `.claude/`
   entry in the ci-devops PR paths filter, WS-E 62, and step-1
   corrections to three ceremony skills. PR #70 (`a97d44d`) is the
   merge whose ci-devops failure evidenced WS-E 62.
3. **WS-E 62 minted and appended** — CI paths-filter coverage gap,
   third recurrence of the WS-E 45 pattern (`docs/`, then `scripts/`,
   now `.claude/`). Append-only compliance verified: inserted after
   item 61, sequence 59-60-61-62 unbroken, no existing item touched.
   **Structurally closed, not proven in flight** — the presenting
   symptom is evidenced closed (ci-devops failure 1m39s at `a97d44d` →
   success 2m43s at `ed5f8b0`), but the post-merge run fires on the
   unfiltered push-to-main trigger and does not exercise the
   pull_request paths filter. Read as symptom closed, remediation
   configured-and-parsed but unproven. Unchanged by this session.
4. **Three ceremony-skill stale-source defects fixed** (PR #71), all
   self-caught, zero damage, recorded as notes-for-the-record by
   ruling rather than as ledger items. Common root cause: a sound rule
   applied past its precondition. The `/ledger-touch` defect was the
   dangerous one — literal compliance during the WS-E 62 append itself
   would have written entry 59 over live items 59-61.
5. **PR #72 merged (`54d2423`)** — the morning handover committed.
6. **PR #73 merged (`e8d1a5e`) — the render-abort class fix.** All five
   ceremony skills audited and their renders made failure-tolerant: a
   `!` render exiting non-zero previously aborted the whole skill
   before a word of its task text was read, so a shell error destroyed
   the ceremony silently and produced not even a diagnosis. Renders now
   fall back to a marker line and are labelled OPTIONAL or
   LOAD-BEARING, so the task text decides what a failure means. **This
   class is owed a WS-E entry** — see the return queue.
7. **PR #74 merged (`26f57ef`) — the SG-07 arc.** Detail below.

## The SG-07 arc

One document-arc, scoped to authoring only.
`verticals/fraud/corpus/documents/SYN-SG-07.md` created — *SG-07 —
Sector Guidance: Automated Fraud Detection Systems*, 1,766 words, 205
lines, commit `edde09b`. Listing in `verticals/fraud/corpus/MANIFEST.yaml`
was deliberately **not** done: authoring and listing are separate
governed acts.

The v0.2 skeleton is a coordinator artefact and is not in the repo by
design; its SG-07 row was supplied by the operator this session and
agreed with the `verticals/fraud/corpus/EDGES.yaml` v0.2.2 minimum set
on all five edges.

**Four rulings taken in-arc:**

1. **No statute citation.** SG-03 owns the s.330(2)(b) hook; SG-07
   points at SG-03 §5.1 rather than re-citing OGL-0004. Realistic
   guidance-to-guidance drafting, and it keeps the panel diff clean.
2. **TR-05 and DL-06 characterised by series role only** — thematic
   review and Chief Executive letter — since neither is authored, per
   the SG-05 precedent for CV-03 and DP-04.
3. **No trim.** SG-07 stands at 1,766 words against its ~1,700
   allocation — the first SG to land on its allocation rather than
   under it (SG-03 1,263/1,600; SG-04 1,289/1,400; SG-05 1,219/1,500;
   SG-06 1,172/1,200). It is the longest document in the series;
   length is panel territory if the panel raises it.
4. **Series title form** — `SG-07 — Sector Guidance: Automated Fraud
   Detection Systems` — over the skeleton row's tabular shorthand.

**Battery.** `scripts/corpus_edges_check.py` exit 0, `OK: closure,
asymmetry, immutability, and authored-doc checks pass`; 38 documents /
155 edges, unchanged, the design file being untouched. That check
carries marker byte-exactness, the five minimums present in prose,
absence of placeholders, and register legality. All five minimums
land: SG-01 (§1.3, §3.4, §6.1), TY-02 (§3.1-3.3), TR-05 (§2.2), TY-09
(§4.2, §5.3), DL-06 (§5.2). One reported extra, SG-03, register-legal
and predicted at outline stage; no firm-register document cited.
`scripts/check_docs.py` exit 0 at 99 files; `scripts/lint.cmd` exit 0
(parity only, no Python changed).

## Elevated-session findings (parked, blocking for retrieval)

1. **ONNX cache ACL fault — confirmed live.** Repair before any
   `--live` retrieval act. Stub-flag runs are unaffected.
2. **Elevated-harness-shell breach** — recorded.
3. **The ONNX cache traversal check returns green under an elevated
   shell — a false-green defect.** The check must assert non-elevation
   before its result is trusted as the standing first act again. Note
   the ordering trap: the defective check is the instrument the
   standing first act relies on, so fixing the check precedes trusting
   any future green from it.

These are the same shape as the three ceremony defects of the morning —
a check whose green cannot mean what it is read to mean — and the
render-abort class fix of PR #73 is a third instance of the family.

## Registers at close

DEC next 0015 · ADR next 0011 · CL next 26 (15 open; none raised this
session) · WS-E next **63**. Derived from an in-session
`scripts/repo_manifest.py` regeneration at boot (13:41 UTC) and
re-derived at close (14:09 UTC, HEAD `26f57ef`) — both agreed, and no
number was consumed by the SG-07 arc. B7 ENTERED, exit evidence open;
unchanged by this session. Two hygiene divergences under
`docs/reviews/2026-06-arch-review/` remain untouched.

## Return queue, in order

1. **Boot ritual via /session-open** (incl. rehash sweep; expect 0
   pins).
2. **Elevated-session findings — blocking for retrieval.** ACL fault
   repair; the shell breach; the false-green check fixed to assert
   non-elevation.
3. **WS-E entry for the render-abort class** — ruled, one entry for the
   class, owed at the next non-corpus session via /ledger-touch. The
   number comes from that session's own manifest regeneration under the
   sequence-hold rule; 63 was next as at this close.
4. **Batch-2 authoring — SG-08 next**, then SG-09. One document-arc per
   session.
5. **PRs #64/#65 standing tree verification — partially chipped, not
   discharged.** See below.
6. **Operator inclusion decision for TY-03..09** when ready.
7. **CL-25 / inc4** (pin writer) pending the agent module; **CL-24**
   when convenient.
8. **History-rewrite deny path test** — the one guard category
   unexercised. Needs a throwaway clone.
9. **TR-05 / DL-06 consistency reads** when those documents are
   drafted, against SG-07 §2.2 and §5.2.
10. **Commit-trailer convention** — ruled: no `Co-Authored-By` trailer
    on corpus authoring commits. Owed as a standing rule in `CLAUDE.md`
    at its next revision.

The `CLAUDE.md` queue block was rewritten to this order and rides this
handover PR. Queue items 6 and 7 of the superseded handover — the
history-rewrite test and the clean `.claude/` filter test — are carried:
the first as item 8 above, the second as an open CI verification, since
no PR since #71 has touched only files under `.claude/`.

## Unchanged / carried

Corpus pins unchanged from `.6` (snapshot `e671292d`, manifest_sha
`6a1371fc`, eligible 16), with the standing WS-E 61 caveat that this
pin has no DB row until CL-25. SG-07 is authored but **not listed**, so
the manifest is unmoved and eligible remains 16. B7 exit items
(grounding, negative, fallback, RAGAS) untouched.

**PRs #64/#65 — chipped, not discharged.** This session read
`verticals/fraud/corpus/EDGES.yaml` at v0.2.2 in full and confirms it
against the record: the v0.2.2 header note, CV-01 into TY-04's minimums
and TR-01 into TY-07's, the declined SG-01/SG-02 promotion with its
dissent, and the SG-07 row. The manifest-history job also ran live on
PR #74. That leaves the `verticals/fraud/corpus/MANIFEST.yaml` side of
#64 and the remainder of #65 (`scripts/manifest_history_check.py` read
directly) still owed a look. Chipping is not discharge.

## Observations parked

- **CI on PR #74 was not read before merge.** ci-docs and ci-mlops both
  have filters covering a corpus document; the manifest-history job
  running live is partial evidence, not a check read.
- **Commit `edde09b` carries a `Co-Authored-By` trailer**, which the
  ruling now forbids for corpus authoring commits. The ruling is
  prospective and the commit is merged; amending merged history is not
  available and is not sought. Recorded as a one-off exception.
- **Stale local branches** — the backlog noted in the superseded
  handover is unchanged; `sg-07-2026-08-08` and `handover-2026-08-08b`
  join it unless deleted after merge.
- **The one-day handover gap for PRs #67-#70** (2026-08-07) is
  unresolved and carried from the superseded handover.
