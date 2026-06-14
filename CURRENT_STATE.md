# CURRENT STATE

*Last updated: 12 June 2026 (post B4 GATE PASSED)*

## Where we are

* **Phase 0 (lockdown): CLOSED.** Suite locked June 2026 — Banking Architecture
v1.0b, System Architecture v1.1, Technical Infrastructure v1.1, Engineering
Blueprint v1.1 (ML Pipeline Sister Document), Learning Bank v2.1, Delivery
Plan v1.1, Executive Presentation v2a. Rulings R1–R13 + DEC-0000–DEC-0004 in
DECISIONS.md. Repo is the single source of truth (Phase 0.5 GATE PASSED).
* **B1 (foundation): GATE PASSED (June 2026).** Skeleton per Blueprint §4, CI
green (ci-devops/ci-mlops), Docker Desktop (WSL 2, disk image on D:\\Docker),
Postgres 16 :5432 + MLflow 2.14.1 :5000 healthy, DVC init committed.
Canonical MLflow experiment: arcaai-fraud **id 2**.
* **B2 (fraud synthetic data): GATE PASSED (June 2026).** 956,684 txns, 2,000
customers, 600 merchants, 17 months, fraud 0.535% across four patterns.
Content hash `6db7d6b191a9c929` (ns-pinned per DEC-0004). GE suite +
integrity PASS; DVC pipeline pinned; leakage-honest label\_available\_date.
* **B3 (fraud features + anti-leakage): GATE PASSED (June 2026).** 12-feature
MVM budget; 956,684 rows featurised, zero filter flags; chronological
70/15/15 split. Anti-leakage suite in ci-mlops. feature\_engineer pinned.
* **B4 (baseline + MVM + calibration): GATE PASSED (12 June 2026).** All four
increments merged; verdict + full evidence chain in docs/build/B4\_GATE.md;
A1–A6 ratified.

  * Inc1 — rules baseline (G2): ROC-AUC 0.9375, precision@1% 0.4718. R9
reference run 008a4df33aa94d43873d8301d8287d2b.
  * Inc2 — XGBoost MVM (G5): ROC-AUC 0.9883, PR-AUC 0.9004. **R9 uplift @1%:
+5.57pp precision, +9.42pp recall** (takeover recall 0.06 -> 0.39).
Run 36ccb6e2a44541f2802944eab3fa3d6a.
  * Inc3 — Platt calibration (G7): **MAE 0.000858 vs gate < 0.05**
(uncalibrated 0.025213); ROC-AUC unchanged; R10 verified. Canonical run
b0abaf8d11174a88809003bd74d252c6 (re-log; first log 25ca8637...).
scripts\\test.cmd now lints before testing (local/CI parity).
  * Inc4 — 6-fold walk-forward (G5): fold ROC-AUC min 0.9581 (Dec, flagged
per A6 with seasonality narrative — self-heals fold 2 on), median
0.9849; MAE max 0.002643 — G7 holds out-of-sample every fold.
Parent run f2da0beae43b4ad1b9e3fe4b73e2593d + 6 nested fold runs.
* **Next: .gitattributes eol fix (gates clean DVC behaviour), then B5**
(BentoML serving + FastAPI + contracts) per the Build \& Quality Plan.

## Open items

* **.gitattributes eol policy — FIRST ACTION of next build session.**
Two CRLF/DVC hash-drift incidents on 12 Jun (mechanism + recovery in
SESSION\_NOTES and the B4\_GATE.md incident notes). Pin `\\\*.py text eol=lf`
(scope tbd), refresh working tree, single dvc.lock re-pin commit.
* Delete staging folder D:\\ArcaAI\\b4 (B4 closed — clear to delete).
* Domain registration (arcaai.com/.co.uk) + email + AWS account hygiene —
short session this week.
* **DEC-0000 image round — GATES CLIENT USE.** BA figs 1.1/3.1/4.1/5.1 + new
4.2 (mortgage flow), Learning Bank figs 1–3, deck diagram regeneration
(DEC-0001 residuals). Inputs staged in diagrams/image-round-inputs/.
* **G10 external domain reviewers** — one per vertical; longest lead; brief
includes document narrative (DEC-0003/D8). Recruit now.
* **ML\_Pipeline\_v0.2 harvest check** — archived April doc vs Blueprint §19
(R13 follow-up).
* Manual: logo artwork spelling; identify REVIEW\_unknown-1/-2 in diagrams;
inspect D:\\ArcaAI\_legacy; stop using the markdown editor that escapes on
save (governance files = Notepad only).
* WS3.1 deck design pass after B9 (incl. use-case roadmap one-pager).
* GPU rental plan for the B12 70B demo configuration.

