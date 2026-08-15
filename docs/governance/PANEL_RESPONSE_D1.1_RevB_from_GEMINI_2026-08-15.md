# PANEL RESPONSE — D1.1 Test Plan RevB — GEMINI (REGULATORY LENS)

**Round 2 · Received 2026-08-15 · On-roster, regulatory lens per circulation pack §4**
**Reviewed hash:** `68270febf4a8ff092112e4adc8b0696c316e99053ac38e8e48cc5f2d007818dd` — reviewer states verified match.

*Provenance: received via the coordinator conversation 2026-08-15 and
transcribed verbatim by the coordinator; transported to disk by the
operator. Chain of custody runs through the coordinator layer, not
directly from the reviewer interface.*

---

This review is delivered on-roster carrying the **regulatory lens** brief set out in circulation pack §4 (EU AI Act, UK GDPR, PRA SS1/23, FCA operational risk/conduct, DORA).

---

### RevB Governing Hash Verification

The RevB hash in pack §1 has been verified against the received document before review:
`68270febf4a8ff092112e4adc8b0696c316e99053ac38e8e48cc5f2d007818dd` — **VERIFIED MATCH**.

---

### Regulatory-Lens Findings Summary

| Severity | Count |
| --- | --- |
| **BLOCKING** | 1 |
| **MATERIAL** | 2 |
| **MINOR** | 2 |
| **OBSERVATION** | 1 |
| **Total** | **6** |

---

### Findings

#### F-GEM-REG-01 — **BLOCKING**

* **Frameworks:** EU AI Act (Art. 10(2)-(4) Data & Governance; Art. 13 Transparency); UK GDPR (Art. 5(1)(a) Transparency, Art. 22 Automated Decision-Making).
* **Summary:** The PROVISIONAL typology label (§2.4) allows formal Regime 2 execution without machine-asserted typology coverage, while §2.4 permits per-scenario typology self-declarations using opaque strings without a enforced vertical schema or controlled vocabulary. Under the EU AI Act and UK GDPR, generating "formal gate evidence" on unvalidated, self-declared typology data creates legal liability by asserting compliance over unverified bias/coverage profiles.
* **Analysis:** Section 2.4 explicitly admits that a Regime 2 run does not prove typology coverage because the manifest lacks a typology field. To paper over this, §2.4 requires per-scenario string declarations, but defers the controlled vocabulary to an unauthored vertical artefact. Allowing formal execution under Regime 2 while relying on unvalidated free-text scenario metadata permits scenario authors to assert coverage for critical fraud types (e.g., Authorized Push Payment fraud vs. Card-Not-Present) without algorithmic or schema verification. Under EU AI Act Art. 10, high-risk AI training/testing datasets must be subjected to appropriate data governance and representation checks. Allowing formal evidence generation under a "PROVISIONAL" label where data provenance is unverified creates non-compliant audit trails under EU AI Act Art. 13 and UK GDPR Art. 5(1)(a).
* **Required Fix:** Regime 2 execution must be **hard-gated** on the landing of the machine-readable manifest typology field and an enforced vertical controlled vocabulary. The "PROVISIONAL" execution route for Regime 2 must be revoked — Regime 2 execution cannot open under a provisional coverage disclaimer.

---

#### F-GEM-REG-02 — **MATERIAL**

* **Frameworks:** PRA SS1/23 (Model Risk Management, Principle 3 - Model Validation & Outcome Coping); FCA General Guidance on AI/ML.
* **Summary:** The 10% `top_k` chunk-ratio bound (§5.4) relaxes automatically as the corpus grows, causing the test acceptance difficulty to loosen dynamically without a governed model-risk re-validation act.
* **Analysis:** Section 5.4 establishes that `top_k` may not exceed 10% of the indexed chunk count of the eligible set without a flag. As the corpus grows (e.g., from 71 chunks to 700 chunks), an unflagged scenario's permissible `top_k` scales from 7 to 70. In retrieval-augmented generation (RAG) and semantic search models, expanding `top_k` linearly with corpus size drastically increases noise payload and distractor density, fundamentally altering the precision profile of the retriever. Under PRA SS1/23 Principle 3, model testing thresholds and pass criteria must remain rigorous, fixed, and auditable across model versions; allowing dynamic relaxation of effective retrieval bounds when the underlying corpus expands masks performance degradation and invalidates prior validation baselines.
* **Required Fix:** Fix absolute `top_k` caps per scenario class in the scenario spec, or require a formal Model Risk Management (MRM) re-validation event whenever a corpus expansion alters the effective `top_k` window by more than a specified threshold.

---

#### F-GEM-REG-03 — **MATERIAL**

* **Frameworks:** DORA (Art. 11 Backup & Recovery Policies / System Integrity); PRA SS1/23 (Principle 2 - Model Governance / Change Management).
* **Summary:** §9.2 row 8 invalidates runner outputs upon a confirmed evaluator defect, but fails to mandate a automated ledger rollback or state assertion for downstream audit consumers, creating a risk of stale/invalidated evidence exposure during supervisory inspection.
* **Analysis:** When a harness defect is confirmed under §9.2, affected historical results are declared invalidated. However, while §9.3 states invalidated results "remain in the ledger, marked", §9 and §10 provide no machine-asserted API contract or cryptographic retraction flag that prevents external reporting tools, B7 gate evaluation scripts, or third-party audit exports from reading those invalidated results as active. Under DORA Art. 11 and PRA SS1/23, operational resilience and model tracking demand strict integrity of audit logs. If an invalidated run can be inadvertently fetched or cited in a gate pack due to missing state assertions, the evidence chain fails supervisory scrutiny under FCA/PRA audits.
* **Required Fix:** Require that the D2.5 ledger entry schema carry an explicit, machine-readable `invalidation_status` flag and cryptographic revocation signature, and enforce that pre-flight / gate-evaluation tools automatically filter out any ledger entry marked invalidated.

---

#### F-GEM-REG-04 — **MINOR**

* **Frameworks:** DORA (Art. 12 ICT Change Management); PRA SS1/23 (Principle 4 - Operational Risk).
* **Summary:** §8.1 pre-flight check defines environment identity pinning but leaves vector database / index configuration drift (e.g., distance metric, HNSW parameters) partially delegated without a mandatory machine-asserted hash.
* **Analysis:** Section 8.1 and §9.2 (row 6) recognise vector-index configuration and embedder configuration changes as invalidation triggers. However, §8.1 does not require an explicit `vector_index_sha256` or equivalent environment config hash to be verified during pre-flight before issuing execution authorization under Regime 2. In vector search platforms, subtle changes in index parameters (e.g., `efSearch`, `M` parameters in HNSW, distance metrics) directly alter retrieval outputs without modifying model weights or document content.
* **Required Fix:** Add an explicit, machine-asserted `environment_config_sha256` (covering vector store and embedding configurations) to the six mandatory pre-flight criteria in §8.1.

---

#### F-GEM-REG-05 — **MINOR**

* **Frameworks:** UK GDPR (Art. 5(2) Accountability Principle); FCA FG21/1 (Operational Resilience).
* **Summary:** §7.2 operator-ruled variance pattern for evidence substitution lacks a mandatory time-bound retention limit or statutory logging standard for operator justifications.
* **Analysis:** Section 7.2 permits substituting preferred-primary evidence via an operator-ruled variance recorded in the register. While converting this to an operator variance strengthens governance compared to RevA, the plan does not define a mandatory logging schema, retention period, or regulatory notification trigger for long-standing variances. Under UK GDPR accountability rules and FCA operational resilience guidelines, discretionary overrides in automated safety controls must carry auditable justification metadata and periodic expiration dates.
* **Required Fix:** Require all §7.2 evidence substitution variances to include an explicit expiration date (or gate-horizon limit) and a structured justification payload within the variance register.

---

#### F-GEM-REG-06 — **OBSERVATION**

* **Frameworks:** EU AI Act (Art. 14 Human Oversight); PRA SS1/23.
* **Summary:** §12 defect routing handles single-chunk confounds via pre-classification investigation, but lacks formal SLA timing boundaries for completing investigations prior to gate submission.
* **Analysis:** Section 12.3 and §12.4 route single-chunk marked scenario failures to investigation prior to defect classification. While methodologically sound, the plan does not specify maximum turnaround windows or escalation paths for unresolved investigations prior to B7 gate submission. From a regulatory oversight perspective, open-ended diagnostic investigations can become institutional bottlenecks that delay time-sensitive regulatory disclosures or gate reviews.
* **Required Fix:** Note for operational implementation: establish an explicit SLA (e.g., 5 business days) for completing §12 investigations before B7 gate submission.

---

### Acceptance Recommendation

Under the Round 2 acceptance rule (§2.1 of the circulation pack), RevB **cannot be accepted** as drafted due to the presence of finding `F-GEM-REG-01` rated **BLOCKING**.
