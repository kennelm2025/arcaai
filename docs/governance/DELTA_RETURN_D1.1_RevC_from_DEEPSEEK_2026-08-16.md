# DELTA RETURN — D1.1 Test Plan RevC — DEEPSEEK

**Delta round · Received 2026-08-16 (session of 2026-08-15)**
**Reviewed hash:** `9d6ab3b0da21d5e6603f7fa505d48a892da9acf11dba60725b83e5a8c590e88c` — reviewer states verified.
**Scope:** F-DS-10, F-DS-11 (residual MATERIALs per delta pack §5; F-DS-11 composite with F-GEM-REG-04)

*Provenance: received via the coordinator conversation and transcribed
verbatim by the coordinator; transported to disk by the operator.*

---

# D1.1 Test Plan Rev C — DeepSeek Delta Response

**Delta Round, 2026-08-16**

**Reviewed hash (verified against pack §1):**
```
9d6ab3b0da21d5e6603f7fa505d48a892da9acf11dba60725b83e5a8c590e88c
```

**Verification statement:** I have verified that the document I received hashes to the value above. This response is pinned to that hash.

---

## Verification of assigned findings

### F-DS-10 — Coverage and precision boundary compose

**DISCHARGED.**

Rev C implements §2.1 Obligation D exactly as my finding required, adopting my proposed sentence in substance:

> **"A series covered only by binary probes — every one of its scenarios at `|E| ≤ 4` — requires at least one scenario at `|E| ≥ 5`, or a stated justification why a binary probe is sufficient evidence for that series."**

This closes the defect: a coverage matrix satisfiable entirely by binary probes is no longer complete by the plan's own criteria. The adopted form keeps coverage and acceptance separate, which is the right architectural choice — a change to §5.4 should not silently change what coverage means.

**The density-stratified note at §5.2 and Appendix A.1 further strengthens the composition** by requiring authors to check chunk density when fixing E, and requiring a note where a series spans more than a 4× ratio. The Statute series at 16× is the live instance, and a single scenario now cannot satisfy Obligation A without stating which density extremes it exercises.

The one thing I would note: Obligation D is stated in prose at §2.1, but Appendix A.1 does not explicitly reference it in its "Obligation D applies per series" note. The note does say "expected sets are fixed at spec authoring, so which series this bites is not knowable from this table alone; it is checked at scenario acceptance" — which is sufficient. A cross-reference would be clearer but is not required for discharge.

**DISCHARGED.**

---

### F-DS-11 — §9.5 element 3 too broad to assert (composite with F-GEM-REG-04)

**DISCHARGED.**

Rev C tightens element 3 to a **named list of material parameters**, with the materiality test stated in terms:

> **"A vector-index or embedder configuration parameter is MATERIAL if it affects the similarity computation, the retrieval algorithm, or search-space pruning. Parameters affecting only resource allocation or logging are NOT material."**

The runner build maintains the list, and **the list's own hash is carried in the environment identity** — so narrowing the list is itself a detectable movement. This addresses both the assertability problem I identified (what counts as material is now defined) and the pre-flight detection problem Gemini identified (criterion 7 adds `environment_config_sha256`).

**The key innovation is the hash of the list itself.** Without it, a future maintainer could narrow the list to exclude parameters that drift, and the environment identity would remain unchanged. The two-hash design closes that.

**Two implementation notes for the runner build:**

1. The named list must include search-time parameters like `ef_search`, not just index-build parameters like `m` and `ef_construction`. My reading of §9.5 element 3 ("retrieval algorithm" and "search-space pruning") covers both. The list's materiality test says "retrieval algorithm" — which includes search-time behaviour — so `ef_search` should be in scope.

2. `environment_config_sha256` at §8.1 criterion 7 must be machine-asserted pre-flight. The document says "mismatch, or an unreadable configuration, blocks the session" — which is the correct failure mode.

**DISCHARGED.**

---

## Defect-in-fix check

I have read the implementing sections for both findings. Neither fix introduces a new defect. The following are observations, not findings:

- The density-stratified note at Appendix A.1 says "RQA-107 requires a density-stratified note" but does not say **where** that note lives. It presumably lives in the scenario spec or in the acceptance review record. This is a documentation clarity issue, not a defect in the fix.

- The named list of material parameters is "maintained by the runner build" but no process is stated for when a new parameter is introduced that is material. The plan's deferral to the runner build is appropriate — this is an implementation detail. The plan states the principle; the runner build implements the list.

---

## Disposition of round-2 MINORs

I note that all eleven MINORs were disposed at the round-2 disposition, and their Rev C landings are traceable at Appendix C.2. I have verified my own MINOR findings:

| Finding | Rev C landing | Status |
|---|---|---|
| DS C1 note | §2.4 — "human-assessable" | DISCHARGED |
| DS C2 note | §5.5 — one variance register named | DISCHARGED |
| DS C3 note | §6.8.1 — runner version deliberately not a leg | DISCHARGED |
| F-DS-12 | §2.4 — reconciliation rule via §9.2 row 5 | DISCHARGED |
| F-DS-13 | Appendix B item 7 — owner OPERATOR | DISCHARGED |
| F-DS-14 | §5.2 — density check and 4× stratified note | DISCHARGED |

---

## Overall delta verdict

**Both MATERIAL findings are DISCHARGED.**

The fixes are faithful to the ruling and close the defects my findings identified:

1. **F-DS-10** is closed by Obligation D, which ensures coverage and precision compose.
2. **F-DS-11** is closed by the named-list mechanism with list-hash carry, which makes §9.5 element 3 assertable.

No defect in either fix is present. The document is materially improved.

---

## Dissent

None. My findings are discharged as ruled. The chair's rulings on both findings are consistent with the substance of what I identified.

---

**Hash verification:** I verify that the document I reviewed hashes to:

```
9d6ab3b0da21d5e6603f7fa505d48a892da9acf11dba60725b83e5a8c590e88c
```

This response is pinned to that hash.
