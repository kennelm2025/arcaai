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
   $msg = @'
   <subject line>

   <body>
   '@
   [IO.File]::WriteAllText('.git\COMMIT_MSG.txt', $msg, (New-Object Text.UTF8Encoding $false))
   git commit -F .git\COMMIT_MSG.txt
   ```

   **Not `Set-Content -Encoding utf8`.** In Windows PowerShell 5.1 that writes
   UTF-8 *with* a BOM, which lands at the head of the subject line. Tested
   2026-08-12 on PowerShell 5.1.26100.9168: a file written by the former
   recipe began `EF BB BF`. The `UTF8Encoding $false` constructor above is the
   no-BOM form and works on both editions; on PowerShell 7+
   `-Encoding utf8NoBOM` is equivalent. Writing the file with the harness's own
   file-write tool is also BOM-free and avoids the quoting question entirely.

2. Subject line: imperative, ≤ 72 chars, names the stage/artefact
   (e.g. `D2.1: add spec schema v0.1 keystone`).
3. Body references the governance artefacts touched (DEC/ADR/CL/WS-E numbers)
   so the register lineage is greppable from `git log`.

4. **No `Co-Authored-By` trailer on any commit in this repo, and none in PR
   bodies.** Ruled first for corpus authoring; practice then ran ahead of the
   rule for ten consecutive instances, which made it an unwritten rule rather
   than a habit.

   **Assert it against the full printed body, never against a recalled
   impression of it.** Print the complete message — `git log -1 --format=%B`,
   or `git log main..HEAD --format=%B` for a branch — as in-session evidence,
   then assert against that printed text that no line asserts co-authorship.
   Say in the success line which bodies were read.

   The test is **attribution, not occurrence**: an attribution line is the
   token at line start, a colon, and a name or address. Prose mentioning the
   token — this bullet, or a commit message discussing the rule — is not
   attribution. Case-insensitive, and anywhere in the body rather than only in
   the trailer block.

   Two methods are **excluded**, both found during CL-24 commit verification:

   - `%(trailers)` parses only the final paragraph, so a `Co-Authored-By` line
     sitting mid-message expands to nothing and the check reports zero while
     the line is plainly visible in the text.
   - `grep -c … || true` inside a substitution renders clean-absence and
     check-never-ran identically, because `grep` exits non-zero on no match and
     the fallback swallows it into an empty string.

   A check whose green is indistinguishable from its not having run belongs to
   the check-method family — see that skill — and is worse here for appearing
   in the very command written to verify a house rule.

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
