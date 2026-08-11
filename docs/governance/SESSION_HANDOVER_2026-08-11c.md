# SESSION HANDOVER — ArcaAI 2026-08-11c (D2.1 spec schema arc)

*Covers one session: the arc named at the 2026-08-11c boot — author D2.1
scenario spec schema v0.1, the keystone artefact, next in TOR Section 9's
proof-first order after the ruled commissioning frame. Landed at PR #91 and
PR #92. **Supersedes the boot line of**
`docs/governance/SESSION_HANDOVER_2026-08-11b.md`, which is retained as the
record of the D2.0 ruling and ONNX root-cause arcs it covers. Authored on
explicit operator command, on its own branch, after PR #92 had merged — the
chain-break shape recorded at that handover's open verification 6, recurring
one arc later and recorded again below rather than quietly repaired.*

## Boot line (next session)

> Resume ArcaAI — B7 in progress. HEAD main `9984696` (PR #92 merge), clean,
> identical to origin/main; the handover PR carrying this file advances it.
> Boot ritual: conda arcaai → main → `git pull --ff-only` → `git fetch
> --prune` → `python scripts/repo_manifest.py --out D:/Downloads` (writes
> outside the tree; the file is gitignored, there is no committed snapshot) →
> Divergences read, **expect zero**, a plain stop condition with no carve-out,
> held now across PRs #86, #88, #89, #90, #91 and #92 → Docker Desktop up →
> `scripts/dev_up.cmd` → `python scripts/rehash_sweep.py` — expected green at
> "0 pins" until CL-25 lands a writer. **Retrieval is not blocked**: the ONNX
> cache ACL fault is repaired and verified. **The pre-flight still has no
> implementing artefact** — the four assertions have been assembled by hand in
> every session that needed them, so the D2.0 frame's entry criteria remain
> unmeetable by any command in the repo. That artefact is now **queue item 2
> and the live next step**, claiming the next free CL number at the D2.2a
> spike. **Standing rule, permanent: the harness never elevates** — any fix
> needing elevation is the operator's, at their own terminal, re-verified
> afterwards from a non-elevated shell. The D2.1 schema is committed and
> immutable: changes are v0.2, never edits.

## What landed (all on main)

1. **PR #91 merged (`e8a4346`) — D2.1 scenario spec schema v0.1.** One commit
   `d93760a`, 9 files, +712 / -1, no `Co-Authored-By` trailer.
   - `arcaai/harness/schema/scenario_spec_v0.1.schema.json` created, +364 —
     the artefact.
   - `arcaai/harness/__init__.py` created, +19 — package init only, no runtime
     code.
   - `tests/harness/test_scenario_spec_schema.py` created, +183, with five YAML
     fixtures: two valid, one per scenario class, and three deliberately
     malformed.
   - `pyproject.toml`, +2 / -1 — `arcaai.harness` added to the setuptools
     packages list; `jsonschema` declared as a direct dependency.
2. **PR #92 merged (`9984696`) — the queue update.** `8a420d8`, `CLAUDE.md`
   +77 / -56, queue block only, by scripted write.
3. **No register number was consumed by either.** DEC, ADR, CL and WS-E all
   close where they opened.

## The arc

### Placement was TOR-directed, not merely defensible

The boundary check ran before anything was written. `decisions/0009-platform-vertical-boundary.md`
is silent on the harness: its Decision 1 table governs ML lifecycle
capabilities and a test harness appears in neither column. DEC-0015 is silent
on harness *code* placement — it rules the register home, a ledger line rather
than a numbered file, and specifies the pre-flight as a standalone invocable
script, but states no path. `docs/governance/TOR_test-capability_RevC_RULED_2026-08-10.md`
is **not** silent: Section 4 names the module path literally as
`python -m arcaai.harness run --spec <file>`. That wording governs, and it
directs exactly the placement taken — `arcaai/harness/` as a third sibling of
`arcaai/platform/`, neither platform machinery serving a request nor vertical
business semantics, but the thing that tests both. No ADR was needed and
ADR-0011 stayed untouched.

CI coverage was confirmed rather than assumed: `arcaai/**` and `tests/**` are
already inside both the ci-devops and ci-mlops paths filters, so the new
directories opened no paths-filter gap.

### Form: a committed, hashable artefact rather than code or prose

Ruled as JSON Schema (draft 2020-12). The reasoning is worth carrying because
it generalises: the frame's entry criterion — a spec "schema-valid against
spec schema v0.1" — has to be a machine-evaluable check against a fixed thing
the check can name. Pydantic-as-source would make it "valid against whatever
the models currently say", which is an unknown wearing a green. A companion
prose document would be a second authority. And the spec-hash leg of the
reproducibility triple hashes a spec, not a Python module.

The schema is closed at every level, mirroring the `extra="forbid"` discipline
of the governance event models: an unknown field is rejected rather than
ignored, because a silently ignored field makes the recorded spec hash
describe something other than what ran.

### The three binding amendments live inside the artefact

No parallel prose artefact — definitions sit in `description` and `$comment`
where they bind.

- **Amendment 3.** Migration-diff comparison semantics declared per scenario
  and required on both classes: bit-identical where the pipeline is
  deterministic, defined tolerances where it is not. A declared tolerance must
  state its bounds and name its nondeterminism source, so a reviewer can check
  the tolerance was chosen rather than reached for. A bit-identical claim
  carrying a tolerance is rejected as a contradiction rather than resolved by
  precedence.
- **Amendment 5.** Gap-detection scoring defined mathematically and kept
  distinct from semantic-distance scoring. It scores absence: weighted
  abstention plus distractor avoidance over the top-k result set, both terms in
  [0,1]. For a planted gap there is no passage it would be correct to retrieve,
  so a similarity measure would score the opposite of what the scenario exists
  to test.
- **Amendment 6.** `generator_seed` mandatory for scoring-class scenarios and
  **forbidden** for retrieval-class, not merely optional there: a seed recorded
  against a run that never invoked the generator is a reproducibility claim
  with nothing behind it.

Corpus snapshot identity is the DEC-0014 manifest hash pair — `manifest_version`
plus `manifest_sha256` — read off `arcaai/platform/governance/corpus.py` rather
than assumed. The retrieval snapshot hash, which folds in chunker version and
therefore determines what the index actually contains, is carried as an
optional additional pin with the question of whether retrieval-class scenarios
should require it left explicitly to the D2.2a spike, as the first thing to run
against a real index.

### One schema change made mid-arc, caught by a negative test

Forbidden fields were first expressed as `false` subschemas. A negative test
showed that form rejects correctly but reports only that a value is disallowed,
without naming the offending property. Changed to `not`/`required`, which
rejects identically and names the field.

That is the check-method rule applied to the schema's own output rather than
merely stated — the first worked application of the generalisation the queue
has been carrying, and it was found by the rejection tests rather than by
review.

## Verification battery

- **`git diff --stat` first, throughout.** PR #91: 9 files, +712 / -1. PR #92:
  `CLAUDE.md` +77 / -56, sole file changed.
- **Lint** via absolute-path PowerShell invocation: `All checks passed!` — the
  substantive line, not exit 0 alone, per the carried lint-defect lesson.
- **Full house battery:** 158 passed, 5 skipped, coverage 76.33% against the
  60% gate. Eleven new tests, of which seven are rejection tests asserting
  which rule fired and where rather than merely that validation raised. The
  minimum negative set is covered: a scoring-class spec missing
  `generator_seed`, a scenario of neither class, and a wrong-typed retrieval
  cut-off.
- **`python scripts/check_docs.py .`** — deliberately NOT run on PR #91, which
  changed no markdown, and said so rather than run ceremonially. Run on PR #92:
  `No findings` across 108 files.
- **CI stated as verified fact, not inferred.** On the `pull_request` event for
  PR #91, ci-devops and ci-mlops both concluded success and ci-docs correctly
  did not run at all. On the push to main, all three concluded success.
- **Queue edit by scripted write**, not a markdown-aware editor. Bytes outside
  the QUEUE-START and QUEUE-END markers asserted unchanged at 13891 by a
  case-sensitive comparison of the entire outside text before and after —
  stronger than a hunk-range check — with LF endings confirmed preserved.
  Numbering asserted contiguous 1..19 programmatically and every internal
  cross-reference re-checked against its renumbered target.
- **Trailer count 0** on every commit, asserted by count.
- **`python scripts/rehash_sweep.py`** at boot — 6 manifest versions in git
  history, 0 pinned `corpus_version` rows, all pins verified.

## Open verifications carried forward

1. **The schema is proved well-formed and expressible, not proved right.** The
   tests establish that both classes are expressible and that the amendments'
   mandatory fields are enforced. Whether amendments 3, 5 and 6 are correctly
   *interpreted* is a reading question, and the D2.2a spike is the first thing
   that tests the schema against reality. This distinction is stated plainly
   because a green suite is exactly the kind of evidence that gets read as more
   than it is.
2. **The schema JSON is not declared package data.** `arcaai.harness` now
   ships; the file it exists to carry does not. Harmless today because the test
   resolves the schema by path, and it bites the moment a runner loads it from
   an installed distribution — which is the D2.2a/D2.2b arc.
3. **`arcaai.platform.retrieval` is still absent from the setuptools packages
   list**, working only by grace of the editable install; and **nothing in the
   repo asserts that list at all**. `tests/test_packaging.py` tests the agent
   packaging node, not setuptools — the name misleads, and that is how the
   omission survived. A test over the packages list is the single fix that
   would have caught both this and item 2 above. Left untouched by ruling this
   arc and queued instead.
4. **The pre-flight still has no implementing artefact.** Every green so far
   has been hand-assembled and is not reproducible by any command in the repo.
5. **Closed this arc, and recorded as closed:** the push-event CI asymmetry
   parked at open verification 6 of `docs/governance/SESSION_HANDOVER_2026-08-11.md`.
   All three workflows carry a push trigger on main with no paths filter, the
   paths list appearing only under `pull_request`, so every merge runs all
   three regardless of content. Evidenced both ways — a docs-only merge ran
   ci-devops and ci-mlops, and PR #91's code-only merge ran ci-docs in 10s. It
   is an unconditional post-merge sweep by construction rather than a defect,
   and ci-devops' own header records it catching a repo-wide lint failure that
   PR-time filtering had missed. Distinct from the corpus-markdown gap, which
   is a PR-time defect and remains open.
6. **The handover chain broke again, the same way, one arc later.** PR #92
   merged the queue update before this file existed, so for the interval
   between them the newest handover on disk both lagged main by two PRs and
   contradicted the committed queue — enumerating D2.1 as item 2 after that
   item had been discharged. This is the second consecutive occurrence and the
   mechanism is structural rather than an oversight: `/session-close` updates
   the queue automatically while handover authoring requires an operator
   command, and nothing in the ceremony surfaces the gap between them at the
   next boot. Recorded as an observation about the ceremony. Changing the
   ceremony is its own arc and was deliberately not folded into this one.
7. **Carried unchanged and untouched by this arc:** PRs #64/#65 standing tree
   verification; the corpus listing debt at three documents (SG-07, SG-08,
   SG-09), with the pin unmoved and eligible at 16; the batch-2 panel
   circulation scope question; and the ci-docs corpus-markdown paths gap.

## Registers at close

DEC next **0016** · ADR next **0011** · CL next **26** (15 open) · WS-E next
**64**. Derived from `scripts/repo_manifest.py` regenerated in-session at boot,
post-merge for each PR, and again at close — every run agreeing. **No number
was consumed this arc.** That is the right outcome for an artefact whose
identity is its filename and its version rather than a register entry, and it
is worth stating explicitly because a keystone deliverable landing without
touching any register looks, at a glance, like an arc that forgot to record
itself. B7 ENTERED, exit evidence open, unchanged.

**Divergences: zero**, at every regeneration.

## Return queue, in order

Enumerates the `CLAUDE.md` queue block committed at `8a420d8`, item for item
and in its order, read back from the committed file rather than from the draft
that produced it.

1. **Boot ritual via /session-open** (incl. rehash sweep; expect 0 pins, expect
   **0** divergences). Carries the queue-maintenance note: where items encode a
   ruled sequence their numbering follows that sequence rather than priority.
2. **D2.2a pre-flight implementing artefact — the live next step.** Claims the
   next free CL number. Must carry the three-state constraint: an assertion is
   green, red or **unknown**, and unknown exits non-zero and never renders as
   green. Non-elevation is asserted first, and on its failure the artefact
   refuses to report the remaining assertions at all. Carries the corpus index
   ownership hazard, recorded not repaired, and the standing no-elevation rule.
3. **Corpus listing for SG-07/SG-08/SG-09** — one act or per document,
   operator's decision.
4. **ci-docs paths-filter gap** — one line; WS-E entry or CL item is an
   operator decision. Now carries the push-event diagnosis as a distinct,
   closed matter.
5. **Lint invocation defects — two, of opposite polarity.**
6. **Check-method defect family, six instances** — pattern-level ruling owed,
   now with one worked application behind it.
7. **Batch-2 panel circulation** — unblocked; open whether SG-03..SG-06 sit
   inside it.
8. **Conventions owed in `CLAUDE.md` at its next revision** — commit trailers
   (ten instances, the axis having widened to code with the D2.1 commit),
   register-number citation, and DEC placement.
9. **PRs #64/#65 standing tree verification** — partially chipped.
10. **Operator inclusion decision for TY-03..09** when ready.
11. **CL-25 / inc4** pending agent module; **CL-24** when convenient.
12. **Governance-guard deny path for history rewrites** — still unexercised.
13. **Consistency reads owed** when their targets are drafted.
14. **`corpus_edges_check.py` design-mode false green** — wording, not logic; a
    member of the family at item 6.
15. **Statute-edge width** — a property of the corpus, and it will recur.
16. **TOR errata** carried to the Test Plan (D1.1).
17. **Gemini consolidation before the Agentic Topology ADR work opens**, which
    would consume ADR next 0011.
18. **Housekeeping, non-blocking** — stale local branches from past arcs.
19. **Packaging declarations are unasserted** — the schema JSON not declared as
    package data, `arcaai.platform.retrieval` absent from the packages list,
    and nothing asserting that list at all.

No correction is flagged against the block: it was read back from the committed
file at the start of this authoring act, and the enumeration above matches it
item for item.

End of handover.
