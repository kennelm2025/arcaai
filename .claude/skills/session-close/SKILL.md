---
name: session-close
description: ArcaAI session close ceremony — regenerate the manifest, update the CLAUDE.md queue, summarise the arc for handover. User-invoked at the end of every session.
disable-model-invocation: true
allowed-tools: Bash(python:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(echo:*)
---

# Session close — closing ceremony

## Authority split (operator ruling 2026-08-13)

> "session-close checks autonomous, register writes still STOP"

Written here rather than remembered, because an authority boundary that lives
only in a transcript is not a boundary. Two classes, and the executor must know
which class each step is in before starting it:

**AUTONOMOUS — the check phases.** Evidence assembly, the verification battery,
regenerating the manifest, reading state back, and stating the rolling
five-step plan. These read and report. None of them changes governed state, and
none of them is improved by asking first: the operator gains nothing from
confirming a `git diff --stat`.

**STOP FOR THE OPERATOR — anything that writes or leaves the machine.** In
particular:

- **Register writes.** Any append to DECISIONS.md, the ADR register, the CL
  changelog or the WS-E ledger. Consuming a register number is a governed act
  and stays one.
- **The queue block update at step 2** — it edits a committed file.
- **Record and handover commits**, and any pull request.
- **Gmail or any outbound dispatch.** Content leaves the machine; it is
  confirmed with its recipient and body shown, every time, with no standing
  grant.

The split is asymmetric on purpose. Checks are cheap to run and cheap to
re-run, so the cost of doing them unasked is near zero. Register writes and
outbound sends are the two things this repository cannot take back.

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
6. State the **rolling five-step plan**: the next five steps as a plan of
   record, each tagged with what kind of step it is. Three kinds, and the
   tag is the point — an untagged list flattens work that cannot be
   parallelised into work that can:
   - **spine** — serial, blocking, and in order. A spine step cannot start
     before its predecessor lands. Merges are almost always spine.
   - **shadow** — work that can run alongside the spine because it touches
     a disjoint set of files. Name the files it touches, so the disjointness
     is checkable rather than asserted; a shadow step that collides with the
     spine is a spine step wearing the wrong label.
   - **ruling** — needs the operator and nothing else, so it is costed in
     the operator's minutes rather than in session time. State roughly how
     long it should take, because a 60-second ruling blocking an hour of
     shadow work is the thing this tagging exists to surface.
   Five is a working horizon, not a target: state fewer if fewer are
   genuinely known, and never pad the list to reach it. The plan is a
   projection and is not itself a ruling — the operator may reorder it
   without that being a deviation from anything.
7. Remind the operator: `/clear` before starting the next arc.
