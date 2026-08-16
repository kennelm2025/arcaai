# FOLD-IN 2026-08-18 — retired prompts 125/126, guard install record, handover annotations

Authored under PROMPT 129 on branch `governance/fold-in-2026-08-18`. This
document carries what the 2026-08-17 close ceremony would have carried had it
reached the repository. It did not, and section 3 is the evidence for that
claim rather than an assertion of it.

**Nothing in this document is a claim that the guard bypass is closed.** See
section 4.

---

## 1. Prompt counter — 125 and 126 are RETIRED-UNVERIFIABLE

`docs/governance/SESSION_HANDOVER_2026-08-18.md` section 6 records the intended
allocation: *"The close ceremony consumes 125 (rulings + close PR) and 126
(merge-verify), so NEXT IS 127 — verify against the close record at boot."*

**The verification it directs was performed at this boot and the close record
does not exist.** No close PR reached the repository (section 3). Scrollback and
the Downloads companion set are inconclusive as to whether either prompt was
composed and issued.

**Ruled disposition: 125 and 126 are RETIRED-UNVERIFIABLE.** They are spent as
numbers and carry no artefact. Neither may be reissued.

**The ruling is gap-beats-collision.** Two numbers referring to nothing is a
legible gap that a reader resolves by finding this entry. Reissuing them would
put two different acts behind one number, and a register cannot distinguish the
second use from the first after the fact. A hole is recoverable; a collision is
not.

Next issued was **127**. The ECHO convention's expected gap is therefore
124 → 127, and it is answered here rather than left for a future reader to treat
as a delivery failure.

**Prompt numbers consumed this session, recorded because the trail otherwise
survives nowhere:** 127 (guard fix draft, scratchpad), 128 (protected-path
enumeration, read-only), 129 (this fold-in).

## 2. Ruled baseline refusal strings

Ruled at PROMPT 128: **F1 and F2 are pattern-matching changes only; the refusal
text is invariant across the fix.** Under that constraint the strings below are
both the pre-fix and the post-fix pass condition, and the ambiguity that would
otherwise sit in the phrase "the guard's own refusal text verbatim" is closed by
ruling rather than resolved silently at run time.

Captured verbatim from `.claude/hooks/governance_guard.py`. Both are implicit
string concatenations in source; the values below are the joined strings, which
are what a probe actually receives.

**Force push family (149 characters):**

> Force push is prohibited (CL-E1). No exception path exists; if you believe one is needed, stop and raise it with the operator outside this tool call.

**Force branch delete family (287 characters):**

> Force branch delete is blocked (-D, or --delete --force). It deletes an unmerged branch without the refusal that makes -d safe. Use -d, which declines rather than destroys on surprising state; if the branch is genuinely unmerged and must go, that is an operator act at your own terminal.

**This externalises the pass-condition referent into the record**, which is the
point of writing them here. Addendum 1 defines the pass condition by pointing at
the guard source, so the condition could not be checked from the artefact that
states it — a check whose subject lives outside itself. The re-probe checks every
REFUSE row against the two strings above.

## 3. Handover annotations

Two annotations against `docs/governance/SESSION_HANDOVER_2026-08-18.md`. The
handover is landed verbatim and is **not** edited; corrections to a narrative
artefact are recorded beside it.

### (a) Section 10's "no housekeeping owed" is DISCONFIRMED

Section 10 states the successor's open is *"boot + verify only, no housekeeping
owed"*, on the premise that the handover, the cost row and the queue deltas
landed in a close PR. **That close PR never existed.** Three concordant reads:

| Read | Result |
|---|---|
| `gh pr list --state all --limit 300` | 139 pull requests total, **0 open**, 139 closed or merged |
| Highest PR number | #139, MERGED — the guard-bypass findings PR, not a close PR |
| Repository tree at boot | no 2026-08-18 handover, no 2026-08-17 cost row, queue item 35 still OPEN |

The housekeeping section 10 describes as done is therefore what this branch
performs. Recorded rather than silently corrected, because the failure mode is
specific and repeatable: a handover written *before* its own close ceremony
completes will describe that ceremony in the past tense, and a successor
trusting it skips the work. **A handover cannot evidence its own landing.**

### (b) The date-label-versus-clock offset is not a constant

The offset is real and is queued rather than repaired. **But the payload's
characterisation of it as one day is not what the tree shows.**

| Source | Value |
|---|---|
| Machine clock at this boot | 2026-08-16 14:58 +01:00 |
| Session label of the handover landed here | 2026-08-18 |
| `ARCAAI_CHAT_HANDOVER_2026-08-17.md` file mtime | 2026-08-16 07:57 |
| `ARCAAI_CHAT_HANDOVER_2026-08-18.md` file mtime | 2026-08-16 10:24 |

**Two consecutive session labels, 08-17 and 08-18, were both written on clock day
08-16** — a two-day offset for one and one day for the other. `SESSION_COSTS.md`
already records the same disagreement from the git side: all eight PRs of the
2026-08-15 and 2026-08-16 sessions merged on clock day 2026-08-15, and no PR
merged on 2026-08-16 at all.

So the offset is **not a fixed skew that a reader can correct by subtracting a
constant.** Any future reconciliation must treat session labels as opaque
identifiers rather than as dates arithmetic can be done on. Queued, not repaired.

## 4. F1/F2 application record — applied and byte-verified; LIVE EFFICACY PENDING

**Status, stated first because the rest of this section is detail and the status
is what a reader needs:** the fix is **installed and byte-verified offline**. It
is **NOT** shown to work. **The bypass is not claimed closed.**

**What was done.** The candidate was drafted outside the tree at PROMPT 127, per
the module's own drafting route — `.claude/hooks/` carries an absolute deny with
no in-session route, so the executor drafts and the operator installs at their
own terminal. The operator installed it and ran `fc.exe` on both sides.

**Pre-install diff, as ruled at PROMPT 127:**

- five adjacency-keyed git patterns re-anchored through a shared
  `GIT_GLOBAL_OPTS` constant, shape (b) — a bounded dash-token run absorbing any
  global option between the executable and the subcommand. The five: the
  force-push deny, the force-branch-delete deny, the history-rewrite deny, the
  HEAD-is-main write ask, and the branch-deletion ask. **Three of the five are
  not in the re-probe list**, and two of those three are ASKS rather than DENIES.
- `WRITEY_RE` leading branch `>>?` replaced by `>(?!&)>?`, so a descriptor
  duplication is no longer read as a file redirection (WS-E 73).
- **both refusal strings byte-identical**, per the section 2 ruling.
- **response classes unchanged** — the three denies still deny, the two asks
  still ask.

**Post-install verification, two independent methods.** The operator's `fc.exe`
returned *"no differences encountered"*. Independently, SHA256 of the installed
file and of the scratchpad candidate were computed at this boot and are equal:

```
C02192E2279F46ADEC85C93A77847DB3B59645CA3889956236FCDC81670DB01B
```

The install is therefore byte-exact against the reviewed candidate. That is the
whole of what is established.

**What is NOT established, stated because the distinction is the entire point.**
Byte-exactness proves the file on disk is the file that was reviewed. It does not
prove the guard fires. It cannot: the PreToolUse matcher in `.claude/settings.json`
must route the call, the hook must execute, and the harness must honour the
response — none of which a hash or an offline pattern evaluation touches. WS-E 64
records three days in which a guard was correct in its patterns and unreachable
in its wiring, and read as green throughout.

**LIVE EFFICACY PENDING the re-probe.** The re-probe is Addendum 1 section 2 as
amended by
`docs/governance/FINDINGS_2026-08-17_guard-bypass-ADDENDUM-2_reprobe-row-amendment.md`,
which corrects two rows that cannot discriminate a fixed guard from an unfixed
one. **Queue item 42 is not discharged by this record, and item 27 Part B remains
held.**

## 5. Notes for queue item 34 M2

Two observations, recorded here because M2's subject is precisely the trail that
otherwise does not survive.

**(a) The numbered-prompt trail survives only where a record happens to quote
it.** Asked at this boot for the last prompt number, the only recoverable
answer came from grepping the governance tree for prompt citations: the highest
was PROMPT 124, in the guard-bypass fix spec. Prompts 125 and 126 are
unverifiable for exactly this reason — nothing quoted them, so nothing evidences
them. **Interim practice adopted, pending M2 proper: every session record and
commissioning record states the prompt numbers it consumed.** It is one line and
it converts the trail from incidental to recorded. Section 1 of this document
carries it as the first instance.

**(b) A predicted next-prompt number has zero authority.** A prompt is real only
when composed by the coordinator and pasted into the terminal. An executor that
anticipates the next number, or reasons from a handover's statement of what the
next number *will* be, is manufacturing an act that has not occurred. This is the
mirror of the PROMPT 115 delivery lesson and it runs in the opposite direction:
115 failed because an acknowledgment from a non-terminal source was treated as
delivery **inbound**; this fails when a number is treated as issued **outbound**
before it is. Both reduce to the same rule — **the terminal is the only channel,
and an act exists when it arrives there and not before.**

## 6. Disposition

No control mapping line is carried, for the reason `docs/governance/SESSION_COSTS.md`
states: queue item 34 M11(d) requires per-class mapping content to be defined
once in the control framework, and that framework does not exist yet.
