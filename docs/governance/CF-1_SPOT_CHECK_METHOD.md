# CF-1 — Architecture conformance spot-check method

**Status: RATIFIED 2026-07-25.** WS-D item 2. Discharges the B7 entry
criterion "CF-1 conformance spot-check design agreed". Binding from B7.

*Reviewed: one external reviewer, concur with one clarification and one
strengthening, both adopted (§7).*

---

## 1. What was missing

Checkpoint 01 established the standing gate question:

> **Architecture conformance (CF-1).** Does this increment conform to
> the Banking Architecture and applicable ADRs?
> → Yes | Deviation recorded as DEC | New ADR required.

The question existed. The method for answering it did not. As things
stood, the honest answer at any gate would have been "yes, as far as I
recall", which is an assertion dressed as a check.

A retrospective audit — reading all code against all rulings at each
gate — was rejected at Checkpoint 01, correctly: it does not scale to a
solo build and it produces a document nobody reads. What replaces it
has to be cheap enough to actually happen.

## 2. The design problem, and the fix

A spot-check chosen at gate close is worthless. Faced with "pick a few
conformance claims to verify" *after* writing the code, the author
picks the ones they already know are fine. The selection is
contaminated by exactly the knowledge the check is supposed to test.

**Conformance claims are nominated at stage entry, in the gate
document, before the code is written.** They are evidenced at exit.
This is the same mechanism as the entry-written gate document itself
and it works for the same reason: the choice is made while the answer
is still unknown.

## 3. Method

**At stage entry**, in a dedicated `CF-1 conformance nominations`
subsection of `BN_GATE.md` — under Entry criteria, **not** under Exit
evidence — nominate **three to five conformance claims**. Each names:

- the ruling, ADR or architecture section it tests;
- what would count as evidence of conformance;
- what a deviation would look like.

**At least one nomination must be a claim the author expects to be
awkward or uncertain.** If, after reasonable effort, no such claim can
be identified, the gate record must state that fact explicitly and
explain why the stage is believed to be fully covered by existing
rulings. A nomination set consisting solely of comfortable claims is a
failed spot-check regardless of the individual results.

That wording is deliberately inspectable: a reviewer reading the Gate
Acceptance Record can tell whether the rule was honoured without having
to form a judgement about the author's state of mind.

**At stage exit**, evidence each nomination in the Gate Acceptance
Record with a path @ SHA, a test, or a written finding. Three outcomes
per claim, matching the standing question:

- **Conforms** — evidence cited.
- **Deviation** — recorded as a DEC. The deviation is not a failure;
  an unrecorded deviation is.
- **New ADR required** — the stage did something the architecture does
  not cover.

**Cost target: under an hour per gate.** If a nomination cannot be
evidenced in roughly ten minutes, it is too broad — narrow it or make
it a CL instead.

## 4. Scope boundaries

- **Spot-check, not audit.** Three to five claims per gate, not
  coverage. Over the remaining stages this accumulates to meaningful
  sampling; at any one gate it is deliberately partial, and the gate
  record says so.
- **Nominations are not carried forward.** Each stage nominates afresh
  against what it is actually building. A claim that failed at one gate
  becomes a CL, not a permanent standing nomination.
- **The boundary test is separate.** The machine-checked
  `platform/` ↔ `verticals/` import check (ADR-0010 §7, and the B9.5 CI
  check) runs continuously and is not a spot-check nomination. CF-1
  covers what a machine cannot check.

## 5. First application — B7 nominations

Nominated 25 Jul 2026, before B7 code exists. Carried in
`docs/build/B7_GATE.md` §1.1; reproduced here as the worked example.

**CF-1/B7-a — R5 vector store (the awkward one).**
Ruling R5 fixes the Phase 2 vector store as a self-managed on-premises
OpenSearch cluster, explicitly excluding managed-cloud stores because
`rm_knowledge` holds customer data. The Build & Quality Plan specifies
ChromaDB for B7. Both can be true — ChromaDB as the reference build's
store, OpenSearch as the target deployment — but **that relationship is
recorded nowhere**, and if it is not stated, the suite says one thing
and the build plan says another.

The substantive risk is not the naming. It is whether B7 writes
ChromaDB-specific calls throughout the retrieval path, in which case
the Phase 2 OpenSearch move is a rewrite rather than a swap. Under
ADR-0009 the retrieval *framework* is platform machinery; the store is
an implementation of it.

- *Evidence of conformance:* a retrieval interface with the store
  behind it; `chromadb` imported in one adapter module and nowhere
  else; a written statement of the ChromaDB-now / OpenSearch-later
  relationship.
- *Deviation looks like:* `chromadb` imported across retrieval,
  ingestion and agent code.
- *Likely outcome:* a DEC recording ChromaDB as the reference-build
  store with OpenSearch as the Phase 2 target, or a note in ADR-0009's
  boundary table.

**CF-1/B7-b — SA5 RAG data classification.**
SA5 classifies `fraud_knowledge` as internal-sensitive. DEC-0011 makes
the corpus synthetic plus an OGL subset, so classification is trivially
satisfied — but the classification must appear in the corpus manifest,
not merely be true in fact.

- *Evidence:* a classification field per manifest entry.
- *Deviation:* manifest carries licence but not classification.

**CF-1/B7-c — ADR-0010 emit coverage.**
Every governed step in B7 emits through the platform wrapper. The
retrieval step is the first new decision point since the trio was
built, and is therefore the first real test of whether the interface is
used rather than bypassed under time pressure.

- *Evidence:* `retrieval_performed` events present in the audit trail
  for a live end-to-end run; no direct writes to audit tables from
  vertical code.
- *Deviation:* retrieval happening outside a wrapper context.

**CF-1/B7-d — R7 retrieval latency rung.**
R7 sets retrieval below 100 ms. B6 explicitly deferred this rung to B7.

- *Evidence:* measurement recorded in the gate document.
- *Deviation:* a measurement above 100 ms is **a finding to record, not
  a gate blocker.** B7's not-allowed list does not include latency and
  that was deliberate — the distinction is to be kept sharp, because a
  slow retrieval that is measured and recorded is a known quantity,
  while a gate blocked on it would invite the number to be massaged.

Four nominations, one uncomfortable. Nothing else in B7 looks genuinely
uncertain against the locked suite, and that statement is part of the
record.

## 6. The R5 tension is left open deliberately

CF-1/B7-a surfaced while designing the method rather than while running
it. The question arises whether to raise it as a CL now.

**It is left as a nomination.** Pre-empting it with a CL would collapse
the check into an entry-time decision and defeat the purpose of
nominating while the answer is still unknown. The method surfacing a
tension early does not require resolving it early.

Outcome paths, so that leaving it open is not the same as leaving it
vague:

- Clean adapter plus a written statement of the ChromaDB-now /
  OpenSearch-later relationship → **conforms**, and a short DEC or a
  note in the ADR-0009 boundary table is enough.
- `chromadb` scattered through the retrieval path → **deviation**,
  recorded as a DEC at exit and raised as a CL then.

## 7. Review disposition

- **§6 clarification — CONFIRMED.** Reviewer concurs that the R5
  observation stays a nomination rather than becoming a CL now.
  Recorded in §6 with both outcome paths written out, so that
  "deliberately open" is distinguishable from "not thought through".
- **Awkward-nomination rule, made operational — ADOPTED as written
  (§3).** The strengthening is worth having: it converts a qualitative
  requirement into something inspectable in the Gate Acceptance Record
  without debate, including the case where no awkward claim can be
  found, which now has to be stated and justified rather than passed
  over.
- **Nominations live under Entry criteria, not Exit evidence —
  ADOPTED (§3).** Implied in the draft, now stated. Carried into
  `B7_GATE.md` as a dedicated §1.1 subsection.
- **B7-d latency distinction kept sharp — ADOPTED (§5).** Reasoning
  added: a gate blocked on latency invites the number to be massaged,
  whereas a measured and recorded slow retrieval is a known quantity.
