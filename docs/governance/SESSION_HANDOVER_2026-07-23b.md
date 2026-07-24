# SESSION HANDOVER — ArcaAI (close of 2026-07-23, evening session)

*Supersedes SESSION_HANDOVER_2026-07-23 (morning). This session: B6 inc4
CLOSED — packaging node merged (PR #20, merge `b82d21f`), all CI green.
First graph↔LLM join is in main. WS-E incident ledger given an
authoritative in-repo home (docs/governance/WS-E_INCIDENTS.md); handover
archive partially committed after revision forensics. Tracker bump was
omitted from PR #20 and repaired in micro-PR #21 [CONFIRM MERGE + HASH].
Several new incident candidates logged below — a productive night for
the ledger.*

## Boot line (paste to resume)
> Resume ArcaAI — B6 at 4 of ~5 increments, inc4 merged and green
> (packaging node: Llama 3.1 8B via ChatOllama temperature=0 turns
> score + provenance into governed analyst prose; fact-validation
> tripwire, no fallback prose; live_packaging flag keeps CI stub-only).
> **NEXT: B6 inc5 — end-to-end latency vs R7**: full graph run
> (live_scoring=True, live_packaging=True) against the R7 ladder —
> full conversational query typically 5–10s, SLA <15s. Evidence to
> date says comfortable: warm 8B generation measured 1.82s (inc4,
> --durations=0), B5 scoring P99 ~33ms. Measure cold-start separately
> and decide whether it's in or out of SLA scope (recommend: report
> both, gate on warm). Green inc5 → B6 GATE.
> Boot ritual: conda activate `arcaai` → git switch main →
> git pull --ff-only → git fetch --prune — all four. For inc5 also:
> Ollama serving (`ollama list` shows llama3.1:8b) AND
> `bentoml serve verticals.fraud.serving.bento_service:FraudScoringService`
> in a second terminal — inc5 needs both live simultaneously.

## What was done (23 Jul, evening)

### B6 inc4 — packaging node — PR #20 (merge `b82d21f`)
- `agent/packaging.py`: `package_node` — ChatOllama (llama3.1:8b, TI7,
  temperature=0) turns state's score + provenance into a governed
  analyst note, written to `narrative`. Prompt supplies only the facts
  (calibrated score, sha256 12-char prefix, Platt-params-present) and
  forbids invented transaction detail, headers, salutations.
- `validate_prose` tripwire: asserts exact score string and sha prefix
  verbatim in output + minimum length; raises ValueError on failure —
  no fallback prose (consistent with the −1.0 sentinel and the
  no-fallback-score rule).
- `graph.py`: `build_graph(live_scoring=False, live_packaging=False)` —
  dual flags, CI fully stubbed/offline by default. Live packaging
  without live scoring is legitimate (canned-state prompt iteration).
- Tests: 3 CI-safe units (prompt builder, two validator rejections),
  stub-default graph invoke test, self-skipping Ollama integration.
  Full suite 71/71 green.
- **Expected prompt-shape churn did NOT materialise** — first prompt
  draft passed fact validation live. Probe prose eyeballed on the
  0.9865 fixture; one cosmetic fix aboard (suppressed To:/Subject:
  email framing). Warm generation 1.82s.
- Prompt template is a module-level constant in packaging.py — no
  prompts/ scaffold until B8's injection detector forces the issue
  (decision made in-session, unchallenged).

### WS-E ledger created in-repo (aboard PR #20)
- docs/governance/WS-E_INCIDENTS.md is now the authoritative home.
  Items 28–29 in full, 24–27 as summaries, 1–23 reserved for backfill.
- Discovery: NO WS-E item had ever been committed to the repo — the
  ledger lived solely in handover documents. CL-08 evidence in itself.
- Handover archive partially committed: 2026-07-22b and 2026-07-23
  (morning) into docs/governance/ so ledger citations resolve in-repo.
- **Revision forensics**: 07-22b existed in Downloads in two divergent
  versions (8,106 bytes @ 17:13 vs 9,440 bytes @ 17:17 ×2). Hash +
  timestamp identified the later as authoritative; committed under the
  clean name. Live evidence for repo-as-archive over Downloads.

### DECISIONS.md — lock-table pointer (aboard PR #20)
- "Authoritative copies of the locked suite: docs/governance/" added
  below the lock table. Incidental improvement: the companion-documents
  line lost its stray `\&` escape artifacts in the edit shuffle.

#### Tracker fix — PR #21 (merge `c431401`)
- B6 → 4 of ~5 incs (PRs #18–#20); NEXT inc5 (e2e latency vs R7 → gate).
  Omitted from PR #20 despite five prompts; repaired same evening.
  Also fixed en route: two stray trailing pipes in the tracker table
  (B6 row, then B9.5 row). Remote branch was briefly pushed EMPTY
  before the commit landed (chained-paste add-skip aftermath) — compare
  page showed "identical"; second exhibit for incident candidate 2.
  See incident candidates.

## Incident candidates (WS-E — number when adding, likely 30+)
1. **Notepad session clobbered DEC-0008 out of DECISIONS.md.** An
   unrelated region of the file was deleted during the pointer edit.
   Caught at the pre-add `git diff` eyeball; restored from HEAD, edit
   redone. The house diff rule paid for itself — commit this one as an
   incident, it's the strongest possible advert for the rule.
2. **Chained multi-command pastes bit twice.** (a) ruff/pytest chain
   swallowed the pytest output; (b) commit+push chained past a skipped
   `git add` — commit no-op'd, push shipped an empty branch (Total 0).
   Candidate RULE: ship-critical git sequences run one command per
   prompt, read each output before the next.
3. **Boarding-item attrition.** BUILD_TRACKER bump was asked five
   times across the session and still missed the commit. Pattern:
   items that live only in chat scroll get lost. Candidate RULE: a
   written boarding checklist (scratch file or PR draft) ticked before
   `git add`, not a mental list.
4. Footnote: stale pasted scrollback misled twice more (old graph.py
   content, pre-pull decoration). Extends 14/25: `git log` /
   `Select-String` are the truth-tellers, not terminal history.

## Findings / riders
- **`decisions/` → `adrs/` rename: upgraded to NAMED BACKLOG** (second
  strike in two days — the misfile on the 22nd, tonight navigating to
  the wrong folder for DECISIONS.md).
- Prompt labelling rider (inc5): prose calls the sha256 prefix "hash";
  relabel in the prompt ("artifact prefix"). Validator already anchors
  the true value — cosmetic, fold into inc5's touch of the area.
- WS-E 1–23 backfill from handover archive: hygiene session. Source
  material: full run 07-20..07-23 sits in D:\Downloads; commit the lot
  to docs/governance/, then dedupe Downloads. Known stale file: the
  UNSUFFIXED 07-22b in Downloads is the early revision — delete it;
  the repo copy is the reference.
- Locked-suite disk sprawl purge: unchanged from morning handover
  (D:\ArcaAI\locked\, Downloads strays, superseded BA v1.0 in
  SmartDog_V4\docs\CURRENT\).
- pytest `-v` is overridden by pyproject config (dots regardless);
  use `-vv` or `--durations=0` for per-test visibility.

## Environment
- Unchanged from morning handover. Warm llama3.1:8b generation for
  short governed prose: 1.82s measured (RTX 3070 8GB).

## Governance state
- WS-A/B/C CLOSED · CL-12/13 CLOSED · **B6 at 4 of ~5 — inc5 (latency
  vs R7) then B6 GATE** · WS-D next governance session (Build &
  Quality Plan; carries CL-10) — still deliberately deferred behind
  the B6 gate · WS-E ledger IN-REPO, items 1–29 (+ tonight's
  candidates pending numbering) · Open CL backlog unchanged:
  CL-06..09, CL-11, CL-16..20 · CL-08 evidence pile grew again
  (ledger-never-committed discovery).
