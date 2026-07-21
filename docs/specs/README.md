> **RETIRED — July 2026 (WS-C governance review).**
> This eight-spec regime was superseded by the June 2026 lockdown before
> any specification was drafted. The canonical specification set is the
> locked document suite registered in /DECISIONS.md (seven locked
> documents, rulings R1-R13, DEC change control). This file and the
> eight section folders below it are retained as a tombstone so stale
> links fail loudly rather than silently. Do not draft against this
> structure. See DEC-0007.

---
# Specifications

The eight canonical specifications that constitute the ArcaAI platform blueprint.

Every specification:

- Follows `_template.md`
- Is owned by a named individual
- Has its own semantic version (independent of other specs)
- Goes through three SME review rounds before reaching v1.0
- Is included in Implementation Pack releases at its current ratified version

## The eight specifications

| # | Specification | Audience weight (Bank / Eng) | Owner | Version | Status |
|---|---|---|---|---|---|
| 1 | [Product Definition](01-product-definition/) | High / Low | Mike | 0.0 | Not started |
| 2 | [Solution Architecture](02-solution-architecture/) | High / Medium | Mike | 0.0 | Not started |
| 3 | [Technical Architecture](03-technical-architecture/) | Medium / High | Mike | 0.0 | Not started |
| 4 | [Data and ML](04-data-and-ml/) | Medium / High | Mike | 0.0 | Not started |
| 5 | [Security and Compliance](05-security-and-compliance/) | High / Medium | Mike | 0.0 | Not started |
| 6 | [Integration](06-integration/) | High / High | Mike | 0.0 | Not started |
| 7 | [Operations and Support](07-operations-and-support/) | High / High | Mike | 0.0 | Not started |
| 8 | [Test and Validation](08-test-and-validation/) | High / High | Mike | 0.0 | Not started |

## Status definitions

- **Not started** — placeholder only
- **Drafting** — substantive content being written; not yet sent for SME review
- **Round 1 review** — structural review with SME panel in progress
- **Round 2 review** — content review in progress
- **Round 3 review** — adversarial review in progress
- **Ratified** — version 1.0 reached; in maintenance only
- **Maintenance** — versioned changes against a ratified base; major changes go through RFC

## Versioning

Each spec has its own version, advanced independently:

- **0.x** — draft, not yet ratified. Patch number increments on each meaningful revision.
- **1.0** — first ratified version (all three SME rounds complete; Mike accepts).
- **1.x** — additive change post-ratification; no breaking changes to bank-side commitments.
- **2.0** — breaking change. Re-ratification required.

## Cross-specification dependencies

The specifications are not independent. Each specification names its **sister specifications** in Section 4 of its own document — sisters are the other specs that together constitute the full blueprint for that subject area. Sister relationships are bidirectional: if Spec A lists Spec B as a sister, Spec B must list Spec A.

The sister graph will be populated as each spec is drafted. Anticipated key relationships:

- All specs are sisters of **Product Definition** (positioning language anchors all)
- **Technical Architecture** and **Solution Architecture** are sisters (one names components, the other says what they're built with)
- **Integration**, **Operations and Support**, and **Test and Validation** are sisters of **Solution Architecture** and **Technical Architecture**
- **Security and Compliance** is a sister of every other spec (cross-cutting)
- **Data and ML** is a sister of **Security and Compliance**, **Integration**, **Operations and Support**, and **Test and Validation**

The full sister graph is produced as specs are drafted. Bidirectional integrity is verified at every review round.

## Authoring discipline

- All specs use the same template structure
- Diagrams are committed as source (Mermaid/PlantUML) in `/diagrams/`, never as images here
- Terms defined in `/glossary/` are referenced, not redefined
- ADRs that affect a spec are cross-referenced explicitly by number
- The two-tier reading model (bank-side summary + engineering detail with `[DETAIL]` markers) is required
