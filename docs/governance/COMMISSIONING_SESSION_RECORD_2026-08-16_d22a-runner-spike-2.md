# COMMISSIONING SESSION RECORD — D2.2a runner spike, arc 2

*This is a **record**, not a report. It carries no pass/fail summary. Under the
D2.0 commissioning frame, everything recorded here is **permanently inadmissible
as gate evidence** and cannot be promoted retroactively. The naming is
deliberate: a report format invites promotion by osmosis. Second instance of the
form, after
`docs/governance/COMMISSIONING_SESSION_RECORD_2026-08-13_d22a-runner-spike.md`.*

- **Date:** 2026-08-15 · **Regime:** COMMISSIONING · **Arc:** queue item 30, the
  D2.2a runner spike proper, under DEC-0017 build-first right of way
- **Register anchor:** `REPO_MANIFEST.md` regenerated this session, 2026-08-15
  12:54 UTC — DEC next 0018, ADR next 0011, CL next 29, WS-E next 72,
  **0 divergences**. That next-free number is **claimed by this arc as CL-29**;
  see the register note below
- **Base:** `c7881f8`, merged `main` after PR #130
- **Runner exercised:** `arcaai/harness/runner.py` at `0.1.0-commissioning`,
  unmodified by this arc

**Register note — CL-29 IS CLAIMED, and its ledger entry lands in the same pull
request.** Queue item 30 says the arc claims the next free CL number, and the
operator ruled the claim on 2026-08-16. **CL-29** is that number. It was stated
before being consumed, per the standing rule, and checked two ways rather than
taken from the anchor alone: the session manifest reads CL highest 28, next 29,
and the ledger itself holds CL-01 through CL-28 contiguously plus CL-E1, so the
sequence-hold rule (highest + 1, only) gives 29 and no other number.

**The claim is consummated here rather than promised.** A CL claimed in a record
whose ledger entry does not exist would put
`docs/governance/GOVERNANCE_REVIEW_CHANGELOG.md` — canonical for CL items — out
of step with the narrative register, which is precisely the divergence class the
manifest scanner exists to catch. The entry therefore travels in the same commit
as this record, not behind it.

*Date note: the arc executed on 2026-08-15 and the record is dated 2026-08-16 in
its filename and its CL entry, on the operator's ruling. Both dates are stated
rather than reconciled, because a record whose apparent date differs from its
execution date should say so in its own text.*

## 1. Exit criterion — stated before the evidence

**The scenario's own pass/fail is NOT an exit criterion. Reproducibility IS.**

Queue item 30 fixes the exit criterion as a result JSON reproducible from its
triple. RQA-107 scored `recall_at_k` 0.0. That is recorded as the result of
record, not as a failure of this spike, and nothing was tuned toward a match.

## 2. Rulings, verbatim

**Ruling 1 — arc naming (operator, CC PROMPT 96).** Discharges the
`/session-open` arc-selection task and the DEC-0017 arc-selection step.

> "this session's arc is ITEM 30 — the D2.2a runner spike. Minimal runner + ONE
> retrieval scenario end-to-end, COMMISSIONING (Regime 1) throughout: every
> result permanently inadmissible, and every artefact this arc produces states
> that in terms."

**Ruling 2 — entry-gate ordering (operator, CC PROMPT 97).**

> "the criterion-3 ordering conflict is resolved as you proposed. The gate
> completes in the order choose → draft → validate; criterion 3 discharges when
> the drafted spec validates against v0.2. The conflict was a defect in CC
> PROMPT 96's drafting, coordinator-owned, recorded."

**Ruling 3 — scope (operator, CC PROMPT 97).** The governed-store pin writer
(queue item 13 / CL-25) remains OUT of scope. The manifest pin is the pin of
record for this spike, and the two senses of "pin" stay distinct in this record.

**Ruling 4 — scenario (operator, CC PROMPT 98).** RQA-107 approved as proposed,
with E, the binary-probe declaration, the threshold, `top_k`, the marginal-case
exclusion and both required justifications as recorded at section 5.

**Ruling 5 — field-less items (operator, CC PROMPT 98).**

> "the four field-less items are CARRIED IN description, each on its own line
> under the machine-findable prefix CARRIED-NO-FIELD: so a future v0.3 migration
> can locate every spec that carried content this way by grep."

**Ruling 6 — execution (operator, CC PROMPT 99).** RQA-107 executed twice under
Commissioning, every output stating its inadmissibility.

**Ruling 7 — the D3.1 baseline key (operator, CC PROMPT 100).**

> "the D3.1 golden-baseline door keys on the COMPARABLE-CONTENT hash
> (aeed2757...09ef), not the raw artefact hash; run 1 (56ab9ac5...) is the
> candidate baseline under that key."

## 3. Entry criteria — four evidence lines

The gate completed in the order **choose → draft → validate** under Ruling 2.
The conflict was real: criterion 3 requires a chosen scenario's spec, and
choosing the scenario was an operator stop later in the same instruction, so the
gate could not close in the order written.

| # | Criterion | Evidence |
|---|---|---|
| 1 | Pre-flight GREEN | `scripts/d22a_preflight.py` 4/4 GREEN, exit 0. Non-elevation corroborated by two independent methods, integrity label `S-1-16-8192`; cache traversal read 4096 bytes from `model.onnx` across 6 files; services — both containers up, port 5432 reachable, vector store exists, readable and writable; env identity arcaai, Python 3.11.15 |
| 2 | Corpus snapshot pinned and stated | Computed live through the DEC-0014 machinery, not from a summary and not from the prior spike's recorded values. Full pin set at section 4 |
| 3 | Scenario spec schema-valid against v0.2 | 0 errors through the runner's own validation path, paired with four deny-shaped mutations. Section 6 |
| 4 | Working tree state recorded | `c7881f8`, **DIRTY BY RULING** — see below |

**Criterion 4, stated in full because "clean" would be false.** The tree carried
two untracked paths throughout: `.claude/agents/probe-route-b.md` and
`.claude/skills/probe-route-a2/SKILL.md.disarmed`. They are staged
dispatch-probe instruments, owed work rather than residue, tolerated for this
session by operator ruling with a **terminus at the earlier of the next session
open or 2026-08-22**. Route B is confirmed never fired. Neither was touched,
edited, committed or dispatched. Nothing else was dirty at any point in the arc.

## 4. The pin set, and the two senses of "pin"

Computed by calling `parse_manifest`, `manifest_sha256`,
`retrieval_snapshot_sha256` and `eligible_set_sha256` from
`arcaai/platform/governance/corpus.py` — the same functions the runner
recomputes with, so these are the values a spec is verified against.

```
manifest_version          2026-08-13.8
manifest_sha256           2d5f2fb5ea6051167d89dc83aa70e1330f2cace212156a8a5014d98e7803809c
retrieval_snapshot_sha256 878b3439e8261e850510c7ea7b5d0e67655ee2eb3b34427a8d7c2b256d6ab928
eligible_set_sha256       bfcdfe66feaad3c83872f71cd4033bc4b2d6c80ab627c2909b79915e149cf339
documents                 30 total, 16 eligible, 71 indexed chunks
```

**The manifest moved since the 2026-08-13 spike and one hash did not.** That
spike pinned `2026-08-06.7` / `97ca36dd…`; documents went 23 to 30 while
eligible stayed at 16, the SG listing act having landed seven documents that are
not retrieval-eligible. `retrieval_snapshot_sha256` is **byte-identical** to the
prior spike's, which is correct rather than stale: the hash covers the eligible
set and its processing facts, and neither moved. Recorded because an unchanged
hash across a changed manifest reads as an error until the reason is stated.

**The v0.2 schema's KNOWN LIMIT does not bite on this snapshot.** The schema
warns that the pin computes cleanly over absent processing facts — "a required
pin with nothing behind it". Checked directly: **16 of 16 eligible documents
carry a processing block, with `chunker_version`, `embedding_model` and
`chunk_count` each populated 16 of 16.** The pin has real content here. This is
evidence bearing on queue item 31, for this snapshot only, and is not a general
finding about the pin.

**The two senses of "pin" are different things and are kept apart.** The
*manifest* pin above exists and is the pin of record. The *governed-store*
`corpus_version` row does **not** exist — the rehash sweep read 0 pinned rows
this session — and the runner writes no database rows at all. This spike
therefore did not create a first real pin, and could not have without the pin
writer, which Ruling 3 placed out of scope.

## 5. Scenario authoring — RQA-107

Chosen from Rev C Appendix A.1, Obligation A, the Statute series slot. Class
`retrieval`, kind `corpus_qa`, scoring `semantic_distance`.

**Query, fixed at authoring:** which provisions of the Fraud Act 2006 create the
offences of fraud by false representation and fraud by abuse of position, and
what must be proved for each.

**Expected set E = OGL-0001, OGL-0002. `\|E\|` = 2.** OGL-0001 is Fraud Act 2006
s.2 at 1 chunk; OGL-0002 is Fraud Act 2006 s.4 at 1 chunk. Both necessary, each
grounding one limb of a two-limb question; both sufficient, each stating the
statutory text creating its offence. Read from the live manifest.

**Rev C §5.2 criterion 4 — FIRST LIVE DISCHARGE.** E was fixed at authoring,
recorded in the spec, and stated in the transcript **before any retrieval was
run for this scenario**. The criterion has existed as plan text since Rev A; this
is the first occasion on which a scenario has been authored under it and the
ordering evidenced rather than asserted.

**Why this scenario.** It is the only Appendix A slot that exercises the round-2
fixes — the Obligation D justification (`F-DS-10`), the density-stratified note
(`F-GROK-11 + F-DS-14`), the binary-probe declaration (`F-GROK-02`) and the
`top_k` cap (`F-GEM-REG-02`) all bite here and nowhere else, every other series
sitting at or below a 1.33x density ratio. It is also the only slot that can fire
the `confound: single_chunk` marker. The other two classes were ruled out on
capability rather than preference: gap detection needs an abstention signal
nothing in the system can produce, and citation-following would have run as a
corpus-QA query wearing a citation label, since the runner does not traverse
edges.

**Binary probe: YES**, `\|E\|` at 2 is at or below 4, so attainable values are
exactly 0 and 1. Default threshold `ceil(0.8 x 2)/2 = 1.0`, derived from §5.3's
formula. No precision-or-rank criterion is owed; §5.4's obligation begins at 5.

**`top_k` = 5** — 7.0% of 71 indexed eligible chunks, unflagged. 7 is the
unflagged ceiling; 5 was chosen because it is the harder window and because the
2026-08-13 run used 5, keeping the two comparable for the D3.1 door.

**Marginal-case record (§5.2).** SYN-TY-01 and SYN-TY-02 discuss false
representation and are excluded from E: a document that mentions the subject is
not grounding it. Recorded because the 2026-08-13 spike observed SYN-TY-02
ranking above the statute for a statute question, making this the exclusion most
likely to be argued with.

**The `F-DS-06` authoring rule, discharged rather than asserted.** The threshold
was derived mechanically from §5.3's formula. It was not chosen with F1's
outcome in view, and the scenario was not selected in order to re-run F1.

## 6. Validation — both halves

Validated through the runner's own `load_and_validate_spec`, so the path is the
one the run would take rather than a re-implementation of it. The runner's schema
registry was printed, so the schema actually applied is evidenced.

**Allow-shaped:** VALID against v0.2, 0 errors. `\|E\|` 2, `top_k` 5, acceptance
`recall_at_k >= 1.0`, all three snapshot pins present, description 1,942 of 2,000
characters carrying four `CARRIED-NO-FIELD:` lines.

**Deny-shaped, four mutations, all refused with the fault named:**

| Probe | Fault injected | Outcome |
|---|---|---|
| D1 | drop `retrieval_snapshot_sha256` | REFUSED exit 2 — `$.corpus_snapshot :: required :: 'retrieval_snapshot_sha256' is a required property` |
| D2 | `schema_version: "9.9"` | REFUSED exit 2 — "unreadable version, not an invalid spec"; names known versions 0.1, 0.2 |
| D3 | `schema_version` removed | REFUSED exit 2 — refuses rather than defaulting, because a default would make the runner decide which rules applied |
| D4 | `generator_seed` on a retrieval-class spec | REFUSED exit 2 — rejected against `{'required': ['generator_seed']}` |

**D1 is the schema discriminator and is the load-bearing probe.** That same spec
**passes** under v0.1, where the field is optional. Its refusal is positive
evidence that **v0.2 was the schema applied**, not merely that some schema was —
which no passing spec could establish. The allow-shaped pass alone would have
been satisfied by a dead validator.

**Observation on D4's legibility.** The v0.2 schema justifies the `not`/`required`
form over a false subschema on the ground that it "names it". It does — but only
after dumping the entire instance, roughly 3KB, with the field name at the very
end. The claim holds; the ergonomics are worse than the comment implies.
Recorded as an observation, not a defect claim.

## 7. Environment identity — the first material-parameter list

Authored this arc as a runner-build artefact, per the `F-DS-11 + F-GEM-REG-04`
composite fix at Rev C §9.5 element 3.

**Two hashes, deliberately, not one.** A single hash over values cannot detect a
narrowing of the *definition*, which is the failure mode R2-5 names when it says
the list would otherwise "become a place to quietly narrow the definition". So
the list's own hash covers what counts as material, and
`environment_config_sha256` covers the observed values.

**Material, by the ruled test** — affects similarity computation, retrieval
algorithm, or search-space pruning. Nine parameters, all read from the live
collection, **zero UNKNOWN**: `embedding_model` all-MiniLM-L6-v2;onnx;chromadb==1.5.9;
`embedding_dimension` 384, measured rather than looked up; `distance_space`
cosine; `index_algorithm` hnsw; `hnsw_ef_construction` 100; `hnsw_max_neighbors`
16; `hnsw_ef_search` 100; `chunker_version` para-pack-v1;target=220w;cap=380w;
`indexed_chunk_count` 71.

**Explicitly NOT material, named so the exclusion is visible rather than
implied:** `hnsw_num_threads`, `hnsw_batch_size`, `hnsw_sync_threshold` as
resource allocation; `log_level` as logging; `persist_directory` as resource
location rather than retrieval behaviour.

Three-outcome discipline was built in: an unreadable parameter would have been
recorded as UNKNOWN inside the hashed payload, so the hash would state its own
gaps rather than silently omit them. No parameter took that path on this run.

## 8. All eight hashes

```
5bad9660c7f8d5ebb3b04cfa5297651474770466444042f22ef9a90d4aeda0a3
a3cd6bdaf48e2770ae30598606b5986ca22d0f1f61f2eb67f741661e785c0ba2
efa3f537b4d5432a241fe1a52d6c521fac5c1f54b2308f0f062f44dcf34f0267
56ab9ac59c989f62e5117941d95e4265187b12984024b9954832564e2a112080
3172ce61283c46f264de2304a8de9ba5410bbae820603d016b17e991232cef92
c851012e2601e6edf402239ef94cde69a698337c9a41b5f9e68cda3abc1762cd
d5928958ede74dc7de9fe3249b0d025047313cd033618e7e34681efba9ea3637
aeed275708bd4b67900d37c763479beb19fe96644ac58bf72aba371624a209ef
```

In order: the RQA-107 spec; the material-parameter list definition; the
environment config over observed values; the run 1, run 2, run 3 and run 4 raw
result artefacts; and the comparable-content hash, which is **the same value for
all four runs**.

## 9. Runs and reproducibility

Four runs, same spec, same manifest, same index, nothing changed between them.
Runs 3 and 4 were byproducts of the failed abort probes at section 11; they were
identical invocations against unchanged inputs, so their agreement is real
evidence and is kept rather than discarded.

**REPRODUCIBLE: YES.**

**The raw files are NOT byte-identical, by construction rather than by defect.**
Diffed externally, not read off the runner's printed self-report, because a
component checking its own claim proves little: **exactly one field differs
across the whole artefact — `generated_at_utc` — and it classifies as
RUN-METADATA.** Every identity-relevant field is identical.

**The raw float scores compare exactly equal, with no rounding applied.** That is
affirmative evidence for the `bit_identical` migration-diff comparison the spec
declares, rather than merely being consistent with it. Its limit is stated: four
runs, one scenario, one machine, one session, index unchanged throughout. It is
not a determinism guarantee for the vector store and must not be cited as one.

The comparable-content hash was **recomputed independently** of the runner and
matches each artefact's embedded self-report in all four cases.

**D3.1 golden baseline, under Ruling 7.** The door keys on the comparable-content
hash `aeed2757…09ef`; run 1, raw `56ab9ac5…`, is the candidate baseline under
that key. The reason the key matters: a raw-file baseline can never match a later
run, because the timestamp guarantees a difference. Content-addressed
comparability already exists in the artefact and the door should use it.

## 10. Result of record

`recall_at_k` **0.0**. Retrieved 5 chunks over 5 documents — SYN-DP-01,
SYN-TY-02, SYN-DP-02, SYN-TR-02 and OGL-0004. Matched: none. **Acceptance NOT
EVALUATED**, the comparison deliberately left unmade under the commissioning
frame. **Permanently inadmissible as gate evidence.**

**Density observation, observed and not chased.** A statute *was* retrieved —
OGL-0004, Proceeds of Crime Act 2002 s.330, **16 chunks** — while both expected
Fraud Act documents, **1 chunk each**, were absent. That is the
density-stratified note's concern appearing in live data from the opposite
direction to the one anticipated, and it strengthens rather than weakens the
single-chunk confound hypothesis at §12.3. Under the D2.0 frame anomalies are
observed, not raised. It was not investigated, and no parameter was changed in
response to it.

## 11. The halted probe — INDETERMINATE mechanism, UNHONOURED substance

**Substance, on code evidence, and this half is conclusive.**
`arcaai/harness/runner.py` contains no `session_status`, no halted state, no
signal handling and no `finally` block. There is no abort path. Rev C §8.3 is
UNHONOURED. None was built; the arc instruction forbade building one mid-arc and
that was the right call.

**Mechanism, INDETERMINATE, twice — and the failure is the probe's, not the
runner's.** `timeout -s INT` at 3 seconds and again at 1 second both allowed the
run to complete and then reported exit 124. SIGINT through the MSYS `timeout`
does not reach a native Windows Python process. Neither attempt interrupted a
run, so neither tested anything about the runner's abort behaviour.

**Retraction, verbatim, because the wrong line was printed before it was
caught:**

> my script's first summary line said "an artefact WAS written by the aborted
> run — FINDING", and that line was wrong, because the run was not aborted.

Recorded rather than corrected silently. A probe that reports a finding about a
system it never exercised is the check-method family at its most dangerous,
because the output is confident and the subject is absent.

## 12. UNHONOURED items — eleven, with fix routes

Rev C is the build target at
`9d6ab3b0da21d5e6603f7fa505d48a892da9acf11dba60725b83e5a8c590e88c` and is
**UNACCEPTED**, with a delta round in flight. This spike is a de facto shakedown
of the round-2 fixes, and these eleven are divergences between Rev C's text and
buildable reality. **They are findings for the acceptance stop, not defects in
Rev C and not blockers for the spike.**

**Runner-side, six. All confirmed ABSENT from the emitted artefact by reading its
keys, not by reading the code alone.**

| # | Requirement | Rev C | Fix route |
|---|---|---|---|
| 1 | `evaluator_version`, the fourth identity leg | §6.8.1 | Runner change; the runner predates the leg |
| 2 | `environment_config_sha256` in the result | §8.1 criterion 7 | Runner change; the value exists, computed this arc |
| 3 | `material_parameter_list_sha256` in the result | §9.5 element 3 | Runner change; the list exists, authored this arc |
| 4 | `confound: single_chunk` marker | §12.3 | Runner change. **It should have fired** — both E documents are single-chunk |
| 5 | `session_status: halted` | §8.3 | Runner change; no abort path exists |
| 6 | `invalidation_status` | §9.8 | D2.5 ledger; the runner writes no rows |

Items 2 and 3 are the sharpest of the six: the values exist and are recorded in
this arc's custody, but the runner does not carry them into the result, **so the
artefact's environment identity is incomplete on its face** while the information
needed to complete it sits beside it.

**Spec-side, five. Schema v0.2 is `additionalProperties: false` at every level
and predates every round-2 fix, so it has no field for four Rev C requirements.**
All four are carried in `description` under the `CARRIED-NO-FIELD:` prefix per
Ruling 5, so a future migration can find every spec that did this by grep.

| # | Requirement | Rev C | Carried as |
|---|---|---|---|
| 7 | absolute `top_k` cap, which §5.4 says every scenario records **in the spec** | §5.4 | `CARRIED-NO-FIELD:` — class corpus_qa cap 7 |
| 8 | binary-probe justification | §5.3 | `CARRIED-NO-FIELD:` |
| 9 | Obligation D justification | §2.1 | `CARRIED-NO-FIELD:` |
| 10 | density-stratified note | §5.2 | `CARRIED-NO-FIELD:` |
| 11 | stable typology identifier with no controlled vocabulary to draw from | §2.4, Appendix B item 16 | Used, prefixed `unverifiable-pending-vocabulary:` |

**Fix route for all five is a v0.3 schema.** v0.2 is immutable once merged; a
change is a new versioned file, never an edit. Item 11 additionally needs the
corpus-side vocabulary, which is not the schema's to supply — a schema can
require a field and cannot require that the field mean something.

## 13. Method notes — two instrument defects, both the harness's own

Recorded because this repository tracks the check-method family, and because
both defects were in instruments written to verify something else.

**M1 — `Refusal.message` does not exist.** The validation probe script printed
`r.message` on refusal, which raised `AttributeError` and crashed the script
while reporting D1. The refusal itself had fired correctly. Fixed by reading the
class definition rather than guessing a second time, and the recorded run is the
corrected one. The defect was in the reporting path of a check, which is the
place where a failure is least likely to be noticed.

**M2 — the abort probe, at section 11.** Two attempts, both INDETERMINATE, with
a confident and wrong summary line printed on the first.

## 14. F7 and queue item 32 — the encoding fault, evidenced fixable

Forcing `PYTHONIOENCODING=utf-8` at invocation rendered the runner's em-dash
regime banner **correctly in every run of this arc**. The 2026-08-13 record's F7
recorded the banner rendering as a replacement character in every captured run
there. This is affirmative evidence that queue item 32's stated fix — force
UTF-8 at harness entry — works, obtained without changing any artefact: the
result JSON is written with an explicit UTF-8 encoding and is unaffected either
way. Transcript fidelity only.

## 15. Artefact custody

In-tree:

- this record — committed by the act it describes

**Held outside the repository, not committed, custody by hash.** This follows the
2026-08-13 precedent, whose section 8 lists the RQA-001 spec, its probe files and
its result artefacts as held outside the tree, with only the runner and the
record committed. The precedent was read before being followed rather than
recalled.

```
5bad9660c7f8d5ebb3b04cfa5297651474770466444042f22ef9a90d4aeda0a3  d22a_scenario_RQA-107_COMMISSIONING-DRAFT.yaml
efa3f537b4d5432a241fe1a52d6c521fac5c1f54b2308f0f062f44dcf34f0267  environment_identity_RQA-107.json
56ab9ac59c989f62e5117941d95e4265187b12984024b9954832564e2a112080  results/result_RQA-107_20260815T133253152481+0000.json
3172ce61283c46f264de2304a8de9ba5410bbae820603d016b17e991232cef92  results/result_RQA-107_20260815T133328576690+0000.json
c851012e2601e6edf402239ef94cde69a698337c9a41b5f9e68cda3abc1762cd  results/result_RQA-107_20260815T133422933535+0000.json
d5928958ede74dc7de9fe3249b0d025047313cd033618e7e34681efba9ea3637  results/result_RQA-107_20260815T133457824933+0000.json
```

The RQA-107 spec is Claude Code authorship and is admissible for this spike only.
Its promotion to a committed scenario, if wanted, is a separate governed act.
**Note the custody weakness plainly:** these artefacts live in a session
scratchpad. Nothing preserves them beyond this session, and the 2026-08-13 arc
needed a manual preservation act for exactly this reason. Preservation is owed
and is not performed by this record.

## 16. What this record does not do

It does not evaluate acceptance, promote any result, or claim that RQA-107
passed or failed — the comparison is deliberately unmade. It does not accept
Rev C, amend it, or dispose any round-2 finding.
It does not commit the spec or the result artefacts. It does not investigate the
density observation at section 10, and it does not build the abort path whose
absence it records.
