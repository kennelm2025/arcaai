# Review Protocols

This document defines the three-round SME review process that every canonical specification passes through before ratification.

## The three rounds

### Round 1 — Structural review

**Question to reviewers:** *Does the structure of this specification make sense? What's missing at the framework level? What's wrong about the way the specification is organised?*

**Focus:** Macro-level. Is the spec answering the right questions? Are the major sections present and in the right order? Are claims at the right level of abstraction? Is anything fundamentally misframed?

**Reviewers:** Grok (primary), DeepSeek, ChatGPT, Mistral (if regulatory content present), Mike

**Duration:** 3-4 days wall-clock

**Output:** Each reviewer submits structured critique. Mike adjudicates. Agreed changes implemented in PR.

### Round 2 — Content review

**Question to reviewers:** *Now that the structure is right, is the content correct, complete, and consistent with the other specifications?*

**Focus:** Specific claims, technical correctness, completeness within each section, consistency with related specs.

**Reviewers:** DeepSeek (primary), ChatGPT, Mistral (regulatory content), NotebookLM (cross-spec consistency with all in-flight specs loaded), Mike

**Duration:** 3-4 days wall-clock

**Output:** Each reviewer submits structured critique. Mike adjudicates. Agreed changes implemented in PR.

### Round 3 — Adversarial review

**Question to reviewers:** *Find what is wrong. Find what a real bank reviewer would push back on. Find what a regulator would query. Find the parts that look fine but are not.*

**Focus:** Stress-testing. Reviewers are explicitly asked to be hostile, skeptical, contrarian.

**Reviewers:** Claude (clean session, fresh eyes), Grok (as "skeptical Director of InfoSec"), ChatGPT (as "hostile Model Risk reviewer"), Mistral (final regulatory sign-off), Mike

**Duration:** 3-4 days wall-clock

**Output:** Each reviewer submits adversarial critique. Mike adjudicates. Agreed changes implemented. Mike then decides whether to accept the specification as v1.0.

## The submission package

Each round, the SME panel receives a **submission package** containing:

1. **The current state of the specification** — markdown source from the repository at a specific commit
2. **The prompt primer for that SME** — from `sme-prompt-primers/`
3. **A round-specific framing message** — what round this is, what to focus on
4. **Relevant ADRs** — at minimum 0001, 0002, 0003; plus any others bearing on this spec
5. **The Project Context document** — `PROJECT_CONTEXT.md`
6. **Cross-references** — any other specs the reviewer needs to see (in Round 2, this includes all in-flight specs for the cross-consistency check)

The submission package is assembled by Mike (or by Claude on Mike's behalf) and packaged as a single message to paste into the SME's interface.

## Capturing review outputs

Each SME's critique is committed to the repository under the specification's folder:

```
specs/04-data-and-ml/
├── README.md
├── data-and-ml.md          # The specification itself
└── reviews/
    ├── round-1-deepseek.md
    ├── round-1-chatgpt.md
    ├── round-1-grok.md
    ├── round-1-mistral.md
    ├── round-1-reconciliation.md
    ├── round-2-...
    └── round-3-...
```

**Reviews are not deleted after the round closes.** They are part of the audit trail.

## The reconciliation document

After each round, Mike (with Claude's help) produces a **reconciliation document** that:

1. Lists every distinct point raised across all reviewers
2. States Mike's verdict on each (Accept, Reject, Modify, Defer)
3. Notes the rationale for each verdict, especially for rejections
4. Lists the changes that will be made to the specification as a result

The reconciliation is committed alongside the reviews. It is the record of decisions made under each review round.

## When a round fails

A round "fails" when:

- A reviewer surfaces a structural problem that requires the specification to be substantially rewritten
- Multiple reviewers identify the same fundamental issue
- Mike concludes that the specification is not ready to proceed to the next round

When a round fails:

1. The specification stays at its current version
2. A new draft is produced addressing the failure
3. The failed round is **re-run** with the same reviewers — not the next round
4. The fact of the failure is noted in the reconciliation document

A specification can fail a round multiple times. There is no maximum. The discipline is that the spec advances only when ready, not on a schedule.

## Acceptance to v1.0

A specification reaches v1.0 when:

1. All three review rounds have completed successfully
2. The reconciliation documents for each round are complete
3. Mike has reviewed the final specification end-to-end
4. Mike marks the specification as accepted via PR
5. The document register is updated to status `Ratified`
6. The CHANGELOG is updated noting the spec's v1.0

After v1.0, the spec enters maintenance. See `CONTRIBUTING.md` for the rules governing post-ratification changes.

## Practical scheduling

The three rounds nominally run 9-12 days each in wall-clock terms, but with multiple specifications in flight in parallel. Rough scheduling assumptions:

- A round is submitted on Friday
- SMEs respond by the following Tuesday or Wednesday
- Reconciliation happens Wednesday-Thursday
- Spec revisions happen Thursday-Friday
- Next round submitted the following Friday (if ready)

This rhythm assumes Mike's 3-hour weekday availability and the panel's typical response latency. If a spec is moving faster or slower, the rhythm adjusts.

Maximum three specifications in flight at any time. Beyond that, context-switching cost exceeds throughput gain.
