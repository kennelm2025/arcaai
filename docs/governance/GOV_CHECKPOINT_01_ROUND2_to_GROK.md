# ArcaAI — Governance Checkpoint 01 — ROUND 2 (to Grok)

You reviewed ArcaAI at programme level in Round 1 (findings
R1-G-01..07). Below: (A) chair's factual corrections and new evidence,
(B) the other reviewer's Round 1 output verbatim, (C) steer questions.

**Round 2 task:** challenge, concur with, or refine the other
reviewer's positions and revise your own where the new evidence
warrants. Same output discipline: numbered responses to the steers,
then any revised or new findings (`R2-G-NN`), each with severity and
smallest proportionate remedy. Round 3 will be convergence and chair
triage.

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

**A2 — Correction to your R1-G-03 remedy.** You proposed "mandatory
decision template + single source of truth". Both already exist
(DECISIONS.md with DEC/ADR templates; canonical CL ledger per
DEC-0007). CL-08's actual content is a one-file edit adding the
four-option question above to the gate checklist. The chair intends
to execute it as a chair action during this checkpoint and record it
closed at Round 3. Confirm this satisfies R1-G-03, or state what
residue remains.

**A3 — Ledger hygiene defect found while extracting A1.** CL-10
appears twice: open-unticked in the 2 Jul list, closed-ticked in a
later section. Anyone grepping the ledger sees an open CL-10 that is
in fact done. Relevant to Q3 and to the other reviewer's evidence-
over-documents point.

**A4 — Exposure statement (relevant to your R1-G-01).** As of today:
zero external users, zero scheduled demonstrations, no deployment
outside the developer machine. The B6 agent runs locally against
local Ollama. First plausible external exposure is B9 (chat UI) at
the earliest.

## B. Other reviewer's Round 1 (ChatGPT) — verbatim

*[Circulated with ChatGPT's Round 1 inserted verbatim at this point —
retained in GOV_CHECKPOINT_01_working_papers.md §2.]*

## C. Steer questions for Round 2

**S1 — The Q1 clash.** You proposed pulling forward three *safety*
controls (injection detector, Presidio redaction, grounding check) as
Must-Fix preconditions for further B6 work. ChatGPT explicitly
declined those and instead proposed three *governance* controls
(prompt/response audit logging, immutable version metadata,
deterministic request-validation wrapper) at Should-Fix, leaving
Presidio/grounding in B8. Given the exposure statement in A4: defend,
amend, or withdraw your precondition framing. Are the two sets
complements or substitutes, and what is the minimal combined set with
honest severities?

**S2 — Precedence hierarchy (CGPT-04).** ChatGPT proposes a one-page
guardrail precedence hierarchy (which control wins in conflict)
defined *before* B8 implementation. React: right, wrong, or
premature before B7 retrieval exists?

**S3 — Acceptance authority.** ChatGPT's omissions section raises
gate acceptance mechanics: who approves, mandatory evidence,
producer/approver separation, failed vs conditional pass, dissent
recording — made explicit even where one person holds all roles.
React, and if you concur, propose the smallest artefact that
satisfies it.

**S4 — Q3 re-triage on real ages.** Your Round 1 triage inferred
rot from item numbering. Re-run it on the A1 table. Note CL-06
intersects with the named decisions/→adrs/ rename backlog item, and
A3 (CL-10 double entry) is new evidence.

**S5 — Cadence merge.** Your cadence (2 gates / 6 weeks, whichever
first) vs ChatGPT's (2 gates, no time bound). ChatGPT's trigger list
includes deployment-target changes — pointed, given DEC-0008 moved
the DVC remote to S3 while the AWS endgame decision is PARKED.
Propose the single merged cadence + trigger list for the Round 3 DEC.
