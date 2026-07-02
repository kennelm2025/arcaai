# ArcaAI — DECISIONS.md

Decision log for the ArcaAI document suite and initial build. Locked June 2026.
Every change to a locked document, and every build deviation from the locked suite,
requires an entry here. Format: ID · decision · date · status.

\---

## Cross-document rulings (R1–R13) — all approved June 2026

* **R1 — Use-case register.** Canonical register: 11-use-case catalogue (Banking Architecture table), 3 in Phase 1 build scope (Fraud, Compliance, RM), 9 by end of Phase 2. AML is not a separate catalogue entry; it sits in the Fraud vertical roadmap. *Applied: BA, SA, EB, deck.*
* **R2 — Layer models.** Banking Architecture L1–L5 is the canonical technical model. Learning Bank's five-layer set renamed "five capabilities" (a value lens) with an explicit mapping to L1–L5. *Applied: LB §4.*
* **R3 — Positioning.** Client-facing strategic material leads with "the AI control layer for regulated banking decisions"; engineering documents keep "platform" internally but carry the control-layer strapline. *Applied: BA cover, deck slides 1 \& 10.*
* **R4 — Database.** PostgreSQL (containerised) from day 1; SQLite dropped from Phase 1; former migration workstream 1 removed. Phase 2 adds HA (primary + hot standby, PgBouncer). *Applied: SA, TI; EB already compliant.*
* **R5 — Vector store.** Phase 2 vector store is a self-managed on-prem OpenSearch cluster. No managed-cloud vector store: rm\_knowledge contains customer data. *Applied: SA, TI.*
* **R6 — Jurisdiction \& currency.** UK-first (PRA/FCA primary; EBA/Basel as supranational context); GBP throughout. Cost model restated at €0.86/£, June 2026. *Applied: SA, TI.*
* **R7 — Latency ladder.** ML scoring P99 <200 ms; retrieval <100 ms; full conversational query typically 5–10 s, SLA <15 s; API synchronous SLA <10 s. The "one to two seconds" worked-scenario claim and the <3 s full-flow target removed. *Applied: BA.*
* **R8 — Performance targets.** Banking Architecture use-case table is the single canonical target set. Fraud: ROC-AUC >0.85 is the Phase 1 sign-off gate; 0.90 is the indicative target. Phase 1 gates reference the table verbatim. *Applied: BA, TI.*
* **R9 — Vocabulary purge.** tip records → recommendation and outcome records; tip settlement → outcome-matching (closed-loop feedback) service; min edge threshold → high-risk score threshold; SP-equivalent → rules-engine baseline; ROI → named per-vertical business metric (fraud: precision uplift at fixed alert budget; compliance: breach-class recall; RM: rank correlation vs expert rating). *Applied: SA, EB.*
* **R10 — Calibration normalisation.** Sum-to-one (softmax) group normalisation applies only where outcomes within a group are genuinely mutually exclusive. None of the eleven use cases qualifies; calibrated independent probabilities are the deliverable. Blueprint §12 step 5 and Gate G7 corrected. *Applied: EB.*
* **R11 — EU AI Act dates.** High-risk credit-decision obligations restated to the deferred schedule (December 2027, remainder 2028, per the Commission's digital omnibus), caveated "subject to final adoption; verified June 2026". Re-verify at first client use. *Applied: LB.*
* **R12 — Knowledge-base scale.** 60K+ chunks is the Phase 1 (three-collection) basis; deck restated from 120K+ to 60K+. 120K+ may be cited only as labelled nine-vertical target state. *Applied: deck slide 1.*
* **R13 — Document map / sister document.** Engineering Blueprint retitled "Production Engineering Blueprint — ML Pipeline Sister Document"; Banking Architecture's sister-document references now name it. Section 19 added to the Blueprint (per-use-case feature outlines, regulatory corpus ingest strategy, starter-kit licensing review). Document-map paragraph added to every cover. *Applied: BA, EB, all docs.*

## Register-item rulings applied at lockdown

* **SA5 — RAG data classification.** fraud\_knowledge: internal-sensitive; compliance\_knowledge: public regulatory + internal policy; rm\_knowledge: customer data — excluded from all cloud backup paths; on-prem (MinIO) snapshots only.
* **TI4 — MLflow placement.** MLflow runs on-prem (Kubernetes); experiment metadata incl. SHAP artefacts stays in-perimeter; S3 holds anonymised artefact backup only.
* **TI5 — Stripe.** Removed from the bank deployment stack; commercial billing lives in the pricing model (Delivery Plan WS3.4).
* **TI6 — Cognito.** Cognito is a federation broker for the bank's corporate IdP only — not a parallel identity system.
* **TI7 — LLM pinning.** Model family pinned at lockdown: Llama 3.3 70B (advisory), Llama 3.1 8B (output packaging). Re-pin via decision record only.
* **EB8 — Build tracker.** Section 18 tracker retired from the locked document; living copy is BUILD\_TRACKER.md in this repo.
* **DP1/DP3 — Delivery lanes.** Founder-led minimum-viable-path lane is the operative plan; the 4–7 FTE plan is the funded case. Funded-case gating dependencies converted to named actions (regulatory lawyer wk 2, CFO reviewer wk 4, advisory-board shortlist wk 6 of the funded phase). G10 external reviewer recruitment starts immediately.
* **BA8/DP5 — Injection detector.** "Rebuff or equivalent"; selection deferred to build stage B8 (Rebuff is dormant upstream).
* **SA8 — Internet lookup.** duckduckgo-search is best-effort, pilot-only; Serper is the production path.

## Decision-log entries (DEC series)

* **DEC-0000 — Image round deferred (open, narrowed by DEC-0001, extended by DEC-0003; now gates client use).** The four Banking Architecture figures (1.1, 3.1, 4.1, 5.1), new Figure 4.2 (mortgage orchestration flow), and the three Learning Bank figures still carry their pending fixes; the fix lists are preserved inline, each prefixed "Image round deferred per DEC-0000". Must complete before any external/client use of either document. Owner: founder.
* **DEC-0001 — Executive deck rasters enhanced and content-patched (closed, June 2026).** The six embedded diagram PNGs (slides 2–7) were unreadable (dark-on-dark, low contrast) and carried pre-lockdown content. Applied: gamma 0.52 shadow lift + contrast 1.18 + saturation 1.25 on all six; raster text patches for the lockdown rulings — slide 2: "9 INDEPENDENT" → "3 IN PILOT · 9 BY PHASE 2" (R1), 120K → 60K chunks and 3 vector collections (R12), Llama 3.3 70B / 3.1 8B titles (TI7); slide 3: EBA/CBI → PRA/FCA (R6), Llama 3.3/3.1; slide 4: EBA·CBI → PRA·FCA (R6); slide 5: four unescaped "<" entity defects fixed, "Isotonic" → "Platt" (G7 default); slide 7: 3→9 endpoints/collections (R1), 60K chunks (R12), Llama 3.3/3.1 (TI7), MLflow card re-captioned "Runs on-prem per ruling TI4". Known residual source defects (regeneration required, folded into DEC-0000): slide 4 card overlaps (two vertical cards partially hidden); slide 3/5 large empty canvas regions; slide 2 LLM-layer band still themed for the two-model layout. Deck shipped as v2a.
* **DEC-0002 — PwC references scrubbed (closed, June 2026).** Suite-wide audit found a single reference (Banking Architecture Appendix A.3, "the framing PwC colleagues may find useful") — rephrased to firm-neutral wording ("a framing that lands well in client conversations"). All other documents, the deck, and the governance docs were already clean. Banking Architecture bumped v1.0 → v1.0a; sibling document-map lines continue to read v1.0 (content-identical suffix polish).
* **DEC-0003 — Process-orchestration pattern and mortgage worked scenario added (closed, June 2026).** Two independent architecture reviews agreed the document proved the advisory pattern but not the L2 orchestration layer it spends pages describing. Decisions D1–D8 approved as recommended: (D1/D2) new Section 2 subsection "Beyond advisory use cases — process orchestration" names mortgage origination as the canonical orchestration pattern — explicitly NOT a 12th register row (ruling R1 intact: 11/3/9) and NOT Phase 1 scope; flagged as a Phase 2 promotion candidate via future decision record. (D3) New Section 4.2 worked scenario "the mortgage onboarding orchestrator" (10 steps: durable case state, declarative path selection incl. self-employed/high-LTV, document validation, KYC, governed credit scoring, valuation wait, underwriter checkpoint with structured outcome, grounded decision comms, closed-loop outcomes, full audit) with an explicit built-vs-enabled honesty line; former 4.2 renumbered 4.3. (D4) Orchestration-intensity column declined; substance carried in subsection prose. (D5) DEC-0000 image round priority raised — now gates client use; scope extended to include new Figure 4.2 (mortgage flow). (D6) Use-case roadmap one-pager assigned to WS3.1 deck design pass, not a v2a patch. (D7) Covered by D3. (D8) G10 external reviewers’ brief extended to cover document narrative as well as model outputs. Banking Architecture bumped v1.0a → v1.0b.
* **DEC-0004 — Content hash pinned to ns timestamp resolution (closed, June 2026).** Cross-environment verification of the B2 dataset found `profile()`'s content hash is sensitive to pandas major version: pandas 3.x defaults new datetimes to microsecond resolution, so identical data (956,684 rows, all counts matching) hashed `ddd3d45c110c3200` instead of the canonical `6db7d6b191a9c929`. Fix: coerce timestamps to `datetime64\[ns]` inside `profile()` before hashing. No-op on the pinned build environment (pandas 2.x, already ns); regenerating under DVC reproduces the canonical hash unchanged. Reproducibility guarantee restated: seed + config + the hash routine are now version-stable; the DVC-pinned artefact remains authoritative. Verified on Linux/py3.12/pandas 3.0.2 → `6db7d6b191a9c929`.

* **DEC-0005 — Build stage B9.5 (Platform Extraction) inserted (closed, July 2026).** Deviation from the locked Build \& Quality Plan v1.0 (twelve stages B1–B12), authorised by ADR-0009 following the WS-B governance review (unanimous panel). B9.5 sits between B9 and B10: extract the platform-side capabilities per the ADR-0009 boundary table from `verticals/fraud/` into a top-level platform layer; generalise `contracts/` to vertical-neutral. Exit criterion gates B10: a second vertical consumes shared ML lifecycle components rather than copying them (target 80–90% platform reuse; bootstrap-from-primitives test). B10 restated from "replicate the fraud vertical" to "instantiate verticals against the platform template". BUILD\_TRACKER.md carries the row per ruling EB8; the locked docx is unchanged.
* **DEC-0006 — Platform wording rule (closed, July 2026).** Until the B9.5 exit criterion is met, all client-facing and locked-document language describes pipeline-as-platform as "architecturally specified, partially evidenced in the current implementation" — never "the platform exists". Source: WS-B finding F-014 / ruling D-06. Applies at the next revision of each document (CL-17); no retro-edit of locked versions.

## Locked suite (June 2026)

|Document|Locked version|
|-|-|
|The Learning Bank|v2.1|
|Learning Bank Delivery Plan|v1.1|
|Banking Architecture|v1.0b (PwC scrub; orchestration pattern + mortgage scenario)|
|System Architecture|v1.1|
|Technical Infrastructure|v1.1|
|Production Engineering Blueprint — ML Pipeline Sister Document|v1.1|
|Executive Presentation|v2a (diagram readability + raster content patches)|

Companion governance documents: ArcaAI Document Review \& Lockdown Register v1.0 · ArcaAI Build \& Quality Plan v1.0.
Build entry gate: PASSED (Phase 0 steps 0.1–0.4 complete; 0.5 = stand up this repo). Next: build stages B1–B2.



