# SESSION HANDOVER — ArcaAI (close of 2026-07-24)

*Supersedes SESSION_HANDOVER_2026-07-23b. This session: **B6 CLOSED —
GATE PASSED** (PR #22, merge `8167f05`, both CI pipelines green).
inc5 e2e latency vs R7 passed with 3.6× headroom; en route it caught
and fixed a real provenance-schema defect (WS-E 34). WS-E ledger now
at 34 items with two trialled rules performing. Programme Governance
Checkpoint 01 pack drafted — next session opens with it.*

## Boot line (paste to resume)
> Resume ArcaAI — B6 GATE PASSED (PR #22, `8167f05`; evidence
> docs/build/B6_GATE.md). **NEXT: Programme Governance Checkpoint 01
> ("WS-D part 0")** — pack at docs/governance/GOV_CHECKPOINT_01_PACK.md
> [COMMIT FIRST — see boarding note]. Circulate Part 1 + prompt to
> Grok and ChatGPT, three-round protocol, findings triaged
> Must-Fix/Should-Fix/Observation. Checkpoint findings then shape the
> WS-D Build & Quality Plan session proper (carries CL-10). Build
> work (B7 Fraud RAG) resumes after WS-D unless the panel finds
> otherwise. Boot ritual: conda activate `arcaai` → git switch main →
> git pull --ff-only → git fetch --prune. No live services needed for
> the checkpoint session.

## What was done (24 Jul)

### B6 inc5 — e2e latency gate — PR #22 (merge `8167f05`)
- Harness `scripts/b6_inc5_latency.py`: full graph, both live flags,
  INTAKE_FIXTURE, cold-first-then-warm design, gate on warm max
  (conservative stand-in for P99 at n=20; no P99 claim from n=20).
- **Results:** warm n=20 min 3.58 / median 3.64 / mean 3.68 / max
  4.10s vs 15s conversational SLA — PASS. Also inside the 10s API
  line. True cold (ollama stop, load + first gen): 7.41s — reported,
  not gated, also inside both lines. Post-reload warm 3.37–3.85s
  confirms representativeness. ~3.6s vs inc4's 1.82s estimate is
  output length + orchestration + HTTP hop, not regression.
- Scoring rung cited from B5 G9 (~33ms); retrieval rung deferred to
  B7 (deliberate, recorded in gate doc).
- Gate doc: docs/build/B6_GATE.md (B5 house pattern).

### Defect caught and fixed: provenance key mismatch (WS-E 34)
- First live e2e run failed immediately: packaging.py read
  prov["sha256"] and prov["platt_params"]; score node emits
  artifact_sha256 and platt_a/platt_b (as its own tests assert).
- The platt variant was the worse defect: no exception — a governed
  note stating calibration params absent when present.
- Root cause: inc4's canned fixture was invented, not derived from
  live score-node output. Unit tests green at every layer; defect on
  first contact between layers.
- Fix: packaging.py conformed to live keys; fixtures consolidated to
  **agent/fixtures.py** (INTAKE_FIXTURE = inc3 vector; SCORED_FIXTURE
  = live-shaped provenance with the real B5 sha). Rule embedded in
  the module docstring: do not invent canned shapes.
- Prompt relabel rider ("sha256 (prefix)" → "artifact prefix") folded
  into the same touch; live-verified.

### WS-E ledger: items 30–34 committed
- 30 Notepad clobber (now with Exhibit B: BUILD_TRACKER wholesale
  overwrite, caught pre-add same session — tripwire's second save).
- 31 chained-paste rule · 32 boarding-checklist rule · 33 stale
  scrollback (extends 14/25) · 34 provenance mismatch.
- Both trialled rules used throughout this session and both
  caught/prevented real failures. Proposed for ratification at the
  checkpoint (Q4).
- 2026-07-23b handover archived to docs/governance/.

### Programme Governance Checkpoint 01 — pack drafted
- Finding zero: no programme-level checkpoint exists on the plan;
  governance is entirely event-driven. Last full panel round was
  WS-B (~2 Jul).
- Pack drafted (state summary + panel prompt, Q1–Q7 incl. schedule
  re-baseline, CL backlog aging, rule ratification, cadence DEC,
  panel composition). Runs as "WS-D part 0".

## Boarding note for next session (FIRST ACTIONS)
1. **GOV_CHECKPOINT_01_PACK.md is NOT yet in the repo** — drafted
   after PR #22 merged. First action: place at docs/governance/,
   micro-PR (with this handover aboard, same pattern as tonight's
   archive commit). Boarding checklist: pack + this handover, two
   files, nothing else.
2. Then circulate to panel and open Round 1.

## Findings / riders (carried)
- WS-E 1–23 backfill from handover archive (hygiene session; source
  material 07-20..07-23 in D:\Downloads; delete stale unsuffixed
  07-22b — repo copy is reference).
- decisions/ → adrs/ rename: NAMED BACKLOG (two strikes).
- Locked-suite disk sprawl purge (D:\ArcaAI-locked\, Downloads strays,
  superseded BA v1.0 in SmartDog_V4\docs\CURRENT\).
- CL-17/19/20 bundle → next Banking Architecture revision (checkpoint
  Q3 will test this).
- prompts/ scaffold decision deferred to B8 (unchanged).
- `git show <merge-commit> -- path` prints empty for clean merges —
  range diff (`git diff A..B -- path`) is the truth-teller. Mental
  note, not a WS-E item.
- Console mojibake on Get-Content without -Encoding UTF8 is
  display-only; git diff renders true bytes.

## Environment
- Unchanged. arcaai conda env (Python 3.11.15). For B7 later:
  ChromaDB comes into scope; BentoML/Ollama not needed for the
  checkpoint session.

## Governance state
- **B6 GATE PASSED** · B1–B6 all gated · WS-A/B/C CLOSED ·
  CL-12/13 CLOSED · WS-E in-repo at 34 items, 2 rules trialled ·
  **NEXT: Governance Checkpoint 01 → WS-D (CL-10) → B7** ·
  Open CL backlog: CL-06..09, CL-11, CL-16..20 (checkpoint Q3
  reviews aging) · DEC through 0008, ADR through 0009.
