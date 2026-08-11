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

ASK (operator confirmation required — governed stores):
  - Edit/Write touching MANIFEST.yaml, EDGES.yaml, WS-E_INCIDENTS.md,
    DECISIONS.md, RULINGS_RECORD*.md, document-register.yaml
  - Bash/PowerShell commands that redirect or stream into those files

Coverage is two-part and both parts must name a tool for it to be
guarded: the PreToolUse matcher in .claude/settings.json routes the
call here, and SHELL_TOOLS below decides whether the command string is
inspected. WS-E 64 records what happens when they disagree.

Cross-platform: pure stdlib, no shell assumptions. Windows-safe.
"""
import json
import re
import sys

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
]
PROTECTED_RE = re.compile("|".join(PROTECTED_PATTERNS), re.IGNORECASE)

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
                "(append-only ledger / manifest / rulings). Confirm the "
                "governed act this serves before it runs.",
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
