# Queue cycle record — 2026-08-19, first round trip

Record of the **first complete round trip** through the ARCA prompt queue: an
item staged in Gmail, released by the chair, polled and executed by the
executor, and answered back into the queue. Written under PROMPT 146.

**Why this exists.** DEC-0018 A4 makes the Q-to-D ruling-by-queue flow standing
practice. A mechanism becomes a control only when its first exercise is
recorded — including what it did not do — so this file records the cycle
rather than merely asserting that it worked.

## 1. The cycle, act by act

| Act | Artefact | Outcome |
|---|---|---|
| Stage | `ARCA-P-0144 [STAGED]` | Staged by the coordinator, 2026-08-19 |
| Release | subject renamed to `ARCA-P-0144 [RELEASED]` | Chair act (D1) |
| Poll | executor searched drafts by subject | Item found, gates run |
| Execute | instructions 1–5 of the fetched body | Completed |
| Answer | `ARCA-R-0144` draft created | Verified by read-back |

**Three gates ran before execution and all three are recorded**, because a gate
whose result is not written is indistinguishable from a gate that did not run.

1. **Fetch** — draft located by subject search. PASS.
2. **Release token** — subject contained `[RELEASED]` verbatim, not `[STAGED]`.
   PASS. This is the gate that makes staging safe: an item can sit fully
   written and remain unexecutable until the chair renames it.
3. **Duplicate** — a search for `ARCA-R-0144` returned empty *before* any
   execution, per the item's own instruction 6. PASS. Ordering matters here:
   run after execution it would prove nothing.

## 2. What was executed, and what it returned

The item asked for an environment check, a HEAD read, and a reply draft. All
figures below are as the terminal printed them, not as expected.

- **Environment:** `Python 3.11.15`, interpreter
  `D:\Users\mikek\anaconda3\envs\arcaai\python.exe`. The interpreter path was
  read in addition to the version, so the version is evidenced as the `arcaai`
  environment's rather than a system interpreter's.
- **HEAD:** `c1b50a892406178cd1ceb3c113bab48821e58781`, tree clean on
  `main...origin/main`.
- **Expected-versus-actual:** the item recorded an expected HEAD of `c1b50a8`
  at staging time and instructed that a difference be reported as a finding
  rather than a failure. Short form matched; no divergence.

**The reply draft, `ARCA-R-0144`, four lines as written:**

```
ANSWERING PROMPT 144
HEAD=c1b50a892406178cd1ceb3c113bab48821e58781
PY=Python 3.11.15
STATUS=OK
```

**Verified at both ends.** The draft was not accepted on the create call's
return value: a read-back query by subject returned exactly one draft with the
content above. Exactly one also means the cycle did not execute twice.

## 3. Findings

### F-Q1 — The per-call permission gate stalls an unattended poll

**The first poll attempt was refused at the permission gate.** The executor
stopped rather than retrying, and the cycle resumed only when the chair
re-approved in the next turn.

**Why it matters to DEC-0018 rather than being a nuisance.** The whole purpose
of the envelope model is to run acts without a person at the prompt. A queue
poll that requires per-call approval cannot be unattended by definition — the
mechanism would stall on its first act every time. This is the concrete case
the envelope is for, and it is worth noting that the failure was **safe**: the
executor stopped and reported rather than working around the refusal.

**It also gives the F5 amendment a first test case.** An envelope whose scope
names the MCP queue tools would resolve this poll to allow-and-log. Per the A6
correction, the MCP leg carries **zero deny overlap** — the PreToolUse matcher
does not name MCP tools — so it is the cleanest available candidate for the
first envelope, and it needs no settings change at all.

### F-Q2 — The reply draft has no recipient, because none was specified

Instruction 5 specified a subject and four body lines and said nothing about
addressing. The executor created a bare draft, mirroring the staged item rather
than inventing a recipient. **Recorded because the return leg's disposition is
undecided:** if a reply is ever meant to be *sent* rather than read in place,
the item must say so. Inventing an address would have been the kind of silent
completion this register exists to prevent.

### F-Q3 — Path case differs between the item and the tree

The item wrote `D:\arcaai-repo\arcaai`; the tree is `D:\ArcaAI-repo\arcaai`.
Identical on Windows, so this is a **non-finding** operationally. It is
recorded only because a case-sensitive consumer of the same string would not
agree, and the queue is a transport that will one day carry strings to
something other than Windows.

### F-Q4 — Idempotency rests on the reply artefact, and not every item has one

`ARCA-P-0144` carried a reply draft, so its duplicate check had something to
look for. `ARCA-P-0146` has no reply leg — it ends at PR-open — so the same
check returns empty whether or not the item has run. **The real idempotency
markers for an item like this are the branch and the PR**, and they must be
checked instead. Worth stating before the queue is unattended: an item without
a reply artefact needs its own stated marker, or a re-poll will re-execute it.

## 4. Register and tally state

**ARCA-P-0127 is RETIRED UNRELEASED**, for tally collision: 127 was consumed in
the 2026-08-18 session, and each number is consumed once under the ECHO
convention. The retirement is recorded here and in the 0144 item's own body so
a later reader does not hunt for a missing 127 release. Nothing was executed
under it.

**First use of the D-series.** `ARCA-D-DEC-0018` carried the chair's ruling of
record from the coordinator chat to this fold-in, under DEC-0018 A4. Its
content is now committed at
`docs/governance/DEC-0018_A6_CORRECTION_2026-08-19.md` section 1. **The
D-series is transport, not register** — the draft says so itself, and the
register is the authority once written.

**Prompt tally.** 144 and 145 were consumed by the round-trip test; 146 by this
fold-in. Per the interim practice at
`docs/governance/FOLD_IN_2026-08-18_prompts-125-126-and-guard-install.md`
section 5, this record states the prompt numbers it consumed. Following the
same section's second note, no next number is predicted here: **a prompt exists
when it arrives in the terminal and not before**, so the tally records what has
been spent rather than what is expected.

## 5. What this cycle did not establish

- **That an unattended poll works.** Every act in this cycle was attended, and
  one of them required an explicit re-approval (F-Q1). The cycle proves the
  *format* round-trips; it says nothing about running it unwatched.
- **That the queue is governed.** The MCP tools the cycle used are outside the
  PreToolUse matcher entirely, so no guard was exercised at any point. That is
  what makes the queue leg safe to unattend and equally what makes it
  unevidenced by any guard probe.
- **That staging is tamper-evident.** An item is mutable until release — the
  0146 item rewrote its own timestamp in place, and says so. Nothing pins a
  staged body against its released form, so the chair's release attests to the
  text at release time and to nothing earlier.

## 6. Protocol rulings, ratified by release of `ARCA-P-0148`

Three rulings carried by that item and **ratified by the chair's release of
it** — the PROMPT 143 pattern, where release is the ratifying act rather than a
separate ruling document. Reproduced verbatim.

**F-R1 — the PR number is the identifier of record.**

> F-R1 ruled as CC stated it: the PR NUMBER is the identifier of record in
> queue traffic; URLs are convenience, not record — transport mangles them.

Raised at `ARCA-R-0147` entry 2 after Gmail rewrote the PR link into a
`google.com/url?q=` wrapper — then rewrote it a second time inside the sentence
describing the rewriting, producing a nested redirect. The finding
self-demonstrated in the record that raised it.

**F-R2 — subject state is not meaningful for the R-series.**

> F-R2 ruled: subject state is NOT meaningful for the R-series; the body STATUS
> line governs, as the two-entry pattern already provides. No terminal rename
> owed on any R-draft.

This resolves the gap raised at `ARCA-R-0147`: A4.1's vocabulary
(STAGED | RELEASED | ANSWERED) fits the P/Q/D flow and left an R-item with
nowhere to go after its PR merged. The answer is that it needs nowhere to go —
**the body governs, not the subject** — so no state was invented and none is
owed. An R-draft reading `[STAGED]` after merge is correct, not stale.

**A4.5 — the return leg does not end at PR-open.**

> A4.5 adopted as standing: every arc reaching merged-verified-cleaned-down
> gets its close-out appended to the same R-draft as entry 2; entry 1 is never
> overwritten.

Entry 1 records what was true at PR-open; entry 2 what was true after the merge
was verified from `main`. **Both are kept, because a return leg that overwrites
its own earlier state cannot evidence the sequence it exists to evidence.**
First applied at `ARCA-R-0147`, before it was ruled — the practice preceded the
rule, which is the same shape DEC-0017 records approvingly of itself.

**Ratification-by-release is worth naming as a mechanism.** The chair's rename
to `[RELEASED]` carries the rulings in the item's own body into force. It is
economical, and it has a cost a later reader should see: the ruling text and
the instruction text arrive in one artefact, so a released item is both a
ruling record and a work order. Where those need to be told apart, this section
is where the ruling half is separated out and committed.

## 7. F-R1 extended, ratified by release of `ARCA-P-0149`

Carried by that item and **ratified by the chair's release of it**, the same
mechanism section 6 names. Reproduced verbatim.

> F-R1 EXTENDED per F-R3's evidence: transport rewrites any dotted token, not
> only URLs — filenames included. Durable identifiers in queue traffic are PR
> numbers and register IDs; file paths and URLs are convenience, and the
> repository is the record. F-R3 does not stand separately; it is F-R1's second
> observed instance.

**F-R3 IS SUBSUMED and does not stand as its own finding.** It is recorded here
rather than deleted, because a finding that is absorbed into a broader one still
happened, and a reader meeting the identifier elsewhere needs somewhere to land.

**What the extension changes in practice.** Section 6's F-R1 was scoped to URLs,
on URL-shaped evidence — the `google.com/url?q=` wrapper. The evidence that
widened it is that the same rewriting reaches any dotted token, so a filename
written into a queue body is mangled exactly as a link is. The consequence is a
drafting rule for queue traffic and nothing more: describe files by directory
and register reference, and let PR numbers and register IDs carry identity.

**The scope of this rule is queue transport, not the repository.** Commit
messages, governance documents and code comments continue to cite exact paths,
because they are not carried by a transport that rewrites them and because the
house rule enforced by `scripts/check_docs.py` requires a cited path to exist. A
reader who generalises this ruling into the tree would break that check.

First applied in `ARCA-R-0149`, whose body describes every file by directory and
register reference throughout.

No control mapping line is carried, for the reason
`docs/governance/SESSION_COSTS.md` states: queue item 34 M11(d) requires
per-class mapping content to be defined once in the control framework, and that
framework does not exist yet.
