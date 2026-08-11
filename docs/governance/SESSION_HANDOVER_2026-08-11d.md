# SESSION HANDOVER — ArcaAI 2026-08-11d (permission tiering arc)

*Covers one session, scoped to two operator-commanded acts: converting the
`CLAUDE.md` queue block to pointer form, and granting harness autonomy by
written policy on the record. The second act uncovered an enforcement gap
that was closed ahead of it, and then a second gap in the policy itself
that was closed the same day. Landed at PR #94; the close PR carries this
file. **Supersedes the boot line of**
`docs/governance/SESSION_HANDOVER_2026-08-11c.md`, retained as the record
of the D2.1 schema arc. Authored on explicit operator command, on the
close branch, so that the queue update and this file ride one PR — the
first arc in three where they do, and the chain-break recorded at that
handover's open verification 6 is closed by construction rather than by
intention.*

## Boot line (next session)

> Resume ArcaAI — B7 in progress. HEAD main to be the PR carrying this
> file; PR #94 merged at `bb389df`, clean, all three workflows green.
> Boot ritual: conda arcaai → main → `git pull --ff-only` → `git fetch
> --prune` → `python scripts/repo_manifest.py --out D:/Downloads` →
> Divergences read, **expect zero**, no carve-out, held now across PRs
> #86 through #94 → Docker Desktop up → `scripts/dev_up.cmd` →
> `python scripts/rehash_sweep.py`. **The sweep expectation has
> inverted: expect RED.** Exactly two `fixture-*` rows are the expected
> state until CL-24 lands; anything other than two fixture-labelled rows
> is the stop. **Permissions now run in three tiers** —
> `docs/governance/HARNESS_PERMISSION_TIERS_2026-08-11.md` is
> authoritative. Tier 1 was narrowed the same day it landed: **a
> settings allow rule pre-empts the guard's ask**, so the two mechanisms
> are alternatives and never grant in Tier 1 anything Tier 2 is relied
> on to gate. **CL-24 is the next arc**, promoted and owed before
> D2.2a, its scope enlarged by WS-E 65. Standing rule, permanent: the
> harness never elevates, and never assumes the database owner role.

## What landed

1. **PR #94 merged (`bb389df`) — permission tiering.** Five commits, 6
   files, +547 / −227. ci-docs 9s, ci-devops 2m36s, ci-mlops 3m54s, all
   success on the post-merge sweep.
   - `3709f70` — the queue block converted to pointer form, +88 / −206.
   - `2a1feaf` — the governance guard extended to the PowerShell tool.
   - `44c3476` — **WS-E 64** appended.
   - `591ce5f` — Tier 1 allow-list in tracked settings, Tier 2 gates in
     the guard.
   - `d7f357e` — the tiers document created; `CLAUDE.md` Enforcement
     layer rewritten; the conventions consolidation written once and
     together; one clause added to `.claude/skills/session-close/SKILL.md`.
2. **The close PR** (this file, the queue update, the Tier 1 narrowing,
   and **WS-E 65**).
3. **Two register numbers consumed**, both WS-E: 64 and 65. DEC, ADR and
   CL close where they opened.

## The arc

### Act 1 — the queue block stopped being a second copy of the record

The block had grown into a duplicate of the handover record, and
duplicated state is the proven source of this week's divergence defects:
the 11b enumeration mismatch, the ordering inversion caused by a
slot-preserving edit, and the TOR document-count conflation that
propagated outward into the panel record. Each item is now number,
one-line title, status word, and a citation. Two pieces of meaning stay
inside the block because they can live nowhere else: the Section 9
sequencing note, whose content is its position, and the pointer lines
for the reporting ruling recorded below.

### Act 2 — the gap found before the grant

Step 0 was an inspection ordered before design, and it earned its place.
The PreToolUse matcher named the Bash tool while PowerShell is this
repository's primary shell. Probing that fix found the same severed
connection a second time inside the guard module, which still returned
allow after the matcher was corrected — **the second half was found only
by exercising the first, not by reading the code.** Both halves dated to
the harness install commit of 2026-08-08.

The guard had been written for PowerShell throughout: its deny list
carried the recursive force-delete forms in both argument orders, its
write-detection the PowerShell content-writing cmdlets, none of it
reachable through the shell it was written for. Recorded as WS-E 64.
Sequencing was ruled absolute — no allow-list widens while the deny
layer has a blind spot — so the fix landed first, in its own commit.

The near-miss attribution is the uncomfortable half and is recorded as
such. During the three-day window the DEC placement trap was caught by
the working protocol's verification-precedes-mutation rule, not by any
gate: no prompt fired, and none could have, because that path matched
none of the guard's protected patterns and no write was ever attempted.
`decisions/` is now gated for exactly that reason, and gated on a
mechanism rather than a convention — `scripts/repo_manifest.py` reads
register numbers off filenames there, so any write to that directory is
register-consuming by mechanism.

### The tiering disabled its own gates, and was narrowed the same day

The tiers document recorded, as UNVERIFIED, whether a Tier 1 allow rule
and a Tier 2 guard ask compose. They do not. **The allow rule wins and
the guard's ask never reaches the operator.** Every Tier 1 grant
therefore switched off the Tier 2 gate covering the same ground: bare
`Edit` and `Write` neutralised every protected-path gate, and the git
write verbs neutralised the branch-deletion and HEAD-on-main gates. Tier
2 was decorative for those paths from the moment the tiering merged
until the narrowing.

Withdrawn: `Edit`, `Write`, and git add, commit, push and branch in both
shells — 54 allow rules to 44. Tier 1 is now read-only operations, the
mandatory batteries, and git navigation that no gate depends on
narrowing. Restoring the rest needs an enumeration of paths provably
containing no protected path; `docs/` and `verticals/` each defeat
wholesale grants, and a mistaken enumeration is a silently disabled gate
rather than a visible error, so it was deliberately not attempted.

A second exposure is recorded rather than papered over: whether an allow
rule also pre-empts a **deny** is untested and has no safe probe, every
deny here being destructive. If it does, then for the interval in which
`git push` sat in the allow-list, the force-push guard was not in force.

**The test method matters more than the result.** As first written the
check turned on observing a prompt — which the harness cannot do, since
an approved ask and no ask are identical in a tool result. That is
precisely how the question survived the arc that created it. The working
form inverts the signal: run an allow-listed command that also carries a
guard ask and have the operator **decline** if prompted, because a
refusal *is* visible. Both outcomes then observable. The alternative
explanation — a pattern that simply missed the string — was ruled out by
feeding the guard the exact string, not a paraphrase.

**A second alternative survived the probe and was excluded afterwards,
which is what makes the diagnosis a controlled pair rather than an
inference.** The session might have been auto-approving at the
permission-mode level, in which case Tier 2 had never gated anything and
the narrowing addressed the wrong cause — indistinguishable from inside
the harness, and demanding a different fix. What separates them is what
happened next: with the allow entries removed and nothing else changed,
same session and same guard, the protected-path edit appending WS-E 65
and the `git push` of the close branch **both prompted**, minutes after
an allow-listed command had executed silently. The allow rule is the
only variable between the two observations. Mode-level auto-approval is
excluded and precedence is the cause. Recorded because the conclusion is
now load-bearing for every future permission decision here, and a reader
who cannot see this pair can reasonably raise the alternative again.

### WS-E 65, found by a count that did not grow

The boot sweep reported two `fixture-*` pin rows. The mandatory battery
ran once during the arc. The closing sweep reported two rows again —
with *different identifiers*, not four. Residue that does not accumulate
is residue being destroyed.

`tests/governance/conftest.py`'s session-scoped schema fixture runs
`drop_all` then `create_all` against the dev `arcaai_audit` database as
`arcaai_owner`. Every battery run erases every audit event and every
corpus-version row before the first test executes. This **corrects
WS-E 61**, which recorded the mechanism as tests that do not clean up:
the inverse is true and worse, and that entry's remediation deleted rows
whose cause was never diagnosed.

Append-only holds exactly as designed for the application role and is
defeated at the owner role by the repository's own mandatory battery. No
harm has resulted only because CL-25 is open and no operational writer
exists, so every row that store has ever held was written by its own
tests — sequencing, not a control, and it expires the moment a writer
lands. Routed to CL-24, enlarging its scope from test-data isolation to
separability of test writes from governed writes.

## Recorded operator ruling — test-cycle reporting (2026-08-11)

Full text, recorded here because the queue carries pointer lines only.

> Every test cycle closes with a governed reporting artefact, not
> complete until ruled by the operator. Two forms.
>
> **Regime 2 (Formal Execution): a TEST REPORT**, specified in the Test
> Plan (D1.1) when authored. Minimum content: cycle identity; the
> reproducibility triple per scenario (spec hash, model version, corpus
> snapshot); pass/fail per scenario; defects raised and routed;
> anomalies; an operator ruling on the cycle outcome (accept / re-run /
> escalate). Committed under `docs/governance/`; the operator ruling is
> part of the report, not a separate act.
>
> **Regime 1 (Commissioning): a COMMISSIONING SESSION RECORD** —
> deliberately NOT called a report. Same triple, what ran, what was
> observed, the COMMISSIONING marker. **No pass/fail summary**: per the
> ruled D2.0 frame, pass/fail is not an exit criterion and commissioning
> results are permanently inadmissible; a "report" format would invite
> promotion-by-osmosis. First instance produced by the D2.2a spike,
> proving the shape before D1.1 formalises the Regime 2 version.

## Detail migrated out of the queue block

Five items existed only in the block and in no committed record. They are
preserved here and the block now cites this file.

1. **Commit-trailer instances.** Three of the ten asserted instances
   appear in no other record: `59fb216` (SG-08), and `54360ac` and
   `e110b08` (both PR #90). The other seven are recorded across the
   2026-08-10c, 11, 11b and 11c handovers. The enumeration is the
   evidence for the count, which is why it is kept.
2. **SG-08 consistency-read basis.** TR-03 was characterised from
   SG-04 §2.1's committed wording rather than by bare series role;
   CV-05 by series role only. Committed records carry the section
   references and the TR-05/DL-06 basis, but not these.
3. **The absent-statute enumeration.** The corpus holds no text of
   s.338, s.339A, MLR 2017 reg 28, or the tipping-off provisions, all of
   which POCA s.327 depends on by reference. What the corpus *does* hold
   is committed in `verticals/fraud/corpus/MANIFEST.yaml`; the absent set
   was block-only.
4. **Listing-debt growth rate.** The debt has grown once per authoring
   arc for three consecutive arcs. Records state the debt at three
   documents but not the rate, which is the part that argues for
   clearing it.
5. **Stale local branch count.** The block said 19; the only committed
   figure is 20, at the 2026-08-08 handover. **Re-derive rather than
   carry either** — a number that has drifted once with no record of the
   change is not evidence.

## Verification battery

- **`git diff --stat` first, throughout.** PR #94: 6 files, +547 / −227.
  Close branch: queue +108 / −82; narrowing 3 files +84 / −44; WS-E 65
  +37, one file.
- **The matcher fix asserted on substance.** Five crafted payloads —
  PowerShell protected-write asks where it allowed; Bash protected-write
  still asks; PowerShell read-only still allows; Write to a protected
  path still asks; PowerShell `git status` still allows. Then one
  end-to-end refusal through the live PowerShell tool, built on the deny
  path **because a refusal is observable where an approved ask is not**.
- **Tier 2 exercised, not inspected.** Eleven payloads across all six new
  protected paths; the branch condition run in a throwaway repository —
  write on `main` asks, read-only on `main` allows, the same write on a
  feature branch allows, and both unresolvable-branch cases fail closed.
- **Full house battery:** ruff `All checks passed!`; 158 passed, 5
  skipped, coverage 76.33% against the 60% gate.
- **`python scripts/check_docs.py .`** — `No findings` across 110 files,
  at every stage.
- **Queue writes by script, never a markdown-aware editor.** Bytes
  outside the QUEUE-START and QUEUE-END markers asserted unchanged by
  length, by md5 and by direct comparison of the whole outside text: Act
  1 at 13994 bytes, the close at 17776. LF asserted by absence of any CR
  byte. Numbering asserted contiguous, 1..19 then 1..22.
- **Sequence-hold check run twice**, for WS-E 64 and 65, each time
  corroborating the ledger's own numbered headings against the
  in-session REPO_MANIFEST before writing.
- **Trailer count 0** across every commit, asserted by count.

## Open verifications carried forward

1. **Whether an allow rule pre-empts a guard DENY is untested**, and no
   safe probe exists. Never allow-list a command family carrying a deny.
2. **The permission rule strings are unverified**, and cannot be tested
   from inside the session they govern. The first session under the
   narrowed Tier 1 confirms by observation whether prompts actually fall.
3. **Hook routing of skill renders and subagent tool calls is
   unverified**, and is recorded as unknown in both directions rather
   than assumed.
4. **Restoring edits and git writes to Tier 1** needs a path enumeration
   that provably excludes every protected path. Not attempted.
5. **The audit store is destroyed by every battery run** (WS-E 65). It
   must be separable before D2.2a writes Commissioning Session Records
   into it.
6. **The check-method family gained three instances this arc** — the
   guard whose stated coverage was a claim about its patterns rather than
   its wiring; `Measure-Object -Line`, which counts non-blank lines while
   reading as a line count *and is the prescribed `wc -l` equivalent*;
   and the queue-block byte-versus-character measurement. The
   pattern-level ruling is further overdue.
7. **Two quoting/parse incidents**, both stopped before harm — one by the
   operator, one by the tool. Standing method now: complexity goes to a
   scratchpad file rather than inline.
8. **Whether the precedence failure warrants its own WS-E entry** is an
   operator decision, deliberately not taken. It is a
   guidance/enforcement discrepancy of the kind `CLAUDE.md` names a WS-E
   item, and it was found and closed the same day.

## Registers at close

DEC next **0016** · ADR next **0011** · CL next **26** (15 open) · WS-E
next **66**. Derived from `scripts/repo_manifest.py` regenerated
in-session at boot, post-merge, and again after each append — every run
agreeing. **Two numbers consumed this arc, both WS-E.** B7 ENTERED, exit
evidence open, unchanged.

**Divergences: zero**, at every regeneration.

## Return queue, in order

Enumerates the `CLAUDE.md` queue block as committed on the close branch,
item for item and in its order, read back from the committed file.

1. **Boot ritual via /session-open** — the sweep now expects RED, two
   fixture rows, and anything else is the stop. Carries the sequencing
   note.
2. **CL-24, test-database isolation — the live next arc**, owed before
   D2.2a, scope enlarged by WS-E 65.
3. **The governance suite destroys the live audit store** — WS-E 65
   appended; the fix belongs to item 2.
4. **D2.2a pre-flight implementing artefact** — sequenced after item 2,
   inheriting the Commissioning Session Record requirement.
5. **Permission-tiering follow-through** — precedence resolved against
   the design; three parts still open.
6. **Corpus listing for SG-07/SG-08/SG-09.**
7. **ci-docs paths-filter gap on corpus markdown.**
8. **Lint invocation defects, two of opposite polarity.**
9. **Check-method defect family** — pattern-level ruling owed.
10. **Batch-2 panel circulation** — scope decision owed.
11. **Ceremony frontmatter harmonisation** — residue of the conventions
    item, which discharged at PR #94.
12. **PRs #64/#65 standing tree verification.**
13. **Operator inclusion decision for TY-03..09.**
14. **CL-25 / inc4** pin writer.
15. **Governance-guard deny path for history rewrites** — unexercised.
16. **Consistency reads owed.**
17. **`corpus_edges_check.py` design-mode false green.**
18. **Statute-edge width.**
19. **TOR errata** carried to the Test Plan (D1.1).
20. **Gemini consolidation** before the Agentic Topology ADR work opens.
21. **Stale local branches** — housekeeping, count to be re-derived.
22. **Packaging declarations are unasserted.**

No correction is flagged against the block: it was read back from the
committed file during this authoring act, and the enumeration above
matches it item for item.

End of handover.
