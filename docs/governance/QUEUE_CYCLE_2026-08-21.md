# Queue cycle record — 2026-08-21, the lane-terminal cycle

Record of the 2026-08-21 queue cycle: envelopes executed through the `_queue`
tree against lane terminals under DEC-0019's transport and
DEC-0018/AMD-A1..A11's envelope discipline. Written under PROMPT 132, the fold
envelope that closes the cycle.

**Why this exists, and why it is a separate file rather than an append.** The
2026-08-19 record at `docs/governance/QUEUE_CYCLE_2026-08-19.md` records the
first round trip. This one records a different thing: a day on which the
transport was used in anger, across multiple envelopes and two lane terminals,
with grant widenings declared per envelope under DEC-0018/AMD-A5. Those are
distinct cycles with distinct evidence, and folding the second into the first
would put two days' findings behind one date — which is exactly the reading
error the dated-append convention exists to prevent elsewhere in this tree.

## 1. Amendment 5 acceptance — the grant architecture is ACCEPTED

**Recorded here at the queue-cycle record location per the ceremony convention,
on the coordinator's recommendation as accepted by the Chair.**

**The finding.** Amendment 5's grant architecture is **ACCEPTED on two-half
evidence**: the granted toolset runs the full queue cycle — poll, read, probe,
edit, battery, commit, push, PR, R-draft — with **no permission dialogs reaching
the operator's screen**.

**The caveat travels with the acceptance and is preserved verbatim:**

> acceptance is per-toolset-as-granted; any future grant widening re-opens the
> question for the widened surface.

**Why the caveat is load-bearing rather than a hedge.** Acceptance is a
statement about a *surface*, not about a mechanism. The evidence is that the
enumerated verbs, as granted, did not prompt; it says nothing whatever about a
verb nobody has exercised. DEC-0018/AMD-A5 already makes this structural — each
widened surface re-opens the acceptance question, and the operator half for that
envelope is the observation of asks on the widened verbs — so the caveat is the
register's restatement of a rule already ruled, kept here so that a reader
meeting the acceptance does not meet it stripped of its bound.

**2026-08-21 evidence, added under this acceptance and banked per widened
surface as exercised.** Every GRANT-DELTA widening of that day surfaced **zero
asks**:

| Envelope | Widened surface | Asks surfaced |
|---|---|---|
| PROMPT 128R | git branch / add / commit | 0 |
| PROMPT 127R2 | git branch / add / commit | 0 |
| PROMPT 128R2 | push + PR creation | 0 |
| PROMPT 129 | push + PR creation | 0 |
| PROMPT 130 | push + PR creation | 0 |
| PROMPT 131 | push + PR creation | 0 |

**What this table is evidence of, stated precisely.** Each row is acceptance
evidence **for its own widened surface**, banked as that surface was exercised.
The rows do not aggregate into a general acceptance of unenumerated verbs, and
reading them that way would be the widening-by-accumulation the caveat forbids.
What they do establish is that the two widenings the day actually needed — the
commit family and the push-and-PR family — each ran without a dialog reaching
the operator, so the acceptance now rests on exercised surfaces rather than on
the poll-and-read core alone.

**The limit inherited from WS-E 75, and it is not cured here.** "Zero asks
surfaced" is an observation of the operator's screen, which is the only vantage
point that can make it. It is not a probe result, and no probe could produce
one: no vantage point both triggers and observes a live ask. The acceptance is
therefore built on the operator half by necessity, which is precisely why the
two-halves pattern exists — and why an executor-only report of a clean run has
never been sufficient to close one of these questions.

## 2. The two-halves fold owed for `ARCA-R-0152` and `ARCA-R-0153` — SPLIT

**Status: the operator half is transcribed here; the append to the R-records is
NOT made, because those records are not in this repository.**

**Where the search looked.** A repository-wide search for the records was run
before concluding, by four independent methods, and all four returned nothing:

1. **Filename** — a tree walk for any file whose name contains `0152` or `0153`.
   No match.
2. **Content, register form** — a recursive content search for the `ARCA-R-0152`
   and `ARCA-R-0153` tokens across markdown, YAML and JSON. `ARCA-R-0152` is
   present **only as cross-references** inside `docs/governance/WS-E_INCIDENTS.md`
   — at item 74's evidence paragraph and item 76's source line — never as a
   record of its own. `ARCA-R-0153` returns **no textual match anywhere in the
   tree**; the only hit for the bare digits is inside an unrelated archived PDF.
3. **Convention** — the governance directory holds exactly two records of the
   relevant shape, `docs/governance/QUEUE_CYCLE_2026-08-19.md` and
   `docs/governance/ARC_RECORD_2026-08-19_dec-0018-fold-in-and-queue-commissioning.md`.
   Neither carries an `ARCA-R-0152` or `ARCA-R-0153` entry structure.
4. **Series enumeration** — every `ARCA-R-0NNN` token committed to the tree was
   enumerated: `0144`, `0147`, `0148`, `0149`, `0150`, `0151`, `0152`. The
   series appears in the repository only as citation; **no `ARCA-R` record
   itself has ever been committed.** The R-series lives in Gmail transport, and
   that is the finding rather than an accident of this search.

**Why this is a split and not a failure.** The operator half is a governed text
that was ruled and must survive; the target it was to be appended to does not
exist inside the evidence perimeter. Transcribing it here preserves it at the
place the ceremony convention already puts cycle evidence, and leaves the append
owed against the R-records wherever they are finally committed. Discarding it
because its container was missing would have lost ruled text — the failure mode
the queue item 34 M2 gap describes, and the third time it has been recorded
against this decision family.

**--- OPERATOR HALF, verbatim (Chair, coordinator chat, 19 Aug 2026) ---**

> "Operator ask-ledger halves: PROMPT 152 - none fired. PROMPT 153 - none
> fired."

**--- Coordinator note carried with it (`ARCA-D-OPERATOR-HALVES-152-153`) ---**

> PROMPT 152: executor observed exactly one denial (Q4, predicted, verbatim
> deny) and zero asks surfaced to the operator. PROMPT 153: a register-write PR
> ran branch-to-PR-open with zero asks surfaced. Both runs now carry complete
> two-half evidence.

**What the two halves establish together.** For PROMPT 152 the executor half
records a *denial* — predicted, and returning the guard's own refusal text
verbatim, which is the deny-shaped probe discipline — while the operator half
records that *no ask* reached the screen. Those are different events and the
distinction is the point: a deny is observable from the transcript, an ask is
observable only from the screen, and neither vantage point can see the other's
class. For PROMPT 153 the executor half is a register-write PR taken from branch
to PR-open, and the operator half records zero asks across it. **Both runs now
carry complete two-half evidence**, which is what the pattern exists to produce.

**Owed forward:** when the `ARCA-R` records are committed — the M2 obligation
this section is a second instance of — the operator half above is appended to
each as its entry 2 under the standing two-halves pattern, entry 1 never
overwritten, per the A4.5 ruling recorded at
`docs/governance/QUEUE_CYCLE_2026-08-19.md` section 6.

## 3. Open — NOT DECIDED: three boundary questions for a Chair ruling batch

**Recorded as open, and deliberately not answered.** Each of the three arises
from the 2026-08-21 cycle's own friction, each has a defensible reading in more
than one direction, and each would bind future envelopes if settled by an
executor's working assumption rather than by a ruling. They are stated as
questions, with the considerations that make them genuine, and no
recommendation is attached where one would function as a decision.

**RB-1 — Does DEC-0018/AMD-A4's instrument boundary reach writes OUTSIDE the
repository?** The clause requires all file writes via the Write and Edit tools
and forbids shell-redirection writes. Its stated purpose is instrument
discipline over governed artefacts. Scratchpad and temp-directory writes are
neither governed artefacts nor inside the evidence perimeter, so a narrow
reading exempts them; a wide reading holds that the boundary is about the
*instrument* rather than the *destination*, and that an executor who keeps two
sets of habits will eventually apply the wrong one to the wrong tree. The cost
of the wide reading is friction on genuinely disposable files; the cost of the
narrow reading is that the discipline has an exception whose edge must be
judged correctly every time.

**RB-2 — Is the no-`2>&1` rule standing discipline, or guard hygiene made
obsolete by fix F2 of 2026-08-19?** WS-E 73 established that the `>` inside
`2>&1` read as a write construct to the guard, so a read-only command naming a
protected path was refused. Fix F2 taught the guard to distinguish a descriptor
duplication from a file redirection, and the re-probe confirmed that a read
carrying `2>&1` now executes. If the rule existed only to route around that
defect it is spent. If it is standing discipline — on the ground that the
construct interleaves two streams into one capture and makes an error's origin
unrecoverable from the transcript — then it survives its original occasion and
should be restated on its own reasoning rather than left as a repealed
workaround nobody repealed.

**RB-3 — What is the sanctioned Write-tool pattern for very large files?** The
instrument boundary forecloses the heredoc route, and a single very large Write
has a failure mode observed on 2026-08-21: the write is attempted whole and
fails on size, leaving nothing. The alternative is Write-then-Edit-append by
section, which lands incrementally and is recoverable, at the cost of a
multi-act write whose intermediate states are each a partially-written governed
artefact in the tree. Neither is obviously right, and the question bites
whenever a transcription act carries a large ruled text — which is the shape of
most fold ceremonies.

## 4. Prompt tally and provenance

**Prompts consumed by this record:** PROMPT 132 wrote it; it carries evidence
from PROMPTs 127R, 127R2, 128R, 128R2, 129, 130 and 131 of the same date, and
transcribes an operator half ruled on 2026-08-19 against PROMPTs 152 and 153.
Per the interim practice at
`docs/governance/FOLD_IN_2026-08-18_prompts-125-126-and-guard-install.md`
section 5, this record states the prompt numbers it consumed; following the same
section's second note, **no next number is predicted here** — a prompt exists
when it arrives in the terminal and not before.

**Transcription source.** The operator half, the coordinator note and the
Amendment 5 acceptance text were carried inside the body of the PROMPT 132
envelope, which is hash-anchored and inside the evidence perimeter. They are
reproduced verbatim, with line wrapping normalised and no other change, and
without added markup inside the reproduced sentences so that formatting cannot
be mistaken for emphasis the Chair did not give.

**Numbering.** No register number is consumed by this file. WS-E 77 is raised
separately by the same envelope and is recorded in
`docs/governance/WS-E_INCIDENTS.md`.

No control mapping line is carried, for the reason
`docs/governance/QUEUE_CYCLE_2026-08-19.md` states: queue item 34 M11(d)
requires per-class mapping content to be defined once in the control framework,
and that framework does not exist yet.
