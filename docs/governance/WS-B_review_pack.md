# Governance Review — Workstream B pack: Architecture & design coherence

**v0.2 (2 Jul 2026):** WS-A now CLOSED — head-start evidence folded into §2a;
BentoML question in Q-B3 updated (ruled platform standard, ADR-0008). Still
pending before send: the §5 source-tree pull.

Second workstream of the ArcaAI governance review. WS-A (decision-system integrity)
is CLOSED (14 Jun): the two colliding `ADR-` namespaces are separated (`ADR-NNNN` =
formal architecture decisions in `decisions/`; `DEC-NNNN` = the build/design log),
and the architecture decisions below are the baseline this workstream checks the build
against. Take **positions** on §4 — do not approve. Challenge Claude's positions (§3).

**Caveat:** unlike WS-A (which had repo greps), WS-B's evidence is partial. §3 are
**hypotheses to test**, not findings. §5 lists the evidence to pull before final
consolidation.

---

## 1. What the architecture claims (the ADRs)

- **ADR-0001:** ArcaAI ships *reference* models (not production); the bank upskills them
  on its own data through Arca's pipeline. Liability sits with the bank for production.
- **ADR-0002:** three-stage lifecycle — **Stage 1** reference modelling (Arca-owned),
  **Stage 2** upskilling (bank-owned, using Arca's pipeline, inside the bank's
  perimeter, approved by the bank's Model Risk), **Stage 3** continuous improvement
  (bank-owned; drift-triggered retraining). Pipeline must integrate with the bank's
  data warehouse, feature store, and Model Risk tooling at Stage 2/3.
- **ADR-0003:** **pipeline-as-platform** — the upskilling + continuous-improvement
  pipeline *is* the product. Reference models are inputs. The bank adopts Arca's
  pipeline as its ML operating environment for the verticals covered.
- **ADR-0006:** serving loads DVC-pinned artefacts (no MLflow Registry); content-hash
  provenance; parity-tested. (Bank-registry reconciliation at Stage 2/3 deferred to a
  future ADR — noted below as a tell.)
- **ADR-0007 (backfilled):** DVC is the artefact source-of-truth — **platform-level**.
- **ADR-0008 (backfilled):** BentoML is the **platform serving standard** (not
  fraud-local). Layer boundary: BentoML serves models (L4); FastAPI is the
  system-integration API (L1); the LangGraph agent (L2) is the single caller of model
  endpoints.

## 2. What's been built (as understood — confirm in §5)

- Fraud vertical, gates Phase 0 + B1–B3 passed; B4 = baseline + MVM + calibration
  (XGBoost + Platt); B5 = serving (inc1 done: BentoML service, DVC-pinned model, parity
  test). Anti-leakage suite (L1–L12; rolling `closed="left"`, `.shift(1)`). Stack:
  Docker/WSL2, postgres, MLflow (run-tracking only), DVC (artefact store).
- Code lives under `verticals/fraud/…` (e.g. `verticals/fraud/synthetic/generator.py`).
- **B10** is planned to *replicate the fraud vertical across other verticals.*

### 2a. Confirmed evidence (from WS-A close, 14 Jun)

- A **top-level `contracts/` directory exists** (`contracts/fraud_scoring.py`) —
  evidence of *intended* platform/vertical separation. But the contract is
  **fraud-named**: right shelf, not yet a vertical-neutral object. P-B1 is live;
  treat this as partial evidence, not resolution.
- Two P-B3 slices are **pre-answered by ratified ADRs**: serving framework =
  platform-level (ADR-0008); artefact store = platform-level (ADR-0007).
  Anti-leakage, calibration, and provenance remain open — take positions on those.

## 3. Claude's positions (hypotheses — challenge them)

- **P-B1 (platform vs vertical boundary).** Everything built so far is the fraud
  vertical. The `verticals/fraud/` path *suggests* a multi-vertical layout was intended,
  but it is unconfirmed whether a reusable **platform/core** exists distinct from the
  vertical, or whether platform logic currently lives *inside* the fraud vertical. If
  the latter, "pipeline-as-platform" (ADR-0003) is aspirational, and B10 ("replicate the
  vertical") will copy fraud-specific code N times rather than instantiate a template.
  **This is the central coherence risk.**
- **P-B2 (lifecycle is Stage-1-heavy).** The build proves **Stage 1** (Arca produces a
  reference model and serves it). **Stage 2/3** — the upskilling pipeline the *bank*
  runs in its perimeter, Model Risk integration, the drift/retrain loop — is asserted in
  ADR-0002 but may be largely undesigned. ADR-0006 deferring the Stage-2/3 bank-registry
  reconciliation is the tell. Yet Stage 2/3 is where the *product value* (the pipeline
  the bank operates) and the recurring revenue live (ADR-0003).
- **P-B3 (quality machinery should be platform-level).** Anti-leakage, calibration,
  provenance, and the serving contract are almost certainly needed by *every* vertical.
  If they're implemented fraud-local, B10 re-implements them per vertical — drift and
  inconsistency follow. They should be platform capabilities the vertical *consumes*.
- **P-B4 (spec drift).** The architecture specs (`docs/specs/02`, `04`) were written in
  the May design phase; the build is June. Likely drift between spec and code, untracked.

## 4. Questions — take a position on each

Q-B1. Is there a clean platform/vertical separation, and **how would you test it**?
What concrete evidence distinguishes "a template" from "a bespoke fraud build with
aspirations"? (Challenge P-B1.)

Q-B2. Is the three-stage lifecycle architected beyond Stage 1? What is the **minimum
Stage-2/3 architecture** that must exist before "pipeline-as-platform" can honestly be
claimed to a bank? (Challenge P-B2.)

Q-B3. Which capabilities are **platform-level** vs **vertical-level** — anti-leakage,
calibration, provenance, feature pipeline? Serving framework and artefact store are
already ruled platform-level (ADR-0008, ADR-0007) — challenge those rulings if you
disagree, otherwise draw the line for the rest. (Challenge P-B3.)

Q-B4. Is **B10 (replicate the vertical)** the right strategy as stated, or does the
architecture need an explicit **platform-extraction** step first? What breaks at
vertical #2 if not?

Q-B5 (red-team). A bank's *architecture* reviewer (not Model Risk — the architect) is
walked through this. Where is the "platform" claim most exposed? What's the question
they ask that there isn't a good answer to yet?

## 5. Evidence to pull (before final consolidation)

- Source tree of `verticals/` and any `platform/`, `core/`, `pipeline/`, `src/` dirs —
  the single most decisive artefact (does a platform core exist distinct from the
  vertical?). PowerShell: `Get-ChildItem -Recurse -Directory | Select FullName`.
- `docs/specs/02-solution-architecture/` and `docs/specs/04-data-and-ml/` — to check
  spec↔build alignment.
- Any Stage-2/3 / upskilling design doc (or confirmation none exists yet).
