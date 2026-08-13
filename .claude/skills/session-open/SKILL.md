---
name: session-open
description: ArcaAI boot ritual — derive register state live, verify environment, read back the queue. User-invoked at the start of every session.
disable-model-invocation: true
allowed-tools: Bash(python:*), Bash(git status:*), Bash(git log:*), Bash(git diff:*), Bash(conda:*), Bash(gh pr list:*), Bash(echo:*)
---

# Session open — boot ritual

Live state, captured now (not from any static file).

Every render below is failure-tolerant, and that is the point: a `!`
render that exits non-zero aborts the whole skill before a word of the
task text is read, so the boot produces nothing at all — not even a
diagnosis of what failed. Each render therefore falls back to a marker
line and the ritual continues to the task text, which decides what the
failure means.

Renders are labelled by class and the two classes are not
interchangeable:

- **OPTIONAL** — context that is nice to have. Note the marker, carry
  on with the boot.
- **LOAD-BEARING** — the ritual's actual evidence. A marker here is a
  stop-and-report at the step that depends on it.

Tolerance governs only *how* a failure is surfaced. It never licenses
proceeding past a load-bearing one.

## Git state — LOAD-BEARING
!`git status 2>&1 || echo "(git status FAILED — see above; tree state UNKNOWN)"`
!`git log --oneline -5 2>&1 || echo "(git log FAILED — see above)"`
!`git diff --stat 2>&1 || echo "(git diff FAILED — see above; tree state UNKNOWN)"`

## Register state (regenerated this session) — LOAD-BEARING
!`python scripts/repo_manifest.py --out D:/Downloads 2>&1 || echo "(repo_manifest FAILED — see above; register anchor UNAVAILABLE)"`

## Open PRs — OPTIONAL
!`gh pr list --limit 10 2>/dev/null || echo "(gh unavailable — open PRs unchecked)"`

# Your task

1. Scan the renders above for FAILED / unavailable markers before
   reading anything else, and say which fired. A marker on an OPTIONAL
   render is noted and the boot continues. A marker on a LOAD-BEARING
   render is a stop at the step below that rests on it — report the
   error text the render captured; never substitute a remembered or
   on-disk value for the render that did not run.
2. Confirm the working tree is clean and local main matches origin. If
   not, stop and report — do not proceed onto a dirty or diverged tree.
3. Confirm the `arcaai` conda env is active (Python 3.11.15). If you
   cannot confirm it, say so and stop.
4. From the manifest regenerated above, read back: WS-E / DEC / ADR / CL
   next-numbers, build-stage state, and any divergences. The render
   prints only a summary line, so read the numbers from the file it
   wrote — `REPO_MANIFEST.md` under `D:/Downloads`, **outside the tree**
   per the `CLAUDE.md` commands section. A `REPO_MANIFEST.md` found
   inside the repository is a leftover from the superseded in-tree
   invocation and is presumed stale; do not read the anchor from it.
   This readback is the session's register anchor — cite it, not memory,
   for every numbered artefact created this session. If the manifest
   render failed, this session has no register anchor: no numbered
   artefact may be created until it is regenerated successfully.
5. Run `python scripts/rehash_sweep.py` and report; expectation is 0
   pins requiring correction. Any non-zero result is a stop-and-report.
6. If this session will touch retrieval, run the standing first act by
   CALLING the artefact, not by re-performing it from prose:
   `python scripts/d22a_preflight.py`. It asserts non-elevation first
   and gates on it, reads bytes from the cached model rather than
   stat-ing it, asserts the vector store's exists/readable/writable
   triple, and confirms environment identity. **Exit 0 with 4/4 GREEN
   is the only pass**; UNKNOWN and SKIPPED both exit non-zero and never
   collapse into green, so a non-zero exit is a stop-and-report at this
   step. Do not substitute a hand-run traversal check: the prose form
   carried no non-elevation assertion and returned green under an
   elevated shell, which is the false green this script exists to close.
7. Read back the Current Queue section of CLAUDE.md and ask the operator
   which single queue item this session's arc is. Do not start work
   until the arc is named. One arc per session.
