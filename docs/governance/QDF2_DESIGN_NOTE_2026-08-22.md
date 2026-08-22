# QD-F2 design note (Step 1) — proposed design for refused-draft terminal state and swept-outcome archive

## 1. Provenance header

**Status: PROPOSED DESIGN. Nothing here is decided.** Every point at which this
note proposes rather than derives is enumerated as a rulable question in the
Decision Register at section 6. The note is written to be ruled on, not to be
implemented from as it stands.

| Field | Value |
| --- | --- |
| Governing source | `docs/governance/QDF2_SPEC_2026-08-22.md`, transcribed under PROMPT 155 |
| Authored under | PROMPT 156, lane T2, QD-F2 Step 1 |
| Gate | PROMPT 155 merged at `1a69e69` (PR #163) — satisfied |
| Date | 22 August 2026 |
| Register numbers consumed | None. The withholding lift remains the next-0020 candidate and is not taken here |

**Footnote — PR series is not the PROMPT series.** The spec transcribes a ruling
that reads "PR #155 authorised to merge", a GitHub pull-request number from the
21 August commissioning arc, unrelated to PROMPT 155 or PROMPT 156. The two
series are independent and neither cites the other. Carried forward from the
spec's own header.

**What this note derives from, and what it may not do.** The spec is the
governing source. Where the spec or the ruled record answers, this note derives
and cites. Where they are silent, it marks OPEN and does not fill the gap with
judgement — the spec's own seven OPEN items are carried forward rather than
quietly closed. Where a design choice must be made to make progress, it is
proposed and routed to the Decision Register rather than taken.

---

## 2. The two mechanisms, kept separate

The spec's section 3.1 is titled "QD-F2 is two mechanisms, not one" and the
separation is load-bearing. The source register entry names the second under
"Same family", which reads easily as a restatement of the first. It is not:
the two have different triggers, act on different objects, and fail in
different directions. **Collapsing them would produce a design that fixes the
paging and leaves the re-alerting, or the reverse, while reporting QD-F2 as
landed.**

### 2.1 Mechanism (a) — refused-draft terminal state

**Trigger.** Any of the driver's five refusal conditions, per the module
docstring in `scripts/queue_driver.py`: a malformed envelope, an unknown lane,
a TARGET disagreeing with the dispatch order, an unisolated lane, or an
existing inbox file whose bytes differ from what would be written.

**The defect, stated precisely.** The driver's refusal behaviour is already
correct in every respect except termination. It emits an ERROR page, writes a
log row, and does not route — and it does not retry, because none of the five
conditions is transient. What it does not do is mark the *input*. The Gmail
draft remains RELEASED, so the next poll selects it again, re-reads it,
re-refuses it, and pages again. Three pages in three passes were observed, and
the arithmetic under a 60-second loop is sixty per hour.

**The proposed remedy is symmetry, not new machinery.** The driver already
relabels a draft on the success path: the docstring records that the only
removal it performs is "of the RELEASED label at relabel time, which is what
'relabel' means and is required by requirement 2". The success path therefore
already has a terminal state, and the refusal path does not. The proposal is
to apply the mechanism that exists to the path that lacks it — relabel the
draft on refusal, to a distinct terminal label, so the poll stops selecting it.

This matters for the DEC-0019 deletes-nothing property: a relabel is not a
deletion, and the register already contemplates exactly this act on the
success path. **The proposal therefore adds no new class of act.**

**State transition (proposed).**

| Stage | Draft label | Inbox | Paging |
| --- | --- | --- | --- |
| Released | RELEASED | absent | — |
| Refused, today | RELEASED (unchanged) | absent | every poll, forever |
| Refused, proposed | terminal refusal label | absent | once |

**What the driver stops doing:** selecting the item on subsequent polls, and
therefore paging on it more than once.

**What evidence travels.** A refused item must carry its refusal report — the
spec derives this from the source text at section 3.1(a). Proposed: the raw
bytes as received, the hash computed on those raw bytes per DEC-0019 B2, the
refusal class from the five above, the timestamp, and the log row's
correlation. Whether that lands as one file with a header block or as the
envelope bytes plus a sidecar is a Decision Register question — the two differ
in whether the preserved bytes remain independently hashable without parsing.

**Filesystem shape.** Proposed `_queue\T{n}\dead\`, following the shape now
live at `_queue\T1\dead\`. See section 3 on the standing of that precedent.

**Bounding.** Any such write sits inside the queue root and is therefore
bounded by `_assert_within_queue` exactly as today, with no change to that
function's contract. The constraint to design within is the one the PROMPT 155
report surfaced: queue paths resolve against the configured root in
`scripts/queue_driver.config.json`, not against a lane worktree, and
`_assert_within_queue` refuses any write inside a lane worktree. A `dead\`
directory under the queue root satisfies both by construction.

**A collision case the design must answer.** One of the five refusal conditions
is "an existing inbox file whose bytes differ". A dead-letter write can hit the
same shape: a second refusal of the same prompt id would collide with the
first. The driver's standing discipline is to refuse on doubt rather than
overwrite, so the dead-letter path must not silently clobber. Proposed:
disambiguate by prompt id plus refusal timestamp, which is the convention the
manual disposition already used at `_queue\T1\dead\`. Routed to the Decision
Register.

### 2.2 Mechanism (b) — processed archive or high-water mark

**Trigger.** The outbox sweep. The driver sweeps each lane's outbox into one
consolidated reply draft per session-day.

**The defect.** Swept outcome files have no terminal state, so a subsequent
sweep sweeps them again and re-alerts. The spec records that this was found
independently three times — by lane T2, by the driver log, and by the Chair's
mobile session — which is unusually strong corroboration for a defect of this
kind and is the reason it is carried as part of QD-F2 rather than as a
nice-to-have.

**The choice the source leaves open.** The source names "processed archive /
high-water mark" and chooses neither; the spec carries this as OPEN-2, noting
that the two are not equivalent — an archive is per-item and survives
reordering, whereas a high-water mark is positional and assumes monotonic
sweep.

**A derivation that bears on the choice, and it is evidence rather than
preference.** A high-water mark keyed on prompt number requires the series to
be monotonic. **It is not.** `docs/governance/PROMPT_SERIES_RECONCILIATION_2026-08-22.md`
records a fork in which numbers 132 to 153 were attested on two session
families, an envelope staged as 141 renumbered to 154, and the QD-F2 pair
renumbered to 155 and 156. The live queue additionally carries revision
suffixes — `128R`, `128R2`, `129R` — which the driver's own dispatch-order
reading treats as first-class. A positional mark over that series would skip
items on any renumbering and is unsound on the evidence available today.

The remaining keys have their own problems, and the spec's OPEN-3 asks exactly
this. Filesystem modification time is mutable and would treat a corrected
outcome file as new. A content hash is per-item, which is an archive by another
name. **The note therefore proposes the archive**, on the ground that the
high-water mark's precondition is contradicted by the live series rather than
on the ground that an archive is tidier. It remains a proposal.

**Filesystem shape.** Proposed `_queue\T{n}\done\`, following the shape now
live at `_queue\T1\done\`.

**A question that must be ruled before implementation, not assumed.** Moving a
swept file into `done\` is the obvious implementation, and DEC-0019 states that
the driver **deletes nothing, ever**. Whether a rename within the queue root
constitutes a deletion for the purposes of that property is not answered
anywhere in the ruled record. It is not a quibble: the property is one of three
the register calls structural rather than intended, and
`tests/harness/test_queue_driver.py` asserts the related never-imports-subprocess
property so that it is checked rather than promised. A design that quietly
reads "move" as "not a delete" would be deciding a structural property by
implementation convenience.

Two shapes are available and the choice belongs to the Chair:

- **Move.** Simplest, keeps the outbox small, and requires the ruling above.
- **Copy-plus-marker, or a marker alone.** Leaves the original in place and
  writes a terminal marker, so nothing is removed from where it was. Avoids the
  ruling entirely at the cost of an outbox that grows without bound, which
  re-raises retention — the spec's OPEN-5, still open.

**Bounding.** As with (a), every write and any rename stays inside the queue
root and remains bounded by `_assert_within_queue` unchanged.

### 2.3 Why they are not one mechanism

They act on different objects — a Gmail draft on the inbound leg, a filesystem
outcome file on the return leg. Their triggers are different — a refusal
decision versus a successful sweep. Their failure directions are different —
(a) re-pages an item that was correctly rejected, (b) re-alerts an item that was
correctly processed. And under the proposal above their remedies live in
different layers: (a) is principally a Gmail relabel with a filesystem record,
(b) is principally a filesystem transition with no Gmail component. **A single
mechanism could not cover both without one of the two being implemented as an
afterthought.**

---

## 3. Empirical basis — cited, not invented

### 3.1 Four live instances of the refusal shape

1. and 2. **The two 21 August mis-window refusals of PROMPT 139.** Manual
   carriage left them as terminal-only text. This is the defect in vivo: the
   refusal was correct and it terminated nowhere the driver could see.
3. and 4. **The two 22 August BLOCKED-RULINGs** — the refusal of the envelope
   staged as PROMPT 141, and the STEP-0 rooting halt.

### 3.2 The `dead\` / `done\` split is a prototype, not a layout

The manual disposition of the 22 August pair produced a filesystem shape that
is now live in the queue root: `_queue\T1\dead\` holding the refused item, and
`_queue\T1\done\` holding the discharged one.

**This note cites that split as the design's empirical starting point and does
not assume it as ruled layout.** No ruling establishes it; it was produced by
hand under two specific dispositions. Its value is that it is the only observed
instance of the shape the design must automate, which is a better starting
point than an invented one and a worse one than a ruled one. The note
**proposes that it be ratified** — that proposal is Decision Register items 3
and 5, and until ruled the shape remains illustrative.

### 3.3 The MCP carriage constraint — established by probe, 22 August, lane T2

Probed live rather than reasoned about:

| Call | Result |
| --- | --- |
| `list_drafts` | works — metadata and body |
| `get_message` on a **draft** | refused: "The caller does not have permission" |
| `get_thread` on a **draft** | refused: "The caller does not have permission" |
| `get_message` on an ordinary inbox message | **works** |

The same call succeeding on an ordinary message and failing on a draft
establishes that **the limitation is draft-specific rather than a blanket
content-read block.** The connector cannot read draft message content or
attachments at all.

**The consequence is a closed option, and it belongs in the design record
because it closes it on evidence rather than on preference: MCP is not a viable
carriage path for an attachment-borne envelope.** Only the driver's own OAuth
path holds the scope. Body-borne drafts remain readable, which is why the
body-borne carriage variation used to deliver PROMPT 156 works at all. Any
future proposal to replace the driver's Gmail leg with the MCP connector is
answerable today, for attachments, with a no.

The constraint is recorded with its date and method because a permission
surface can change; what is established is the state on 22 August 2026 and the
method by which a future session can re-establish it in three calls.

---

## 4. Sibling defects and sequencing

The spec lists these at its section 3.3 as siblings, expressly **not** part of
QD-F2, with sequencing deferred to this note. This section proposes options and
does not rank them.

### 4.1 The siblings

**F1 — Gmail invents an `http://` scheme on bare paths.** Two live instances,
both on ordinary governance traffic rather than contrived input:

1. The 21 August staged draft's bare outcome-file path, corrupted into an
   invented `http://` redirect URL — F1 occurring in transport on the document
   that specifies its own register.
2. **New, 22 August:** the PROMPT 156 release prompt's inbox path arrived
   wrapped in backtick decoration. It was caught by the F1 guard written into
   the release prompt itself, which instructed the reader to strip the
   formatting and treat the filename as authoritative. **The guard worked**, and
   the instance is worth recording for that reason as much as for the defect:
   it is the first case in this family where the corruption was anticipated in
   the artefact and neutralised on arrival rather than discovered afterwards.

**Lazy-auth-inside-retry.** Authorisation must move outside the retried call,
or any network flap re-prompts human consent.

**Driver deps not yet in `pyproject.toml`.** Marked in the source as Tier 2 and
"its own act". This is why DEC-0019 counts three follow-on landing acts where
the register lists four items, as the spec's section 2 records.

### 4.2 An observation that bears on sequencing, raised as a question

The withholding names QD-F2 as **the** gate on unattended operation. Taken
literally, QD-F2 landing would satisfy it.

**But lazy-auth-inside-retry has the same character.** An unattended run in
which a network flap triggers a prompt for human consent is not running
unattended — it is halted, waiting for a person, which is the condition
unattended operation exists to remove. The two defects are different in
mechanism and identical in effect on the unattended claim: QD-F2 makes the
escalation channel untrustworthy by flooding it, lazy-auth makes the run itself
stoppable by a human gate.

This note does **not** assert that the withholding is under-specified. It
observes that the question is open on the face of the record and routes it to
the Chair as Decision Register item 8, because it changes what "QD-F2 lands"
buys.

### 4.3 Sequencing options

Presented with rationale, deliberately **not ranked**.

**Option 1 — QD-F2 alone, then consider the lift.** Rationale: it is the named
gate, and the register says so in terms. Fastest route to the question. Risk:
if item 8 resolves against it, the lift does not follow and the option has only
moved the question.

**Option 2 — QD-F2 with lazy-auth, then consider the lift.** Rationale: answers
the "unattended means unattended" objection before it is put, and the two
together are what an unattended run actually requires. Cost: couples a defect
the register did not name as the gate to the one it did.

**Option 3 — All three follow-on landing acts (F1, QD-F2, lazy-auth), then
consider the lift.** Rationale: matches DEC-0019's own framing of three owed
acts, and leaves no transport defect outstanding when traffic multiplies. Cost:
the largest scope before any lift, and F1 has a working mitigation in the guard
convention shown at 4.1.

`pyproject.toml` deps sit outside all three: the source marks the item as its
own act, and nothing in QD-F2 depends on it.

---

## 5. The withholding

**Restated, and not lifted here.** The 60-second unattended loop is WITHHELD
until QD-F2 lands. Single-pass and attended operation are authorised.
**Lifting the withholding is a Chair ruling, not a consequence of code
landing** — the next-0020 candidate, cited as next 0020 and not as a claim that
the entry exists.

The reasoning DEC-0019 records for keeping the withholding in the register
rather than only in a session record applies directly to this design: a
repeating loop that re-pages on a refused draft is an escalation channel
training its reader to ignore it. That is what makes QD-F2 a precondition for
the channel meaning anything once nobody is at the prompt, rather than a
tidiness fix.

### 5.1 Proposed acceptance criteria for a lift

Offered so that the lift becomes checkable rather than a judgement call. **These
are proposed, not adopted** — Decision Register item 10.

1. **A refused item pages exactly once.** Demonstrated by inducing a deliberate
   refusal and running **N consecutive polls at the 60-second cadence**, with
   exactly one page observed across all N. Single-pass evidence cannot establish
   this, because the defect is by construction invisible in one pass.
2. **A swept outcome file alerts exactly once**, demonstrated the same way.
3. **Nothing was deleted.** File counts across the queue root conserved before
   and after, consistent with the DEC-0019 property, and reconciled against
   whichever shape section 2.2 is ruled into.
4. **The refused item's evidence is present and readable** — the refusal report
   located, and its preserved bytes hashing to the value recorded at refusal
   time, per B2's raw-bytes discipline.
5. **Probe expectations stated per response class, not per table.** The
   check-method instance of 2026-08-19 established that one pass condition
   cannot serve two response classes whose observable signatures are opposite.
   A refusal that pages once and a success that pages not at all are different
   signatures and need separately stated expectations.

**A limit on criterion 1 that should not be discovered later.** These criteria
establish that the mechanism works. They do not establish that a human sees the
one page that is emitted — WS-E 75's limit is untouched by anything proposed
here, and no arrangement of these probes reaches it.

---

## 6. Decision Register for the Chair

Every point at which this note proposes rather than derives, phrased as a
rulable question. Numbers are for reference in a ruling, not priority.

1. **Is Gmail-side relabel-on-refusal adopted as the load-bearing terminal
   state for mechanism (a)?** The note proposes it on the ground that the
   success path already relabels, so the refusal path is asking for an existing
   act rather than a new class of act. (Section 2.1.)
2. **Does the refusal record carry the envelope bytes with a header block, or
   the bytes plus a sidecar?** The two differ in whether the preserved bytes
   remain independently hashable without parsing. (Section 2.1.)
3. **Is `_queue\T{n}\dead\` ratified as the layout**, or does the T1 prototype
   remain illustrative? (Sections 2.1, 3.2.)
4. **Archive or high-water mark for mechanism (b)?** The note proposes the
   archive, on the evidence that the series is non-monotonic and a positional
   mark's precondition therefore fails. (Section 2.2; spec OPEN-2.)
5. **Is `_queue\T{n}\done\` ratified as the layout?** (Sections 2.2, 3.2.)
6. **Does a rename within the queue root constitute a deletion for the purposes
   of DEC-0019's deletes-nothing property?** This must be ruled before
   implementation; the alternative shape, copy-plus-marker, avoids the question
   at the cost of unbounded outbox growth. (Section 2.2.)
7. **Do mechanisms (a) and (b) land as one act or two?** The source treats them
   as one family under one label and does not rule that they land together.
   (Spec OPEN-7.)
8. **Does lifting the withholding require lazy-auth-inside-retry as well as
   QD-F2**, given that an unattended run which re-prompts for human consent is
   not unattended? (Section 4.2.)
9. **Which sequencing option is adopted** for QD-F2 against F1, lazy-auth and
   the `pyproject.toml` deps? (Section 4.3.)
10. **Are the proposed acceptance criteria at section 5.1 adopted** as the test
    a lift must pass?
11. **Retention and expiry of terminal-state items** — ruled now, or deferred
    with the question recorded? The copy-plus-marker shape at item 6 makes this
    urgent rather than theoretical. (Spec OPEN-5.)
12. **Is the refusal report's destination settled** by the existing ERROR page
    and log row plus the new dead-letter record, or does it need a further
    channel? (Spec OPEN-4.)

### 6.1 Spec OPEN items carried forward, not closed by this note

- **OPEN-1**, where terminal state lives — addressed by proposal at items 1
  to 3, closed only when those are ruled.
- **OPEN-3**, what a high-water mark is keyed on — becomes moot if item 4 is
  ruled to the archive, and is otherwise still open.
- **OPEN-6**, the commissioning checklist is not in the tree. Untouched by this
  note and not resolvable within it; the TLS dual-stack rule and OAuth
  test-user gate still have no in-tree target.

---

## 7. What this note does not do

It implements nothing. It takes no decision. It does not lift the withholding,
does not ratify the `dead\` and `done\` layout, and does not close any of the
spec's OPEN items — each is either carried forward or converted into a question
above. QD-F2 Step 2, implementation, is gated on the Chair ruling this
register.
