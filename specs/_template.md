# [Spec Name] Specification

**Spec number:** NN of 08
**Version:** 0.1 (draft)
**Status:** Drafting | Round 1 review | Round 2 review | Round 3 review | Ratified | Maintenance
**Owner:** [Name]
**Last updated:** YYYY-MM-DD
**Implementation Pack version:** [included in pack-vX.Y.Z]

---

## Two-tier reading guide

This specification serves two audiences in the same document.

**Bank-side reviewers** (CTO, CDAO, Model Risk, InfoSec, Procurement) — read sections 1-4 and 9-10 for full understanding. Skim 6-8 for context. See section 4 (Sister specifications) for what to read alongside this document.

**Engineering** — read all sections. Section 6 onwards is where implementation-critical detail lives.

Throughout the document, **summary tier** content uses plain prose. **Detail tier** content is signposted with the marker `[DETAIL]` at the start of paragraphs or sub-sections — engineering reads these; bank-side reviewers may skip them.

---

## 1. Purpose

What this specification is for. What question it answers. Why it exists.

One paragraph, maximum two. The reader should know after this section whether to read on.

## 2. Scope

### In scope

What this specification covers. List the major topics, components, or concerns addressed.

### Out of scope

What this specification deliberately does not cover, and where the reader should look instead. This section is at least as important as the in-scope list — it prevents the spec from being asked to answer questions it was never intended to answer.

## 3. Audience

Who reads this specification, what they read it for, and how they use it.

Differentiate where relevant — bank-side audiences may use the spec for one purpose (procurement assessment, Model Risk evidence), engineering audiences for another (building, integrating, testing).

## 4. Sister specifications

This specification is part of a set. The full blueprint for the subject area is spread across multiple sister documents. **A reader cannot fully understand the subject from this specification alone.**

### What this means

The sister relationship is structural, not editorial. Each sister contains content that this specification depends on, and each sister depends on content this specification contains. Together, the sister set constitutes the full blueprint. The Implementation Pack release packages sisters together when relevant for a given use case.

### Sister set

| Sister | What it covers | What this spec uses from it | What it provides to this spec |
|---|---|---|---|
| [Spec NN — Name] | [The sister's subject in one line] | [What this spec relies on from the sister — e.g. "the named architectural layers"] | [What the sister relies on from this spec — e.g. "the data contract for layer 3"] |
| [Spec NN — Name] | ... | ... | ... |

Every entry in this table must be reciprocated. If this spec lists Spec X as a sister, Spec X must list this spec as a sister. The bidirectional integrity of the sister graph is verified at every spec review round.

### Reading guidance by audience

Bank-side reviewers and engineering audiences need different subsets of the sister set when assessing this subject area.

**For bank-side reviewers** (CTO, CDAO, Model Risk, InfoSec, Procurement) the essential sisters to read alongside this spec are:
- [Spec NN — Name] — [why bank-side reviewers need this sister]
- [Spec NN — Name] — [why bank-side reviewers need this sister]

**For Arca engineering** the essential sisters are:
- [Spec NN — Name] — [why engineering needs this sister]
- [Spec NN — Name] — [why engineering needs this sister]

Other sisters in the table above are relevant when specific questions arise but are not required for general understanding.

## 5. Definitions

Terms used in this specification that are defined in the shared glossary are not redefined here. They are referenced by name.

Terms specific to this specification that are *not* in the shared glossary may be defined here. If a definition turns out to be needed across multiple specs, it migrates to the glossary in a follow-up PR.

## 6. Specification

This is the body of the document. Its structure is determined by what is being specified — there is no universal sub-structure for this section. However, all eight specifications use the following organising principles:

- **Statements are testable** — wherever possible, a claim is phrased such that it can be evaluated as met or not met
- **Diagrams are referenced**, not embedded inline. Diagram source files live in `/diagrams/` and are rendered at release time. The specification references them by filename and figure number.
- **Cross-references to other specs are explicit** — "see Integration Specification §4.2" not "see the integration spec somewhere"
- **Cross-references to ADRs use the ADR number** — "this follows from ADR-0003" not "this follows from a decision we made"

## 7. Open questions

Questions known to be unresolved at the current version of the specification.

Each open question has:
- A clear statement of the question
- Why it is open
- What the impact is of leaving it open
- A target resolution date or trigger condition

Open questions are not flaws — they are honest acknowledgements that the specification is not yet complete. They become RFCs or ADRs when resolved.

## 8. Validation criteria

How do we know this specification is good?

For each criterion:
- A specific, observable indicator
- A threshold or target value

Validation criteria are used by the SME panel during review and by Mike when deciding whether to accept a version 1.0 release.

## 9. Decisions made

ADRs that bear on this specification, listed with cross-references.

| ADR | Title | How it affects this spec |
|---|---|---|

## 10. Revision history

| Version | Date | Author | Summary of changes |
|---|---|---|---|
| 0.1 | YYYY-MM-DD | [Name] | Initial draft |

## 11. SME review record

Reviews are committed to this spec's `reviews/` folder. This section indexes them.

| Round | SMEs | Submitted | Verdict | Reconciliation |
|---|---|---|---|---|

---

## Notes for authors

- This template is the single shape all eight canonical specifications follow. Deviation from this structure requires an RFC.
- The two-tier reading model (bank-side summary + engineering detail) is fundamental — don't lose it in production.
- **Section 4 (Sister specifications) is the structural backbone of the specification set.** Every entry in the sister table must be reciprocated by the named sister. The bidirectional integrity of the sister graph is checked at every review round — if Spec A lists Spec B as a sister, Spec B must list Spec A. This is what makes the eight specifications a coherent set rather than eight separate documents.
- Diagrams as source files (not images embedded in this Markdown). Reference by filename.
- Open questions are encouraged in early drafts; they should reduce as the spec matures.
- The spec is finished when validation criteria are met, not when it "feels done."
