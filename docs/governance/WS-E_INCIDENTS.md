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
*Derived from items 24, 35, 41, 43, 46; extended by 51 (verification
values), 52 (control-precondition existence), 53 (derived state asserted
from one source) and 55 (recurrence of 51); item 56 escalates 51's rule from
assent to structure (verify and commit may not share a paste).*

**A caveat is not a gate.** An instruction not to proceed, expressed in
prose alongside runnable content, will be overrun - the runnable
content is what the message is read for. Where a step must not proceed
past a point, the message ends at that point and the commands for the
blocked step are withheld entirely. Applies beyond git: any delivered
sequence with a hold in it. *Derived from items 39, 42, 50; extended by 54 (runnable form
regardless of surrounding prose).*

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

49. **ORM default silently diverged from SQL semantics; caught by the
    suite's raw-SQL assertion (2026-07-25).** SQLAlchemy serialises
    Python `None` into a JSON `null` *value* on JSON/JSONB columns by
    default. A JSON null passes `IS NOT NULL` while meaning "not
    populated" — a sentinel masquerading as NULL, the precise failure
    RAT-02 spec section 4 prohibits, and invisible to any test that
    round-trips through the ORM that caused it. Caught on the
    governance suite's first run because the NULL-discipline test
    asserts `IS NULL` in raw SQL. Fixed with `JSONB(none_as_null=True)`
    on all JSONB columns. RULE: invariants about stored state are
    asserted in SQL against the database, not through the abstraction
    layer whose defaults are under test.
50. **Multi-line console paste truncated mid-line inside a here-string;
    write commands queued in the same message ran against the empty
    variables (2026-07-25).** A ~60-line here-string paste dropped its
    tail silently (PSReadLine), leaving the console inside the
    here-string. Separately, a later message supplied the variable
    definitions AND the join-and-write commands together; the runnable
    content was executed in order and the file was written from one
    populated variable plus two empty ones — a structurally valid but
    gutted workflow file reached the working tree, caught by a length
    check before staging. Third exhibit of **A caveat is not a gate**
    in one day, coordinator-side. RULES: (a) delivered multi-line
    content is split into blocks, each assigned to a single variable,
    with an expected `.Length` stated per block; (b) the consuming
    write ships only after every block's length is confirmed from
    output; (c) a length mismatch stops the sequence at that block.
    The length check caught both faults the same evening.
51. **Verification numbers stated without being executed
    (2026-07-25).** Expected here-string lengths were asserted to the
    operator from estimation, twice wrong: once fabricated outright,
    once computed under the wrong newline model (console here-strings
    join lines with LF, not CRLF — an 838 that "should" have been
    861). The operator's correct paste failed a wrong check.
    Generalisation of item 37's rule beyond code idioms: **an expected
    value stated as a check is not ratified until it has been computed
    by execution.** All subsequent checks this session (byte counts,
    character lengths, diff shapes) were machine-computed before being
    stated, and every one then matched first time. Instance of
    **Verify state before mutating it**, extended to delivered
    verification values.
52. **`_staging` bypassed by browser default; three-location hunt for
    a file never downloaded (2026-07-25).** Item 44's postscript
    executed itself: `D:\Downloads\_staging` did not exist at session
    start, the browser default still pointed at `D:\Downloads`, and
    one artefact was hunted across both Downloads folders before
    establishing it had never been downloaded at all. Recovery was by
    console-delivered content (see item 50). No new rule — item 44's
    rules stand; logged as recurrence evidence that creating the
    folder without changing the browser default is a nul control, and
    that the check "does the staging folder exist" belongs in the boot
    ritual rather than the capture step.

53. **Register number reported as fact from one file while a differing
    file of the same base name sat beside it (2026-07-27).**
    `REPO_MANIFEST.md` reported "CL: highest 22 -> next 23", read from
    `GOVERNANCE_REVIEW_CHANGELOG.md`, while an untracked
    `GOVERNANCE_REVIEW_CHANGELOG (1).md` in the same directory carried
    the CL-23 entry and differed from the canonical by exactly that
    20-line block. `CL-23_policy-as-code.md` sat untracked alongside.
    The 25b handover recorded the changelog entry as written, which was
    true of a file DEC-0007 does not recognise as the register. The
    manifest listed tracked and untracked files identically, so nothing
    distinguished landed from pending; it separately reported B7 NOT
    STARTED from BUILD_TRACKER.md while `docs/build/B7_GATE.md` existed
    reading ENTRY CRITERIA MET (5 of 5). Neither the manifest nor
    `check_docs.py` looked for a second file of the same base name.
    Fixing the class in `repo_manifest.py` the same day surfaced three
    further instances of it: `COUNT_DIRS` still named `platform/` after
    DEC-0013 moved it, hiding the entire RAT-02 trio from the boot
    artefact built to show it; `sql/` was in no listing; and the
    open-CL regex `CL-\d+` had never matched `CL-E1`. RULES: (a) a
    derived register is reported with its source, and where a narrative
    document and the filesystem disagree both are shown and the
    divergence raised - neither is silently preferred; (b) a file whose
    name differs from another only by a download suffix is a divergence
    until proven byte-identical, and its remediation differs by commit
    status; (c) a hardcoded list of paths inside a tool that walks the
    tree is itself a parallel document.
54. **Existing text quoted in a fenced block, read as content to paste
    (2026-07-27).** Two lines of a ratified document were reproduced in
    a fenced block to show what the file currently said, in a message
    that also carried genuine paste blocks. The operator asked what to
    do with it rather than acting, so nothing was run. Same family as
    **A caveat is not a gate**: the runnable-looking form is what a
    message is read for, and surrounding prose does not re-label it.
    RULE: a fenced block contains only content to run or to paste;
    existing text being quoted for reference is delivered inline or
    carries an explicit label, in the same message.
55. **Verification values stated without being executed - four
    instances in one session (2026-07-27).** Recurrence of item 51,
    whose rule already covered every one. Expected check values were
    given to the operator uncomputed: `CL-17/19/20 bundle` predicted at
    0 occurrences (actual 1 - a second occurrence in a review-
    disposition section, correctly left as written); a file's first
    three bytes predicted 35,32,42 (actual 35,32,87); "the closeout
    never landed" asserted from a dirty working tree without
    ahead/behind counts (actual 0 ahead, 2 behind - it had landed as
    PR #39); and a screenshot's relative timestamp ("Today at 6:02 PM")
    read as an absolute date, briefly indicting five correct CI
    transcriptions in `B7_GATE.md`. No new rule - item 51 stands.
    Logged as evidence that the rule needs a mechanical prompt rather
    than assent: the value is computed in the same message that states
    it, or it is not stated.

56. **Decision ledger reverted by a stale-download copy; verification
    present but structurally void (2026-07-28).** PR #45 was meant to
    add DEC-0014 to `DECISIONS.md`. Its commit `e88c09f` carried the
    DEC-0014 title but its content was a 25 Jul copy of the ledger:
    `Copy-Item "D:\Downloads\DECISIONS.md"` picked up a three-day-old
    file, the browser having suffixed the current download to
    `DECISIONS (1).md` because the stale one occupied the name — the
    items 38/52 class, now against the decision register itself. The
    merge (`04cb022`) therefore DELETED two lines (DEC-0013 and its
    preceding blank) and added nothing; main carried a ledger without
    the package-path decision until the reland (`baee17a`, PR #46).
    Three controls existed and none fired: (a) the instruction block
    contained line-count, pattern-count and diff-stat checks, but ran
    verify → stage → commit in ONE paste, so no output was seen before
    the commit was issued — item 51's rule was formally present and
    functionally absent; (b) the PR Files Changed tab would have shown
    2 red / 0 green and was not opened; (c) ci-docs passed the broken
    PR because the deleted entry was the only content citing a
    then-missing path — the check that later correctly failed the
    reland had nothing to object to in the inversion. Detection came
    from the post-merge `git pull` diffstat reading `2 --`, read by
    the coordinator. Instruction-side cause: the block author (Claude)
    had gated commit on pasted output all of 27 Jul and regressed to a
    single block on the morning of the 28th. RULES: (a) a command
    block may contain verification OR mutation, never both — a commit,
    push or merge is issued only in a message that follows the pasted
    verification output it depends on; (b) `Copy-Item` from a
    downloads directory names the exact file listed by an immediately
    preceding `Get-ChildItem`, never a bare expected name; (c) the PR
    Files Changed tab is read before every merge — green/red counts
    against the intended diffstat — and this is the merge gate, not
    the checks tick; (d) after any merge, the `git pull` diffstat is
    read against the PR's intended shape before the next action.

57. **Test suite coupled to governed content - four tests red on a
    content change (2026-07-28).** PR #49 r2: ci-devops #80 failed
    with four governance-suite tests asserting properties of the live
    MANIFEST.yaml (counts and hashes), so a legitimate governed
    content change broke machinery tests. The parallel-document class
    (item 53 rule (c)) in test form: a test that hardcodes governed
    content is a parallel register of that content. Fixed at r3 by
    the suite rewrite (48 tests: 27 trio + 21 corpus). RULE (recorded
    in the suite docstring at the rewrite; this entry closes the
    loop): machinery tests run against owned fixtures; the live
    manifest receives only shape-invariant tests.
58. **Verification-skip-under-momentum - three instances in one
    session (2026-07-29).** The aa1a153 CI-green gate was asked four
    times and the Block 3 mutation ran before it was answered
    (resolved benign); Files Changed went unconfirmed pre-merge twice
    (PR #51, #52; caught after by pull diffstat); the manifest-v6
    git-diff eyeball was asked three times and never confirmed before
    commit (belt-and-braces held: read-back, check_append_only,
    silent generator, pinned load). Items 51/55 class, operator-side,
    under session momentum. RULE: a block whose expectation is
    unanswered blocks the next block - the coordinator holds the
    sequence, not just states it; a mutation block is not delivered
    until the verification output it depends on has been pasted.
    Tooling notes to the same class: (a) short SHAs fail OPEN on the
    Actions API head_sha filter (zero results, no error) - always the
    full SHA; (b) an expectation statement names which hashes are
    run-stable (eligible_set, retrieval_snapshot) and which
    legitimately vary (manifest_sha, via ingest_timestamp) - a bare
    "hashes match" expectation is unanswerable.
59. **Angle-bracket placeholder in a runnable block,
    coordinator-executed (2026-07-29).** A Copy-Item carrying a
    placeholder path was authored by the coordinator and executed
    (inc3 fixture redelivery). Third instance of the item 54 class,
    first coordinator-executed. No new rule: the standing fix (no
    angle-bracket placeholders in authored documents or runnable
    examples, now design rule 10 of the corpus skeleton) was already
    in force; this entry evidences it.
60. **Windows newline translation broke content-hash fixtures after a
    green sandbox run (2026-07-29).** pathlib write_text translated
    LF to CRLF on the operator machine, changing fixture bytes and
    therefore content hashes; the Linux sandbox suite had passed on
    identical code. Fixed with write_bytes in the fixture; the
    production ingest path was unaffected. CLASS NOTE: sandbox green
    is advisory, local suites are runs of record - held exactly as
    designed, and the divergence surfaced precisely where the design
    said it would.

61. **rehash_sweep first run: fixture rows in corpus_version; no
    operational pin writer (2026-08-06).** The DEC-0014 item-7
    operator-machine sweep (`scripts/rehash_sweep.py`, ruled
    2026-08-04, landed PR #61), on its first live run, hard-failed
    with two `corpus_version` rows whose pinned manifest_sha256
    values are not reproducible from any historical MANIFEST.yaml.
    Established: (a) both rows were test fixtures (`fixture-*`
    labels) committed by `tests/governance/test_corpus_manifest.py`
    via `load_snapshot` at 2026-07-30 11:00:35 UTC - `conftest.py`
    defaults its DSNs into the local dev database and the tests do
    not clean up; (b) the `.6` run-of-record pin (manifest_sha
    `6a1371fc`, eligible 16) has never existed as a row - a
    repo-wide caller search shows `load_snapshot` is invoked only by
    its own tests; the operational ingest never writes the evidence
    row that `corpus.py`'s docstring defines as proof a version was
    loaded. Remediation ruled 2026-08-06: fixture rows deleted via
    owner role (one-off; app-role DELETE first attempted and
    correctly denied by the grants - a live validation of
    `sql/governance_grants.sql`; transcripts in session record);
    CL-24 raised (test DB isolation); CL-25 raised (wire
    `load_snapshot` into operational ingest - candidate for inc4
    scope); sweep re-run green (0 pins - vacuously and truthfully,
    until CL-25 gives real loads a writer). CLASS NOTE: the sweep
    detecting real state drift on first run, before its own PR
    merged, is the intended behaviour of the control.

62. **CI paths-filter coverage gap, third recurrence: the `.claude/`
    tree absent from the ci-devops PR trigger (2026-08-08).** The
    harness PR (#70) touched only `CLAUDE.md`, the `.claude/` tree
    and `.gitignore`; none matched the `ci-devops` pull_request
    paths filter, so the PR ran `ci-docs` alone (matched via the
    top-level markdown entry) and reported green with no lint leg.
    The repo-wide `ruff check .` therefore first executed on the
    unfiltered `push: branches: [main]` trigger and failed I001
    (import block un-formatted) in
    `.claude/hooks/governance_guard.py` after merge. Remediated
    same-day on branch harness-doc-fix-2026-08-08: autofix applied
    (one blank line; no behavioural change, deny path re-tested and
    still blocking), full lint green, and a recursive `.claude/`
    entry added to the ci-devops paths filter. Same shape as WS-E
    45's two exhibits (`docs/`, then `scripts/`), which the
    workflow's own header comment records. CLASS NOTE: a new
    top-level directory is uncovered until named in each workflow's
    PR filter, and the push-to-main trigger carrying no filter of
    its own makes post-merge the first place the gap can show.

63. **Ceremony renders aborted the ceremony: a non-zero `!` render
    destroyed the skill it belonged to, silently (2026-08-08).** All
    five ceremony skills embedded `!` shell renders whose non-zero
    exit aborted skill expansion before a word of the task text was
    read, so a shell error produced no ceremony and no diagnosis of
    itself - the operator saw an absence, not a failure. The
    sharpest case is `scripts/check_docs.py`, which exits 1 by
    design on any finding: the intolerant render aborted `/pr-prep`
    precisely when the docs check had something to say. Remediated
    same-day in PR #73 (`e8d1a5e`): all five skills audited, every
    render given a marker-line fallback so a failure names its
    cause, and each render labelled OPTIONAL or LOAD-BEARING so the
    task text, not the shell, decides what a failure means. Ruled
    one entry for the class rather than one per skill. Exercised
    2026-08-10, this entry's own session: `/session-open`,
    `/pr-prep` and `/ledger-touch` each rendered under the new
    scheme with every render returning. The fault path itself was
    not exercised - check_docs exited 0 at 100 files - so read as
    scheme in use, not as the abort path proven closed. CLASS NOTE:
    third instance of a family - a check whose green cannot mean
    what it is read to mean - after the three ceremony-skill
    stale-source defects of PR #71 (of which the `/ledger-touch`
    case would have written entry 59 over live items 59-61) and the
    ONNX cache traversal check that returns green under an elevated
    shell. The common shape is an instrument trusted past its
    precondition, and it carries an ordering trap: the defective
    check is the instrument the standing first act relies on, so
    fixing the check precedes trusting any future green from it.

64. **The governance guard never saw the primary shell: a hook wired
    to one tool of two (2026-08-11).** The PreToolUse matcher in
    `.claude/settings.json` named the Bash tool and not the
    PowerShell tool, and `.claude/hooks/governance_guard.py` gated
    its command-inspection branch on the Bash tool alone. Either
    half makes the other a silent no-op. For three days every deny -
    force push, history rewrite, recursive force delete - and every
    protected-store ask was enforced on the Bash path only, while
    PowerShell was and remains this repository's primary shell. Not
    an omission but a severed connection: the guard was written for
    PowerShell from the start, its deny list carrying the recursive
    force-delete forms in both argument orders and its
    write-detection regex carrying the PowerShell content-writing
    cmdlets, all of it unreachable through the very shell it was
    written for. `git blame` puts both halves at the harness install
    commit df3f77d of 2026-08-08, and the hook has been touched once
    since, a lint autofix the same day, so coverage was never
    revisited and the gap was never narrower than at discovery.
    CLAUDE.md's statement that hard rules are enforced by hooks and
    that the hook wins was therefore true of one shell out of two,
    which is the guidance/enforcement discrepancy that document
    itself names a WS-E item. WHY NO HARM RESULTED: the soft layer
    held, and which soft layer held is worth stating, because the
    comfortable answer is wrong. The nearest miss of the period was
    the DEC placement trap of the 2026-08-11 arc, where a document
    was commanded as a four-digit-numbered file under `decisions/`
    and would have consumed ADR numbers silently. No prompt caught
    it and none could have: that path matches none of the guard's
    protected patterns, and no write was ever attempted, because
    `scripts/repo_manifest.py` was read first. What held was the
    working protocol's verification-precedes-mutation rule, not a
    gate. Closed the same day it was found, in the PR carrying this
    entry: the matcher extended to the PowerShell tool and the
    module's shell-tool set made explicit, verified by five crafted
    payloads asserting on decision substance rather than exit status
    and by one end-to-end refusal through the live PowerShell tool
    aimed at a throwaway scratchpad path. CLASS NOTE: the second
    half was found only by probing the first - the matcher change
    alone still returned allow - so a fix to a two-part mechanism is
    unproven until the mechanism is exercised end to end, and a
    guard's stated coverage is a claim about its wiring rather than
    about the patterns it contains.

65. **The governance suite destroys the audit store it exists to
    verify (2026-08-11).** The session-scoped schema fixture in
    `tests/governance/conftest.py` runs `drop_all` then `create_all`
    against the dev `arcaai_audit` database as `arcaai_owner`, so
    every run of the mandatory battery erases every audit event and
    every corpus-version row before the first test executes. Found at
    the 2026-08-11d close from an anomaly rather than by review: the
    boot sweep reported two `fixture-*` pin rows, the battery ran once
    during the arc, and the closing sweep reported two rows again with
    *different identifiers* - not four. Residue that does not
    accumulate is residue being destroyed. CORRECTS WS-E 61, which
    recorded the mechanism as tests that do not clean up. The inverse
    is true and worse: they do not fail to clean up afterwards, they
    destroy beforehand - so that entry's remediation deleted rows
    whose cause was never diagnosed, and the sweep going green
    afterwards was the next suite run's doing as much as the
    deletion's. The append-only property holds exactly as designed for
    the application role, `sql/governance_grants.sql` withholding
    UPDATE and DELETE and two tests in that same file asserting the
    denial, while the owner role drops the tables wholesale: the
    repository's own mandatory battery defeats the guarantee its own
    suite proves. WHY NO HARM RESULTED: nothing of record has ever
    been in that store. CL-25 is open precisely because no operational
    writer exists, so every row the store has ever held was written by
    its own tests. That is a benign accident of sequencing, not a
    control, and it expires the moment an operational writer lands.
    ROUTED, not remediated here: the fix belongs to CL-24, whose scope
    this enlarges from test-data isolation to the separability of test
    writes from governed writes - by database, by schema, or by a
    marker the sweep treats as excluded-by-rule. Owed before D2.2a,
    where the first Commissioning Session Records would be written
    into that store and erased by the next battery run. CLASS NOTE:
    what exposed it was a count that stayed constant when it should
    have grown. An expectation stated as "two rows" would have passed
    every time; the expectation that caught it was "two rows, and
    these two". Identity, not count.

66. **Harness assumed the Postgres superuser account for read-only
    inspection (2026-08-12).** Early in the CL-24 arc, before the
    isolation picture was established, three commands were issued
    through `docker exec` as `psql -U arcaai`, the cluster superuser: a
    database listing and two SELECTs against `arcaai_audit`. Read-only,
    no DDL, no writes, nothing changed. The rule denies elevation
    outright with no exception path, and it is written about which
    account is assumed rather than about what is done once assumed —
    precisely so that "it was only a read" never has to be adjudicated.
    Self-disclosed in-session at the point the isolation work made the
    account choice salient, not found by review. Corrective is
    load-bearing rather than promissory:
    `scripts/governed_store_identity.py` hardcodes the `arcaai_app`
    role and refuses any database but the governed one, and every
    equivalent fact was afterwards re-established non-elevated —
    pg_database is world-readable, so the database listing that
    prompted the breach never required the superuser at all. CLASS
    NOTE: the non-elevated route existed and was not looked for. The
    failure mode is reaching for the account that certainly works, and
    checking first costs nothing.

67. **A CREATE DATABASE reported done had not happened, and the
    mandatory battery was what found it (2026-08-12).** The CL-24
    isolation change requires `arcaai_audit_test` to exist on the
    operator machine, because Postgres runs its `docker-entrypoint-initdb.d`
    scripts only at cluster initialisation and this volume predates the
    new init file. The create was issued at the operator terminal and
    reported done; `scripts\test.cmd` then failed at fixture setup on
    about 27 governance and retrieval tests with `FATAL: database
    "arcaai_audit_test" does not exist`, and a non-elevated read of
    pg_database confirmed six databases with no near-miss spelling —
    nothing had been created under any name. Wrong-container and
    wrong-instance were excluded: `docker ps` showed
    arcaai-dev-postgres-1 as the sole listener on 5432. Cause recorded
    as the command erroring unnoticed with its output unread. Re-issued
    with a catalogue read appended to the same invocation so the act
    carried its own verification, which returned one row; the battery
    then ran green, 165 passed. NO HARM, and the reason matters: the
    failure was fail-closed. The suite errored at connect with no code
    path retrying against the governed database, so an absent test
    database could not silently redirect writes back into
    `arcaai_audit`. CLASS NOTE: a report that a command was issued is
    not existence evidence. What was conveyed here was the act, and no
    output at all — the output went unread, which is precisely where
    the failure was sitting. Only output actually read, or better a
    read of the catalogue itself, establishes that an object exists.
    The distinction is not pedantry about what psql prints: "I ran it"
    and "it worked" are different claims, and only the second is
    evidence. Same family as item 64, the
    `Measure-Object -Line` instance and the queue-block measurement — a
    check whose stated subject is not the subject it interrogates.

## Footnotes

- To 14/25: git log decoration reflects LOCAL refs; a prune racing a
  just-deleted remote branch leaves ghost decoration. See item 33.
- pytest `-v` is overridden by pyproject config (dots print
  regardless); use `-vv` or `--durations=0` when per-test visibility
  matters.
- To 55 (and RAT-01 section 3.1): a relative timestamp is not
  transcribable evidence. "Today at 6:02 PM" in a screenshot carries no
  information without the capture date, and GitHub's Actions list shows
  relative times while a run's own page shows the absolute one. Read
  dates from the run page, not the list.
- To 35: for repo `.md` writes prefer an explicit LF variable over
  `[Environment]::NewLine`, which is CRLF on Windows. `.gitattributes`
  normalises `.md` to LF on staging, so CRLF in the working copy is
  harmless to the committed blob but warns on every `git diff` and
  leaves the working copy unlike what git checks out.
- To 51/55: `git branch -d` reports the deleted branch's *tip*
  commit, not the merge commit that absorbed it; and `git log
  --oneline` on a just-created branch lists the merge first, its own
  commit second (both parents walked in commit-date order). Two
  coordinator expectation misses, benign, recorded so the
  expectations stop being re-derived wrong at each encounter.
- To 56/58: the 58-shape persisted post-ratification - Files Changed
  unread before merge on PRs #55-#58 (one answered late); the 56(d)
  post-merge diffstat read caught or confirmed every one. No new
  rule - the belt-and-braces is carrying the load. Working
  mechanical prompt, in force from the later merges of 30 Jul: the
  coordinator withholds the merge-step block until the Files Changed
  reading is pasted.
- To the 30 Jul session (handover of record; no ledger item):
  chromadb's ONNX cache existence probe fails *open* into a fresh
  83 MB re-download when ACLs block traversal of the cached tree -
  the probe cannot see the cache, assumes absence, re-downloads, and
  the re-extraction then fails overwriting the unreadable survivors,
  so the symptom (`PermissionError` inside `tarfile` extractall)
  points at the archive when the fault is the tree's ACLs. Class
  note from the elevated/normal shell mixing; diagnostic rule:
  extraction PermissionError on a *cached* model -> check tree ACLs
  before suspecting the download.
