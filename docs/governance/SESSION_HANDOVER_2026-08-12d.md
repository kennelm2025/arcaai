# SESSION HANDOVER — ArcaAI 2026-08-12d (D2.2a pre-flight arc)

*Covers one session, scoped to a single named arc: queue item 3, the D2.2a
pre-flight implementing artefact. Landed at PR #104, merged `b1fc7f3`, claiming
CL-26. **Supersedes the boot line of**
`docs/governance/SESSION_HANDOVER_2026-08-12c.md`, retained as the record of the
CL-24 closure arc. Authored on explicit operator command, on the close branch, so
the queue update and this file ride one PR — the fifth consecutive arc where they
do. Verified against the **committed** queue on this branch (30 items, markers at
316 and 676), not against the summary it was drafted from.*

## Entry-criteria note — carried verbatim, at operator ruling

> Pre-flight green is ONE of four D2.0 entry criteria; the other three are
> run-record obligations: corpus snapshot pinned and stated, scenario spec
> schema-valid against v0.1, working tree state recorded. A green pre-flight
> alone does not satisfy entry.

This line is ruled to head the next session's spike brief as well. It is recorded
here because a green pre-flight now exists to point at, which is the moment the
misreading becomes available.

## Boot line (next session)

> Resume ArcaAI — B7 in progress. HEAD main to be the PR carrying this file;
> PR #104 merged at `b1fc7f3`, all five checks green. Boot ritual: conda arcaai →
> main → `git pull --ff-only` → `git fetch --prune` →
> `python scripts/repo_manifest.py --out D:/Downloads` → Divergences read,
> **expect zero** → Docker Desktop up → `scripts/dev_up.cmd` →
> `python scripts/rehash_sweep.py`, which **expects GREEN at exit 0 with no
> carve-out** — any red is a plain stop.
> **New: `python scripts/d22a_preflight.py` is the pre-flight artefact.** It
> asserts non-elevation first and gates on it, reads bytes from the cached model
> rather than stat-ing it, asserts the vector store's exists/readable/writable
> triple, and confirms environment identity. Exit 0 only when all four are GREEN;
> UNKNOWN and SKIPPED both exit non-zero. **The ceremony skills do not yet call
> it** — queue item 29.
> **Next arc is the D2.2a runner spike itself**, queue item 30, under DEC-0017.
> Standing rules: the harness never elevates, never assumes the database owner
> role, never bare-`cd`s in a persistent shell.

## Session summary

Authored `scripts/d22a_preflight.py` and merged it as CL-26, discharging the
prose-only authoring debt in which the ONNX cache traversal check existed as
narrative in `CLAUDE.md` and `.claude/skills/session-open/SKILL.md` with no script
behind it and no non-elevation assertion at all.

**The session's most useful event was a CI failure.** The first push tripped the
CF-1/B7-a guard, which permits exactly one importer of `chromadb`: the draft
pre-flight had imported it to derive the model cache location. The boundary held
and the artefact was corrected rather than the allowlist widened — a pre-flight is
not a retrieval adapter, and admitting the script that checks the cache would have
been adapting the control to the code. The correction also made two outcomes
honest about their difference: an absent cache **root** is now UNKNOWN, because
the layout is chromadb's to define and its absence may mean the layout moved
rather than that the model is missing, while a present root with an absent model
directory is RED. The draft had collapsed both into RED, asserting a fact about
the model from evidence that was only about a path convention.

## Verification battery

`git diff --stat` first throughout. Arc diff: `scripts/d22a_preflight.py` 440
insertions plus the CL-26 register entry; close diff `CLAUDE.md` only, 48
insertions, 2 deletions, inside the queue markers.

`ruff` all passed · `check_docs.py` 122 files, no findings · `repo_manifest.py`
0 divergences · **all five CI checks green** on #104 (lint-test, vertical-tests,
promotion-gate, manifest-history, structural-checks) · attribution asserted
against full printed commit bodies, no line asserting co-authorship.

Artefact behaviour, re-run from `main` after merge rather than only on the branch:
**4/4 GREEN, exit 0**. Self-tests: `--provoke cache_traversal` gives 3/4 GREEN with
UNKNOWN 1 and **exit 1**, proving UNKNOWN does not become a pass even when every
other assertion is green; `--provoke non_elevation` gives 0/4 GREEN, UNKNOWN 1,
**SKIPPED 3, exit 1**, proving the gate holds and the remaining assertions are not
reported as passing.

Preconditions verified before the arc opened: sweep GREEN at exit 0 with both
categories zero; governed store still empty across all five tables
(`0/0/0/0/0`); Docker and the dev stack up; conda `arcaai`, Python 3.11.15.

## Observed-not-raised

The vector store directory remains `BUILTIN\Administrators`-owned from the
elevated interlude, and the writability probe succeeded through the inherited
grant to authenticated users. Observed under the frame's records rule; not
converted into a finding or a fix.

## Open verifications carried forward

1. **Ceremony skills still describe rather than call the artefact.** Ruled in as
   transcription-in-spirit, deferred as a Tier 2 edit; the prose stands until then
   and anyone touching it carries a known-superseded note. Queue item 29.
2. **A green pre-flight is not entry.** See the verbatim note above.
3. **The instrument at queue item 28** — `governed_store_identity.py` still
   enumerates four tables from a hardcoded list and cannot see `audit_payload`.
4. **Tier 1 rule strings remain verified-and-wrong**, queue item 27, and want the
   same PR as item 29.

## Return queue

Source of truth is the queue block in `CLAUDE.md` as committed at PR #105,
verified against this file. **Thirty items.** Item 3 closed; items 29 and 30 new.
The next arc under DEC-0017 is **item 30, the D2.2a runner spike**: spec in,
corpus queried at a pinned snapshot, result JSON out, COMMISSIONING-labelled
throughout, pinned to the snapshot current at spike time and therefore not
blocked by the corpus listing debt at item 5. It closes with a **Commissioning
Session Record, not a report**.
