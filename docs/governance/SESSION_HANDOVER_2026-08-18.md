# ARCAAI CHAT HANDOVER — 2026-08-18 (morning)

For the successor coordinator chat. Covers the state at close of the
2026-08-17 session — the session that discharged item 35 (scenario spec
schema v0.3), authored RQA batch 1 (seven scenarios), and found a live
guard bypass by controlled probe, contained the same hour by server-side
branch protection. Registers are the authority; this handover is
narrative. Where this document and a live read disagree, the repo wins.

Companion state on D:\Downloads: the CC finding file (git -C bypass),
the amendment pack, and the stop reports for PRs #135–#139.

---

## 1. REGISTER STATE (verify live at boot)

DEC next 0018 · ADR next 0011 (reserved, unconsumed) · CL next 31 ·
WS-E next 74 (72 and 73 both consumed 2026-08-17).

HEAD at close: merge commit 8b693cf (PR #139). Verify against a freshly
regenerated manifest at boot — do not trust this line, read it.

Branch protection is LIVE on main: ruleset `main-protection`,
id 20906548, Active, bypass list EMPTY — PR required (0 approvals),
force pushes blocked, deletions blocked. Recorded as read via gh api in
PR #139. Note: classic branch-protection API 404s because the repo uses
rulesets; the 404 is the expected reading, not an absence.

## 2. HEADLINE: SCHEMA v0.3 + BATCH 1 AUTHORED + GUARD BYPASS FOUND

- Item 35 DISCHARGED — scenario spec schema v0.3 merged (PR #136),
  honouring all five RevC spec-side requirements. Typology ruled
  Option A: identifier-shaped string, pattern
  `^[a-z0-9]+([._-][a-z0-9]+)*$`, form-only, non-comparability
  disclaimed in the description AND asserted by test. No enum — RevC
  §2.4 and ADR-0009 bar vertical semantics in platform machinery.
- RQA-101..107 AUTHORED against v0.3 (PR #137): seven specs + seven
  authoring records + a batch set-record, all validating exit 0, all
  pinned to ONE corpus state (manifest 2026-08-13.8, retrieval snapshot
  878b3439...). Authored under item 12 option (b): current 16-doc
  corpus, re-pin debt accepted and logged.
- WS-E 72 RAISED: a git global option before the subcommand (-C proven;
  class named: -c, --git-dir, --work-tree, --no-pager) defeats the
  guard's subcommand-anchored deny regexes. Two controlled pairs:
  branch -D and force-push (the CL-E1 guard). Case-folding and
  deny-precedence explicitly disconfirmed as causes.
- WS-E 73 RAISED: the redirection inside 2>&1 reads as a write
  construct — the real mechanism behind item 39's false-red; the
  path-string theory is disconfirmed and item 39 corrected.
- EMERGENCY M3 SUBSET DONE (operator, browser): branch protection per
  §1. Full item 34 treatment (required status checks, M4 signing)
  still owed — the status-check refinement is blocked on the ci-docs
  paths-filter question (see §7).

## 3. WHAT LANDED 2026-08-17 (all merged to main, all verified post-merge)

- PR #135 — session-open housekeeping: 2026-08-17 handover landed
  verbatim, two owed cost rows (with derived PRs/registers, NOT
  SUPPLIED discipline), six queue corrections + five appends (35–39),
  WS-E 71 identified (coverage excludes arcaai/ — same defect as the
  owed coverage-source ruling).
- PR #136 — schema v0.3 (five files, +626). Both version→path map
  sites edited in one commit (runner.py 81–83, test file 42–43),
  duplication flagged not refactored; 16 tests added; harness suite
  46 passed. document-register.yaml entry NOT made — it is a retired
  tombstone; resurrection refused correctly; gap queued as item 41.
- PR #137 — RQA batch 1 (16 files, +1418). Series-level findings
  S1–S4 recorded, not passed silently (see §5).
- PR #138 — set-record Rulings section: R1 evidence boundary, R2
  RQA-107 marker-drop ratification, placed BEFORE the findings they
  govern.
- PR #139 — guard-bypass findings landed by copy (hash-verified
  source=destination=blob), fix-spec addendum as an adjacent file
  (verbatim-hash and append cannot both hold in one file — adjacent
  placement ratified), amendment record honestly titled ("P4 FAILED —
  deny bypass found; widening HELD"), WS-E 72+73 raised, items 39
  corrected / 27 HELD / 42+43 raised. First merge under branch
  protection. SO-1's first exercise verified it — all six steps, no
  judgement calls, anchor movement 71→73 as independent confirmation.

## 4. THE GUARD BYPASS (what the successor must hold)

Until the guard repair lands, the git deny surface is bypassable at
the client and BRANCH PROTECTION IS THE CONTROL ACTUALLY HOLDING main.
Nothing improper was attempted; but no prior session's clean record is
evidence the denies worked, and no such claim may be made.

- Fix spec (operator-authored, at the operator's terminal — .claude/
  writes have no in-session route): F1 anchor each deny on the
  subcommand anywhere in the argument vector, not immediately after
  `git`; F2 stop treating a stderr redirection (2>&1) as a write.
- Re-probe list (item 42): both controlled pairs + one probe per named
  global option. A green counts only when EVERY row passes. Item 42
  blocks item 27 Part B.
- Amendment state: Part A (read/verify allows) APPLIED and unaffected —
  read-class allows cannot reach the deny families. Part B
  (reversible-mutation widening) drafted and HELD; the
  allow-pre-empts-guard interaction is recorded as an open question.
- Item 43: reconcile the no-bare-cd convention (WS-E 68) with the
  guard's patterns — the two individually-correct rules combined into
  this hole. Tested, not reasoned about. Interim practice adopted:
  plain git from the repo-root cwd.
- Incidental mechanism of record: when the guard refuses, it blocks
  the ENTIRE tool call, not the offending line.

## 5. BATCH 1 — THE FACTS THAT GOVERN ITS USE

- R1 (ruled, in the set-record, BEFORE the findings): a green across
  RQA-101..107 evidences document-level presence only — no precision,
  rank, or distractor claims. Practical test included in R1's text.
- S1: the entire set sits at |E| = 2 — structural, every eligible
  series holds exactly two documents. RevC §5.4's precision-or-rank
  obligation begins at |E| ≥ 5 and never triggers in batch 1. THE
  ITEM 12 INCLUSION DECISION IS NOW THE GATE ON EVIDENTIAL DEPTH:
  admitting the pending fourteen makes |E| ≥ 5 constructible
  (RQA-104's series goes two → nine).
- S2: the dense end of the corpus is unexercised — OGL-0003 (7 chunks)
  and OGL-0004 (16) in no expected set.
- S3: two inclusion triggers differing in kind — RQA-106 re-authoring
  (sufficiency fails by construction if TY-03/04 land); RQA-104
  Obligation D expiry.
- S4: the v0.3 1000-char justification cap refused its own author
  twice — uncalibrated; first entry in the v0.4 hopper.
- Re-pin debt: all seven scenarios, logged on item 12, contingent on
  the inclusion ruling.
- RQA-107 typology ratified as `statute.fraud_act_2006` (marker
  dropped; R2 in the set-record).
- Nothing has been RUN. Authoring and execution are separate acts.
  Regime 2 remains blocked behind the evaluator golden-fixture suite.

## 6. COORDINATOR-CHAT CONVENTIONS (binding; additions this session marked NEW)

- Every instruction to CC ships as a NUMBERED CC PROMPT block; only
  pure information travels bare. Tally: prompts through 124 consumed
  (115 consumed-with-delivery-failure; 122 consumed-with-delivery-
  uncertain, never echoed). The close ceremony consumes 125 (rulings +
  close PR) and 126 (merge-verify), so NEXT IS 127 — verify against
  the close record at boot.
- NEW — ECHO: every CC response opens "ANSWERING PROMPT <n>" and flags
  any gap in received numbers ("last received was N"). A response
  without a valid echo is checked for a wrong-window paste before any
  ruling in it is acted on.
- NEW — DELIVERY: rulings travel ONLY as numbered prompts into the CC
  terminal. An acknowledgment from anywhere else is not delivery
  (the PROMPT 115 lesson — a non-CC source answered in CC's voice and
  the chain ran two turns on an undelivered ruling).
- NEW — PLACEHOLDERS: a prompt containing an unfilled [FILL] slot is
  not ready to issue. The coordinator collects the value BEFORE
  issuing. (Third unfilled-placeholder instance reached CC this
  session: 103, 106, 124.)
- NEW — SO-1 (merge verification standing order): trigger form
  "PROMPT <n>: MERGED — VERIFY #<pr>". Fixed six steps: gh pr view
  from the artefact; pull + HEAD check; all stop-report hashes at
  HEAD; safe branch delete + prune; manifest regen (dirtied tree =
  STOP); fixed report table. Any failed step is a STOP, not a repair.
  Scope: the named PR only. Both exercises to date ran on unnumbered
  triggers — honoured, gap flagged; use the numbered form.
- NEW — Part A live: read/verify commands (git read ops, hashing,
  grep/find-read, validators, pytest, check_docs, ruff) are settings-
  allowed and no longer ask. Mutation commands still ask until item 42
  then Part B.
- Payloads move as FILES in both directions; panel returns disk-first;
  both-halves evidence, separately attributed; silence != pass;
  decline ALL don't-ask-again offers; verify from the artefact, never
  the report; gh pr merge is an UNCONDITIONAL ASK — operator merges in
  the browser; Gmail progress summary at close (standing rule).
- Subagent constraint of record: subagents hold no execution tool —
  they AUTHOR only; all hashes, pins, and validation are computed
  centrally by CC.

## 7. THE OWED LIST (verify against a live queue readback)

Head of the queue:
1. Item 42 — guard repair F1/F2 at the OPERATOR'S terminal, then the
   re-probe list. Blocks item 27 Part B. Until then branch protection
   is the control holding main.
2. Item 12 — corpus inclusion decision (14 documents pending_review),
   now carrying batch 1's re-pin debt AND gating evidential depth
   (S1). Two scenarios need more than a re-pin (RQA-106, RQA-104).
3. Evaluator golden-fixture suite — §8.1 entry criterion, contract per
   F-GROK-09, ownership OPERATOR. Blocks Regime 2. Unmoved.
4. Item 36 — runner RevC conformance, now SEVEN elements (six result
   fields + the load-time top_k <= top_k_absolute_cap assertion + the
   §5.5 ruled-variance assertion on corpus expansion).
5. Item 34 — full M3 treatment (required status checks — blocked on
   the ci-docs paths-filter gap below) + M4 signing; item 41 (register
   home for code-series artefacts) routes here, M7's traceability
   matrix needs it.
6. Item 33 ruling pack + B7_GATE.md sync (before first gate exit).
7. Item 40 — pre-existing pytest failure (FastAPI drift,
   test_route_is_wired_to_contract_models): full-suite green is
   unavailable as evidence until fixed.

Also owed:
- Operator's probe-evidence half — NOT SUPPLIED at close (whether any
  ask fired during P1/P2/P4 and the extension probes). A late supply
  lands as a dated supplement to the amendment record. "Not observed"
  is a valid value.
- Item 25 WIDENED + workflow half: neither check_docs (roots docs/,
  decisions/) nor the ci-docs paths filter reaches verticals/ — nine
  scenario markdown files have structural checking from NEITHER layer.
- Item 43 — cd-convention/guard reconciliation (tested, not reasoned).
- RevC filename DRAFT-drop (item 37) · delta pack send-time slot
  (item 38) · Gemini standing primer · vector-store ownership repair ·
  embedder decision record (before Regime 2) · coverage-source
  widening ruling (WS-E 71's fix) · default-mode discriminator re-run ·
  shell-branch anchoring (WS-E 70) · pin-value pre-run assertion ·
  TOR §5A:101 amendment (three-leg identity statements).

## 8. COORDINATOR ERRORS (owned, for calibration)

2026-08-17, this coordinator:
- Ruled a closed typology enum (D2) against text the panel accepted two
  days earlier — RevC §2.4 bars exactly that cure (vertical semantics
  in platform machinery, ADR-0009). Caught by CC's stop condition
  before it reached an immutable file. Lesson: check the accepted
  text's own ruling on a cure before ruling it.
- Treated a non-CC acknowledgment as delivery of PROMPT 115; the chain
  ran two turns on an undelivered ruling and PROMPT 116 fired against
  a phantom merge. Caught by CC's precondition. Mend: the DELIVERY and
  ECHO conventions in §6.
- Shipped an unfilled [FILL] placeholder in PROMPT 124 (third
  instance). Mend: the PLACEHOLDERS convention in §6.
- Instructed "apply Part A" in a prompt (122/123) though settings
  writes are operator-only by the WS-E 69 hardening. CC stopped
  correctly at the gate.
Every one caught by CC's verification, the harness, or a stop
condition, and repaired on the record. The successor holds the same
standard.

CC acts ratified this session (this-instance-only, not licences): the
item-39 isolation probes and the force-push extension probe (outside
the ruled set, safe by construction, decisive); the adjacent-file
placement of the fix-spec addendum.

## 9. COSTS (for SESSION_COSTS.md — read from /cost, never composed;
this entry is the one permitted derivation, method stated)

The CC terminal was NOT restarted after 2026-08-16, so the close
readout is cumulative over both sessions. Raw readout, transcribed:
$121.05 · API 2h 6m 8s · wall 22h 24m 5s · 7,595 added / 97 removed ·
dominant model claude-opus-5 (haiku negligible at $0.0011).

2026-08-17 row, DERIVED BY SUBTRACTION of the already-transcribed
2026-08-16 row ($33.00 · 49m 27s · +2,791/−41) from the same counter:
- $88.05 · API 1h 16m 41s · +4,804 / −56 · dominant model
  claude-opus-5 (READ from the readout — fills a column NOT SUPPLIED
  on the two prior rows).
Consistency: all four fields subtract clean; the counter cannot
include 2026-08-15 (removals would go negative, 264 > 97).
Wall time for the day is NOT SEPARABLE (the counter's wall spans the
overnight idle) — carry the raw 22h 24m 5s in the notes with the
derivation stated, per the 2026-08-15 row's precedent. NOT SUPPLIED
beats a fabricated figure if any of this is questioned.

## 10. TODAY'S SUGGESTED OPENING

Boot expects a clean tree, branch protection Active (read it via
gh api at boot — it is now part of the anchor), WS-E next 74. This
handover, the 2026-08-17 cost row, and the close queue deltas
(item 35 DISCHARGED; items 44 RCF/RGD-blocked-on-runner and 45
evaluator golden-fixture suite appended) landed in the CLOSE PR —
the successor's open is boot + verify only, no housekeeping owed.
Collect the operator's probe-evidence half at boot if available.

The natural first arc is ITEM 42 — the operator applies F1/F2 at the
terminal from the fix-spec addendum, then CC runs the full re-probe
list; a green unblocks item 27 Part B and restores trust in the client
deny surface. The strongest alternative is ITEM 12 — the inclusion
ruling is now the gate on evidential depth, and it is an operator
decision that may need no build work at all. The operator resequences
freely.
