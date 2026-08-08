---
name: session-open
description: ArcaAI boot ritual — derive register state live, verify environment, read back the queue. User-invoked at the start of every session.
disable-model-invocation: true
allowed-tools: Bash(python:*), Bash(git status:*), Bash(git log:*), Bash(git diff:*), Bash(conda:*), Bash(gh pr list:*)
---

# Session open — boot ritual

Live state, captured now (not from any static file):

## Git state
!`git status`
!`git log --oneline -5`
!`git diff --stat`

## Register state (regenerated this session)
!`python scripts/repo_manifest.py`

## Open PRs
!`gh pr list --limit 10`

# Your task

1. Confirm the working tree is clean and local main matches origin. If
   not, stop and report — do not proceed onto a dirty or diverged tree.
2. Confirm the `arcaai` conda env is active (Python 3.11.15). If you
   cannot confirm it, say so and stop.
3. From the regenerated manifest output above, read back: WS-E / DEC /
   ADR / CL next-numbers, build-stage state, and any divergences. This
   readback is the session's register anchor — cite it, not memory, for
   every numbered artefact created this session.
4. Run `python scripts/rehash_sweep.py` and report; expectation is 0
   pins requiring correction. Any non-zero result is a stop-and-report.
5. If this session will touch retrieval, run the standing first act:
   the normal-shell ONNX cache traversal check.
6. Read back the Current Queue section of CLAUDE.md and ask the operator
   which single queue item this session's arc is. Do not start work
   until the arc is named. One arc per session.
