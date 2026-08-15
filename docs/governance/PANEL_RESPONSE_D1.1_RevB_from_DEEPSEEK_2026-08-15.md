# PANEL RESPONSE — D1.1 Test Plan RevB — DEEPSEEK

**Round 2 · Received 2026-08-15**
**Reviewed hash:** `68270febf4a8ff092112e4adc8b0696c316e99053ac38e8e48cc5f2d007818dd` — reviewer states verified.

*Provenance: received via the coordinator conversation 2026-08-15 and
transcribed verbatim by the coordinator; transported to disk by the
operator. Chain of custody runs through the coordinator layer, not
directly from the reviewer interface.*

---

# D1.1 Test Plan Rev B — DeepSeek Panel Response

**Round 2, 2026-08-15**

**Reviewed hash (verified against pack §1):**
```
68270febf4a8ff092112e4adc8b0696c316e99053ac38e8e48cc5f2d007818dd
```

**Verification statement:** I have verified that the document I received hashes to the value above. This response is pinned to that hash.

---

## Overall technical verdict

**Rev B is a materially improved document that faithfully carries the round-1 disposition.** The architecture is now defensible: the coverage rule is honest, the threshold regime is coherent, the invalidation table is complete, and the evaluator integrity triangle is closed. However, **two MATERIAL findings remain open** — both are structural, not implementation-level, and both are deficiencies in the document's own reasoning rather than in its carriage of the disposition. The document is close to acceptance, but not yet there.

---

## Verification of carriage: round-1 findings

### C1 — Coverage and typology

| Finding | Carriage | Verdict |
|---|---|---|
| F-DS-04 (BLOCKING) | §2.1, §2.4, §2.5, Appendix A | **FAITHFUL** |
| F-GROK-01 | §2.4 | **FAITHFUL** |
| F-CHATGPT-01 | §2.1 | **FAITHFUL** |
| F-CHATGPT-01-D | §2.1, Appendix A | **FAITHFUL** |
| F-GEMINI-01 | §2.4, §2.5 | **FAITHFUL** |
| F-GROK-05 | Appendix A | **FAITHFUL** |
| G-ALT-REG | §2.5 | **FAITHFUL** |

**Comment:** The composite fix is implemented exactly as specified in R-2. The typology vocabulary requirement is correctly placed vertical-side (ADR-0009 boundary) — I confirm this reading. The PROVISIONAL label is properly load-bearing and not softened. **One subtle issue:** §2.4 states that per-scenario typology declaration "makes typology coverage assessable at spec level now" — but assessable by whom? A human reviewer checking manually, or mechanically? The RevB text is ambiguous. It should say "human-assessable" until the controlled vocabulary is defined. This is a MINOR clarity issue.

### C2 — Threshold and acceptance

| Finding | Carriage | Verdict |
|---|---|---|
| F-GROK-02 | §5.3 | **FAITHFUL** |
| F-CHATGPT-02 | §5.2 | **FAITHFUL** |
| F-DS-01 | §5.4 | **FAITHFUL** |
| F-DS-02 | §5.5 | **FAITHFUL** |
| F-DS-08 | §5.3 | **FAITHFUL** |
| F-GEMINI-02 | §5.4 | **FAITHFUL** |

**Comment:** The binary-probe extension to `|E| ≤ 4` is correctly implemented. The precision boundary at `|E| ≥ 5` is properly shared. The `top_k` ratio bound at 10% of 71 chunks is sensible. The coupled-pair treatment of weights and thresholds is correct. **One implementation note:** The variance discipline at §5.5 requires operator approval for threshold departures. There is no stated mechanism for how that approval is recorded — is it the same variance register as evidence substitution at §7.2(b)? The document implies yes but does not say so explicitly. This is MINOR.

### C3 — Evaluator and verdict integrity

| Finding | Carriage | Verdict |
|---|---|---|
| F-GROK-03 | §5.7(a), §8.1 criterion 6 | **FAITHFUL** |
| F-CHATGPT-03 | §5.7(b) | **FAITHFUL** |
| F-DS-03 | §9.1, §9.2 row 8 | **FAITHFUL** |
| Structural option | §6.8, §9.2 row 7 | **FAITHFUL** |

**Comment:** The fourth leg (evaluator version) is correctly introduced, and the rationale is properly stated. The golden-fixture suite is correctly positioned as an entry criterion. The content-addressed artefact with ledger hash is the correct architectural pattern. **One clarity issue:** The relationship between the evaluator version and the runner version is not fully specified. If the runner version changes but the evaluator version does not, does a result carry both? §6.8 says evaluation logic is "versioned independently of the runner as a whole" — but does the result carry the runner version as well? The reproducibility identity lists four legs; this is not among them. The omission is deliberate (only the evaluator matters for scoring semantics) but the reader has to infer this. **MINOR.**

### C4 — Invalidation completeness

| Finding | Carriage | Verdict |
|---|---|---|
| F-CHATGPT-04 | §9.2 row 6, §9.5 | **FAITHFUL** |
| F-CHATGPT-04-D | Discharged by joint adoption | **FAITHFUL** |
| F-GEMINI-03 | §9.5 elements 1–4 | **FAITHFUL** |
| F-GROK-04 | §9.2 row 2, §6.4 | **FAITHFUL** |
| F-DS-05 | §9.2 row 3, §9.3 | **FAITHFUL** |

**Comment:** The environment identity definition at §9.5 is complete. The "recorded processing facts" definition at §6.4 correctly excludes `ingest_timestamp`. The four reachable cases at §9.3 are correct and properly verified. Row 3's STANDS branch is confirmed.

### Singletons and pairs

| Finding | Carriage | Verdict |
|---|---|---|
| F-DS-06 | Appendix A.4 | **FAITHFUL** |
| D-001 | §12.1 | **FAITHFUL** |
| F-DS-07 | §8.3 | **FAITHFUL** |
| D-002 | §7.2(b) | **FAITHFUL** |
| F-CHATGPT-05 | §6.8, §8.1 criterion 4 | **FAITHFUL** |
| F-CHATGPT-06 | §12.3 | **FAITHFUL** |
| F-DS-09 | §12.3 | **FAITHFUL** |
| F-GROK-06 | §7.3 | **FAITHFUL** |
| F-GEMINI-04 | §7.3, Appendix B item 6 | **FAITHFUL** |
| F-GROK-07 | §8.1 | **FAITHFUL** |
| DS-CURRENCY | §12.3(3), §12.5, Appendix B item 8 | **FAITHFUL** |
| DS-PROTOCOL-01 | No RevB change | **FAITHFUL** |
| DS-PROTOCOL-02 | No RevB change | **FAITHFUL** |
| G-ALT-CI | §8.1 | **FAITHFUL** |

**Comment:** All rows are carried. Appendix C is accurate and complete.

---

## Finding F-DS-10 (MATERIAL) — The coverage rule is internally inconsistent on the `top_k` precision boundary

**Section:** §2.1, §5.4, Appendix A

**Issue:** The coverage rule at §2.1 Obligation A states that every eligible series carries **at least one** corpus-QA scenario. Obligation B states that every emitting series carries **at least one** citation-following scenario. Obligation C states exactly one scenario per planted gap.

The precision boundary at §5.4 requires an additional precision-or-rank criterion for `|E| ≥ 5` (or any scenario where distractor contamination bears on the claim). Appendix A instantiates scenarios. But **the coverage rule does not require that a series' scenario be one that actually exercises the precision criterion.**

This creates a structural problem: Suppose a series is covered by a corpus-QA scenario with `|E| = 4` (binary probe, no precision obligation). That series is **covered** under Obligation A. The fact that a different series has `|E| = 5` and carries precision is irrelevant — the claim "series X is covered" is true even though the scenario for series X might not exercise the precision-boundary rule at all.

**Why this matters:**

1. The coverage rule is one thing. The threshold rule is another. The document treats them as independent requirements. But for the coverage matrix to mean anything about retrieval quality, the scenarios that constitute coverage must *actually be* threshold-acceptance scenarios that the system can pass or fail.

2. A series that is covered by a binary probe (`|E| ≤ 4`) is equally covered — but its evidence is weaker (a binary yes/no). A claim "series X is covered by a corpus-QA scenario" does not distinguish between `|E| = 1` and `|E| = 8`. Yet the claims one might draw from those two scenarios are very different.

3. The `top_k` bound at §5.4 is expressed as a ratio against the *corpus* chunk count. But the coverage rule never requires that a scenario's `top_k` be set such that it actually tests retrieval in a meaningful way. A scenario with `top_k = 1` and `|E| = 1` is a trivial test; a scenario with `top_k = 7` and `|E| = 1` is also a binary probe but with greater sensitivity. The coverage rule is agnostic to this.

**What should change:**

The coverage rule should be amended to require that coverage scenarios also meet a minimum threshold of discrimination. The simplest form:

> **"Any corpus-QA scenario with `|E| ≤ 4` is a binary probe and is not, by itself, sufficient to evidence retrieval quality for that series. At least one scenario per series must either have `|E| ≥ 5` (and thus carry precision) or have a stated justification for why a binary probe is sufficient evidence for that series."**

Alternatively, the precision boundary could be made part of the coverage obligation: coverage means "at least one scenario that, if it passed, would be citable as evidence of retrieval quality under §5.4." That would align the coverage rule with the evidence standard.

**Why I rate this MATERIAL:** The document is internally coherent on each rule but does not ensure that the rules compose. A coverage matrix that is satisfied by binary probes over every series would be complete by the document's own criteria but would produce weak evidence. This is a structural flaw in how coverage and acceptance are connected, and it is not addressed anywhere in RevB.

---

## Finding F-DS-11 (MATERIAL) — The environment identity definition at §9.5 is underspecified for vector-index configuration

**Section:** §9.5 element 3

**Issue:** Element 3 of the environment identity is "vector-index configuration — index type and parameters, and the identity of the store the retrieval runs against."

This is too broad. "Index type" could mean an OpenSearch index type (e.g., `hnsw` vs `knn`), but it could also mean parameters like `ef_construction`, `m`, `ef_search`, `num_neighbors`, `algorithm`, `metric`, `space_type`, or the specific vector index version. "Parameters" is open-ended. "Identity of the store" could mean the URL, the index name, the S3 bucket, the OpenSearch cluster version, or the specific index build version.

**Why this matters:**

1. The row's assertability condition (§9.5) is that pre-flight can detect a change. If the definition is too broad (e.g., "index parameters" meaning everything in the index settings), pre-flight cannot reasonably pin it all without effectively pinning the entire index build — which is what the retrieval-snapshot hash already does.

2. If the definition is too narrow (e.g., only the algorithm type), a change in `ef_search` (which dramatically affects recall) would not be detected and would be a silent movement. That is exactly the failure mode the row exists to prevent.

3. The row needs to be **actionable**, not aspirational. A rule that says "any change to any vector-index configuration" without saying which parts are material is a rule that cannot be enforced uniformly.

**What should change:**

The definition should be tightened to a **specific enumerated list of configuration parameters that are considered material to retrieval behaviour**. This list can be maintained by the runner build and extended when new parameters are introduced, but the document should state the principle:

> **"Vector-index configuration changes that affect the similarity computation, retrieval algorithm, or search-space pruning are material. Changes that only affect resource allocation or logging are not material. The runner build maintains a named list of material parameters, and a result's environment identity includes the hash of that list at the time of the run."**

This aligns with the document's own principle: the identity must be something that can be observed, asserted, and compared. A broad statement is not actionable; a named list is.

**Why I rate this MATERIAL:** The row's assertability condition is explicitly stated as the reason pre-flight was extended. If the row's definition cannot be asserted, the row is not actually real — it's a statement of intent. The document needs to specify the mechanism by which a vector-index configuration change is detectable, or the row is weaker than it appears.

---

## Finding F-DS-12 (MINOR) — The controlled vocabulary requirement is stated, but its relationship to the manifest typology field is not fully specified

**Section:** §2.4

**Issue:** The controlled vocabulary must live vertical-side, not in the schema. The manifest typology field is deferred to the corpus workstream. Per-scenario typology declaration is required now.

But: **What happens if a scenario's declared typology does not match the manifest field once it lands?** Are mismatches errors? Are they evidential gaps? Does the scenario need to be re-authored? Are mismatches caught at acceptance review, or only after the corpus field lands?

The document says: "Per-scenario declaration makes typology coverage assessable at spec level now and reconciles with the corpus when the manifest field lands." But it does not say what reconciliation means.

**Why this matters:**

1. If a mismatch is ignored, the declaration was meaningless. If the mismatch is corrected by changing the declaration, the corrected declaration might no longer match the scenario's intended claim. If the mismatch is resolved by deferring the scenario's admissibility until the corpus field lands, then the "assessable at spec level now" claim is misleading.

2. The document should state a **reconciliation rule**, even if provisional. For example: "When the manifest typology field lands, the scenario's declared typology will be verified against it. A mismatch invalidates the scenario's prior results under §9.2 row 5 (spec hash change)." Or, alternatively: "The manifest field will be ignored for scenarios declared pre-field, and the declared typology governs."

**Why I rate this MINOR:** The issue is real but it is a gap in a provisional system. The document already acknowledges the typology situation as PROVISIONAL. A reader who understands that will know this is pending. It should be fixed for RevB because the document claims the field is "assessable at spec level," but it is not a BLOCKING/MATERIAL issue by itself.

---

## Finding F-DS-13 (MINOR) — The F1 investigation has no owner assigned

**Section:** Appendix B item 7

**Issue:** The single-chunk investigation is listed at Appendix B item 7 with owner "Unassigned." The disposition at R-1 says the act is "owned by platform architecture" but that was for the embedder decision record. The §12.3(3) investigation itself is unassigned.

**Why this matters:** An unassigned investigation is a note, not an obligation. The document routes the question to a named investigation, but does not say who is responsible for conducting it. The plan can be accepted without this being resolved (it is a post-acceptance item), but the document should either assign an owner or state that ownership is deferred with a named route.

**What should change:** Assign an owner, or state that ownership is deferred to the operator with a note that it will be assigned at the time the investigation is initiated.

**Why I rate this MINOR:** It does not affect the plan's ability to function, but it is an open action item that should be resolved before Regime 2 opens. The document already lists it as open; it just needs owner.

---

## Finding F-DS-14 (MINOR) — The §5.2 criterion 4 says E is fixed before any retrieval is run, but does not address scenario authoring tooling

**Section:** §5.2 criterion 4, Appendix D item 2

**Issue:** Appendix D item 2 notes that RQA-107 covers four statute documents of uneven chunk density (1, 1, 7, 16 chunks). The document notes this as a coverage question but does not resolve it.

The issue goes deeper: The expected set E is chosen by the scenario author during spec authoring. The author knows which documents are grounding. But the author may not know the chunk density distribution of those documents without manual inspection. If the author picks a document that happens to be single-chunk, the confound marker applies. If the author picks a multi-chunk document, no marker.

**Why this matters:** The §5.2 criterion 4 says E is fixed before retrieval is run. But the document does not address whether the author is expected to check chunk density before fixing E, or whether the author can rely on tooling. The "single-chunk confound" is only detected after the fact, by machine check of the resulting artefact. But by then, the scenario has already been authored. If the scenario has `|E| = 4` and one document is single-chunk, the scenario is a binary probe with a confound marker — and the policy at §12.3 says it routes to investigation before classification. But the author didn't necessarily intend that.

**What should change:** The document should note that scenario authors are expected to check chunk density when choosing grounding documents, and that the confound marker is a safety net, not a substitute for attention. This is a documentation/minor guidance issue.

**Why I rate this MINOR:** It is not a structural flaw; it's a note for scenario authors. The document has already placed the marker in the result, so the confound is visible. The only issue is whether the author is expected to know about it in advance.

---

## Severity summary

| Severity | Count | IDs |
|---|---|---|
| **BLOCKING** | 0 | — |
| **MATERIAL** | 2 | F-DS-10, F-DS-11 |
| **MINOR** | 3 | F-DS-12, F-DS-13, F-DS-14 |
| **OBSERVATION** | 0 | — |
| **TOTAL** | 5 | — |

---

## Acceptance recommendation

**Not accepted.** Two MATERIAL findings remain open. The document is close — the carriage is faithful and the structure is coherent — but two structural defects prevent acceptance:

1. **F-DS-10:** The coverage rule and the precision boundary do not compose. Coverage can be satisfied by binary probes that do not exercise the precision criterion.

2. **F-DS-11:** The environment identity definition is underspecified for vector-index configuration, making the row's assertability condition weaker than claimed.

If these are fixed in RevC (or via chair ruling that the document's interpretation of "coverage" already includes the precision criterion, or that the environment identity row is adequately specified), the document could be accepted.

---

## Dissent

None. All MATTERS are stated as findings. No reviewer disagreement requires a dissenting position.

---

## Additional notes

### On the regulatory lens (Gemini brief)

I note that the regulatory lens has been reassigned to Gemini and runs inside round 2. My findings are technical/architectural and do not overlap with the regulatory review. The plan's governance structure is materially improved; whether it survives a PRA/FCA lens is for Gemini to assess.

### On the B7 gate silence

The document's treatment at §7.3 — stating that preferred-primary harness evidence remains usable despite the gate document being silent — is pragmatic and correctly bounded. The gate-synchronisation patch is recorded as owed; the document does not over-claim. This is the right treatment.

### On the variance discipline

The document applies the same variance discipline to threshold departures (§5.5) and evidence substitution (§7.2(b)). This is a good architectural choice. It makes the document internally consistent on where rule departures are handled.

### On the F1 routing

The document handles F1 correctly: permanently inadmissible, cannot be cited as evidence, can motivate scenarios. The explicit ruling at §12.1 is the right approach. The single-chunk investigation with four candidate mechanisms is appropriately structured.

### On the embedder currency

The document correctly routes this out of scope, names the timing consequence (free today, expensive later), and records the need for a decision record before Regime 2 opens. This is a mature treatment.

---

## Hash verification

I verify that the document I reviewed hashes to:

```
68270febf4a8ff092112e4adc8b0696c316e99053ac38e8e48cc5f2d007818dd
```

This response is pinned to that hash.
