# ArcaAI — Session Handover · 10–11 June 2026

Drop this file into the repo as `SESSION_NOTES_entry_2026-06-11.md` (root now,
`archive/snapshots/` when superseded). It is the complete state of play.

---

## 1. What happened (two sessions)

| Commit | What |
|---|---|
| `986afd3` | **Phase 0.5** — repo became the monorepo: locked suite into `docs/governance/`, DECISIONS.md + BUILD_TRACKER.md at root, April lineage archived with SUPERSEDED notes, diagrams renamed AcraAI→ArcaAI into `diagrams/image-round-inputs/`, reviews into `docs/reviews/`, Git LFS live (42 binaries) |
| `0a80a86` | Phase 0.5 GATE PASSED — **Phase 0 closed, all five gates** |
| `8414b9c` | **B1 foundation** — skeleton per Blueprint §4, ci-devops + ci-mlops workflows, Postgres+MLflow compose stack, root docs rewritten to post-lockdown state, document-register.yaml retired |
| `849a4a9` | **B2 fraud synthetic data** — generator, GE suite, data dictionary, DVC pipeline pinned |
| `c06022c` | Tracker: **B2 GATE PASSED**; B1 IN PROGRESS (Docker pending) |

All five commits on `origin/main`. CI: 4 runs, 4 green.

## 2. Current state

- **Phase 0 — CLOSED.** Suite locked (BA v1.0b · SA v1.1 · TI v1.1 · EB v1.1 ·
  LB v2.1 · DP v1.1 · deck v2a), rulings R1–R13, ADR-000–003 recorded.
- **B1 — IN PROGRESS.** Everything done and CI-verified except the Docker stack:
  install Docker Desktop → `scripts\dev_up.cmd` (Postgres :5432, MLflow UI :5000,
  create experiment `arcaai-fraud`) → tick remaining boxes in `docs\build\B1_GATE.md`
  → flip tracker.
- **B2 — GATE PASSED.** Dataset: **956,684 txns**, 2,000 customers, 600 merchants,
  17 months (2025-01-01→2026-05-31), fraud rate 0.535% across four patterns
  (spree 2,506 · testing 1,630 · takeover 603 · first_party 380).
  Content hash **`6db7d6b191a9c929`** — byte-identical on Windows/py3.13 and
  Linux/py3.12. GE suite + 4 integrity checks PASS, worst anomaly 0.0000% (gate 5%).
  DVC pipeline `generate → data_validate` pinned in `verticals/fraud/dvc.lock`;
  data in local remote `.dvcstore`. 15 tests in CI, coverage 70.8% (gate 60%).

## 3. Key working facts

- Repo = single source of truth: `D:\ArcaAI-repo\arcaai`. **Edit governance files
  in the repo only** — never in `D:\ArcaAI` or `locked\` (both now inbox/dead).
- Markdown editors that reformat on save are banned for governance files —
  Notepad or PowerShell `.Replace()` one-liners for status flips.
- `label_available_date` on every row is load-bearing: B3+ must never use a
  label before that date (anti-leakage rule 3 starts at the data).
- Doc–code drift = ADR in DECISIONS.md, or it didn't happen.
- Regenerate dataset any time: `dvc repro verticals\fraud\dvc.yaml` — same seed,
  same hash, validation re-runs.

## 4. Next steps plan

### Next build session — B3: fraud features + anti-leakage suite (the headline)
1. **Feature pipeline** (`verticals/fraud/features/feature_pipeline.py`, DVC stage
   `feature_engineer`): velocity windows (txn counts/amounts 1h/24h/7d, `shift(1)`
   discipline), amount z-score vs customer history, device novelty, merchant-risk
   and category-shift signals, night/intl flags, time-since-last-txn — the
   signatures the injected patterns left behind. Chronological 70/15/15
   train/cal/test split. All aggregates date-filtered, labels respected via
   `label_available_date`.
2. **Anti-leakage suite** (`test_leakage.py`, runs in ci-mlops): shuffle test
   (target randomised → AUC must be < 0.55), `.rolling`-without-`.shift(1)` source
   audit, date-filter audit, split-order assertions. **Gates G3/G4.**
3. Pre-train filters: VIF > 8, missing > 30%, near-zero variance — filter report
   committed. Same delivery pattern: zip → apply cmd → run → commit → CI green.

### Then, in order
- **B4** — rules-engine baseline (G2) + 12-feature MVM + Platt calibration +
  6-period walk-forward (G5, G7). First AUC numbers appear here.
- **B5** — BentoML serving + first real contract in `contracts/`.
- **B6** — LangGraph agent v0 + Llama 3.1 8B via Ollama.

### Background / parallel (owner: Mike)
- [ ] **Docker Desktop** install → close B1 gate (30 min)
- [ ] **ADR-000 image round** — GATES CLIENT USE. Inputs + Grok regeneration brief
      staged in `diagrams/image-round-inputs/`. BA figs 1.1/3.1/4.1/5.1 + new 4.2,
      LB figs 1–3, deck regeneration.
- [ ] **G10 external reviewers** — one per vertical; longest lead; brief includes
      document narrative. Every week unrecruited slips the endgame.
- [ ] **ML_Pipeline_v0.2.docx** → upload to Claude for the R13 harvest check
- [ ] Manual trio: logo artwork spelling · REVIEW_unknown-1/-2 · `D:\ArcaAI_legacy`
- [ ] Post-B9: WS3.1 deck design pass (+ use-case roadmap one-pager); GPU rental
      plan for the B12 70B demo config

### Session-opening line for next time
> "ArcaAI B3 — fraud features + anti-leakage suite. Repo at c06022c, B2 GATE
> PASSED, dataset hash 6db7d6b191a9c929. Read START_HERE.md."

---
*Phase 0 closed · B1 one install from done · B2 passed with a reproducible
million-row dataset. The control layer has a foundation.*
