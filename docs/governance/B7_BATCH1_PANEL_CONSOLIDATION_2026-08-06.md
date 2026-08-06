# B7 Batch 1 — Panel Round 1 Consolidation (2026-08-06)

*Coordinator-authored consolidation of the batch-1 panel round. Records
composition, verdicts, machine-verified facts, dissent map, and the open
chair rulings. Nothing here is ruled; recommendations are advisory.
Companion to the three reviewer returns (Grok, Gemini, DeepSeek),
retained verbatim by the operator.*

## Round composition

| Reviewer | Status | Notes |
|---|---|---|
| Grok | Returned | Third pass over related material (passes 1–2 were pre-review, no verdicts). Familiarity annotation carried (WS-E 36 class). Circulated as repo-sourced ZIP. |
| Gemini | Returned | Substitute reviewer — appointed after ChatGPT withdrawal. chatgpt-primer applied unmodified (no gemini primer on the bench). Individual-file circulation. |
| DeepSeek | Returned | Primed bench reviewer (deepseek-primer ratified). |
| ChatGPT | Withdrawn | Subscription wall. Conduct note: pass 1 ignored the pack and proposed unrequested work (stale-context read); pass 2 correctly refused to issue verdicts on truncated ZIP evidence — a positive reviewer-integrity data point despite withdrawal. |

Circulation method finding: packs to ChatGPT-class sandboxes go as
individual files, not archives (ZIP extraction truncation). Grok took
the ZIP intact.

## Verdicts as returned

| Question | Grok | Gemini | DeepSeek |
|---|---|---|---|
| TY-03 | Accept | Accept | Accept |
| TY-04 | Accept | Accept w/ amendment (TR-01 pinpoints) | Accept w/ amendment (CV-01 promote) |
| TY-05 | Accept | Accept | Accept |
| TY-06 | Accept | Accept | Accept |
| TY-07 | Accept | Accept | Accept w/ amendment (TR-01 promote) |
| TY-08 | Accept | Accept | Accept |
| TY-09 | Accept | Accept | Accept |
| Batch | Accept | Accept w/ amendments | Accept w/ amendments |
| CL-23 | Accept (B8 design input) | Accept | Accept in principle + 6 amendments + 1 challenge |

## Machine-verified facts (operator's machine, 2026-08-06)

1. **Gemini's TY-04 amendment DISCHARGED.** TY-04 §5.1 cites TR-01 §3.4;
   TR-01 §3.4 (line 72) is "Rules should degrade safely… [silent
   failure]" — aligned. TY-04 §5.2 cites TR-01 §5.1; TR-01 §5.1 (line
   105) is "Confirmed fraud outcomes should flow back into rule
   calibration…" — aligned. Both pinpoints verified correct.
   Gemini's verdict therefore resolves to Accept.
2. **Word counts (Measure-Object):** TY-03 970, TY-04 1018, TY-05 911,
   TY-06 861, TY-07 958, TY-08 718, TY-09 843. Total 6,279.
   Gemini exact on all seven. DeepSeek's TY-04 "861" was a
   transposition of TY-06's count (its batch total of 6,279 was
   correct). Grok stated no counts.
3. **TY-07 → TY-03 reference:** real — one occurrence, line 13,
   in-passing ("in the typologies at TY-02 and TY-03 the customer
   authorises the payment under coercion or deception"). Carries NO
   pinpoint. DeepSeek's "§5.1" attribution is fabricated. Whether this
   reference belongs in the check transcript is a parsing-rule
   question (formal citation vs in-passing mention) — flagged for the
   next check/pack revision, not a batch defect.

## Dissent map (chair to rule; dissent logged whichever way)

| Item | For promote | Against / silent | Coordinator note |
|---|---|---|---|
| CV-01 → TY-04 design edge | Grok, DeepSeek | Gemini silent | Two-of-three, both citing §4.1 coercion indicators as structural to the exit-decision framework. Strongest promotion case. |
| SG-01, SG-02 → TY-04 | Grok | DeepSeek: leave (supportive not structural) | Genuine split. DeepSeek's structural/supportive distinction is the sharper argument. |
| TR-01 → TY-07 design edge | DeepSeek | Grok: leave ("well-anchored") | Split. DeepSeek's textual case (§5.3 "applies with full force") is strong. |

Any promotions land as EDGES.yaml v0.2.2 with its own change note
(nine-edge v0.2.1 precedent: operator-approved repair revision).

## CL-23 — DeepSeek amendments (for folding into the B8 design brief)

1. Gap 6: routing decision + policy_version recorded at routing time,
   pre-agent-action; human judgement a separate linked Tier 3 event.
2. Gap 4: one-way ratchet applies to removal; schema expansion is a
   platform release act, new fields denylisted by default.
3. Architecture Principle corollary: policy bundles content-addressed,
   versioned, retained immutably; no deletion from historical store.
4. Gap 2: sentinel policy_version for pre-policy decisions
   ("no policy in force" distinguishable from "not recorded").
5. Tier 1 red line stated commercially: a bank requiring Tier 1
   policy-addressability is outside the deployment perimeter.
6. Engine-fit challenge: B8 brief to test OPA/Rego per domain;
   retention scheduling may prefer declarative config + scheduler,
   with identical policy_version provenance either way.

None conflict with the Grok/Gemini accepts (they accepted a weaker
document). Recommended treatment: accept CL-23 as B8 design input with
amendments 1–6 folded as panel-sourced revisions for the B8 brief to
test; no re-review this stage.

## Reviewer calibration ledger (entries this round)

- **Grok:** 21/21 accepts across all verdicts ever issued; zero
  amendments; third-pass familiarity. Weight accordingly until it
  produces a finding that survives verification.
- **Gemini:** counts exact 7/7; sole amendment was a real check it
  honestly could not perform (TR-01 absent from evidence base) and it
  discharged on verification. Clean first outing.
- **DeepSeek:** deepest semantic read (only reviewer to interrogate
  CL-23; found the untranscribed TY-03 reference) AND fabricated a
  pinpoint (§5.1) and transposed a word count. High-yield,
  low-precision: findings valuable, every citation spot-checked
  before action.
- **ChatGPT:** refused to fabricate over incomplete evidence (pass 2).
  Positive integrity marker if re-benched later.

## Scope note

All three returned reviewers pre-endorsed batch-2 authoring
proceeding. Sequencing is the operator's ruling (WS-E 58), not the
panel's to grant. Recorded once; no weight attached.

## Open chair rulings

1. Per-document verdicts TY-03..09 (all three converge on
   accept-in-substance; amendments are EDGES questions, not rewrites).
2. CV-01 → TY-04 promotion (recommend: grant).
3. SG-01/SG-02 → TY-04 (recommend: leave as extras; log Grok dissent).
4. TR-01 → TY-07 (recommend: grant on the §5.3 textual case; log Grok
   dissent — or leave and log DeepSeek; genuinely arguable).
5. CL-23: accept as B8 design input with DeepSeek amendments folded.
6. Listing: TY-03..09 to pending_review (new manifest version,
   appended transitions only, per DEC-0014).
7. Batch-2 gate (WS-E 58 condition — verdicts in — now satisfied).
8. EDGES v0.2.2 (contents per rulings 2–4).

## Round status

CLOSED at three reviewers on operator confirmation. Verdict documents
retained verbatim by operator; this note consolidates, it does not
supersede them.
