# ADDENDUM to FOLD-IN 2026-08-18 — history-rewrite refusal string, baselined

Authored under PROMPT 135 on branch `governance/item-42-discharge-2026-08-19`,
riding the item 42 discharge write. This addendum externalises the **third**
DENY-class refusal string into the record, alongside the two that
`docs/governance/FOLD_IN_2026-08-18_prompts-125-126-and-guard-install.md`
section 2 already carries.

## 1. Why an addendum and not an edit — the frozen call, stated

**The fold-in is treated as FROZEN.** This was a judgement call and the
reasoning belongs in the record rather than in a commit message.

**(a) The fold-in sets the precedent against itself.** Its own section 3 rules
that *"corrections to a narrative artefact are recorded beside it"*, and applies
that to `docs/governance/SESSION_HANDOVER_2026-08-18.md`, which it annotates
without editing. A document that declines to edit its neighbour on that
principle does not get edited on a weaker one.

**(b) Editing section 2 would retroactively change what a ruling covered.**
Section 2 records a PROMPT 128 ruling that the refusal text is **invariant
across the F1/F2 fix**, and states that the strings it carries are *"both the
pre-fix and the post-fix pass condition"*. The re-probe rows were then measured
against that text. Adding a third string to that section would make the ruling
appear to have covered a string it did not name, and would make the re-probe
appear to have measured against a baseline that did not exist when it ran. The
whole value of this addendum is that it records the opposite — see section 3.

**(c) The timing is the substance.** This string entered baseline on
**2026-08-19, after the discharge**, not before the probes. A reader must be
able to see that ordering. Folding it into an 2026-08-18 document would erase
the one fact it exists to preserve.

## 2. The string, read from the live guard

Read from `.claude/hooks/governance_guard.py` at the installed, byte-verified
version — the file whose SHA256 is recorded at fold-in section 4 as
`C02192E2279F46ADEC85C93A77847DB3B59645CA3889956236FCDC81670DB01B`.

**Method, stated because "read from the guard" admits of a weak reading.** The
value was extracted by **AST parse**, not by transcription and not by importing
the module. The parse matters for two reasons: importing a hook module executes
its top level, which a read has no business doing; and Python's parser joins
adjacent string literals into a single constant, so an implicit concatenation
in source arrives already joined — which is the value a probe actually
receives, and therefore the only value worth baselining. Lengths below are
counted from the joined value, in characters and in UTF-8 bytes, and the two
agree for all three strings (every character is ASCII).

**History-rewrite family — 55 characters, 55 UTF-8 bytes.** Source line 331. It
is a **single literal**, unlike the two below, which are implicit
concatenations:

```
Git history rewriting is prohibited on this repository.
```

Carried in fenced blocks rather than the blockquotes section 2 uses, so that no
markdown interpretation sits between the record and the bytes. The two strings
below are reproduced for completeness, so that this file is a **complete**
DENY-class baseline rather than a fragment a reader must assemble from two
documents.

**Force push family — 149 characters, 149 UTF-8 bytes.** Source line 326:

```
Force push is prohibited (CL-E1). No exception path exists; if you believe one is needed, stop and raise it with the operator outside this tool call.
```

**Force branch delete family — 287 characters, 287 UTF-8 bytes.** Source line
319:

```
Force branch delete is blocked (-D, or --delete --force). It deletes an unmerged branch without the refusal that makes -d safe. Use -d, which declines rather than destroys on surprising state; if the branch is genuinely unmerged and must go, that is an operator act at your own terminal.
```

**A corroboration worth recording, because it was available and cheap.** The
149 and 287 figures were **re-derived by the same AST extraction at this
authoring**, not copied from fold-in section 2, and they match that section
exactly. So the section 2 baseline is confirmed still true against the live
guard after the F1/F2 install — an independent check on the section 4 claim
that the refusal strings were invariant across the fix, arrived at from the
string side rather than the file-hash side.

## 3. What this does and does not repair

**It repairs the referent, prospectively.** From this date a probe asserting the
history-rewrite deny has an externalised string to assert **against**, held in a
different file from the one it checks.

**It does not retroactively strengthen the rows already run.** Those rows were
checked against the live guard — that is, against themselves — and a check whose
subject and whose standard are the same artefact cannot detect that the artefact
is wrong. That is caveat (b) of the item 42 discharge and it stands as written;
this addendum is the fix going forward, not a re-grading of what has already
happened. **The discharge is not strengthened by this file** and no citation of
it should say otherwise.

**Scope.** DENY-class strings only. The ASK class has no equivalent baseline and
cannot usefully acquire one while **WS-E 75** stands: an ask's text is not
observable from either vantage point, so externalising it would produce a
standard nothing can be measured against.

## 4. Disposition

No control mapping line is carried, for the reason
`docs/governance/SESSION_COSTS.md` and fold-in section 6 both state: queue item
34 M11(d) requires per-class mapping content to be defined once in the control
framework, and that framework does not exist yet.

**Prompt numbers consumed: 134 (boot and verify, read-only), 135 (this
addendum, the item 42 discharge write, WS-E 75 and the cost row).** Recorded per
the interim practice adopted at fold-in section 5(a).
