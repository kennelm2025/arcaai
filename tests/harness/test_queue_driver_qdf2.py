"""QD-F2 conformance — refused-draft terminal state and swept-outcome archive.

Authored under PROMPT 157 against the twelve Chair rulings of 22 August 2026
(`docs/governance/RULINGS_RECORD_2026-08-22_post156.md`), implementing the design
at `docs/governance/QDF2_DESIGN_NOTE_2026-08-22.md`.

Ruling 7 admits ONE implementation envelope but requires the two mechanisms to be
evidenced SEPARATELY, so the two groups below are kept apart and neither shares a
fixture with the other. A single combined test that happened to pass would not
tell the chair which mechanism it passed for.

Every test builds an isolated queue root under pytest's ``tmp_path``. The live
``_queue`` is never touched, and ``test_tests_never_touch_the_live_queue`` asserts
that as a property of the fixture rather than leaving it to reviewer discipline.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
DRIVER_PATH = REPO_ROOT / "scripts" / "queue_driver.py"


def _load_driver():
    spec = importlib.util.spec_from_file_location("queue_driver_qdf2", DRIVER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["queue_driver_qdf2"] = module
    spec.loader.exec_module(module)
    return module


qd = _load_driver()


ENVELOPE_BODY = "# PROMPT 900\nTARGET: T2\n\nBody of the envelope.\n"


def _config(tmp_path):
    lane = tmp_path / "wt"
    lane.mkdir()
    (lane / ".git").write_text("gitdir: /x/worktrees/wt\n", encoding="utf-8")
    return qd.Config(
        queue_root=tmp_path / "_queue",
        lanes={"T2": qd.Lane("T2", lane)},
        backoff_base=0.0,
    )


def _driver(tmp_path, drafts=None):
    config = _config(tmp_path)
    transport = qd.FakeTransport(list(drafts or []))
    notifier = qd.RecordingNotifier()
    return qd.QueueDriver(config, transport, notifier), transport, notifier


def _all_files(root: Path) -> set[Path]:
    return {p for p in root.rglob("*") if p.is_file()}


# --------------------------------------------------------------------------
# Fixture safety: the live queue is out of reach
# --------------------------------------------------------------------------


def test_tests_never_touch_the_live_queue(tmp_path):
    """The isolation is asserted, not merely intended.

    DEC-0016's lesson is that a suite which can reach the governed store will
    eventually erase it. The queue is not a database, but the reasoning carries:
    a fixture that COULD address the live `_queue` is one typo from doing so.
    """
    config = _config(tmp_path)
    resolved = Path(str(config.queue_root)).resolve()
    assert resolved.is_relative_to(Path(str(tmp_path)).resolve())
    for lane_id in config.lanes:
        for path in (config.dead(lane_id), config.done(lane_id), config.outbox(lane_id)):
            assert Path(str(path)).resolve().is_relative_to(resolved)


# --------------------------------------------------------------------------
# Mechanism (a) — refused-draft terminal state (rulings 1, 2, 3, 6, 12)
# --------------------------------------------------------------------------


def test_refused_draft_is_relabelled_refused_not_consumed(tmp_path):
    """Ruling 1. The terminal relabel is the act that closes the paging defect."""
    draft = qd.make_draft("ARCAAI-PROMPT-900", "no target header here", draft_id="dA")
    driver, transport, _notifier = _driver(tmp_path, [draft])

    driver.poll_inbound(qd.CycleReport())

    assert transport.refused == ["dA"], "the refused draft must reach the terminal label"
    assert transport.consumed == [], "a refused draft must never be marked consumed"


def test_refused_draft_stops_re_paging_on_subsequent_polls(tmp_path):
    """The defect itself: three pages in three passes becomes one page.

    This is the test the whole mechanism exists for, so it drives the real
    ``poll_inbound`` three times rather than asserting on an internal.
    """
    draft = qd.make_draft("ARCAAI-PROMPT-900", "no target header here", draft_id="dA")
    driver, _transport, notifier = _driver(tmp_path, [draft])

    for _ in range(3):
        driver.poll_inbound(qd.CycleReport())

    pages = [p for p in notifier.pages if "REFUSED" in p[0]]
    assert len(pages) == 1, (
        f"expected exactly one REFUSED page across three polls, got {len(pages)}"
    )


def test_refusal_without_the_relabel_would_re_page(tmp_path):
    """Discriminator: proves the assertion above is caused by the relabel.

    Without this, ``test_refused_draft_stops_re_paging`` could pass for an
    unrelated reason — a dedup elsewhere, or the fake simply not returning the
    draft twice — and a future change removing the relabel would not fail it.
    Here the terminal relabel is neutered and the defect must reappear.
    """
    draft = qd.make_draft("ARCAAI-PROMPT-900", "no target header here", draft_id="dA")
    driver, transport, notifier = _driver(tmp_path, [draft])
    transport.relabel_refused = lambda record: None  # type: ignore[method-assign]

    for _ in range(3):
        driver.poll_inbound(qd.CycleReport())

    pages = [p for p in notifier.pages if "REFUSED" in p[0]]
    assert len(pages) == 3, (
        "with the relabel neutered the item must re-page every poll; if it does not, "
        "the passing test above is not evidence for the relabel"
    )


def test_dead_letter_preserves_bytes_and_is_hashable_without_the_sidecar(tmp_path):
    """Rulings 2 and 6. The envelope file is bytes and nothing else."""
    draft = qd.make_draft("ARCAAI-PROMPT-900", ENVELOPE_BODY, draft_id="dA")
    expected = qd.extract_plain_body(draft.raw)
    driver, _transport, _notifier = _driver(tmp_path, [draft])

    # Refuse on an unroutable lane: the body parses, so the lane is known.
    driver.refuse(draft, "synthetic refusal for test", qd.CycleReport())

    dead_dir = driver.config.dead("T2")
    envelopes = sorted(p for p in dead_dir.glob("*.md"))
    sidecars = sorted(p for p in dead_dir.glob("*.sidecar.json"))
    assert len(envelopes) == 1 and len(sidecars) == 1

    landed = envelopes[0].read_bytes()
    assert landed == expected, "dead-lettered bytes must be the bytes received"
    # Hashable WITHOUT parsing anything — the whole point of ruling 2's sidecar.
    assert qd.sha256_hex(landed) == qd.sha256_hex(expected)

    sidecar = json.loads(sidecars[0].read_text(encoding="utf-8"))
    assert sidecar["schema"] == qd.SIDECAR_SCHEMA
    assert sidecar["content_sha256"] == qd.sha256_hex(expected)
    assert sidecar["refusal_reason"] == "synthetic refusal for test"
    assert sidecar["origin"]["kind"] == "gmail-draft"
    assert sidecar["origin"]["draft_id"] == "dA"


def test_dead_letter_records_origin_for_an_unparseable_subject(tmp_path):
    """A refusal can precede any lane being known; the record must not invent one."""
    draft = qd.make_draft("NOT-AN-ARCAAI-SUBJECT", "nothing useful", draft_id="dZ")
    driver, _transport, _notifier = _driver(tmp_path, [draft])

    driver.refuse(draft, "malformed subject", qd.CycleReport())

    lane_dir = driver.config.dead("T2")
    root_dir = driver.config.dead(None)
    assert not lane_dir.exists(), "an unattributable refusal must not be filed under a lane"
    envelopes = sorted(root_dir.glob("*.md"))
    assert len(envelopes) == 1
    assert envelopes[0].name.startswith("UNPARSED-dZ")

    sidecar = json.loads(next(root_dir.glob("*.sidecar.json")).read_text(encoding="utf-8"))
    assert sidecar["lane"] is None and sidecar["prompt_id"] is None
    assert sidecar["origin"]["intended_path"] is None


def test_dead_letter_never_overwrites_existing_evidence(tmp_path):
    """The driver refuses on doubt rather than clobbering a prior record."""
    draft = qd.make_draft("ARCAAI-PROMPT-900", ENVELOPE_BODY, draft_id="dA")
    driver, _transport, _notifier = _driver(tmp_path, [draft])

    first = driver._dead_letter(draft, "first refusal")
    existing = Path(first["envelope_path"])
    before = existing.read_bytes()

    # Force the collision the timestamp normally prevents.
    driver_utc = qd.utc_now_iso
    try:
        qd.utc_now_iso = lambda: "2026-08-22T10:00:00Z"  # type: ignore[assignment]
        second = driver._dead_letter(draft, "second refusal")
        colliding = Path(second["envelope_path"])
        with pytest.raises(qd.QueueDriverError, match="never deletes or overwrites"):
            driver._dead_letter(draft, "third refusal")
        assert colliding.exists()
    finally:
        qd.utc_now_iso = driver_utc  # type: ignore[assignment]

    assert existing.read_bytes() == before, "the first record must be untouched"


def test_dead_letter_paths_are_bounded_by_the_queue_guard(tmp_path):
    """The `dead` dirs fall inside the queue root, so the existing guard suffices."""
    driver, _transport, _notifier = _driver(tmp_path)
    for path in (driver.config.dead("T2"), driver.config.dead(None)):
        assert driver._assert_within_queue(path) == Path(str(path)).absolute()


# --------------------------------------------------------------------------
# Mechanism (b) — processed archive (rulings 4, 5, 6)
# --------------------------------------------------------------------------


def _write_outcome(
    config, lane_id: str, name: str, status: str = "BLOCKED-RULING", body: str = "body"
) -> Path:
    """Write an outcome file the driver will actually parse.

    ``STATUS:`` must be on LINE 1 — ``parse_outcome_status`` reads no further and
    treats anything else as ERROR with a note. An earlier version of this helper
    put a markdown heading first, so every outcome parsed as ERROR and a test
    filtering for BLOCKED-RULING saw zero pages. The fixture was wrong and the
    driver was right, which is worth a comment because the failure looked like a
    paging defect.
    """
    outbox = config.outbox(lane_id)
    outbox.mkdir(parents=True, exist_ok=True)
    path = outbox / name
    path.write_text(f"STATUS: {status}\n\n{body}\n", encoding="utf-8")
    return path


def test_swept_outcome_is_archived_with_hash_preserved_and_origin_recorded(tmp_path):
    """Rulings 4, 5, 6. The move is a rename with both ruling-6 conditions met."""
    driver, _transport, _notifier = _driver(tmp_path)
    path = _write_outcome(driver.config, "T2", "PROMPT-900.outcome.md")
    original = path.read_bytes()
    original_hash = qd.sha256_hex(original)

    driver.sweep_outboxes(qd.CycleReport())

    assert not path.exists(), "the outcome must leave the outbox"
    archived = driver.config.done("T2") / "PROMPT-900.outcome.md"
    assert archived.exists(), "the outcome must arrive in done/"
    assert archived.read_bytes() == original, "bytes must survive the move"
    assert qd.sha256_hex(archived.read_bytes()) == original_hash

    sidecar = json.loads(
        (driver.config.done("T2") / "PROMPT-900.outcome.md.sidecar.json").read_text(
            encoding="utf-8"
        )
    )
    assert sidecar["schema"] == qd.ARCHIVE_SCHEMA
    assert sidecar["content_sha256"] == original_hash
    assert sidecar["origin_path"] == str(path), "ruling 6 requires the origin recorded"


def test_archived_outcome_does_not_re_alert(tmp_path):
    driver, _transport, notifier = _driver(tmp_path)
    _write_outcome(driver.config, "T2", "PROMPT-900.outcome.md")

    for _ in range(3):
        driver.sweep_outboxes(qd.CycleReport())

    pages = [p for p in notifier.pages if "BLOCKED-RULING" in p[0]]
    assert len(pages) == 1, f"expected one alert across three sweeps, got {len(pages)}"


def test_archive_survives_loss_of_the_driver_log(tmp_path):
    """The discriminator that justifies the archive over the log's own dedup.

    ``swept_outcomes`` already dedups by path, so a re-alert test alone passes
    with or without an archive. The archive earns its place only if it holds when
    the log does not — so here the log is destroyed and a FRESH driver sweeps the
    same queue root. State ABOUT the file is gone; state OF the file remains.
    """
    driver, _transport, _notifier = _driver(tmp_path)
    _write_outcome(driver.config, "T2", "PROMPT-900.outcome.md")
    driver.sweep_outboxes(qd.CycleReport())

    log_path = driver.config.log_path
    assert log_path.exists()
    log_path.unlink()  # simulate log loss/rotation — the driver itself never deletes

    fresh = qd.QueueDriver(driver.config, qd.FakeTransport([]), qd.RecordingNotifier())
    fresh.sweep_outboxes(qd.CycleReport())

    pages = [p for p in fresh.notifier.pages if "BLOCKED-RULING" in p[0]]
    assert pages == [], (
        "with the log gone the archive must still prevent the re-alert; if it does not, "
        "the mechanism is the log dedup and not the archive"
    )


def test_archive_never_overwrites_a_prior_archived_outcome(tmp_path):
    """Two outcomes of the same name both survive; the driver deletes nothing.

    Driven at the ``_archive_outcome`` level deliberately. The sweep cannot reach
    this branch, because its own dedup is keyed on the OUTBOX PATH, so a second
    file at the same path is skipped before any archiving is attempted — see
    ``test_sweep_dedup_is_keyed_on_path_which_hides_a_regenerated_outcome``.
    Testing it through the sweep would therefore assert nothing about the guard.
    """
    driver, _transport, _notifier = _driver(tmp_path)
    first_src = _write_outcome(driver.config, "T2", "PROMPT-900.outcome.md", body="one")
    first_hash = qd.sha256_hex(first_src.read_bytes())
    driver._archive_outcome(first_src, "T2", first_hash)

    first = driver.config.done("T2") / "PROMPT-900.outcome.md"
    first_bytes = first.read_bytes()

    second_src = _write_outcome(driver.config, "T2", "PROMPT-900.outcome.md", body="two")
    second_hash = qd.sha256_hex(second_src.read_bytes())
    assert second_hash != first_hash
    driver._archive_outcome(second_src, "T2", second_hash)

    assert first.read_bytes() == first_bytes, "the earlier archive must be untouched"
    archived = sorted(p for p in driver.config.done("T2").glob("PROMPT-900*.md"))
    assert len(archived) == 2, "both versions must survive; the driver deletes nothing"
    assert {qd.sha256_hex(p.read_bytes()) for p in archived} == {first_hash, second_hash}


def test_sweep_dedup_is_keyed_on_path_which_hides_a_regenerated_outcome(tmp_path):
    """Pre-existing behaviour, recorded rather than changed — and NOT introduced here.

    ``sweep_outboxes`` skips any outcome whose OUTBOX PATH already appears in the
    log. After QD-F2 the first file is moved to ``done``, so a genuinely new
    outcome written to the same path afterwards sits in the outbox and is never
    swept, because the path key still matches.

    This is unchanged by QD-F2 — the same key hid the same case before the
    archive existed — and fixing it is neither in the rulings nor in this
    envelope's grant. It is asserted here so the behaviour is a recorded fact
    rather than a surprise, and so that whoever changes the dedup key finds a
    test describing what today's key actually does.
    """
    driver, _transport, notifier = _driver(tmp_path)
    _write_outcome(driver.config, "T2", "PROMPT-900.outcome.md", body="first")
    driver.sweep_outboxes(qd.CycleReport())
    assert (driver.config.done("T2") / "PROMPT-900.outcome.md").exists()

    regenerated = _write_outcome(driver.config, "T2", "PROMPT-900.outcome.md", body="second")
    pages_before = len(notifier.pages)
    driver.sweep_outboxes(qd.CycleReport())

    assert regenerated.exists(), "the regenerated outcome is left in the outbox"
    assert len(notifier.pages) == pages_before, "and it raises no alert"


def test_done_paths_are_bounded_by_the_queue_guard(tmp_path):
    driver, _transport, _notifier = _driver(tmp_path)
    path = driver.config.done("T2")
    assert driver._assert_within_queue(path) == Path(str(path)).absolute()


# --------------------------------------------------------------------------
# Both mechanisms — the DEC-0019 property ruling 6 interprets
# --------------------------------------------------------------------------


def test_no_bytes_leave_the_queue_root_across_either_mechanism(tmp_path):
    """Ruling 6's own definition: deletes-nothing means no bytes leave the root.

    Counted rather than argued. Every byte present before the two mechanisms run
    must still be findable inside the queue root afterwards, at the same hash.
    """
    draft = qd.make_draft("ARCAAI-PROMPT-900", ENVELOPE_BODY, draft_id="dA")
    driver, _transport, _notifier = _driver(tmp_path, [draft])
    outcome = _write_outcome(driver.config, "T2", "PROMPT-901.outcome.md")
    outcome_hash = qd.sha256_hex(outcome.read_bytes())

    driver.poll_inbound(qd.CycleReport())
    driver.sweep_outboxes(qd.CycleReport())

    root = driver.config.queue_root
    hashes = {qd.sha256_hex(p.read_bytes()) for p in _all_files(root)}
    assert outcome_hash in hashes, "the swept outcome's bytes must still be in the queue root"
    assert qd.sha256_hex(qd.extract_plain_body(draft.raw)) in hashes, (
        "the refused envelope's bytes must still be in the queue root"
    )
