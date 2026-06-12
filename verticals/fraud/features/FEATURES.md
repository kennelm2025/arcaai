# Fraud feature contract — the 12-feature MVM budget (B3)

`data/fraud/features.parquet` carries `transaction_id`, `timestamp`,
`customer_id`, the 12 features below (order is the contract — B4 trains on
exactly these columns via `feature_pipeline.FEATURES`), and the label columns
(`is_fraud`, `fraud_pattern`, `label_available_date`) for downstream use under
the `label_available_mask` discipline.

| # | Feature | Definition | Leakage discipline |
|---|---------|------------|--------------------|
| 1 | `txn_count_1h` | Customer's txn count in the hour before this txn | `rolling("1h", closed="left")` — window is [t−1h, t), current row excluded |
| 2 | `txn_count_24h` | Count in prior 24h | as above |
| 3 | `txn_count_7d` | Count in prior 7 days | as above |
| 4 | `amount_sum_24h` | Sum of amounts in prior 24h | as above |
| 5 | `amount_zscore` | Amount vs customer's own history | expanding mean/std on `shift(1)`; 0 when history is empty |
| 6 | `mins_since_last_txn` | Minutes since previous txn | diff vs previous row only; 30-day sentinel for first txn |
| 7 | `device_novelty` | 1 if device never seen in customer's PRIOR txns | `duplicated()` marks repeats of strictly earlier rows |
| 8 | `category_shift` | 1 if merchant category is new for this customer | as above |
| 9 | `category_risk` | Static MCC-style category risk weight (0.1–1.0) | static map — deliberately NOT a label-derived statistic |
| 10 | `is_night` | 1 if hour < 06:00 | row-local |
| 11 | `is_international` | Passthrough of txn flag | row-local |
| 12 | `log_amount` | log1p(amount) | row-local |

Excluded by design: merchant historical fraud rate, customer fraud history,
and any target-encoded signal — all are label-derived and would constitute
target leakage. If a future stage proposes one, it must pass the shuffle test
and be recorded as a decision.

Split: chronological 70/15/15 (train/calibration/test) by timestamp, never
shuffled. Train labels must be filtered through
`label_available_mask(df, as_of)` at every training cut (anti-leakage rule 3 —
`label_available_date` is load-bearing).

Enforcement: `tests/test_leakage.py` (gates G3/G4) runs in ci-mlops — shuffle
test (< 0.55 AUC, shuffled before featurisation), planted-leak detector-power
control, source audit, future-blindness test, split-order assertions.
