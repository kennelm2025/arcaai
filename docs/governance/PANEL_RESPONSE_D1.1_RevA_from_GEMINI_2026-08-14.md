<!-- PROVENANCE: Response received by the chair from the Gemini session and
relayed via the coordination chat to this file, 2026-08-14. The chair
attests this text matches the Gemini tab. Composition note: Gemini was
fielded OFF-ROSTER by chair direction (Mistral, the on-roster regulatory
seat, was unavailable to the operator this round); Gemini reviewed under
an in-pack role brief, no committed primer. LaTeX-style notation
($\vert{}E\vert{}$ etc.) is the reviewer's own rendering, preserved
as-received. Committed under the PANEL-ROUND CONVENTION: verbatim,
unedited below this comment block, pinned to the reviewed hash. -->

PANEL RESPONSE — D1.1 Test Plan RevA — GEMINI

Reviewed hash: `21a5831f27cb55b98595413c9d047c433fe590c5a6939a82e18bdf64778e8caf`

---

## Summary

The D1.1 Draft Test Plan (Rev A) provides a rigorous, highly disciplined, and governance-first foundation for formal execution (Regime 2). The document excels in establishing clear data provenance, binding immutability requirements, and enforcing a strict separation between presence (retrieval quality) and absence (gap detection). However, material gaps remain regarding edge-case coverage within the dynamic coverage rule, potential gaming vectors in threshold formulas for small grounding sets, and an incomplete row structure in the invalidation matrix.

---

## Strengths

* **Rigorous Boundary Enforcement**: The plan clearly separates presence measurements (Corpus QA, Citation-following) from absence measurements (Gap Detection), preventing misinterpretation of gap-detection capability as broad retrieval quality.

* **Immutable Governance Pack**: The machine-asserted criteria for entry/exit, regime marking, and pass/fail verdicts—specifically making verdicts immutable in the results ledger (H-8)—significantly reduces human operational error and tampering risks.

* **Traceable Data Provenance**: Requiring the full reproducibility triple (spec hash + model version + corpus snapshot) for every result ensures strict line-of-sight auditing across execution runs.

* **Proof-First Approach**: Authoring the plan against an operational, executed runner spike (D2.2a) ensures that governance rules are grounded in working software rather than aspirational design.

---

## Concerns / Findings

### F-GEMINI-01: Coverage Rule Fails to Bound Corpus Expansion or Dynamic Schema Shifts

* **Section(s)**: §2.1, §2.4, Appendix A

* **Severity**: MATERIAL
* **Finding**: The plan defines coverage dynamically over the current listed snapshot's eligible set rather than a fixed list. While this avoids plan stale-mate during corpus growth, it leaves a loophole: if a new document series is added or an existing series drifts drastically in chunk density, Appendix A becomes out of date without requiring a governed panel review. Furthermore, because the manifest lacks structured series or typology fields (§2.4), series assignment is determined manually from `source:` prose, introducing subjective human error into an otherwise automated rule.

* **Shape of a fix**: Require that any change to the eligible set that introduces a new series triggers an automated schema check and an explicit, ledgered "coverage audit event," even if a full plan amendment is not invoked.

### F-GEMINI-02: Degenerate Behavior in Binary Probe Thresholds ($\vert{}E\vert{} = 1$)

* **Section(s)**: §5.2

* **Severity**: MATERIAL
* **Finding**: The default formula for semantic-distance scenarios ($\text{ceil}(0.8 \times \vert{}E\vert{}) / \vert{}E\vert{}$) evaluates to $1.0$ for all $\vert{}E\vert{} \le 4$. For single-chunk or single-document grounding sets ($\vert{}E\vert{} = 1$), the sensitivity relies entirely on `top_k`. If `top_k` is set excessively high (e.g., `top_k = 20` on a tiny corpus), a scenario can achieve a trivial pass while producing a noise-heavy payload that degrades downstream agent context windows. The threshold rule lacks a bound on `top_k` relative to total corpus size or expected set size.

* **Shape of a fix**: Introduce a maximum allowable `top_k` ratio relative to $\vert{}E\vert{}$ or total corpus chunk count within the default threshold rule, or flag scenarios where `top_k` exceeds a defined context ratio.

### F-GEMINI-03: Invalidation Table Omits Environmental and Dependency Movement

* **Section(s)**: §9.2

* **Severity**: MATERIAL
* **Finding**: The five-row invalidation table covers eligible set, retrieval snapshot, manifest, model version, and spec hash changes. It misses two critical vectors: (1) **Runner or execution environment drift** (e.g., updates to ONNX runtime, vector DB index settings, underlying chunker code without snapshot hash updates), and (2) **Embedder configuration changes** (e.g., changes to normalization or distance metrics). If the runner infrastructure updates its execution dependencies, prior Regime 2 results may be rendered un-reproducible despite snapshot and model versions remaining identical.

* **Shape of a fix**: Add a row to the §9.2 invalidation table explicitly addressing runner/dependency updates, mandating re-flight or pre-flight checksum validation of the runtime binary environment.

### F-GEMINI-04: Unaddressed Gap Between Gate B7 and Harness Requirements

* **Section(s)**: §7.3, Appendix B

* **Severity**: MINOR
* **Finding**: Section 7.3 correctly identifies that `docs/build/B7_GATE.md` contains no reference to the harness or D1/D2 gap detection. While this is explicitly routed to the B7-exit ruling pack, operating under a preferred-primary evidence model (§7.1) while the gate documentation itself remains entirely silent on the harness creates an audit ambiguity during a PRA/FCA-style inspection.

* **Shape of a fix**: Note in §7.3 a formal requirement for a B7_GATE.md synchronisation patch prior to triggering the first gate exit under Regime 2.

---

## Alternative Perspectives

* **Auditor / Regulatory Lens**: An external auditor might find the dynamic coverage rule (§2.1) overly permissive. Regulators generally prefer explicit, version-locked lists of test cases per gate rather than algorithmically generated sets, as dynamic generation can mask omissions if the underlying generator script carries a bug.

* **Engineering / CI Lens**: A build engineer might argue that forcing hard pre-flight failures on SKIPPED/UNKNOWN states (§8.1) without a distinct dry-run pipeline mode could impede CI pipeline diagnostics and developer velocity during early iteration phases.

---

## What I Cannot Assess

* **Code-Level Runner Enforcement**: I cannot verify whether the runner implementation (`scripts/d22a_preflight.py` or D2.2a/b) correctly enforces ledger immutability and regime markers as described in §5.3 and §8.1.

* **Schema Enforcement Validation**: I cannot independently validate `arcaai/harness/schema/scenario_spec_v0.2.schema.json` to confirm that bit-identical vs. tolerance parameters are structurally blocked as claimed in §11.2.

* **External Gate Requirements**: I cannot verify whether non-harness evidence routes permitted under §7.2 satisfy specific PRA/FCA regulatory mandates.

---

## Dissents

* **None.** The operator's preference for a preferred-primary gate model (Ruling 3) over a hard single-point dependency is pragmatically justified for an early-stage harness, provided the equivalence test (§7.2c) is strictly enforced.

---

## Confidence and Limits

This review was conducted solely against the provided text of `D1.1_TEST_PLAN_DRAFT_RevA_2026-08-14.md` (hash `21a5831f27cb55b98595413c9d047c433fe590c5a6939a82e18bdf64778e8caf`) and associated pack guidelines. External file references (e.g., TOR Rev C, B7_GATE.md, schema files) were assessed based on the excerpts and logic contained within the draft text itself.
