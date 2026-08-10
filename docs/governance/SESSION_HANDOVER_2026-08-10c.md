# SESSION HANDOVER — ArcaAI 2026-08-10c (TOR panel-pass arc)

*Covers **two** sessions: 10b (the SG-09 arc, PRs #81/#82) and 10c (the
TOR panel-pass arc, PR #83). **Supersedes the boot line of
`docs/governance/SESSION_HANDOVER_2026-08-10.md`**, which is retained as
the record of the WS-E 63 arc. The 10b close updated the `CLAUDE.md`
queue but authored no handover, so that session had no narrative record
until this file; closing that gap is why this handover carries two
sessions rather than one. Commit via handover PR per the 30 Jul
pattern.*

## Boot line (next session)

> Resume ArcaAI — B7 in progress. HEAD main `148ba27` (PR #83 merge),
> clean, identical to origin/main; the handover PR carrying this file
> advances it. Boot ritual: conda arcaai → main → `git pull --ff-only`
> → `git fetch --prune` → `python scripts/repo_manifest.py --out
> D:/Downloads` (writes outside the tree; the file is gitignored, there
> is no committed snapshot) → Divergences read, **expect exactly one and
> expect it to be this one**: *DEC — cited but above the DECISIONS.md
> high-water mark: DEC-0015. Ledger entry missing.* It is the 10c arc's
> own footprint, it is correct, and it clears when DEC-0015 is authored;
> any **other** divergence is a genuine stop → Docker Desktop up →
> `scripts/dev_up.cmd` → `python scripts/rehash_sweep.py` — expected
> green at "0 pins" until CL-25 lands a writer. **Retrieval remains
> blocked**: the ONNX cache ACL fault is confirmed live and must be
> repaired before any `--live` retrieval act, and the ONNX cache
> traversal check cannot be trusted to tell you otherwise — it has no
> implementing artefact at all, so making it assert non-elevation is an
> authoring job, not a fix. Stub-flag runs are unaffected. Next arc is
> already named: DEC-0015 authoring paired with the D2.0 commissioning
> frame.

## What landed across both sessions (all on main)

1. **PR #81 merged (`66041e5`, 11:28 UTC) — SG-09 authored.** One file,
   `verticals/fraud/corpus/documents/SYN-SG-09.md`, +234 / -0. Batch-2
   authoring **complete at 7/7**.
2. **PR #82 merged (`bc607d4`, 11:40 UTC) — `CLAUDE.md` queue updated**
   at the 10b close. One file. No handover accompanied it.
3. **PR #83 merged (`148ba27`, 11:54 UTC) — TOR panel-pass artefacts.**
   Two files, +246 / -0. The 10c arc. Detail below.

## The SG-09 arc (session 10b)

One document-arc, closing batch 2. SG-09 — *Sector Guidance: Account
Restriction and Exit Where Criminal Property Is Suspected*. Recorded
here from the repository record and the queue block that session wrote;
this handover is retrospective for 10b and does not claim in-session
observation of it.

- **Batch 2 complete at 7/7**: SG-03/SG-04 (PR #67), SG-05/SG-06 (PR
  #68, AO-2 discharged in SG-05), SG-07 (PR #74), SG-08 (PR #80), SG-09
  (PR #81). No SG authoring remains.
- **Citation quality, and the reason it matters.** All three of SG-09's
  minimum targets (DP-01, SG-06, OGL-0003) were already authored, so
  every citation landed by pinpoint rather than by series role, and the
  ruled-in extra (TY-04) was read in full before drafting to keep it
  that way. SG-09 is the first batch-2 document to add **nothing** to
  the consistency-read debt.
- **Ruled in-arc: SG-09 lands as a leaf in the authored subgraph.** Its
  only design inbound is `DL-05: [SG-09, SG-06]`, and DL-05 is
  unauthored, so no authored document cites SG-09. Not a check failure —
  closure runs against the design file, not prose — but it is precisely
  the condition the v0.2.1 closure repair exists to prevent at design
  level, and it was ruled into the circulation pack as a stated
  condition rather than left implicit.
- **Ruled in-arc: panel circulation is a batch-level act, not a
  per-document precondition**, on the evidence of the SG-05/SG-06 and
  SG-07 arcs. Batch end has now arrived, so the circulation is unblocked.
- **Statute-edge width stated on the face of the document.** SG-09 §1.2
  states the boundary rather than papering it, per the SG-08 §1.2
  pattern.
- **Defect observed live: `scripts/corpus_edges_check.py` design-mode
  false green.** Run without `--docs` it reports closure, asymmetry,
  immutability and authored-doc checks passing having read no authored
  document at all. The docs-mode re-run is what actually evidenced
  SG-09.

## The TOR panel-pass arc (session 10c)

One governed act, off-queue and operator-directed: entry of the TOR
panel-pass artefacts into `docs/governance/`.

- `docs/governance/RULINGS_RECORD_2026-08-10_TOR-test-capability.md`
- `docs/governance/TOR_test-capability_RevC_RULED_2026-08-10.md`

**The TOR enters the repo at Rev C RULED as a ruled coordinator
artefact. The Gmail draft is superseded as the working copy from
`99b63cd` forward.** Panel pass: three reviewers (Grok, ChatGPT,
DeepSeek), ACCEPT WITH AMENDMENTS. Composition is recorded in the
rulings record itself, including the prior-familiarity annotation on
Grok and ChatGPT's return to the bench after withdrawal from the batch-1
corpus panel. Four operator rulings — OQ1 register home (DEC-0015, no
new workstream ID); OQ2 confirmed as resolved at Rev B; OQ3
preferred-primary on the B7 evidence relationship, the panel's one
divergent point; OQ4 the D2.6 pre-migration baseline a formal hard
precondition to serving-layer cutover. OQ5 deferred. Nine amendments
accepted onto D1.1/D2.1, none amending TOR text. Reviewer outcomes
phrased as rulings are recorded as concurrence only.

**Hash-pinned round trip, verified three times.** Both artefacts were
verified in full at the session boundary before anything entered the
tree, re-hashed in place after copy, and re-hashed again on main after
merge:

| Artefact | SHA256 |
| --- | --- |
| Rulings record | `d00974ef62f540b0c216465510721464a4925e8c68f352a553ca06109938b30f` |
| TOR Rev C RULED | `83b3fabe0da68ae2af3517ded25723084e8507c5f5834cf28f0891e750f6da2c` |

Both digests unchanged at all three points. The sources were pure LF at
origin (0 CR bytes), so the copy was byte-exact and no conversion was
needed — which is why the pinned identity survived git's checkout
filters intact. The digests recorded in `99b63cd` and in the PR #83 body
therefore remain citable against the working tree, not merely against
the transfer.

**Errata recorded, not amended.** Two defects were found in the TOR
while reading it before commit. The TOR is committed as ruled at Rev C
and is immutable as committed, so both are recorded in the PR #83 body
at the point the error entered the repo, and both carry forward:

1. §2 and §7 cite PR #80 for batch-2 completion; batch 2 completed at PR
   #81. Operator's note for the record: the claim was **wrong at the
   moment of writing**, not merely stale — batch 2 stood at 6/7 when Rev
   B was drafted and SG-09 did not yet exist. Coordinator defect.
2. §2's authored count should read **30 of 54**. The parenthetical
   enumeration (16 + TY-03..09 + SG-03..09) is the correct one; 23
   belongs to the listing pipeline, not to authoring — 16 currently
   listed/eligible → 23 after the batch-1 listing act → 30 after
   batch-2's. The TOR text conflated authored-on-disk with
   eligible-listed. This propagated outward: Reviewer B's "23-document
   corpus" phrasing derives from it, which makes the correction owed to
   the panel record and not only to the TOR.

For the record on the drafting: the build agent's first reading of
erratum 2 was backwards — it inferred the parenthetical was the loose
element and the 23 sound. The operator corrected it before the PR body
was written, and the corrected form is what landed.

**ci-docs control case.** PR #83 touched two files under `docs/` and
ci-docs **fired on the `pull_request` event**, passing in 16s. This is
the first clean control case for the paths-filter gap: the filter works
for covered paths, so the defect is isolated to the root-only `*.md`
glob failing to reach corpus markdown, not to ci-docs triggering
generally. All three workflows ran green post-merge on main.

**Third no-trailer instance, first outside corpus.** `99b63cd` carries
no `Co-Authored-By` trailer, asserted by trailer-count query rather than
by eyeball, on the ground that the build agent authored no part of
either document. The 2026-08-10 ruling's stated terms reach
corpus-authoring commits, so the practice now runs ahead of the rule on
two axes — non-corpus commits, and PR bodies (the generated-with footer
was omitted from #80, #81 and #83). The rule gets written once,
properly, at the next `CLAUDE.md` revision rather than accreting.

## Open verifications carried forward

1. **One divergence stands, by construction.** DEC-0015 is cited in two
   committed documents and has no `DECISIONS.md` entry. Expected at next
   boot; clears when DEC-0015 is authored. Written into queue item 1 so
   it is not read as a stop.
2. **Two register numbers are spoken for but unheld.** DEC-0015 (TOR
   Ruling 1) and CL-26 (flagged in the TOR as the runner pre-flight
   candidate). Both match the live anchor today, but the sequence-hold
   rule means a competing act takes them. This is the reason the next
   arc is what it is.
3. **The render-abort fix remains unproven in flight.** No render exited
   non-zero across either session; the marker-line fallback has still
   never been triggered.
4. **The ONNX cache traversal check still has no implementing
   artefact.** Unchanged. Note the TOR's D2.2a pre-flight is specified
   to *be* that artefact, which is how this debt finally discharges.
5. **PRs #64/#65 standing tree verification** — untouched by both
   sessions, carried unchanged.
6. **Corpus listing debt now three documents deep** (SG-07, SG-08,
   SG-09), none listed in `verticals/fraud/corpus/MANIFEST.yaml`. The
   corpus pin is unmoved and eligible remains 16.

## Registers at close

DEC next **0015** · ADR next **0011** · CL next **26** (15 open) · WS-E
next **64**. Derived from `scripts/repo_manifest.py` regenerated in
session 10c at boot (11:43 UTC, HEAD `00f7dc2`) and again at close
(12:01 UTC, HEAD `148ba27`) — both agreed on every number. **No number
was consumed by either session**: SG-09 is a corpus document, and the
TOR act appended to no register. B7 ENTERED, exit evidence open,
unchanged. **Divergences: one**, as above — the first non-zero reading
since PR #76 cleared the series, and it is self-inflicted by design
rather than drift.

## Return queue, in order

1. **Boot ritual via /session-open** (incl. rehash sweep; expect 0 pins,
   expect the one DEC-0015 divergence).
2. **DEC-0015 authoring paired with the D2.0 commissioning frame — the
   named next arc.** Small, paired, and it claims the DEC number while
   the TOR's ink is wet. Authoring it also clears the boot divergence.
   The D2.0 frame is held to one page by ruled amendment 8: session
   objective, entry criteria, exit criteria, records rule, admissibility
   rule — nothing else.
3. **TOR errata carry to the Test Plan (D1.1)** and any future TOR
   revision, including the correction owed to the panel record for the
   propagated "23-document corpus" phrasing.
4. **Gemini consolidation before the Agentic Topology ADR work opens.**
   Gemini's architecture-review assessment of the orchestration / memory
   / dreaming document arrived in the same circulation as the TOR pass
   but reviews a different document; it is recorded as out of scope in
   the rulings record and stands as an unconsolidated two-reviewer
   return with Grok's. ADR-0011 is the next free ADR number and that
   work would consume it.
5. **CL-26 claimed at the D2.2a spike**, when the runner pre-flight is
   authored — the same act that gives the ONNX cache check its
   implementing artefact.
6. **Elevated-session findings — blocking for retrieval.** ACL fault
   repair; the shell breach; the false-green check.
7. **Corpus listing for SG-07/SG-08/SG-09** — one act or per document,
   operator's decision.
8. **Batch-2 panel circulation** — unblocked; open whether SG-03..SG-06
   sit inside it.
9. **ci-docs paths-filter fix** — one line; PR #83 supplies the control
   case. Whether it also warrants WS-E 64 or CL-26 is an operator
   decision.
10. **`corpus_edges_check.py` design-mode false green** — minimum fix is
    wording, not logic.
11. **PRs #64/#65 standing tree verification**, TY-03..09 inclusion
    decision, CL-25 / CL-24, history-rewrite deny-path test,
    consistency reads, commit-trailer standing rule — all carried
    unchanged.

The `CLAUDE.md` queue block was updated as its own step of the close
ceremony and rides the same PR as this handover, both authored on
explicit command.
