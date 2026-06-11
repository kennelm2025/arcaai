# Spec 01 — Product Definition — Working Brief

**Status:** Working brief v0.2, pre-draft. Produced 2026-05-13.
**Purpose:** Stage the structural decisions, harvest map, and rationalisation calls for Spec 01 before drafting. The brief is robust to whatever shape `specs/_template.md` turns out to require; the prose isn't.
**Next session:** Upload `specs/_template.md`, draft Spec 01 against this brief.
**v0.2 changes:** Added working tagline candidate to §3; added §6d (position against consulting/services as a fourth category); added §7e (tiered read strategy across the Implementation Pack). Source for additions: ChatGPT review of exec deck v12 dated 2026-05-13 — partial uptake, scores/SWOT/commercial-model sections rejected as out-of-scope or insufficiently grounded.

---

## 1. What Spec 01 is — and is not

Spec 01 is the **bank's first read**. It is the document a Bank CTO, CDO, Head of Model Risk, or AI Governance lead opens to answer the question *"what is ArcaAI, who is it for, and what would it do for us?"* — and forms an independent view from before sales engagement begins.

It is **not** the architecture document. It is not the implementation document. It does not contain stack choices, deployment topology, or training methodology. It contains:

- What ArcaAI is, conceptually and commercially
- Who it is for — the named audience(s) and the named use cases
- What it delivers — outcomes, productivity uplifts, deployment timeline expectations
- The three foundational positions (reference models, three-stage lifecycle, pipeline-as-platform) expressed in language the bank reads, not engineering language
- The boundary with the other seven specs — what each sister spec covers

Architectural detail, technical stack, MLOps internals, security controls, and integration mechanics all sit in Spec 02 onwards. Spec 01's job is to make a non-engineer bank reader **want to read Spec 02**.

## 2. Audience tiering

Per START_HERE.md, bank-side reviewers read each spec at **summary tier**; engineering reads end-to-end including `[DETAIL]` content. Spec 01 is dominated by summary-tier content because its primary audience is bank-side.

Three named bank-side reader segments for Spec 01:

| Reader | What they want from Spec 01 |
|---|---|
| **Bank CEO / Executive Sponsor** | The first two paragraphs. The board-level proposition. |
| **Bank CTO / CDAO** | The five-layer concept in one diagram, the eleven use cases in one table, the data sovereignty position |
| **Bank Head of Model Risk / AI Governance** | The three-stage lifecycle, the reference-vs-production-model distinction, the regulatory mapping (which is in Spec 05, but Spec 01 must point clearly at it) |

Engineering audience for Spec 01 is **secondary** — engineers will mostly skip Spec 01 and go to Spec 02 onwards. Spec 01 still needs to be correct for engineering, but it does not need to teach engineering anything.

## 3. The Spec 01 / Spec 02 boundary

This is the most important call in the brief because Banking Architecture v0.4 collapses the two.

| In Spec 01 | In Spec 02 |
|---|---|
| What ArcaAI **is** | How ArcaAI **works** |
| The five layers **named**, with a one-paragraph role each | The five layers **specified**, with components, interfaces, data flows |
| The eleven use cases **listed**, with target uplifts and time-to-production | Each use case as a **vertical pattern** with ML + RAG + LLM components |
| The three forms of AI (ML, agents, LLMs) **defined commercially** | The three forms specified architecturally — what each component is, how they integrate |
| The Control Plane **named as a defence-in-depth feature** | The Control Plane **specified** — Presidio, Rebuff, OPA, output grounding |
| Pipeline-as-platform **named as the product** | The pipeline **specified** — Reference / Upskilling / Continuous Improvement, gates, registry |
| Data sovereignty **as a commitment** | Data sovereignty **as enforced controls and deployment topology** |

**Test for boundary calls:** if a bank exec reading Spec 01 would skip the paragraph as "too technical," it belongs in Spec 02. If a bank exec reading Spec 02 would skip the paragraph as "marketing," it belongs in Spec 01.

**Working single-sentence proposition for §2 executive summary.** Test the following framing against Banking Architecture v0.4 and the exec deck v12 at draft time: *"ArcaAI is the sovereign AI intelligence layer that enables banks to build, govern, and scale AI across every core business process."* This is sharper than the current "hybrid ML and AI platform for UK banks" framing and lifts the platform out of the "another banking AI tool" category without overclaiming. Source: ChatGPT review of exec deck v12, 2026-05-13. Not yet adopted; subject to drafting test.

## 4. Inferred section roadmap

This is my best guess at Spec 01's section list, pending the template. Section numbering is illustrative; the template defines the canonical eleven sections.

| Section | Content | Length |
|---|---|---|
| **1. Purpose and audience** | Who Spec 01 is for, what they get from reading it | ½ page |
| **2. Executive summary** | The platform on one page — for the CEO/sponsor read | 1 page |
| **3. What ArcaAI is** | Hybrid AI (ML + agents + LLMs), in-house, wraps the bank's existing systems. The three forms of AI, defined. The conceptual frame. | 2 pages |
| **4. Sister specifications** | The bidirectional sister table — which other specs together complete the picture | 1 page (table) |
| **5. What ArcaAI delivers** | The eleven use cases. Target uplifts. Time-to-first-production. Adoption pattern (use case by use case, each funds the next). | 3 pages |
| **6. Who ArcaAI is for** | Target market segment — and this is where ADR-0004 gates Spec 01. | 1-2 pages |
| **7. The three foundational positions** | (a) Reference models, not production models; (b) Three-stage lifecycle; (c) Pipeline-as-platform. Each expressed in bank-reader language with a one-line link to the ADR. | 2 pages |
| **8. The five layers, named** | A one-diagram-and-one-paragraph treatment of the five layers. Detail in Spec 02. | 1 page |
| **9. How ArcaAI is sold and delivered** | Describer Pack → Banking Demo → Implementation Toolkit. First production model in 6-8 weeks. | 1 page |
| **10. What ArcaAI is not** | An honest demarcation: not a frontier LLM provider, not a vendor AI-inside replacement, not a core banking system. Pre-empts confusion. | 1 page |
| **11. Definitions and references** | Pointer to glossary; pointer to the three ADRs; pointer to sister specs. | ½ page |

**Estimated length:** 14-16 pages. That is long for Spec 01 but appropriate — this is the document the bank reads first and most carefully.

## 5. Harvest map — what comes from where

The Spec 01 draft is built by harvesting from these sources:

### Primary — almost lift-and-shift
- **Exec deck slide 1** — the five-point opening (Sovereignty, Agent-First, Auditable, Extensible, Bank-Owned) → Spec 01 §2 executive summary
- **Exec deck slide 3** — "Why ArcaAI" six reasons → Spec 01 §3 and §6
- **Banking Architecture v0.4 §1.1** (What we mean by hybrid AI) → Spec 01 §3
- **Banking Architecture v0.4 §1.4 — the ten principles** → adapted into Spec 01 §3 and §7 (with reduction; 10 is too many for Spec 01 — needs trimming to the 5-6 that earn the space)
- **Banking Architecture v0.4 §2 — the eleven use cases table** → Spec 01 §5, lifted near-verbatim (this is gold)

### Secondary — reframed
- **Exec deck slide 5** (Platform Architecture, five layers) → Spec 01 §8, simplified to one diagram + one paragraph per layer, full treatment deferred to Spec 02
- **Exec deck slide 18** (Where ArcaAI Sits in the Market) → Spec 01 §10 (What ArcaAI is not / market position)
- **Exec deck slide 20** (Three Arca-built assets) → Spec 01 §9 (How ArcaAI is sold and delivered)
- **Exec deck slide 11** (Nine ML Engines) → reconciled with Banking Architecture v0.4's eleven use cases. **Open question:** is it 9 or 11? Banking Arch v0.4 lists 11; exec deck lists 9. They are not the same set. To resolve before drafting §5. See §7 below.

### Tertiary — supplied by ADRs
- **ADR-0001** → Spec 01 §7(a), reference models language, sharpened beyond "starter kit"
- **ADR-0002** → Spec 01 §7(b), three-stage lifecycle named and explained briefly
- **ADR-0003** → Spec 01 §7(c), pipeline-as-platform positioned

### What does NOT get harvested
- **System Architecture v1.0** — nothing useful for Spec 01. Confirmed.
- **Grok audit** — not an audit; an unsolicited v0.3 rewrite that pre-dates v0.4. Set aside.
- **ML Pipeline / Engineering Blueprint / Technical Infrastructure** — these are Spec 03/04 sources, not Spec 01.

## 6. The three places Spec 01 must actively do new work

Most of Spec 01 is harvest. These three areas are not — they require Spec 01 to advance the framing beyond what the legacy docs offer.

### 6a. Sharpen ADR-0001's language

Banking Architecture v0.4 says: *"pre-trained foundation models sourced from open-weight publishers... pulled once into the bank's controlled environment, and then extended by the bank through the controlled training pipeline. The base is inherited. The specialisation is the bank's."*

This is on the path to ADR-0001 but conflates two distinct things:

- **Open-weight LLMs** (Llama 3, Mistral) — pulled once, pinned, used as the language layer. These are inherited as-is; the bank does not retrain them.
- **Predictive ML models** (XGBoost, LightGBM fraud/credit/RM classifiers) — Arca ships reference models trained on representative public + synthetic banking data. The bank upskills them on its own data. These are explicitly **not production-ready** out of the box.

ADR-0001 is about the second category. Spec 01 must make this distinction visible without descending into the technical specifics that belong in Spec 04 Data & ML. The right language is something like: *"Arca ships two kinds of pre-trained model. The open-weight language models — Llama 3 and similar — are inherited as-is and used to generate narrative. The predictive models — the fraud, credit, compliance, and RM classifiers — are reference models, trained on representative public and synthetic banking data to demonstrate the architecture. They are not production-ready as shipped. The bank upskills them on its own operational data through Arca's controlled pipeline before any production deployment."*

### 6b. Introduce the three-stage lifecycle in bank-reader language

ADR-0002 establishes Reference → Upskilling → Continuous Improvement. The legacy docs have the pieces (especially Banking Architecture v0.4 principle #4, "A bank that gets smarter over time") but don't name the three stages.

Spec 01 needs a single paragraph (and ideally a single small diagram) that names the three stages, says who owns each, and what happens at each. The detail belongs in Spec 04. Spec 01's job is to plant the three stages so that the rest of the spec set can refer to them.

### 6c. Position pipeline-as-platform — not models-as-artefacts

ADR-0003 is the hardest of the three to land in bank-reader language because it is fundamentally a positioning move *against* a more obvious alternative. Banks know how to buy models. They know how to buy platforms. Pipeline-as-platform is neither — and it has implications for how the bank thinks about ownership, MLOps integration, and what it is actually procuring.

Spec 01 must make this position explicit, because every part of the rest of the spec set (especially Specs 04 and 07) depends on it. The right framing — provisional — is something like: *"What the bank adopts is not a set of pre-trained models that it bolts into its existing MLOps. What the bank adopts is Arca's upskilling pipeline as the operating environment for the verticals ArcaAI covers. The models are the most visible deliverable; the pipeline is the actual product."*

This is the one piece of Spec 01 most likely to draw bank pushback (*"why can't we just take the models?"*) — so Spec 01 must answer the implicit objection rather than just assert the position.

### 6d. Position against four categories, not three

The exec deck slide 18 positions ArcaAI against three categories: Hyperscaler AI (sovereignty trade-off), Specialist & Core-Banking AI (breadth trade-off), and Enterprise Agents (banking-grade trade-off). This is good but incomplete.

A fourth category will come up in every bank conversation: **consulting and services firms** — the Big Four, Accenture, Capgemini and their banking AI practices. Banks evaluating an in-house AI capability will inevitably compare ArcaAI to "let our existing advisor build this for us." Spec 01 should pre-empt this comparison rather than ignore it.

The position is roughly: *"ArcaAI is not a consulting proposition. It is a productised platform with implementation assets. Where a consultancy sells advisory hours and project delivery, ArcaAI ships a self-hostable platform, a controlled training pipeline, reference models, and a validation harness. Consultancies can deploy ArcaAI — many will — but the platform itself is not a services engagement."*

This sharpens what ArcaAI **is** (a platform-centric proposition with consulting-enabled delivery) and what it **is not** (a consulting engagement with platform assets). Lands in §10 (What ArcaAI is not).

## 7. Open questions to resolve before drafting

### 7a. ADR-0004 (Target Market Segment) — gates Section 6

Spec 01 §6 ("Who ArcaAI is for") cannot be written without ADR-0004. Banking Architecture v0.4 says "UK banks." The exec deck broadens to "UK and European banks." PROJECT_CONTEXT.md says "UK and European banks." These are not the same proposition. UK alone is one regulatory frame (PRA, FCA, BoE) and one supervisory culture. UK + EU adds DORA, EU AI Act, NIS2, national supervisors. Material difference for Spec 05 and for how aggressive Spec 01's regulatory claims can be.

SESSION_NOTES deferred ADR-0004 to Month 2. We're at Month 1, Week 1. Two options:
- Draft Spec 01 to a working assumption ("UK + Ireland as initial focus, EU follow") and explicitly flag §6 as provisional pending ADR-0004
- Bring ADR-0004 forward and resolve it before Spec 01 drafts §6

**Recommendation:** the first option. Spec 01 can be 80% drafted without ADR-0004; the §6 work is contained.

### 7b. Nine use cases or eleven?

| Source | Count | List |
|---|---|---|
| Exec deck slide 11 | 9 | Fraud, Compliance, RM Support, Credit Risk, Payments, Retail Lifecycle, Customer Mgmt, Customer Insight, Investment |
| Banking Architecture v0.4 §2 | 11 | The 9 above + Model Risk Management/Validation + Regulatory Reporting Narrative |
| PROJECT_CONTEXT.md | "eleven" | not enumerated |

The eleven version is more recent and more useful — Model Risk Management is a *strong* use case to put in front of a CRO/CDAO, and Regulatory Reporting Narrative is the most credible RAG showcase. The exec deck slide 11 needs updating, not the other way around.

**Recommendation:** Spec 01 lists eleven. Flag for the next exec deck rev.

### 7c. Reduce the ten principles to how many?

Banking Architecture v0.4 §1.4 has ten principles in three tiers. That's a lot for Spec 01. Suggestions:
- Tier 1 (Universal): five principles → keep all five, they are the platform's selling proposition
- Tier 2 (Control & sovereignty): two principles → keep both
- Tier 3 (Fit for purpose): three principles → consider compressing to two

But this is a judgment call that depends on how Spec 01 reads in draft, not a decision to take now. Note the tension; revisit at draft time.

### 7d. Where does "what ArcaAI is not" sit?

Two options:
- §10 standalone section ("What ArcaAI is not") — explicit, slightly defensive
- Folded into §3 or §6 — softer

**Recommendation:** standalone. Banking buyers respect the demarcation; it pre-empts a difficult conversation later.

### 7e. Tiered read strategy across the Implementation Pack

A review of the exec deck (ChatGPT, 2026-05-13) flagged that a single executive presentation tries to serve three different reader contexts: a 5-minute board read, a 30-minute CIO/CDO/CRO read, and a multi-hour architectural due-diligence read. These are different documents with different purposes.

The Implementation Pack already accommodates this structurally — the Describer Pack is the executive read, the eight canonical specs are the technical read. But a 5-slide **Board Deck** (separate from the current ~24-slide executive deck v12) is plausibly missing.

This is **not a Spec 01 question** — Spec 01 is itself the deepest technical-tier document, not the board read. But it is a question for the Describer Pack workstream. Flag for RFC if/when the Describer Pack is scoped. Spec 01 §9 (How ArcaAI is sold and delivered) should mention the tiered read pattern when describing the Describer Pack, even if the Board Deck doesn't yet exist.

## 8. Sister specifications — preliminary list for Spec 01

Per the section 4 discipline (bidirectional), Spec 01 names the following sisters, and each of those specs must list Spec 01 back:

| Sister | Why Spec 01 needs it |
|---|---|
| **Spec 02 — Solution Architecture** | Spec 01 names the five layers; Spec 02 specifies them |
| **Spec 04 — Data and ML** | Spec 01 names the three-stage lifecycle; Spec 04 specifies it |
| **Spec 05 — Security and Compliance** | Spec 01 makes regulatory claims; Spec 05 evidences them |
| **Spec 06 — Integration** | Spec 01 says "wraps around the bank's existing systems"; Spec 06 specifies how |
| **Spec 08 — Test and Validation** | Spec 01 cites productivity uplifts as outcomes; Spec 08 specifies how they are measured and validated |

Spec 03 (Technical) and Spec 07 (Operations) are *not* immediate sisters of Spec 01 — they are downstream of Spec 02 and Spec 04 respectively. Spec 01 readers do not go directly to them.

## 9. Definition of done for this brief

This brief is complete enough to support drafting when next session can answer YES to all of these:

- [ ] `specs/_template.md` is available
- [ ] The Spec 01 / Spec 02 boundary in §3 of this brief is confirmed or amended by Mike
- [ ] The 11 use cases (not 9) is confirmed
- [ ] The §6 ADR-0004 working assumption is confirmed (UK + Ireland focus, EU follow)
- [ ] The three "active work" pieces in §6 of this brief — sharpen ADR-0001 language, three-stage lifecycle, pipeline-as-platform — are read by Mike and confirmed as the right places to push beyond the legacy

## 10. Estimated drafting effort once unblocked

| Section | Effort (with template in hand) |
|---|---|
| §1 Purpose and audience | 15 min |
| §2 Executive summary | 30 min |
| §3 What ArcaAI is | 60 min |
| §4 Sister specifications | 15 min (table) |
| §5 What ArcaAI delivers | 45 min (lift-and-edit from Banking Arch v0.4 §2) |
| §6 Who ArcaAI is for | 45 min + ADR-0004 dependency |
| §7 Three foundational positions | 60 min (the active work) |
| §8 Five layers, named | 30 min |
| §9 How ArcaAI is sold and delivered | 30 min |
| §10 What ArcaAI is not | 30 min |
| §11 Definitions and references | 15 min |
| Total | ~6 hours of focused drafting |

That is roughly **two full daily sessions** (3 hours each) to a v0.1 ready for SME panel Round 1 (structural review). Realistic given the brief and the harvest map.
