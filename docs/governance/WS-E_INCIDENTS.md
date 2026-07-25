# WS-E — Process Incident Ledger

Append-only register of process incidents (tooling traps, workflow
failures, discipline gaps) and the rules they produced. Numbering is
continuous and reserved. Authoritative home of WS-E as of this file's
creation (2026-07-23, PR #20); prior items lived only in session
handover documents.

**Backfill rider:** items 1-23 to be transcribed from the handover
archive in a hygiene session (same bucket as the locked-suite disk
sprawl purge). Items 24-27 are entered as summaries pending the same
backfill. Discovery that no WS-E item had ever been committed to the
repo is itself CL-08 evidence.

## Items

1-23. *Reserved — backfill from handover archive.*

24. PowerShell path resolution trap. (Summary; full text in
    handover 2026-07-22. Backfill.)
25. Local tidy-up sequencing. (Summary; full text in handover
    2026-07-22. Backfill.) See also footnote under 29.
26. Boot ritual gaps. (Summary; full text in handover 2026-07-22.
    Backfill.)
27. Backtick paste handling. (Summary; full text in handover
    2026-07-22. Backfill.)

28. **DEC misfiled into ADR register.** DEC/ADR namespace separation
    held on paper, failed at filesystem level — the ADR folder is
    named `decisions/`, inviting it. Guard paragraph added to
    decisions/README.md. Candidate: rename folder `adrs/` someday.

29. **Here-string writes omit trailing newline → ruff W292 in CI.**
    RULE: run `ruff check --fix` locally before any Python-touching
    commit (joins the git-diff eyeball). Amend-and-force-with-lease
    is the fix pattern pre-merge on own PR branch; never post-merge.

30. **Notepad clobber of DEC-0008 during pointer edit.** Caught at
    pre-add diff eyeball, restored from HEAD, edit redone. Exhibit B
    (2026-07-24): BUILD_TRACKER.md wholesale-overwritten with a script
    during the B6 row edit; caught pre-add, `git restore`, redone —
    second save by the same tripwire in two sessions.
31. **Chained multi-command pastes bit twice.** (a) ruff/pytest chain
    swallowed pytest output; (b) commit+push chained past a skipped
    `git add` — commit no-op'd, push shipped an empty branch. RULE
    (trialled): ship-critical git sequences run one command per
    prompt; read each output before the next.
32. **Boarding-item attrition.** Tracker bump missed across five
    prompts (PR #20). Exhibits (2026-07-24): harness fixture-import
    edit specified in plan, not landed, hit twice at runtime. RULE
    (trialled): written boarding checklist ticked against `git status`
    before `git add`, not a mental list.
33. **Stale scrollback misled twice more.** Extension of 14/25:
    `git log` / `Select-String` are the truth-tellers, not terminal
    history or decoration.
34. **Provenance key mismatch caught by first live e2e run.**
    packaging.py read `sha256`/`platt_params`; the score node emits
    `artifact_sha256`/`platt_a`+`platt_b`. Invisible to unit tests on
    an invented canned fixture; the `platt_params` variant produced a
    factually wrong governed note with no exception. Fixed in the inc5
    PR; fixtures consolidated to `agent/fixtures.py` mirroring live
    shape. Cross-ref docs/build/B6_GATE.md.
35. **Script-delivery encoding + working-directory class (2026-07-24).**
    A BOM-less UTF-8 `.ps1` was parsed by Windows PowerShell 5.1 as ANSI:
    each em-dash (E2 80 94) decoded via Windows-1252, whose trailing byte
    0x94 is a curly closing double-quote, silently terminating string
    literals and producing parser errors pointing nowhere near the fault.
    Second clause, same script: `[IO.File]` static methods resolve
    relative paths against the .NET process working directory, which
    `Set-Location` does not change - the first run looked for DECISIONS.md
    in `C:\Users\mikek` (recurrence of item 24, now with the fix stated as
    a pin rather than a habit). Third clause: downloaded scripts carry
    Mark-of-the-Web and are refused under RemoteSigned until
    `Unblock-File`. All three caught before any write; guards held,
    nothing corrupted. RULES: (a) any `.ps1` delivered for PS 5.1
    execution is UTF-8 WITH BOM - repo `.md` stays no-BOM, the two rules
    coexist because the consumers differ; (b) any script calling
    `[IO.File]` pins `[Environment]::CurrentDirectory =
    (Get-Location).Path` or uses absolute paths only; (c) `Unblock-File`
    is a named step in the delivery sequence, not an ad-hoc recovery.
36. **Panel-capture labelling (2026-07-24).** Governance Checkpoint 01
    Round 1 outputs were returned unlabelled; a duplicate of Grok's review
    was presented as ChatGPT's, and byte-identical text came within one
    step of entering the record as two independent concurring reviews.
    Caught by coordinator text comparison before analysis began. Had it
    landed, a unanimity claim would have rested on a single reviewer.
    RULE: panel outputs are labelled reviewer + round at the moment of
    capture; the coordinator runs a distinctness check before any
    cross-round analysis.
37. **Ratified rule shipped without execution (2026-07-24).** The
    backtick-free newline idiom ratified in item 27, `[char]13 +
    [char]10`, is defective when passed to `String.Replace`: the
    concatenation evaluates to a two-character string, PowerShell
    resolves the overload from the second argument to
    `Replace(Char,Char)`, and the cast throws at runtime. The rule sat
    in the ledger from 22 Jul and was never executed once before being
    delivered in a script. Caught on first run of the WS-E 35-36
    append; guards held, no write occurred. RULES: (a) cast explicitly
    to `[string]` when a `[char]` value feeds `.Replace`; (b) a house
    rule that expresses a code idiom is not ratified until the idiom
    has been run at least once.
38. **Download-suffix ambiguity reached a commit (2026-07-24).** Three
    copies of the same handover sat in Downloads - clean, `(1)` at 8 KB
    superseded, `(2)` at 10 KB authoritative - and all three were copied
    into `docs/governance/` and staged, producing a 4-file 522-insertion
    commit where 2 files and 45 insertions were intended. Caught on the
    GitHub compare page before any PR existed; repaired by
    `git reset --soft HEAD~1`, removal, restage, force-with-lease.
    Third occurrence of the class (07-22b hash forensics, the 17:32 /
    17:34 / 17:53 trio, this). Prior judgement that the class was not
    worth logging because it had not yet bitten was wrong; it bit
    within the hour. RULES: (a) stale suffixed downloads are deleted at
    capture time, before any copy step is written; (b) the copy step
    names its source with `-LiteralPath` and is verified by byte size
    against the expected file before `git add`; (c) `git status` is read
    against a written boarding list, not scanned - the extra two files
    were on screen and not seen (item 32 recurrence).
39. **Command delivered ahead of its step (2026-07-24).** A repair
    sequence was issued with the concluding `git push --force-with-lease`
    in a runnable block alongside prose instructing that the commit be
    held for a further edit. The push ran directly after the restage,
    while HEAD was still at the reset target, forcing the remote branch
    back to `ee0c916`. No loss - the staged set survived and the branch
    had no PR or reviewer - but the remote briefly misrepresented the
    work. Coordinator-side fault, not operator: runnable blocks read as
    a queue regardless of surrounding prose. RULE: no command appears in
    a runnable block before the step it belongs to; forward steps are
    described in prose only, and the next block is issued after its
    predecessor's output has been read.
40. **Merge before green
    PR #25 was merged without waiting for the PR checks to report. Both
    pipelines ran green against main minutes later, and the substance was
    nil (two markdown files, no Python), so no harm followed. The house
    rule is "merge only on green with closures aboard", and the signal is
    meant to arrive before the merge, not after it. Logged as a near miss:
    a near-miss ledger earns its keep on the harmless cases, because the
    harmful ones are indistinguishable from them at the moment of the
    decision.
    Rule (restatement, not new): the PR checks must report green before the
    merge button is used. A merge whose checks are still queued is held,
    regardless of how small the diff looks.

## Footnotes

- To 14/25: git log decoration reflects LOCAL refs; a prune racing a
  just-deleted remote branch leaves ghost decoration. See item 33.
- pytest `-v` is overridden by pyproject config (dots print
  regardless); use `-vv` or `--durations=0` when per-test visibility
  matters.
- To 35: for repo `.md` writes prefer an explicit LF variable over
  `[Environment]::NewLine`, which is CRLF on Windows. `.gitattributes`
  normalises `.md` to LF on staging, so CRLF in the working copy is
  harmless to the committed blob but warns on every `git diff` and
  leaves the working copy unlike what git checks out.
