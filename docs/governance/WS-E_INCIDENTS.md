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

## Standing principles

Named principles derived from recurring incident classes. Entries cite
them by name and do not restate the reasoning. Named rather than
numbered, to avoid collision with the SS1/23 principle numbering used
elsewhere in the governance set.

**Verify state before mutating it.** Before any command that changes
the repository, the working directory or the environment, the state it
assumes is confirmed from output already available - not from
recollection. Paths, branch, staging contents, active environment. The
check is always cheaper than the recovery, and in every instance so far
the information needed was already on screen and was not read.
*Derived from items 24, 35, 41, 43, 46.*

**A caveat is not a gate.** An instruction not to proceed, expressed in
prose alongside runnable content, will be overrun - the runnable
content is what the message is read for. Where a step must not proceed
past a point, the message ends at that point and the commands for the
blocked step are withheld entirely. Applies beyond git: any delivered
sequence with a hold in it. *Derived from items 39, 42.*

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
40. **Merge before green.**
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

41. **Repo path asserted from memory rather than verified
    (2026-07-25).** A `git add` was issued citing
    `docs/governance/DECISIONS.md`; the file is at repo root. The
    pathspec failed, git's add is atomic on pathspec failure, and
    nothing staged - the error cost one command and no unwinding. Same
    class as 24 and 35 but a distinct cause: not a working-directory or
    encoding problem, an assertion made from recollection of the repo
    layout without checking. The correct layout was available in the
    session and was not consulted. RULE: a path appearing in a runnable
    command is verified against the repo before the command ships - by
    `Get-ChildItem`, by a listing already in the session, or by asking.
    Instance of **Verify state before mutating it**.
42. **Merge proceeded against a stated hold (2026-07-25).** PR #26 was
    merged while the BUILD_TRACKER table change - decision item 2 of the
    artefact being merged - was explicitly outstanding and the
    coordinator had written "do not merge yet". Main briefly carried a
    ratified section describing a tracker shape the tracker did not
    implement. Cause is structural rather than a lapse in reading: the
    hold was stated in prose in the same message that supplied the
    `git commit` and `git push` commands and the PR-creation
    instruction. That is item 39's pattern. RULE (extension of 39, and
    the origin of the standing principle **A caveat is not a gate**):
    when a step must not proceed past a point, the message ends at that
    point; commands for the blocked step are withheld entirely rather
    than supplied with a caveat.
43. **Branch state assumed rather than verified before staging
    (2026-07-25).** A commit intended for a new branch landed on
    `wsd-rat01-gate-plan`, already merged with its remote deleted. The
    branch-creation sequence had been supplied but not run; the
    coordinator moved on to file capture and staging without confirming
    it, and did not read the branch name in the `git status` output
    returned at each subsequent step - the information was present and
    repeatedly ignored. Recovery was clean (`git branch` at HEAD,
    switch, delete the stale label) because nothing had been pushed; had
    the push landed on the old branch name, recovery would have involved
    a deleted remote branch and a merged PR. RULE: after any command
    that changes branch, working directory or environment, the next
    message confirms the new state from returned output before issuing
    further commands. `git status` is read for its branch line, not only
    its file list; `git branch --show-current` is requested before any
    staging step.
    RECURRING HUMAN-FACTOR PATTERN - state assumption under time
    pressure. Items 41, 43 and 46, following 24 and 35, are one pattern
    rather than five incidents: recollection substituted for reading
    information already available, clustering in state that is cheap to
    check, concentrated in the fastest-moving parts of a session.
    Classified explicitly so the trend is visible to later analysis
    rather than embedded in narrative. Governed by **Verify state before
    mutating it**.
44. **General Downloads folder used as capture staging (2026-07-25).**
    Multiple file-capture failures in one session resolved to name
    ambiguity in `D:\Downloads`, which holds 100+ markdown files across
    five projects, many with `(1)`..`(4)` suffixes; one memo exists in
    five versions ranging 8 KB to 46 KB. Item 38's rule - delete stale
    suffixed downloads at capture time - assumes the stale file can be
    seen. At this folder size it cannot be, and the rule silently stops
    working. RULES: (a) repo-bound files are captured to a dedicated
    staging folder, `D:\Downloads\_staging`, holding nothing else, so
    the pre-capture check is "is the folder empty" and the post-capture
    check is "does it hold exactly what I expect" - both answerable at a
    glance. Creating the folder is NOT sufficient: it was created this
    session and the browser continued writing to `D:\Downloads`, because
    download location is a browser setting, not a property a directory
    can claim. Either the browser default changes for the session, or
    the move into staging is an explicit step. (b) Order is download,
    verify, THEN delete the stale copy. Deleting first - as instructed
    three times this session - leaves a window in which the intended
    file exists nowhere, and produced three failed copies. A stale file
    cannot mislead a copy already verified by name and byte count.
45. **"Merge only on green" was unenforceable for documentation PRs
    (2026-07-25).** PRs #25 through #31 showed no checks section; both
    workflows ran only after merge, against `main`. The `paths:`
    triggers do not fire the pipelines on pull requests touching
    `docs/**`, so a governance PR could not report green before merge -
    there was nothing to report. The house rule "merge only on green
    with closures aboard" was therefore unenforceable on every
    documentation-only PR in the programme, including the one that
    logged item 40 for breaching it. Item 40 remains correctly logged;
    what it recorded was a rule already inoperative in that context. A
    rule that cannot fail is not a control. DISPOSITION: option (a),
    ratified 2026-07-25 - add `pull_request` triggers covering
    `docs/**` so documentation PRs report before merge. The rejected
    alternative was to scope the rule to code-touching PRs and record
    the gap as deliberate; rejected because a permanent exception must
    be remembered at exactly the moment it is least likely to be, and
    because documentation changes are the class that most needs
    pre-merge visibility here - they alter the decision record, the gate
    criteria and the claimed regulatory posture. Implementation is
    additive and lightweight: a docs-only workflow running lint, link
    check and a files-present assertion is sufficient; it does not need
    the ML suite, only to exist. FOLLOW-UP QUEUED: workflow change owned
    by Mike, due before the next documentation PR after 2026-07-27.
46. **`git add` on an unchanged path succeeds silently (2026-07-25).**
    `git add DECISIONS.md` was issued twice against a file whose edit
    had not been made. Both calls returned success and staged nothing,
    because the path was valid and the content unchanged. The complement
    of 41: there a bad path failed loudly; here a good path with no
    changes said nothing. The second is more dangerous - the operator
    has no signal that the intended change is missing, and the commit
    proceeds without it. RULE: `git diff --cached --stat` after every
    `git add`, with the file count read against what was expected.
    `git add` returning success is not evidence that anything was
    staged. Instance of **Verify state before mutating it**.
47. **PowerShell default encoding assumption presents as file
    corruption (2026-07-25).** `Get-Content` on `DECISIONS.md` returned
    mojibake where em-dashes and middots belong, presenting as
    corruption in a governance record. The file was intact: PS 5.1's
    `Get-Content` defaults to ANSI for files without a byte-order mark,
    and the house write rule (`UTF8Encoding($false)`) deliberately
    produces BOM-less UTF-8 - the two defaults disagree.
    `Get-Content -Encoding UTF8` rendered it correctly. Extension of
    item 35 in the opposite direction: 35 covered the same default
    assumption at execution, where a BOM-less `.ps1` was parsed as ANSI;
    this is the same assumption at inspection. The consequence is worse
    than it sounds - apparent corruption in a decision log invites a
    repair attempt on a file that is not broken. RULE: repo `.md` files
    are inspected with `Get-Content -Encoding UTF8`; no repair action is
    taken on suspected encoding corruption until the file has been
    re-read with the encoding stated explicitly.
48. **Column-0 continuation inside a list item broke a committed record
    (2026-07-25).** DEC-0010 was drafted wrapped at column 0 across
    sixteen lines inside a bullet. The closing `**` was lost at a line
    break, leaving bold unterminated from mid-entry to the end of
    `DECISIONS.md`, and a code span was closed with an apostrophe rather
    than a backtick. Both survived review and landed on main. Item 40 of
    this ledger carries the identical defect from the same cause,
    introduced when a drafted heading was converted to the numbered
    format and the closing `**` was dropped; repaired 2026-07-25 in the
    same commit as this entry. The fault is specifically UNINDENTED
    continuation: this ledger wraps inside numbered items throughout and
    is safe, because four-space continuation keeps the item intact.
    RULES: (a) continuation lines inside a list item are indented to the
    item's content column, never column 0; (b) DECISIONS.md ledger
    entries are single lines, matching that file's house style; (c)
    delivered text for append follows the target file's existing wrap
    convention, which is read before drafting. Repairs of this class are
    markup correction rather than a change to the record, and are
    therefore addenda rather than DECs under RAT-01 section 3.1.

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
