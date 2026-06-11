# Grok Image Regeneration Brief
## ArcaAI Banking Architecture — Image round

Good morning. This file is a precise set of image regeneration requests for the ArcaAI Banking Architecture v0.4 document. Please regenerate the images below with the specific fixes noted. Keep the existing visual style, colour palette (Banking Blue #003087 + Intellith Teal #00C4B4), layout, and the ArcaAI logo placement consistent across all images.

---

## FIXES TO EXISTING IMAGES

### Image 1 — Five-Layer Application Architecture (vertical stack, numbered 1-5)
**Current state:** good, nearly ready to use.
**Fix needed:**
- Near the top of the image, the text "ArcaAl" appears with a lowercase L where a capital I should be. Correct to **"ArcaAI"**.

Everything else about this image is fine. Keep the vertical five-layer stack, the blue-to-teal-to-green colour gradient, the one-line descriptions under each layer name, and the "ArcaAI adds Layers 2, 3 and 4 on top of the bank's existing systems" subtitle.

---

### Image 2 — MLOps Y-Model Delivery Lifecycle (two-track Y diagram)
**Current state:** good structure, needs one terminology update.
**Fix needed:**
- Change the convergence box label from **"Deployment Release Management"** to **"Controlled Deployment"**. This matches the updated v0.4 terminology.

**Nice-to-have:**
- Add a small label on the feedback arrows at the bottom (the arrows going from the monitoring boxes back up) showing **"Retraining trigger"** — so the feedback loop's purpose is clearer to the reader.

Everything else stays: two parallel tracks (Data Science & ML Track on left in blue, Software Delivery Track on right in green), the Y-shape converging at the controlled deployment box, the tool logos at the top (MLflow, DVC, Feast, Evidently AI), the Production Runtime box below, and the four monitoring outputs (Feature drift / Prediction drift / Retrieval quality / Retraining).

---

### Image 3 — End-to-End Query Flow (ten-step horizontal flow)
**Current state:** good concept, multiple text typos and a structural duplication to fix.

**Typo fixes:**
- Title: **"Ard-to End-to-End Query Flow"** → **"End-to-End Query Flow"** (the "Ard-to" prefix is spurious)
- Step 4 label: **"Agentic Orchetay"** → **"Agentic Orchestration"**
- Step label referencing LangGraph: **"classifies & & routes"** (has double ampersand) → **"classifies & routes"**
- Review all step labels for similar rendering artefacts.

**Structural fix:**
- The current image shows **"5. AI Guardrails"** and **"5. AI Guardrails check"** both labelled as step 5, which is a duplication error.
- The correct flow has **two distinct guardrails steps** at different positions:
  - **Step 3 — Inbound guardrails** (before the agent processes the query — PII scrub + injection defence)
  - **Step 8 — Outbound guardrails** (after the intelligence layer produces a response — response validation + grounding check)

The full correct ten-step flow is:
1. Query arrives (L1 — Chat UI or API)
2. Auth & gateway
3. Inbound guardrails (L3 — PII scrub + injection defence)
4. Agentic orchestration (L2 — LangGraph classifies & routes)
5. ML prediction (L4)
6. Knowledge retrieval (L4 — RAG)
7. LLM narrative generation (L4)
8. Outbound guardrails (L3 — response validation + grounding check)
9. Immutable audit log written
10. Response delivered to L1 with citations, SHAP, and human override option

The subtitle "Deterministic, auditable, human-in-the-loop path — No data leaves the bank" is excellent. Keep it.

---

### Image 4 — Hybrid AI Three Forms Venn diagram
**Current state:** good concept, needs text cleanup on one circle.

**Fixes:**
- In the Large Language Models circle (right side), the text currently reads **"OPA & OPA"** — this is a rendering error and incorrect anyway (OPA belongs in the agentic orchestration circle, not the LLM circle).
  - Remove **"OPA & OPA"**.
  - Replace with: **"RAG grounding"** and **"Narrative generation"** — these are what the LLM actually does.
- Near the top-left of the Machine Learning circle, the floating text **"Banking Blue"** appears. This is a colour palette label that has leaked onto the diagram. **Remove it entirely.**

The three circles (Machine Learning / Agentic Orchestration / Large Language Models) and their overlap showing "Hybrid Intelligence" are conceptually perfect. The caption at the bottom — "ML provides precision → Agent orchestrates → LLM communicates — All grounded in the bank's own data" — is excellent and should stay.

---

### Image 6 — High-Level Enterprise Architecture (detailed five-layer view)
**Current state:** good detailed layered view showing all product names, needs multiple text fixes.

**Typo fixes in the Layer 2 (Agentic Orchestration) boxes:**
- **"queves"** → **"queries"**
- **"invokes oses"** → **"invokes tools"**
- **"enforces oses policies"** → **"enforces policies"**
- The garbled sentence **"Selects use cases invokes oses"** should read **"Selects use cases, invokes tools, enforces policies"**

**Typo fix in the Layer 5 (Enterprise Services) box:**
- **"Warehouste"** → **"Warehouse"**

**Label fix in the Layer 3 (AI Guardrails) row:**
- One of the boxes currently just says **"Response"** — this appears truncated. It should read **"Response Validation"**.

Everything else about this image is correct and well-structured. Keep all the product names (React Chat UI, FastAPI, React Native Mobile, LangGraph, XGBoost/LightGBM + BentoML, ChromaDB/OpenSearch, Llama 3 70B, Core Banking, CRM, Payments, Data Warehouse), the colour-banded five-layer structure, the right-side vertical axis showing "Query → Orchestration → Guardrails → Intelligence → Response + Audit", and the bottom tagline "Hybrid ML + RAG + Agentic AI — Full data sovereignty — No data leaves the bank".

---

## NEW IMAGES REQUESTED

### Image 7 — Data Sovereignty Perimeter (NEW)
**Purpose:** A visual representation of the core principle that no bank data leaves the bank's perimeter. This is currently explained only in prose; a diagram would make it instantly clear.

**Suggested composition:**
- A large rectangular boundary box labelled **"Bank's perimeter"** taking up most of the image.
- **Inside the perimeter** (arranged as labelled components): Customer data, Transaction data, ML models, Prompts, Vector database, ML inference, LLM serving, Feature store, Audit trail, Labels and case outcomes.
- **Outside the perimeter**: Empty space labelled "(nothing sensitive leaves)".
- **External model registry** (HuggingFace logo or generic "open-weight model registry") shown as a box outside the perimeter, with a **one-way arrow pointing INTO the perimeter** labelled **"Models pulled once, signed, scanned, pinned. Never phones home. No auto-updates."**
- **Optional internet lookup** shown as a **dashed line** going OUT from the perimeter to an "External domains (whitelisted)" box, labelled **"Opt-in only: PII-scrubbed, domain whitelisted, audit-logged"**.

**Style:** use the same Banking Blue + Intellith Teal palette as the other images. Keep it clean and architectural rather than busy.

**Intended placement:** between Section 1.1 and Section 1.2, or as a sidebar in Section 6 (Securing the AI and ML components).

---

### Image 8 — Three-Tier Principles Pyramid (NEW, nice-to-have)
**Purpose:** Visual summary of the ten core principles grouped into three tiers. Currently the reader works through 10 principle blocks in text; a pyramid visual would give them the architecture at a glance.

**Suggested composition:**
- A three-tier stacked horizontal-band diagram (or pyramid if it reads better visually).
- **Tier 1 (base band, widest) — "Universal guiding principles"** — list the 5 principles beneath the banner:
  1. Deepen every customer relationship
  2. Productivity uplift, use case by use case
  3. Sharper customer intelligence
  4. A bank that gets smarter over time
  5. Wraps around the bank's strategy and operating model — AI to the bank's data
- **Tier 2 (middle band) — "Control and sovereignty"** — list the 2 principles:
  6. The bank is always in control
  7. No bank intelligence leaks out, no unknown intelligence leaks in
- **Tier 3 (top band) — "Fit for purpose and responsible operation"** — list the 3 principles:
  8. Active guardrails and always-on monitoring
  9. Fit for purpose — in-house, open source, secured supply chain
  10. Channel-consistent consumption

**Style:** use the tier-banner colours already in the document: Tier 1 in teal, Tier 2 in blue, Tier 3 in amber.

**Intended placement:** Section 1.4, as the opening visual before the written principle blocks.

---

### HOLD FOR LATER (ML Pipeline document, not this doc)

### Image 5 — Data Journey (already exists, one fix needed when we get there)
This image is excellent but belongs in the sister ML Pipeline document, not in the Banking Architecture doc. When we build the ML Pipeline document, apply this fix:
- **"MLOps Traiectations"** → **"MLOps Stages"** or **"MLOps Pipeline"** (the current word is not a real word)

Everything else about this image is correct and ready to use.

---

## STYLE CONSISTENCY NOTES FOR ALL IMAGES

- **Primary colours:** Banking Blue #003087 and Intellith Teal #00C4B4
- **Logo placement:** the ArcaAI wordmark-with-brain-icon logo appears on Images 1, 4, 5, and 6. Keep this consistent.
- **Typography:** clean, corporate, no handwritten or overly-decorative fonts
- **Background:** dark (Images 4, 6) or clean light (Images 1, 2, 3, 5) — use whichever matches the image's existing treatment
- **No text typos:** this is the critical one. A bank CTO will notice typos and it will undermine the document's credibility. Please review every label carefully before delivery.

---

## DELIVERY

Please return all six regenerated/new images as individual PNG or JPG files. We'll embed them into the v0.5 build once they're in.

Thank you.
