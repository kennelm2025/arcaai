# B5 Gate — Fraud Scoring Service (G9)

**Status: GATE PASSED** · Date: 2026-07-21 · main @ a901e28 (post PR #11)

## 1. Scope

Closes build track B5 (BentoML fraud-scoring service): inc1 (service —
PR #5, with follow-up merges #6–#7 from the same branch) + inc2
(FastAPI internal route, contracts as single source of truth,
cross-side contract tests — PR #11).

## 2. Environment (prerequisite, completed this session)

Project-isolated conda env `arcaai`, Python 3.11.15 (matches CI).
Editable install from pyproject only — no requirements files, no
Anaconda base underneath. `import contracts` verified from outside the
repo root: the e0d1d5b packaging fix holds with no masking environment
(ref: incident 1, 20 Jul handover). No OpenTelemetry conflict at serve.

## 3. Smoke (pinned model)

`dvc pull`: everything up to date. `bentoml serve
verticals.fraud.serving.bento_service:FraudScoringService` → service
initialized, listening :3000. POST /score returned a well-formed
FraudScoreResponse (calibrated probability 0.0065 for the reference
payload) with full provenance.

**Pinned-model identity (served == on-disk == DVC pointer):**

- schema_version: fraud-scoring/1.0.0
- artifact_name: xgb_mvm.ubj
- artifact_sha256: c623c3a604193ee4636fcb4da90caf298e5302c6509e6d35b7883eea625728c0
- platt_a: 0.8340317182779828
- platt_b: -3.286447786452075

Cross-check: Get-FileHash of the workspace artefact matches the
provenance sha256 exactly.

## 4. G9 — Latency (authoritative)

Harness: `scripts/g9_latency.py` — httpx persistent client, 20 warm-up
requests, 1,000 sequential timed requests against POST /score.
Reference hardware: Windows 11 workstation — Intel Core i7-11800H
(11th Gen, 8C/16T @ 2.30GHz base), 32 GB RAM.

    runs=1000  min=13.66ms  p50=19.74ms  p95=24.03ms  p99=32.93ms  max=174.50ms

**G9 criterion P99 < 200ms: PASS (32.93ms, ~6x margin).**

Method note: sequential single-client is the honest measure for G9 as
stated (request latency); concurrency/throughput is out of scope for
this gate.

## 5. CL-12 / CL-13 scope (scoped here, built later, own PR)

**CL-12 — Provenance manifest (build-time generation, not
hand-committed).** A platform-side script (per ADR-0009: outside the
vertical) emits `provenance_manifest.json` from the same code path the
service uses — schema_version, artifact_name, artifact_sha256, Platt
params — plus git SHA and build timestamp. Runs as a CI step; attached
as a build artefact. Rationale: the service already computes provenance
live; a hand-maintained JSON would be a second source of truth that can
drift (the D-06 failure class in new form).

**CL-13 — Promotion-gate CI.** A workflow job blocking promotion
unless: (a) manifest sha256 == DVC pointer hash; (b) the cross-side
contract test pair passes; (c) a serve-and-score correctness check
passes on the runner. Latency is NOT gated in CI: runner hardware is
not reference hardware. The authoritative P99 remains a
reference-hardware measurement recorded in gate documents (this one and
successors).

## 6. Residuals (tracked elsewhere, none block this gate)

- ci-devops bare `pytest --cov` collects the entire vertical suite —
  WS-E decision owed (handover incident 7).
- `~$*` gitignore line — housekeeping, next commit.
- Incidents 1–7 of 20 Jul + execution-policy discovery (21 Jul: PS
  `Restricted` policy silently suppressed the conda hook/profile —
  same invisible-environment class as incident 5) → WS-E log.