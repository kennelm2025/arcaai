# ADR-0006 — Serving model source: DVC-pinned artefacts, not an MLflow Registry

**Status:** Accepted
**Date:** 14 June 2026
**Decider:** Mike Kennelly
**Supersedes:** none
**Related:** ADR-0001 (pre-trained model positioning), ADR-0002 (three-stage model lifecycle), ADR-0003 (pipeline-as-platform)

> Numbering: formal `decisions/` numbers **0004** and **0005** are reserved for the deferred strategic ADRs **Target Market Segment** and **Data Strategy** (cited across planning docs since May 2026, not yet written), so this serving ADR is **0006**. Note: `DECISIONS.md` separately uses "ADR-004" for the pandas ns-pin decision — a cross-ledger namespace collision to resolve (see README audit note), unrelated to this ADR. Status flips `Proposed → Accepted` at merge.

---

## Context

B5 builds the **serving component of the pipeline** — the platform product per ADR-0003 — and needs an unambiguous source for the model it scores against.

In B4 the calibrated MVM is logged to MLflow only as a **loose run artefact**. There is no MLflow Model Registry, so there is no registered name/version/stage to resolve at serving time. The reproducible source of truth for the trained model is therefore the DVC-pinned B4 outputs:

- `data/fraud/models/xgb_mvm.ubj` — the XGBoost booster
- `data/fraud/models/platt_scaler.json` — the Platt parameters `{a, b}`

**Stage scoping (important — prevents mis-application at B10).** This serving component is currently exercised on the **Stage-1 reference model** (ADR-0002, Stage 1). Per ADR-0001 a reference model is explicitly *not* authorised for production decisioning on a bank's customer data. The same *mechanism* is what a bank operates at Stage 2/3 inside its own perimeter, but **no Stage-2/3 deployment is in scope at B5**. Stating this here stops the pattern being read as a production-serving contract and copied as such when the vertical is replicated at B10.

A serving unit must also not drag the trainer into the Bento: importing `calibrate_mvm` would pull the training stack (and its dependencies) into the serving image. The scoring composition itself is a two-line monotone map (`p = sigmoid(a*margin + b)`).

## Decision

1. **Model source.** `FraudScorer.from_pinned_artifacts()` loads the DVC-pinned B4 booster and Platt scaler directly from `data/fraud/models/`. Serving has **no MLflow runtime dependency**. Serving consumes a specific `(git commit, DVC revision)` pair; **promotion** is a pin bump in a reviewed commit; **rollback** is reverting the pin.

2. **No trainer import.** `scorer.py` re-states the margin→Platt→probability map rather than importing `calibrate_mvm`. Byte-identity to the offline pipeline is not assumed — it is **enforced** by `test_serving.py` (`test_serving_matches_offline_calibration`, `assert_array_equal`).

3. **Provenance.** Each response carries `ModelProvenance` — `schema_version`, `artifact_name`, `artifact_sha256`, `platt_a`, `platt_b`. The response schema stays **minimal**. Richer lineage (training `run_id`, `git_sha`, `dataset_rev`) is **not** added to the per-score response — the scorer loads two files off disk and cannot authoritatively supply it. Instead, **B4 emits a sidecar provenance manifest** (e.g. `data/fraud/models/provenance.json`) that the scorer may load and attach to **logs/observability**, not to the customer-facing scoring contract.

4. **Registry stance — deferred, not rejected.** No Registry today. The decision is revisited when any of these triggers appear: multi-model serving, multiple model authors, or a Stage-2/3 bank that mandates registry-based promotion inside its perimeter (see Scope boundary below).

5. **Promotion gate.** A pre-merge CI check instantiates the scorer **from the proposed pinned artefacts** and runs parity + schema contract + calibration invariants + latency budget, failing the merge on violation. DVC integrity proves *these are the bytes*; the gate proves *these bytes are the right, correctly-scoring model*. Cheap insurance that pays off once multiple verticals exist at B10.

## Scope boundary and deferred work

Model resolution in **customer-operated (Stage 2/3) environments** is out of scope here and deferred to a future ADR, *"Model resolution in customer-operated environments."*

The intended split is recorded now so it is not reconstructed under pressure later:

- The **bank's registry / Model Risk process is the promotion and approval authority** at Stage 2/3. Per ADR-0002's ownership split and ADR-0001's liability split, Arca's DVC pin must **not** be the production authority — "production is whatever Arca's pin points at" is precisely what a regulated bank rejects, and would re-create the model-risk liability ADR-0001 exists to avoid.
- The **content hash remains the byte-identity** that the bank's registry reference *resolves to*. The pipeline keeps DVC-pin reproducibility as the identity anchor; the bank's tooling holds approval and rollback authority. These are different axes and do not conflict.

## Consequences

### Positive

- **Reproducible** — the content hash pins the exact served bytes; any score is reproducible from its provenance.
- **Lean serving image** — no MLflow client, no training stack in the Bento.
- **Single mechanism** — the DVC pin is the same artefact CI, the promotion gate, and the B5 gate doc all measure.
- **Self-contained** — a pipeline-owned resolution mechanism, consistent with pipeline-as-platform (ADR-0003); depends on no one's Registry.

### Negative / costs / risks

- **No registry-mediated promotion at the Arca layer** — promotion is a manual pin bump via PR. Acceptable for a solo build; the promotion gate (decision 5) is the safety.
- **Duplicated serving logic — the B10 scaling risk.** The re-stated map is trivial today, but as the serving composition grows (thresholding, policy overrides, reason codes, confidence adjustment) the parity surface grows and "re-state, don't import" gets expensive. **Tripwire:** when the serving composition outgrows a trivial monotone map, revisit whether re-statement still beats a shared, separately-packaged inference module. The parity test is the standing mitigation and **must remain a hard, non-skippable CI gate**.
- **Bank-coordination visibility — the Stage-2/3 risk.** A mature bank with its own registry, CI/CD, and approval gates may find "bump a DVC pin in a PR" invisible or bypassing of its process ("where is the model approval record?"). Mitigated by the future-ADR bridge above; will require integration work and diplomacy around B8–B10.
- **Content-hash-only provenance is sufficient for *scoring* reproducibility but not full lineage** — the sidecar manifest (decision 3) closes the audit gap at the pipeline level without bloating the response.

## Compliance with related ADRs

- **ADR-0001** — consistent. Serving the reference model is Stage-1 infrastructure, not production decisioning; the liability split is preserved (Arca's pin is not the production authority).
- **ADR-0002** — **not a deviation.** ADR-0002 defines ownership and governance weight per stage and is silent on the artefact-resolution *mechanism*; this ADR fills that gap. The Stage-2/3 bank-tooling integration ADR-0002 mandates is honoured via the future-ADR bridge in Scope boundary.
- **ADR-0003** — positively aligned. A self-contained DVC-pin mechanism belongs to the pipeline as the bank's ML operating environment, rather than coupling serving to anyone's Registry.

## Alternatives considered and rejected

**MLflow Model Registry as the serving source** — rejected. No Registry exists (B4 logs a loose run artefact only). It adds a serving-time dependency and promotion machinery with no payoff for a single-model, single-author build, and a content hash is a stronger reproducibility anchor than a mutable Registry version pointer.

**Import `calibrate_mvm` into the scorer for guaranteed parity** — rejected. Drags the training stack into the serving image (bloat, attack surface, cold-start cost). Replaced by a re-stated map plus an enforced parity test.

**Expand the scoring response with full lineage now** — rejected. The scorer cannot authoritatively supply `run_id`/`git_sha`/`dataset_rev`; adding fields it cannot populate is worse than omitting them. Lineage belongs in the B4 sidecar manifest and observability, not the per-score response.

**Make the bank's registry authoritative as the general pattern now** — rejected as premature. No Stage-2/3 deployment is in scope at B5; deciding it now would bake a customer-environment assumption into Stage-1 infrastructure. Deferred to the future ADR with the authority/identity split pre-recorded.

## Notes

- The 200 ms SLA (G9) is sanity-checked in `test_serving.py`; the authoritative P99 on the pinned model / reference hardware is recorded in the **B5 gate doc**, not here.
- This decision governs the B6 fraud tool and is inherited by every vertical replicated in B10.
