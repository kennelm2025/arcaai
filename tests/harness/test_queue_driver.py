"""Checks for the ARCAAI queue driver (``scripts/queue_driver.py``), PROMPT 129/129R.

Two kinds of check live here and they are not interchangeable.

STRUCTURAL checks assert properties of the source that no runtime test can
establish: that the driver never imports ``subprocess`` and never invokes git.
Requirement 6 forbids the driver touching the working trees, and a runtime test
can only show that it did not happen on the paths exercised. A source scan
shows the capability is absent.

BEHAVIOURAL checks drive the real routing code through a fake transport. The
module's own ``--selftest`` is invoked as one of them, so CI runs the same
dry-run scenarios the envelope's item 8 names rather than a reduced copy of them.

A note on why the corrupting-write case exists at all: a mutation probe run
while building this suite stubbed the B2 read-back comparison to always agree,
and the dry run stayed green — the verification was unfalsifiable because
expected and actual agreed by construction. The seam that makes it falsifiable
is ``QueueDriver._write_bytes``. That is the check-method family at queue
item 8, found in this suite rather than in production, and it is the reason
every check below was probed by mutation before being trusted.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
DRIVER_PATH = REPO_ROOT / "scripts" / "queue_driver.py"


def _load_driver():
    spec = importlib.util.spec_from_file_location("queue_driver", DRIVER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["queue_driver"] = module
    spec.loader.exec_module(module)
    return module


qd = _load_driver()


# --------------------------------------------------------------------------
# Structural: the capability to touch a working tree is absent, not merely unused
# --------------------------------------------------------------------------


def test_driver_never_imports_subprocess_or_git():
    source = DRIVER_PATH.read_text(encoding="utf-8")
    code_lines = [
        line
        for line in source.splitlines()
        if line.startswith(("import ", "from ")) or line.lstrip().startswith(("import ", "from "))
    ]
    joined = "\n".join(code_lines)
    assert "subprocess" not in joined, "driver must not import subprocess (requirement 6)"
    assert "import git" not in joined, "driver must not import a git binding"
    assert "os.system" not in source, "driver must not shell out"
    assert "pygit2" not in joined


def test_worktree_identity_is_established_without_running_git(tmp_path):
    """The B1 assertion is a pure read of the .git pointer file."""
    lane = tmp_path / "wt"
    lane.mkdir()
    (lane / ".git").write_text("gitdir: /elsewhere/.git/worktrees/wt\n", encoding="utf-8")
    result = qd.assert_lane_isolation(qd.Lane("T9", lane))
    assert result.outcome == "GREEN"
    assert result.gitdir == "/elsewhere/.git/worktrees/wt"


# --------------------------------------------------------------------------
# Lane isolation (DEC-0019 B1) — three outcomes, never two
# --------------------------------------------------------------------------


def test_main_tree_is_red_not_green(tmp_path):
    main = tmp_path / "main"
    (main / ".git").mkdir(parents=True)
    result = qd.assert_lane_isolation(qd.Lane("T9", main))
    assert result.outcome == "RED"
    assert "UNISOLATED" in result.detail


def test_absent_worktree_is_red(tmp_path):
    result = qd.assert_lane_isolation(qd.Lane("T9", tmp_path / "nope"))
    assert result.outcome == "RED"
    assert not result.routable


def test_git_file_without_gitdir_pointer_is_unknown_not_green(tmp_path):
    lane = tmp_path / "wt"
    lane.mkdir()
    (lane / ".git").write_text("this is not a pointer\n", encoding="utf-8")
    result = qd.assert_lane_isolation(qd.Lane("T9", lane))
    assert result.outcome == "UNKNOWN"
    assert not result.routable


def test_two_lanes_sharing_a_path_are_both_refused(tmp_path):
    lane = tmp_path / "wt"
    lane.mkdir()
    (lane / ".git").write_text("gitdir: /x/worktrees/wt\n", encoding="utf-8")
    config = qd.Config(
        queue_root=tmp_path / "_queue",
        lanes={"TA": qd.Lane("TA", lane), "TB": qd.Lane("TB", lane)},
    )
    results = qd.assert_all_lanes(config)
    assert not results["TA"].routable
    assert not results["TB"].routable
    assert "collides" in results["TA"].detail


# --------------------------------------------------------------------------
# Envelope parsing
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "subject,expected",
    [
        ("ARCAAI-PROMPT-129", ("129", "129", "")),
        ("ARCAAI-PROMPT-129R", ("129R", "129", "R")),
        ("ARCAAI-PROMPT-127R3", ("127R3", "127", "R3")),
    ],
)
def test_parse_subject_handles_revisions(subject, expected):
    assert qd.parse_subject(subject) == expected


@pytest.mark.parametrize(
    "subject",
    ["", "PROMPT-129", "ARCAAI-PROMPT-", "ARCAAI-PROMPT-12X", "Re: ARCAAI-PROMPT-129"],
)
def test_parse_subject_refuses_malformed(subject):
    with pytest.raises(qd.QueueDriverError):
        qd.parse_subject(subject)


def test_parse_target_reads_the_header_block():
    body = "PROMPT 129 | TARGET: T2 | CLASS: harness-build\n\nbody\n"
    assert qd.parse_target(body) == "T2"


def test_parse_target_ignores_lane_mentions_in_prose():
    """A prompt discussing another lane must not route to it.

    PROMPT 129 itself names T1 in its dispatch discussion, which is exactly the
    shape that would misroute under a whole-body scan.
    """
    body = (
        "PROMPT 129 | TARGET: T2 | CLASS: harness-build\n"
        "\n" * 12
        + "Later prose discussing TARGET: T1 at length.\n"
    )
    assert qd.parse_target(body) == "T2"


def test_parse_target_refuses_conflicting_header_targets():
    body = "PROMPT 1 | TARGET: T1 | TARGET: T2\n\nbody\n"
    with pytest.raises(qd.QueueDriverError, match="conflicting TARGET"):
        qd.parse_target(body)


def test_parse_target_refuses_absent_target():
    with pytest.raises(qd.QueueDriverError, match="no TARGET"):
        qd.parse_target("PROMPT 1 | CLASS: x\n\nbody\n")


def test_body_prompt_number_must_agree_with_subject():
    with pytest.raises(qd.QueueDriverError, match="body says PROMPT 130"):
        qd.check_body_prompt_number("PROMPT 130 | TARGET: T2\n", "129")


def test_body_without_prompt_token_is_accepted_and_noted():
    notes = qd.check_body_prompt_number("TARGET: T2\n", "129")
    assert notes and "subject taken as authority" in notes[0]


# --------------------------------------------------------------------------
# Transformations are a closed, logged set
# --------------------------------------------------------------------------


def test_bom_is_stripped_and_reported():
    data, notes = qd.strip_bom(qd.BOM + b"PROMPT 1")
    assert data == b"PROMPT 1"
    assert notes == ["stripped UTF-8 BOM from draft body"]


def test_absent_bom_produces_no_note():
    data, notes = qd.strip_bom(b"PROMPT 1")
    assert data == b"PROMPT 1"
    assert notes == []


def test_google_redirect_wrapper_is_unwrapped():
    raw = b"see https://www.google.com/url?q=https%3A%2F%2Fex.invalid%2Fa&sa=D end"
    data, notes = qd.normalise_gmail_rewrites(raw)
    assert b"https://ex.invalid/a" in data
    assert b"google.com/url" not in data
    assert notes and "redirect wrapper" in notes[0]


def test_angle_bracket_wrapping_is_unwrapped():
    data, notes = qd.normalise_gmail_rewrites(b"path <https://ex.invalid/a> here")
    assert data == b"path https://ex.invalid/a here"
    assert notes


def test_line_endings_are_not_normalised():
    """CRLF is preserved: nothing rules on it and byte-for-byte is the requirement."""
    raw = b"line one\r\nline two\r\n"
    data, notes = qd.normalise_body(raw)
    assert data == raw
    assert notes == []


# --------------------------------------------------------------------------
# Outcome status vocabulary and the ntfy policy (B6)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("status", ["COMPLETE", "BLOCKED-RULING", "RETRYING", "ERROR"])
def test_status_vocabulary_round_trips(status):
    parsed, notes = qd.parse_outcome_status(f"STATUS: {status}\n\nbody\n".encode())
    assert parsed == status
    assert notes == []


def test_unknown_status_becomes_error_not_silence():
    parsed, notes = qd.parse_outcome_status(b"STATUS: FINISHED\n\nbody\n")
    assert parsed == qd.ERROR
    assert notes and "outside vocabulary" in notes[0]


def test_missing_status_line_becomes_error():
    parsed, notes = qd.parse_outcome_status(b"no status here\n")
    assert parsed == qd.ERROR
    assert notes


def test_ntfy_policy_pages_exactly_two_statuses():
    assert qd.PAGING_STATUSES == {qd.BLOCKED_RULING, qd.ERROR}
    assert qd.COMPLETE not in qd.PAGING_STATUSES
    assert qd.RETRYING not in qd.PAGING_STATUSES


# --------------------------------------------------------------------------
# Retry policy: transient only
# --------------------------------------------------------------------------


def test_transient_failures_are_retried_then_raised():
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        raise qd.TransientError("boom")

    with pytest.raises(qd.TransientError):
        qd.retry_with_backoff(flaky, retries=3, base=0.0, sleep=lambda _s: None)
    assert calls["n"] == 4, "one initial attempt plus three retries"


def test_refusals_are_not_retried():
    calls = {"n": 0}

    def refusing():
        calls["n"] += 1
        raise qd.QueueDriverError("malformed")

    with pytest.raises(qd.QueueDriverError):
        qd.retry_with_backoff(refusing, retries=3, base=0.0, sleep=lambda _s: None)
    assert calls["n"] == 1, "a malformed envelope retried is still malformed"


# --------------------------------------------------------------------------
# Write-scope guard
# --------------------------------------------------------------------------


def _driver_for(tmp_path):
    lane = tmp_path / "wt"
    lane.mkdir()
    (lane / ".git").write_text("gitdir: /x/worktrees/wt\n", encoding="utf-8")
    config = qd.Config(
        queue_root=tmp_path / "_queue",
        lanes={"T2": qd.Lane("T2", lane)},
        backoff_base=0.0,
    )
    return qd.QueueDriver(config, qd.FakeTransport([]), qd.RecordingNotifier()), lane


def test_write_outside_queue_root_is_refused(tmp_path):
    driver, _lane = _driver_for(tmp_path)
    with pytest.raises(qd.QueueDriverError, match="outside the queue root"):
        driver._assert_within_queue(tmp_path / "escape.md")


def test_write_inside_a_lane_worktree_is_refused(tmp_path):
    """The lane guard needs a lane nested INSIDE the queue root to be reached at all.

    With the lane outside the queue root — the ordinary layout — the
    outside-the-root guard fires first and this branch is never exercised. An
    earlier version of this test asserted the lane message against the ordinary
    layout and passed on the other guard's refusal, which is a check passing
    for a reason other than its name.
    """
    queue_root = tmp_path / "_queue"
    lane = queue_root / "nested-wt"
    lane.mkdir(parents=True)
    (lane / ".git").write_text("gitdir: /x/worktrees/nested\n", encoding="utf-8")
    config = qd.Config(
        queue_root=queue_root, lanes={"T2": qd.Lane("T2", lane)}, backoff_base=0.0
    )
    driver = qd.QueueDriver(config, qd.FakeTransport([]), qd.RecordingNotifier())
    with pytest.raises(qd.QueueDriverError, match="inside lane worktree"):
        driver._assert_within_queue(lane / "evil.md")


# --------------------------------------------------------------------------
# The dry run itself, so CI exercises the same scenarios the envelope names
# --------------------------------------------------------------------------


def test_offline_dry_run_is_green():
    assert qd.run_selftest() == 0
