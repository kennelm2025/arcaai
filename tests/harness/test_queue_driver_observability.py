"""Observability rows — auth acquisition and per-poll heartbeat.

Authored under PROMPT 161, the first post-lift act scheduled by DEC-0020. The two
rows close the two shortfalls that ruling accepted as known limitations of the
logging surface rather than as preconditions of the lift:

  * acquisitions were uncountable — the 159 trial could only offer indirect
    evidence (an expired token plus a completed run with no consent prompt);
  * a healthy quiet loop was indistinguishable from a dead one — quiet polls
    wrote nothing, so an absence of rows meant either "polling, nothing to do"
    or "process died", with no way to tell which.

Every fixture uses an isolated temp queue root. The live ``_queue`` is never
addressed, and the running loop is never stopped, restarted or touched.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DRIVER_PATH = REPO_ROOT / "scripts" / "queue_driver.py"


def _load_driver():
    spec = importlib.util.spec_from_file_location("queue_driver_obs", DRIVER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["queue_driver_obs"] = module
    spec.loader.exec_module(module)
    return module


qd = _load_driver()


def _driver(tmp_path, drafts=None):
    lane = tmp_path / "wt"
    lane.mkdir()
    (lane / ".git").write_text("gitdir: /x/worktrees/wt\n", encoding="utf-8")
    config = qd.Config(
        queue_root=tmp_path / "_queue",
        lanes={"T2": qd.Lane("T2", lane)},
        backoff_base=0.0,
    )
    transport = qd.FakeTransport(list(drafts or []))
    return qd.QueueDriver(config, transport, qd.RecordingNotifier()), transport


def _rows(driver, action):
    return [r for r in driver.log.rows() if r.get("action") == action]


# --------------------------------------------------------------------------
# §2.3(a) — N polls produce exactly N heartbeats, zero-action polls included
# --------------------------------------------------------------------------


def test_every_poll_writes_exactly_one_heartbeat_including_quiet_ones(tmp_path):
    """The whole point: a poll that does nothing must still leave a mark."""
    driver, _t = _driver(tmp_path)

    for _ in range(5):
        driver.run_once()

    beats = _rows(driver, qd.ACT_HEARTBEAT)
    assert len(beats) == 5, f"5 polls must write 5 heartbeats, got {len(beats)}"
    assert [b["poll"] for b in beats] == [1, 2, 3, 4, 5], "ordinals must be 1..N in order"
    # Every one of these polls was entirely quiet — nothing routed, swept or paged.
    for b in beats:
        assert (b["routed"], b["refused"], b["swept"], b["paged"], b["errors"]) == (0, 0, 0, 0, 0)


def test_heartbeat_counts_reflect_what_the_poll_actually_did(tmp_path):
    """A liveness row that always read zero would be a clock, not a signal."""
    driver, _t = _driver(tmp_path)
    outbox = driver.config.outbox("T2")
    outbox.mkdir(parents=True, exist_ok=True)
    (outbox / "PROMPT-900.outcome.md").write_text("STATUS: COMPLETE\n\nbody\n", encoding="utf-8")

    driver.run_once()  # poll 1 sweeps one outcome
    driver.run_once()  # poll 2 is quiet

    beats = _rows(driver, qd.ACT_HEARTBEAT)
    assert beats[0]["swept"] == 1, "poll 1 swept one outcome and must say so"
    assert beats[1]["swept"] == 0, "poll 2 swept nothing and must say so"


def test_poll_ordinal_is_per_run_not_per_log(tmp_path):
    """A fresh driver restarts at 1 — the heartbeat describes THIS run.

    Carrying the ordinal across restarts would blur two runs into one trail, and
    the question the row answers is "is this process alive and how far has it
    got", which is a per-process question.
    """
    driver, _t = _driver(tmp_path)
    driver.run_once()
    driver.run_once()

    second = qd.QueueDriver(driver.config, qd.FakeTransport([]), qd.RecordingNotifier())
    second.run_once()

    beats = _rows(second, qd.ACT_HEARTBEAT)
    assert [b["poll"] for b in beats] == [1, 2, 1], (
        "the third heartbeat is the new run's first, so its ordinal restarts at 1"
    )


# --------------------------------------------------------------------------
# §2.3(b) — one acquisition plus M refreshes produce 1 + M labelled rows
# --------------------------------------------------------------------------


def test_one_acquisition_across_many_polls_writes_exactly_one_auth_row(tmp_path):
    """Criterion (c) of the 159 trial, now countable from the log."""
    driver, transport = _driver(tmp_path)

    for _ in range(6):
        driver.run_once()

    auth = _rows(driver, qd.ACT_AUTH)
    assert len(auth) == 1, f"6 polls, one credential: expected 1 AUTH row, got {len(auth)}"
    assert auth[0]["poll"] == 1, "the acquisition happened on the first poll"
    assert auth[0]["mode"] == qd.AUTH_TOKEN_LOADED
    # And the trail is long enough to prove the other five polls happened at all.
    assert len(_rows(driver, qd.ACT_HEARTBEAT)) == 6


def test_auth_rows_distinguish_consent_from_refresh(tmp_path):
    """The two sides of the 158 boundary must never need inferring from a row."""
    for mode in (qd.AUTH_CONSENT, qd.AUTH_REFRESH, qd.AUTH_TOKEN_LOADED):
        sub = tmp_path / mode
        sub.mkdir()
        driver, transport = _driver(sub)
        transport.auth_mode = mode
        driver.run_once()
        auth = _rows(driver, qd.ACT_AUTH)
        assert len(auth) == 1 and auth[0]["mode"] == mode, f"{mode} must be recorded verbatim"

    assert qd.AUTH_CONSENT != qd.AUTH_REFRESH, "the human-gated and automatable sides differ"


def test_reused_credential_writes_no_auth_row(tmp_path):
    """Silence is the evidence the boundary held.

    A row on every poll would make acquisitions uncountable again — the very
    shortfall this act closes — so the absence of rows after the first is not an
    omission, it is the signal.
    """
    driver, _t = _driver(tmp_path)
    driver.run_once()
    before = len(_rows(driver, qd.ACT_AUTH))
    for _ in range(4):
        driver.run_once()
    assert len(_rows(driver, qd.ACT_AUTH)) == before == 1


def test_failed_authorisation_writes_no_auth_row_but_still_halts_loudly(tmp_path):
    """A failure is not an acquisition and must not be counted as one."""
    driver, transport = _driver(tmp_path)
    transport.auth_fails_with = qd.QueueDriverError("grant revoked")

    report = driver.run_once()

    assert _rows(driver, qd.ACT_AUTH) == [], "no credential was acquired, so no AUTH row"
    assert any("authorisation failed" in e for e in report.errors)


# --------------------------------------------------------------------------
# §2.3(c) — a run killed mid-poll leaves the trail at the last COMPLETED poll
# --------------------------------------------------------------------------


def test_a_poll_that_dies_midway_leaves_no_heartbeat_for_itself(tmp_path):
    """Dead-versus-quiet, demonstrated rather than asserted.

    The heartbeat is written at the END of the cycle. A poll interrupted before
    it finishes therefore contributes no row, so the trail's last ordinal is the
    last poll that actually completed. That is precisely what lets a reader tell
    a loop that is quietly working from one that stopped: the quiet loop's trail
    keeps growing, the dead one's does not.
    """
    driver, _t = _driver(tmp_path)
    driver.run_once()
    driver.run_once()

    boom = RuntimeError("process killed mid-poll")

    def exploding_sweep(report):
        raise boom

    driver.sweep_outboxes = exploding_sweep  # type: ignore[method-assign]

    try:
        driver.run_once()
    except RuntimeError as exc:
        assert exc is boom
    else:
        raise AssertionError("the third poll was supposed to die midway")

    beats = _rows(driver, qd.ACT_HEARTBEAT)
    assert [b["poll"] for b in beats] == [1, 2], (
        "the interrupted third poll must leave no heartbeat; the trail ends at 2"
    )


def test_the_heartbeat_trail_distinguishes_a_quiet_loop_from_a_stopped_one(tmp_path):
    """The 159 finding, inverted into a check.

    Two drivers over the same queue root: one keeps polling, one stops. Before
    this act both looked identical in the log — nothing written by either. Now
    the difference is visible without inspecting the OS.
    """
    driver, _t = _driver(tmp_path)
    for _ in range(3):
        driver.run_once()
    stopped_at = len(_rows(driver, qd.ACT_HEARTBEAT))

    # ... time passes, and a LIVE loop keeps writing where a dead one would not.
    for _ in range(3):
        driver.run_once()
    alive_at = len(_rows(driver, qd.ACT_HEARTBEAT))

    assert stopped_at == 3 and alive_at == 6
    assert alive_at > stopped_at, "a live loop's trail grows; a stopped one's does not"


# --------------------------------------------------------------------------
# Negative space, 157 style — suppress the heartbeat and the 159 gap returns
# --------------------------------------------------------------------------


def test_suppressing_the_heartbeat_reproduces_the_liveness_gap(tmp_path):
    """REQUIRE the defect to reappear when the mechanism is removed.

    Without this, every assertion above could hold for an unrelated reason and a
    future change dropping the heartbeat write would fail nothing by name. Here
    the write is neutered and the pre-161 condition must return: a run of quiet
    polls leaves a log indistinguishable from a run that never happened.
    """
    driver, _t = _driver(tmp_path)
    driver._write_heartbeat = lambda report: None  # type: ignore[method-assign]

    for _ in range(5):
        driver.run_once()

    beats = _rows(driver, qd.ACT_HEARTBEAT)
    assert beats == [], (
        "with the heartbeat suppressed the log must fall silent again — if it does "
        "not, the tests above are not evidence for the heartbeat"
    )
    # And this is the gap itself, stated as an assertion: nothing in the log
    # distinguishes five completed polls from zero.
    assert driver.log.rows() and all(
        r.get("action") != qd.ACT_HEARTBEAT for r in driver.log.rows()
    )


# --------------------------------------------------------------------------
# Shape of the rows, so a later reader can rely on the fields
# --------------------------------------------------------------------------


def test_rows_are_json_lines_with_the_documented_fields(tmp_path):
    driver, _t = _driver(tmp_path)
    driver.run_once()

    raw = driver.config.log_path.read_text(encoding="utf-8").splitlines()
    parsed = [json.loads(line) for line in raw if line.strip()]

    beat = [r for r in parsed if r["action"] == qd.ACT_HEARTBEAT][0]
    for key in ("timestamp", "action", "poll", "routed", "refused", "swept", "paged", "errors"):
        assert key in beat, f"heartbeat row must carry {key}"

    auth = [r for r in parsed if r["action"] == qd.ACT_AUTH][0]
    for key in ("timestamp", "action", "mode", "poll"):
        assert key in auth, f"auth row must carry {key}"
