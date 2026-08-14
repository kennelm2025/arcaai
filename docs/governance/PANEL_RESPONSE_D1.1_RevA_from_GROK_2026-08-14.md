<!-- PROVENANCE: Response received by the chair from the Grok session and
relayed via the coordination chat to this file, 2026-08-14. The chair
attests this text matches the Grok tab. Two independent chat relays of this
response were line-identical. Committed under the PANEL-ROUND CONVENTION:
verbatim, unedited below this comment block, pinned to the reviewed hash. -->

PANEL RESPONSE — D1.1 Test Plan RevA — GROK
Reviewed hash: 21a5831f27cb55b98595413c9d047c433fe590c5a6939a82e18bdf64778e8caf

FINDINGS

F-GROK-01: Coverage rule claims "fraud typologies" but the matrix is only series
  Section(s): §2.1, §2.4, Appendix A
  Severity: MATERIAL
  Finding: TOR §3:30 (as cited) requires a coverage matrix "per vertical, fraud typologies, RETRIEVAL SCENARIO CLASSES". The plan correctly notes that the manifest carries no structured typology field and therefore cannot generate a per-typology matrix (§2.4). It then substitutes document series and proceeds as if the requirement is satisfied. A series is not a typology. The instantiated set in Appendix A therefore covers series, not the fraud behaviours the TOR asked for. An auditor reading the TOR and then this plan will see the substitution and ask why the required dimension was dropped rather than deferred with an explicit gap.
  Shape of a fix: State explicitly that typology coverage is unavailable until the manifest carries the field, record it as a known gap against TOR §3:30, and do not claim the series matrix discharges the typology obligation.

F-GROK-02: Default threshold rule produces binary probes for all |E| ≤ 4 and is presented as graded
  Section(s): §5.2
  Severity: MATERIAL
  Finding: The default `ceil(0.8 × |E|) / |E|` evaluates to 1.0 for every |E| ≤ 4. The plan acknowledges that |E| = 1 is a binary probe, then applies the same rule to |E| = 2, 3 and 4 without the same honesty. Four of the seven corpus-QA scenarios in Appendix A will therefore be binary under the default, yet the plan still speaks of "recall at k" and "graded measure" language around them. This is the quantisation problem F1 exposed, now baked into the default rather than isolated.
  Shape of a fix: Extend the binary-probe declaration to every scenario whose attainable values under the default are only {0, 1}, and require the author to justify any |E| ≤ 4 as intentional rather than accidental.

F-GROK-03: Runner self-evaluates acceptance with no independent check on the evaluation code
  Section(s): §5.3
  Severity: MATERIAL
  Finding: H-8 is disposed by giving the runner both the scoring and the pass/fail verdict, then making the verdict immutable in the ledger. Immutability closes post-hoc edit attacks; it does not close a defective comparison inside the runner itself. If the threshold comparison is wrong, every Regime 2 result carries a permanently recorded wrong verdict. The plan offers no second instrument, no golden-fixture test of the evaluator, and no requirement that the evaluation logic be separately asserted. This is the same shape of risk H-9 closed for the regime marker, now accepted for the more quotable field.
  Shape of a fix: Require an independent, versioned evaluation of the threshold comparison (fixture set or separate pure function under test) before any Regime 2 run is admissible, or accept the residual risk explicitly in the plan.

F-GROK-04: Invalidation table is silent on embedding-model / chunker / index rebuild movement that leaves both content hashes unchanged
  Section(s): §9.2, §9.4
  Severity: MATERIAL
  Finding: The table treats "retrieval-snapshot hash changes, eligible-set unchanged" as the processing-drift row. If the snapshot hash is computed over absent or incomplete processing facts (the caveat already admitted at §9.4), an embedding-model bump, chunker-parameter change, or full index rebuild can leave both content hashes identical while changing every retrieval result. The plan records the caveat but does not give the operator a row that fires when processing facts are present and have moved. The strongest practical argument the plan itself makes for closing the corpus-side processing obligation is left without an operational consequence.
  Shape of a fix: Add an explicit row (or strengthen row two) that fires on any change to recorded processing facts when those facts are present, and state that the current caveat makes row two provisional until the obligation is closed.

F-GROK-05: Appendix A instantiates only 11 scenarios and leaves citation-following and gap-detection sparse relative to the coverage rule
  Section(s): §2.1, Appendix A
  Severity: MINOR
  Finding: The coverage rule requires every class × every series. Appendix A supplies seven corpus-QA (one per series), two citation-following, and two gap-detection. Citation-following covers only two of seven series; gap-detection is bound to the two planted defects rather than to series. The rule is therefore only partially instantiated. The plan does not state whether the missing class×series cells are deliberate exclusions (with reasons) or simply not yet filled. A regenerable appendix that under-generates the rule it claims to implement is a silent relaxation.
  Shape of a fix: Either add the missing cells or list them as named exclusions with reasons so the appendix is complete against the rule.

F-GROK-06: B7 mapping correctly records the gate's silence, then leaves the consequence unowned
  Section(s): §7.3, Appendix B
  Severity: MINOR
  Finding: The plan correctly observes that B7_GATE.md is silent on the harness and on D1/D2, and routes the gap to the B7-exit ruling pack. That is honest. What is missing is any statement of whether the Test Plan can be accepted while that silence remains, or whether Regime 2 evidence for "preferred-primary" items is usable at B7 exit before the gate document is updated. The boundary is drawn; the operational implication is not.
  Shape of a fix: One sentence stating that preferred-primary harness evidence remains usable under the existing B7 text via the substitution route already defined at §7.2, or that it is not, until the gate is amended.

F-GROK-07: Formal-execution pack entry criteria 2–5 are declared machine-asserted with no assertion interface named
  Section(s): §8.1
  Severity: MINOR
  Finding: H-10 is cited as moving the three non-pre-flight obligations to machine assertion. The plan restates the claim but does not name the instrument, the command, or the failure mode that blocks session entry when any of 2–5 is false. Pre-flight has a concrete script and exit-code contract; the others do not. "Machine-asserted" without an assertion surface is still a human obligation with better rhetoric.
  Shape of a fix: Name the assertion mechanism (or explicitly defer the interface to the runner build) so the claim is testable.

DISSENTS

None that rise above the findings above. The operator rulings of 2026-08-14 are implemented faithfully; the problems are in the engineering consequences of those rulings, not in a refusal to follow them.

CONFIDENCE AND LIMITS

- I could not verify the cited TOR clauses, rulings-record passages, or schema definitions against primary sources; claims that rest on those citations are assessed for internal coherence only.
- I have not seen the actual manifest or the scenario-spec schema file; series membership and eligible-set counts are taken as stated.
- The regulatory seat (Mistral) is unfielded; this response carries no EU AI Act / DORA / PRA SS1/23 lens and must not be read as supplying one.
- Whether the runner's current code already implements the H-8 evaluation path is outside the document; the finding addresses the plan's allocation of responsibility, not the present implementation state.
