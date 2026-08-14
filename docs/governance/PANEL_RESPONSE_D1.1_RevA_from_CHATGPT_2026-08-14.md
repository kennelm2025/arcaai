<!-- PROVENANCE: Response received by the chair from the ChatGPT session and
relayed via the coordination chat to this file, 2026-08-14. The chair
attests this text matches the ChatGPT tab. Committed under the PANEL-ROUND
CONVENTION: verbatim, unedited below this comment block, pinned to the
reviewed hash. -->

# PANEL RESPONSE — D1.1 Test Plan RevA — ChatGPT

**Reviewed hash:** `21a5831f27cb55b98595413c9d047c433fe590c5a6939a82e18bdf64778e8caf`

## FINDINGS

### F-CHATGPT-01: Coverage rule and instantiated matrix do not currently agree

**Section(s):** §2.1, Appendix A
**Severity:** **MATERIAL**

**Finding:** The stated coverage rule is:

> "Every retrieval scenario class × every document series represented in the current listed snapshot's eligible set"

but Appendix A does not instantiate that Cartesian product. It contains seven corpus-QA scenarios covering the seven series, but only two citation-following scenarios and two gap-detection scenarios. The plan subsequently claims that "Every eligible series is covered by at least one corpus-QA scenario, satisfying the rule." That is a weaker rule than the one actually stated.

This matters because a rule-shaped matrix is being presented as the control that guarantees coverage as the corpus changes. If the intended rule is actually "every series must have corpus-QA coverage, with selected citation-following and gap-detection coverage", that is defensible but materially different. If the stated Cartesian-product rule is intended, Appendix A is presently under-instantiated.

**Shape of a fix:** Make the coverage rule and its regeneration logic express the same requirement. Either instantiate every class × series combination, or explicitly define the class-specific coverage obligation rather than claiming a Cartesian product.

---

### F-CHATGPT-02: The acceptance rule controls the threshold mathematically, but not the construction of the expected set

**Section(s):** §5.1–§5.2
**Severity:** **MATERIAL**

**Finding:** The plan gives a carefully constructed default threshold based on `|E|`, and correctly identifies the binary nature of `|E| = 1`. However, the acceptance mechanism leaves the most consequential input to that calculation — the composition and granularity of the expected grounding set `E` — to scenario authoring. A scenario can therefore materially change its acceptance difficulty by defining the grounding at a different granularity, while still complying with the threshold rule. The only stated control on a per-scenario acceptance override is that it "must carry a stated reason."

This is not a mathematical defect in the threshold formula. It is a test-design governance gap: the plan governs *how the threshold follows from E* more strongly than it governs *how E is constituted*. For an external reviewer, that leaves room for apparently compliant but strategically favourable scenario construction.

**Shape of a fix:** Define the review/control point for expected-set construction and the permitted granularity, independently of the threshold calculation. A stated reason alone should not be the only control where changing `E` changes the effective acceptance bar.

---

### F-CHATGPT-03: H-8 makes the ledger verdict immutable, but does not establish integrity of the result artefact to which it also applies

**Section(s):** §5.3–§5.4
**Severity:** **MATERIAL**

**Finding:** The plan requires the runner to write the verdict both to the D3.1 result artefact and the D2.5 ledger, with immutability explicitly attached to the **ledger**. It does not say that the result artefact itself is immutable, content-addressed, or cryptographically bound to the immutable ledger entry. Yet the result artefact carries the threshold, `|E|`, and `top_k`, and is therefore part of the evidential interpretation of the verdict.

An immutable ledger entry saying `PASS` does not by itself prevent the associated result artefact from subsequently being changed in a way that alters the inputs or measured result to which that `PASS` appears to refer. The two records need an explicit integrity relationship, not merely duplicate storage.

**Shape of a fix:** Require the ledger record to bind cryptographically to the complete result artefact, or otherwise make the artefact itself immutable/content-addressed. The invariant should be that the immutable verdict can always be shown to refer to exactly the result bytes that produced it.

---

### F-CHATGPT-04: Environment drift is a suspension trigger but has no corresponding invalidation rule

**Section(s):** §8.3, §9.2–§9.3
**Severity:** **MATERIAL**

**Finding:** §8.3 explicitly says a formal session halts on "environment drift" and that re-entry requires a freshly pinned reproducibility triple. It then says that which prior results survive the movement causing suspension is determined by §9.

But the §9 invalidation table contains rows for eligible-set, retrieval-snapshot, manifest, model and spec movement — **not environment movement**.

This leaves a real operational state without a defined consequence. A reviewer can know that environment drift stops the session, but cannot determine from the Test Plan which previously produced results remain admissible, which are invalidated, or what exactly must be re-run.

**Shape of a fix:** Add an explicit environment/toolchain movement rule, including what constitutes an environment identity change and which result classes depend upon it.

---

### F-CHATGPT-05: "Model version stated" is weaker than the reproducibility control used elsewhere

**Section(s):** §8.1, §6.7, §9.2
**Severity:** **OBSERVATION**

**Finding:** The formal entry criterion says only that the "Model version [is] stated", while the plan's overall evidence discipline is otherwise built around pinned identities and hashes. The reproducibility triple includes "model version", but the plan does not here establish whether that identifier is immutable/content-addressed or merely a version label.

For a governed evidence chain, the distinction matters: a mutable artefact behind a stable version label would weaken the otherwise strong reproducibility model.

**Shape of a fix:** Clarify elsewhere in the model-governance chain that the model version carried by a result resolves to an immutable model artefact, or explicitly require its content identity here.

---

### F-CHATGPT-06: Known single-chunk confound is required procedurally but not visibly controlled as evidence

**Section(s):** §12.3, Appendix A
**Severity:** **MINOR**

**Finding:** The plan correctly identifies the single-chunk statute population as a known confound and says that it "must be recorded with the result". Two currently eligible documents are affected.

However, the requirement is prose-level. The plan does not identify a mandatory result field, schema assertion, or other machine check that makes omission of that confound detectable. Given the otherwise strong treatment of mandatory provenance and acceptance metadata, this is an unusual manual dependency.

**Shape of a fix:** Make the confound a machine-checkable result attribute for affected scenarios, or explicitly state that its presence is validated as part of result admissibility.

---

## DISSENTS

I do **not** dissent from the overall architecture of the plan. The separation between retrieval quality, gap detection, provenance, admissibility and B7 evidence is strong, and the permanent treatment of Regime 1/F1 is correctly disciplined.

I do dissent from the proposition, implicit in the current §2 wording, that the instantiated Appendix A demonstrates the stated coverage rule. It does not: the prose says Cartesian-product coverage, while the appendix demonstrates series coverage for corpus QA plus selected scenarios for the other classes. That distinction should be resolved before the rule is treated as the durable coverage control.

I also regard the environment-drift gap as more than a documentation nicety. The plan deliberately makes environment drift a formal suspension condition, then delegates its survival consequences to §9, but §9 does not contain the corresponding movement. That is a genuine hole in the execution state machine.

## CONFIDENCE AND LIMITS

The reviewed bytes were hash-verified against the circulation pack: `21a5831f27cb55b98595413c9d047c433fe590c5a6939a82e18bdf64778e8caf`. The circulation pack explicitly requires that exact hash to be verified before review.

I reviewed the D1.1 plan itself and the panel circulation/request documents. I did **not** review the underlying TOR, scenario schema, rulings record, B7 gate document, runner implementation, or manifest. Where this review relies on the plan's description of those artefacts, I have treated that description as the basis rather than independently validating the cited artefact.

The strongest findings are therefore **internal findings against the Test Plan as written**, rather than assertions that an underlying implementation definitely behaves incorrectly. The panel request explicitly requires that distinction where cited source material is unavailable.
