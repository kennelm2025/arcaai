---
name: pr-prep
description: Pre-PR battery and house-style PR body draft. Runs the doc checks, shows the diff-stat first, and drafts the PR body for operator review. Does not push or open the PR itself.
disable-model-invocation: true
allowed-tools: Bash(python:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(gh pr:*)
---

# PR prep — battery then body

Live state — two distinct checks with opposite polarity. PR content
FIRST.

(1) PR CONTENT — merge-base to HEAD, the diff GitHub renders as the
pull request. EMPTY means there is nothing to PR: stop, the act has
not happened. This is the only diff that answers that question. A
bare `git diff --stat` compares the working tree against the index,
is blind to committed work, and therefore reads empty on exactly the
healthiest pre-PR state — every act committed, tree clean. Never
substitute it here:
!`git diff --stat main...HEAD`
!`git log --oneline main..HEAD`

(2) WORKING TREE — must be CLEAN at PR time. Opposite polarity to
(1): anything reported below is uncommitted work the PR will NOT
carry. Non-empty is the stop, and the remedy is the opposite one —
commit it into the branch or discard it, then re-run:
!`git status --short`
!`git diff --stat`

Battery:
!`python scripts/check_docs.py`

# Your task

1. Read the PR-content diff-stat (1) aloud. If it is empty, stop: the
   act has not happened and there is nothing to PR. Judge this from
   (1) alone — the working-tree diff in (2) cannot see committed work
   and must never stand in for it.
2. Confirm the working tree (2) is clean. If anything is reported,
   stop with the opposite remedy to step 1: commit it into the branch
   or discard it, then re-run. Uncommitted work at PR time ships a PR
   silently missing it.
3. Report the check_docs result. If the arc touched corpus edges, also
   run `python scripts/corpus_edges_check.py` and report the edge
   count against the previous known count. If the arc touched
   MANIFEST.yaml listings, also run
   `python scripts/corpus_manifest_entries.py` and report drift.
4. Run the lint step appropriate to what changed (`scripts/lint.cmd`
   locally on Windows; state clearly if you could not run it and it
   must be left to CI).
5. Draft the PR body in house style:
   - **Act**: the single governed act this PR lands
   - **Stores touched**: governed files changed, append-only
     compliance stated
   - **Battery**: each check run, with its result; diff-stat quoted
   - **Registers**: WS-E / DEC / ADR / CL items raised, discharged,
     or advanced, with numbers as read from this session's manifest
     regeneration
6. Propose the branch name and the single next git command. One
   command per prompt from here: wait for each result before
   proposing the next. Do not push and do not open the PR without an
   explicit command per step.
