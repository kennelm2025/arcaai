# SESSION HANDOVER — ArcaAI 2026-08-11b (D2.0 ruling / ONNX root-cause arc)

*Covers one session: the arc named at the 2026-08-11b boot — rule the D2.0
commissioning frame — which the operator issued as a conditional ruling and
which therefore became, first, a diagnosis of the parked ONNX findings. Landed
at PR #88 and PR #89. **Supersedes the boot line of**
`docs/governance/SESSION_HANDOVER_2026-08-11.md`, which is retained as the
record of the DEC-0015 and D2.0 authoring arc. Authored on explicit operator
command at the following session's boot, as that session's own arc, together
with a queue correction owed from this arc's close — both acts riding one PR.
The `CLAUDE.md` queue block itself was updated and merged separately at PR #89,
a departure from the 30 Jul pattern where the queue update rides the handover
PR, and the direct cause of the chain break recorded at open verification 6.*

## Boot line (next session)

> Resume ArcaAI — B7 in progress. HEAD main `e2bb714` (PR #89 merge), clean,
> identical to origin/main; the handover PR carrying this file advances it.
> Boot ritual: conda arcaai → main → `git pull --ff-only` → `git fetch
> --prune` → `python scripts/repo_manifest.py --out D:/Downloads` (writes
> outside the tree; the file is gitignored, there is no committed snapshot) →
> Divergences read, **expect zero** — and zero is now a plain stop condition
> with no carve-out, held across PRs #86, #88 and #89 → Docker Desktop up →
> `scripts/dev_up.cmd` → `python scripts/rehash_sweep.py` — expected green at
> "0 pins" until CL-25 lands a writer. **Retrieval is no longer blocked.** The
> ONNX cache ACL fault is repaired and verified, so a `--live` retrieval act is
> no longer barred by it. **But the pre-flight still has no implementing
> artefact**: the four assertions were run by hand this arc and can only be run
> by hand again, so the D2.0 frame's entry criteria remain unmeetable by any
> command in the repo. The artefact arrives at the D2.2a pre-flight and claims
> the next free CL number there. **Standing rule, permanent: the harness never
> elevates** — any fix needing elevation is the operator's, at their own
> terminal, re-verified afterwards from a non-elevated shell.

## What landed (all on main)

1. **PR #88 merged (`21699d4`) — the D2.0 ruling and its evidence.** Two
   files, +187 / -4, two commits, neither carrying a `Co-Authored-By` trailer.
   - `8cc66b8` — `docs/governance/FINDINGS_2026-08-11_onnx-acl-root-cause.md`
     created, +170.
   - `a20a03b` — `docs/governance/D2.0_COMMISSIONING_FRAME_2026-08-11.md`
     amended, +17 / -4, preamble only.
2. **PR #89 merged (`e2bb714`) — the queue update.** `a59cd7e`, `CLAUDE.md`
   +80 / -53, queue block only.
3. **No register number was consumed by either.** DEC, ADR, CL and WS-E all
   close where they opened.
4. Riding the PR that carries this handover: the queue correction described in
   the closing note, `CLAUDE.md` +18 / -15, queue block only.

## The arc

Named as "rule the D2.0 commissioning frame". The operator returned a
**conditional** ruling: verify the four pre-flight assertions first, and if any
failed, stop without ruling and return to the ONNX item. That condition is what
the arc actually turned on, and it is the reason the session produced a
diagnosis before it produced a ruling.

### The pre-flight ran red, and the ruling correctly did not happen

Assertion 1 (non-elevation) was established first and deliberately alone,
because the recorded defect in the traversal check is that it returns green
under an elevated shell — a traversal result read before elevation is known is
worthless. It was corroborated by two independent methods rather than one, for
a reason recorded at open verification 4.

Assertion 2 then failed. Traversal into the extracted ONNX model directory was
denied outright from a shell positively established as non-elevated. Under the
operator's condition this was a stop: the frame was not ruled, no branch was
opened, and the status line was left untouched.

**The sequencing was vindicated by the result.** Had the frame been ruled
first, main would have carried a governance document whose entry criteria the
machine provably failed — the escalation the previous arc's queue had already
flagged, realised.

### Root cause: one incident, not two parked findings

The queue had carried an ONNX cache ACL fault and an elevated-harness-shell
breach as separate items across several arcs. They are cause and effect.

The extraction was performed by an elevated process, and the consequences were
asymmetric in a way that hid the fault. The parent cache directory was left
owned by the administrators group but carried an explicit entry granting the
normal user full control, so it listed and traversed normally. The extracted
child directory received an administrators-only access list with no entry for
the normal user and no effective inheritance — under the normal identity it
denied not merely read but the reading of its own security descriptor. So the
parent listed the child's name while the child denied everything about itself,
and any check stopping at the parent saw a well-formed cache.

The corpus index used by `scripts/b7_run.py` was created in the same interlude,
two seconds after the archive, and is likewise owned by the administrators
group. It stayed usable only because its inherited access list grants
authenticated users modify rights. **Same cause, different blast radius** — one
artefact was bricked for the normal user, the other kept working, so nothing
ever failed loudly enough to be noticed.

Repair was the operator's, at their own terminal: deletion of the extracted
directory. Re-extraction was then triggered from the ordinary harness shell by
exercising the warm-up path that `arcaai/platform/retrieval/chroma_store.py`
runs at adapter construction. The re-extraction was local, not fetched — the
archive's size, modification time and SHA256 were identical before and after.
The re-created directory is owned by the normal user, and access flows through
an owner-rights entry rather than a named user entry, which means access is
contingent on ownership not changing.

### The false-green mechanism, stated once

An elevated process bypasses the access list that caused this fault. The
traversal check therefore returned green exactly when run under the condition
that created the fault, and red only under the condition in which the system is
actually used. It did not merely fail to detect the fault; its green was
strongest where it was least meaningful. This is the failure class WS-E 63
records, and the reason TOR Section 5A bars commissioning results from ever
becoming gate evidence.

### The ruling, once the pre-flight was green

Ruled Option 1: status flipped to RULED with its pre-flight evidence stated on
the face of the document, scope held to the D2.2a session per Section 5A's
literal "frame per commissioning session", plus a re-adoption clause under two
mandatory constraints — an adoption ruling must name the specific session it
adopts for, so no adoption is open-ended or standing; and re-adoption holds
only while the frame text stands unamended, with silence on any amendment
meaning prior adoptions do not carry.

A standing-scope frame was considered and declined. It departs from ruled TOR
wording, and a deviation from a locked document needs a `DECISIONS.md` entry
before the change merges — so it would have consumed DEC next 0016 and made the
act two governed acts rather than one. Recorded here because the queue had
described it as a one-line change either way, which is true of the text and not
of the governance cost.

The frame's five parts were untouched; the change is preamble only and the
one-page limit under rulings-record amendment 8 holds at 541 words.

## Verification battery

- **`git diff --stat` first, throughout.** PR #88: frame +17 / -4, findings
  note +170. PR #89: `CLAUDE.md` +80 / -53, sole file changed. The queue
  correction riding this handover: `CLAUDE.md` +18 / -15.
- **Queue edit confinement asserted, not assumed.** For PR #89, all seven diff
  hunks were checked to fall inside the QUEUE-START and QUEUE-END markers and
  the numbering asserted contiguous 1..19 programmatically. For the correction
  riding this handover, the same checks plus the stronger one: bytes outside
  the markers asserted unchanged at 13891 by both length and MD5, before and
  after the edit.
- **`python scripts/check_docs.py .`** — `No findings` across 107 files, run on
  both PRs and again after the correction. No intermediate reds this arc.
- **Trailer count 0** on every commit, asserted by count rather than by
  eyeball, consistent with the practice recorded at queue item 9.
- **CI.** ci-docs `structural-checks` fired on the `pull_request` event and
  concluded success for both PRs — 7s on #88, 9s on #89.
- **`python scripts/rehash_sweep.py`** at boot — 6 manifest versions in git
  history, 0 pinned `corpus_version` rows, all pins verified.
- **Pre-flight, run twice.** Red on the first run at assertion 2; green on all
  four after the repair. Assertion 3 was upgraded from partial to green only
  once the vector store's persistence was actually evidenced — present,
  readable, and writable, all three, since the underlying database engine needs
  write access to serve reads. It was not upgraded on reachability alone.
- **Post-merge, both times.** Both PR #88 commits confirmed ancestors of
  origin/main by ancestry check rather than by reading the log; branches
  deleted, remotes pruned; manifest regenerated after each merge.

## Open verifications carried forward

1. **The pre-flight has no implementing artefact, and this arc did not author
   one.** That was deliberate — authoring it is a separate arc and it claims
   the next free CL number at D2.2a. The consequence to carry: this arc's green
   pre-flight is **not reproducible by any command in the repo**. It was
   assembled by hand, and the next session that needs one must assemble it by
   hand again.
2. **The corpus index remains owned by the administrators group**, usable only
   through an inherited grant to authenticated users. Recorded as a latent
   hazard and deliberately not repaired: repair needs elevation, and under the
   standing rule that is the operator's act, not the harness's.
3. **The check-method defect family stands at six instances**, consolidated at
   queue item 7 this arc. Two were newly observed here and are described in
   prose in the findings note: a structured exception handler wrapped around a
   native command, which can never fire because native commands set an exit
   code rather than raising; and a git invocation piped into a first-item
   selector returning a non-zero status while succeeding completely. **The
   generalisation owed a ruling: an exit code alone evidences nothing.** A
   check must assert on the substance of what it returns and name the
   assertions it actually evaluated. The D2.2a pre-flight is the first artefact
   that would encode it, which couples queue items 2 and 3 to item 7.
4. **A method can degrade silently, which is why elevation is corroborated
   twice.** The first attempt to read the process token's integrity label
   returned an empty result rather than an error. Had it been the only method,
   the assertion would have produced neither a green nor a red but a blank. The
   second method was introduced for that reason. This is the concrete origin of
   the three-state constraint recorded in the queue: an assertion is green,
   red, or **unknown**, and unknown must exit non-zero and never render as
   green. Every false green catalogued so far is an unknown rendered as a green.
5. **Carried unchanged and untouched by this arc:** PRs #64/#65 standing tree
   verification; the corpus listing debt at three documents (SG-07, SG-08,
   SG-09), with the pin unmoved and eligible at 16; the batch-2 panel
   circulation scope question; and the ci-docs paths-filter gap, for which PR
   #88 is a third confirming case on the covered path classes and no evidence
   at all on corpus markdown, which no run can reach and so no run can evidence.
6. **The handover chain broke at this arc, and that is why this file exists.**
   The queue update merged at PR #89 without a handover riding it, so for one
   session the newest handover on disk described the D2.0 frame as awaiting
   ruling — a merged fact misstated in the very document `CLAUDE.md` orientation
   names as the current state of play. Recorded as an observation about the
   ceremony rather than a defect in any artefact: `/session-close` updates the
   queue and drafts the summary, but authoring the handover is a governed act
   requiring operator command, and nothing in the ceremony makes the gap between
   them visible at the next boot. Both corrections in the closing note were
   found only because the next session's boot read the block back line by line.

## Registers at close

DEC next **0016** · ADR next **0011** · CL next **26** (15 open) · WS-E next
**64**. Derived from `scripts/repo_manifest.py` regenerated in-session at boot,
post-merge for each PR, and again at close — every run agreeing. **No number
was consumed this arc**, which is the correct outcome for a ruling that
executes an existing decision rather than making a new one. B7 ENTERED, exit
evidence open, unchanged.

**Divergences: zero**, at every regeneration. Notably zero after the queue edit
introduced an unconsumed register citation, written in the "next N" form
established by the PR #85 correction note — the convention works, and the
scanner did not read it as a claim that the item exists.

## Return queue, in order

Enumerates the `CLAUDE.md` queue block as amended by the correction riding this
handover, item for item and in its order, so the two agree by construction
rather than by assertion.

1. **Boot ritual via /session-open** (incl. rehash sweep; expect 0 pins, expect
   **0** divergences, now without carve-out).
2. **D2.1 spec schema v0.1 — the live keystone**, unblocked by the ruling. Both
   scenario classes from v0.1, carrying rulings-record amendments 3, 5 and 6
   from the start. The schema and the pre-flight artefact are both upstream of
   the first real test result, and items 2 and 3 are numbered in TOR Section 9's
   proof-first order rather than by priority.
3. **D2.2a pre-flight implementing artefact** — the residue of the parked
   elevated-session findings. The ACL fault is discharged; what remains is the
   missing artefact, the three-state constraint it must encode, the corpus
   index ownership hazard, and the standing no-elevation rule. Claims the next
   free CL number.
4. **Corpus listing for SG-07/SG-08/SG-09** — one act or per document,
   operator's decision. The ruled frame settles the interaction rather than
   leaving it open: commissioning runs pin the snapshot current at spike time
   and do not wait on this act, but Regime-2 formal runs use listed snapshots
   only.
5. **ci-docs paths-filter fix** — one line; whether it also warrants a WS-E
   ledger entry or a CL item is an operator decision.
6. **Lint invocation defects — two, of opposite polarity.**
7. **Check-method defect family, six instances** — a pattern-level ruling owed
   rather than separate fixes.
8. **Batch-2 panel circulation** — unblocked; open whether SG-03..SG-06 sit
   inside it.
9. **Conventions owed in `CLAUDE.md` at its next revision** — commit trailers
   (now seven instances across three arcs, which reads as an unwritten rule
   rather than practice running ahead of a written one), register-number
   citation, and DEC placement.
10. **PRs #64/#65 standing tree verification** — partially chipped, not
    discharged.
11. **Operator inclusion decision for TY-03..09** when ready.
12. **CL-25 / inc4** (pin writer) pending agent module; **CL-24** when
    convenient.
13. **Governance-guard deny path for history rewrites** — still unexercised;
    needs a throwaway clone.
14. **Consistency reads owed** when their targets are drafted — SG-07 §2.2 and
    §5.2, SG-08 §2.3 and §5.2.
15. **`corpus_edges_check.py` design-mode false green** — minimum fix is
    wording, not logic; a member of the family at item 7.
16. **Statute-edge width** — a property of the corpus rather than of any one
    document, and it will recur.
17. **TOR errata** carried to the Test Plan (D1.1), including the correction
    owed to the panel record for the propagated document-count phrasing.
18. **Gemini consolidation before the Agentic Topology ADR work opens**, which
    would consume ADR next 0011.
19. **Housekeeping, non-blocking** — stale local branches from past arcs.

### Corrections landed this arc

Two defects in the block committed at `a59cd7e` were found when the next
session's boot read it back, and both are discharged by the `CLAUDE.md` act
riding this handover. Neither is flagged forward; both are recorded as
completed history.

**The item 7 instance count read five while its own enumeration summed to
six** — the ONNX traversal check, **both** lint invocation defects,
`corpus_edges_check.py`, and the two observed during this arc. Ruled by the
operator: **six is correct, and the wording changes rather than the count.**
The family's stated rule is deliberately bidirectional — a check whose success
message claims more than it verified, *or* an exit status evidencing neither
success nor failure — so the false-red lint defect qualifies under the second
limb. Narrowing the family to false greens alone to rescue the number five
would subordinate the definition to the arithmetic, which is backwards. The
correction was first deferred, on the ruling that no fresh act should be opened
on a closed session for a two-word cosmetic fix, and made mandatory at the next
`CLAUDE.md` touch. This arc is that touch, and it is discharged here rather
than carried further.

**Queue items 2 and 3 were ordered against TOR Section 9.** The block placed
the D2.2a pre-flight artefact at 2 and the D2.1 schema at 3, while Section 9's
proof-first order runs frame → schema → spike, with the pre-flight a component
of the spike and therefore downstream of the schema. The inversion was not a
decision: old item 2 was reduced in place at the previous close and kept its
slot while the schema moved up into 3, and nothing weighed the two against each
other. Ruled swapped, with the cross-references in items 2 and 7 updated to
follow, and a sequencing note added to item 2 recording that the numbering
follows Section 9 rather than priority — so that a future in-place reduction
cannot silently invert it again. The general lesson is the one already learned
about register numbers at the previous arc, in a new register: **an edit that
preserves a slot can move a meaning that lives in the slot rather than in the
text.**

End of handover.
