# Harness permission tiers — ArcaAI

**Operator ruling: 2026-08-11.** Autonomy granted by written policy on
the record. This document is authoritative for the tiers; `CLAUDE.md`
describes them and points here. Where the two disagree, this document
governs and the discrepancy is a WS-E item.

Landed alongside WS-E 64, which records that the enforcement layer had
been wired to one shell of two since installation. The sequencing was
ruled absolute: no allow-list widens anything while the deny layer has
a blind spot, so the guard was extended to the PowerShell tool and
verified end to end in the same PR that grants Tier 1.

## Tier 1 — auto-allow, no prompt

Read-only operations (git status, diff, log, show, branch listing,
blame, rev-parse, fetch; file reads; directory listings; `Get-Acl`;
`Test-NetConnection`). The mandatory batteries (`scripts/check_docs.py`,
lint, tests, pytest, `scripts/repo_manifest.py`,
`scripts/rehash_sweep.py`). Routine git writes on feature branches
(add, commit, checkout, switch, push, fetch, fast-forward-only pull).
Edits to ordinary, non-protected files.

*Rationale:* every one of these is reversible, branch-isolated, and
verified by batteries that run regardless of whether a prompt preceded
them. The prompt was never the control; the evidence after the act is.

## Tier 2 — gated, every touch

The six governed stores, unchanged: `verticals/fraud/corpus/MANIFEST.yaml`,
the corpus edges file, `docs/governance/WS-E_INCIDENTS.md`,
`DECISIONS.md`, the rulings records, and the document register. Added
2026-08-11: `pyproject.toml`; `.github/workflows/`;
`.claude/settings.json`, `.claude/hooks/` and `.claude/skills/`; and
`decisions/`. Plus, by repository state rather than by path: PR merge,
branch deletion, and any git write while HEAD is main.

*Rationale, per group.* `pyproject.toml` and the workflows change what
every future run means, so a silent edit rewrites the meaning of every
later green. The permission and ceremony system is gated against
itself because the harness must never widen its own latitude
unprompted — `.claude/settings.json` now guards the file these tiers
live in, which is the point rather than an accident. `decisions/` is
gated on a mechanism, not a convention: `scripts/repo_manifest.py`
reads the leading four digits off each filename there, so that
filesystem **is** the ADR register and any write to it consumes
register numbers silently. It is register-consuming by mechanism and
therefore gated by consequence. WS-E 64 records that the one near miss
of this kind was caught by the working protocol and not by any gate;
this is the gate that was missing.

**Absolute denies, unchanged and with no exception path:** force push
in any form, git history rewrites, recursive force deletes, and the
standing rule that the harness never elevates — extended 2026-08-11 to
database roles: the harness runs as the application role and never
assumes owner.

## Tier 3 — operator rulings

Arc selection, scope, merges, frame rulings, register decisions. These
are not tool gates and are unaffected by anything in this document. No
mechanism grants or withholds them.

## Safeguard 1 — batteries remain mandatory

Auto-allow moves the gate from *before* the act to the evidence
*after* it. It removes prompts, not verification. Unchanged: `git diff
--stat` comes first in every battery and an empty diff means the act
did not happen; success is asserted on the substance a check returns
and on the assertions it names, never on an exit code alone; one act
at a time, with state checked before mutation and effect verified
after it.

## Safeguard 2 — rollback is one revert

Every change implementing these tiers rides a single PR. Reverting
that PR restores the prior enforcement state in one act, with no
partial condition to reason about.

## Enforcement coverage

"Gated" must not be able to quietly mean "gated on one tool". Three
mechanisms exist, and they do not cover the same ground.

1. **The PreToolUse guard** (`.claude/hooks/governance_guard.py`,
   routed by the matcher in `.claude/settings.json`). Covers the Bash
   and PowerShell tools for command inspection, and the file-writing
   tools for path inspection. Coverage is two-part: the matcher must
   route the call *and* the module's shell-tool set must name the
   tool. Either alone is a silent no-op — the WS-E 64 defect exactly.
   Adding a shell tool means adding it in both places.
2. **Permission rules** in `.claude/settings.json`. These match
   command text only. They cannot read repository state, which is why
   the branch condition is not expressible here and lives in the guard
   instead.
3. **Skill frontmatter `allowed-tools`**, per ceremony under
   `.claude/skills/`. **Tier 1 grants are not in force inside a
   ceremony**; that ceremony's own frontmatter governs, and all five
   are currently Bash-only. This narrows rather than widens, which is
   the safe direction — a ceremony that prompts more than the tiers
   promise is friction, not exposure — but it means the boot battery
   may prompt where Tier 1 says it will not. Harmonising the
   frontmatter is a follow-up, deliberately not folded into this arc.

**The guard may only ever restrict.** It returns deny or ask and never
allow. It can narrow a Tier 1 grant but can never enlarge one, so a
permission granted on the record cannot be quietly widened by a hook.

## Soft-enforced — named, not implied covered

Real content, because a policy that implies coverage it lacks is the
false-green shape this repository catalogues.

- **The never-elevate rule.** Not mechanically enforced at all.
  Partially detectable through the obvious invocations, but elevation
  can arrive by means no pattern sees. Guidance only.
- **The never-assume-owner-role rule** (2026-08-11). Same status:
  partially detectable through the owner DSN and role name, never
  completely. Guidance only.
- **"Branch deletion other than the just-merged branch."** The guard
  gates all branch deletion because it cannot know which branch was
  just merged. The qualifier is soft; the gate is deliberately
  broader than the rule.
- **"Any register-consuming act."** Consumption is semantic, not
  textual. Three registers are gated by path and `decisions/` is now
  gated by mechanism, but no mechanism can recognise a number being
  claimed in prose.
- **Whether skill renders and subagent tool calls route through
  PreToolUse is UNVERIFIED.** Not observed from inside a session and
  therefore not claimed in either direction. Moot in practice today,
  since background subagents are disabled repository-wide.
- **The permission rule strings themselves are unverified.** Rules
  governing a session cannot be tested from inside that session, and
  declaring them working on merge would be exactly the false green
  this repository keeps cataloguing. The PowerShell rule forms in
  particular are asserted by construction, not by observation.
- **Precedence between a Tier 1 allow rule and a Tier 2 guard ask is
  UNVERIFIED.** The design assumes the guard's ask prevails over a
  settings allow. The guard is confirmed live in-session and its
  decisions are confirmed correct in isolation, but the interaction
  itself has not been observed. The resolving test is in the
  post-merge note below.

## Post-merge verification — required

The first session after merge is the evidence, not the session that
wrote this.

1. **Expect prompts that have never appeared before.** Protected-path
   asks will fire on the PowerShell tool for the first time in this
   repository's history. A new prompt is the matcher fix working. The
   first such prompt is its live confirmation, and must not be read as
   a failure of the tiering.
2. **Resolve the precedence UNKNOWN.** Attempt an edit to a governed
   store. Tier 1 grants `Write`; Tier 2 must still ask. If it asks,
   precedence is confirmed and the allow-narrowed-by-guard design
   holds. If it does not, the allow-list is too broad and `Write` must
   be removed from Tier 1 in favour of enumerated paths.
3. **Confirm Tier 1 actually reduces prompts.** If routine git and
   battery calls still prompt, the rule strings do not match and are
   to be corrected against observed behaviour rather than reasoned
   about further.

## Machine-local settings

`.claude/settings.local.json` is gitignored and remains legitimate for
machine-local experimentation. It is never policy: a permission
configuration that no reviewer can see is the opposite of a governed
artefact, which is why Tier 1 lands in the tracked file. Its two prior
entries are disposed of as follows — the docs-check rule migrates into
tracked Tier 1, generalised to its argument forms; the exit-code echo
rule is **dropped**, because it is tooling for reading an exit status
in isolation and tracked policy must not enshrine a check method this
repository's own findings discredit. Clearing the stale local entries
is an operator act on their own machine.
