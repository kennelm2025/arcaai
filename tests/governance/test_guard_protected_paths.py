"""Unit coverage for the never-silent path deny (WS-E 69 fix item 1).

Written for the ask -> deny upgrade ruled by the operator on 2026-08-14.
Four paths - ``.claude/settings.json``, ``.claude/hooks/``,
``.claude/skills/``, ``.claude/agents/`` - drew an ASK until that ruling
and now draw a DENY on both branches of the guard.

WHY THE UPGRADE, in one line so this file stands alone: an ask can be
satisfied by a MODE rather than by a person, as the 2026-08-14
discriminator session demonstrated when it auto-approved asks without
surfacing them. A deny is the only response no mode overrides.

THESE TESTS DRIVE ``main()``, NOT THE PATTERNS. The sibling file
``test_guard_deny_patterns.py`` mirrors the deny loop and asserts regexes
directly, which is the right shape for a flat list. It is the wrong shape
here, because this arc's whole failure mode is ORDERING: ``respond()``
exits on first match, so a never-silent deny placed behind the
protected-path ask would be inert while every regex in it still matched
perfectly. A test that asserted the pattern would pass against a guard
that never reaches it. So each case below feeds a real hook payload on
stdin and reads the decision off stdout.

WHAT THIS FILE STILL DOES NOT EVIDENCE, stated because the distinction
has cost this repository three days once already (WS-E 64). It asserts
that the module decides correctly when it is invoked. It says nothing
about whether the PreToolUse matcher in ``.claude/settings.json`` routes
the tool here at all. A guard can be perfectly correct and completely
unreachable, and only a live deny-shaped probe returning this guard's own
refusal text separates the two. That probe is owed at the landing of this
change, in DEFAULT mode - deny-precedence outside ``bypassPermissions``
is unproven and is itself an open WS-E 69 item.

BOUNDARY, KEPT VISIBLE. This arc upgrades the RESPONSE for what already
matches; it does not widen WHAT matches. The shell branch remains exactly
as porous as ``WRITEY_RE``'s verb list, and the ``test_boundary_*`` cases
below assert that porosity deliberately so that the separate verb-coverage
act shows up here as a change in behaviour rather than as a quiet
improvement nobody ruled.
"""

from __future__ import annotations

import importlib.util
import io
import json
import pathlib
import sys

import pytest

GUARD_PATH = (
    pathlib.Path(__file__).resolve().parents[2]
    / ".claude" / "hooks" / "governance_guard.py"
)


def _load_guard():
    """Load the guard by path; it is a hook script, not a package member.

    Resolved from this file's own location rather than the working
    directory, for the reason the guard itself records at WS-E 68.
    """
    spec = importlib.util.spec_from_file_location("governance_guard", GUARD_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


guard = _load_guard()

FILE_WRITING_TOOLS = ("Edit", "Write", "MultiEdit", "NotebookEdit")


@pytest.fixture()
def decide(monkeypatch, capsys):
    """Run the hook end to end; return its decision dict, or None for allow.

    None means the guard fell through to ``sys.exit(0)`` having printed
    nothing, which is how it allows. That is a real third outcome and is
    never collapsed into a pass or a fail by the callers below.
    """

    def _decide(tool: str, tool_input: dict) -> dict | None:
        payload = {"tool_name": tool, "tool_input": tool_input}
        monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
        with pytest.raises(SystemExit) as exit_info:
            guard.main()
        assert exit_info.value.code == 0, "the hook must always exit 0"
        out = capsys.readouterr().out.strip()
        return json.loads(out)["hookSpecificOutput"] if out else None

    return _decide


# --------------------------------------------------------------- deny, paths
# Both separators, absolute and repo-relative, and a case-folded spelling -
# PROTECTED_RE and NEVER_SILENT_RE are both IGNORECASE and that must stay
# true, since Windows will happily hand either casing to the hook.
NEVER_SILENT_PATHS = [
    ".claude/settings.json",
    ".claude\\settings.json",
    "D:/ArcaAI-repo/arcaai/.claude/settings.json",
    "D:\\ArcaAI-repo\\arcaai\\.claude\\hooks\\governance_guard.py",
    ".claude/hooks/governance_guard.py",
    ".claude/skills/session-open/SKILL.md",
    ".claude\\skills\\pr-prep\\SKILL.md",
    ".claude/agents/corpus-lister.md",
    ".claude\\agents\\probe-route-b.md",
    "D:/ArcaAI-repo/arcaai/.CLAUDE/HOOKS/governance_guard.py",
]


@pytest.mark.parametrize("path", NEVER_SILENT_PATHS)
def test_file_tool_writes_to_never_silent_paths_are_denied(decide, path):
    result = decide("Write", {"file_path": path})
    assert result is not None, f"no decision at all for {path!r}"
    assert result["permissionDecision"] == "deny", (
        f"{path!r} drew {result['permissionDecision']!r}, not deny. An ask "
        f"here is satisfiable by a mode, which is the defect this arc closes."
    )
    assert guard.NEVER_SILENT_DENY_PREFIX in result["permissionDecisionReason"]


@pytest.mark.parametrize("tool", FILE_WRITING_TOOLS)
def test_every_file_writing_tool_is_covered(decide, tool):
    """All four write tools, not just the two in daily use.

    A deny wired to ``Write`` alone would leave ``Edit`` open, which is the
    same act reached by a different tool name - the H-11 long-form lesson
    applied to the tool tuple instead of to a flag spelling.
    """
    result = decide(tool, {"file_path": ".claude/hooks/governance_guard.py"})
    assert result is not None and result["permissionDecision"] == "deny"


def test_alternate_path_key_is_covered(decide):
    """``path`` as well as ``file_path``: main() reads either."""
    result = decide("NotebookEdit", {"path": ".claude/settings.json"})
    assert result is not None and result["permissionDecision"] == "deny"


# --------------------------------------------------------------- deny, shell
SHELL_WRITE_FORMS = [
    "Set-Content -Path .claude\\settings.json -Value x",
    "Add-Content .claude/agents/probe.md 'x'",
    "Out-File -FilePath .claude\\skills\\session-open\\SKILL.md",
    "echo {} > .claude/settings.json",
    "cat patch.json >> .claude/settings.json",
    "cp /tmp/guard.py .claude/hooks/governance_guard.py",
    "Copy-Item C:\\tmp\\guard.py D:\\repo\\.claude\\hooks\\guard.py",
    "mv draft.md .claude/skills/session-open/SKILL.md",
    "Move-Item x.md .claude\\agents\\y.md",
    "sed -i s/ask/deny/ .claude/hooks/governance_guard.py",
    "tee .claude/settings.json",
]


@pytest.mark.parametrize("command", SHELL_WRITE_FORMS)
@pytest.mark.parametrize("tool", guard.SHELL_TOOLS)
def test_shell_writes_to_never_silent_paths_are_denied(decide, tool, command):
    """Parametrised across BOTH shell tools on purpose.

    PowerShell is this repository's primary shell and was missing from the
    guard's tool set for three days (WS-E 64). A test that exercised Bash
    alone would have been green throughout that window.
    """
    result = decide(tool, {"command": command})
    assert result is not None, f"no decision at all for {command!r}"
    assert result["permissionDecision"] == "deny", (
        f"{command!r} drew {result['permissionDecision']!r}, not deny."
    )
    assert guard.NEVER_SILENT_DENY_PREFIX in result["permissionDecisionReason"]


# ------------------------------------------------- allow: reads must survive
# The operator's stated requirement for this arc: a file merely NAMED like
# a protected path in a read command must not trip the deny. Every ceremony
# in this repository reads .claude/ and none of them may start prompting.
READ_FORMS_ON_NEVER_SILENT_PATHS = [
    "Get-Content .claude\\settings.json",
    "cat .claude/settings.json",
    "type .claude\\hooks\\governance_guard.py",
    "python .claude/hooks/governance_guard.py --selftest",
    "grep -rn respond .claude/hooks/",
    "ls .claude/skills/",
    "Get-ChildItem .claude\\agents\\",
    "head -20 .claude/agents/corpus-lister.md",
    "diff .claude/settings.json settings.expected.json",
    "Test-Path .claude\\skills\\session-open\\SKILL.md",
]


@pytest.mark.parametrize("command", READ_FORMS_ON_NEVER_SILENT_PATHS)
@pytest.mark.parametrize("tool", guard.SHELL_TOOLS)
def test_reads_naming_a_never_silent_path_are_not_denied(decide, tool, command):
    result = decide(tool, {"command": command})
    assert result is None, (
        f"read command {command!r} drew {result} - a deny on a read is a "
        f"false red that would stop every ceremony that inspects .claude/."
    )


def test_read_tool_on_a_never_silent_path_is_not_gated(decide):
    """``Read`` is absent from the file-writing tuple and must stay absent."""
    assert decide("Read", {"file_path": ".claude/settings.json"}) is None


# -------------------------------------------- allow: adjacent innocent paths
ADJACENT_INNOCENTS = [
    "CLAUDE.md",
    "docs/governance/HARNESS_PERMISSION_TIERS_2026-08-11.md",
    "docs/governance/claude-settings-notes.md",
    "docs/governance/notes-on-claude-hooks.md",
    "tests/governance/test_guard_protected_paths.py",
    "C:/Users/x/AppData/Local/Temp/claude/scratchpad/governance_guard.py",
    "C:/Users/x/AppData/Local/Temp/claude/scratchpad/settings.json",
]


@pytest.mark.parametrize("path", ADJACENT_INNOCENTS)
def test_adjacent_innocent_paths_are_not_gated(decide, path):
    """Named like a protected path, or about one, but not one.

    The scratchpad entries are load-bearing rather than decorative: the
    ruled working method is that harness changes are DRAFTED there and
    installed by the operator. If the deny reached the draft location, the
    posture would have no authoring route at all and the arc would be
    self-defeating.
    """
    assert decide("Write", {"file_path": path}) is None


# ------------------------------- the other eight protected paths still ASK
STILL_ASK_PATHS = [
    "DECISIONS.md",
    "verticals/fraud/corpus/MANIFEST.yaml",
    "verticals/fraud/corpus/EDGES.yaml",
    "docs/governance/WS-E_INCIDENTS.md",
    "docs/governance/RULINGS_RECORD_2026-08-14_example.md",
    "docs/governance/document-register.yaml",
    "pyproject.toml",
    ".github/workflows/ci-devops.yml",
    "decisions/0011-example.md",
]


@pytest.mark.parametrize("path", STILL_ASK_PATHS)
def test_other_protected_paths_still_ask_and_are_not_denied(decide, path):
    """The upgrade is four paths wide, and the boundary is the point.

    These are stores the executor must be able to append to as ordinary
    governed acts. Denying them would stop the register discipline rather
    than protect it, so an over-broad deny fails here loudly.
    """
    result = decide("Write", {"file_path": path})
    assert result is not None, f"{path!r} lost its gate entirely"
    assert result["permissionDecision"] == "ask", (
        f"{path!r} drew {result['permissionDecision']!r}; the never-silent "
        f"set is four paths wide and this is not one of them."
    )
    assert guard.NEVER_SILENT_DENY_PREFIX not in result["permissionDecisionReason"]


def test_shell_write_to_a_still_ask_path_is_an_ask(decide):
    """An unanchored protected path, which is six of the eight."""
    result = decide(
        "PowerShell",
        {"command": "Set-Content docs/governance/WS-E_INCIDENTS.md -Value x"},
    )
    assert result is not None and result["permissionDecision"] == "ask"
    assert guard.NEVER_SILENT_DENY_PREFIX not in result["permissionDecisionReason"]


PRE_EXISTING_ANCHOR_GAP = [
    "Set-Content DECISIONS.md -Value x",
    "Set-Content decisions/0011-example.md -Value x",
    "echo x > DECISIONS.md",
]


@pytest.mark.parametrize("command", PRE_EXISTING_ANCHOR_GAP)
def test_known_gap_anchored_patterns_miss_a_bare_filename_mid_command(
    decide, command
):
    """PRE-EXISTING, NOT INTRODUCED HERE, and NOT FIXED HERE.

    Two of the twelve protected patterns are anchored -
    ``(?:^|[/\\\\])DECISIONS\\.md`` and ``(?:^|[/\\\\])decisions[/\\\\]``.
    The anchor is correct for the file-writing-tool branch, where the path
    IS the whole string, and wrong for the shell branch, where a filename
    follows a space and reaches neither alternative. So a shell write to
    DECISIONS.md or into decisions/ draws NO gate at all - not an ask, not
    a deny. The other ten patterns are unanchored and match mid-command.

    Found by this arc's own suite on 2026-08-14 and left alone
    deliberately: closing it widens WHAT matches for two paths outside the
    never-silent set, and the ruled boundary for this arc is that it
    upgrades the RESPONSE only. Asserted here so the gap is visible in a
    run rather than resting in a comment, and so that fixing it later
    turns this test red - which is the signal that it worked.

    One pattern list is serving two different string shapes, which is the
    root of it. That is a design question and therefore a ruling.
    """
    assert decide("PowerShell", {"command": command}) is None


# ------------------------------------------------------------ structural
def test_never_silent_patterns_remain_inside_protected_patterns():
    """The deliberate duplication, asserted so it cannot be tidied away.

    If the never-silent check were ever reordered behind the ask or removed,
    these paths must degrade to the ASK they drew before 2026-08-14 rather
    than to a silent allow. That fallback only exists while the four
    patterns are also spliced into PROTECTED_PATTERNS.
    """
    for pattern in guard.NEVER_SILENT_PATTERNS:
        assert pattern in guard.PROTECTED_PATTERNS, (
            f"{pattern!r} left PROTECTED_PATTERNS. The duplication is the "
            f"fail-degraded path, not redundancy to be removed."
        )


def test_never_silent_set_is_exactly_the_four_ruled_paths():
    """Widening this set is a ruling, not a patch. Four, and these four."""
    assert len(guard.NEVER_SILENT_PATTERNS) == 4
    assert guard.NEVER_SILENT_RE.search(".claude/settings.json")
    assert guard.NEVER_SILENT_RE.search(".claude/hooks/x.py")
    assert guard.NEVER_SILENT_RE.search(".claude/skills/x/SKILL.md")
    assert guard.NEVER_SILENT_RE.search(".claude/agents/x.md")
    assert not guard.NEVER_SILENT_RE.search(".github/workflows/ci-devops.yml")


def test_pre_existing_force_push_deny_still_answers_first(decide):
    """Regression: the CL-E1 deny must keep its own message.

    The new deny was inserted into the same branch. If it had gone in ahead
    of the DENY_COMMAND_RES loop, a force push naming a .claude/ path could
    have come back with the wrong refusal - still a deny, so still green to
    a careless assertion, while the incident guard's own text vanished.
    """
    result = decide("Bash", {"command": "git push --force origin main"})
    assert result is not None and result["permissionDecision"] == "deny"
    assert "Force push is prohibited (CL-E1)" in result["permissionDecisionReason"]
    assert guard.NEVER_SILENT_DENY_PREFIX not in result["permissionDecisionReason"]


# ------------------------------------------------------------ boundaries
# Asserted, not described. Each of these is a live gap on the day this
# landed; the separate WRITEY_RE verb-coverage act will turn these red,
# and that red is the signal that it worked, not a regression.
BOUNDARY_UNMATCHED_COMMANDS = [
    "rm .claude/hooks/governance_guard.py",
    "Remove-Item .claude\\agents\\probe-route-b.md",
    "New-Item -ItemType File .claude\\skills\\x\\SKILL.md",
    "python -c \"open('.claude/settings.json','w').write('{}')\"",
    "git checkout -- .claude/hooks/governance_guard.py",
]


@pytest.mark.parametrize("command", BOUNDARY_UNMATCHED_COMMANDS)
def test_boundary_verbs_outside_writey_re_are_not_matched(decide, command):
    """The verb-coverage boundary, kept visible in the suite.

    This arc changes the response for what matches. It does not widen what
    matches, and pretending otherwise would let the change be reported as
    closing a hole it never touched.
    """
    assert decide("PowerShell", {"command": command}) is None


def test_boundary_relative_path_without_the_dot_claude_prefix(decide):
    """A command addressing the file from inside .claude/ does not match.

    The patterns require the ``.claude/`` prefix in the command string. The
    house no-bare-cd convention is what keeps this narrow in practice, which
    means a convention is load-bearing for a mechanism - worth knowing.
    """
    assert decide("PowerShell", {"command": "Set-Content settings.json -Value x"}) is None


def test_known_limitation_copying_out_of_a_protected_path_is_denied(decide):
    """A regex cannot tell a source from a destination.

    Copying OUT of .claude/ is a read, and it draws the deny anyway. This is
    the false-red direction, which is the safe one for a deny; the route is
    the Read tool, which no path check here touches. Asserted so that any
    future change to this behaviour is a decision rather than a drift.
    """
    result = decide("PowerShell", {"command": "Copy-Item .claude\\settings.json bak.json"})
    assert result is not None and result["permissionDecision"] == "deny"


def test_known_limitation_redirect_away_from_a_protected_path_is_denied(decide):
    """Same shape: the read is of .claude/, the write is elsewhere."""
    result = decide("Bash", {"command": "grep -rn respond .claude/hooks/ > notes.txt"})
    assert result is not None and result["permissionDecision"] == "deny"
