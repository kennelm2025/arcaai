# B4 Gate — Baseline + MVM + Calibration (fraud)

Stage definition: rules-engine baseline (G2) + 12-feature XGBoost MVM +
Platt calibration (G7, MAE < 0.05) + 6-period walk-forward (G5).
First model numbers in the build. All runs log to MLflow `arcaai-fraud`.
R8 governs sign-off: test ROC-AUC > 0.85 (gate), 0.90 (indicative target).
R9 business metric: precision uplift at fixed alert budget vs the rules
baseline. R10: calibrated independent probabilities — no sum-to-one.

## Assumptions requiring ratification (flag before gate close)

The Build & Quality Plan B4 section was not to hand when this doc was
drafted; the following were set by judgement. Ratified by Mike 12 Jun 2026.

- [x] A1 — Calibration MAE definition. MAE < 0.05 read as mean absolute
      calibration error over 10 equal-frequency probability bins on the
      test split: mean |observed fraud rate - mean predicted probability|
      per bin, unweighted.
- [x] A2 — Canonical alert budget = 1.0% of transactions. Reported at
      0.5% and 1.0%; the R9 uplift headline uses 1.0%. (Dataset fraud rate
      0.535% by count is above real-world ~0.1% — per the data dictionary,
      class-weighting and budget choices must note this.)
- [x] A3 — Walk-forward scheme. 6 monthly test periods Dec 2025 -> May
      2026, expanding training window from 2025-01, label_available_mask
      applied at each training cut. Fold 1 lands on the December
      seasonality lift by design.
- [x] A4 — Evaluation labels. label_available_mask binds TRAINING cuts
      only; test/calibration evaluation is retrospective with full labels.

- [x] A5 — Per-fold calibration slice (walk-forward). Each fold's Platt
      scaler is fitted on the 90 days immediately before the fold cut,
      masked at the cut; the model trains on everything earlier. 90 days
      leaves ~45 days of confirmed mixed-class data after the nonfraud
      settle. The global inc3 scaler is NOT reused across folds - it was
      fitted on data post-dating the early fold cuts and would leak.
      Ratified by Mike 12 Jun 2026.
- [x] A6 — Stability tolerance. "Materially below" = fold ROC-AUC more
      than 0.02 under the full-test reference. Flagged folds require
      narrative at gate review, not automatic failure. Ratified by Mike
      12 Jun 2026.

## Increment 1 — Rules-engine baseline (G2)

- [x] verticals/fraud/training/rules_baseline.py committed — static
      domain-prior rules over the 12 contract features, never fitted,
      label-blind (structurally tested). Merged to main at 99e32c3.
- [x] Tests green in ci-mlops (test_rules_baseline.py: determinism,
      label-blindness, contract-only inputs, signal floor, budget
      arithmetic, report contract). CI green on main post-merge.
- [x] DVC stage baseline_eval pinned; data/fraud/baseline_report.json
      produced at full scale (956,684 rows; test split 143,503)
- [x] MLflow run #1 logged to arcaai-fraud (run name rules_baseline_g2)
      — run id: 4cd4186171724eb08ed1d6ba899c5b3a
- [x] Full-scale baseline numbers:
      ROC-AUC 0.9375 - PR-AUC 0.7757 - precision@1% 0.4718 - recall@1% 0.7974
      Per-pattern recall@1%: spree 0.9325 - testing 0.9164 - takeover 0.0602
      - first_party 0.0000 (blind by design — the MVM's headroom)

      Context note (data dictionary honoured): an unfitted rules engine
      already clears R8's 0.85 — injected patterns are cleaner than reality.
      B4's meaningful result is uplift over this baseline (R9) and
      calibration quality, not the R8 number itself.

      MLflow note: duplicate arcaai-fraud experiment found at first run —
      manual B1 creation with whitespace-corrupted name; zero runs; deleted.
      Canonical experiment id 2. Only committed creation path is
      set_experiment in rules_baseline.py (exact-named, idempotent).

      Baseline re-logged as 008a4df33aa94d43873d8301d8287d2b at inc2 repro
      (manual MLflow run had rewritten baseline_report.json, invalidating
      the stage); metrics identical; this id is the R9 reference run.

## Increment 2 — XGBoost MVM (G5 entry)

- [x] xgboost added to pyproject (the one new B4 dependency)
- [x] Trainer: exactly the 12 FEATURES columns, chronological 70 train
      split, label_available_mask at train-end, seed-pinned
- [x] Uncalibrated test ROC-AUC recorded; R8 gate check (> 0.85)
- [x] R9 headline: precision uplift at 1% budget vs baseline recorded
- [x] MLflow run logged with params, metrics, model artefact

      Run id: 36ccb6e2a44541f2802944eab3fa3d6a (xgb_mvm_uncalibrated)
      ROC-AUC 0.9883 - PR-AUC 0.9004 (R8: gate and indicative both passed,
      synthetic-data context note applies)
      R9 @1% budget: precision 0.4718 -> 0.5275 (+5.57pp; achievable
      ceiling at this budget/prevalence 0.5917) - recall 0.7974 -> 0.8916
      (+9.42pp)
      @0.5% budget: precision 0.9986 (716/717 alerts fraud) vs 0.8661
      Pattern recall @1%: spree 0.9976 - testing 1.0000 - takeover 0.3855
      (was 0.0602 — the uplift source) - first_party 0.0000 (by design)
      Training audit: 97,709/669,678 train rows excluded for unconfirmed
      labels (as_of 2025-12-26); 3,224 fraud rows; scale_pos_weight 176.41

## Increment 3 — Platt calibration (G7)

- [x] Platt scaler fitted on the 15 calibration split only (mask at
      cal-end): p = sigmoid(a*margin + b), a 0.8340 / b -3.2864, fitted
      on 61,745 of 143,503 cal rows (81,758 excluded for unconfirmed
      labels at as_of 2026-03-14 - labels lag, so the back of the cal
      window is mostly unsettled; recorded in the run calibration_audit)
- [x] Calibration MAE < 0.05 on test (per A1): 0.000858 calibrated vs
      0.025213 uncalibrated - the scale_pos_weight inflation corrected
      (top bin mean predicted 0.2510 -> 0.0632 against observed 0.0563).
      Reliability table logged as an artefact in the MLflow run.
- [x] Independent probabilities verified - no group normalisation (R10):
      batch-independent, row-independent, monotone in margin. ROC-AUC
      bit-identical pre/post (0.988349) - inc2 R8/R9 numbers stand.

      Run id: 25ca86376650494691523e60cd8655d9 (xgb_mvm_platt_calibration)
      Scaler persisted as transparent JSON (models/platt_scaler.json).
      scripts\test.cmd now runs ruff before pytest (local/CI parity -
      the inc2 lesson closed).

      Re-logged as b0abaf8d11174a88809003bd74d252c6 at the inc4 repro
      (branch switch recreated calibrate_mvm.py with CRLF endings,
      invalidating the stage - same class as the morning incident);
      metrics and scaler bit-identical; b0abaf8d... is the canonical G7
      run, per the inc1 baseline re-log precedent.

      Incident note (12 Jun): the inc3 repro initially tried to re-run
      train_mvm - dvc.lock held the LF hash of train_mvm.py while the
      working copy was CRLF (git autocrlf rewrite; git compares
      normalised, DVC 3 hashes raw bytes). Aborted before any MLflow run
      was minted. Recovery: model restored from DVC cache; mvm_report.json
      restored byte-identical from the run 36ccb6e2 artefact plus run-id
      reinjection (md5 verified against the lock); lock re-pinned via
      dvc commit. No retrain - 36ccb6e2 remains the pinned MVM.
      Carry-item: .gitattributes eol policy, decide at session close.

## Increment 4 — Walk-forward (G5/G7 close)

- [x] 6 folds per A3; per-fold ROC-AUC, precision@1%, calibration MAE
      Fold ROC-AUC: 0.9581 (Dec, flagged) - 0.9846 - 0.9705 - 0.9900 -
      0.9852 - 0.9889. Min 0.9581, median 0.9849 vs full-test 0.9883.
      Calibration MAE per fold: max 0.002643 (Dec) - the G7 gate
      (< 0.05) holds out-of-sample on every fold with fold-local
      Platt scalers (A5).
- [x] Stability read (A6): December is the only flagged fold
      (ROC -0.0302 vs reference) and it is the anticipated one - the
      fold-1 model trained Jan-Nov 2025 and met December's seasonality
      shift (1.35x volume, 1.2x amounts) unseen. The expanding window
      self-heals: with December in the training data, folds 2-6 are all
      within tolerance. Precision@1% spread (0.30-0.75) is prevalence
      arithmetic, not model decay: as a share of each month's
      achievable ceiling (n_fraud/alerts) the folds sit at
      77/89/83/91/86/91% - December lowest, same cause (754 alerts in
      a high-volume month against 292 fraud rows; ceiling 0.387).
- [x] All folds logged to MLflow as nested/tagged runs
      Parent: f2da0beae43b4ad1b9e3fe4b73e2593d (walk_forward_g5);
      six nested fold runs tagged stage=B4 / gate=G5 / fold /
      test_month.
- [x] Gate review: tracker flip, CURRENT_STATE update, SESSION_NOTES
      entry (session close, 12 Jun 2026)

## Gate verdict

- [x] DevOps COMPLETE - MLOps COMPLETE - GATE: PASSED - Date: 12 June 2026

      Evidence chain: G2 baseline run 008a4df33aa94d43873d8301d8287d2b;
      G5 MVM run 36ccb6e2a44541f2802944eab3fa3d6a (R9 +5.57pp precision,
      +9.42pp recall at the 1% budget); G7 calibration run
      b0abaf8d11174a88809003bd74d252c6 (MAE 0.000858); G5 walk-forward
      parent run f2da0beae43b4ad1b9e3fe4b73e2593d (6 folds, one
      explained flag). Synthetic-data context note applies throughout:
      the narrated result is uplift and calibration, never the raw R8
      pass.