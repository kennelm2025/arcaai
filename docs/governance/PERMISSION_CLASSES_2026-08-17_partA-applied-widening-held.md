# Permission classes — Part A applied; P2 PASS; P1 mechanism identified; P4 FAILED — deny bypass found. Widening HELD pending guard repair + re-probe.

**2026-08-17. The amendment record for the item 27 permission-tier work.**

The title is the outcome, deliberately. A record titled "probe-tested" was drafted
and **not written**: P4 failed, the extension probes found a general deny bypass,
and this repository's rule is that a failed probe is a stop rather than a repair.

**Item 27 status: NOT DISCHARGED. HELD.**

---

## 1. What is applied, and by whom

**Part A — READ/VERIFY widening. APPLIED. OPERATOR ACT**, at the operator's own
terminal, per the pack at
`D:\Downloads\CC_AMENDMENT_PACK_2026-08-17_permission-classes.md`. `.claude/`
carries an absolute deny with no in-session route, so no executor act could have
applied it.

Read-class allow entries only: hashing, text search and slicing, explicit git read
subcommands, `Select-String`, `Get-FileHash`. `find` and `sort` were **excluded**
at drafting — the settings file already records that `find -delete` and `find
-exec rm` execute arbitrary deletion and that `sort -o` writes a file, and
`CLAUDE.md` places those write forms in the denied-outright set.

**Part B — REVERSIBLE-MUTATION widening. DRAFTED AND HELD. NOT APPLIED.**

It was held before any probe ran, on a blocker recorded in the pack: an allow rule
pre-empts a guard ask (tested 2026-08-11, controlled pair), the HEAD-is-main
protection lives in the guard, and the branch condition cannot be expressed as a
rule string — so settings-allowing `git add/commit/push` would remove the gate on
main rather than merely widen the verbs on feature branches. The probes then made
the case stronger rather than weaker: see §3.

**Part A stays applied.** Read-class allows cannot reach the deny families the
probes found bypassed. The allow-pre-empts-guard interaction remains an **open
question, recorded not resolved**.

## 2. Probe outcomes

| Probe | Ruled expectation | Executor in-harness result | Verdict |
|---|---|---|---|
| **P1** deny-probe, read-only command naming a protected path | Must still refuse; a false-red is a FINDING | **Executed, no refusal.** Isolation then identified the true trigger | Item 39's stated mechanism **DISCONFIRMED**; now WS-E 73 |
| **P2** allow-probe, read class | Must pass with no ask | **Passed.** `sha256sum` returned RQA-107's committed hash | **PASS** |
| **P3** mutation-probe | Not run — probes Part B, which is held | not run | n/a |
| **P4** `-d`/`-D` boundary on the live branch-delete rule | `-D` must refuse | **`-D` EXECUTED** under a `-C` prefix; **refused** in the plain form | **FAIL** — cause is the deny pattern, not case-folding |

**The `-d`/`-D` case-folding hypothesis is disconfirmed.** The settings file
records it as an open risk; the plain-form `-D` refused, so the
`Bash(git branch -d:*)` allow rule is **not** swallowing `-D`. That boundary is
sound. The deny's own pattern is what fails.

### Operator evidence — both-halves completion

**NOT SUPPLIED.** The instruction carried the placeholder
`[FILL: no asks fired / asks fired at … / not observed]` and it arrived unfilled.

Recorded as **NOT SUPPLIED** rather than left blank or inferred, per this
repository's own discipline that an absence is written. **This record therefore
carries the executor half only and is not a complete both-halves record.** The
operator's observed ask behaviour during P1, P2, P4 and the extension probes
remains owed.

## 3. The finding the probes produced

Full record at `docs/governance/FINDINGS_2026-08-17_guard-bypass-git-global-options.md`,
with the coordinator-ruled fix spec and re-probe list at
`docs/governance/FINDINGS_2026-08-17_guard-bypass-ADDENDUM_fix-spec.md`.

**In one line: every governance-guard deny keyed on a git subcommand is bypassed
by inserting a global option — proven for `-C` — between `git` and the
subcommand.** Two controlled pairs, one variable: force-push (CL-E1) and
`branch -D` both refuse in the plain form and both execute with the prefix.

Raised as **WS-E 72**. The write-construct false-red is **WS-E 73**.

**Why this strengthens the hold on Part B rather than merely delaying it.** The
pack's blocker was that Part B would remove a guard protection by pre-emption.
The probes show the protection is weaker than that argument assumed: the guard's
git denies can fail to match at all. Widening the git write verbs against a deny
surface with a known bypass would compound two defects.

## 4. What replaced the client-side protection in the interim

**OPERATOR ACT, DONE.** GitHub branch protection on `main`, as an emergency subset
of item 34 **M3**. Read from the artefact via `gh api` and recorded as read:

- ruleset **`main-protection`**, id `20906548`, target `branch`, enforcement
  **active**, updated 2026-08-16T10:03:01+01:00
- applies to `~DEFAULT_BRANCH`; **`bypass_actors`: NONE**
- rules: **`deletion`** (branch deletion blocked) · **`non_fast_forward`** (force
  push blocked) · **`pull_request`** (pull request required)
- `pull_request` parameters as read: `required_approving_review_count: 0`,
  `dismiss_stale_reviews_on_push: false`, `require_code_owner_review: false`,
  `require_last_push_approval: false`, `allowed_merge_methods: [merge, squash, rebase]`

Classic branch protection returns **404 Branch not protected** — the repository
uses the ruleset mechanism, not the legacy endpoint, and the 404 is therefore the
expected reading rather than an absence of protection.

**Stated precisely so it is not over-read: a pull request is required; an approval
is not.** `required_approving_review_count` is 0. The control is
"nothing reaches main except through a PR", not "nothing reaches main without
review".

**This is environment-independent**, which is the property the client-side guard
lacks and the reason it matters here: a deny that fails to match, or a render that
bypasses the hook, cannot reach `main` past a server-side rule. **Full M3
treatment remains owed under item 34.**

## 5. STANDING ORDER SO-1 — post-merge verification

Lands with this record. **It is a procedural convention and is independent of the
deny findings** — nothing in WS-E 72 or 73 bears on it.

**Trigger form:** `PROMPT <n>: MERGED — VERIFY #<pr>`

An **unnumbered** trigger is **honoured**, and the gap is **flagged in the
output** — per the instance of 2026-08-16, where the trigger was the bare line
"merge verify", the acts were read/verify class plus a safe delete, and nothing
improper occurred.

**Fixed sequence. Scope is the named PR only. Any failed step is a STOP, not a
repair.**

| Step | Act | Stop condition |
|---|---|---|
| i | `gh pr view <pr>` — confirm `state: MERGED` **from the artefact** | Not merged → STOP |
| ii | pull; confirm HEAD is the merge commit | HEAD not the merge commit → STOP |
| iii | Verify **all** hashes listed in the stop report against the blobs at HEAD | Any mismatch → STOP |
| iv | Delete the merged local branch (**`-d` only**), prune | `-d` refuses → STOP, do not escalate to `-D` |
| v | Regenerate the manifest; report the anchor line and divergences | **A dirtied tree is a STOP** |
| vi | Report the fixed table: merge commit · blob results · cleanup · anchor | — |

No drafted body is needed — the sequence is the order, and the output table is
fixed so a missing row is visible as a missing row.

## 6. Rollback

**One line.** Remove the Part A entries from `permissions.allow` in
`.claude/settings.json` and restart the session. Same mechanism used at amendment
4, when 55 entries were removed rather than annotated inactive — *"a grant that is
live in every fresh process is granted, whatever the surrounding prose says."*

Part B is not applied, so nothing of it needs reverting. Had it been applied
alongside a guard change, rollback would have been **two** acts and would have
broken Safeguard 2 unless both rode one PR.

## 7. Item 27 status

**NOT DISCHARGED. HELD.**

| Component | Status |
|---|---|
| Rule-string restatement | Discharged earlier, at `678f46a` |
| `.claude/agents/` narrowing | Discharged; the path left Tier 2 entirely on 2026-08-14 when all four `.claude/` paths became DENY |
| READ/VERIFY widening (Part A) | **Applied**, probe-supported by P2 |
| REVERSIBLE-MUTATION widening (Part B) | **HELD** pending guard repair and the re-probe list |

The item cannot be discharged while its principal component is held. The
together-in-one-PR condition is satisfied in form — the other two components
landed earlier — but the substance is incomplete and saying otherwise would be the
overclaim the condition existed to prevent.

## 8. What this record does not claim

It does not claim the widening is probe-tested; P4 failed. It does not claim the
guard is sound; two denies were shown bypassable. It does not claim any prior
session's clean record is evidence the denies worked — **nothing improper was
attempted, and that is a fact about what was attempted, not about what was
prevented.** It does not apply any fix.
