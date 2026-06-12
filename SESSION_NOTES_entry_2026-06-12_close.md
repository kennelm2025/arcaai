# ArcaAI — Session Notes entry · 12 June 2026 (B4 increments 3+4 — GATE PASSED)

Drop this file into the repo root (archive/snapshots/ when superseded).

---

## What was built / decided / produced

| Commit | What |
|---|---|
| 342d146 (PR #3) | **B4 inc3 — Platt calibration (G7).** calibrate_mvm.py (fit on masked 15% cal split, transparent JSON scaler, reliability table to MLflow), test_calibrate_mvm.py (6 tests), DVC stage calibrate_mvm, scripts\test.cmd now runs ruff before pytest (local/CI parity — inc2 lesson closed), dvc.lock re-pin after CRLF drift |
| f7f6f64 -> MERGE_HASH (PR #4) | **B4 inc4 — 6-fold walk-forward (G5) + gate close.** walk_forward.py (A3 scheme, fold-local Platt per A5, stability read per A6), test_walk_forward.py (6 tests), DVC stage walk_forward, B4_GATE.md verdict: **GATE PASSED 12 Jun 2026** |

CI green throughout. Local suite 49 passed, coverage 77.16% (gate 60%).

**Headline numbers:**
- **G7 calibration:** MAE 0.000858 vs gate < 0.05 (uncalibrated 0.025213 —
  the scale_pos_weight inflation, corrected; top bin 0.2510 -> 0.0632 vs
  observed 0.0563). ROC-AUC bit-identical pre/post (0.988349). R10 verified
  structurally. Masked cal fit used 61,745/143,503 rows (57% excluded —
  labels lag; recorded, not hidden).
- **G5 walk-forward:** fold ROC-AUC 0.9581/0.9846/0.9705/0.9900/0.9852/
  0.9889; median 0.9849 vs full-test 0.9883. MAE max 0.002643 — G7 holds
  out-of-sample every fold. December flagged (-0.0302, beyond A6's 0.02)
  with the anticipated seasonality narrative; expanding window self-heals
  fold 2 onward. Precision@1% spread is prevalence arithmetic: as share of
  monthly ceiling, folds sit at 77/89/83/91/86/91%.

**MLflow (experiment arcaai-fraud, id 2):**
- xgb_mvm_platt_calibration: 25ca86376650494691523e60cd8655d9 (first log),
  re-logged b0abaf8d11174a88809003bd74d252c6 at the inc4 repro — metrics
  and scaler bit-identical; **b0abaf8d... is the canonical G7 run** (inc1
  baseline re-log precedent).
- walk_forward_g5 parent: f2da0beae43b4ad1b9e3fe4b73e2593d, 6 nested
  fold runs tagged stage/gate/fold/test_month.

**A5/A6 ratified (Mike, 12 Jun):** A5 per-fold 90-day calibration slice
before each cut, masked at the cut (global scaler would leak into early
folds); A6 "materially below" = ROC > 0.02 under reference, flags demand
narrative not auto-failure. Recorded in B4_GATE.md alongside A1–A4.

## Key reasoning that won't be obvious from the committed files

**The CRLF/DVC hash-drift class — two incidents, one mechanism.** Git on
Windows (autocrlf) writes working copies CRLF whenever it materialises a
file (branch switch, pull creating a file new to that branch). Git compares
content normalised, so `git status` stays clean; DVC 3 hashes raw bytes, so
the stage goes stale and `dvc repro` re-runs it.
- Incident 1 (morning): train_mvm tried to re-run at the inc3 repro.
  Aborted in time (Ctrl-C before MLflow logging — train_mvm logs at the
  end). DVC had already deleted the stage outs. Recovery: model from DVC
  cache; mvm_report.json (cache:false — in neither DVC cache nor git!)
  rebuilt byte-identical from the run-36ccb6e2 MLflow artefact plus run-id
  reinjection, md5-verified against the lock; lock re-pinned via
  `dvc commit -f`. No retrain.
- Incident 2 (afternoon): calibrate_mvm.py recreated CRLF by the post-PR#3
  pull; stage re-ran inside the inc4 repro before it could be stopped.
  Outcome benign — deterministic, bit-identical metrics — handled by the
  re-log precedent (new id canonical).
**Lesson recorded: cache:false metrics exist ONLY in the workspace; an
aborted DVC stage deletes them. The MLflow artefact copy is the backstop —
but note train_mvm logs the report BEFORE appending mlflow_run_id, so
reconstruction needs the run-id reinjection step.**

**Walk-forward design subtlety (A5's origin).** A naive "last 15% of the
fold window" calibration slice dies at the mask: the 45-day nonfraud
settle annihilates recent rows, leaving a sliver biased toward fraud
(fraud labels confirm in ~18 days). The fixed 90-day slice leaves ~45
days of confirmed mixed-class data per fold. Corollary discovered in
testing: the 90-day buffer pushes the training window past the settle,
so train-side mask exclusions are legitimately ZERO in every fold — the
mask's work concentrates in the cal slice. The test suite asserts this
rather than the (wrong) intuition that train must always lose rows.

**December precision is a ceiling story, not a model story.** At a fixed
1% budget, precision is capped at n_fraud/alerts. December's high volume
(75,465 txns -> 754 alerts) against 292 fraud rows caps precision at
0.387; the fold achieved 77% of that ceiling. Normalising by ceiling
turns an alarming spread (0.30–0.75) into a tight one (77–91%). Use this
framing in any narrative about per-period precision.

## Settled decisions — do NOT re-open

1. A5/A6 as recorded in docs/build/B4_GATE.md (ratified 12 Jun 2026).
2. Canonical G7 calibration run is b0abaf8d... (re-log precedent).
3. B4 GATE PASSED — evidence chain in the gate-doc verdict block.
4. Walk-forward references read from the committed inc2/inc3 reports as
   declared DVC deps — if those reports change, the stability read
   correctly re-runs; do not hardcode reference numbers.

## Open questions / carried items

- **.gitattributes eol policy — PROMOTED to first action of next build
  session.** `*.py text eol=lf` (scope to be decided), then a deliberate
  working-tree refresh + single dvc.lock re-pin commit. Until then every
  branch switch that materialises .py files can re-flip DVC hashes.
- Delete staging folder D:\ArcaAI\b4 (B4 now closed — clear to delete).
- Carry-forwards unchanged: domain + AWS hygiene; ADR-000 image round
  (gates client use); G10 reviewers; ML_Pipeline_v0.2 harvest; manual trio
  (logo spelling, REVIEW_unknown-1/-2, D:\ArcaAI_legacy); WS3.1 post-B9;
  B12 GPU rental plan; identify/stop the markdown editor that escapes on
  save (governance files = Notepad only).

## Next concrete action

B5 (BentoML serving + FastAPI + contracts) in a fresh chat, AFTER the
.gitattributes fix. Boot line:

> "ArcaAI: .gitattributes eol fix then B5 entry. Repo at MERGE_HASH, B4
> GATE PASSED (all four increments, evidence chain in
> docs/build/B4_GATE.md). Read START_HERE.md, BUILD_TRACKER.md and the
> Build & Quality Plan B5 section. First: pin *.py eol, refresh working
> tree, single dvc.lock re-pin commit. Then scope B5 increment 1."

## Addendum (post-close finding)

The mystery escaping editor is IDENTIFIED: Windows 11 Notepad's new
markdown Formatted view rewrites files on save (it re-padded the whole
BUILD_TRACKER table during this close; restored via git, re-edited
byte-exact via python). Fix: Notepad Settings -> Markdown formatting
OFF; prefer byte-exact scripted edits for governance tables. This
closes the identify-the-editor carry item.
