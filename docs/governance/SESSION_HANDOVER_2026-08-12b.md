# SESSION HANDOVER — ArcaAI 2026-08-12b (accelerator-pack install and hook-invocation arc)

*Covers one session, scoped to a single named arc: install the Accelerator Pack
v3 and repair the fail-closed hook deadlock that ended the previous session.
Landed at PR #98, merged `7ff26b8`. Two register numbers consumed, DEC-0017 and
WS-E 68. **Supersedes the boot line of**
`docs/governance/SESSION_HANDOVER_2026-08-12.md`, retained as the record of the
CL-24 isolation arc. Authored on explicit operator command, on the close branch,
so the queue update and this file ride one PR — the third consecutive arc where
they do, keeping closed the chain-break recorded at open verification 6 of the
2026-08-11b and 2026-08-11c handovers. Every queue reference below was verified
against the **committed** queue on the close branch, not against the summary this
file was drafted from.*

## Boot line (next session)

> Resume ArcaAI — B7 in progress. HEAD main to be the PR carrying this file;
> PR #98 merged at `7ff26b8`, clean, both checks green (lint-test 2m47s,
> structural-checks 8s). Boot ritual: conda arcaai → main → `git pull --ff-only`
> → `git fetch --prune` → `python scripts/repo_manifest.py --out D:/Downloads`
> → Divergences read, **expect zero**, no carve-out, held now across PRs #86
> through #99 → Docker Desktop up → `scripts/dev_up.cmd` →
> `python scripts/rehash_sweep.py`.
> **The sweep still expects RED, and its shape is the check** — exactly
> `category irreproducible-pin : 0` and `category excluded-by-rule (test) : 2`,
> naming `fixture-d53c6ac1-…` and `fixture-9e191dd4-…`. Those two rows are
> static since DEC-0016; if their identifiers change, the isolation has broken.
> Any other shape is the stop. **Unchanged this arc** — the carve-out retires
> when the residue cleanup lands, and not before, and this session did not touch
> it.
> **New and binding from this arc: DEC-0017, build-first right of way.** Arc
> selection at `/session-open` must take a build-queue artefact before any
> governance refinement item, unless a governance item *directly blocks* a
> merge — a narrow exception carrying an evidential obligation, the blocking
> relationship stated in the session record. Queue items 1, 2 and 3 are the
> build lane; most of the remainder is refinement and now yields.
> **The governance hook changed shape.** `.claude/settings.json` now invokes the
> guard in exec form with `${CLAUDE_PROJECT_DIR}`, and the guard derives its
> repository root from its own file location. Standing rules, permanent and
> extended this arc: the harness never elevates, never assumes the database
> owner role, and **never bare-`cd`s in a persistent shell**.

## The arc

Install the pack, then fix what the install exposed. The arc's centre of gravity
moved within the first hour: the pack install was routine, and the hook defect
was not.

## What landed

**PR #98** — merged `7ff26b8`, 16 files, 797 insertions, both checks green.

**Pack, five files.** Three skills (`check-method`, `commit-hygiene`,
`harness-discipline`) and two subagents (`corpus-lister`, `test-author`). Four
were byte-identical to the verified zip at install. The fifth,
`corpus-lister.md`, installs at 2130 B / SHA256 `86D986FD…` from the
**quarantined lineage** and deliberately not from the verified zip, whose copy
is a 2009 B truncated reconstruction (`C7AAD779…`) missing the description's
leading sentence. Adjudicated on two independent grounds: an 11 Aug 18:18 mtime
matching every sibling in that tree against the reconstruction's later 12 Aug
07:02, and all sibling files byte-identical between trees. Ruled: installed
correct, pack defective for that one file. The quarantined artefact verifies
itself — its filename `…QUARANTINE-07F5D363.zip.bak` matches the first eight of
its own hash.

**Hook repair.** `.claude/settings.json` moves to the exec form with
`${CLAUDE_PROJECT_DIR}`; `.claude/hooks/governance_guard.py` gains `REPO_ROOT`
derived from `__file__` and passes `cwd=` to its git call.

**Governance.** `DEC-0017` (build-first right of way, ruled verbatim from the
pack README) and `WS-E 68` (the hook deadlock). Two convention lines added to
`CLAUDE.md`. Eight alignment dispositions applied to the pack's own transcription
defects, including the no-`Co-Authored-By` rule, absent from the pack's
commit-authoring skill and now transcribed there in full.

**Bundle.** Mobile Ruling Protocol as **PILOT** — issue template, `ruling-briefs/`
convention, three GitHub labels — with a review clause firing after the first
five mobile rulings. Boundary Tagging and `contract-seed.md` ruled in.

**PR #99** — the queue update, riding with this file.

**Register state, read live at close:** DEC next 0018, ADR next 0011, CL next 26,
WS-E next 69, 0 divergences. ADR and CL untouched; 0011 remains reserved for
Agentic Topology.

## The incident, and why it is worth reading

WS-E 68 is the longest entry this register has taken in a single arc, and the
original defect is its least interesting part. A `cd .claude` broke a
relative-path hook invocation and every tool failed closed, including the edit
that would have fixed it.

The corrective then reproduced the outage twice. Escaped backslashes are
unescaped twice — JSON decodes the pair, then command parsing consumes the
survivor — collapsing the path and deadlocking the session inside its own repair.
Then two operator fixes were reported applied while the loaded configuration was
unchanged; the settings-file-shadowing theory was disproved by enumeration
(exactly one guard line existed anywhere), leaving a stale editor buffer writing
old content over new. A read-once-at-session-start hypothesis was raised and
**excluded on evidence already in hand** rather than by spending a restart: the
first mis-edit took effect on the very next tool call.

**Fail-closed held at every stage**, under conditions that escalated from
mis-pathed to actively erroring. That is the property worth protecting, and it is
the same one credited at WS-E 67.

The method finding is the durable one. The guard was certified only by a
**deny-shaped** probe returning its own refusal text verbatim, paired with an
**allow-shaped** probe. A dead hook and a working hook are indistinguishable from
any command that was going to be allowed anyway, so an allow-shaped probe alone
would have certified a dead guard silently, three times over. Queue item 8 has
accumulated instances for weeks without producing a method; this pairing is the
first positive discriminator it has yielded.

## Verification battery

`git diff --stat` first, throughout. Final close diff: `CLAUDE.md` only, 63
insertions, 8 deletions, all four hunks between lines 362 and 483 and therefore
inside the 316–510 queue-marker range.

`ruff` all passed · `check_docs.py` 118 files, no findings · `repo_manifest.py`
0 divergences · CI on #98 both green · attribution check performed by printing
every commit body in full on each branch and reading it, per the amended
convention, with no line asserting co-authorship.

**Guard probes run five times**, deny-shaped and allow-shaped: after the
exec-form change, after the guard's own code changed, and again post-merge from
`main`. Every deny-shaped probe returned the guard's own refusal text, not a path
error.

**The BOM claim was tested before the skill was amended**, on operator ruling
rather than assumed: a file written by the old recipe begins `EF BB BF` on
PowerShell 5.1.26100.9168. Confirmed, and the recipe amended to the no-BOM form
with the test cited as provenance.

## Open verifications carried forward

1. **`.claude/` CI coverage is a green of unknown meaning.** Two checks passed on
   a PR whose largest surface was `.claude/`, and no workflow's `paths` filter
   was confirmed to name that directory. Not a known gap — an unverified pass,
   which is the worse shape. Queue item 24.
2. **Skill and subagent hook routing remain unprobed**, as do the Tier 1 and
   Tier 2 rule strings. Only PowerShell-tool routing is now evidenced. Queue
   item 4(c).
3. **The three new reference skills declare no `allowed-tools` at all**, a
   different shape from the five ceremony skills, and whether an absent
   declaration inherits, denies or is inert has not been established. Queue
   item 10.
4. **`${CLAUDE_PROJECT_DIR}` is verified in this harness only.** It has never
   been exercised in CI or in another clone, which is precisely the portability
   the change was made to buy. The first CI run touching `.claude/` settles it,
   and item 1 above may mean no such run has happened yet.
5. **The Mobile Ruling Protocol is a pilot with a counter at zero.** No mobile
   ruling has yet been made through the issue template. Nothing may cite the
   protocol as settled practice until the five-ruling review returns. Queue
   item 22.

## Return queue

Source of truth is the queue block in `CLAUDE.md` as committed at PR #99,
verified against this file. Twenty-four items.

Items **1, 2 and 3** are the build lane and hold right of way under DEC-0017.
Item 2 — CL-24 residue cleanup — is the operator's own owner-role act, still
gates item 3, and still gates the retirement of item 1's carve-out. Nothing this
arc touched it.

New this arc: **22** (pilot review, counter at zero), **23** (DEC-0017 standing,
binding arc selection), **24** (`.claude/` coverage unverified). Amended:
**4** narrowed, **8** gains two instances and its first counter-example, **10**
widened from five skills to eight.

The next arc should be a build item under DEC-0017. Nearest is queue item 3,
which sits behind the operator's item 2.
