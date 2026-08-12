---
name: harness-discipline
description: Elevation and privilege rules for the ArcaAI harness. Consult this skill before ANY command that could require elevation, admin rights, sudo, "Run as Administrator", registry writes, service installs/restarts, Docker daemon changes, firewall or PATH-machine-scope changes, or repairs to a failed environment. Also consult it whenever a command fails with a permissions/access-denied error and a fix is being considered. Applies to every session, every subagent, no exceptions.
---

# Harness Elevation Discipline

Standing rule (ruled by Mike, reinforced across sessions; provenance: WS-E process incidents register):

**The harness never elevates.** No exceptions, no "just this once", no
temporary elevation to unblock a task.

## The rule in operation

1. If a repair, install, or fix requires elevation of any kind, the harness
   **stops** and records the situation. The repair belongs to Mike, at his own
   terminal, in his own elevated session.
2. The harness's output at that point is a **handover note**, not an attempted
   fix. The note states:
   - what failed, as a prose description (never a live reproduction — see the
     check-method skill),
   - why elevation is believed necessary,
   - the exact command(s) Mike would run, written out for him,
   - what the harness will re-verify afterwards.
3. After Mike performs the elevated repair, the harness re-verifies **from a
   non-elevated shell**. A verification run from an elevated context proves
   nothing about the harness's normal operating conditions and is invalid.
4. Subagents inherit this rule in full. A subagent may not be granted tool
   permissions that would let it elevate, and a lead agent may not route an
   elevation around the rule by delegating it.

## What counts as elevation (non-exhaustive)

- `sudo`, `runas`, "Run as Administrator", UAC prompts
- `Start-Process -Verb RunAs`
- Machine-scope environment or PATH changes
- Writes under `HKLM`, `Program Files`, `C:\Windows`
- Service install/uninstall/restart requiring admin
- Docker Desktop settings changes requiring admin consent

## Relationship to the ruled permission system

Mechanical enforcement of this rule lives in the permission tiering system
ruled and sealed at PR #95 (11 Aug 2026), which has its own verification
test. This skill does not restate or duplicate that enforcement; it teaches
the rule and the handover procedure. If this file and the ruled policy ever
disagree, the ruled policy wins and this file has a transcription defect.
Formal provenance of the rule itself: ruled 11 Aug 2026 — "the automated
tooling never runs with admin rights; admin work is Mike's, at his own
terminal" — following the model-cache root-cause finding.

## Why this exists

The harness operating identically to production conditions is a governance
property, not a convenience. An elevated harness produces green checks that
cannot be trusted from a normal shell. Permanent inadmissibility of
commissioning-regime results (D2.0 frame) rests on the same principle:
results are only meaningful under the conditions they claim to represent.
