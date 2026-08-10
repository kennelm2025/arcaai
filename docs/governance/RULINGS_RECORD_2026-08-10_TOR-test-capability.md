# Rulings Record - TOR: ArcaAI Test Capability Build-Out (Rev C)

Date of rulings: 2026-08-10
Document under review: TERMS OF REFERENCE - ArcaAI Test Capability Build-Out, Rev C (10 Aug 2026). Held as a Gmail draft (coordinator artefact); Section 10 annotated with these rulings same day.
Ruling authority: operator (Mike). Reviewer content is SME concurrence and recommendation only, per house discipline; no reviewer ruling is effective.

## 1. Panel composition

Three reviews received 2026-08-10. Identities recorded here for the register; where a reviewer has previously reviewed this document or its antecedents, the one-reviewer-across-passes rule (WS-E 36 class) applies and is annotated.

- Reviewer A: Grok. First pass on this document. Prior-familiarity annotation carried: Grok has reviewed ArcaAI material on multiple prior occasions (batch-1 corpus review, 2026-08-04 mechanical items two-pass, architecture reviews); its concurrence here is informed, not independent of that history.
- Reviewer B: ChatGPT (GPT). First pass on this document. Note: ChatGPT was withdrawn from the batch-1 corpus panel; this is its return to the ArcaAI bench.
- Reviewer C: DeepSeek. First pass on this document.

Note for the record: Reviewer B phrased four outcomes as "RULED: APPROVED / CONFIRMED / AMENDED". These are recorded as concurrence and recommendation only. All effective rulings in this record are the operator's.

Out-of-scope submission: a fourth return in the same circulation, from Gemini, was an assessment of the architecture-principles review (orchestration / memory / dreaming), not of this TOR. It is parked to its own process and forms no part of this record; Gemini is therefore not counted as a reviewer of this TOR.

## 2. Verdicts

- Reviewer A: ACCEPT WITH AMENDMENTS (twelve findings; nine accept, three accept-with-amendment).
- Reviewer B: sound and well-framed; strengths and three concerns; recommendations against all open questions.
- Reviewer C: strong, coherent, ready for next refinement pass; residual points to tighten; recommendations against open questions.

Convergent across all three, with no ruling tension: the two-regime governance model (Section 5A) with permanent inadmissibility of commissioning results; proof-first sequencing (Section 9) endorsed without modification; retrieval as scenario batch 1 / B7 first cargo; the reproducibility triple; the pre-flight fold-in discharging the parked ONNX check authoring debt; the AWS annex.

## 3. Operator rulings on the open questions

### Ruling 1 - Register home (OQ1)

RULED: DEC-0015 establishes the harness under the existing structure. No new workstream ID. Work items track under the WS-T deliverable naming within existing ledger discipline.
Panel position: all three reviewers concurred.

### Ruling 2 - Scenario batch 1 scope (OQ2)

Confirmed as resolved at Rev B: batch 1 is retrieval over the fraud corpus (corpus QA, citation-following, D1/D2 gap detection), because it is the B7 exit evidence. Scoring scenarios follow as batch 2.
Panel position: all three reviewers concurred.

### Ruling 3 - B7 exit relationship to harness evidence (OQ3)

RULED: preferred-primary (the middle position).
Harness Regime-2 runs against the ruled Test Plan are the preferred primary evidence for retrieval quality and for detection of the planted D1/D2 gaps. They are not a hard single-point dependency that can block the entire B7 gate if equivalent citable evidence exists by another governed route.
Rationale (operator's, verbatim): making the gate wholly dependent on a brand-new harness creates unnecessary coupling and a single point of failure during the harness's own early life. Making the harness merely "nice to have" under-weights the very capability being built. Preferred-primary gives the harness its proper weight while preserving an escape path if the harness itself is still maturing.
Panel positions, recorded as divergent: Reviewer B recommended a hard requirement (Regime-2 evidence mandatory, manual notes commentary only). Reviewer C recommended preferred-primary with no single-point dependency. Reviewer A took no position and required the Test Plan to make the relationship precise. The ruling adopts C's position; A's requirement is satisfied by amendment 9.4 below.

### Ruling 4 - Migration diff gate (OQ4 / Annex A)

RULED: the D2.6 pre-migration baseline (a Regime-2 run against the ruled Test Plan) is a formal hard precondition to any serving-layer cutover to AWS. The D3.5 diff report is formally reviewed before migration is declared complete.
Panel position: all three reviewers concurred.

### Naming (OQ5)

Deferred, unruled. Trivial; carries.

## 4. Amendments accepted

All nine accepted. None amends the TOR text; all land as requirements on the Test Plan (D1.1) or the scenario spec schema (D2.1), and are binding on those artefacts at authoring:

1. Invalidation and re-test rules stated operationally in the Test Plan - which corpus or model movement invalidates which prior results and what must re-run - not merely named as a category. (Reviewer A, finding 6.)
2. The Test Plan preserves the distinction between a scenario detecting a deliberately planted under-implementation and any general claim about retrieval quality. D1/D2 detection evidences gap-detection capability; it does not by itself evidence retrieval quality broadly. (Reviewer A, finding 9.)
3. Migration-diff comparison semantics settled per scenario class: bit-identical at specified inputs where the pipeline is deterministic; defined tolerances where nondeterministic components exist. The semantics live in the schema so each scenario declares its own comparison rule. (Reviewer A, finding 12.)
4. The Test Plan states the precise relationship between harness evidence and the complete B7 exit evidence set, implementing Ruling 3. (Reviewer A, panel-ruling paragraph.)
5. Gap-detection scoring defined mathematically in schema v0.1: how non-retrieval / negative grounding of the planted gaps is scored, distinct from standard semantic-distance scoring. (Reviewer B, concern 1.)
6. generator_seed mandatory in the spec schema and reproducibility payload for scenarios that invoke the synthetic data generator (scoring class). Retrieval-class scenarios do not invoke the generator; for scoring-class scenarios the reproducibility identity is effectively spec hash + model version + corpus snapshot + generator seed. (Reviewer B, concern 2.)
7. Pre-flight failure fails hard: non-zero exit immediately on any pre-flight assertion failure, blocking all downstream steps, so no partial or corrupted ledger entry can be written in CI or locally. (Reviewer B, concern 3.)
8. The D2.0 commissioning frame is held to one page: session objective, entry criteria, exit criteria, records rule, admissibility rule - nothing else. It must not grow into a miniature Test Plan. (Reviewer C, point 4.)
9. The commissioning spike pins to the corpus snapshot current at spike time and records it; it does not wait for the eligible-23 listing act. Formal (Regime 2) runs use listed snapshots only, per Section 5A. Defect routing (harness to WS-E ledger; system-under-test findings to CL register or stage evidence; corpus defects to the corpus rulings process) is stated explicitly in the Test Plan's formal-execution pack. (Reviewer C, points 5 and 6.)

## 5. Consequences and next acts

- The TOR proceeds as the working document at Rev C, Section 10 annotated with these rulings. No Rev D.
- DEC-0015 is to be authored consuming the next DEC number, establishing the harness register home per Ruling 1. Separate governed act.
- Next build sequence, per Section 9 as endorsed: rule the D2.0 commissioning frame (one page, operator); author schema v0.1 (carrying amendments 3, 5, 6); execute the D2.2a runner spike under the commissioning frame at the pinned current snapshot.
- The D2.2a commissioning result remains permanently non-evidential, exactly as Rev C Section 5A specifies. All three reviewers restated this independently; recorded here so no later reading can soften it.

End of record.
