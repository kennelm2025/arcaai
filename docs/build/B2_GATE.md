# B2 gate — Synthetic data (fraud)

Per Build & Quality Plan v1.0 / Blueprint G1. All ticked = GATE PASSED.

- [x] `dvc repro verticals/fraud/dvc.yaml` runs both stages clean
- [x] `data/fraud/data_profile.json` — ~950k rows, fraud rate inside 0.1–1%,
      all four patterns present
- [x] `data/fraud/validation_report.json` — overall_success: true,
      worst anomaly < 5%, all integrity checks pass
- [x] `pytest verticals/fraud/tests/test_synthetic.py` — 10 passed (also in ci-mlops)
- [x] Determinism: re-run generate → identical content_hash
- [x] `dvc add`/pipeline outs tracked; `git add data/fraud/*.dvc dvc.lock` committed
      → **DVC data version pinned** (the gate's final condition)
- [x] BUILD_TRACKER.md B2 row updated; CURRENT_STATE.md updated

## Addendum — retrospective completion (25 Jul 2026)

**The tick marks above were applied on 25 July 2026, not at the gate.**
This document was found during the WS-D RAT-01 work carrying every
criterion unticked while BUILD_TRACKER.md recorded B2 as GATE PASSED
(Jun 2026). Mike confirmed the gate was passed; the criteria were met
and the document was never updated to reflect it.

The ticks are therefore a record of a confirmed past state, not a
contemporaneous account. They are marked as such here rather than
applied silently, because a gate document that appears to have been
maintained at the time when it was completed thirteen months later
misrepresents the evidence trail — which is the failure the RAT-01
refresh exists to prevent.

Corroborating evidence for the underlying claim, independent of this
document: B3_GATE.md records `dvc repro` running all three stages clean
(generate → data_validate → feature_engineer), which requires the B2
stages to have been passing; the generator content hash
`6db7d6b191a9c929` is pinned there; and B3 records the full vertical
suite green at 20 tests, which includes B2's ten.

Class: trail integrity — same as the 2 Jul 2026 note in
GOVERNANCE_REVIEW_CHANGELOG.md and CL-10. Root cause is the Q-A6
finding: trail documents were not updated in the same commit as the
work they record. Disposition under RAT-01 §3.1: **addendum, not DEC.**
The gate decision would not have differed; the evidence existed and the
record of it did not.

B1, B3 and B4 gate documents were written at stage entry as criteria
checklists and were filled in as evidence landed. B2 is the one that
was missed. This is not a gap in the practice but an uneven
application of it — see the §1 correction to
`docs/governance/WS-D_RAT-01_GATE_PLAN.md`.
