# SESSION HANDOVER — ArcaAI (close of 2026-07-22, PM session)

*Supersedes SESSION_HANDOVER_2026-07-22.md. This session: CLOSURE DEBT
FULLY DISCHARGED via PR #16 (merge `0e48e02`) — CL-12/13 ledger flip with
evidence note + CI diagnostic strip, merged on green with closures aboard
(the merge-discipline candidate rule executed once in anger). Branch
hygiene completed. Two new WS-E incidents logged (24–25). NO closure debt
outstanding.*

## Boot line (paste to resume)
> Resume ArcaAI — closure debt CLEAR (PR #16, merge `0e48e02`, ci-devops
> #35 + ci-mlops #44 green on main). CL-12/13 CLOSED in every sense:
> functionally, in CI, and on the canonical ledger.
> **FIRST TASK (small): DEC entry for the s3store default-remote
> switch** — decided and executed 22 Jul AM but unrecorded; append to
> DECISIONS.md (check tail for next DEC number first — don't guess),
> rationale = AWS over R2 (banks demo/deploy into their own AWS
> estates; endgame = self-contained deployable, banks never touch our
> bucket), cross-ref ADR-0007 (artefact store). NOTE the separate
> platform-endgame decision (AWS as deployment target) stays PARKED as
> candidate — record only the remote switch. Then choose:
> **BUILD B6** (LangGraph agent v0 + Llama 3.1 8B) or **GOVERNANCE WS-D**
> (Build & Quality Plan; carries CL-10). WS-D keeps the build/governance
> alternation and clears the last blocking review work before the agent
> build. Boot ritual (amended): conda activate `arcaai` (prompt shows
> `(arcaai)`) → `git switch main` → `git pull --ff-only` →
> `git fetch --prune` — ALL FOUR before anything else (stale-tree
> incident, this morning).

## What was done this session (22 Jul PM)

### Closure PR — PR #16 (merge `0e48e02`)
- Branch `closure-cl-12-13`, two commits:
  - **`0607659`** — governance: CL-12/13 flipped `[x]` in
    `docs/governance/GOVERNANCE_REVIEW_CHANGELOG.md` (canonical ledger,
    DEC-0007), with a dated closure note inserted before the
    Trail-integrity note. Evidence recorded: PRs #14+#15 jointly,
    promotion-gate green ci-mlops #41/#42. The note also records the
    **deviation from the ADR-0006 literal path**: manifest is generated
    platform-side in CI (same serving code path) and uploaded as a build
    artefact — NOT committed at `data/fraud/models/provenance.json`.
    Deviation is now on the trail, not silent.
  - **`b6a2686`** — ci: four-line AWS secrets diagnostic step removed
    from ci-mlops.yml (incident 16 resolved; step had served its purpose).
- Split into two commits deliberately: flip = governance evidence,
  strip = CI housekeeping — cleaner WS-E trail.
- **Merged only on green**: ci-mlops #43 green on the PR (promotion gate
  re-ran the full S3 pull + sha256 identity + known-answer check with
  the diagnostic gone — remote and repaired platt_scaler re-proven
  healthy). Post-merge: ci-devops #35 + ci-mlops #44 green on main.
- Ledger flip verified live on main post-merge (`git grep` shows `[x]`
  on both + closure note at line 73).

### Branch hygiene completed
- `origin/closure-cl-12-13` auto-deleted on merge; pruned locally.
- Local branches `cl-12-13-provenance-gate` and `closure-cl-12-13`
  deleted. Remote is origin/main only. Local is main only.
- Local main at `0e48e02`, up to date with origin.

## Incidents / process lessons (WS-E ledger — add as 24 onward)
24. **`[IO.File]` relative-path trap**: .NET static methods resolve
    relative paths against the PROCESS working directory
    (`C:\WINDOWS\system32`), not PowerShell's prompt location. First
    attempt at the ledger edit failed loudly (no harm — read and write
    both failed on the same bad path). `Set-Content` never had this
    problem, so the IO.File house rule (WS-E 17) met its first sharp
    edge one session after adoption. RULE AMENDED: **absolute paths
    only for `[IO.File]` calls — resolve via
    `(Resolve-Path 'rel\path').Path` first.** Bonus: Resolve-Path fails
    loudly up front if the path is wrong.
25. **Tidy-up before merge confirmation**: local tidy sequence (switch/
    pull/prune/branch-delete) executed before PR #16 was actually
    merged. `git pull` said "Already up to date" (the tell — main was
    still at `1179abe`); `git branch -d` then deleted `closure-cl-12-13`
    anyway, because **`-d`'s safety check was satisfied by the branch's
    own upstream (origin/closure-cl-12-13), not by HEAD** — the guard
    didn't guard. No loss (commits were on the remote + in the PR), but
    the failure mode is real: `-d` after a push is NOT protection that
    main contains the work. RULE: **confirm merge on GitHub before any
    local tidy-up** — sits beside the merge-discipline candidate (WS-E
    15).
26. **Stale tree at session open**: yesterday's session ended without a
    final pull on main; today opened seven commits behind, producing a
    spurious "can't locate file" on the ledger (the CL-12/13 merge
    hadn't reached the working tree). Fix folded into the boot ritual:
    **pull main + prune at session open**, before touching files.
27. **Long-paste breakage**: the single-command monolith for the ledger
    edit broke mid-paste at a backtick newline literal (`` "`r`n" ``),
    leaving the `>>` continuation prompt (Ctrl+C to abandon; nothing
    ran). Recovery pattern that worked: **split scripted edits into
    short single-assignment steps** ($p, $t, $nl, $note, replace,
    write) — variables persist in-session, each paste too small to
    wrap. Newline literals built via `[Environment]::NewLine` or
    `[char]13+[char]10` instead of backticks. Also proven: the
    **silent-no-op guard** — compare `$t2.Length` vs `$t.Length` and
    print "NO-OP - STOP" before any disk write (companion to the
    git-diff eyeball, catches the failure one step earlier).
- **Prune scope note** (footnote to 14): `git fetch --prune` cleans
  remote-tracking refs only — local branches survive and need explicit
  `git branch -d`. Observed: `cl-12-13-provenance-gate` still local
  this morning despite yesterday's sweep.

## Environment (unchanged from 22 Jul AM handover)
- conda env `arcaai`, Python 3.11.15. Activate before everything.
- DVC 3.67.1 with s3 support. Default remote: s3store
  (`s3://arcaai-dvc-kennelm/dvc`, eu-west-2). Local creds
  `.dvc/config.local`; CI creds repo secrets.
- AWS console: kennelm (972379852538); region picker → eu-west-2.
- ci-mlops.yml now clean — no diagnostic steps. Node 20 deprecation
  warnings on checkout@v4/setup-python@v5 still pending (harmless).

## Governance state
- WS-A CLOSED · WS-B CLOSED · WS-C CLOSED · **CL-12/13 FULLY CLOSED
  (PR #16, `0e48e02`) — no debt outstanding** · WS-D next governance
  session (Build & Quality Plan; carries CL-10 evidence) · WS-E pending
  — ledger now carries incidents 1–13 (20–21 Jul) + 14–23 (22 Jul AM)
  + **24–27 (this session)** + candidates: merge-discipline rule
  (now executed once — strengthens ratification case),
  merge-confirmed-before-tidy rule, IO.File-absolute-paths amendment,
  cache:false audit, OIDC hardening · WS-F cross-cutting.
- Open CL backlog unchanged: CL-06..09 · CL-11 · CL-16 · CL-17 · CL-18
  · CL-19 · CL-20 (CL-17/19/20 bundle at next Banking Architecture
  revision).

## House rules (amended this session)
All prior rules stand, with amendments:
1. **`[IO.File]` writes only, ABSOLUTE PATHS ONLY** — resolve via
   `(Resolve-Path ...).Path` first (incident 24).
2. **Split scripted edits into short single-assignment steps** with a
   length-comparison no-op guard before the write, then verify with
   `git --no-pager diff` before staging (incident 27; extends rule 2
   from the AM handover).
3. **Merge only on green CI with closures aboard** (candidate,
   operative — executed once this session).
4. **Confirm merge on GitHub before any local tidy-up** (incident 25).
5. Boot ritual: activate env → switch main → pull --ff-only → fetch
   --prune, all four, before touching files (incident 26).
6. `git fetch --prune` before any remote-branch operation; remember it
   does NOT delete local branches.
7. Keep console pastes under ~2KB; one command per paste; prompt
   eyeball for `(arcaai)`.

## Recorded-decision gap (identified at close, 22 Jul PM)
The **s3store default-remote switch** (22 Jul AM) is executed and live
but exists only as config + handover prose — no DEC entry. It changed
the storage backing of the artefact source-of-truth (ADR-0007
territory), so it clears the significance bar. First task next session
(see boot line). The **platform-endgame** decision (AWS as deployment
target) is correctly PARKED as candidate — not yet decided, do not
record. This gap is a live instance of the CL-08 problem (the
decision-capture gate question, still on backlog) — cite it as
supporting evidence when CL-08 is executed.

## Next session — the fork
- **First**: DEC entry for s3store (small PR — see boot line).
- **Option A — BUILD B6**: LangGraph agent v0 + Llama 3.1 8B. The more
  interesting session; new ground.
- **Option B — GOVERNANCE WS-D**: Build & Quality Plan review; carries
  CL-10 evidence (tracker accuracy is a §4 D task). Keeps the
  build/governance alternation; clears the last blocking review work
  before the agent build.
- No blockers either way. Closure debt: **zero** (the DEC gap is
  recording debt, not closure debt — the work itself is done and
  proven).
