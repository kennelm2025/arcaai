# Governance Review — Workstream A pack: Decision-system integrity

You are one of three reviewers (with the repo author and Claude) on a governance
review of ArcaAI, a solo-built, AI-assisted banking-AI platform. This is the
first workstream: the **decision record system itself**. A routine ADR review
found the system had drifted in ways invisible in isolation, and a follow-up
sweep found the drift is structural, not cosmetic. Take **positions** on the
questions in §4 — do not approve. Where Claude has a position (§3), challenge it.

---

## 1. The setup — TWO parallel "ADR" series

- **Series 1 — formal ADRs, `decisions/` folder, four-digit (`ADR-0001`).**
  Immutable, one Markdown file each, governed by a README (copy `_template.md` →
  next sequential number → PR → discuss → merge; `Proposed → Accepted` at merge;
  accepted ADRs never edited; significance test gates what qualifies). Files:
  0001 reference-model positioning, 0002 three-stage lifecycle, 0003
  pipeline-as-platform, 0006 serving model source; 0004/0005 reserved
  (Target Market, Data Strategy — deferred, unwritten); `_template.md`, README.
  **Subject matter: platform/product architecture.**

- **Series 2 — `DECISIONS.md` log, repo root, three-digit (`ADR-001`).** A running
  ledger of design/build/document-phase decisions, referencing "rulings R1–R13."
  Entries include: **ADR-000** (image round deferred — open, gates client use),
  **ADR-001** (executive-deck raster fixes — closed), **ADR-003** (mortgage
  process-orchestration pattern added — closed), **ADR-004** (content-hash ns-pin
  / pandas fix — closed). Cited from `generator.py`, `B3_GATE.md`,
  `CURRENT_STATE.md`, `BUILD_TRACKER.md`. **Subject matter: documents, decks,
  diagrams, synthetic-data tactics.**

## 2. What the audit found (evidence, not memory)

- **Namespace collision across two series — three numbers double-booked:**
  - `ADR-001`: deck-raster fixes (S2) vs reference-model positioning (S1)
  - `ADR-003`: mortgage orchestration (S2) vs pipeline-as-platform (S1)
  - `ADR-004`: pandas ns-pin (S2) vs Target Market (reserved S1)
  Same citation string → different decision. The three- vs four-digit form is the
  *only* tell, and it isn't used consistently.
- **`ADR-000` identified:** a real, open Series-2 decision (image round, gates
  client use) — not a dangling reference to a missing formal ADR.
- **Reserved-but-unwritten formal ADRs:** 0004 (Target Market) and 0005 (Data
  Strategy) cited across planning docs since May, deferred, gating Spec 01 §6.
- **Not under version control:** a `git mv` on the new serving ADR returned
  `fatal: not under version control` — the file was never committed. An ADR that
  exists only in the working tree is not immutable; immutability is enforced by
  git history, not by the README.
- **Undocumented significant decisions (to re-triage):** DVC-as-artefact-store
  (ADR-0006 rests on it), XGBoost, BentoML. NOTE some choices *are* recorded in
  Series 2 / rulings (Platt-over-isotonic = G7; orchestration pattern) — check
  there before declaring a gap.
- **Process vs practice:** README implies ADR-first; recent decisions were made
  in code first and documented after — the root-cause pattern.

## 3. Claude's positions (challenge these)

- **P-A1 (one canonical namespace).** The four-digit `decisions/` series is
  canonical "ADR." Rename Series 2 out of the `ADR-` namespace (`DEC-NNN`, a
  design/build decision log); update the four citations. Then triage Series 2:
  entries that clear the significance test (candidate: the mortgage orchestration
  pattern) are **promoted** to fresh four-digit ADRs; the rest stay `DEC-` log
  entries.
- **P-A2 (triage undocumented decisions using the existing ADRs).** DVC-as-store
  → backfill ADR (foundational; 0006 depends on it). XGBoost / Platt → Model Card,
  not ADR (ADR-0003 classes the model as an *input, not the product*). BentoML →
  fold into ADR-0006. Re-check each against Series 2 / rulings first.
- **P-A3 (stop reserving).** Honour the existing 0004/0005 reservations; number
  ADRs at creation thereafter; planning docs refer to unwritten ADRs by name.
- **P-A4 (backfill + commit integrity).** Backfilled ADRs carry both a *Decision
  Date* and a *Recorded Date*, flagged as reconstructed, pointing to
  contemporaneous evidence (commit SHA / log entry / code comment). AND every ADR
  must be committed — an uncommitted ADR has no immutable trail. Template needs a
  backfill field; process needs a commit check.
- **P-A5 (capture at the gate).** Add a decision-capture step to every gate
  review ("what significant decisions were made; are they recorded?") rather than
  mandating ADR-first.

## 4. Questions — take a position on each

Q-A1. Two ADR series collide at three numbers. Unify into one series (renumber,
breaks citations) or separate the namespaces (rename Series 2)? If separate, what
is the boundary and notation? (Challenge P-A1.)

Q-A2. For DVC-as-store / XGBoost / BentoML / Platt — ADR, Model-Card, fold-in, or
nothing? Apply the significance test. (Challenge P-A2.)

Q-A3. Reserve ADR numbers, or assign only at creation? Handle the already-cited
0004/0005 how? (Challenge P-A3.)

Q-A4. How do you backfill a months-old decision into an immutable,
audit-trail-for-banks system without it reading as fabrication — and how do you
enforce that "immutable" is real (vs uncommitted working-tree files)? (Challenge
P-A4.)

Q-A5. Minimal process change that stops significant decisions reaching a gate
undocumented, without ceremony a solo founder abandons? (Challenge P-A5.)

Q-A6 (red-team). Rank the §2 findings by how badly each undermines the
"defensible audit trail" claim to a bank Model Risk reviewer. Which is worst?
