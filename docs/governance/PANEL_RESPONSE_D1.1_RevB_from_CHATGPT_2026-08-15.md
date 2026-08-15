# PANEL RESPONSE — D1.1 Test Plan RevB — CHATGPT

**Round 2 · Received 2026-08-15**
**Reviewed hash:** `68270febf4a8ff092112e4adc8b0696c316e99053ac38e8e48cc5f2d007818dd` — INDEPENDENTLY RECOMPUTED by the reviewer.

*Provenance: received via the coordinator conversation 2026-08-15 and
transcribed verbatim by the coordinator; transported to disk by the
operator. Chain of custody runs through the coordinator layer, not
directly from the reviewer interface.*

---

## Round 2 — D1.1 Test Plan Rev B

### Hash verification

I verified the supplied Rev B bytes **before reviewing the content**.

* File: `D1.1_TEST_PLAN_DRAFT_RevB_2026-08-15.md`
* Bytes: **94,385**
* Lines: **1,687**
* CR characters: **0**
* SHA-256 actually calculated:
  **`68270febf4a8ff092112e4adc8b0696c316e99053ac38e8e48cc5f2d007818dd`**

It exactly matches the governing hash in pack §1.

So this review is pinned to the requested Rev B text.

---

# 1. Round-1 carriage check

**Verdict: substantially faithful. I found no omitted round-1 finding or dissent.**

The round-1 disposition records **35 rows** and explicitly says that all rows were ruled.

I cross-checked those 35 row IDs against Rev B Appendix C programmatically and manually. **All 35 are present.** Appendix C additionally contains two new chair-level drafting decisions — the strengthened Obligation B form and the carried-in evaluator-version structural option — which are not round-1 rows and therefore do not constitute omissions.

### Particularly important carriage checks

* **F-DS-04 / BLOCKING:** faithfully converted into the bounded Rev B treatment. The Cartesian-product claim is withdrawn; class-specific obligations are explicit; typology coverage is explicitly labelled **PROVISIONAL** rather than falsely claimed; per-scenario typology declarations and the coverage-audit event are carried.
* **F-GROK-02 / binary probes:** correctly extended from `|E|=1` to `|E|≤4`, with the graded-measure language withdrawn.
* **F-CHATGPT-02 / expected-set construction:** four explicit criteria plus marginal-case recording are present.
* **F-DS-01 / recall limitation:** correctly carried, including the `|E|≥5` precision/rank boundary.
* **F-DS-02:** threshold departure is now a ruled variance, not an author's justification.
* **F-GROK-03:** golden-fixture control is present and made an entry criterion.
* **F-CHATGPT-03:** D3.1 result artefact is content-addressed and its hash is carried by the immutable ledger entry.
* **F-DS-03:** harness-defect invalidation is present; the evaluator version was additionally carried in as a fourth reproducibility leg.
* **F-CHATGPT-04 / F-GEMINI-03:** environment/toolchain movement is now explicitly defined, including embedder configuration.
* **F-DS-05:** the disputed row-3 reachability is explicitly re-established with four reachable cases.
* **D-001:** the F1 distinction is explicitly ruled: motivation is permitted; evidentiary use is not.
* **D-002:** substitution is strengthened into an operator-ruled variance.
* **F-DS-07:** halted partial results get an explicit `session_status: halted` treatment.
* **F-CHATGPT-05:** model identity must resolve to an immutable content-addressed artefact.
* **F-CHATGPT-06 / F-DS-09:** single-chunk confounding is explicit, machine-checkable and does **not** get a lowered acceptance bar.
* **F-GROK-07:** all six entry criteria now either have an assertion surface or an explicit deferral.

So on the first question I am comfortable saying:

> **Round-1 carriage: PASS. No round-1 finding or dissent has been silently dropped or materially weakened.**

That is important because the disposition itself made faithful carriage the primary objective for Rev B.

---

# 2. Whole-document review

The acceptance rule is unusually hard: **one BLOCKING or MATERIAL finding sustained by the chair prevents acceptance**.

I therefore applied a fairly high bar before rating anything MATERIAL.

## Finding R2-01 — MATERIAL

### Evaluator-version change does not have a complete invalidation route

There is a logical hole between §9.2 rows 7 and 8.

Row 7 says:

> evaluator version changes, no defect confirmed → **nothing invalidated**, provided the golden-fixture suite is green at both versions.

Row 8 handles a **confirmed harness defect** and invalidates results from the affected evaluator version.

The problem is the document then says:

> "where a behaviour change is intended, the change ... falls to row 8."

But row 8 is explicitly:

> **"Harness defect affecting scoring or acceptance evaluation, CONFIRMED."**

An **intentional semantic change is not a confirmed defect**.

That leaves three materially different cases being treated as though two were sufficient:

1. evaluator implementation changes but produces demonstrably equivalent behaviour → row 7, arguably fine;
2. evaluator implementation is defective → row 8, fine;
3. evaluator semantics intentionally change → **no properly defined invalidation/re-baselining route**.

The problem is made more significant by the stated purpose of adding evaluator version as a reproducibility leg: the plan says a change to evaluation logic must be visible and that the evaluator is separately versioned.

The golden-fixture suite does not completely solve this. §5.7 describes it specifically as asserting the **threshold comparison**, with known inputs, verdicts and quantisation boundaries. That is narrower than demonstrating semantic equivalence of the whole evaluator.

### Why MATERIAL

A deliberate change in evaluation semantics can alter the meaning of historical pass/fail results without any defect existing. That is an evidence-integrity issue, not merely documentation.

### Required change

Separate the third case explicitly, e.g.:

* evaluator version changed + semantic equivalence demonstrated → prior results survive;
* evaluator defect confirmed → affected results invalidated;
* evaluator semantics intentionally changed → prior results invalidated/re-baselined for the affected classes.

And make the fixture/equivalence criterion correspond to the distinction.

**Rating: MATERIAL**

---

## Finding R2-02 — MINOR

### Appendix B violates its own ownership rule

Appendix B opens with:

> "Each carries an owner, because an open item without one is a note rather than an obligation."

But item 7 — the single-chunk disadvantage investigation — has:

> **Owner: Unassigned**

This is a straightforward internal inconsistency.

It matters because the document has deliberately converted the single-chunk issue from an observation into a named investigation, with four candidate mechanisms and a routing consequence. Without an owner, the obligation cannot actually be discharged through the governance mechanism the document describes.

### Required change

Assign an owner, or explicitly change the opening rule to permit intentionally unassigned items with a defined mechanism for assignment.

**Rating: MINOR**

---

## Finding R2-03 — OBSERVATION

### RQA-107 may be too thin to support the claimed series-level coverage

The plan says Obligation A is discharged by **one corpus-QA scenario per series**, and RQA-107 represents the four statute documents. Those documents have chunk counts:

**1, 1, 7 and 16.**

The document itself recognises this in Appendix D and deliberately holds it for later consideration.

I agree with the decision **not** to reopen the coverage rule in this revision. The current rule is "one scenario per series"; it does not claim one scenario exhaustively validates every document within a series.

So I am **not** raising this as MATERIAL or MINOR.

However, it is worth preserving as an observation because the statute series is unusually heterogeneous, and the one-scenario construction could eventually become a coverage-quality question rather than merely a coverage-presence question.

**Rating: OBSERVATION**

---

# 3. Things I deliberately did *not* raise as findings

Several things initially look like defects but, after checking them against the round-1 ruling, I think raising them would be wrong.

### Typology coverage remains provisional

This is **intentional and faithfully carried**, not an accidental gap. Rev B explicitly says the plan does not yet deliver the TOR typology matrix and that Regime-2 execution is not evidence of typology coverage.

The round-1 ruling specifically required the gap to be named rather than papered over. So I would not re-find it.

### Four of six entry criteria remain deferred

Again, this is honest carriage rather than concealment. Criteria 2–5 are explicitly marked deferred to the runner build rather than falsely claiming they are presently asserted.

### B7 gate synchronisation remains outstanding

The plan correctly says the B7 gate document is silent on the harness and that the synchronisation patch is owed **before first Regime-2 gate exit**, not as a condition for accepting D1.1 itself.

I would not convert that into a D1.1 acceptance finding.

### The manifest/processing-facts caveat

The provisional status of row 2 is explicit, and the document verifies that the current 16 eligible documents all have the processing block.

Again, correctly bounded.

---

# 4. Round-2 verdict

| Finding                                                                   | Severity        |
| ------------------------------------------------------------------------- | --------------- |
| **R2-01 — evaluator semantic-change invalidation gap**                    | **MATERIAL**    |
| **R2-02 — Appendix B item 7 has no owner despite its own ownership rule** | **MINOR**       |
| **R2-03 — RQA-107 depth/heterogeneity**                                   | **OBSERVATION** |

### Overall

**Rev B is NOT ACCEPTABLE under the §2.1 acceptance rule as currently written**, because I have one **MATERIAL** finding.

The important distinction from Round 1 is that I am **not** challenging the carriage of the previous work. That part is good: the Rev B author has genuinely incorporated the round-1 disposition rather than merely ticking the boxes. The new MATERIAL issue arises from the interaction of two of the newly added controls — evaluator versioning and the invalidation table — and is therefore exactly the sort of whole-document consistency problem Round 2 is supposed to catch.

I would **not** issue a dissent against any round-1 chair ruling. My R2-01 is a new finding arising from the Rev B implementation, not disagreement with the disposition.

**Verified Rev B hash:** `68270febf4a8ff092112e4adc8b0696c316e99053ac38e8e48cc5f2d007818dd`
