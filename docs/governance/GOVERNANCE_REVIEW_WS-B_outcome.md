# Governance Review — Workstream B: consolidated outcome

**Date:** 2 Jul 2026 · **Panel:** Mike (chair), Claude (coordinator), Grok, ChatGPT
**Inputs:** WS-B_review_pack v0.3 (source tree §2b), Grok response 2 Jul, ChatGPT
response 2 Jul. Context note: panel last active on the review ~3 weeks prior; both
responses were checked for stale assumptions — none found; all evidence cited is
from the pack.

## Consolidated position

**Unanimous, including Claude.** The build is a well-engineered fraud vertical
inside a monorepo *shaped* for a platform — but the platform does not yet exist as
extracted, reusable components. Both reviewers applied the same decisive test:
*delete `verticals/fraud/` — what reusable ML platform remains?* Answer today:
API, agent, infra, monitoring — **not** the ML lifecycle (features, training,
evaluation, validation, calibration, anti-leakage, serving), all of which
disappear with fraud. P-B1 confirmed; P-B2 confirmed; P-B3 confirmed with a
sharper boundary (below); P-B4 confirmed emphatically.

This is **not** an incoherence finding. The ADRs describe the platform correctly;
the skeleton anticipates it (contracts/, three vertical folders, shared infra);
the gap is the extraction step that every first vertical precedes. ChatGPT's
formulation is adopted as the defensible language: **"pipeline-as-platform is
architecturally specified but only partially evidenced in the current
implementation"** — not "aspirational".

## Consolidated rulings (for Mike)

**Q-B1 — Separation: not yet demonstrated.** Unanimous. Evidence is location, not
quality: all ML machinery is fraud-local; `contracts/fraud_scoring.py` is the
right shelf holding a vertical-named object; `compliance/` and `rm_support/` are
empty placeholders with no platform to consume. Acceptance evidence for
"platform" is either (A) an extracted `platform/` layer consumed by fraud, or
(B) a second vertical built with 80–90% platform reuse (ChatGPT), operationalised
by Grok's bootstrap test: a new vertical stood up in under a week from platform
primitives + contracts alone.

**Q-B2 — Lifecycle is Stage-1-heavy.** Unanimous. Stage 1 is convincingly built
(reference model, DVC-pinned serving, validation, provenance). Stage 2/3 — the
bank-operated product per ADR-0002/0003 — is specified but unimplemented and
largely undesigned. Converged minimum Stage-2/3 architecture before
"pipeline-as-platform" is claimed to a bank: (1) data adapters
(warehouse/feature-store integration points); (2) a Model Risk gateway
(train → validate → approve → promote workflow the bank runs); (3) registry
reconciliation — closes ADR-0006's deferred bank-registry ADR; (4) drift
detection → retraining trigger → approval → deployment loop; (5) bank-perimeter
deployment blueprints. The ADR-0006 deferral was independently identified by both
as the tell.

**Q-B3 — The boundary: machinery vs semantics.** ChatGPT's split is adopted as
the ruling frame — **the platform supplies the machinery; the vertical supplies
the business semantics**:

| Capability | Platform | Vertical |
|---|---|---|
| Serving (BentoML) | framework (ADR-0008) | endpoint config |
| Artefact provenance (DVC) | entirely (ADR-0007) | — |
| Anti-leakage | framework (windows, look-ahead detection, train/test validation) | domain leakage rules (txn timing, merchant hierarchy) |
| Calibration | framework (Platt/isotonic support) | method choice + thresholds |
| Validation | framework | thresholds |
| Feature pipeline | framework (transforms, dependency graph, execution, caching) | feature definitions (velocity, entropy, device reuse) |
| Model architecture, business rules, synthetic generators, evaluation metrics | — | entirely |

Grok's list is consistent; no split to resolve.

**Q-B4 — B10 as stated is wrong.** Unanimous and the panel's strongest position.
"Replicate the vertical" without prior extraction copies fraud-specific code N
times; both reviewers independently described the same failure sequence
(duplicated calibration/anti-leakage per vertical → divergence within months →
governance inconsistency a bank reviewer will find). Ruling recommended: insert
an explicit **Platform Extraction milestone** (working name **B9.5**) before B10,
with exit criterion: *a second vertical consumes shared ML lifecycle components
(training, validation, provenance, calibration, feature framework, serving,
governance) rather than copying them.* B10 then becomes "instantiate vertical
against platform template."

**Q-B5 — Red team: the exposed question.** Both produced the same killer question
from a bank's enterprise architect: *"Show me where your reusable platform begins
and the fraud solution ends"* — with ChatGPT's commercial variant *"If I buy only
Compliance, which code is common with Fraud?"* Today the honest answer is
infra/API/orchestration, not the ML lifecycle. Secondary exposure: the Stage-2/3
Model Risk gating and registry story. Both are answered by the B9.5 + Stage-2/3
rulings above; until then, external material must use the "specified, partially
evidenced" language, never "the platform exists."

## Unique catches

- **ChatGPT:** the machinery/semantics boundary table (adopted); the wording
  discipline; the buy-one-vertical commercial question.
- **Grok:** the bootstrap-in-a-week operational test (adopted as B9.5 acceptance
  evidence); make `contracts/` vertical-neutral now, not at extraction; track
  spec↔build alignment as a decision record (feeds WS-C/WS-D).

## Splits

None of substance. One tonal split (aspirational vs partially-evidenced)
resolved in ChatGPT's favour for all external and locked-doc language; Grok's
bluntness retained for internal planning.

## Claude's position (stated last, per method)

Concur with the consensus in full. Two additions on **timing**, which the panel
was not asked to rule on:

1. **Do not halt the build to extract now.** B6–B9 (agent, RAG, guardrails, UI)
   are mostly not vertical-ML machinery; extraction naturally sits after B9,
   exactly where ChatGPT placed it. Halting at B5 to extract would trade momentum
   for abstractions designed against a sample of one vertical.
2. **Adopt platform-first discipline from B5/inc2 onward** for anything new and
   shared: CL-13's promotion-gate CI should be written as a platform mechanism
   with fraud-supplied config, not a fraud-local script; the CL-12 provenance
   manifest schema should be vertical-neutral. This makes B9.5 smaller when it
   arrives.

## Findings register — additions

| ID | Area | Sev | Finding | Recommendation |
|---|---|---|---|---|
| F-011 | B | High | No extracted platform layer; ML lifecycle entirely fraud-local; ADR-0003 partially evidenced | B9.5 Platform Extraction milestone before B10 (D-05) |
| F-012 | B | Med | Stage 2/3 unimplemented and largely undesigned; product value per ADR-0003 sits there | Minimum Stage-2/3 design per Q-B2 list; closes ADR-0006's deferred registry ADR (D-07) |
| F-013 | B | Low | `contracts/fraud_scoring.py` vertical-named on the platform shelf | Generalise to vertical-neutral contract at B5/inc2 or B9.5 (Grok) |
| F-014 | B/C | Low | External/positioning language risks overclaiming "platform" | Standard wording: "architecturally specified, partially evidenced" until B9.5 exit met (D-06) |

## Decisions owed by Mike (gate WS-B close)

- **D-05** Insert the B9.5 Platform Extraction milestone (exit criterion as
  above) — amends the Build & Quality Plan; rises to a formal ADR
  (candidate ADR-0009: platform/vertical capability boundary + extraction gate,
  adopting the Q-B3 machinery/semantics table).
- **D-06** Ratify the language ruling (F-014) for all client-facing and locked
  documents.
- **D-07** Commission the minimum Stage-2/3 design as a named workstream (post
  governance review; feeds the deferred bank-registry ADR from 0006).
- **D-08** Timing: confirm extraction at B9.5 (not now), with platform-first
  discipline for new shared components from B5/inc2 (Claude's position; panel
  silent).

## Remediation

**Nothing here blocks resume to B5/inc2** — the resume gate (CL-01–05) closed in
WS-A. All WS-B items gate **B10** (and D-05's ADR gates the plan amendment):
- CL-14: write ADR-0009 per D-05 (boundary + B9.5 gate). Blocks B10.
- CL-15: amend Build & Quality Plan + BUILD_TRACKER with B9.5. Blocks B10.
- CL-16: generalise `contracts/` to vertical-neutral (F-013). Backlog; latest B9.5.
- CL-17: apply F-014 wording to external material at next revision. Backlog.
- CL-18: Stage-2/3 minimum design brief (D-07). Named workstream, post-review.

## WS-B exit status

**Closes on Mike's ratification of D-05–D-08.** Per plan exit criterion 2, the
architecture is confirmed ADR-*consistent in intent* with every drift logged and
owned — the honest formulation the review exists to produce. → Next: WS-C
(specifications currency); first exhibit already identified (Spec 01 working
brief re-base).
