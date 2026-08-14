<!-- PROVENANCE: Response received by the chair from the DeepSeek session and
relayed via the coordination chat to this file, 2026-08-14. The chair
attests this text matches the DeepSeek tab. Two chat relays of this
response were consistent, including two internal anomalies preserved
as-received per the verbatim rule (they are the reviewer's own text, not
transport damage): (1) the CONFIDENCE AND LIMITS section references
"my finding F-DS-11", but the response contains findings F-DS-01..09 only;
(2) the closing paragraph says "two BLOCKING gaps" while only F-DS-04 is
rated BLOCKING (F-DS-03 is rated MATERIAL). Both anomalies are noted for
the chair's disposition, not corrected. Committed under the PANEL-ROUND
CONVENTION: verbatim, unedited below this comment block, pinned to the
reviewed hash. -->

PANEL RESPONSE — D1.1 Test Plan RevA — DEEPSEEK

Reviewed hash: 21a5831f27cb55b98595413c9d047c433fe590c5a6939a82e18bdf64778e8caf

---

## FINDINGS

**F-DS-01: Recall at k as the sole metric for semantic-distance scenarios is under-specified for multi-document expected sets**

  **Section(s):** §5.2, §3.2, Appendix A

  **Severity:** MATERIAL

  **Finding:** The plan defines recall at k as `|R_k ∩ E|/|E|`, which treats all expected documents as equally important. This is defensible for `|E| = 1` and small sets, but the plan does not address whether the expected set itself has internal structure — whether some expected documents are *more* expected than others. The plan also does not distinguish between retrieving *any* k documents from E versus retrieving the *correct* k documents, when `|E| > k`. The latter cannot be detected by recall at k alone, which saturates at 1.0 once k expected documents are retrieved regardless of whether the retrieved set also contains non-expected material that would be judged incorrect in context. The schema's semantic-distance branch does not appear to account for precision or rank-order quality.

  **Why it matters:** A scenario with `|E| = 5, k = 5` that returns all five expected documents plus five distractors returns the same recall score as one that returns exactly the five expected documents. An auditor reviewing the acceptance verdict cannot distinguish the cases. The runner's evaluation treats both as a pass at threshold 1.0, but the qualitative claim — "the grounding was retrieved" — is stronger than the metric can support. The plan's statement at §4.3 that gap detection "is a weighted combination of abstention and distractor avoidance, neither term a semantic distance" makes the asymmetry worse: semantic-distance scenarios have no distractor-avoidance term at all.

  **Shape of a fix:** Either add an explicit note that recall at k is a *presence* metric only and does not claim precision or rank quality, and that any scenario where precision matters must state an additional acceptance criterion; or amend the schema to permit a threshold over recall at k *and* some precision-or-rank measure for cases where `|E|` is large enough that the distinction matters. The plan should state a boundary — at what `|E|` does a scenario author need to think about precision?

---

**F-DS-02: The quantisation argument for the threshold default is mathematically correct but philosophically questionable as a *default* rule**

  **Section(s):** §5.2

  **Severity:** MATERIAL

  **Finding:** The plan argues that a threshold of `ceil(0.8 × |E|)/|E|` is correct because recall at k has granularity `1/|E|` and a threshold not at an attainable multiple silently rounds. This is mathematically sound. The issue is that the plan then states this is the *default* and that a scenario author may override it with a stated reason. The quantisation argument makes the default the *only* threshold that expresses 0.8 exactly, but the plan's own reasoning implies that any threshold is either exact or misleading — so what does an override accomplish? A threshold of `0.6` at `|E| = 5` is exactly attainable; a threshold of `0.7` is not. If the rule is that thresholds must be multiples of `1/|E|`, then the "default" is the only threshold whose value is independent of `|E|` and expresses a consistent intent. Overriding it to `(m)/|E|` with `m != ceil(0.8|E|)` is not "per-scenario tuning" — it is a different acceptance standard with no clear relation to the default. The plan does not provide a rationale for what an override is *for*, or how a reviewer assesses whether an override is justified. §5.1 says an override "must carry a stated reason" but gives no criterion for what counts as a sufficient reason. "The scenario is more difficult" or "less difficult" would be a reason but is not falsifiable.

  **Why it matters:** A rule that permits arbitrary overrides without substantive criteria for justification creates a backdoor. A motivated scenario author can write thresholds that produce the desired pass/fail outcome while satisfying the letter of the plan. The invalidation table at §9.2 does not capture threshold changes, so a scenario whose threshold was adjusted between runs would not be re-run — the result would survive despite the acceptance bar having moved.

  **Shape of a fix:** Either (a) make the default *mandatory* unless a scenario has a structural property that the default does not address (e.g., an expected set with internal weighting, per F-DS-01), and require that property to be stated; or (b) define an override as a *variance* that requires operator approval and is recorded as a ruled variance, not merely a stated reason in the spec. The plan's current "stated reason" requirement is too weak to prevent gaming.

---

**F-DS-03: The H-8 instrument-asserted verdict has a gap in the immutability argument**

  **Section(s):** §5.3, §8.2

  **Severity:** MATERIAL

  **Finding:** The plan states that the pass/fail verdict is "immutable in the ledger by the same mechanism that makes the regime marker immutable" and that an absent verdict must never read as a pass. The plan also states that the runner evaluates acceptance and writes the verdict. The immutability argument is: a process that can edit the marker is a promotion path, so the verdict must be immutable too. But the plan assumes that the ledger's immutability mechanism is sufficiently strong to prevent *the runner itself* from writing a verdict it has asserted as evaluated but that was in fact computed incorrectly. The runner that asserts the verdict is also the runner that computes the verdict. A defect in the evaluation implementation — e.g., a signed integer overflow in the recall calculation, a mis-indexed `R_k` set, a race condition between retrieval and scoring — would produce an incorrect verdict that is then immutably recorded. The plan routes classification of such a defect as a harness defect under §10.1, and invalidation of prior results is §9.2. But nothing in §9.2 invalidates results for *harness defect discovered after the fact*. The table's rows are only corpus hash changes, model version changes, and spec hash changes. A harness bug is not a row. The plan's statement at §8.5 says routing is "not closing it" but does not say that a routed harness defect invalidates prior results if found to affect them.

  **Why it matters:** A bug in the runner's evaluation logic discovered after Regime 2 results have been accepted would produce invalidated results that remain in the ledger, marked only as harness defects, but with no re-test obligation. The plan says "invalidation does not delete the prior result" but re-run is triggered only by §9.2 movements. Harness bugs are not movements. The plan effectively trusts that the runner is correct, and if it is not, the evidence chain breaks without a governed recovery path. This is the same failure mode the TOR's WS-E 63 records — a green read meaning something it cannot mean — imported into the evaluator itself.

  **Shape of a fix:** Add a row to the invalidation table for "Harness defect affecting scoring or acceptance evaluation, confirmed". That row should invalidate all results produced by the affected runner version for the relevant scenario classes. Alternatively, route all evaluation logic to a separately versioned component and treat a version change as a model-version-like movement. The plan's current §10 routing discipline is not enough because routing a defect is not the same as stating what happens to results produced under that defect.

---

**F-DS-04: The coverage matrix rule over document series does not discharge the TOR's "per vertical, fraud typologies" requirement**

  **Section(s):** §2.1, §2.4, §2.5

  **Severity:** BLOCKING

  **Finding:** The plan itself states at §2.4 that the manifest carries no structured typology field, that a per-fraud-typology matrix is "unavailable", and that the matrix is expressed over document series "derived by reading the `source:` prose" and therefore "maintained by hand". The plan records this as a candidate act for `DEC-0014` but does not resolve it. The coverage rule at §2.1 states that the matrix operates over "every document series represented in the current listed snapshot's eligible set", which is narrower than the TOR requirement. `TOR §3:30` requires a "coverage matrix per vertical, fraud typologies" — not per document series. The plan asserts that one vertical (fraud) is in scope and that the series-level coverage is a proxy, but the plan does not demonstrate that series coverage implies typology coverage. The manifest may have multiple typologies per series, or a typology may be absent from a series while another series covers it redundantly. The plan does not know, and cannot know, because the information is not machine-readable.

  **Why it matters:** This is the single largest gap in the plan's auditability. A PRA-style reviewer would ask: "How do you know you have tested every fraud typology you claim to support?" The plan's answer is effectively "we don't, because the manifest doesn't tell us, so we test by series instead." That is not a sufficient answer for a regulated bank. The operator ruling at OQ2 that "scoring scenarios follow as batch 2" does not exempt the retrieval-class batch from typology coverage. The plan's Appendix A shows one scenario per series, but that says nothing about whether the *queries* within those scenarios cover all relevant typologies.

  **Shape of a fix:** This is not a fix the Test Plan can make alone; the manifest must carry structured typology fields. The plan must either (a) state that the matrix is *provisional* until the manifest is amended, and that a Regime 2 run against the current manifest is not evidence of typology coverage; or (b) require that each scenario's spec declares which fraud typology it covers, and that the coverage rule is satisfied when every typology in the eligible set has at least one scenario. The current series-based rule is not defensible against the TOR. I regard this as BLOCKING because it means the plan does not implement the coverage requirement it claims to implement.

---

**F-DS-05: The invalidation table row for manifest-hash changes is correct but incomplete for metadata-only changes that affect scenario selection**

  **Section(s):** §9.2

  **Severity:** MATERIAL

  **Finding:** The table states that a manifest hash change with both content hashes unchanged invalidates nothing because the change is "metadata-only". The plan defines the manifest hash over "normative canonical form" per §6.3. But the manifest contains more than content hashes — it contains eligibility history, licence status, and SA5 classification per §6.2. If an eligibility transition is recorded (e.g., a document moves from `pending_review` to `eligible`), the manifest hash changes while document content hashes remain unchanged. Under §9.2, this invalidates nothing. But eligibility is not metadata for the coverage rule: §2.1 defines the matrix over the *eligible* set, and §2.3 treats eligibility as the boundary. A manifest version change that moves a document into eligibility changes the coverage rule's instantiation — documents that were previously invisible to the retriever become visible, and the eligible-set hash changes. The table treats that as row one (eligible-set hash change), invalidating retrieval-class results. The concern is the opposite direction: a manifest change that moves a document from eligible to `pending_review` also changes the eligible-set hash, triggering invalidation. The table's row for manifest-hash changes with content hashes unchanged is therefore correct only for changes that do not affect eligibility. But the plan does not state that eligibility transitions are content changes — they are not, by §6.2's split, and the plan's own text says eligibility is in the immutable identity block. If eligibility is immutable, it cannot be updated — a revised document is a new entry. But the manifest version changed, so the identity block changed, and the content hashes changed. The row "manifest hash changes, both content hashes unchanged" may be impossible under the plan's own immutability rules. The plan does not explain this.

  **Why it matters:** The table asserts a row that may be unreachable, and the plan's distinction between "listed" and "eligible" (§6.5) complicates the mapping further. A document can be listed but not eligible, and eligibility transitions are the core governed act the plan operates over. If the invalidation table's logic is based on a hash split that does not actually align with the governed acts, the table's guarantees are weaker than stated.

  **Shape of a fix:** Either make the eligibility status part of the document's *identity* block (so an eligibility change is a new document, changing content hashes) or make it part of processing facts (so the retrieval-snapshot hash captures it). The current split — identity immutable, eligibility in identity, but manifest version changes with no content hash change — is internally inconsistent. The table should be revisited once this is resolved.

---

**F-DS-06: The F1 disposition is correct, but the plan creates a scenario class based on it while claiming not to**

  **Section(s):** §3.3, §12.3

  **Severity:** MATERIAL

  **Finding:** The plan states that "a distinct statute-retrieval class was considered following F1, and is not created for batch 1" and that the reason is "creating a scenario class to explain a single observation risks encoding that observation as a design fact before it is understood." But Appendix A creates `RQA-107` as a corpus-QA scenario with series `Statute`, and §12.3(3) notes that the single-chunk confound is "recorded with the result." The plan has effectively created a statute-specific scenario — RQA-107 is a statute query, and the plan notes that two statute documents are single-chunk and affected by the same confound as F1. The distinction between "a statute-retrieval class" and "a corpus-QA scenario whose series is Statute" is formally present but practically absent. The plan's stated reason for not creating the class — avoiding encoding a single observation as a design fact — is weakened by the fact that the plan has encoded the observation as a scenario with special handling.

  **Why it matters:** The plan's §12.1 says F1 "may motivate a scenario; it may not be cited as showing anything about retrieval quality." RQA-107 is a scenario that was motivated by F1. The plan must ensure that the scenario's design is *not* contaminated by knowledge of the F1 outcome — e.g., that the query, expected set, and `top_k` were chosen independently of the fact that F1 failed. The plan does not state this. The scenario is not yet authored (Appendix A says "Not yet authored"), so the contamination is not yet assessable. But the plan's §3.3 rationale creates a false appearance of separation. A scenario motivated by a known failure is a legitimate diagnostic tool, but the plan should be explicit about how it avoids overfitting.

  **Shape of a fix:** When RQA-107 is authored, the spec should record the basis for the query selection, expected grounding, and `top_k` — ideally from a structured, ruled scenario-design process rather than from F1's failure case. The plan should state that this record will be present, and that the scenario's acceptance threshold was chosen before seeing F1's outcome. If the threshold was chosen after, the scenario is not a test but a validation exercise, which is a different governed act.

---

**F-DS-07: The formal-execution governance pack's suspension and re-entry rules do not address partial sessions**

  **Section(s):** §8.3, §8.4

  **Severity:** MINOR

  **Finding:** §8.3 states that a session halts on certain conditions and that re-entry requires a fresh pre-flight and a re-pinned triple. It also states that re-entry is "not resumption": results before and after were produced under different pinned conditions and "must not be presented as one continuous set." This is correct. But the plan does not specify what happens to a session that halts *after* some scenarios have executed and before others have. The suspension consumes the partial results: they are produced under the old pin and are invalidated by the movement that caused the suspension. But the plan does not state whether the partial results are recorded, marked as partial, or discarded. The ledger entry for the halted session would contain some results but not all; §8.2 item 1 requires "every scheduled scenario executed, or its non-execution recorded with a reason." The halting condition is a reason, but the plan does not say that the partial results must be recorded and marked as part of a halted session.

  **Why it matters:** If a session halts and the partial results are discarded, the ledger contains no record that the session occurred. The suspension is consumed only when re-entry conditions are met; but if the partial results disappear, the audit trail of what was run and when is incomplete. The plan's §9.3 says invalidated results "remain in the ledger, marked," but only for invalidated results, not for halted partial sessions.

  **Shape of a fix:** Add a statement that a halted session's partial results are recorded in the ledger with a `session_status: halted` marker and the reason, and that the partial results are marked as inadmissible for any use other than diagnosing the suspension. The re-entry session is a separate entry with its own triple.

---

**F-DS-08: The gap-detection scoring formula's default threshold of 0.8 has an unstated interaction with the default weights**

  **Section(s):** §5.2

  **Severity:** MINOR

  **Finding:** The plan states that at `w_a = 0.6, w_d = 0.4`, a threshold of 0.8 makes abstention necessary. This is correct: any threshold above `w_d` (0.4) requires A=1 to reach 0.8, because the maximum score without abstention is `w_d = 0.4`. The plan also states that "any threshold above `w_a` additionally constrains distractor avoidance." This is also correct: threshold 0.8 > 0.6 means the system must score at least 0.2 on the distractor term, requiring `|R_k ∩ D|/|D| <= 0.5`. The concern is that the plan's default of 0.8 is *not independent* of the weights. If a scenario author changes the weights (which §5.2 permits, though it says "a scenario changing them changes what its threshold means"), the default threshold of 0.8 may become nonsensical. For example, if an author sets `w_a = 0.9, w_d = 0.1`, a threshold of 0.8 *does not* make abstention necessary — the system can score 0.8 without abstention (0.9 + 0.1×score_d = 0.8 requires score_d >= -1.0, always true). The default threshold was calibrated to the default weights; the plan does not state that changing the weights requires reconsidering the threshold, nor does it provide a rule for what the threshold should become under weight changes.

  **Why it matters:** A scenario author could change the weights and keep the threshold at 0.8, producing a materially different acceptance bar without it being obvious. The plan's §5.2 says "the weights are therefore not presentational" but does not say that threshold and weights form a pair that must be evaluated together.

  **Shape of a fix:** Either (a) fix the weights as well as the threshold as a default, with overrides requiring justification for both; or (b) define the threshold in terms of the weights — e.g., "threshold = 0.5 + w_a/2" or something that preserves the abstention-necessary property at a consistent level. The plan's current approach treats weights and threshold as independently adjustable, which they are not.

---

**F-DS-09: The single-chunk confound in §12.3(3) is correctly recorded but the handling is underspecified**

  **Section(s):** §12.3

  **Severity:** MINOR

  **Finding:** The plan states that "a retrieval result whose expected grounding document occupies a single chunk carries a known confound, and that must be recorded with the result rather than noticed afterwards." This is a good discipline. But the plan does not state what happens if a scenario's expected grounding document occupies a single chunk and the scenario fails. Is the failure attributed to the confound, or is it a genuine retrieval failure? The plan's §10.3 classification procedure would route it to the corpus, harness, or system-under-test depending on the classification. But the confound is a *known limitation of the corpus design* — single-chunk documents are at a structural disadvantage because the chunker's paragraph-packing may over-condense statute text. The plan's own F1 analysis notes that OGL-0001 and OGL-0002 are both single-chunk. The plan does not say whether single-chunk expected sets are acceptable for Regime 2 evidence, or whether they require special acceptance thresholds (e.g., a lower bar) to account for the disadvantage.

  **Why it matters:** If RQA-107 fails, the plan's §12.3(3) confound will be recorded, but an auditor will ask "what does this failure mean?" The answer is ambiguous. The plan should state a policy: either single-chunk expected sets are permitted and failures are interpreted with the confound noted, or single-chunk expected sets are not permitted for Regime 2 evidence and must be re-chunked before formal runs. The plan's current "recorded with the result" is a mitigation, not a resolution.

  **Shape of a fix:** State that single-chunk expected sets are permitted for Regime 2 runs but their results carry a `confound: single_chunk` marker, and that a scenario with a single-chunk expected set passes if it would have passed with the confound taken into account — e.g., the threshold is adjusted to `ceil(0.6 × |E|)/|E|` instead of 0.8. Alternatively, require that all expected grounding documents in Regime 2 scenarios have at least two chunks. The current plan leaves the interpretation open.

---

## DISSENTS

**D-001: The plan's treatment of F1 as "permanently inadmissible" is correct, but the reason given — "a green read as meaning something it cannot mean" — is a stronger argument than the plan uses.**

The plan states the reason at §1.2: "the failure class WS-E 63 records: a green read as meaning something it cannot mean. A promotion path would reintroduce exactly that." This is a good argument. But the plan then treats F1 as a "routed question" (§12.1) and creates a scenario motivated by it. The inadmissibility is permanent *as evidence*, but F1 is not *ignored*. The chair may hold that this is a distinction without a difference. I believe the plan is correct to use F1 to motivate diagnostic scenarios while barring its use as evidence. The chair should rule explicitly that this use does not violate the inadmissibility bar, because the bar is on *evidentiary use*, not on *motivation*.

**D-002: The plan's "preferred-primary" position on harness evidence (§7.2) is a compromise that may be too weak for a PRA-style review.**

The operator adopted Reviewer C's position over Reviewer B's hard requirement. I agree with the operator's rationale — a brand-new harness is a single point of failure — but the compromise creates a "substitution permitted" path that an external auditor might view as a loophole. The plan requires a justification in the record, but the justification criterion is not objective. A motivated gate closer could write "harness evidence was unavailable" and substitute a manual review that is substantially weaker. The plan's §7.2(c) attempts to close this by requiring the substitute to meet the same properties as a Regime-2 run, but manual reviews cannot be reproducible by construction. The chair may wish to strengthen this: substitutes should be drawn from a pre-approved list of governed routes, or should require operator sign-off as a variance. As written, the plan permits a retreat from harness evidence without a hard barrier.

---

## CONFIDENCE AND LIMITS

I have not reviewed the following documents, which the plan cites or relies on:

- The Terms of Reference (Rev C) — I have only the plan's paraphrases and citations.
- The D2.1 schema — I have only the plan's description of its behaviour, including the semantic-distance/gap-detection scoring split, the `migration_diff` definition, and the tolerance-block structure. My finding F-DS-11 about the nondeterminism-source field being omissible is based on the plan's description; I have not verified the schema JSON.
- The rulings record or DEC-0015 register — I have only the plan's implementation of amendments 1–4 and 9.
- The D2.5 results ledger or D3.1 result artefact schemas — I cannot assess whether the plan's recording requirements are consistent with those artefacts.
- The runner implementation (D2.2a/D2.2b) — I cannot assess whether the H-8 assertion that the runner evaluates acceptance is implementable in the current codebase.
- `docs/build/B7_GATE.md` — I have only the plan's citation that it is silent on the harness; I cannot verify that statement or assess whether the plan's mapping of B7 items to harness relationships is accurate.

I have relied on the plan's own statements about the schema behaviour, particularly at §3.2, §4.3, and §11.2. If the schema's actual behaviour differs from the plan's description, findings F-DS-01, F-DS-02, and F-DS-08 may need revisiting. I have flagged dependencies where the plan cites a source I cannot see rather than verifying it.

I have not assessed the corpus content, the planted under-implementations D1/D2, or the adequacy of the scenario queries themselves. My findings are about the *plan's structure, metrics, governance, and invalidation logic*, not about whether the scenarios would actually pass.

I have not assessed whether the `all-MiniLM-L6-v2` embedding model is appropriate for the use case in 2026. The plan does not justify the model choice; it states it as a fact. The plan's currency requirement asks whether the evaluation approach reflects older patterns. I note that `all-MiniLM-L6-v2` was released in 2021 and is widely considered a baseline model, not a state-of-the-art retrieval embedding in 2026. The plan does not defend its use, nor does it state what would trigger an upgrade. This is a gap, but I have not rated it because the plan's scope is the *test plan*, not the retrieval architecture selection. However, if the question is whether this plan reflects 2026 practice, the absence of any discussion of embedding model currency is itself notable. I note this as an observation rather than a finding.

I have not assessed the AWS migration-diff comparison semantics beyond the plan's §11 description, because the plan explicitly points to the schema as normative. The plan's §11.3 finding that `nondeterminism_source` is omissible is plausible but I cannot verify it without the schema.

I have not assessed the plan's treatment of generator seeds and reproducibility for scoring-class scenarios, because scoring scenarios are batch 2 and the plan's §6.1 states they are "out of scope" for the current batch. The plan's requirements on generator seeds are therefore forward-looking and not tested by the current coverage rule.

I have not assessed the plan's listing-versus-eligible distinction beyond §6.5, because I do not have the manifest resolver implementation. The plan's statement that "listed is not the same as eligible" is clear, but I cannot assess whether the resolver's behaviour matches the plan's description.

I have not assessed the plan's defect routing discipline (§10) beyond its internal consistency, because I do not have the WS-E ledger or CL register to compare against.

**Overall, the plan is a well-structured and technically serious document. The F1 handling is exemplary. The invalidation table is the correct shape. The gap-detection/retrieval-quality distinction is a crucial piece of discipline and is well-argued. However, the plan has two BLOCKING gaps: the coverage matrix does not discharge the TOR's typology requirement, and the H-8 immutability argument has a logical gap for harness defects discovered post-facto. The threshold-override rule is too permissive. These are fixable, but the plan should not be accepted as drafted.**

Reviewed hash: 21a5831f27cb55b98595413c9d047c433fe590c5a6939a82e18bdf64778e8caf
