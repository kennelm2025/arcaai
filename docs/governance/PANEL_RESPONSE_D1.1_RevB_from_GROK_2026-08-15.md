# PANEL RESPONSE — D1.1 Test Plan RevB — GROK

**Round 2 · Received 2026-08-15**
**Reviewed hash:** `68270febf4a8ff092112e4adc8b0696c316e99053ac38e8e48cc5f2d007818dd`

*Provenance: received via the coordinator conversation 2026-08-15 and
transcribed verbatim by the coordinator; transported to disk by the
operator. Chain of custody runs through the coordinator layer, not
directly from the reviewer interface.*

---

```
PANEL RESPONSE — D1.1 Test Plan RevB — GROK
Reviewed hash: 68270febf4a8ff092112e4adc8b0696c316e99053ac38e8e48cc5f2d007818dd

CARRIAGE CHECK (own round-1 findings first)

F-GROK-01 (typology vs series): Carried faithfully via F-DS-04 composite. §2.4 now states the matrix is PROVISIONAL against TOR §3:30, that a Regime 2 run is NOT evidence of typology coverage, and that series ≠ typology. Discharged as-subsumed. Clean.

F-GROK-02 (binary probes for |E|≤4): Carried. §5.3 extends the binary-probe declaration to every scenario whose attainable values under the default are only {0,1}, withdraws graded-measure language from those cases, and requires justification for |E|≤4. Clean.

F-GROK-03 (runner self-evaluates with no independent check): Carried as fixture route. §5.7(a) and §8.1 criterion 6 require a versioned golden-fixture suite GREEN before any Regime 2 run. Clean.

F-GROK-04 (no row for processing-fact movement when facts present): Carried. §9.2 row 2 strengthened, marked PROVISIONAL, and "recorded processing facts" explicitly limited to the three fields the snapshot hash covers (§6.4). Clean.

F-GROK-05 (Appendix A under-instantiated the stated rule): Carried via the restated class-specific obligations and the now-complete Appendix A (15 scenarios, named exclusions). Clean.

F-GROK-06 (B7 silence left unowned): Carried. §7.3 now states the operational implication. Clean.

F-GROK-07 (machine-asserted without named surface): Carried. §8.1 now requires a named surface or explicit deferral for all six criteria. Clean.

All seven of my round-1 findings are present, correctly severity-preserving, and mapped in Appendix C. No silent narrowing or loss.

FINDINGS

F-GROK-08: Evaluator-version as fourth identity leg is asserted without a migration path for existing statements of the triple
  Section(s): §6.8, §9.2 row 7, cross-refs to TOR §5:74 / §8:124
  Severity: MATERIAL
  Finding: The plan correctly carries the structural option from F-DS-03 and makes evaluator version a fourth leg of the reproducibility identity. It does not, however, state how the many existing statements of "the triple" (spec + model + corpus snapshot) are to be read after this change, nor whether TOR text that still says three legs is now stale. A reader (or later instrument) that still expects three legs will silently drop the fourth. The addition is real; the migration of the surrounding language is not.
  Shape of a fix: Explicitly declare the identity now four-legged, list every prior three-leg statement that is superseded, and require any remaining three-leg reference to be treated as incomplete.

F-GROK-09: Golden-fixture suite is an entry criterion whose failure mode and ownership are still underspecified
  Section(s): §5.7(a), §8.1 criterion 6, Appendix B item 13
  Severity: MATERIAL
  Finding: The suite must be GREEN before Regime 2, which is correct. The plan does not define what "GREEN" means in observable terms (exit code? coverage of the quantisation boundary cases? both pass and fail shapes?), who owns the suite's currency when the threshold rule itself changes, or what happens if the suite and the live evaluator diverge after a runner change. An entry criterion without a crisp failure signature is still partly aspirational.
  Shape of a fix: State the minimal fixture contract (known inputs, known verdicts, both polarities, quantisation points) and the ownership/refresh rule when §5 thresholds move.

F-GROK-10: Coverage obligations are now honest, but the typology vocabulary remains an unowned external dependency that can still make per-scenario typology declarations non-computable
  Section(s): §2.4, Appendix B items 1–2
  Severity: MINOR
  Finding: The PROVISIONAL label and the vertical-side vocabulary requirement are correctly stated. The plan still has no interim mechanical check that two specs declaring "card-not-present" and "CNP fraud" are treated as the same typology. Until the vocabulary artefact exists, coverage assessment at spec level is still string-equality and therefore fragile. This is acknowledged but not mitigated.
  Shape of a fix: Either supply a minimal interim controlled list inside the fraud vertical or require the scenario author to reference a stable typology identifier even before the full artefact lands.

F-GROK-11: Appendix D items are correctly held, but item 2 (RQA-107 covering a 16× density range) is a latent coverage defect the obligations do not catch
  Section(s): Appendix D item 2, Appendix A.1
  Severity: MINOR
  Finding: One corpus-QA scenario is asked to cover four statute documents whose chunk counts are 1, 1, 7 and 16. The coverage obligations treat series as uniform. They are not. A single scenario can satisfy the letter of Obligation A while being information-theoretically incapable of exercising the density extremes. The plan records the observation and holds it; that is honest, but the obligation itself remains blind to intra-series heterogeneity.
  Shape of a fix: Either split the statute series for coverage purposes or require an explicit density-stratified note when a series spans more than a defined chunk-count ratio.

DISSENTS

None. The chair's round-1 dispositions and the five Appendix E rulings are implemented as ruled. I do not dissent from the carriage.

CONFIDENCE AND LIMITS

- Hash stated in the pack is accepted as the governing value; I cannot recompute the blob in this session but treat the post-merge confirmation claim as the operator's responsibility.
- I have not re-verified the live manifest numbers or the EDGES.yaml claims; series membership, edge existence and the 71-chunk denominator are taken as stated.
- Regulatory lens is now Gemini's primary brief; this response deliberately carries no EU AI Act / DORA / PRA SS1/23 substance and must not be read as supplying it.
- The runner implementation state (whether the fixture suite or environment pin already exists) is outside the document; findings address the plan's requirements, not current code.
```
