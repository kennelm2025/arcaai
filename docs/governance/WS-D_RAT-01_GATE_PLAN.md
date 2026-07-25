# WS-D / RAT-01 — Gate-based plan refresh

**Status: RATIFIED 2026-07-25 (DEC-0010). Binding from B7.**

*Replaces the week column in BUILD_TRACKER.md "Build stages" table.
Ratified from draft 3; drafts 1–3 are working papers and are not
retained in the repo.*

## Review provenance

| Round | Reviewer | On | Outcome |
|---|---|---|---|
| R1 | Grok | Draft 1 | 3 amendments — 2 accepted, 1 accepted with reasoning replaced |
| R2 | Grok | Draft 2 | Concur, no changes; one non-blocking observation |
| R1 | ChatGPT | Draft 2 | Concur with 1 Must-Fix, 2 Should-Fix, 2 minor |

Attribution as captured by the coordinator. Grok R2 and ChatGPT R1 are
independent readings of the same draft and count as two concurrences on
the shape. Grok R1 is not a third — it is the same reviewer on an
earlier draft. Recorded explicitly per WS-E 36.

Draft 3 changes were ChatGPT-originated except where noted. One
ChatGPT recommendation was declined (§8, C2).

---

## 1. The change that matters

The week column is already gone. The temptation is to replace it with
nothing and let the Gate column carry the load. That fails, because of
*when* the gate document gets written.

B5_GATE.md was written at close. So was every gate doc before it. A
gate document written at close is a **report**: it describes what
happened and then declares it sufficient. The criteria are inferred
backwards from the evidence that happens to exist. That is not a gate;
it is a changelog with a stamp on it.

**The gate document is created at stage *entry*, with the exit evidence
section present but empty.** Entry criteria are checked and signed
before the first commit of the stage. Exit evidence is filled as it
lands. The Gate Acceptance Record closes it.

That is the replacement for the week column. The week said *when* a
stage would happen. The entry-written gate doc says *what must be true
before it may start, and what will prove it finished* — decided while
those answers can still be inconvenient. The criteria cannot be tuned
to fit the evidence.

Cost: one extra document write per stage, ~20 minutes.

## 2. Tracker table — new shape

Drop `Wk`. Add `Depends on` and `Gate doc`:

| Stage | Depends on | Scope | DevOps | MLOps | Gate | Gate doc |
|---|---|---|---|---|---|---|

`Depends on` is the second gain. The week column encoded a false claim
— that the stages are a strict chain. They are not. B11 observability
has work that can land against B7 alone; B10 is the *test* of B9.5, not
merely its successor. Naming the dependency makes the DAG explicit and
makes it obvious which stages could be reordered under pressure and
which cannot.

**Standing rule: the tracker links to each `BN_GATE.md` and never
restates its criteria.** Any future "exit criteria" column recreates
the problem this refresh exists to fix — criteria in two places drift,
and the copy in the summary table wins by being easier to read.

## 3. Per-stage gate document — schema

Five sections. Fixed order, fixed headings.

1. **Entry criteria.** Binary, checkable, dated at sign-off.
   Predecessor gate(s) passed; named prerequisites (environment,
   services, data, decisions that must exist first). If an entry
   criterion cannot be answered yes/no by inspection, it is not an
   entry criterion. Each criterion carries an **external-dependency
   flag** (§3.2).
2. **Scope.** From the Build & Quality Plan, restated verbatim. Changes
   to scope require a DEC, referenced here.
3. **Exit evidence.** Each item cites a **path @ commit SHA**, or a
   transcribed CI result (§3.1). "Tested" is not evidence;
   `tests/test_x.py::test_y` green in ci-mlops #NN, at SHA, is
   evidence. Blank at entry, filled as it lands.
4. **Gate questions.** Standing checklist (§4) plus stage-specific
   questions. Answered in prose in the Gate Acceptance Record — the
   answers are the record, not a tick.
5. **Deferrals.** Two lists: *allowed* (may be pushed to a later stage
   without reopening this gate) and *not allowed* (absence blocks the
   gate regardless of what else landed). Written at entry. This is the
   scope-creep brake, and in a solo build it is the only one that works.

**Required versus supporting evidence.** The *not allowed* deferral
list **is** the required-evidence list; everything else under exit
evidence is supporting. One control, one name — no second taxonomy
inside the evidence section. The obligation this creates is that the
not-allowed list must be exhaustive at entry: if an item would block
the gate, it is named there, and if it is not named there it does not
block. Ambiguity about whether a given artefact is gate-blocking is a
defect in the not-allowed list, not a reason for a new axis.

**Vocabulary note.** "Deferrals — not allowed" is this schema's only
term for a blocking exit item. "Must-Fix" belongs to the CL
ratification vocabulary and is not reused here; two names for one
control is how ledgers start disagreeing with themselves.

### 3.1 Evidence citation and immutability

**Evidence immutability.** Evidence cited in a closed gate — commits,
CI results, manifests, reports, hashes — is immutable after gate
closure. Previously accepted evidence is never silently replaced.

A declaration alone does not achieve this, because two of the three
evidence classes are not immutable by nature:

- **Commits are.** A SHA is content-addressed and cannot be edited.
  Therefore: **cite path @ SHA, never a bare path.** A bare path names
  a file whose content will change; `docs/build/B7_GATE.md @ a1b2c3d`
  names a fixed artefact.
- **Branch refs are not.** `main` moves. Never cite `main`.
- **CI runs are not.** GitHub Actions logs and artefacts expire — the
  default retention is 90 days. A gate closed in July citing
  "ci-mlops #53" points at nothing by November, which is roughly when
  an external reviewer would first ask. Therefore: **the CI result is
  transcribed into the Gate Acceptance Record as text** — workflow
  name, run number, conclusion, date, and the commit SHA it ran
  against. The link is a convenience; the transcription is the
  evidence.

**Correction path, graduated.** Not every correction warrants a DEC:

- Transcription error, or evidence that was cited wrongly but exists as
  intended → **addendum to the Gate Acceptance Record**, dated,
  original text struck through and left visible.
- Evidence that turns out not to support what the gate claimed, such
  that the gate should not have passed on it → **DEC**, and the gate
  reopens.

The test is whether the gate decision would have differed. Anything
else is an addendum. Requiring a DEC for typos would train the habit of
fixing them silently, which is the behaviour the rule exists to
prevent.

### 3.2 External-dependency flag

Each entry criterion is marked as either **self-resolvable** or
**externally dependent** — dependent on a third party, a licence, a
regulator's publication, or another person's availability.

The distinction is operational, not administrative: self-resolvable
criteria are cleared by working on them, externally dependent ones are
not, and only the latter need lead time booked before the stage is
anywhere near ready. Known externally dependent criteria today: B7
corpus licence terms, B9's RAT-12 FCA publication check, B12's G10
external domain reviewers, B12's GPU rental.

This replaces a per-criterion ownership column, declined at §8/C2.

## 4. Standing gate checklist (binding from B7)

Applies to every stage. Answered in the Gate Acceptance Record.

- Both pipelines green at the nominated gate commit. **The Acceptance
  Record transcribes workflow name, run number, conclusion, date and
  SHA in text** (§3.1) — not "CI green", not a link that will rot.
- Every decision taken during the stage is recorded as DEC or ADR
  before the gate closes — none in flight.
- WS-E incidents arising in the stage are in the ledger before close.
- **CF-1 conformance spot-check** — platform/vertical boundary
  (ADR-0009) holds for code added in this stage. Spot-check, not audit.
- Provenance manifest (CL-12) covers artefacts added in this stage.
- Open CLs touched by the stage are dispositioned — closed, or
  explicitly carried with a reason.
- All exit evidence cited as path @ SHA (§3.1).
- Gate Acceptance Record signed, gate commit SHA recorded, tracker row
  flipped in the same PR.

The checklist stays stage-agnostic. Anything that applies to one stage
belongs in that stage's gate doc, however tempting it is to make it
universal by writing it here.

## 5. Stages B7–B12

Entry criteria and exit evidence below are the source content for each
gate doc. Scope is unchanged from the Build & Quality Plan. Every
not-allowed list is exhaustive as written and is the required-evidence
list for that stage (§3).

---

### B7 — Fraud RAG (ChromaDB, 50+ seed docs, RAGAS)

**Depends on:** B6.

**Entry criteria**
- B6 gate passed. *(self-resolvable)*
- RAT-02 governance trio landed as pre-B7 work: audit logging,
  execution metadata, request wrapper. All three, not two.
  *(self-resolvable)*
- ChromaDB in the `arcaai` env, version pinned. *(self-resolvable)*
- **Corpus sourcing decision recorded as a DEC. No ingest before it
  exists.** *(externally dependent — licence terms are someone else's)*
  A 50-document seed corpus of UK fraud and financial-crime material
  means FCA Handbook extracts, JMLSG guidance, UK Finance material —
  third-party text with terms that do not contemplate redistribution in
  a repo, even a private one. The choice is synthetic/paraphrased
  corpus, link-and-hash-only with local ingestion outside the repo, or
  per-document licence clearance. Decide before ingesting, not after 50
  documents are committed.
- CF-1 spot-check design agreed (WS-D item 2). *(self-resolvable)*

**Exit evidence**
- **Corpus manifest**: per document — id, source, licence status,
  sha256, ingest date, chunk count, and **retrieval eligibility state**
  (included / pending review / withdrawn / deprecated).
  - Eligibility is **time-versioned, not a mutable flag.** A document
    withdrawn in November must not silently rewrite what was
    retrievable in August: B9 replay needs the eligibility state *as at
    the decision*, and a boolean that flips in place destroys exactly
    the fact replay depends on. Record eligibility as dated
    transitions. This is also how a licence lapse is handled without
    deleting the provenance of decisions already made on that document.
- **Grounding test**: every generated claim carries a chunk id; a
  response containing an uncited assertion fails the test.
- **Negative test**: a query with no supporting document in the corpus
  returns the fallback, not a fluent answer. The single most important
  grounding test and the easiest to omit.
- Confidence threshold + "insufficient evidence" fallback implemented;
  threshold value recorded with the reasoning for it.
- CF-1 spot-check result.
- RAGAS baseline: scores as committed JSON alongside the run config and
  the eval set. Offline. **Recording the baseline is required; passing
  a threshold is not** — B7 establishes the number that later stages
  are measured against, and inventing a pass mark now would be a
  threshold with no evidence behind it.
- Retrieval latency measured against the R7 ladder, recorded. Recorded,
  not gated — G9 was the latency gate and it closed at B5.

**Stage-specific gate questions**
- Can every claim in a generated narrative be traced to a retrieved
  chunk and thence to a manifest entry, by a reviewer with repo access
  and no help from me?
- Does the manifest carry licence status per document, and would that
  status survive a client's procurement review?

**Deferrals — allowed:** reranker; hybrid/BM25 search; corpus beyond 50
docs; any RAGAS pass threshold; latency optimisation; RAGAS in the
request path (rejected outright, candidate 4).
**Deferrals — not allowed:** corpus manifest with provenance, licence
status and time-versioned eligibility; grounding test; negative test;
insufficient-evidence fallback; CF-1 spot-check result.

---

### B8 — Guardrails (Presidio, OPA, grounding, injection detector)

**Depends on:** B7.

**Entry criteria**
- B7 gate passed. *(self-resolvable)*
- RAT-05 threat catalogue seeded, including the three example rules
  from step-change candidate 2 as OPA-before-LLM seed cases.
  *(self-resolvable)*
- RAT-06 precedence hierarchy decided and written down *before* the
  first policy is authored. *(self-resolvable)*
- `prompts/` scaffold decision taken (deferred here from B6).
  *(self-resolvable)*

**Exit evidence**
- Threat catalogue with at least one executable test per entry;
  pass/fail matrix committed.
- **Conflict case, traceable to the catalogue.** A worked example where
  two guardrails disagree while handling a *catalogued* threat — not a
  conflict invented for the demonstration, which can be built to be
  resolvable. The precedence hierarchy resolves it deterministically;
  the resolution and the overridden rule's objection both appear in the
  audit trail. Without this the hierarchy can be written and then
  quietly ignored.
- Every block/redaction emits a reason into the audit trail; test
  proving it, and proving a redaction is distinguishable from a block.
- Injection-detector selection memo — candidates, evaluation method,
  result — recorded as a DEC.
- OPA policy bundle plus sample decision logs showing pre-LLM
  evaluation firing.
- RAT-07 model-risk tiering recorded in the B8 artefacts (candidate 3,
  record only; challenger build rejected).

**Stage-specific gate questions**
- When two guardrails disagree, is the outcome deterministic, and is
  the losing rule's objection still in the record?
- Is a redaction distinguishable from a block in the audit trail, or
  do they collapse into "denied"?

**Deferrals — allowed:** policy coverage beyond the catalogue; Presidio
recall tuning; challenger model build (rejected); UI surfacing of block
reasons.
**Deferrals — not allowed:** threat catalogue with a test per entry;
traceable conflict case; block/redaction reason emission; the
injection-detector DEC.

**Hard trigger on exit:** CL-17/19/20 bundle → next Banking
Architecture revision (RAT-11).

---

### B9 — Chat UI + audit-trail replay (→ WS1.4 artefact)

**Depends on:** B8.

**Entry criteria**
- B8 gate passed. *(self-resolvable)*
- **DEC recording the `outcome_event` contract shape** (step-change
  candidate 1). The DEC settles *what the record looks like*, not
  whether there is one — see exit evidence. It is a scope change to a
  locked stage and needs the entry, but it is not a fork.
  *(self-resolvable)*
- RAT-12 check: has FCA guidance on audit trails / human-in-the-loop
  published? If yes, exceptional-checkpoint trigger fires *before* B9
  design, not after. *(externally dependent — regulator's timing)*

**Exit evidence**
- Audit record schema, versioned, with a migration note.
- **Replay exhibit**: a stored decision replayed end to end. Either it
  reproduces byte-for-byte against pinned model and pinned retrieved
  set, or it does not — and this clause is not to be "improved" into a
  reproducibility claim.
- **Nondeterminism register.** Where exact replay does not hold, the
  answer is not a paragraph explaining why. It is an enumerated list,
  one row per source, each with its bound and what the reviewer may
  rely on instead. Opening set to work from: LLM sampling parameters
  and seed; retrieval ordering and tie-breaks; embedding model version;
  corpus eligibility state at decision time; prompt version; model
  weight pin; ChromaDB index state; library and hardware float
  differences. The register is living — a source discovered later is
  added, not argued away. An auditor can work through a list; they
  cannot work through prose.
- **`outcome_event` contract + append-only table.** Synthetic labels
  acceptable; the point is the shape of the record, not the truth of
  the label. Rationale is SS1/23, not the deck: ongoing model
  performance monitoring is an MRM expectation, and performance cannot
  be monitored against decisions whose outcomes were never recorded. A
  pipeline that can say what it decided but never whether it was right
  leaves the L3/L4 gap open no matter how good the audit trail is.
- One complete worked trace as the WS1.4 artefact: transaction → score
  (with Platt params and model sha) → retrieval set → narrative →
  guardrail decisions → outcome event. One page, readable by a
  non-engineer.

**Stage-specific gate questions**
- Given only the audit record, can a reviewer say *why* this decision
  came out this way — not just what the pipeline did?
- Is the L3/L4 claim-vs-evidence gap closed by the outcome table, or
  merely relabelled?

**Deferrals — allowed:** real outcome labels; any learning loop (out of
scope, explicitly); outcome-driven retraining; UI polish beyond the
trace exhibit.
**Deferrals — not allowed:** the `outcome_event` contract and table;
the replay exhibit; the nondeterminism register; the versioned audit
schema; the worked trace.

---

### B9.5 — Platform Extraction gate (ADR-0009)

**Depends on:** B9. **Tested by:** B10.

**Entry criteria:** B9 gate passed; CF-1 spot-checks from B7–B9 all
clean or their exceptions dispositioned. *(both self-resolvable)*

**Exit evidence**
- Import graph showing `verticals/fraud` importing contracts only, and
  platform importing nothing from `verticals/`. Machine-checked, in CI.
- A second vertical scaffolded from contracts alone — stub, no
  behaviour — proving the boundary is usable, not merely unviolated.

**Gate question:** if this boundary is wrong, B10 is where it hurts.
What would B10 have to look like for us to reopen B9.5?

**Deferrals — allowed:** contract ergonomics; documentation of the
extraction.
**Deferrals — not allowed:** the machine-checked boundary in CI; the
second-vertical scaffold.

---

### B10 — Replicate: Compliance + RM verticals

**Depends on:** B9.5.

**Entry criteria:** B9.5 gate passed; per-vertical scope written before
build (what each vertical does and does *not* replicate). *(both
self-resolvable)*

**Exit evidence**
- Both verticals running end to end.
- **Replication cost, recorded as a number**: files added, lines of
  bespoke code per vertical, and hours. This number is the platform
  claim. It is the single most valuable artefact B10 produces — it
  turns "pipeline as platform" from a slogan into a measurement, and it
  is what a client CTO will ask for.
- Named deviations: anything in a vertical that had to reach past the
  contract, with the reason.

**Gate question:** does the replication cost support the platform claim
in the Banking Architecture as written? If not, the architecture
document changes, not the number.

**Deferrals — allowed:** feature parity with the fraud vertical;
per-vertical model quality.
**Deferrals — not allowed:** the replication cost number; the named
deviations list.

---

### B11 — Observability (Grafana 8 panels, Evidently, kill-switch drill)

**Depends on:** B10 (three verticals to observe).

**Exit evidence**
- Eight panels populated from **real pipeline runs**, not seeded or
  mock data. Screenshot plus the query behind each panel.
- Drift detection fired by a **deliberately drifted batch** — the test
  is that it alerts, not that it exists.
- Kill-switch drill executed: written procedure, time to effect
  measured, what was still in flight when it fired, result recorded.
- Process-intelligence design note (candidate 5) naming the metric
  schema and carrying a version number. Note only; no panels, no
  collection. Versioning the schema costs nothing now and is what makes
  the note referenceable later.

**Gate question:** which of the eight panels would actually change a
decision, and which are there because the deck expects them?

**Deferrals — allowed:** process-intelligence panels and collection;
alert routing and on-call; panel aesthetics.
**Deferrals — not allowed:** eight panels from real runs; the drift
alert fired by a drifted batch; the kill-switch drill result.

---

### B12 — Hardening + demo pack

**Depends on:** B11.

**Entry criteria**
- B11 gate passed. *(self-resolvable)*
- **CL-09 Model Card complete** — RAT-11 puts this before any external
  review, and B12 is where external exposure begins.
  *(self-resolvable)*
- GPU rental plan resolved for the 70B configuration — book at B11
  exit, not B12 start. *(externally dependent)*
- G10 external domain reviewers identified. *(externally dependent —
  longest lead item in the programme)*

**Exit evidence**
- Three demo scripts run end to end **from a clean clone on a clean
  environment**, following deploy guide v0 with no undocumented step.
  Not a run on the dev box — the dev box knows too much.
- Deploy guide v0 with the clean-run transcript as its proof.
- 70B demo configuration exercised at least once.

**Deferrals — allowed:** the 70B run, **if and only if** the GPU rental
plan failed on external grounds, recorded as such — in which case the
demo pack ships with the 8B configuration and the 70B claim is removed
from client-facing material rather than left as an untested assertion.
**Deferrals — not allowed:** the clean-clone run of all three scripts;
deploy guide v0.

---

## 6. Ratified decisions

1. **Gate doc written at entry, not close** (§1).
2. **`Depends on` replaces `Wk`** (§2); criteria out of the tracker;
   tracker links, never restates.
3. **Five-section gate schema** (§3), including the deferrals split and
   the vocabulary note.
4. **B9.5 gets a row** in the tracker table.
5. **B7 corpus licensing → DEC before ingest** (§5, B7).
6. **WS-E candidate 40** — log short.
7. **`outcome_event` contract + table is a non-deferrable B9 exit
   item**, on the SS1/23 monitoring argument.
8. **Evidence immutability and citation** (§3.1) — path @ SHA, CI
   results transcribed because runs expire, graduated correction path.
9. **The not-allowed deferral list is the required-evidence list**
   (§3), and must be exhaustive at entry.
10. **External-dependency flag on entry criteria** (§3.2), in place of
    per-criterion ownership.

## 7. Raised CL candidate

**Board-level KPIs in the Executive Presentation are not anchored to
any build artefact.** Surfaced by Grok while arguing its B11 amendment.
Real finding, wrong home — it is a document-currency defect, not a gate
criterion, and forcing it into the B11 gate would make the standing
checklist carry a deck's obligations. Raise as a CL against the
Executive Presentation and consider it for the CL-17/19/20 bundle at
the next Banking Architecture revision.

## 8. Review disposition

### Grok R1 on draft 1

- **B9 outcome capture — ACCEPTED, reasoning replaced.** The amendment
  was right: an entry-criterion DEC with "if rejected, B9 is unchanged"
  was too soft, and the contract plus table belong in the
  non-deferrable exit list. The *reason* offered — the architecture
  already sold closed-loop, so the build must show the pipe — was
  rejected. That is scope driven by a deck, and it is the same move
  refused at B10, where the rule is that the architecture changes to
  match the measured number rather than the reverse. The recorded
  reason is SS1/23. Implementation splits the either/or: the DEC stays
  as an entry criterion but settles shape, not existence; existence is
  an exit item.
- **B8 conflict case — ACCEPTED, tightened.** Conflicts between
  guardrails are not themselves catalogue entries, so the requirement
  is that the conflict arises while handling a catalogued threat and is
  traceable to that entry.
- **B11 metric schema — ACCEPTED in substance, RELOCATED.** The
  standing checklist is stage-agnostic; a metrics requirement applies
  to one stage. Moved to B11 exit evidence. The underlying worry about
  unanchored KPIs is separated out as a CL (§7).

### ChatGPT R1 on draft 2

- **C3, evidence immutability (Must Fix) — ACCEPTED and extended**
  (§3.1). Right catch, right severity. Its own observation that "the
  commit hash almost gives you this" understates the gap: commits are
  immutable, but branch refs and CI runs are not, and CI is where this
  actually fails. GitHub Actions logs expire at 90 days by default, so
  a gate closed in July citing a run number points at nothing by
  November — roughly when an external reviewer would first look. A
  declaration cannot fix that; transcription can. The correction path
  is graduated rather than DEC-for-everything: requiring a DEC to fix a
  typo trains the habit of fixing typos silently, which is the
  behaviour the rule exists to stop.
- **C1, required vs supporting evidence (Should Fix) — ACCEPTED,
  mechanism rejected** (§3). The concern is legitimate: arguing at the
  gate about whether latency is blocking is a real failure mode. But a
  second required/supporting axis duplicates a control the schema
  already has — "deferrals, not allowed" *is* the required list — and
  introducing a parallel taxonomy is the same defect refused when
  "Must-Fix" was declined as a second label. The equivalence is stated
  explicitly instead. Working through it exposed the actual finding:
  the draft-2 not-allowed lists were under-specified. B7's omitted the
  grounding test, which plainly blocks; B8, B9.5, B10 and B11 had no
  lists at all. All seven rewritten and made exhaustive.
- **C2, per-criterion ownership (Should Fix) — DECLINED.** This is a
  one-person programme. Developer, architect, chair and reviewer are
  the same individual; an ownership column against each criterion
  records that fact seven times and controls nothing. It is also the
  RACI the same review asked not to add, wearing a different hat. The
  instinct underneath it is sound and is kept in operable form: what
  matters is not who owns a criterion but whether it can be cleared by
  working on it. Entry criteria carry an external-dependency flag
  (§3.2). Revisit if a second person joins the build.
- **C4, B7 retrieval eligibility (minor) — ACCEPTED and extended.**
  Cheap, and it is the difference between a corpus and a controlled
  corpus. Extended in one respect the review did not reach: eligibility
  must be time-versioned rather than a mutable flag, because B9 replay
  needs the eligibility state *as at the decision*.
- **C5, B9 enumerate nondeterminism sources (minor) — ACCEPTED.** A
  register with a bound per source is auditable; a paragraph is not.
  Made a living list, and non-deferrable.

## 9. Not addressed here

WS-D items 2–4 (CF-1 spot-check design detail, RAT-02 trio
specification, SS1/23 principle mapping for B8/B9) are named in the
gate criteria above but not designed. They follow from this ratified
shape. They are now named entry and exit items and cannot be left vague
once B7 opens.
