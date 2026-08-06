# ArcaAI — Batch-1 Panel Rulings Record

Date: 2026-08-06 (machine session)
Operator: Mike Kennelly
Coordinator: Claude
Status: RULED
Repo state at ruling: main at 85aedc3, clean, identical to origin/main
Evidence base: three reviewer returns (Grok, Gemini, DeepSeek — retained
verbatim by operator) + B7_BATCH1_PANEL_CONSOLIDATION_2026-08-06.md
(sha256 73fa28cb46d43e550e244f17d5f766fdde6ca70beab4be9f492f13d7df685fdb)
+ machine verifications of 2026-08-06 (TR-01 pinpoints, word counts,
TY-07 reference), transcripts held in session record.

## Ruling

Operator ruling issued 2026-08-06: all eight consolidation items
approved as recommended, no divergence.

1. **Per-document verdicts** — TY-03, TY-04, TY-05, TY-06, TY-07,
   TY-08, TY-09: ACCEPTED. Three-reviewer convergence on substance;
   Gemini's TY-04 amendment discharged by machine verification
   (TR-01 §3.4 and §5.1 pinpoints confirmed aligned).
2. **CV-01 → TY-04 design edge: GRANTED.** Two-of-three reviewer
   support (Grok, DeepSeek), §4.1 coercion indicators structural to
   the exit-decision framework.
3. **SG-01/SG-02 → TY-04: DECLINED — remain extras.** DeepSeek's
   structural-vs-supportive distinction adopted. Grok dissent
   (promote) recorded.
4. **TR-01 → TY-07 design edge: GRANTED** on the §5.3 textual case
   ("the data completeness lesson of TR-01 §3.4 applies with full
   force"). Grok dissent (leave; "well-anchored") recorded.
5. **CL-23: ACCEPTED as B8 design input** with DeepSeek amendments
   1–6 folded as panel-sourced revisions for the B8 design brief to
   test (per consolidation note §CL-23). No re-review this stage.
6. **Listing: APPROVED** — TY-03..09 transition to pending_review;
   new manifest version, appended transitions only, per DEC-0014.
7. **Batch-2 gate: OPEN.** WS-E 58 condition (batch-1 verdicts in)
   satisfied. Sequencing ruled by operator; panel pre-endorsements
   noted, no weight attached.
8. **EDGES.yaml v0.2.2: APPROVED** — two additions per rulings 2 and
   4: TY-04 minimum set becomes [OGL-0003, OGL-0004, TY-01, TR-01,
   CV-01]; TY-07 minimum set becomes [TY-02, SG-03, OGL-0001, TR-01].
   Version note to cite this record. Both edges already present in
   authored prose (verified), so no document amendment follows; the
   corpus_edges_check must pass green against v0.2.2 before the
   revision lands.

## Dissents recorded

- Grok: promote SG-01/SG-02 (ruling 3 declined it).
- Grok: leave TR-01 as extra (ruling 4 granted promotion).

## Execution queue arising

- EDGES v0.2.2 edit + corpus_edges_check green + listing transitions:
  ride together as the listing act (Docker up first per boot ritual
  if the act touches the ingest DB).
- Outcome circulations to Grok, Gemini, DeepSeek: after this record.
- Consolidation note + this record: commit to docs/governance/ at
  next docs touch.
- Reviewer calibration ledger: retained chair-side; not circulated.

## Round status

Batch-1 panel round 1 CLOSED at three reviewers (ChatGPT withdrawn,
recorded). Operator ruling is the deciding act; reviewer input
advisory throughout.
