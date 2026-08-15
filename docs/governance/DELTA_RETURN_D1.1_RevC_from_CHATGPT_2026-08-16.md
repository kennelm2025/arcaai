# DELTA RETURN — D1.1 Test Plan RevC — CHATGPT

**Delta round · Received 2026-08-16 (session of 2026-08-15)**
**Reviewed hash:** `9d6ab3b0da21d5e6603f7fa505d48a892da9acf11dba60725b83e5a8c590e88c` — INDEPENDENTLY RECOMPUTED by the reviewer.
**Scope:** R2-01 (residual MATERIAL per delta pack §5)

*Provenance: received via the coordinator conversation and transcribed
verbatim by the coordinator; transported to disk by the operator.*

---

## D1.1 Rev C — Delta Review: ChatGPT

I reviewed the Rev C delta under the **light-delta scope**, not as a whole-document re-review. The circulation pack limits my task to verifying whether the implementing text discharges my sustained MATERIAL finding, **R2-01**, with a new finding permitted only if there is a defect in the fix itself.

### Hash verification

I independently computed the SHA-256 of the uploaded Rev C file:
**`9d6ab3b0da21d5e6603f7fa505d48a892da9acf11dba60725b83e5a8c590e88c`**
This exactly matches the governing hash in the Rev C delta pack, which states that it was confirmed against the working file and committed blob at merged `main`.

---

# R2-01 — Evaluator semantic-change invalidation gap

### **DISCHARGED**

My Round-2 finding was that Rev B had a logical hole between §9.2 rows 7 and 8:

* an evaluator changed with demonstrated equivalence → row 7;
* a confirmed defect → row 8;
* but an **intentional semantic change** was neither an equivalence case nor a defect, leaving no invalidation route.

Rev C closes that hole explicitly.

The new three-way treatment is:

1. **Implementation changed, behaviour equivalent and demonstrated** → row 7a; nothing invalidated.
2. **Implementation defective, confirmed** → row 8; affected results invalidated.
3. **Semantics intentionally changed** → row 7b; affected prior results invalidated or re-baselined.

That is the exact missing case identified in my finding.

### The fixture-suite issue is also properly closed

I specifically noted in Round 2 that the golden-fixture suite only established threshold-comparison behaviour and was **not sufficient to establish whole-evaluator semantic equivalence**.

Rev C does not make that mistake. It expressly says the fixture suite is necessary but insufficient, and creates a separate §9.7 equivalence test.

The three conditions are:

* fixtures green at both versions;
* retained affected results replay to the same verdict;
* **no intended behaviour change**.

Crucially, an asserted intention to change behaviour automatically moves the change to 7b regardless of fixture results.

That is materially stronger than the Rev B position and directly addresses the concern I raised.

### I also checked for a defect in the fix

I do **not** find one.

The per-class scope of 7b is explicit, avoiding unnecessary invalidation of unrelated result classes.

The disposition also correctly records that the fixture/equivalence distinction was part of the adopted fix rather than silently assumed.

---

## Result

| Finding                                                | Round-2 severity | Rev C result   |
| ------------------------------------------------------ | ---------------: | -------------- |
| **R2-01 — evaluator semantic-change invalidation gap** |         MATERIAL | **DISCHARGED** |

**No new finding raised. No dissent.**

The defect I identified in Rev B is closed by Rev C's implementing text.

**Verified Rev C hash:**
`9d6ab3b0da21d5e6603f7fa505d48a892da9acf11dba60725b83e5a8c590e88c`
