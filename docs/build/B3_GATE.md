# B3 gate — Fraud features + anti-leakage suite

Per Build & Quality Plan v1.0 / Blueprint G3–G4. All ticked = GATE PASSED.

- [x] `dvc repro verticals/fraud/dvc.yaml` runs all three stages clean
      (generate → data_validate → feature_engineer)
- [x] `data/fraud/features.parquet` — 956,684 rows, exactly the 12-feature
      MVM budget (see `verticals/fraud/features/FEATURES.md`) + label columns
- [x] `data/fraud/feature_report.json` — `flagged: []` (no feature breaches
      VIF > 8, missing > 30%, or near-zero variance); 70/15/15 chronological
      split boundaries recorded
- [x] `pytest verticals/fraud/tests/test_leakage.py` — 10 passed (also in
      ci-mlops). Includes:
      - shuffle test: label shuffled BEFORE featurisation, held-out
        AUC < 0.55
      - planted-leak control: detector must FIRE on a deliberate leak
      - source audit: every `.rolling(` excludes current row, every
        `.expanding(` is shift(1)-lagged, no label columns in feature code
      - future-blindness: features bit-identical when future rows removed
      - split-order and `label_available_mask` assertions
- [x] `pytest verticals` — full vertical suite green (20 tests)
- [x] Generator content hash unchanged at `6db7d6b191a9c929` after the
      ADR-004 ns-pin (data identical; hash now pandas-version-stable)
- [x] `dvc push`; `git add data/fraud/*.dvc dvc.lock` committed
      → features version pinned
- [x] DECISIONS.md ADR-004 appended; BUILD_TRACKER.md B3 row updated;
      CURRENT_STATE.md updated
