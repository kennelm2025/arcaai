---
name: pr-prep
description: Pre-PR battery and house-style PR body draft. Runs the doc checks, shows the diff-stat first, and drafts the PR body for operator review. Does not push or open the PR itself.
disable-model-invocation: true
allowed-tools: Bash(python:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(gh pr:*)
---

# PR prep — battery then body

Live state (diff-stat FIRST — an empty diff means there is nothing to
PR, whatever else is green):

!`git diff --stat`
!`git status`

Battery:
!`python scripts/check_docs.py`

# Your task

1. Read the diff-stat above aloud. If it is empty, stop: the act has
   not happened.
2. Report the check_docs result. If the arc touched corpus edges, also
   run `python scripts/corpus_edges_check.py` and report the edge
   count against the previous known count. If the arc touched
   MANIFEST.yaml listings, also run
   `python scripts/corpus_manifest_entries.py` and report drift.
3. Run the lint step appropriate to what changed (`scripts/lint.cmd`
   locally on Windows; state clearly if you could not run it and it
   must be left to CI).
4. Draft the PR body in house style:
   - **Act**: the single governed act this PR lands
   - **Stores touched**: governed files changed, append-only
     compliance stated
   - **Battery**: each check run, with its result; diff-stat quoted
   - **Registers**: WS-E / DEC / ADR / CL items raised, discharged,
     or advanced, with numbers as read from this session's manifest
     regeneration
5. Propose the branch name and the single next git command. One
   command per prompt from here: wait for each result before
   proposing the next. Do not push and do not open the PR without an
   explicit command per step.
