#!/usr/bin/env python3
"""ArcaAI governance guard — PreToolUse hook.

Deterministic enforcement of the house hard rules. Runs on every tool
call; reads the hook payload as JSON on stdin; answers via JSON on
stdout with a permissionDecision of "deny" or "ask", or exits 0 silently
to allow.

DENY (no exception path):
  - git push --force / -f / force-with-lease (CL-E1 incident guard)
  - git history rewrites reaching the remote (filter-branch, filter-repo)
  - rm -rf / recursive force deletes and PowerShell equivalents
  - git branch -D, and --delete --force (H-11 hardening)
  - find -delete / -exec / -execdir, and sort -o / --output (Option B)
  - writes to the permission and ceremony system itself:
    .claude/settings.json, .claude/hooks/, .claude/skills/,
    .claude/agents/ — the never-silent set, upgraded from ask to deny
    on 2026-08-14 (WS-E 69 fix item 1). See NEVER_SILENT_PATTERNS.

ASK (operator confirmation required — Tier 2):
  - Edit/Write touching MANIFEST.yaml, EDGES.yaml, WS-E_INCIDENTS.md,
    DECISIONS.md, RULINGS_RECORD*.md, document-register.yaml,
    pyproject.toml, .github/workflows/, decisions/
  - Bash/PowerShell commands that redirect or stream into those files
  - PR merge; branch deletion; any git write while HEAD is main, or
    while the branch cannot be established at all

READS ARE UNTOUCHED throughout. The path checks below govern the
file-writing tools and shell write verbs only, so every ceremony that
reads .claude/ - which is all of them - is unaffected by the deny.

Coverage is two-part and both parts must name a tool for it to be
guarded: the PreToolUse matcher in .claude/settings.json routes the
call here, and SHELL_TOOLS below decides whether the command string is
inspected. WS-E 64 records what happens when they disagree.

Cross-platform: pure stdlib, no shell assumptions. Windows-safe.
"""
import json
import pathlib
import re
import subprocess
import sys

# The repository this guard governs, derived from the guard's own location
# rather than from the working directory. WS-E 68 (2026-08-12): a relative
# invocation path plus a persisted cwd deadlocked every tool fail-closed, and
# the same read found current_branch() inheriting the ambient directory - so
# inside a DIFFERENT repository it would have reported that repository's
# branch and could have cleared the HEAD-is-main gate on evidence from the
# wrong tree. An enforcement path must not depend on ambient state that any
# ordinary act can change.
REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]

# Every tool that executes a shell command string. PowerShell is this
# repo's primary shell, and both halves of the guard missed it until
# WS-E 64 (2026-08-11): the settings.json matcher did not route the
# tool here, AND this module gated on tool == "Bash" alone. The
# PowerShell-shaped patterns below (Remove-Item, Set-Content, Out-File,
# Copy-Item) were present from the install commit and unreachable for
# three days — written for a shell the wiring never delivered. Add a
# tool here and to the settings.json matcher together; either alone is
# a silent no-op, which is how the original gap read as green.
SHELL_TOOLS = ("Bash", "PowerShell")

# ----------------------------------------------------------- never-silent set
#
# The permission and ceremony system itself. WS-E 69 fix item 1, operator
# ruling 2026-08-14: these four paths move from ASK to DENY, on both the
# shell branch and the file-writing-tool branch.
#
# WHY THE ASK WAS NOT ENOUGH. The harness never widens its own latitude
# unprompted, and until now that was expressed as an ask - a governed touch
# made deliberate rather than impossible. That reasoning held only while an
# ask was guaranteed to reach a person, and it is not: the 2026-08-14
# discriminator session auto-approved asks without surfacing them, so the
# absence of a prompt evidenced nothing. An ask that a MODE can satisfy is a
# gate whose green is indistinguishable from its never having been put -
# the check-method family - and here it had the harness's own latitude
# behind it.
#
# WHY DENY, AND WHY THERE IS NO MIDDLE. There is no stronger ask. Deny is
# the only response this hook returns that no mode and no approval
# overrides. Unconditional is the property being bought, not a side effect.
#
# WHAT IT COSTS, STATED RATHER THAN DISCOVERED. There is no in-session route
# to these paths again, with or without live operator approval - INCLUDING
# the route that would repair a defect in this guard, or roll back this very
# deny. That is accepted: it is the same route every other denied verb
# already takes. Harness changes are drafted outside the tree (the
# scratchpad is unmatched by these patterns), installed by the operator at
# the operator's own terminal, then branch -> PR -> merge -> restart to
# load. Drafting is unaffected; only installing is denied, and installing is
# the act that changes what every future run means.
#
# WHY THESE FOUR AND NOT THE OTHER EIGHT PROTECTED PATHS. Each of these
# grants latitude. settings.json carries the tiers, and a Tier 1 allow rule
# there pre-empts a Tier 2 guard ask (tested 2026-08-11) - a write here can
# switch a gate off silently. hooks/ is this file. skills/ carry
# allowed-tools frontmatter that governs inside a ceremony, and may carry an
# executing render. agents/ declare what a subagent MAY DO. The other eight
# protected paths are stores the executor must be able to append to as
# ordinary governed acts; denying those would stop the register discipline
# rather than protect it, so they keep their ask.
#
# KNOWN LIMITATION, ASSERTED AS A TEST rather than left in prose. On the
# shell branch a regex cannot tell a source from a destination, so copying
# OUT of these paths - a read - draws the deny too. The route is the Read
# tool, which no path check here touches. This is the false-red direction,
# which is the safe one for a deny.
#
# THESE STAY IN PROTECTED_PATTERNS TOO, spliced in below rather than moved
# out. The duplication is deliberate and must not be tidied away: if the
# never-silent check were ever reordered behind the ask or lost outright,
# these paths degrade to the ASK they drew yesterday rather than to a silent
# allow. Carrying both is safe precisely because this module returns deny or
# ask and never allow, so the two overlapping responses are both
# restrictions - unlike the Tier 1 allow versus Tier 2 ask pairing, where
# the overlap switches the gate off.
NEVER_SILENT_PATTERNS = [
    r"\.claude[/\\]settings\.json",
    r"\.claude[/\\]hooks[/\\]",
    r"\.claude[/\\]skills[/\\]",
    r"\.claude[/\\]agents[/\\]",
]
NEVER_SILENT_RE = re.compile("|".join(NEVER_SILENT_PATTERNS), re.IGNORECASE)

NEVER_SILENT_DENY_PREFIX = "HARNESS WRITE DENIED"

# Named once and shared by both branches, so the two refusals cannot drift
# into describing different routes out of the same deny.
NEVER_SILENT_ROUTE = (
    "There is no in-session route to this path under any mode or approval - "
    "that is the ruled posture (WS-E 69 fix item 1, 2026-08-14), not an "
    "oversight to work around. Draft the change outside the tree, have the "
    "operator install it at the operator's own terminal, then branch -> PR "
    "-> merge -> restart to load it. Reading these paths is unaffected."
)

PROTECTED_PATTERNS = [
    r"MANIFEST\.ya?ml",
    r"EDGES\.ya?ml",
    r"WS-E_INCIDENTS\.md",
    r"(?:^|[/\\])DECISIONS\.md",
    r"RULINGS_RECORD[^/\\]*\.md",
    r"document-register\.ya?ml",
    # Tier 2 additions (permission tiering, 2026-08-11). Each changes
    # what every future run means, so each is gated on every touch.
    r"pyproject\.toml",
    r"\.github[/\\]workflows[/\\]",
    # decisions/ is the ADR register AND its filesystem: repo_manifest
    # reads the leading four digits off each filename, so writing a
    # file here consumes register numbers silently. Register-consuming
    # by mechanism, therefore gated by consequence. The DEC placement
    # trap of the 2026-08-11 arc was caught by protocol, not by a gate
    # (WS-E 64) - this is that gate.
    r"(?:^|[/\\])decisions[/\\]",
] + NEVER_SILENT_PATTERNS
PROTECTED_RE = re.compile("|".join(PROTECTED_PATTERNS), re.IGNORECASE)

# Tier 2, state-dependent. These cannot be expressed as permission
# rules, which match command text and cannot read repository state -
# which is why the branch condition lives here and not in
# settings.json. The guard may only ever restrict: it returns deny or
# ask and never allow, so it can narrow a Tier 1 grant but can never
# widen one.
GIT_WRITE_RE = re.compile(
    r"\bgit\s+(add|commit|push|merge|rebase|reset|revert|cherry-pick|am"
    r"|apply|tag)\b"
)
ASK_COMMAND_RES = [
    (re.compile(r"\bgit\s+branch\s+-[dD]\b"),
     "Branch deletion is gated (Tier 2). Deleting the just-merged branch "
     "is routine, but this guard cannot tell which branch that is - "
     "confirm which branch is going and why."),
]

DENY_COMMAND_RES = [
    # H-11 hardening, operator ruling 2026-08-13: "H-11 hardening in by
    # mechanism". Force-deleting a branch is denied outright; the lowercase
    # -d stays permitted and Tier 1 grants it (PR #109).
    #
    # WHY A DENY AND NOT AN ASK. -d refuses to delete an unmerged branch, and
    # that refusal is the guard the cleandown grant relies on. -D removes the
    # refusal, which is precisely the property that made -d safe to grant. An
    # ask would leave the two forms one keystroke apart with the same prompt
    # behind them; a deny makes the difference mechanical.
    #
    # CASE-SENSITIVE ON PURPOSE. re is case-sensitive by default and this
    # pattern must never gain re.IGNORECASE: folding case here would deny the
    # lowercase form too and silently revoke the ruled cleandown grant.
    #
    # Recovery is not lost. A branch deleted with -d is reachable by reflog,
    # and a genuinely unmerged branch that must go is an operator act at the
    # operator's own terminal - the same route as every other denied verb.
    # Both spellings: -D, and the long form --delete --force (in either
    # order, and --force pairs with nothing else here that this should miss).
    # Caught during probe design: a pattern matching only -D would have left
    # the long form open, which is the same verb reached by a different
    # keystroke - exactly the gap a one-spelling rule string always leaves.
    (re.compile(r"\bgit\s+branch\b(?:[^\n]*\s-D\b|[^\n]*\s--force\b)"),
     "Force branch delete is blocked (-D, or --delete --force). It deletes an "
     "unmerged branch without the refusal that makes -d safe. Use -d, which "
     "declines rather than destroys on surprising state; if the branch is "
     "genuinely unmerged and must go, that is an operator act at your own "
     "terminal."),
    (re.compile(r"git\s+push\b[^\n]*(\s--force\b|\s-f\b|--force-with-lease)"),
     "Force push is prohibited (CL-E1). No exception path exists; "
     "if you believe one is needed, stop and raise it with the operator "
     "outside this tool call."),
    (re.compile(r"git\s+(filter-branch|filter-repo)\b"),
     "Git history rewriting is prohibited on this repository."),
    (re.compile(r"\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r)\b"),
     "Recursive force delete is blocked. Delete specific files "
     "explicitly, one path at a time, with operator confirmation."),
    (re.compile(r"Remove-Item\b[^\n]*-Recurse\b[^\n]*-Force\b|"
                r"Remove-Item\b[^\n]*-Force\b[^\n]*-Recurse\b"),
     "Recursive force delete is blocked (PowerShell). Delete specific "
     "files explicitly with operator confirmation."),
    # Option B pairing, operator ruling 2026-08-14 (queue item 27 arc).
    #
    # WHY THESE EXIST. Amendment 3 restored the read-class families deferred
    # at amendment 2, and two of them are not reads. `find` is deferred as a
    # filesystem read but reaches arbitrary deletion and arbitrary execution;
    # `sort` reaches file creation. The ruling was to grant them as deferred
    # and PAIR each with a deny on its write forms, rather than to narrow the
    # grant - so the read use stays frictionless and the write use is blocked
    # by mechanism.
    #
    # WHY IN THE GUARD AND NOT IN settings.json. Permission rules match
    # command text by prefix; they cannot express a flag appearing anywhere
    # after the command, and they have no alternation. This repository has
    # never carried a `deny` key at all - every deny is here. The decisive
    # precedent is H-11 above: it needed a deny on a FLAG (`git branch -D`)
    # and it went here, using alternation to catch both spellings.
    #
    # THE H-11 LONG-FORM LESSON APPLIED FORWARD. A pattern matching one
    # spelling leaves the other open, which is the same verb reached by a
    # different keystroke. `-exec` is therefore paired with `-execdir`, and
    # `sort -o` with `--output` in both its spaced and `=` forms.
    #
    # BOUNDARIES ARE LOAD-BEARING IN BOTH DIRECTIONS. Each flag must be
    # preceded by whitespace and closed by a word boundary, so that a
    # filename embedding the flag text - `file-delete.txt`, `report-o.txt`,
    # `-name "*-delete*"` - does NOT match. A deny firing on innocent
    # filenames is a false red, and a deny missing a mid-line flag is the
    # false green H-11 exists to prevent. Both are tested.
    #
    # KNOWN AND NOT COVERED, stated rather than left to be discovered.
    # (1) Combined short flags: `sort -ro out.txt` reaches the output flag
    # without a bare `-o` token, and is not matched. Covering it means
    # matching any short-flag cluster ending in `o`, which false-reds on a
    # leading-dash filename; the ruled spec is short form plus long form, and
    # widening it is a decision, not a patch. (2) Flag text inside a quoted
    # argument matches, because a regex cannot see quoting. That is the false
    # red direction, which is the safe one for a deny, and the message names
    # the operator route.
    (re.compile(r"\bfind\b[^\n]*\s-delete\b"),
     "`find` with its delete flag is blocked. The read-class grant covers "
     "searching, not deletion, and a bare `rm` reached this way does not "
     "match the recursive-force deny. Delete specific paths explicitly, one "
     "at a time, with operator confirmation."),
    (re.compile(r"\bfind\b[^\n]*\s-exec(?:dir)?\b"),
     "`find` with an exec flag is blocked (-exec and -execdir both). It runs "
     "an arbitrary command over every match, so the grant on `find` as a "
     "read would otherwise extend to whatever that command does. Run the "
     "search first, read the results, then act on specific paths."),
    (re.compile(r"\bsort\b[^\n]*(?:\s-o\b|\s--output\b)"),
     "`sort` with its output flag is blocked (-o, --output, and --output=). "
     "It writes a file, and the grant on `sort` is a read-class grant. Write "
     "through an explicit, reviewable act instead."),
]

# Bash constructs that can write into a file: redirection, tee, sed -i,
# in-place perl/python, move/copy onto the path.
WRITEY_RE = re.compile(
    r"(>>?|\btee\b|\bsed\b[^\n]*-i|\bmv\b|\bcp\b|\bMove-Item\b|"
    r"\bCopy-Item\b|\bSet-Content\b|\bAdd-Content\b|\bOut-File\b)",
    re.IGNORECASE,
)


# ---------------------------------------------------------------- merge gate
#
# Merge delegation, Option B (operator ruling 2026-08-13, CL-27 arc, queue
# item 27). The candidate clause proposed that `gh pr merge` become an ALLOW
# when the operator's approval and green checks are both present. It is
# deliberately NOT built that way.
#
# The invariant stated above at "Tier 2, state-dependent" is load-bearing and
# is preserved here verbatim in effect: this guard returns deny or ask and
# NEVER allow, so it can narrow a Tier 1 grant but can never widen one. A
# guard that could allow would be a GRANTING mechanism, and every future
# defect in it would confer merge rights rather than merely fail to block.
# Option B keeps the live reads the candidate wanted and spends them on
# refusing early rather than on proceeding automatically:
#
#   approval missing / not APPROVED ............ DENY
#   approval not pinned to current head SHA .... DENY  (approve-push-merge)
#   any check not green ........................ DENY
#   state unreadable or UNKNOWN ................ DENY  (fail closed)
#   approval on current head AND checks green .. ASK   (never allow)
#
# This is strictly stronger than the unconditional ASK it replaces, which
# asked identically on every PR regardless of its state. The operator still
# confirms; what changes is that the confirmation can now only be reached by
# a PR that genuinely carries approval and green checks.
#
# Decision logic is a PURE FUNCTION over a state dict, separate from the IO
# that fetches it. That is not tidiness: it is what makes the refusal paths
# probeable. A stale-approval or checks-failing state can be injected
# directly, where manufacturing a real one would mean creating a genuinely
# broken pull request to test with.

GH_PR_MERGE_RE = re.compile(r"\bgh\s+pr\s+merge\b")
_PR_NUM_RE = re.compile(r"\bgh\s+pr\s+merge\s+(?:[^\s]+\s+)*?(\d+)\b")

MERGE_DENY_PREFIX = "MERGE DENIED"


def _gh_json(args: list[str], timeout: int = 4):
    """Run a gh command expecting JSON on stdout.

    Returns the parsed object, or None for ANY failure — non-zero exit,
    timeout, gh absent, unparseable output. None is UNKNOWN and the caller
    must treat it as a refusal, never as an absence of problems.
    """
    try:
        result = subprocess.run(
            ["gh"] + args, cwd=REPO_ROOT, capture_output=True,
            text=True, timeout=timeout,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except Exception:
        return None


def read_merge_state(command: str) -> dict:
    """Fetch live merge-relevant state for the PR named in ``command``.

    Every field defaults to the UNKNOWN-ish value that denies. Reviews are
    read through the REST API rather than ``gh pr view --json reviews``
    because the latter does not carry the commit each review was submitted
    against, and without that the approval cannot be pinned to the head SHA
    — which is the whole point of the pin.
    """
    state: dict = {"readable": False, "head_oid": None,
                   "approvals_on_head": [], "failing_checks": [],
                   "pending_checks": [], "pr": None}

    match = _PR_NUM_RE.search(command)
    pr = match.group(1) if match else None
    if pr is None:
        view = _gh_json(["pr", "view", "--json", "number"])
        if not isinstance(view, dict) or "number" not in view:
            return state
        pr = str(view["number"])
    state["pr"] = pr

    view = _gh_json(["pr", "view", pr, "--json", "headRefOid,statusCheckRollup"])
    if not isinstance(view, dict) or not view.get("headRefOid"):
        return state
    head = view["headRefOid"]
    state["head_oid"] = head

    for check in view.get("statusCheckRollup") or []:
        name = check.get("name") or check.get("context") or "<unnamed>"
        verdict = (check.get("conclusion") or check.get("state") or "").upper()
        if verdict in ("SUCCESS", "NEUTRAL", "SKIPPED"):
            continue
        if verdict in ("", "PENDING", "QUEUED", "IN_PROGRESS", "EXPECTED"):
            state["pending_checks"].append(name)
        else:
            state["failing_checks"].append(f"{name}={verdict.lower()}")

    reviews = _gh_json(["api", f"repos/{{owner}}/{{repo}}/pulls/{pr}/reviews"])
    if not isinstance(reviews, list):
        return state
    for review in reviews:
        if (review.get("state") or "").upper() != "APPROVED":
            continue
        who = (review.get("user") or {}).get("login") or "<unknown>"
        state["approvals_on_head"].append(
            {"login": who, "commit_id": review.get("commit_id"),
             "on_head": review.get("commit_id") == head}
        )

    state["readable"] = True
    return state


def evaluate_merge_delegation(state: dict) -> tuple[str, str]:
    """Pure decision over merge state. Returns (decision, reason).

    Returns only "deny" or "ask". There is no branch that returns allow, and
    adding one would reverse this module's invariant — see the block comment
    above before considering it.
    """
    if not state.get("readable"):
        return ("deny", (
            f"{MERGE_DENY_PREFIX} (state unreadable): live GitHub state for this "
            "PR could not be read, so approval and checks cannot be shown to "
            "hold. UNKNOWN is not a green and never collapses into proceed. "
            "Merge at the GitHub UI, or re-run once gh can reach the API."))

    approvals = state.get("approvals_on_head") or []
    if not approvals:
        return ("deny", (
            f"{MERGE_DENY_PREFIX} (no approval): the PR carries no APPROVED "
            "review. The operator's approval IS the ruling record; without it "
            "there is nothing for a merge to execute."))

    on_head = [a for a in approvals if a.get("on_head")]
    if not on_head:
        stale = ", ".join(
            f"{a.get('login')}@{str(a.get('commit_id'))[:7]}" for a in approvals)
        return ("deny", (
            f"{MERGE_DENY_PREFIX} (stale approval): approval(s) {stale} were "
            f"submitted against a commit other than the current head "
            f"{str(state.get('head_oid'))[:7]}. Approve-push-merge must not "
            "launder an unreviewed change through an older approval."))

    failing = state.get("failing_checks") or []
    pending = state.get("pending_checks") or []
    if failing or pending:
        detail = "; ".join(filter(None, [
            ("failing: " + ", ".join(failing)) if failing else "",
            ("not yet green: " + ", ".join(pending)) if pending else "",
        ]))
        return ("deny", (
            f"{MERGE_DENY_PREFIX} (checks not green): {detail}."))

    who = ", ".join(a.get("login") or "<unknown>" for a in on_head)
    return ("ask", (
        f"Merge gate satisfied: approved by {who} against the current head "
        f"{str(state.get('head_oid'))[:7]}, all checks green. This guard "
        "never returns allow, so merging remains an operator act (Tier 3) - "
        "confirm before it runs."))


def current_branch() -> str | None:
    """The checked-out branch, or None if it cannot be established.

    None is UNKNOWN, never a green. Callers must treat it as "cannot
    be shown to be off main" and ask, per the check-method rule that
    an unknown rendered as a pass is the shape every false green in
    this repository has taken.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=REPO_ROOT, capture_output=True, text=True, timeout=5,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def respond(decision: str, reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # never wedge the session on a malformed payload

    tool = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}

    if tool in SHELL_TOOLS:
        command = tool_input.get("command", "") or ""
        for pattern, message in DENY_COMMAND_RES:
            if pattern.search(command):
                respond("deny", message)
        # Never-silent set, checked BEFORE the protected-path ask below.
        # respond() exits on the first match, so an ask sitting ahead of
        # this deny would answer for these paths and the upgrade would be
        # inert - a reordering here is a silent revocation, not a tidy-up.
        # The conjunction with WRITEY_RE is deliberate and unchanged: this
        # arc upgrades the RESPONSE for what already matches and does not
        # widen WHAT matches, so the shell branch stays exactly as porous
        # as WRITEY_RE's verb list. Widening that list is its own act.
        if NEVER_SILENT_RE.search(command) and WRITEY_RE.search(command):
            respond("deny", (
                f"{NEVER_SILENT_DENY_PREFIX}: this command writes into the "
                "permission and ceremony system - settings.json, hooks/, "
                f"skills/ or agents/ under .claude/. {NEVER_SILENT_ROUTE}"
            ))
        if PROTECTED_RE.search(command) and WRITEY_RE.search(command):
            respond(
                "ask",
                "This command appears to write into a governed store "
                "(append-only ledger / manifest / rulings / permission "
                "and ceremony system). Confirm the governed act this "
                "serves before it runs.",
            )
        if GH_PR_MERGE_RE.search(command):
            decision, reason = evaluate_merge_delegation(
                read_merge_state(command))
            respond(decision, reason)
        for pattern, message in ASK_COMMAND_RES:
            if pattern.search(command):
                respond("ask", message)
        if GIT_WRITE_RE.search(command):
            branch = current_branch()
            if branch is None:
                respond(
                    "ask",
                    "The current branch could not be established, so this "
                    "git write cannot be shown to be off main. UNKNOWN is "
                    "not a green - confirm explicitly.",
                )
            if branch == "main":
                respond(
                    "ask",
                    "This writes to git while HEAD is main. The house rule "
                    "is feature branch, PR, merge. Confirm the deliberate "
                    "exception before it runs.",
                )

    if tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        path = (tool_input.get("file_path", "")
                or tool_input.get("path", "") or "")
        # Ahead of the protected-path ask, for the reason given on the
        # shell branch above. No verb condition here: this branch is the
        # executor's primary write path and every tool reaching it writes,
        # so a path match alone is the whole condition. Read is absent
        # from the tool tuple above and stays absent - ceremonies read
        # these paths constantly and must keep doing so.
        if NEVER_SILENT_RE.search(path):
            respond("deny", (
                f"{NEVER_SILENT_DENY_PREFIX}: '{path}' is part of the "
                "permission and ceremony system, which no in-session edit "
                f"may touch. {NEVER_SILENT_ROUTE}"
            ))
        if PROTECTED_RE.search(path):
            respond(
                "ask",
                f"'{path}' is a governed store. Edits must be sanctioned "
                "appends serving a named governed act (DEC-0014 / WS-E "
                "discipline). Confirm to proceed.",
            )

    sys.exit(0)


if __name__ == "__main__":
    main()
