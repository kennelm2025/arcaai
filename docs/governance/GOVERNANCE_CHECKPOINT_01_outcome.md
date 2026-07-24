# Governance Checkpoint 01 — Outcome (July 2026)

**Status:** CLOSED — converged 24 Jul 2026, unanimous, zero dissents
**Chair/decider:** Mike Kennelly · **Coordinator:** Claude
**Panel:** ChatGPT, Grok · **Protocol:** three rounds per house standard
**Pack:** GOV_CHECKPOINT_01_PACK.md (this folder, PR #23)
**Position in plan:** ran as "WS-D part 0", preceding the WS-D Build &
Quality Plan session

## Summary

First programme-level governance checkpoint (its own absence to date
recorded as finding zero). Round 1: independent review against Q1–Q7;
Round 2: cross-review against chair corrections (CL ledger ages,
CL-08 actual content, CL-10 double entry, exposure statement);
Round 3: convergence pack of 14 ratification items + 2 chair
findings, all CONCUR from both reviewers with no factual objections.

Panel verdict (ChatGPT, Round 3): governance framework "credible,
proportionate, and internally consistent"; progression to B7
authorised subject to execution of RAT-02 and the chair actions.
Grok (Round 2): "no new Must-Fix items remain under the corrected
exposure and CL data."

Notable Round 2 movement: Grok withdrew its Round 1 Must-Fix
precondition on safety controls upon the exposure statement (zero
external users/demos/deployment); ChatGPT adopted the threat
catalogue, residual-risk statement, and six-week cadence backstop.
Convergence was genuine — findings were refined, merged, or
withdrawn on evidence rather than defended.

## Chair rulings

- **CR-1:** cadence backstop retained — every two closed gates OR six
  weeks, whichever first (grounds: research-heavy stages stall
  silently; B6 sat at 4-of-5 increments for days with no governance
  visibility).
- **CR-2:** safety-trio wording unified — Must-Fix exit criterion of
  B8 AND hard precondition for any external exposure, whichever first.

## Chair findings

- **CF-1:** architecture-conformance gap — no control checked
  conformance of the build to the locked BA/ADRs (WS-E 34 the proof
  instance). Remedy: standing gate-checklist conformance question
  (with CL-08's decision-capture question, same edit); spot-check at
  B7 gate. Retrospective B1–B6 audit rejected as gold-plating.
  Carried into WS-D.
- **CF-2:** chair actions — (a) CL-08 executed (checklist edit);
  (b) CL-10 phantom open entry corrected; (c) DEC-0008 annotated
  with reversibility sentence.

## Ratified items (all unanimous)

| # | Item | Severity / timing |
|---|---|---|
| RAT-01 | Week model abandoned; gate-based tracking official; one-time variance note | Must-Fix |
| RAT-02 | Governance trio: prompt/response audit logging, immutable execution metadata, request-validation wrapper | Should-Fix, before B7 |
| RAT-03 | Safety trio: injection detection, PII redaction, grounding verification | Per CR-2 |
| RAT-04 | Gate Acceptance Record section in gate template (producer + approver statements, evidence, residual risks, Pass/Conditional/Fail) | Should-Fix |
| RAT-05 | One-page AI threat catalogue (prompt manipulation, retrieval poisoning, hallucination, provenance failure, information leakage, unsafe tool invocation) | Should-Fix, before B8 |
| RAT-06 | Guardrail precedence hierarchy, one page | First artefact of B8 |
| RAT-07 | Model-risk artefacts (inventory entry, validation plan skeleton, audit-trail schema) | B8 exit criterion |
| RAT-08 | Reversibility sentence rule for technical decisions ahead of parked strategic decisions; DEC-0008 retro-annotated | Rule |
| RAT-09 | Ledger consistency check in checkpoint preparation | Rule |
| RAT-10 | Process rules ratified: one-git-command-per-prompt; written boarding checklist. WS-E 30–34 closed "trialled and ratified"; backfill rider retained; ledger first-class in-repo | Ratified |
| RAT-11 | Backlog healthy; CL-08 closed; CL-10 fixed; CL-17/19/20 bundle confirmed, hard trigger post-B8; CL-09 before any external review | Verdict |
| RAT-12 | Cadence: 2 gates OR 6 weeks; exceptional triggers: gate failure, boundary/model-risk ADR, deployment-target or artefact-store change, FCA/PRA-facing engagement, ship-critical WS-E incident, scheduled external exposure/demo/audit | DEC-0009 |
| RAT-13 | Panel: current pair adequate; regulatory/Model Risk seat from B8; research seat parked | Ratified |
| RAT-14 | Build order B7→B8→B9→B9.5 unchanged; B7 after WS-D | Ratified |

## Obligations register (created by this checkpoint)

- Before B7: RAT-02 governance trio.
- Before/at B8: RAT-05 threat catalogue; RAT-06 precedence hierarchy
  (first artefact); RAT-03 safety trio (exit criterion); RAT-07
  model-risk artefacts (exit criterion); RAT-13 regulatory seat.
- Standing: RAT-08 reversibility rule; RAT-09 ledger check; RAT-12
  cadence (DEC-0009); Gate Acceptance Record (RAT-04) from the next
  gate document onward.
- Executed at closure (this PR): RAT-01 (BUILD_TRACKER week column
  removed, variance note recorded); CF-2 chair actions; standing gate
  checklist (CL-08 + CF-1 questions) established in BUILD_TRACKER.
- WS-D carries: CF-1 spot-check design for the B7 gate.

## Round record

Reviewer outputs for all rounds are retained verbatim in
GOV_CHECKPOINT_01_working_papers.md (this folder). Circulation packs:
GOV_CHECKPOINT_01_ROUND1_CIRCULATION / ROUND2_to_GROK /
ROUND2_to_CHATGPT / ROUND3_CONVERGENCE.

**Next programme checkpoint due:** two closed gates after this one
(B8 gate) or 4 Sep 2026, whichever comes first.
