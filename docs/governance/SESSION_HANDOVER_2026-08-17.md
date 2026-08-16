# ARCAAI CHAT HANDOVER — 2026-08-17 (morning)

For the successor coordinator chat. Covers the state at close of the
2026-08-16 session — the session that took D1.1 from RevB through a
second review round and a delta round to ACCEPTANCE, plus a runner
spike. Registers are the authority; this handover is narrative. Where
this document and a live read disagree, the repo wins.

Companion state on D:\Downloads: the accepted RevC and its acceptance
record and four returns (all committed, paths below); the artefact
custody folder D:\ArcaAI-artefact-custody\2026-08-16-spike-2\.

---

## 1. REGISTER STATE (verify live at boot)

DEC next 0018 · ADR next 0011 (reserved, unconsumed) · CL next 31
(29 and 30 both consumed 2026-08-16) · WS-E next 72.

HEAD at close: merge commit 9027584 (PR #134). Verify against a
freshly regenerated manifest at boot — do not trust this line, read it.

## 2. HEADLINE: D1.1 TEST PLAN ACCEPTED

D1.1 is ACCEPTED at RevC (hash
9d6ab3b0da21d5e6603f7fa505d48a892da9acf11dba60725b83e5a8c590e88c).
This closes the critical-path head that stood since Thursday:
RevB -> round 2 -> acceptance. D1.1 is out of DRAFT status; the TOR
precondition "ruled ACCEPTED by the panel process" is SATISFIED; the
§5A:101 post-acceptance amendment route is OPEN.

Key artefacts, all committed under docs/governance/:
- D1.1_TEST_PLAN_DRAFT_RevC_2026-08-15.md (the accepted text; filename
  still says DRAFT — cosmetic rename owed, see §5)
- D1.1_REVC_ACCEPTANCE_2026-08-16.md (the ruling + 9-verdict table)
- DELTA_RETURN_D1.1_RevC_from_{GROK,CHATGPT,DEEPSEEK,GEMINI}_2026-08-16.md
- D1.1_ROUND2_DELTA_CIRCULATION_2026-08-16.md (the delta pack)
- D1.1_PANEL_ROUND2_DISPOSITION_2026-08-15.md
- Four round-2 panel responses (RevB), committed 2026-08-15

## 3. WHAT LANDED 2026-08-16 (all merged to main)

- PR #130 — RevC delta circulation pack authored, first committed pack
  of its kind; acceptance rule landed in-tree.
- PR #131 — D2.2a runner spike 2 Commissioning Session Record; CL-29.
- PR #132 — section-15 custody-hash correction (a file hash had been
  cited where a payload hash sat; caught at first use of the custody
  table, before the preservation copy).
- PR #133 — delta pack window amendment (24h -> same-day; send-time
  slot ruled record-only).
- PR #134 — RevC ACCEPTANCE: four delta returns + acceptance record +
  CL-30 + CL-29 re-pin to the corrected record hash 84738dc4....

## 4. THE DELTA ROUND (how acceptance was reached)

Because RevC already carried every ruled round-2 fix, a full re-review
was unnecessary. A LIGHT DELTA ROUND asked each reviewer to verify
only whether RevC's text discharges their own residual MATERIAL(s):
DISCHARGED / NOT DISCHARGED against the CHAIR'S ADOPTED remedy (not the
reviewer's proposed one), dissent routed separately, no whole-document
re-review, no new findings except a defect in a fix.

OUTCOME: 9/9 DISCHARGED, zero dissents, zero defects-in-fix.
- Grok: F-GROK-08, F-GROK-09 — both DISCHARGED.
- ChatGPT: R2-01 — DISCHARGED (hash independently recomputed).
- DeepSeek: F-DS-10, F-DS-11 — both DISCHARGED; also self-verified its
  six MINORs as landed. Left a runner-build note: the material-
  parameter list must include SEARCH-TIME params (ef_search), not just
  index-build params.
- Gemini: F-GEM-REG-01/02/03/04 — all DISCHARGED, verified against the
  adopted remedies. NOTE FOR THE TRAIL: Gemini's first two responses
  were document summaries with no verdicts, rejected as non-responsive;
  verdicts came on a third, strict fill-in-template prompt. The non-
  response machinery was NOT needed. If circulating to Gemini again,
  use a verdict-template prompt from the outset, not a prose brief.

## 5. THE D2.2a RUNNER SPIKE (2026-08-16, item 30, Commissioning)

A throwaway shakedown of the runner machinery, Regime 1 throughout
(all results permanently inadmissible). Discharged DEC-0017's build-
lane arc. What it proved and found:

- REPRODUCIBILITY PROVEN: four identical runs of RQA-107, one differing
  field (generated_at_utc, run-metadata), raw scores exactly equal.
- RULED: the D3.1 golden-baseline door keys on the COMPARABLE-CONTENT
  hash (aeed2757...), not the raw file hash. Run 1 (56ab9ac5...) is the
  first candidate baseline; preserved to
  D:\ArcaAI-artefact-custody\2026-08-16-spike-2\ (6/6 verified at
  destination against the corrected record).
- ELEVEN UNHONOURED RevC requirements found and recorded, none hidden:
  SIX runner-side — evaluator_version (4th identity leg),
  environment_config_sha256 in result, material_parameter_list_sha256
  in result, confound:single_chunk marker, session_status:halted (no
  abort path exists in runner.py), invalidation_status.
  FIVE spec-side — the four CARRIED-NO-FIELD items (absolute top_k cap,
  binary-probe justification, Obligation D justification, density-
  stratified note) + the unverifiable typology identifier. Fix route
  for all five: schema v0.3 (v0.2 is immutable, additionalProperties:
  false, predates every round-2 fix).
- Result of record (observed, not chased): recall_at_k 0.0; a 16-chunk
  statute retrieved while both 1-chunk expected statutes were missed —
  strengthens the §12.3 single-chunk confound hypothesis. Commissioning,
  so observed-not-raised.
- Item 32 / F7 (PYTHONIOENCODING=utf-8 renders the em-dash banner)
  CONFIRMED fixable at harness entry, evidenced.

## 6. THE PROBE INSTRUMENTS — RETIRED (clean tree)

The two dispatch-probe instruments (route B agent; frontmatter-
disambiguation skill, disarmed) were RETIRED UNFIRED on 2026-08-16,
deleted at the operator's terminal (.claude/ writes have no in-session
route — deny is absolute). The CC PROMPT 93 tolerance and its terminus
(was: next session or 2026-08-22) are DISCHARGED by retirement, ahead
of the outer bound. Tree is CLEAN OUTRIGHT at close — the first time
this session. Owed-list item 4c (subagent/skill routing through
PreToolUse) remains OPEN and unprobed; instruments cheap to rebuild if
taken up.

The next boot should NOT stop on a dirty tree.

## 7. THE OWED LIST (verify against a live queue readback)

Critical path, now UNLOCKED by acceptance:
1. Schema v0.3 — likely the first authoring act. The spike found five
   RevC requirements v0.2 cannot hold; every scenario authored against
   v0.2 carries CARRIED-NO-FIELD baggage until v0.3 lands.
2. Scenario authoring — RQA-101..107, RCF-101..106 (per-series after
   E1), RGD-101..102. RQA-107 has a commissioning-draft spec already
   (5bad9660..., held in custody, against v0.1). RQA-107 carries its
   F1-independence design record per DS-06. RGD/RCF need capability the
   runner lacks (abstention signal; edge traversal) — spike confirmed.
3. Evaluator golden-fixture suite — §8.1 entry criterion; contract
   defined (F-GROK-09 fix), ownership OPERATOR. Blocks Regime 2.
4. Runner work — the six runner-side unhonoured items from §5, incl.
   DeepSeek's ef_search note on the material-parameter list.
5. M13 standards register -> M12 first audit cycle (Prompt 21 reserved,
   rider on disk; after Test Plan acceptance [now done], before
   Regime 2).
6. Item 33 ruling pack + B7_GATE.md sync (before first gate exit).
7. TOR §5A:101 amendment — the three-leg identity statements (first
   customer of the now-open route, per F-GROK-08's deferral).

Also owed:
- WS-E 71 IDENTIFICATION — surfaced 2026-08-15 (manifest said next 72,
  handover said next 71); never chased. One tail-read of
  WS-E_INCIDENTS.md identifies what 71 is.
- Guard false-red on a read-only command naming a protected path
  (WS-E-shaped, unraised; WS-E next 72 free).
- RevC filename DRAFT-drop (cosmetic; content is accepted, filename
  lags).
- Gemini standing primer — seat permanent now; still no committed
  primer (round-2 pack §8 item 3).
- Vector-store ownership repair (operator's ten minutes; oldest single
  item on the board).
- Embedder decision record (before Regime 2; free now, expensive
  later).
- Corpus inclusion decision (item 12; SG-03..09; eligibility 16->23).
- Default-mode discriminator re-run; shell-branch anchoring fix
  (WS-E 70); pin-value pre-run assertion (the rehash sweep is vacuous
  at 0 pins — first real pin activates this); coverage-source widening
  ruling (76.33% excludes the platform package; fail_under decision
  owed).

## 8. COORDINATOR-CHAT CONVENTIONS (binding on the successor)

- Every instruction to CC ships as a NUMBERED CC PROMPT block. Anything
  that instructs an act gets a number; only pure information ("merged",
  a file path) travels bare. Tally: prompts through 107 consumed across
  2026-08-15/16. NEXT IS 108.
- NAME THE TOOL for every act in a prompt (Read/Write/Edit/Bash), and
  mark operator-only acts (browser merge; .claude/ writes) as such.
- Payloads move as FILES (write -> present -> operator downloads to
  D:\Downloads -> CC reads from disk), IN BOTH DIRECTIONS — CC's stop
  reports too. The chat truncated repeatedly across both sessions; a
  prompt too long to paste goes out as a file. Full hashes on their own
  lines.
- Panel returns land DISK-FIRST: coordinator writes each return to a
  file with a provenance header, operator downloads, CC reads and lands
  from disk. Do not have CC transcribe from the chat.
- Both-halves evidence: CC's in-harness result + operator's terminal
  observation, separately attributed, never merged. Silence != pass;
  a non-zero exit is reported as itself, not folded into a green.
- Decline ALL don't-ask-again offers. Verify from the artefact, never
  the report — including the close's own writes and the coordinator's
  own memory (coordinator memory is not a register; neither is
  coordinator sight — it sees only what arrives).
- gh pr merge is an UNCONDITIONAL ASK — the operator merges in the
  browser (the designed route). CC opens the PR and stops.
- Gmail progress summary to drafts at session close / before breaks
  (standing rule). Format: plain English; costs block at the bottom
  carrying this session + a running multi-session total.

## 9. COORDINATOR ERRORS (owned, for calibration)

2026-08-15: prompt misnumbering (22 for 80); stale dissent count
propagated from a handover (two -> four, corrected by CC via the CL-24
pattern); asserted a file's existence without verification
(BOOT_NOTES on disk — it wasn't); issued landing prompts against
response files that did not yet exist on disk.
2026-08-16: an unfilled [OPERATOR: state...] placeholder shipped in a
prompt; a wrong artefact count (five written, six enumerated); a stale
hash citation directed into a ledger entry (caught by CC before it
pinned a false value); a gate ordering conflict baked into a prompt
(criterion 3 required a spec the same prompt reserved the choice of).
Every one caught by the harness or CC's verification and repaired on
the record. The successor holds the same standard.

## 10. COSTS (for SESSION_COSTS.md transcription — read from /cost,
never composed)

Two distinct sessions, two entries:
- 2026-08-15 (RevB + round 2 + RevC): $41.66, API 54m 57s, wall
  18h 7m (spans the overnight gap), 4,008 added / 223 removed.
- 2026-08-16 (D2.2a spike + delta + acceptance): $33.00, API 49m 27s,
  wall 4h 4m, 2,791 added / 41 removed.
Prior for context: 2026-08-14 paper-landing $8.43; afternoon marathon
$79.89. NOT SUPPLIED beats a fabricated figure if a /cost readout is
lost.

## 11. TODAY'S SUGGESTED OPENING

Boot on a clean tree (no probe stop expected). Arc naming is the
operator's at step 7. The natural first arc is SCHEMA v0.3 — it
unblocks scenario authoring without CARRIED-NO-FIELD debt, and it is
the direct product of the spike's five spec-side findings. Scenario
authoring follows. The operator resequences freely; DEC-0017 gives the
build lane right of way but the test-capability critical path is now
the live front.
