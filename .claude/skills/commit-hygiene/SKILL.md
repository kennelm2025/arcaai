---
name: commit-hygiene
description: How to author commits, PRs, and governance register entries in the ArcaAI repo. Consult this skill before ANY git commit, before opening or describing a PR, and before drafting or numbering a DEC, ADR, CL, or WS-E entry. Applies whenever commit messages, PowerShell quoting, register numbering, or house-style ledger entries are involved — even for trivial commits.
---

# Commit & Register Hygiene

Standing rules (ruled by Mike; provenance: repeated WS-E incidents on
PowerShell quoting; DEC-0015 house-style ruling).

## Commits

1. **Commit messages go via a message file, never inline.** PowerShell
   quoting of `git commit -m "..."` has repeatedly mangled messages. Always:

   ```powershell
   Set-Content -Path .git\COMMIT_MSG.txt -Value @'
   <subject line>

   <body>
   '@ -Encoding utf8
   git commit -F .git\COMMIT_MSG.txt
   ```

2. Subject line: imperative, ≤ 72 chars, names the stage/artefact
   (e.g. `D2.1: add spec schema v0.1 keystone`).
3. Body references the governance artefacts touched (DEC/ADR/CL/WS-E numbers)
   so the register lineage is greppable from `git log`.

## Register discipline

- Numbers are allocated strictly in sequence from the register state and are
  **never** consumed speculatively. If drafting a candidate decision for
  Mike to rule on, label it `DEC-candidate (unnumbered)` until ruled.
- Current next-numbers are read from the register files in the repo at the
  time of writing — never from memory of a previous session.
- House style: decisions land as ledger bullets (per the DEC-0015 ruling),
  not as long-form documents, unless Mike rules otherwise for a specific item.
- ADR-0011 is reserved (Agentic Topology). Do not allocate it to anything else.

## PRs

- One concern per PR where practical; governance-only changes and build
  changes are not mixed in a single PR unless the governance change is the
  direct record of the build change.
- PR descriptions state what was checked before merge, using the wording
  rules in the check-method skill.

## Drafting vs ruling

The harness (Brain or Hands) may **draft** any register entry. Only Mike
**rules**. A drafted entry is clearly marked as a draft until his ruling is
recorded; the ruling itself is never inferred, assumed, or backfilled.
