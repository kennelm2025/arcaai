# RQA batch 1 — set-level record

Covers `RQA-101` through `RQA-107`, the seven Obligation A corpus-QA scenarios of
D1.1 Rev C Appendix A.1. **Authored 2026-08-17 against the 16-document eligible
set at manifest `2026-08-13.8`, all seven pinning one corpus state.**

This record exists because **two of Rev C's requirements are series-level and the
schema cannot enforce them** — Obligation D (§2.1) and the density-stratified
note (§5.2) both turn on properties of a series that no single spec can observe.
Rev C puts both checks at scenario acceptance. This is that check, run across the
set rather than inside any one file.

## The set

| Scenario | Series | E | \|E\| | Density ratio | Density note owed |
|---|---|---|---|---|---|
| RQA-101 | Customer Vulnerability | SYN-CV-01, SYN-CV-02 | 2 | 1.33x | No |
| RQA-102 | Chief Executive letter | SYN-DL-01, SYN-DL-02 | 2 | 1.33x | No |
| RQA-103 | Decision Procedures | SYN-DP-01, SYN-DP-02 | 2 | 1.33x | No |
| RQA-104 | Sector Guidance | SYN-SG-01, SYN-SG-02 | 2 | 1.0x | No |
| RQA-105 | Thematic Review | SYN-TR-01, SYN-TR-02 | 2 | 1.25x | No |
| RQA-106 | Typology | SYN-TY-01, SYN-TY-02 | 2 | 1.0x | No |
| RQA-107 | Statute | OGL-0001, OGL-0002 | 2 | **16x** | **Yes, carried** |

Seven series, seven scenarios, complete against Obligation A. No expected
document appears in more than one scenario.

## Rulings

Placed before the findings deliberately: R1 governs how Finding S1 is read, and a
constraint on reading is worth nothing if the reader meets it afterwards.

### R1 — the batch-1 evidence boundary. **OPERATOR RULING via coordinator, 2026-08-17.**

> **A green across `RQA-101`..`RQA-107` evidences DOCUMENT-LEVEL PRESENCE ONLY.
> No precision claim, no rank-quality claim, no distractor-avoidance claim.
> Nothing may quote batch-1 results as more than that.**

Acknowledged as a **standing constraint**, not an observation to be weighed. It
governs the reading of Finding S1 below, which records why the boundary exists:
all seven scenarios sit at |E| = 2, so Rev C §5.4's precision-or-rank obligation —
which begins at |E| >= 5 — is never triggered anywhere in this batch.

The practical test: a sentence citing a batch-1 result is within the boundary if
it says a document was or was not retrieved, and outside it if it says anything
about how well, in what order, or against what competing content.

### R2 — `RQA-107` typology marker drop, RATIFIED. **OPERATOR RULING via coordinator, 2026-08-17.**

> **`statute.fraud_act_2006` stands as committed.**

Rationale of record: the schema's pattern description and its tests carry the
non-comparability disclaimer, so the marker's work is done where it can be
asserted rather than in each value; and **vocabulary status is a property of the
vocabulary, not of each value**, so a marker embedded per-value goes stale the
moment the fraud-side vocabulary lands.

The re-key history — `unverifiable-pending-vocabulary:statute.fraud_act_2006` at
v0.2, refused by the v0.3 pattern for its colon, then the marker dropped rather
than re-punctuated — is at `RQA-107.authoring.md`. All seven batch-1 scenarios
carry plain descriptive identifiers on this reasoning.

## Finding S1 — the whole set is binary probes, and nothing exercises the precision boundary

**All seven scenarios sit at |E| = 2. Not one is at |E| >= 5.** Obligation D is
therefore discharged by the **justification** route in all seven cases and by the
additional-scenario route in none.

This is structural, not a drafting choice: **every eligible series holds exactly
two documents**, so no honest query confined to a series can reach five necessary
grounding documents. Each spec records that reasoning in its own
`obligation_d_justification`.

**The consequence worth stating plainly.** Rev C §5.4's precision-or-rank
obligation begins at |E| >= 5 and is therefore **never triggered anywhere in
batch 1**. The batch evidences document-level presence and nothing about
precision, rank quality or distractor avoidance. A green across all seven means
every series' documents are reachable at `top_k` 5 — it does not mean retrieval
is good. Nothing in this set should be cited as precision evidence.

## Finding S2 — the dense end of the corpus is never exercised

`OGL-0003` (7 chunks) and `OGL-0004` (16 chunks) appear in **no** expected set.
The batch covers 14 of the 16 eligible documents, and every document it does
cover sits between 1 and 5 chunks.

RQA-107's density note says this for the Statute series. It is true of the whole
batch: **no scenario in batch 1 evidences retrieval from a dense document.** That
is a coverage-quality gap the obligations themselves do not ask about, recorded
here rather than left to be discovered.

## Finding S3 — two scenarios carry inclusion-decision triggers, and they differ in kind

| Scenario | Trigger | Kind |
|---|---|---|
| **RQA-106** | `SYN-TY-03` or `SYN-TY-04` becoming eligible | **RE-AUTHORING.** Both are near-duplicates of an E member by subject. Sufficiency is a property of the eligible set: if TY-04 restates mule-network structure, "the absence of TY-01 would leave the answer ungrounded" may cease to be true, and criterion 2 fails by construction rather than judgment. Re-pinning alone would carry forward a sufficiency argument that no longer holds |
| **RQA-104** | `SG-03`..`SG-09` becoming eligible | **OBLIGATION D EXPIRY.** The series grows from two documents to nine, the \|E\| >= 5 route becomes constructible, and the justification stops holding. Obligation D would be re-discharged by a graded scenario against the enlarged set, not by re-citing this one |

Two weaker cases are recorded in their own authoring records rather than here:
RQA-105 (`SG-03` could plausibly ground the evidence limb) and RQA-101 (`SG-08`
could plausibly enter E).

**All seven carry ordinary re-pin debt** on the inclusion decision — the
`retrieval_snapshot_sha256`, the eligible-set hash and the indexed chunk count
all move. That is queue item 12 and is not a defect in any spec.

## Finding S4 — the v0.3 justification cap bit twice

`binary_probe_justification` and `obligation_d_justification` carry a 1000-character
cap. RQA-101 and RQA-102 exceeded it on first drafting and were **refused at exit
2** until trimmed, with the overflow moved into their authoring records.

Recorded as a fact about the schema rather than a complaint: the cap was set at
v0.3 authoring without calibration against real justifications, and the refusal
is arguably the schema working — it pushes long-form reasoning into the authoring
record, which is where Rev C §5.2 puts E-composition review anyway. But it was
not a calibrated choice, and a future v0.4 should decide the number deliberately.

## Conventions, uniform across all seven

`schema_version` 0.3 · `scenario_class` retrieval · `vertical` fraud ·
`retrieval_kind` corpus_qa · `scoring_method` semantic_distance · `top_k` 5 ·
`top_k_absolute_cap` 7 · `migration_diff` bit_identical · `acceptance`
`recall_at_k >= 1.0`.

Every typology identifier is unique, pattern-conformant and a **plain descriptive
identifier** — no vocabulary-status prefix. See RQA-107's authoring record for
why the prefix was dropped.

## What this set is not

It is not evidence of typology coverage: the Rev C §2.4 external-reliance bar
applies to every scenario here, and none may be cited externally as evidence of
typology coverage until the manifest typology field and the controlled vocabulary
land. It contains no citation-following (RCF) or gap-detection (RGD) scenarios —
both are out of scope for this act, and the runner lacks the capability either
would need.

**It is also not precision evidence, and that is a ruling rather than a caveat —
see R1 above.** A green here says the documents were reached; it says nothing
about how well, in what order, or against what competing content.
