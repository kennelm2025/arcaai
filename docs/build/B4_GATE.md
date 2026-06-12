\# B4 Gate — Baseline + MVM + Calibration (fraud)



Stage definition: rules-engine baseline (G2) + 12-feature XGBoost MVM +

Platt calibration (G7, MAE < 0.05) + 6-period walk-forward (G5).

First model numbers in the build. All runs log to MLflow `arcaai-fraud`.

R8 governs sign-off: test ROC-AUC > 0.85 (gate), 0.90 (indicative target).

R9 business metric: precision uplift at fixed alert budget vs the rules

baseline. R10: calibrated independent probabilities — no sum-to-one.



\## Assumptions requiring ratification (flag before gate close)



The Build \& Quality Plan B4 section was not to hand when this doc was

drafted; the following were set by judgement. Ratify or amend, then tick.



\- \[x] \*\*A1 — Calibration MAE definition.\*\* MAE < 0.05 read as mean absolute

&#x20;     calibration error over 10 equal-frequency probability bins on the

&#x20;     test split: mean |observed fraud rate − mean predicted probability|

&#x20;     per bin, unweighted.

\- \[x] \*\*A2 — Canonical alert budget = 1.0% of transactions.\*\* Reported at

&#x20;     0.5% and 1.0%; the R9 uplift headline uses 1.0%. (Dataset fraud rate

&#x20;     0.535% by count is above real-world \~0.1% — per the data dictionary,

&#x20;     class-weighting and budget choices must note this.)

\- \[x] \*\*A3 — Walk-forward scheme.\*\* 6 monthly test periods Dec 2025 → May

&#x20;     2026, expanding training window from 2025-01, label\_available\_mask

&#x20;     applied at each training cut. Fold 1 lands on the December

&#x20;     seasonality lift by design.

\- \[x] \*\*A4 — Evaluation labels.\*\* label\_available\_mask binds TRAINING cuts

&#x20;     only; test/calibration evaluation is retrospective with full labels.



\## Increment 1 — Rules-engine baseline (G2)



\- \[ ] `verticals/fraud/training/rules\_baseline.py` committed — static

&#x20;     domain-prior rules over the 12 contract features, never fitted,

&#x20;     label-blind (structurally tested)

\- \[ ] Tests green in ci-mlops (`test\_rules\_baseline.py`: determinism,

&#x20;     label-blindness, contract-only inputs, signal floor, budget

&#x20;     arithmetic, report contract) — 6 passed locally 12 Jun; CI tick at push

\- \[x] DVC stage `baseline\_eval` pinned; `data/fraud/baseline\_report.json`

&#x20;     produced at full scale (956,684 rows; test split 143,503)

\- \[x] MLflow run #1 logged to `arcaai-fraud` (run name `rules\_baseline\_g2`)

&#x20;     — run id: 4cd4186171724eb08ed1d6ba899c5b3a

\- \[x] Full-scale baseline numbers recorded here:

&#x20;     ROC-AUC 0.9375 · PR-AUC 0.7757 · precision@1% 0.4718 · recall@1% 0.7974

&#x20;     Per-pattern recall@1%: spree 0.9325 · testing 0.9164 · takeover 0.0602

&#x20;     · first\_party 0.0000 (blind by design — the MVM's headroom)

&#x20;     \*\*Context note (data dictionary honoured):\*\* an unfitted rules engine

&#x20;     already clears R8's 0.85 — injected patterns are cleaner than reality.

&#x20;     B4's meaningful result is uplift over this baseline (R9) and

&#x20;     calibration quality, not the R8 number itself.

&#x20;     \*\*MLflow note:\*\* duplicate `arcaai-fraud` experiment found at first

&#x20;     run — manual B1 creation with whitespace-corrupted name; zero runs;

&#x20;     deleted. Canonical experiment id 2. Only committed creation path is

&#x20;     `set\_experiment` in rules\_baseline.py (exact-named, idempotent).



\## Increment 2 — XGBoost MVM (G5 entry)



\- \[ ] xgboost added to pyproject (the one new B4 dependency)

\- \[ ] Trainer: exactly the 12 FEATURES columns, chronological 70 train

&#x20;     split, label\_available\_mask at train-end, seed-pinned

\- \[ ] Uncalibrated test ROC-AUC recorded; R8 gate check (> 0.85)

\- \[ ] R9 headline: precision uplift at 1% budget vs baseline recorded

\- \[ ] MLflow run logged with params, metrics, model artefact



\## Increment 3 — Platt calibration (G7)



\- \[ ] Platt scaler fitted on the 15 calibration split only (mask at

&#x20;     cal-end), applied to test

\- \[ ] Calibration MAE < 0.05 on test (per A1); reliability table in the

&#x20;     MLflow run

\- \[ ] Independent probabilities verified — no group normalisation (R10)



\## Increment 4 — Walk-forward (G5/G7 close)



\- \[ ] 6 folds per A3; per-fold ROC-AUC, precision@1%, calibration MAE

\- \[ ] Stability read: no fold materially below the full-test number

&#x20;     without explanation (December fold expected to move)

\- \[ ] All folds logged to MLflow as nested/tagged runs

\- \[ ] Gate review: tracker flip, CURRENT\_STATE update, SESSION\_NOTES entry



\## Gate verdict



\- \[ ] DevOps COMPLETE · MLOps COMPLETE · \*\*GATE: \_\_\_\_\_\_\*\* · Date: \_\_\_\_\_\_

