# Claude Code harness — install & shake-out runbook

*Finalises the "Claude Code setup checklist" draft (8 Aug 2026) into
committed artefacts. Two deliberate departures from the draft, both
recorded below. Companion to: Test TOR Rev A §7 (harness ceremonies
precondition), DXB process doc Stage 4 (prototype sessions assume this
harness).*

## Departures from the draft checklist

1. **No hardcoded register state in CLAUDE.md.** The draft carried
   WS-E 61 / CL 24; the 7 Aug REPO_MANIFEST already said WS-E 62 /
   CL 26; PR #67 has moved state again since. A static block goes stale
   within a session — the CL-26 stale-origin pattern reproduced inside
   the harness. Instead `/session-open` regenerates
   `scripts/repo_manifest.py` and the readback from that run is the
   session's register anchor. CLAUDE.md carries only the queue pointer,
   maintained by `/session-close` between explicit markers.
2. **Skills-only, no `.claude/commands/`.** Commands are the legacy
   form; skills (`.claude/skills/<name>/SKILL.md`) are current, support
   the same `/name` invocation, and win on name collision. Ceremony
   skills carry `disable-model-invocation: true` so they fire only when
   the operator types them — the model cannot decide to open or close a
   session, touch a ledger, or prep a PR on its own.

## What is in this package

```
CLAUDE.md                                  repo root — guidance layer
.claude/settings.json                      hook wiring (project scope)
.claude/hooks/governance_guard.py          PreToolUse guard (Python, x-plat)
.claude/skills/session-open/SKILL.md       /session-open  (user-only)
.claude/skills/session-close/SKILL.md      /session-close (user-only)
.claude/skills/ledger-touch/SKILL.md       /ledger-touch  (user-only)
.claude/skills/hash-verify/SKILL.md        /hash-verify   (model may invoke)
.claude/skills/pr-prep/SKILL.md            /pr-prep       (user-only)
```

Hook behaviour: **deny** (no override) force-push / history rewrite /
recursive force delete; **ask** (operator confirms) any Edit/Write or
writing shell command touching MANIFEST.yaml, EDGES.yaml,
WS-E_INCIDENTS.md, DECISIONS.md, RULINGS_RECORD*.md,
document-register.yaml. Hooks are the enforcement layer — the model
cannot skip them; CLAUDE.md is the guidance layer. Hard rules live in
the hook, soft rules in CLAUDE.md, per the draft's own principle.

## Install sequence (this is the session)

1. `gh auth login` if not already done; verify with `gh pr list` on the
   arcaai repo.
2. Copy this package into the repo root (CLAUDE.md at root, `.claude/`
   directory alongside it). No existing files are overwritten unless a
   CLAUDE.md already exists — diff it first if so.
3. Sanity-check the hook fires: in a Claude Code session, ask for a
   trivial edit to MANIFEST.yaml and confirm the ask-prompt appears;
   ask for `git push --force` and confirm the deny. Then revert
   nothing — neither should have executed.
4. Branch `harness-install`, commit, `/pr-prep`, PR in house style.
   The harness lands through the same door as everything else.
5. **Shake-out arc (per the draft's session order step 5):** run the
   next real queue item end-to-end under the harness — batch-2
   authoring, SG-05 (carries AO-2 as the batch check), per the v0.2
   skeleton and EDGES v0.2.2 minimums:
   `SG-05: [SG-02, DP-02, TY-03, CV-03, DP-04]`.
   `/session-open` → author SG-05 (authoring act only; listing is a
   separate act, hook-gated) → `/pr-prep` → `/session-close`.
6. Add remaining ceremonies as they are hit in real use, not up front
   (draft §2 discipline). Candidate next: `/manifest-list` for the
   authoring/listing second act, once its shape is proven manually
   under the harness once.

## Later (unchanged from the draft)

- Plugin bundling once stable, for portability to the MyBank simulator
  repo and SmartDog: same commands + hooks + CLAUDE.md pattern as a
  single installable package.
- PostToolUse lint/format hooks: deliberately omitted from v1. Add
  after the shake-out arc if manual lint invocation proves to be
  friction; adding them untested would put an unproven mutation in the
  loop of every write.

## Open items carried to their proper homes (not this harness)

- Test TOR Rev A: §7 precondition "CLAUDE.md and harness ceremonies in
  place before build sessions" is DISCHARGED by this install. TOR open
  questions remain for panel session.
- DXB: Stage 4 prototype sessions inherit this harness as-is;
  prototype files are not governed stores and get no hook gate —
  correct, they are disposable by design.
- CL-24 (governance test suite default) and CL-25 (operational ingest
  pin writer): unchanged; the hook here guards interactive sessions,
  not the ingest path — CL-25 remains the ingest-side control.
