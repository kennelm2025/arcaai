# SESSION HANDOVER — ArcaAI 2026-08-11 (DEC-0015 / D2.0 arc)

*Covers one session: the arc named at the 2026-08-10c close — DEC-0015
authoring paired with the D2.0 commissioning frame, landed at PR #86.
**Supersedes the boot line of**
`docs/governance/SESSION_HANDOVER_2026-08-10c.md`, which is retained as
the record of the SG-09 and TOR panel-pass arcs. Authored on explicit
operator command from the ruled close summary; the `CLAUDE.md` queue
block was updated as its own step of the close ceremony and rides the
same PR as this file, per the 30 Jul pattern.*

## Boot line (next session)

> Resume ArcaAI — B7 in progress. HEAD main `1c98205` (PR #86 merge),
> clean, identical to origin/main; the handover PR carrying this file
> advances it. Boot ritual: conda arcaai → main → `git pull --ff-only`
> → `git fetch --prune` → `python scripts/repo_manifest.py --out
> D:/Downloads` (writes outside the tree; the file is gitignored, there
> is no committed snapshot) → Divergences read, **expect zero**. The
> DEC-0015 divergence that stood by construction across the 10c and 11
> arcs cleared when the ledger entry landed, so the carve-out is gone
> and **any** divergence is now a genuine stop → Docker Desktop up →
> `scripts/dev_up.cmd` → `python scripts/rehash_sweep.py` — expected
> green at "0 pins" until CL-25 lands a writer. **Retrieval remains
> blocked, and the block now reaches a committed governance document**:
> the ONNX cache ACL fault is confirmed live and must be repaired
> before any `--live` retrieval act, and the D2.0 commissioning frame
> merged at PR #86 makes a green pre-flight — non-elevation and cache
> traversal among its four assertions — an entry criterion. The cache
> traversal check still cannot be trusted to tell you otherwise: it has
> no implementing artefact at all, so making it assert non-elevation is
> an authoring job, not a fix, and the artefact arrives at the D2.2a
> pre-flight. Stub-flag runs are unaffected. **Ruled sequencing: the
> ONNX ACL repair comes ahead of the D2.0 frame ruling.**

## What landed (all on main)

1. **PR #86 merged (`1c98205`) — DEC-0015 and the D2.0 commissioning
   frame.** Two files, +66 / -0, two commits, neither carrying a
   `Co-Authored-By` trailer.
   - `cffafe0` — DEC-0015 appended to `DECISIONS.md`, +3.
   - `7b07dbd` — `docs/governance/D2.0_COMMISSIONING_FRAME_2026-08-11.md`
     created, +63.
2. The close branch carries `229b5d8`, the `CLAUDE.md` queue update, and
   rides the same PR as this handover.

## The arc

One arc, two paired governed acts, executed in sequence rather than
chained: the ledger entry first, then the frame that cites it.

- **DEC-0015 — test capability harness register home.** Discharges TOR
  Ruling 1 (OQ1) and consumes the number that two ruled documents —
  `docs/governance/TOR_test-capability_RevC_RULED_2026-08-10.md` and
  `docs/governance/RULINGS_RECORD_2026-08-10_TOR-test-capability.md` —
  already cited forward. Authored as a ledger bullet in `DECISIONS.md` on
  the DEC-0014 house style, not as a standalone document: at +3 lines it
  cannot carry the TOR and rulings-record content inline, and does not
  try to — it establishes the register home and binds that content **by
  citation**. What the entry fixes in the ledger: the
  capability under the existing register structure with **no new
  workstream ID**, WS-T deliverable naming, all four rulings with OQ3's
  divergent panel position recorded as divergent, the nine amendments as
  binding on D1.1 and D2.1, the two-regime admissibility rule, the
  reproducibility triple, defect routing, and the panel composition
  including the reason Gemini is not counted as a reviewer of this TOR.
- **D2.0 commissioning frame.** Authored per TOR Section 5A Regime 1 and
  held to one page by rulings-record amendment 8: session objective,
  entry criteria, exit criteria, records rule, admissibility rule, and
  nothing else. Defect routing was deliberately excluded — amendment 9
  assigns it to the Test Plan's formal-execution pack, and admitting it
  here is exactly how the page would have started growing into the
  miniature Test Plan the amendment exists to prevent.
- **The frame merged unruled, by design.** Section 5A reserves the
  commissioning frame to the operator's direct ruling, so it carries
  `Status: awaiting operator ruling` and nothing executes under it until
  that ruling happens. Its scope is written as the D2.2a spike session,
  with extension to any further commissioning session stated as an
  operator ruling rather than assumed — the literal reading of Section
  5A's "frame per commissioning session". Both decisions were left open
  deliberately in the text rather than resolved by the build agent.

### The placement trap, caught before mutation

The arc was commanded as a 0015-numbered document under `decisions/`.
Read against `scripts/repo_manifest.py` before any file was written,
that path fails twice over:

- The script states in terms that for ADR "the filesystem IS the
  register": it globs the `decisions/` directory and reads the leading
  four digits off each filename. A file numbered 0015 there would have
  set ADR highest to 0015, consuming ADR-0011 through 0014 — including
  the number reserved for the Agentic Topology work — and taking 0015
  itself.
- The DEC ledger is parsed from `DECISIONS.md` alone, while DEC
  citations are scanned across the `docs` and `decisions` trees. A file
  under `decisions/` would therefore have added DEC-0015 to the cited
  set and not to the ledger set, leaving the orphan-DEC divergence
  standing — the very thing the arc existed to clear.

Ruled to the ledger. Recorded inside the DEC-0015 entry as considered
and rejected, on the house principle that the intuitive wrong answer
gets written down because it will be proposed again.

## Verification battery

- **PR content, merge-base to HEAD:** `DECISIONS.md` +3;
  `D2.0_COMMISSIONING_FRAME_2026-08-11.md` +63. Two files, 66
  insertions. Not empty. The working-tree `git diff --stat` read empty
  at close, which is the healthy state once both acts are committed and
  merged, not evidence the act did not happen — the distinction
  `/pr-prep` exists to force.
- **Queue update:** `CLAUDE.md` +133 / -120, by scripted write rather
  than a markdown-aware editor. Bytes outside the QUEUE-START /
  QUEUE-END markers asserted unchanged at 13873 by the replacement
  script on both of its runs.
- **`python scripts/check_docs.py .`** — `No findings` across 106 files at
  close, this handover being the 106th. Run repeatedly across the arc.
  **Two intermediate reds, both recorded rather than quietly fixed.**
  *Red 1:* the first queue write reported an unbalanced bold span at 115
  marker occurrences, an odd count, caused by a third literal `docs` glob
  in the queue prose where the pre-existing text happened to carry
  exactly two and was even by luck. Fixed by writing the glob as prose,
  per the 30 Jul precedent recorded at item 1 of
  `docs/governance/RULINGS_RECORD_2026-08-04.md`. *Red 2:* this handover
  file then failed on an unbalanced bold span at 95 marker occurrences
  together with a dead-path citation of the rejected `decisions/`
  filename — **created by the act of recording red 1**. That is the
  self-inflicting shape, and this is its second instance: the 10c
  correction note re-created its own divergence by quoting it, and the
  note's first attempt did so twice. **General rule, stated here because
  two instances make it a pattern and not a coincidence: a defect is
  recorded as a prose description, never as a live reproduction, because
  quoting a defect verbatim can reconstitute it.** Both reds fixed;
  re-run green.
- **Lint:** `scripts/lint.cmd` by absolute path under PowerShell exits 0
  with "All checks passed!", and a bare `ruff check .` exits 0
  independently. No Python changed in this arc.
- **`python scripts/rehash_sweep.py`** at boot — 6 manifest versions in
  git history, 0 pinned `corpus_version` rows, all pins verified.
- **CI, stated as verified fact.** Path-filtering held on the
  `pull_request` event: ci-docs run **#92** fired on `7b07dbd` for
  branch `dec-0015-d2-0-frame` and concluded success in 7s. On the push
  to main at `1c98205`, ci-docs **#93**, ci-mlops **#135** and
  ci-devops **#130** all fired and all concluded **success** —
  confirmed by run query before this handover was authored, not
  inferred.

## Open verifications carried forward

1. **The D2.0 frame is merged unruled, and two decisions travel with
   it.** The ruling itself, which flips the status line; and its scope,
   currently written as D2.2a-session-only with extension stated as an
   operator ruling. Both now need a fresh branch, the authoring PR
   having merged. Nothing executes under the frame until it is ruled.
2. **The ONNX findings have escalated from parked to blocking a
   committed document.** The ACL fault is confirmed live; the frame
   requires a green pre-flight; the machine therefore fails the entry
   criteria of a governance document now on main. The implementing
   artefact for the traversal check arrives at the D2.2a pre-flight,
   which is also where the next free CL number is claimed.
3. **Three false-green defects are on the books, and they are a family
   rather than three coincidences.** The ONNX cache traversal check
   (green under an elevated shell); `corpus_edges_check.py` in design
   mode (prints its full success line having read no authored document,
   because `--docs` defaults to none and the loop never runs); and the
   lint invocation defect newly observed this arc. Each is a check whose
   success message claims more than it verified. Treating them as one
   family is the point: the shared fix is that a success line must state
   what it actually checked.
4. **A general direction-of-failure, of which the placement trap is one
   instance.** Where a register's authority is the filesystem, an
   artefact's *name* consumes register numbers regardless of what the
   act intended — no ledger line is written, no confirmation gate fires,
   and the consumption is silent. The DEC-into-`decisions/` case is the
   instance caught this arc; the general rule is that any artefact whose
   filename encodes a register number must be checked against which
   register actually reads that filename before it is written. Correct
   direction of caution: verify the scanner, not the convention.
5. **Carried unchanged and untouched by this arc:** PRs #64/#65 standing
   tree verification; the corpus listing debt at three documents
   (SG-07, SG-08, SG-09), with the pin unmoved and eligible at 16; and
   the batch-2 panel circulation scope question.
6. **New, parked — push-event CI triggering on docs-only merges.** The
   merge at `1c98205` changed two markdown files and nothing else, yet
   ci-mlops **#135** and ci-devops **#130** both fired on the push to
   main and ran to success, while on the `pull_request` event their
   paths filters correctly excluded them and only ci-docs ran. The
   asymmetry between push-event and pull-request-event filtering is
   recorded as an observation with its evidence runs; no cost was
   incurred beyond wasted CI minutes and nothing is claimed about the
   cause. Parked, not raised.

## Registers at close

DEC next **0016** · ADR next **0011** · CL next **26** (15 open) · WS-E
next **64**. Derived from `scripts/repo_manifest.py` regenerated in this
session at boot, after the act, post-merge, and again at close — every
run agreeing. **One number was consumed: DEC-0015.** ADR next 0011 is
unmoved and deliberately so; it was within one command of being consumed
by accident (open verification 4). B7 ENTERED, exit evidence open,
unchanged.

**Divergences: zero.** The first clean reading since the 10c arc created
its own expected divergence by design. The boot line above no longer
carries a carve-out, which means the next session's divergence check is
once again a plain stop condition.

## Return queue, in order

Enumerates the `CLAUDE.md` queue block committed at `229b5d8`, item for
item and in its order, so the two agree by construction rather than by
assertion.

1. **Boot ritual via /session-open** (incl. rehash sweep; expect 0 pins,
   expect **0** divergences).
2. **Parked elevated-session findings** — the ONNX cache ACL repair, the
   elevated-harness-shell breach, and the false-green traversal check.
   **Ruled ahead of the frame ruling.** Blocks `--live` retrieval and now
   also blocks satisfying the entry criteria of a committed document.
3. **Rule the D2.0 commissioning frame**, and with it the scope
   question (D2.2a-session-only, or standing for the commissioning
   regime). Own branch; the status line flips as part of the ruling.
4. **D2.1 spec schema v0.1 — the keystone.** Next in the TOR's
   proof-first sequencing after the frame: both scenario classes from
   v0.1, carrying rulings-record amendments 3, 5 and 6 from the start.
   The D2.2a runner spike follows, and is where the first real test
   result lands and where the pre-flight artefact is authored.
5. **Corpus listing for SG-07/SG-08/SG-09** — one act or per document,
   operator's decision. Note the interaction with the harness:
   commissioning runs pin the snapshot current at spike time and do not
   wait on this act, but Regime-2 formal runs use listed snapshots only.
6. **ci-docs paths-filter fix** — one line. This is the pre-existing and
   separately evidenced defect: ci-docs cannot fire on corpus markdown at
   PR time, because the root-level glob does not reach it, and PR #86
   isolated that conclusively by exercising both covered path classes in
   a single run. **Distinct from open verification 6**, which parks a
   different observation entirely — the push-event triggering of ci-mlops
   and ci-devops on a docs-only merge. Different workflows, different
   events, different defects; neither is evidence for the other. Whether
   this one also warrants a WS-E ledger entry or a CL item is an operator
   decision.
7. **Lint invocation defects — two, of opposite polarity.** The carried
   relative-path false red, and the false green newly observed this arc
   where `cmd /c` by absolute path from the Bash tool exits 0 without
   running ruff at all.
8. **Batch-2 panel circulation** — unblocked; open whether SG-03..SG-06
   sit inside it.
9. **Conventions owed in `CLAUDE.md` at its next revision** — the
   commit-trailer rule, the register-number citation rule, and the DEC
   placement rule, written once together rather than accreting.
10. **PRs #64/#65 standing tree verification** — partially chipped, not
    discharged; the MANIFEST.yaml side of #64 and the rest of #65 are
    still owed a look.
11. **Operator inclusion decision for TY-03..09** when ready; the next
    ingest then populates processing fields at a .8 version.
12. **CL-25 / inc4** (pin writer) pending agent module; **CL-24** when
    convenient.
13. **Governance-guard deny path for history rewrites** — the one
    documented category still unexercised; needs a throwaway clone, not
    this working tree.
14. **Consistency reads owed** when their targets are drafted — SG-07
    §2.2 and §5.2, SG-08 §2.3 and §5.2.
15. **`corpus_edges_check.py` design-mode false green** — minimum fix is
    wording, not logic.
16. **Statute-edge width** — the corpus holds POCA s.327 and s.330 and no
    text of the disclosure-regime provisions they depend on by reference.
    A property of the corpus rather than of any one document, and it will
    recur.
17. **TOR errata** carried to the Test Plan (D1.1), including the
    correction owed to the panel record for the propagated
    "23-document corpus" phrasing.
18. **Gemini consolidation before the Agentic Topology ADR work opens**,
    which would consume ADR next 0011.
19. **Housekeeping, non-blocking** — stale local branches from past arcs
    remain after their merges.

The ordering above is the committed block's ordering, item for item,
including the ruled sequencing of the ONNX repair ahead of the frame
ruling. No correction is flagged against the block because none is owed.
