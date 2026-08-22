# RB ruling dossier — RB-1, RB-2, RB-3, 21 August 2026

**What this is.** A batched decision paper for three boundary questions raised as
OPEN and NOT DECIDED at `docs/governance/QUEUE_CYCLE_2026-08-21.md` section 3,
prepared under PROMPT 140 so the three can be ruled in one sitting.

**What this is not.** It is not a decision and consumes **no register number**.
It carries no recommendation: each chapter ends at a numbered decision ask, and
where the ruled record is silent the gap is marked **OPEN** rather than filled
with the author's judgement. Where the record already binds a question, it is
transcribed and cited rather than re-derived.

**One premise conflict is reported and deliberately not resolved** — see chapter
RB-3 section 2(e). It affects what RB-3 is actually asking, so it is raised
before the options rather than inside them.

---

## Chapter RB-1 — does the instrument boundary reach writes outside the repository?

### 1. The question, verbatim as raised

> **RB-1 — Does DEC-0018/AMD-A4's instrument boundary reach writes OUTSIDE the
> repository?** The clause requires all file writes via the Write and Edit tools
> and forbids shell-redirection writes. Its stated purpose is instrument
> discipline over governed artefacts. Scratchpad and temp-directory writes are
> neither governed artefacts nor inside the evidence perimeter, so a narrow
> reading exempts them; a wide reading holds that the boundary is about the
> *instrument* rather than the *destination*, and that an executor who keeps two
> sets of habits will eventually apply the wrong one to the wrong tree. The cost
> of the wide reading is friction on genuinely disposable files; the cost of the
> narrow reading is that the discipline has an exception whose edge must be
> judged correctly every time.

Origin: `docs/governance/QUEUE_CYCLE_2026-08-21.md` section 3, written under
PROMPT 132.

### 2. Ruled context

**(a) The clause itself, verbatim** (`DECISIONS.md`, DEC-0018/AMD-A4 as ratified
2026-08-21):

> A4. STANDING TOOL-DISCIPLINE CLAUSE. The instrument boundary (all file writes
> via Write/Edit tools; Bash read-only unless expressly granted; no
> shell-redirection writes per WS-E 76; no 2>&1 per WS-E 73 hygiene) is a
> standing clause incorporated into every envelope by reference. Envelopes state
> only deltas.

**The text says "all file writes" and names no destination.** It is silent on
scope, which is why the question is genuine rather than pedantic: the phrase
supports the wide reading on its face, and the clause's *purpose* — instrument
discipline over governed artefacts — supports the narrow one.

**(b) The guard already ignores the destination, and this is probe-established
rather than inferred.** `docs/governance/WS-E_INCIDENTS.md` item 76, amendment
block (c):

> **THE DESTINATION IS NEVER CONSULTED — now isolated rather than inferred.**
> Every denied probe wrote outside the repository entirely or had no write target
> at all. Not one had a protected destination.

So the mechanical control that exists today draws **no repository boundary at
all**. A ruling for the narrow reading would place the *rule* and the *guard* on
different sides of a line the guard cannot see.

**(c) The originating incident already involved an outside-tree write.** Item 76
records that the refused command's two write targets were "a scratchpad file
outside the tree and `CLAUDE.md`". The outside-tree destination is not a
hypothetical raised by this question; it is in the incident that produced the
rule the question is about.

**(d) Instrument asymmetry — the sharpest fact bearing on this chapter.** Item
76, amendment block (d):

> The file-write instrument is evaluated by its DECLARED TARGET PATH; shell
> commands are evaluated by a TEXT SCAN of the command. Identical content — the
> same two protected path strings — passes through the file tool and is denied
> through the shell. **Effective coverage therefore differs by INSTRUMENT rather
> than by ACT.**

This says the choice of instrument changes what the control can see, everywhere,
independent of destination.

**(e) OPEN — no ruled source states the boundary's destination scope.** Searched:
`DECISIONS.md` DEC-0018 and its amendment note, both riders, the A6 correction,
`docs/governance/WS-E_INCIDENTS.md` items 73, 75, 76 and 77, and
`docs/governance/GOVERNANCE_REVIEW_CHANGELOG.md` CL-31. None addresses whether
the clause reaches outside the tree. **The record is silent and this is a gap,
not an answer.**

**(f) Live interaction with AMD-A6, evidenced this session.** PROMPT 137 granted
`git commit` while withholding `Write` of any new file. Under the wide reading
that combination forecloses the house message-file convention, because the
message file is a new file outside the repository; under the narrow reading it
does not. The envelope was executed with the message supplied on stdin and the
tension disclosed as an AMD-A6 observation — *"an envelope must not grant an act
its own tool discipline forecloses"*. **How RB-1 is ruled determines whether that
grant was self-inconsistent or unremarkable**, and therefore how future grants
must be written.

### 3. Options

**Option 1-A — WIDE: the boundary is about the instrument and applies to every
destination.**
*Closes:* the two-habits risk; makes the rule and the guard agree, since the
guard consults no destination (2(b)). Removes any edge to judge.
*Opens:* friction on genuinely disposable files, and a standing AMD-A6 hazard —
every envelope granting a commit or a PR body must also grant `Write`, or it
forecloses the house convention by construction (2(f)).

**Option 1-B — NARROW: governed artefacts only; outside-tree writes exempt.**
*Closes:* the friction, and the AMD-A6 hazard at 2(f).
*Opens:* an exception whose edge must be judged correctly on every act, and a
divergence between the rule and the guard (2(b)) — a shell-redirection write to
the scratchpad would be rule-compliant and still guard-denied whenever the
command text carries a protected string. **That combination is worse than either
reading alone**, because the executor would be following the rule and refused
anyway, which is the false-RED shape item 76 already records.

**Option 1-C — HYBRID: wide by default, with a named exemption declared per
envelope.**
*Closes:* both costs in principle, and keeps the exemption visible in the
envelope rather than in the executor's judgement.
*Opens:* a new declaration obligation on every envelope, and the question of
what happens when the declaration is absent — which must be answered as
refuse-by-default or the exemption becomes the rule by omission.

**Interaction with RB-3.** A narrow or hybrid ruling makes scratchpad staging
available as a route for very large content, which changes RB-3's option space
materially. **RB-1 should therefore be ruled before RB-3**, or RB-3 ruled
conditionally on it.

### 4. Evidence the Chair needs

| For | What must be true | Exists today? |
|---|---|---|
| 1-A | Friction is tolerable | **Exists** — this session ran two full landings under the wide reading; the only casualty was the message-file convention at 2(f) |
| 1-B | The two-habits risk does not materialise | **Does not exist, and the record points the other way** — WS-E 77 records the pull toward shell writes as a per-turn instruction, and one realised breach on the day it was raised |
| 1-B | Rule and guard divergence is acceptable | **OPEN** — nobody has assessed the rule-compliant-but-refused case |
| 1-C | A default for the absent declaration | **OPEN** — needs ruling, not evidence |

### 5. Decision ask

1. Does AMD-A4's instrument boundary reach writes outside the repository — wide
   (1-A), narrow (1-B), or hybrid (1-C)?
2. If narrow or hybrid, what is the disposition of the rule-compliant-but-
   guard-refused case at 3/1-B?
3. If hybrid, is an absent exemption declaration refuse-by-default?
4. Consequentially: must every envelope granting `git commit` or `gh pr create`
   also grant `Write`, so that AMD-A6 self-consistency holds (2(f))?

---

## Chapter RB-2 — is the no-`2>&1` rule standing discipline or spent hygiene?

### 1. The question, verbatim as raised

> **RB-2 — Is the no-`2>&1` rule standing discipline, or guard hygiene made
> obsolete by fix F2 of 2026-08-19?** WS-E 73 established that the `>` inside
> `2>&1` read as a write construct to the guard, so a read-only command naming a
> protected path was refused. Fix F2 taught the guard to distinguish a descriptor
> duplication from a file redirection, and the re-probe confirmed that a read
> carrying `2>&1` now executes. If the rule existed only to route around that
> defect it is spent. If it is standing discipline — on the ground that the
> construct interleaves two streams into one capture and makes an error's origin
> unrecoverable from the transcript — then it survives its original occasion and
> should be restated on its own reasoning rather than left as a repealed
> workaround nobody repealed.

Origin: `docs/governance/QUEUE_CYCLE_2026-08-21.md` section 3.

### 2. Ruled context

**(a) The clause labels the rule as hygiene and attaches it to WS-E 73 by name.**
AMD-A4 reads "no 2>&1 per WS-E 73 hygiene". The word *hygiene* and the explicit
attachment to a single incident are textual support for the spent reading.

**(b) The defect it routed around is DISCHARGED, and probe-established.**
`docs/governance/WS-E_INCIDENTS.md` item 73, DISCHARGE NOTE 2026-08-19:

> **(a) DISCHARGED by the F2 fix at PR #143, 2026-08-19** — the fix that stopped
> treating `2>&1` as a write construct, distinguishing a descriptor duplication
> from a file redirection.

> **(b) EVIDENCE — the entry's own probes, re-run.** … the fourth — this entry's
> only refusal — now EXECUTES.

Corroborated from the other side at item 76, amendment block (b): *"Tokens that
DO NOT trigger: descriptor duplication `2>&1`, and pipes."* Sources:
`docs/governance/ARCA-R-0152_2026-08-19.md` (nine probes) and its part A re-run.

**(c) THE CRUX, and it cuts against the spent reading. AMD-A4 was ratified on
2026-08-21 — two days AFTER F2 landed on 2026-08-19.** The prohibition was
therefore re-enacted into standing law *after* the defect it names had been
fixed and the fix independently confirmed. Two readings follow and the record
does not choose between them: the Chair carried it forward deliberately as
standing discipline, or it was carried by inertia in a clause being ratified as
a whole. **This is the question RB-2 actually turns on**, and it is not
answerable from the artefacts — only the Chair knows which it was.

**(d) OPEN — the transcript-forensics ground is UNEVIDENCED in the record.** The
question as raised offers a candidate independent basis: the construct
interleaves two streams into one capture and makes an error's origin
unrecoverable. **No ruled source states this**, and a search of the incident
register found **no recorded instance of `2>&1` causing a misattribution.** The
nearest thing is the opposite — a case where the distinction was successfully
kept without the construct being involved at all, at
`docs/governance/ARCA-R-0152_2026-08-19.md` part A, probe A2: *"exit 1 is GIT'S
OWN answer… It is NOT a guard denial. Per the WS-E 74 probe-spec lesson, a
tool's own error and a guard result are different facts and collapsing them is
how a table produces false rows."* That is the failure mode the construct could
create, recorded as a discipline that held — not as a failure that occurred.

**(e) A related rule that is NOT this one, kept separate to prevent conflation.**
The probe-spec expectation rule at `CLAUDE.md` queue item 8 (2026-08-19 instance)
requires pass conditions stated **per tier**, because an approved ask and a live
deny have opposite observable signatures. That governs how a probe result is
*interpreted*; RB-2 governs whether a shell construct may be *used*. They meet
only in that both are about telling a tool's own error from a guard's refusal.

### 3. Options

**Option 2-A — SPENT: repeal, and restate AMD-A4 without the clause.**
*Closes:* a rule whose stated basis is discharged, which is the
repealed-workaround-nobody-repealed shape the question names.
*Opens:* if the transcript-forensics ground is real but unevidenced (2(d)), a
repeal discards it before it was ever tested.

**Option 2-B — STANDING, restated on its own reasoning.**
*Closes:* the ambiguity, and puts the rule on a basis that survives its
occasion.
*Opens:* the obligation to state that basis, which requires the Chair to supply
reasoning the record does not currently hold (2(d)).

**Option 2-C — RETAIN UNCHANGED.**
*Closes:* nothing.
*Opens:* the worst combination — a live prohibition whose only cited ground is
an incident marked DISCHARGED in the same register, which any careful reader
will notice and none can resolve.

**Option 2-D — NARROW: forbid only where the construct could obscure a guard
refusal from a tool's own error.**
*Closes:* the specific forensic risk while releasing ordinary use.
*Opens:* an edge to judge per command, and a dependency on the WS-E 73/76
unification decision, which is **owed and unmade** (carried as item (b) of the
STILL OWED list in `docs/governance/ARCA-R-0153_2026-08-19.md`).

### 4. Evidence the Chair needs

| For | What must be true | Exists today? |
|---|---|---|
| 2-A | The F2 discharge holds | **Exists, probe-established** — item 73 discharge note (b); item 76 amendment (b) |
| 2-A | No independent ground survives | **OPEN** — 2(d): unevidenced, not disproved |
| 2-B | An independent ground, stated | **Does not exist in the record** — must be supplied by the Chair |
| 2-B / 2-C | Whether the 21 Aug re-enactment was deliberate | **OPEN, and only the Chair can answer** (2(c)) |
| 2-D | The WS-E 73/76 unification decision | **Owed and unmade** |

### 5. Decision ask

5. Was the `2>&1` prohibition carried into AMD-A4 on 2026-08-21 **deliberately**,
   knowing F2 had discharged its stated basis two days earlier?
6. Is the rule spent (2-A), standing on restated grounds (2-B), retained
   unchanged (2-C), or narrowed (2-D)?
7. If standing or narrowed, what is its ground, given the record holds none?
8. Does this ruling wait on the WS-E 73/76 unification decision, or precede it?

---

## Chapter RB-3 — the sanctioned Write-tool pattern for very large files

### 1. The question, verbatim as raised

> **RB-3 — What is the sanctioned Write-tool pattern for very large files?** The
> instrument boundary forecloses the heredoc route, and a single very large Write
> has a failure mode observed on 2026-08-21: the write is attempted whole and
> fails on size, leaving nothing. The alternative is Write-then-Edit-append by
> section, which lands incrementally and is recoverable, at the cost of a
> multi-act write whose intermediate states are each a partially-written governed
> artefact in the tree. Neither is obviously right, and the question bites
> whenever a transcription act carries a large ruled text — which is the shape of
> most fold ceremonies.

Origin: `docs/governance/QUEUE_CYCLE_2026-08-21.md` section 3.

### 2. Ruled context

**(a) The heredoc route is foreclosed twice over, and the second reason is
independent of AMD-A4.** Beyond the clause itself, item 76's amendment block (b)
lists the heredoc form among the tokens that **trigger** the guard's write-deny
when a protected path string is present. For a governance artefact — which
routinely names protected paths — the heredoc route is denied by mechanism as
well as forbidden by rule.

**(b) OPEN — no ruled source states a Write size ceiling.** None was found in
`DECISIONS.md`, the incident register, or any ruled document. The threshold is
unknown.

**(c) OPEN — it is unestablished whether a failed Write leaves nothing or a
partial file.** The question as raised asserts "leaving nothing". No source
evidences it. **Option 3-A's entire risk profile depends on this**, so it is
flagged rather than assumed.

**(d) In-tree counter-evidence: large single Writes have succeeded.** Three
artefacts were created by single Write calls on 2026-08-21 and are committed on
`main`:

| Artefact | Lines |
|---|---|
| `docs/governance/ARCA-R-0152_2026-08-19.md` | 426 |
| `docs/governance/ARCA-R-0153_2026-08-19.md` | 341 |
| `docs/governance/QUEUE_CYCLE_2026-08-21.md` | 202 |

This establishes that a single Write succeeds at least to 426 lines. It does
**not** locate the ceiling.

**(e) PREMISE CONFLICT — REPORTED, NOT RESOLVED.** The question attributes the
2026-08-21 size failure to **Write**. The incident register attributes it to the
**heredoc**. `docs/governance/WS-E_INCIDENTS.md` item 77:

> The **heredoc reach** was attempted and **failed on size**, so nothing landed
> by it; the attempt is recorded because a reach that fails for an unrelated
> reason is still the instruction being followed.

**Both texts were written on the same day and they disagree about which
instrument hit the size limit.** The consequence is not cosmetic: if the register
is right, then no Write-side size failure has ever been observed, 2(d) shows
Writes succeeding at scale, and **RB-3 as posed rests on a defect that does not
exist** — the question would become "is there a ceiling at all", not "which
pattern handles the ceiling". If the question is right, the register's item 77
understates what happened. **This must be settled before RB-3 is ruled**, and it
is not settled here.

### 3. Options

Each is stated on the assumption that a Write ceiling exists somewhere; if 2(e)
resolves against that, options 3-B and 3-C are moot.

**Option 3-A — single Write always.**
*Closes:* the partially-written-artefact concern; every artefact is atomic in the
tree.
*Opens:* an unbounded failure at an unknown threshold (2(b)), with an unknown
failure mode (2(c)).

**Option 3-B — Write-then-Edit-append by section.**
*Closes:* recoverability; each section lands or does not.
*Opens:* intermediate states that are partially-written artefacts. **Consequence
worth stating precisely:** under the governed route those intermediates exist
only in a working tree on a feature branch before any commit, so they are not
artefacts of record unless a commit is taken mid-sequence — which narrows but
does not eliminate the concern, and does not address an interrupted session
leaving a half-written file on disk.

**Option 3-C — threshold rule: single Write below a stated size, sectioned
above.**
*Closes:* both, in principle.
*Opens:* it requires the threshold, which nobody has (2(b)), and a threshold set
by guess would be a number presented as a measurement.

**Option 3-D — Write plus mandatory verification read-back.**
*Closes:* the silent-partial-write risk directly, whatever the pattern; this is
the discipline already used for the ARCA-R transcriptions, where the landed body
was hash-compared against its source.
*Opens:* nothing by itself — it is orthogonal to 3-A/3-B/3-C and could be ruled
alongside any of them.

**Interaction with RB-1.** If RB-1 is ruled narrow or hybrid, scratchpad staging
becomes available and a further option opens that does not exist under the wide
reading. **RB-3 is therefore downstream of RB-1.**

### 4. Evidence the Chair needs

| For | What must be true | Exists today? |
|---|---|---|
| Any option | Which instrument failed on size, 21 Aug | **CONFLICTED** — 2(e); must be settled first |
| 3-A | The ceiling is above realistic artefact sizes | **Partially exists** — 426 lines demonstrated (2(d)); ceiling unknown |
| 3-A | A failed Write leaves nothing rather than a partial | **OPEN** (2(c)) |
| 3-C | A measured threshold | **Does not exist**; producing it needs a probe, not granted here |
| 3-D | Read-back is practicable | **Exists** — used for both ARCA-R transcriptions |

### 5. Decision ask

9. Which instrument failed on size on 2026-08-21 — Write, or the heredoc (2(e))?
   RB-3 cannot be ruled soundly until this is answered.
10. If a Write ceiling is established to exist: which pattern is sanctioned —
    3-A, 3-B, or 3-C?
11. If 3-C, what threshold, and on what measurement?
12. Is a verification read-back (3-D) made mandatory for large artefact writes,
    independently of the pattern chosen?

### 6. CORRECTION — ruled 22 August 2026

**Appended under PROMPT 154, lane T1.** The chapter above is retained unaltered;
this section is additive and supersedes it where they conflict. Ruling and
reasons: `docs/governance/RULINGS_RECORD_2026-08-22_sitting.md` Item 4.

> CORRECTION (ruled 22 Aug 2026): the premise event did not occur. Fact ruled verbatim: instrument = Write, single call, 690 lines / 40,076 bytes, succeeded; no size failure on 21 Aug 2026. RB-3's original failure question is discharged as misconceived. This section supersedes the RB-3 statement above; original text retained unaltered for the record.

> SUCCESSOR ITEM (reserved, unnumbered by ruling): 'What is the demonstrated ceiling for single-Write artefacts, and does the house need an explicit one?' Register number to be consumed at a deliberately chosen later transcription, not by this envelope. Deferred probe attached to this item.

**Consequences for the chapter above, stated so a reader does not have to
derive them.**

- **2(e), the premise conflict, is RESOLVED** — and resolved in favour of the
  incident register. The question attributed the 21 August size failure to
  Write; the ruled fact is that the Write succeeded. Item 77's attribution of
  the size failure to the heredoc therefore stands, and the register did not
  understate what happened.
- **2(d)'s demonstrated floor moves from 426 lines to 690 lines / 40,076
  bytes.** The table above remains accurate as to the three artefacts it lists;
  it is simply no longer the largest single Write on record. The ceiling is
  **still not located** — a floor is not a ceiling, which is precisely the gap
  the successor item is reserved against.
- **Decision asks 9 to 12 are spent as posed.** Ask 9 is answered by the ruled
  fact. Asks 10 and 11 were conditional on a Write ceiling being established to
  exist, and none is; they do not arise. Ask 12, the read-back question, is not
  ruled here and is **not** carried by the successor item — it survives as an
  open question of practice, noting that read-back was in fact used to verify
  every artefact written under this envelope.
- **2(b) and 2(c) remain OPEN and are re-homed.** The Write size ceiling and the
  failure mode of a failed Write are the substance of the reserved successor
  item, together with its deferred probe. They are no longer RB-3 residue.

**On the reserved number.** The successor item is deliberately unnumbered. Per
the standing convention, it is cited as "next" and never as a bare number until
the register number is consumed at a later transcription — a bare number reads
as a claim that the item already exists.

**Standing flexibility principle applies** to this correction as to every ruling
of the 22 August sitting: binding for current direction, not irreversible
architecture.

---

## Interaction map — how the three sit together

**A ruling order is implied by the dependencies and is stated so the batch can
be taken in one sitting.**

1. **RB-1 first.** It is the only one of the three with no upstream dependency,
   and it feeds RB-3 (a narrow or hybrid ruling opens a scratchpad-staging
   option that does not otherwise exist) and it settles the AMD-A6 grant-writing
   consequence at RB-1 2(f), which binds every future envelope.
2. **RB-3 second, and only after its premise conflict at 2(e) is settled.** The
   conflict is a question of fact about 21 August, not a matter of judgement.
3. **RB-2 is independent of both** and can be ruled in any position. Its only
   dependency is internal: option 2-D leans on the WS-E 73/76 unification
   decision, which is **owed and unmade**.

**Against owed items elsewhere:**

- **WS-E 73/76 unification** (owed; `docs/governance/ARCA-R-0153_2026-08-19.md`
  STILL OWED item (b)) — gates RB-2 option 2-D only. A ruling of 2-A, 2-B or 2-C
  does not wait on it.
- **Item 34 M2** (`CLAUDE.md`) — RB-3 is the instrument question for exactly the
  act M2 describes: fold ceremonies transcribing large ruled texts. If M2 is ever
  mechanised, the sanctioned pattern is what it must implement, so RB-3's answer
  becomes a build constraint rather than a habit.
- **F5 / queue item 48** (`CLAUDE.md`; CL-31 in
  `docs/governance/GOVERNANCE_REVIEW_CHANGELOG.md`) — F5 moves envelope
  resolution **inside** `.claude/hooks/governance_guard.py`. RB-1 and RB-2 both
  concern what that guard should see and refuse, so **an F5 design settled before
  RB-1 and RB-2 would be designing against an undecided rule.** The relationship
  is stated; whether F5 waits is not this dossier's to decide.
- **CL-31** — records the harness-uplift disposition and parks the settings-side
  deny into F5. It consumes the CL number for that disposition; **this dossier
  consumes none.**

**OPEN gaps, collected.** RB-1 2(e), the destination scope, unaddressed anywhere.
RB-1 3/1-B, the rule-compliant-but-guard-refused case, unassessed. RB-1 3/1-C,
the absent-declaration default. RB-2 2(c), whether the 21 August re-enactment was
deliberate — **answerable only by the Chair**. RB-2 2(d), the transcript-forensics
ground, unevidenced in the record. RB-3 2(b), the Write size ceiling. RB-3 2(c),
the failure mode of a failed Write. RB-3 2(e), the premise conflict, **a question
of fact and the most urgent of these**.

No control mapping line is carried, for the reason
`docs/governance/QUEUE_CYCLE_2026-08-19.md` states: queue item 34 M11(d) requires
per-class mapping content to be defined once in the control framework, and that
framework does not exist yet.
