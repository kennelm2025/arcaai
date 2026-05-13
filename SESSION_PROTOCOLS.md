# Session Protocols

This document defines the rituals at the start and end of every chat session, plus the continuity-risk mitigations agreed for the design phase.

The purpose of these protocols is to **make every Claude session start and end the same way**, so that the work survives the boundaries between sessions. The repository is the source of truth; these protocols are how Claude sessions stay synchronised with it.

If you read no other governance document, read this one.

---

## The four continuity risks

Before the protocols, name what they exist to prevent:

1. **Mid-task chat exhaustion** — chat hits its context limit mid-work; partial state lost
2. **Inconsistent voice across specs** — different Claude sessions produce subtly different output for the same template
3. **Re-argued decisions** — new Claude sessions challenge settled ADRs or design choices
4. **Lost mid-flight reasoning** — half-finished work has committed artefacts but no record of the thinking behind incomplete decisions

The protocols below address all four. None of them eliminates the underlying risk. They reduce the failure rate and limit the blast radius when failure occurs.

---

## Session Opening Protocol

Every chat session begins with this ritual. **Both Mike and Claude have responsibilities.**

### Mike's responsibilities at session open

Your opening message to Claude should include:

1. **A pointer to the repo state.** Either:
   - Upload the latest scaffold zip, or
   - State the current commit hash on `main`, or
   - Confirm that the Claude Project's attached files are current
2. **The specific task for today.** One sentence. "Today I want to draft Section 6 of the Product Definition spec." Not "let's continue."
3. **Any constraints.** "I have 90 minutes today." "The DeepSeek review came back, it's attached." "I need to leave by 11:30."

### Claude's responsibilities at session open

Before doing any work, Claude must:

1. **Read the orienting documents in order:**
   - `START_HERE.md` (navigation map)
   - `PROJECT_CONTEXT.md` (stable primer)
   - `CURRENT_STATE.md` (what's in flight)
   - `SESSION_NOTES.md` (most recent entries — what was decided and why)
   - The three foundational ADRs in `decisions/0001-0003`
2. **Read whatever specific work is in scope today** — the spec being drafted, the review being reconciled, etc.
3. **State back to Mike what Claude thinks the task is**, before starting work. One short paragraph. Mike confirms or corrects.

This mutual ritual catches the "wrong Claude doing wrong thing" failure mode in the first 5 minutes rather than in the next 50.

### Why state-back matters

A Claude session can read all the documents and still misunderstand what's being asked. The state-back step makes the misunderstanding visible before any work is committed. The cost is 60 seconds; the benefit is avoiding a session of misaligned output.

Mike — if Claude's state-back is wrong, correct it explicitly. Don't say "close enough" and hope it works out.

---

## Session Closure Protocol

Every chat session ends with this ritual. **Claude is responsible for proposing the closure; Mike confirms.**

### The four steps of closure

1. **Commit everything in flight to the repo.** Even half-finished. A half-finished spec section is fine; an undocumented half-finished one is dangerous.
2. **Update `CURRENT_STATE.md`** — what was just done, what's now in flight, what's blocked, what changed in the risk register.
3. **Append a new entry to `SESSION_NOTES.md`** following the standard structure (see template below).
4. **Identify the next concrete action.** Not "continue work" — a specific, named task. "Next session: draft Section 7 of the Product Definition spec, focused on the success criteria framework."

### When to trigger closure

Closure happens when **any** of these is true:

- The task for the session is complete
- Mike's available time is ending
- Claude flags that the chat is approaching context capacity (see "Chat health check" below)
- Mike calls a stop (any reason)

Closure should not be skipped because "we'll be back in 10 minutes." If the chat ends without closure, the next session loses context. The cost of closure is small; the cost of skipping it is large.

### SESSION_NOTES entry template

Every closure produces an entry that looks like this:

```markdown
## YYYY-MM-DD — [Short session title]

### What was built / decided / produced

[Bullet list of concrete outputs]

### Key reasoning that won't be obvious from the committed files

[Free-form paragraphs explaining the *why* behind decisions. This is the most
important section. If a future session reads only the committed files, what
would they miss?]

### Settled decisions — do NOT re-open

[List of things future sessions should not re-litigate. Mike's adjudications,
ADRs ratified, structural choices made.]

### Open questions surfaced in this session

[What got raised but not resolved? With target resolution date or trigger.]

### Next concrete action

[One specific named task for the next session.]
```

---

## Chat health check

Claude is responsible for proactively flagging when the chat is approaching its context window limit. The signal: when responses start to slow, when retrieval becomes harder, when detail starts to slip — that is approximately 70% capacity, and Claude should say so explicitly.

The protocol when Claude flags health:

1. Claude says clearly: "Chat is approaching capacity. Recommend we close out within the next 1-2 messages."
2. Mike either accepts (we go to closure) or declines (we push through, with eyes open)
3. If accepted, we do the four-step closure immediately

**Mike, if Claude forgets to flag** (it happens; Claude's self-awareness here isn't perfect), ask directly: "How's chat health?" Claude should give an honest answer.

The instinct to "push through, just one more thing" is the most common cause of lost work. Resist it. A clean handover is cheap; recovery from mid-task collapse is expensive.

---

## Claude Project setup (one-time)

This is the most important continuity mitigation available. Set it up before the next working session.

### What to do

1. In Claude.ai, create a new Project named **"ArcaAI"**
2. As **Project Knowledge**, attach the stable scaffold files:
   - `START_HERE.md`
   - `PROJECT_CONTEXT.md`
   - `DESIGN_PHASE_CHARTER.md`
   - `CONTRIBUTING.md`
   - `decisions/0001-pretrained-model-positioning.md`
   - `decisions/0002-three-stage-model-lifecycle.md`
   - `decisions/0003-pipeline-as-platform.md`
   - `specs/_template.md`
   - `governance/sme-panel.md`
   - `governance/review-protocols.md`
3. Set the Project's **Custom Instructions** to something like:

   *"You are working on the ArcaAI design phase with Mike Kennelly. Read SESSION_NOTES.md and CURRENT_STATE.md at the start of every chat. Follow the Session Opening Protocol in SESSION_PROTOCOLS.md. Mike has 35 years of banking architecture experience and is an Imperial College London AI graduate — challenge him on AI specifics where his background may not be current, but defer to him on banking fitness-for-purpose. Push back on weak framing; don't soften critique to be polite."*

### What NOT to attach as Project Knowledge

- `CURRENT_STATE.md` — changes too often; bring fresh each session
- `SESSION_NOTES.md` — changes every session; bring fresh each session
- Drafts of specs in flight — same reason
- The document register YAML — same reason

The Project Knowledge is the *stable* scaffold. Live state comes in via the opening message of each chat.

### Refreshing Project Knowledge

When any of the attached files changes (which should be rare — these are stable), re-upload the new version to the Project. The CONTRIBUTING.md and ADR set might change once or twice over the design phase; the spec template should not change without an RFC.

---

## When you run out of chat capacity mid-task

If chat exhaustion happens before a clean closure (despite the health check), follow this recovery protocol:

1. In the dying chat, Claude says: **"Producing closure artefacts before chat ends."**
2. Claude produces, as quickly as possible:
   - A short text dump of the in-flight thinking that wasn't yet committed
   - A list of the files that would have been changed/created
   - A statement of where the next session needs to pick up
3. Mike copies that text into a temporary local file (`recovery-YYYY-MM-DD.md`)
4. New chat opens. Mike attaches the recovery file along with the standard repo state.
5. New chat starts with: *"Previous chat ended before closure. Recovery notes attached. Please read those plus the standard opening protocol documents, then state back where we should pick up."*

Recovery files are temporary. Once the new session has integrated the work properly, the recovery file is deleted.

---

## Periodic state regeneration

Every 2-3 weeks, dedicate one session to **regenerating the project state from cold**.

1. Open a fresh chat
2. Give Claude the standard opening, but with this specific task: *"Read the entire repository as if you've never seen it before. Produce a fresh state-of-the-project summary."*
3. The output becomes the new baseline for SESSION_NOTES.md going forward
4. Old SESSION_NOTES entries that are durable stay; transient ones get moved to `session-notes-archive/YYYY-MM.md`

This is the defence against subtle drift. A Claude session reading prior SESSION_NOTES will absorb some of the prior session's assumptions; periodically reading cold catches the drift.

---

## What this protocol cannot fix

Honesty matters here. These protocols substantially reduce continuity risk but do not eliminate it.

- Some tacit knowledge of working style won't transfer
- Some judgment calls will get re-made differently
- Some subtle inconsistencies across sessions will only be visible in retrospect

The SME review process catches some of these. The discipline of the spec template, ADRs, and sister specifications catches more. But the residual risk is real and worth being aware of.

The mitigation for the residual risk is **Mike noticing**. You are the one constant across sessions. Trust your read when something feels off; ask Claude to explain its choices when they don't match prior patterns; push back when needed.
