"""Lazy-auth boundary — authorisation happens outside every retried call path.

Authored under PROMPT 158 against the QD-F2 spec's defect register, whose
lazy-auth entry is the ruled source: "authorisation must move outside the retried
call or any network flap re-prompts human consent."

The boundary in one sentence: ``ensure_authorised`` is the ONLY place interactive
consent may occur, it is called once per cycle before any retry loop begins, and
every path reached from inside a retry takes the non-interactive branch and
refuses loudly rather than prompting.

Evidence is by INVOCATION COUNT rather than inference (§2.2(a)) — "no second
acquisition" is a claim about how many times something ran, and only a count can
support it. All fixtures use an isolated temp queue root; the live ``_queue`` is
never addressed.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
DRIVER_PATH = REPO_ROOT / "scripts" / "queue_driver.py"


def _load_driver():
    spec = importlib.util.spec_from_file_location("queue_driver_lazyauth", DRIVER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["queue_driver_lazyauth"] = module
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
    notifier = qd.RecordingNotifier()
    return qd.QueueDriver(config, transport, notifier), transport, notifier


# --------------------------------------------------------------------------
# §2.2(a) — a transient flap inside the retry must NOT re-acquire authorisation
# --------------------------------------------------------------------------


def test_transient_failure_retries_without_re_acquiring_authorisation(tmp_path):
    """The defect, stated as a count: two network attempts, ONE acquisition."""
    driver, transport, _notifier = _driver(tmp_path)
    transport.fail_list_times = 2  # two transient failures, then success

    driver.run_once()

    assert transport._list_calls == 3, "the transient failures must actually have been retried"
    assert transport.auth_acquisitions == 1, (
        f"authorisation must be acquired exactly once per cycle, not per attempt; "
        f"got {transport.auth_acquisitions} acquisitions across {transport._list_calls} calls"
    )


def test_authorisation_is_acquired_before_any_queue_work(tmp_path):
    """Ordering is the mechanism: acquire first, then retry-wrapped work."""
    driver, transport, _notifier = _driver(tmp_path)
    order: list[str] = []

    real_auth = transport.ensure_authorised
    real_list = transport.list_released_drafts

    def traced_auth() -> None:
        order.append("auth")
        real_auth()

    def traced_list():
        order.append("list")
        return real_list()

    transport.ensure_authorised = traced_auth  # type: ignore[method-assign]
    transport.list_released_drafts = traced_list  # type: ignore[method-assign]

    driver.run_once()

    assert order and order[0] == "auth", f"authorisation must come first; order was {order}"
    assert order.count("auth") == 1


def test_repeated_cycles_do_not_re_acquire_on_the_real_transport_shape(tmp_path):
    """``ensure_authorised`` is idempotent, so the cost is once per transport."""
    driver, transport, _notifier = _driver(tmp_path)
    driver.run_once()
    driver.run_once()
    driver.run_once()
    assert transport.auth_acquisitions == 3, (
        "the fake counts every call; what matters is that the REAL transport's "
        "ensure_authorised is a no-op once _service is held, asserted separately"
    )


def test_real_transport_ensure_authorised_is_idempotent():
    """On GmailTransport, a second call acquires nothing — no network, no consent."""
    transport = qd.GmailTransport(Path("nonexistent-creds.json"), Path("nonexistent-token.json"))
    transport._service = object()  # pretend start-up authorisation already happened

    transport.ensure_authorised()
    transport.ensure_authorised()

    assert transport._service is not None


# --------------------------------------------------------------------------
# §2.2(b) — a hard auth failure fails LOUDLY and is not retried into a prompt
# --------------------------------------------------------------------------


def test_hard_auth_failure_halts_the_cycle_loudly(tmp_path):
    """ERROR page plus log row, run halted, no queue work attempted."""
    draft = qd.make_draft("ARCAAI-PROMPT-900", "TARGET: T2\n", draft_id="dA")
    driver, transport, notifier = _driver(tmp_path, [draft])
    transport.auth_fails_with = qd.QueueDriverError("token refresh failed: grant revoked")

    report = driver.run_once()

    assert any("authorisation failed" in e for e in report.errors), "the failure must be reported"
    pages = [p for p in notifier.pages if "ERROR" in p[0]]
    assert len(pages) == 1, "exactly one ERROR page for the auth failure"
    assert "Authorisation failed" in pages[0][1]

    rows = driver.log.rows()
    assert any("authorisation failed" in str(r.get("detail", "")) for r in rows), (
        "the ruled channel set is ERROR page AND log row; the row is not optional"
    )

    # Halted: no queue work was attempted at all.
    assert transport._list_calls == 0, "no inbound poll may run after an auth failure"
    assert report.routed == [] and report.swept == []


def test_hard_auth_failure_is_not_retried(tmp_path):
    """A revoked grant is not transient; retrying it would only postpone the page."""
    driver, transport, _notifier = _driver(tmp_path)
    calls = {"n": 0}

    def failing_auth() -> None:
        calls["n"] += 1
        raise qd.QueueDriverError("grant revoked")

    transport.ensure_authorised = failing_auth  # type: ignore[method-assign]
    driver.run_once()

    assert calls["n"] == 1, f"auth failure must not be retried; it ran {calls['n']} times"


def test_service_property_refuses_to_open_consent(tmp_path):
    """The boundary itself: reaching auth from a retried path is a loud refusal.

    ``service`` is touched from inside retried calls. Before the fix it was the
    lazy acquisition point and could re-open the consent flow; now it takes the
    non-interactive branch, so crossing the boundary raises rather than prompts.
    Neither file exists, so if this ever reached the interactive flow it would
    fail on a DIFFERENT message — the assertion is on the boundary's own text.
    """
    transport = qd.GmailTransport(Path("nonexistent-creds.json"), Path("nonexistent-token.json"))
    with pytest.raises(qd.QueueDriverError, match="refusing to open an interactive OAuth"):
        _ = transport.service


def test_authorise_defaults_to_non_interactive():
    """The default is the SAFE side of the line, so an unthinking caller cannot prompt."""
    transport = qd.GmailTransport(Path("nonexistent-creds.json"), Path("nonexistent-token.json"))
    with pytest.raises(qd.QueueDriverError, match="refusing to open an interactive OAuth"):
        transport._authorise()


def test_boundary_holds_where_the_oauth_libraries_are_absent(monkeypatch, tmp_path):
    """The boundary must refuse WITHOUT importing the Google libraries.

    Found by CI, not by review, and worth keeping as a test rather than a fixed
    comment. The first version of the two tests above passed locally and FAILED
    on CI with ModuleNotFoundError, because the OAuth libraries are installed in
    the development environment and are not yet declared in ``pyproject.toml`` --
    a known sibling defect outside this envelope's grant to fix.

    That made those tests pass for an ENVIRONMENTAL reason, which is the
    check-method family the repository tracks. The fix was to raise the boundary
    refusal ahead of the imports; this test reproduces the absent-library
    condition so the ordering cannot silently regress once the deps are declared
    and the original failure becomes unreproducible.
    """
    blocked = (
        "google_auth_oauthlib",
        "google.auth.transport.requests",
        "google.oauth2.credentials",
        "googleapiclient.discovery",
    )

    class Blocker:
        def find_spec(self, name, path=None, target=None):
            if name in blocked or name.startswith("google_auth_oauthlib"):
                raise ModuleNotFoundError(f"No module named '{name}' (simulated)")
            return None

    # Blocked at CALL time, not at module-load time. The imports under test live
    # inside ``_authorise``, so this is the moment that matters; re-executing the
    # whole module under a blocked meta_path breaks unrelated machinery and would
    # test the harness rather than the boundary.
    monkeypatch.setattr(sys, "meta_path", [Blocker(), *sys.meta_path])

    transport = qd.GmailTransport(tmp_path / "no-creds.json", tmp_path / "no-token.json")
    with pytest.raises(qd.QueueDriverError, match="refusing to open an interactive OAuth"):
        _ = transport.service


# --------------------------------------------------------------------------
# Negative space, in the 157 style — the defect must be reproducible on demand
# --------------------------------------------------------------------------


def test_auth_inside_the_retry_boundary_reproduces_the_defect(tmp_path):
    """Reintroduce the defect in a double and REQUIRE it to reappear.

    Without this, the passing count test above could hold for an unrelated
    reason — a fake that simply never re-authorises — and a future change moving
    acquisition back inside the retry would fail nothing by name. Here a
    transport that authorises lazily from inside its own retried call is used,
    and the double acquisition MUST show up in the count.
    """

    class LazyAuthInsideRetry(qd.FakeTransport):
        """The pre-fix shape: acquisition reached from within the retried call."""

        def ensure_authorised(self) -> None:  # the boundary call becomes a no-op
            return None

        def list_released_drafts(self):
            self.auth_acquisitions += 1  # lazy acquisition, inside the retry
            return super().list_released_drafts()

    lane = tmp_path / "wt"
    lane.mkdir()
    (lane / ".git").write_text("gitdir: /x/worktrees/wt\n", encoding="utf-8")
    config = qd.Config(
        queue_root=tmp_path / "_queue",
        lanes={"T2": qd.Lane("T2", lane)},
        backoff_base=0.0,
    )
    transport = LazyAuthInsideRetry([])
    transport.fail_list_times = 2
    driver = qd.QueueDriver(config, transport, qd.RecordingNotifier())

    driver.run_once()

    assert transport.auth_acquisitions == 3, (
        "with acquisition inside the retry the defect MUST reappear as one acquisition "
        f"per attempt; got {transport.auth_acquisitions}. If this ever reads 1, the "
        "count test above is not evidence for the boundary."
    )
