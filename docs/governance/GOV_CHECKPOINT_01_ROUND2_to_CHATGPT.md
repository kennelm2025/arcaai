# ArcaAI — Governance Checkpoint 01 — ROUND 2 (to ChatGPT)

You reviewed ArcaAI at programme level in Round 1 (findings
R1-CGPT-01..05). Below: (A) chair's factual corrections and new
evidence, (B) the other reviewer's Round 1 output verbatim, (C) steer
questions.

**Round 2 task:** challenge, concur with, or refine the other
reviewer's positions and revise your own where the new evidence
warrants. Same output discipline: numbered responses to the steers,
then any revised or new findings (`R2-CGPT-NN`), each with severity
and smallest proportionate remedy. Round 3 will be convergence and
chair triage.

---

## A. Chair's corrections and new evidence

**A1 — CL ledger ages (requested by both reviewers).** Canonical
ledger is docs/governance/GOVERNANCE_REVIEW_CHANGELOG.md (DEC-0007).
Open items with content and age as of 24 Jul:

| CL | Content | Opened | Age |
|---|---|---|---|
| CL-06 | Standardise ADR citations to four-digit repo-wide | WS-A ~1 Jul | ~3.5 wks |
| CL-07 | Triage DECISIONS.md entries for ADR promotion (DEC-0003 candidate) | WS-A ~1 Jul | ~3.5 wks |
| CL-08 | Add decision-capture question to gate checklist + BUILD_TRACKER ("What architecturally significant decisions since last gate? → None / Existing ADR / DEC log only / New ADR required") | WS-A ~1 Jul | ~3.5 wks |
| CL-09 | Fold XGBoost + Platt rationale into fraud Model Card | WS-A ~1 Jul | ~3.5 wks |
| CL-11 | Decider/Deciders field-name mismatch (cosmetic) | 2 Jul | ~3 wks |
| CL-16 | Generalise contracts/ to vertical-neutral — latest B9.5 | WS-B ~2 Jul | ~3 wks |
| CL-17 | DEC-0006 wording rule to external material at next doc revision | WS-B ~2 Jul | ~3 wks |
| CL-18 | Stage-2/3 minimum design brief (D-07) — named workstream | WS-B ~2 Jul | ~3 wks |
| CL-19 | Pre-trained-models distinction sharpened at next BA revision | 21 Jul | 3 days |
| CL-20 | Fourth competitive category into BA positioning + WS3.1 | 21 Jul | 3 days |

**A2 — CL-08 disposition.** Both reviewers said execute now. The
actual item (see table) is a one-file edit; the "mandatory template +
single source of truth" the other reviewer proposed already exist
(DECISIONS.md; canonical ledger per DEC-0007). The chair intends to
execute CL-08 as a chair action during this checkpoint and record it
closed at Round 3. Object if you see residue.

**A3 — Ledger hygiene defect found while extracting A1.** CL-10
appears twice: open-unticked in the 2 Jul list, closed-ticked in a
later section. Anyone grepping the ledger sees an open CL-10 that is
in fact done — relevant to your evidence-over-documents point and to
Q3.

**A4 — Exposure statement.** As of today: zero external users, zero
scheduled demonstrations, no deployment outside the developer
machine. The B6 agent runs locally against local Ollama. First
plausible external exposure is B9 (chat UI) at the earliest.

## B. Other reviewer's Round 1 (Grok) — verbatim

*[Circulated with Grok's Round 1 inserted verbatim at this point —
retained in GOV_CHECKPOINT_01_working_papers.md §1.]*

## C. Steer questions for Round 2

**S1 — The Q1 clash.** Grok proposed pulling forward three *safety*
controls (injection detector, Presidio PII redaction, grounding
check) at Must-Fix, as preconditions for any further B6 work or
external demonstration. You proposed governance controls instead
(audit logging, version metadata, request-validation wrapper) at
Should-Fix. Given the exposure statement in A4: is Grok's
precondition framing defensible, over-scoped, or right-but-mistimed?
Are the two sets complements or substitutes, and what is the minimal
combined set with honest severities?

**S2 — Grok's omissions set.** Grok flagged four omissions you did
not: (a) no threat model / abuse-case catalogue for the LLM agent —
arguing the WS-E 34 provenance defect is exactly the class a threat
model surfaces; (b) no residual-risk statement in gate docs, only
pass evidence; (c) no model-risk artefact readiness (model inventory
entry, validation plan skeleton, audit-trail schema); (d) the
S3-remote switch (DEC-0008) executed while the AWS platform-endgame
decision is PARKED, with reversibility unstated. React to each:
finding-worthy now, park to a named gate, or noise?

**S3 — Q3 re-triage on real ages.** Your Round 1 declined to age the
backlog without contents. Re-run on the A1 table. Grok's inferred
"rotting" list was CL-06/07/09/11 — does it survive contact with the
actual contents? Note CL-06 intersects with a named decisions/→adrs/
rename backlog item, and A3 (CL-10 double entry) is new evidence.

**S4 — Cadence merge.** Your cadence (every two gates) vs Grok's
(two gates or six weeks, whichever first). Given research-heavy
stages can stall silently — B6 sat at 4-of-5 increments for several
days — does a time bound earn its place? Propose the single merged
cadence + trigger list for the Round 3 DEC.

**S5 — Acceptance authority, sized.** Your acceptance-authority
omission stands unchallenged so far. Propose the smallest concrete
artefact that satisfies it for a solo founder — a one-page gate
authority note? A section in the gate template? Name it, so Round 3
can ratify something specific rather than an aspiration.
