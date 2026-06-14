# ADR-0007: DVC as the artefact source-of-truth

- **Status:** Accepted (backfilled)
- **Decision Date:** June 2026 (B1 foundation; reinforced at B4 artefact pinning)
- **Recorded Date:** 2026-06-14
- **Decision Type:** Backfilled
- **Deciders:** Mike Kennelly
- **Relates to:** ADR-0006 (serving model source) - 0006 rests on this decision
- **Evidence:**
  - `verticals/fraud/dvc.yaml` and `dvc.lock` - the pipeline stages and pinned outputs.
  - ADR-0006, which specifies serving loads DVC-pinned, content-hash-verified artefacts
    and explicitly does not use an MLflow Registry.
  - Architecture v1.0b infrastructure-split table: MLflow listed as "metadata server"
    (run-tracking), not as an artefact registry; artefact backup is object storage.
  - B4 close: the dvc.lock re-pin commits and the byte-perfect MLflow-backstop recovery
    of a CRLF/DVC hash drift - operating proof that DVC hashes are the trusted reference.

> This ADR records a decision already in operation and does not imply it was made on the
> Recorded Date.

## Context

The platform needs one trusted source of truth for model artefacts (trained models,
calibrators, and their lineage), pinned by content so that the artefact served is provably
the artefact trained and validated. Two candidates exist in the stack: the MLflow Model
Registry, and DVC. MLflow is already present for experiment and run tracking. The serving
design (ADR-0006) needs to load a specific, immutable artefact by a verifiable identity.

## Decision

DVC is the artefact source-of-truth. Artefacts are versioned and pinned by DVC content
hash; the serving path loads by that hash. MLflow is used for run and metric tracking only
- it is not the artefact registry and is not on the serving path. The two are separated by
role: DVC owns artefact identity and provenance; MLflow owns experiment history.

## Alternatives considered

- **MLflow Model Registry as source-of-truth** - rejected: splits artefact identity across
  two systems, puts a registry dependency on the serving path, and gives weaker
  content-hash provenance than DVC's hashing.
- **Object store + manual versioning** - rejected: no built-in content-hash provenance or
  pipeline lineage; reintroduces the training-serving drift this decision exists to prevent.

## Consequences

- **Positive.** Content-hash provenance end to end; serving pins by DVC hash (ADR-0006);
  artefact identity is verifiable in an audit. MLflow stays metadata-only, matching the
  architecture's infra split.
- **Platform-level.** This is a platform decision, not a fraud-vertical one: every vertical
  inherits DVC-as-store at B10. (A WS-B P-B3 platform/vertical line item, answered for the
  artefact-store slice: platform.)
- **Obligation.** The DVC remote/storage and the pin-by-hash discipline must be a platform
  capability the verticals consume, not re-established per vertical.
- **Interaction with ADR-0006.** 0007 decides where artefacts live and how they are
  identified; 0006 decides how the serving path loads them. Read together.
