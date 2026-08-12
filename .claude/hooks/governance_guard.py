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

ASK (operator confirmation required — Tier 2):
  - Edit/Write touching MANIFEST.yaml, EDGES.yaml, WS-E_INCIDENTS.md,
    DECISIONS.md, RULINGS_RECORD*.md, document-register.yaml,
    pyproject.toml, .github/workflows/, .claude/settings.json,
    .claude/hooks/, .claude/skills/, decisions/
  - Bash/PowerShell commands that redirect or stream into those files
  - PR merge; branch deletion; any git write while HEAD is main, or
    while the branch cannot be established at all

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
    # The permission and ceremony system gates itself: the harness
    # never widens its own latitude unprompted, and settings.json is
    # the file the tiers themselves live in.
    r"\.claude[/\\]settings\.json",
    r"\.claude[/\\]hooks[/\\]",
    r"\.claude[/\\]skills[/\\]",
    # decisions/ is the ADR register AND its filesystem: repo_manifest
    # reads the leading four digits off each filename, so writing a
    # file here consumes register numbers silently. Register-consuming
    # by mechanism, therefore gated by consequence. The DEC placement
    # trap of the 2026-08-11 arc was caught by protocol, not by a gate
    # (WS-E 64) - this is that gate.
    r"(?:^|[/\\])decisions[/\\]",
]
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
    (re.compile(r"\bgh\s+pr\s+merge\b"),
     "Merging a PR is an operator act (Tier 3). Confirm before it runs."),
    (re.compile(r"\bgit\s+branch\s+-[dD]\b"),
     "Branch deletion is gated (Tier 2). Deleting the just-merged branch "
     "is routine, but this guard cannot tell which branch that is - "
     "confirm which branch is going and why."),
]

DENY_COMMAND_RES = [
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
]

# Bash constructs that can write into a file: redirection, tee, sed -i,
# in-place perl/python, move/copy onto the path.
WRITEY_RE = re.compile(
    r"(>>?|\btee\b|\bsed\b[^\n]*-i|\bmv\b|\bcp\b|\bMove-Item\b|"
    r"\bCopy-Item\b|\bSet-Content\b|\bAdd-Content\b|\bOut-File\b)",
    re.IGNORECASE,
)


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
        if PROTECTED_RE.search(command) and WRITEY_RE.search(command):
            respond(
                "ask",
                "This command appears to write into a governed store "
                "(append-only ledger / manifest / rulings / permission "
                "and ceremony system). Confirm the governed act this "
                "serves before it runs.",
            )
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
