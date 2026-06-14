# ArcaAI — Session Notes entry · 13 June 2026

Drop into the repo root (archive/snapshots/ when superseded). The boot line
below is what to paste into a fresh chat to resume.

---

## Boot line for next session

> "ArcaAI — B5 inc2 entry. `main` at `5f4e570` (B5 inc1 merged: fraud scoring
> contract + BentoML scorer, parity/contract/latency green, CI green both
> workflows). Read START_HERE.md, BUILD_TRACKER.md, and the Build & Quality
> Plan B5 row. inc1 lives in `contracts/fraud_scoring.py` +
> `verticals/fraud/serving/{scorer,bento_service}.py` +
> `verticals/fraud/tests/test_serving.py`. Next: B5 inc2 — FastAPI skeleton
> over the Bento (api/ already scaffolded), endpoint schema, cross-side
> API↔BentoML contract test, and the `contracts/**` CI path trigger (deferred
> from inc1). Then B5 close: `bentoml serve` smoke + authoritative G9 (P99
> <200ms on the pinned model) → docs/build/B5_GATE.md. **First moves: flip
> BUILD_TRACKER B5 → IN PROGRESS; draft an ADR for the serving model-source
> decision (DVC-pinned artefacts, not MLflow Registry — check vs Engineering
> Blueprint/ADR-002, add Blueprint errata if it's a deviation).** Housekeeping
> owed: project-isolated env to kill the BentoML/MLflow OpenTelemetry clash;
> `~$*` in .gitignore."

---

## What was done / decided / produced

| Commit | What |
|---|---|
| a7a5eab (main) | **eol fix.** `.gitattributes` LF rules for DVC-hashed text (`*.py`, `*.yaml`, `dvc.lock`, etc.), CRLF for Windows scripts, binary for non-LFS data/model formats — **existing Git LFS lines preserved**. `walk_forward` re-pinned in `verticals/fraud/dvc.lock` (line-ending-only change, `dvc commit`). |
| eff1d2c (REVERTED) | LFS-clobber incident — see below. Rolled off `main` via `reset --hard 8934905` + force-push; orphaned objects gc'd. |
| a764ce4 → 5f4e570 (main, PR #5) | **B5 inc1** — fraud scoring contract + BentoML scorer. Both CI workflows green on the PR and on the post-merge `main` commit. |

### B5 inc1 — what's in it
- `contracts/fraud_scoring.py` (+ `__init__.py`) — Pydantic request/response
  schema. Request = the 12 MVM features in contract order + optional
  `transaction_id`; response = calibrated probability + provenance. Single
  source of truth; `extra="forbid"`; a test asserts the field order equals
  `feature_pipeline.FEATURES`.
- `verticals/fraud/serving/scorer.py` — loads the B4 model + Platt scaler,
  scores `margin → sigmoid(a·margin + b)`. Self-contained (does NOT import the
  trainer); the parity test guarantees it matches `calibrate_mvm` exactly.
- `verticals/fraud/serving/bento_service.py` — BentoML 1.2+ service exposing
  `/score`. (No automated test — six-line wrapper; exercised by `bentoml serve`.)
- `verticals/fraud/tests/test_serving.py` — contract, parity (byte-exact vs
  offline), latency sanity. All green; full vertical suite green; ruff clean.
- `pyproject.toml` — `bentoml>=1.2`; `contracts` added to `packages` and
  coverage `source`.

### Key decisions (B5 inc1)
- **Model source = DVC-pinned artefacts, not MLflow.** B4 logs the model to
  MLflow only as a loose run artefact (no Model Registry), so the reproducible
  source of truth is `data/fraud/models/{xgb_mvm.ubj, platt_scaler.json}`.
- **Scoring uses the raw margin**, not `predict_proba` — calibration preserved.
- **Contract granularity = the 12-feature MVM vector.** Online feature assembly
  is the agent/tool layer's job (B6), not the scorer.
- **Provenance in every response**: model artefact sha256 + Platt (a, b) +
  schema version — a score is reproducible from the response alone.

---

## Incident log — LFS clobber (recovered, no lasting damage)

The repo's `.gitattributes` already carried the Git LFS config
(`*.png/.docx/.pptx/.pdf/.jpg filter=lfs … -text`). The first eol attempt
**overwrote** that file instead of merging into it, dropping the `filter=lfs`
lines. The next commit (`eff1d2c`) then stored ~15 MB of real binaries
directly in git instead of as LFS pointers. Caught on `git show --stat`
(`Bin 130 -> 27401 bytes` etc. — 130-byte LFS pointers replaced by full files).
Recovery: `git reset --hard 8934905` + `git push --force`, then
`git reflog expire --expire=now --all && git gc --prune=now`. Redone with a
`.gitattributes` that keeps the five LFS lines verbatim and appends the eol
rules.

**Lesson (carry forward):** never overwrite `.gitattributes` — the LFS config
lives there. Merge new rules in. A `modified: .gitattributes` in status is the
signal that a tracked file with existing rules is being changed.

---

## State now
- `main` at `5f4e570`, CI green (ci-devops + ci-mlops).
- B5 inc1 landed. **BUILD_TRACKER.md B5 row still reads NOT STARTED** — flip to
  IN PROGRESS (inc1 done; inc2 + gate doc remain).
- Local env: BentoML 1.4.39 installed into base Anaconda (`d:\users\mikek\anaconda3`).

## Next actions
1. **B5 inc2** — FastAPI skeleton over the Bento (`api/` scaffolded: `main.py`,
   `routers/`, `schemas/`, `version.py`), endpoint schema, cross-side
   API↔BentoML contract test, and add `contracts/**` to both CI workflows'
   `paths:` (deferred from inc1).
2. **B5 close** — `bentoml serve …:FraudScoringService` smoke against the
   pinned model (needs `dvc pull`/`dvc repro` for `data/fraud/models/*`), record
   authoritative G9 (P99 <200ms) → `docs/build/B5_GATE.md`, flip BUILD_TRACKER
   B5 to GATE PASSED.

## Governance follow-ups (per the Build & Quality Plan process)
- [ ] **BUILD_TRACKER.md** — flip B5 row NOT STARTED → IN PROGRESS now;
  → GATE PASSED at B5 close.
- [ ] **ADR — serving model-source.** Record: "serving loads the DVC-pinned B4
  artefacts (`xgb_mvm.ubj` + `platt_scaler.json`), not an MLflow Registry
  model." First check the Engineering Blueprint's model-lifecycle section /
  ADR-002 (three-stage lifecycle): if it assumed registry-based promotion to
  serving, this is a **deviation** → ADR **plus** an errata entry against the
  Blueprint; if it's silent on the mechanism, a one-paragraph ADR fixes the
  pattern before B6 (fraud tool) and B10 (compliance/RM replication) inherit it.
  Use `decisions/_template.md`; next ADR number per DECISIONS.md.
- [ ] (Optional) **DECISIONS.md** — one-line note that the eol recovery
  force-pushed `main` (CONTRIBUTING deviation; emergency infra fix).

> The locked Build & Quality Plan docx is NOT edited mid-build — decisions land
> as ADRs/errata in the repo and the suite is re-issued at build close.

## Housekeeping owed
- Project-isolated env (`conda create -n arcaai` or a venv) → kills the
  BentoML/MLflow OpenTelemetry transitive clash (warning only, currently inert).
- `~$*` line in `.gitignore` (Word lock files).
- Optional: DECISIONS.md note that the eol fix + recovery force-pushed `main`
  (against CONTRIBUTING) — emergency infra fix; record if you want the audit
  trail tidy.
