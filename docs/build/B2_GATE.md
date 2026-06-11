# B2 gate — Synthetic data (fraud)

Per Build & Quality Plan v1.0 / Blueprint G1. All ticked = GATE PASSED.

- [ ] `dvc repro verticals/fraud/dvc.yaml` runs both stages clean
- [ ] `data/fraud/data_profile.json` — ~950k rows, fraud rate inside 0.1–1%,
      all four patterns present
- [ ] `data/fraud/validation_report.json` — overall_success: true,
      worst anomaly < 5%, all integrity checks pass
- [ ] `pytest verticals/fraud/tests/test_synthetic.py` — 10 passed (also in ci-mlops)
- [ ] Determinism: re-run generate → identical content_hash
- [ ] `dvc add`/pipeline outs tracked; `git add data/fraud/*.dvc dvc.lock` committed
      → **DVC data version pinned** (the gate's final condition)
- [ ] BUILD_TRACKER.md B2 row updated; CURRENT_STATE.md updated
