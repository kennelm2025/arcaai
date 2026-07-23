# SESSION HANDOVER — ArcaAI (close of 2026-07-23)

*Supersedes SESSION_HANDOVER_2026-07-22b. This session: DEC-0008 recorded
(PR #17, merge `7f9cdab`) after a misfile into the ADR register was caught
and guarded; B6 OPENED and driven through THREE increments (PRs #18 merge
`4aaf192`, #19 merge `24080b6`), all green. Agent layer now scores real
transactions through the B5 service. Two new WS-E incidents (28–29) plus
one footnote. No closure debt, no recording debt.*

## Boot line (paste to resume)
> Resume ArcaAI — B6 IN PROGRESS, three increments merged and green
> (inc1 LLM smoke + TI7 pin, inc2 hello-graph, inc3 fraud score node
> over HTTP to the B5 service). **NEXT: B6 inc4 — the packaging node**:
> replace `package_stub` with a Llama 3.1 8B node (`ChatOllama`,
> temperature=0) that turns state's score + provenance into governed
> analyst prose. This is the first graph↔LLM join; expect prompt-shape
> churn. Then inc5: end-to-end latency vs R7 (5–10s typical, <15s SLA;
> warm 8B measured 0.5s for short output, budget comfortable) → B6 gate.
> Boot ritual: conda activate `arcaai` → git switch main →
> git pull --ff-only → git fetch --prune — all four. For inc4 also:
> Ollama serving (`ollama list` shows llama3.1:8b) and for integration
> tests `bentoml serve verticals.fraud.serving.bento_service:FraudScoringService`
> in a second terminal.

## What was done (23 Jul)

### DEC-0008 recorded — PR #17 (merge `7f9cdab`)
- s3store default-remote switch recorded in DECISIONS.md, house bullet
  style, placed after DEC-0007. Platform-endgame stays PARKED.
- Misfile caught: entry had been duplicated as `decisions/00010-*.md`
  (ADR register) with a wrong five-digit DEC number. File was untracked
  — deleted, never entered history. Register-scope guard added to
  decisions/README.md (WS-E 28).
- Both the recording gap and the misfile are CL-08 evidence.

### B6 inc1+2 — PR #18 (merge `4aaf192`)
- inc1: tests/test_llm_smoke.py — ChatOllama round trip + TI7 pin check
  (asserts llama3.1:8b present); self-skips when Ollama absent (CI).
  Warm inference 0.5s on the RTX 3070 (8GB). Deps floored in
  pyproject.toml: langgraph>=1.2.9, langchain-core>=1.5.0,
  langchain-ollama>=1.1.0, ollama>=0.6.2.
- inc2: `agent/` package (platform-side per ADR-0009) — minimal
  deterministic graph intake→score_stub→package_stub; stub score −1.0
  sentinel (fails loud if leaked); named slot reserved for the B8
  injection detector; 3 CI-safe structural tests.
- First push went red: ruff W292 (here-strings lack trailing newline) —
  fixed with ruff --fix, commit amended, force-with-lease (WS-E 29).
- Tracker: B6 → IN PROGRESS; stale "Next DEC number" line replaced with
  a drift-proof pointer.

### B6 inc3 — PR #19 (merge `24080b6`)
- agent/scoring.py: score_transaction + score_node — HTTP to the B5
  BentoML service via the fraud-scoring contract. Imports contract
  types ONLY, never verticals.fraud (ADR-0009 boundary held at the
  import level). Full provenance (sha256, Platt params) flows into
  agent state for inc4/audit. URL via ARCAAI_FRAUD_SCORING_URL
  (default http://localhost:3000). Fail-loud: no fallback score.
- graph.py: state gains `provenance`; build_graph(live_scoring=False)
  — default keeps CI stub-only; True wires the real node.
- Tests: 2 CI-safe (stub default; ValidationError on bad transaction
  BEFORE any network call) + 2 integration (self-skip without service;
  live run asserts probability >0.5 on a fraud-flavoured vector, checks
  provenance shape incl. 64-char sha256). Probe scored 0.9865 on the
  dodgy vector — model behaving. Ruff B017 caught a blind
  raises(Exception); tightened to ValidationError.
- Bento serve incantation (from the service docstring):
  `bentoml serve verticals.fraud.serving.bento_service:FraudScoringService`

## Incidents (WS-E — add as 28–29)
28. **DEC misfiled into ADR register.** DEC/ADR namespace separation
    held on paper, failed at filesystem level — the ADR folder is named
    `decisions/`, inviting it. Guard paragraph added to
    decisions/README.md. Candidate: rename folder `adrs/` someday.
29. **Here-string writes omit trailing newline → ruff W292 in CI.**
    RULE: run `ruff check --fix` locally before any Python-touching
    commit (joins the git-diff eyeball). Amend-and-force-with-lease is
    the fix pattern pre-merge on own PR branch; never post-merge.
- Footnote to 14/25: git log decoration reflects LOCAL refs; a prune
  racing a just-deleted remote branch leaves ghost decoration. The
  prune is the truth-teller, not the decoration.

## Findings / riders (small, non-blocking)
- **Locked suite location**: canonical copies ARE in the repo at
  docs/governance/ (all five, 13 Jun). Disk sprawl found: redundant
  full set at D:\ArcaAI\locked\, v0.x strays in Downloads ×2 and
  _legacy, and — the hazard — a SUPERSEDED Banking_Architecture_v1_0
  inside SmartDog_V4\docs\CURRENT\. Hygiene purge someday; add one
  line to repo README or DECISIONS lock table: "authoritative copies:
  docs/governance/".
- docs/specs/ tombstones work (redirect correctly); spec 03 was never
  written — its territory (deployment topology, sizing) resurfaces
  when platform-endgame unparks, likely as a TI revision (CL-17-ish).
- Failed CI runs: prefer keeping them (incident evidence) over deleting.

## Environment
- Unchanged plus: llama3.1:8b pulled (ID 46e0c10c039e, same weights as
  existing :latest tag). Ollama 0.18.3. RTX 3070 8GB confirmed.
- websockets downgraded 16.1.1→15.0.1 by langgraph-sdk; BentoML/uvicorn
  imports verified healthy after.

## Governance state
- WS-A/B/C CLOSED · CL-12/13 CLOSED · **B6 IN PROGRESS (3 of ~5 incs)**
  · WS-D next governance session (Build & Quality Plan; carries CL-10)
  — deliberately deferred in favour of B6 this session · WS-E ledger
  1–27 + pending 28–29 · Open CL backlog unchanged: CL-06..09, CL-11,
  CL-16..20.
