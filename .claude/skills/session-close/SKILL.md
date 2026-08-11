---
name: session-close
description: ArcaAI session close ceremony — regenerate the manifest, update the CLAUDE.md queue, summarise the arc for handover. User-invoked at the end of every session.
disable-model-invocation: true
allowed-tools: Bash(python:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(echo:*)
---

# Session close — closing ceremony

Live state, captured now. Each render falls back to a marker line
rather than exiting non-zero: a hard-failing `!` render aborts the
ceremony before the task text is read, losing the arc summary over a
shell error. All three are LOAD-BEARING — a marker is a stop-and-report,
and in particular a failed diff render is NOT the empty diff that step 3
treats as proof an act did not happen:

!`git status 2>&1 || echo "(git status FAILED — see above; tree state UNKNOWN)"`
!`git diff --stat 2>&1 || echo "(git diff FAILED — see above; NOT an empty diff, tree state UNKNOWN)"`
!`git log --oneline -8 2>&1 || echo "(git log FAILED — see above)"`

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
5. Ask the operator explicitly for the handover command, and do not
   report this ceremony as complete until the handover is either
   commanded, or deferred on the record in the operator's own words.
   Silence is not deferral. The queue update at step 2 lands by
   ceremony while the handover needs an operator command, so the two
   drift apart unless the gap is named here — this has now happened
   twice consecutively, the queue merging ahead of its handover and
   leaving the newest handover on disk contradicting the committed
   queue (open verification 6 of
   `docs/governance/SESSION_HANDOVER_2026-08-11b.md`, and again at
   open verification 6 of
   `docs/governance/SESSION_HANDOVER_2026-08-11c.md`). Handover
   authoring itself stays a governed act on operator command —
   unchanged by this step, which asks for the command and never
   substitutes for it.
6. Remind the operator: `/clear` before starting the next arc.
