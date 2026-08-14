# Correction amendments — restart-dependent claims

**Status: LANDED 2026-08-14. The two amendments below are APPLIED to their target
documents in the same commit that places this file.** Two committed documents
carry claims that timestamp evidence now contradicts or weakens. Each correction
below is an **amendment recording evidence**, appended to the document it
corrects — never a quiet edit of the original text, which stays as written so the
reader can see what was believed and when.

**Provenance, and the single edit made at landing.** This file was drafted in the
predecessor session's scratchpad, which is not durable. It was copied here
byte-identical and verified at SHA256
`cdce0f93c7308414e6e27f8993cd27a4cdab6213c1b2ea978d6c9b48cd2eaf16` before any
edit was made. Exactly one edit followed — this status block — because the
original opened "CANDIDATE DRAFTS. Nothing applied, nothing committed", and
committing that unchanged would have published a document whose first line
contradicted the commit carrying it. **The amendment texts below are untouched
from the draft.**

**Hash verification, and its shortfall stated rather than glossed.** The pinned
value could not be compared in full: the report carrying it truncated in the
coordination channel, so only its opening characters reached the session that
placed the file. Those characters match. The check therefore rests on a prefix
match plus **direct-read provenance** — the file was read from the same disk it
was written to and crossed no machine boundary, so the transport that convention
6 exists to protect never occurred — and it closes by operator inspection of the
amendment texts at landing. That is the basis on which convention 6 is treated as
satisfied here, and it is weaker than a full-string comparison.

**The evidence base, stated once.** `claude` PID 27792 started **08:55:58Z** on
2026-08-14 and has run continuously since. Every act of the session falls after
that timestamp, so no process restart occurred at any point during it.

---

## Amendment 1 — for `docs/governance/GROUP1_FAILURE_route-a-bypass_2026-08-14.md`

> ## Amendment, 2026-08-14 — section 5's registry-wall finding is WITHDRAWN
>
> **What was believed.** Section 5 records that the first route A probe did not
> fire, returning `Unknown skill: probe-route-a`, and explains it as a registry
> populated at process start — concluding that "load-at-start surfaces cannot be
> introduced into the running process that needs them, so they are testable only
> across a restart boundary", and generalising from settings to skills.
>
> **What the evidence now shows.** The `claude` process (PID 27792) started at
> 08:55:58Z and ran continuously through the entire session. The route A sequence
> — authoring the probe skill, the `Unknown skill` result, the retry, and the
> successful firing — all falls between roughly 10:10Z and 10:27Z, bracketed by
> the design readback written at 10:10:14Z and this entry's own draft at
> 10:27:33Z. **All of it inside one process.** No restart separated the failed
> invocation from the successful one.
>
> **The corrected finding.** The skill became invokable **without a process
> restart**. What section 5 recorded as a wall was a **delay** in registration.
> The believed restart between the two attempts did not occur; only the passage
> of one or more turns did.
>
> **The generalisation is withdrawn.** "Load-at-start surfaces" was too broad on
> two counts: agent definitions register live, and skills — on this evidence —
> register mid-process too. What triggers the refresh is **not established** by
> anything here, and is not claimed. Whether `settings.json` reloads mid-process
> remains **open**; it was never tested, because the widened families were
> deliberately never exercised.
>
> **The governance edge, which is the part worth keeping.** The corrected
> mechanism is not merely less inconvenient than the wall — it is a larger
> exposure. **The invokable surface of this repository can change mid-process,
> without a restart.** That cuts both ways and the benign direction is the less
> important one: a corrected skill or agent propagates live, which is convenient;
> but a skill authored mid-session becomes invokable in the same session, which is
> not.
>
> Combine that with this document's primary finding and the chain is complete, and
> was open today end to end: **write a skill file → it registers live → its render
> executes ungoverned.** The only gate on the first link is the protected-path ask
> on `.claude/skills/`, and this session ran in `bypassPermissions`, where that ask
> was auto-approved without surfacing. So on 2026-08-14 the entire chain — author,
> register, execute outside the guard — was reachable with no operator interaction
> at any step. That is stated as the configuration's reach, not as an allegation
> about what occurred; every skill authored this session was authored to order and
> is accounted for.
>
> **What survives untouched, and it is the substance of this document.** Route A's
> **BYPASS** classification does not depend on restart semantics in any way. The
> render executed a command carrying an absolute deny and returned no guard text,
> in a process where Bash denies were demonstrably firing — the force-push probe
> had returned the guard's refusal verbatim. Sections 1 through 4, and 6 through
> 9, stand as written.
>
> **Why this correction is recorded rather than edited in.** The original section
> is left intact because what was believed, and on what basis, is part of the
> record. A quiet edit would leave a document that had never been wrong, which is
> not the document this was.

---

## Amendment 2 — for `docs/governance/PRECEDENCE_DISCRIMINATOR_OUTCOME_2026-08-14.md`

> ## Amendment, 2026-08-14 — precondition 1 holds; its stated mechanism is weaker
>
> **The restart was real, and precondition 1 stands.** The `claude` process
> running the probe started at **08:55:58Z** on 2026-08-14. Phase 1's in-session
> series ran on 2026-08-13, and a further boot is recorded at approximately
> 08:47Z, both before that start. So a genuine process restart did separate Phase
> 1 from Phase 2, and the temporary allow rule — written to disk in the earlier
> session — was on disk before this process began. **The branch A outcome is not
> disturbed.**
>
> **What is weaker is the reasoning, not the result.** Section 2's "Precision on
> precondition 1" argues that the restart replaces the earlier probe's unevidenced
> assumption (that `settings.json` reloads mid-session) with "the documented
> mechanism (that it loads at session start)". Later evidence in the same session
> shows that at least one configuration surface — the skill registry — **does**
> refresh mid-process without a restart. Load-at-start can therefore no longer be
> assumed as a general property, and whether `settings.json` specifically reloads
> mid-process is **untested and open**.
>
> **Why this changes nothing about the outcome.** The rule was present on disk
> before this process started, so it was loaded under either mechanism. The
> restart was sufficient; it is only its stated rationale that was broader than
> the evidence supports.
>
> **Scope note on settings-reload semantics, stated because the temptation is to
> resolve it and the evidence does not.** It was suggested that a later read
> proved `settings.json` is re-read live. It does not. That read used the file-read
> tool and a JSON parse — **both read the file on disk**. A disk read shows what
> the file contains and can say nothing whatever about what the process had loaded
> or what it would enforce. The instrument cannot distinguish the two states, so
> the question is **INDETERMINATE**: whether `settings.json` reloads mid-process
> is untested in either direction.
>
> The one experiment that would have settled it — exercising a newly granted
> family and observing whether it was permitted — was **deliberately not run**,
> because the widening's activation was ruled conditional on a gate that failed.
> That was the right call and it left this question open as a side effect. It
> should be settled by design, not by accident, whenever the widening is next
> attempted.
>
> **A standing caveat, recorded here because it belongs with this document and is
> not resolved by this amendment.** The session ran in `bypassPermissions` mode,
> under which an ask is auto-approved without surfacing. The "no prompt" half of
> the branch A observation is therefore **uninformative on its own** — no prompt
> would have appeared regardless. The deny half is unaffected: denies are not
> auto-approved, and the guard's refusal was returned verbatim. What the probe
> establishes without qualification is that **the deny fired while a matching
> allow rule was in force**. Whether an ask would have preceded it cannot be read
> from this run.

---

## The three phantom restarts, for the session record

None of these appears as a claim in a committed document, so none needs an
amendment. They are listed because they were believed at the time, acted on, and
are the reason two documents needed correcting at all.

| Believed restart | When it was believed | What the timeline shows |
| --- | --- | --- |
| Widening Phase 2, "fresh restart so the merged settings provably load" | after merge #120 at 10:01:00Z | **UNDERMINED.** Process start 08:55:58Z; no restart before or after the merge |
| Prompt 33, "retry across the restart boundary" | between the failed and successful route A invocations, 10:10Z–10:27Z | **UNDERMINED.** Both invocations inside PID 27792 |
| Prompt 41, "fresh launch from a shell clean of CLAUDE_* variables" | 11:49Z onward | **UNDERMINED.** Same PID and same session id as the session it was meant to replace |

**The pattern is worth more than the three instances.** A restart is not
self-evidencing from inside the process, and the harness cannot tell one had
happened. In each case the belief was reasonable and the evidence that would have
tested it — process identity — was one command away and not run. **PID and start
time are the cheap check**, and they should precede any claim that rests on a
restart having occurred.

## Not corrected, and why

- **PR #121's commit and PR bodies** say "Phase 2 runs in a fresh process on this
  branch". That was a statement of plan, not of fact, and it is accurate as a
  plan. It did not happen, which is recorded here rather than in those bodies.
- **The tiers document's skill-render bullet** makes no restart claim. Its
  TESTED-UNGOVERNED finding rests on the render's behaviour alone and is
  unaffected.
