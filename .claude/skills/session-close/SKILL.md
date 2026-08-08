---
name: session-close
description: ArcaAI session close ceremony — regenerate the manifest, update the CLAUDE.md queue, summarise the arc for handover. User-invoked at the end of every session.
disable-model-invocation: true
allowed-tools: Bash(python:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*)
---

# Session close — closing ceremony

Live state, captured now:

!`git status`
!`git diff --stat`
!`git log --oneline -8`

# Your task

1. Regenerate the repo manifest for this session's live register
   numbers: `python scripts/repo_manifest.py --out D:/Downloads` —
   written OUTSIDE the tree. REPO_MANIFEST.md is gitignored and
   untracked by design; there is no committed snapshot to refresh. It
   is a convenience for the *next* session's paste-in contexts, and
   that session must still regenerate it (see CLAUDE.md register-state
   rule) — a manifest found on disk is presumed stale.
2. Update ONLY the section between `<!-- QUEUE-START -->` and
   `<!-- QUEUE-END -->` in CLAUDE.md to reflect the queue as it now
   stands: items completed this arc removed or marked, new items
   appended. Touch nothing else in CLAUDE.md.
3. Write the arc summary in house handover style:
   - The arc (one line: what act this session was scoped to)
   - Landed (PRs merged, files created, registers appended — with
     numbers as read from this session's manifest regeneration)
   - Verification battery run, leading with the `git diff --stat`
     output (empty diff = the act has not happened)
   - Open verifications carried forward
   - Return queue for next session
4. Present the summary to the operator for inclusion in the session
   handover document. Do NOT write the handover file yourself unless
   the operator explicitly commands it — handover authoring is a
   governed act in its own right.
5. Remind the operator: `/clear` before starting the next arc.
