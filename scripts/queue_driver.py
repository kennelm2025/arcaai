#!/usr/bin/env python3
"""ARCAAI queue driver — Gmail <-> ``_queue`` transport for envelope execution.

Built under PROMPT 129/129R (harness-build class) against the consolidated
requirement set carried in the envelope, which supersedes the 20 Aug spec
Section 6 by amendment B7. Authority: DEC-0019 B1-B7 as adopted 21 Aug 2026;
DEC-0018 as ratified with A1-A11 governs the envelope's form.

WHAT THIS IS. The chair writes numbered prompts as Gmail drafts and releases
them by label. This driver moves a released draft into the addressed lane's
inbox as ``_queue/T{n}/inbox/PROMPT-NNN.md``, relabels the draft consumed, and
sweeps each lane's outbox back into one consolidated reply draft per
session-day. It is the transport, and only the transport.

THREE PROPERTIES THAT ARE STRUCTURAL RATHER THAN INTENDED, because a transport
that can reach the working trees is not a transport:

1. **It never runs git and never imports subprocess.** Requirement 6 forbids
   touching the working trees; requirement 3 nonetheless obliges a worktree
   assertion. Those are reconciled by establishing worktree identity from the
   filesystem alone: a linked git worktree carries ``.git`` as a FILE holding a
   ``gitdir:`` pointer, where a main tree carries ``.git`` as a DIRECTORY. That
   is a pure read. It touches no index, acquires no lock, and cannot mutate the
   tree it is asserting about. ``tests/harness/test_queue_driver.py`` asserts
   the absence of the ``subprocess`` import, so the property is checked rather
   than promised.

2. **Every write is inside the queue root**, enforced by
   ``_assert_within_queue`` on the path immediately before the write rather
   than by review of the call sites.

3. **It deletes nothing, ever** — no file, no draft. The only removal it
   performs is of the RELEASED label at relabel time, which is what "relabel"
   means and is required by requirement 2. Consumed drafts remain in Gmail.

TRANSFORMATIONS ARE A CLOSED SET, AND EACH ONE IS LOGGED. Requirement 2 says
byte-for-byte; requirements 2 and 5 then name two exceptions. Only those two
are applied, because a transport that silently improves its payload is not
byte-faithful, and the divergence would surface as a hash mismatch months later:

  (a) **BOM strip** (requirement 5). The chair's hand-staged prompts observed
      on 2026-08-21 are UTF-8 *with* BOM, so the driver deliberately diverges
      from current hand practice here, on the ruled requirement.
  (b) **Gmail URL-rewriting of bare paths** (requirement 2), unwrapped only in
      the two forms reversible without guessing: the ``google.com/url?q=``
      redirect wrapper, and angle-bracket wrapping of a bare URL.

Line endings are NOT normalised. Nothing rules on them, the raw draft body
arrives CRLF, and the chair's hand-staged files are CRLF, so preserving them is
both byte-faithful and consistent with observed practice. Inventing a third
transformation would be the driver making policy.

HASHES ARE COMPUTED ON RAW BYTES (B2) and verification is a read-back: the file
is written, re-read from disk, and its bytes hashed against the hash of what
was meant to land. A write that reports success while landing different bytes
is the failure this closes, and it is checkable only by reading what the
filesystem actually holds.

REFUSAL IS THE DEFAULT ON DOUBT. A malformed envelope, an unknown lane, a
TARGET disagreeing with the dispatch order, an unisolated lane, and an existing
inbox file whose bytes differ from what would be written are all REFUSALS: an
ERROR page, a log row, and no route. None is retried, because none is transient.

DISPATCH ORDER, AND A STATED LIMIT. Requirement 2 refuses on "lane/TARGET
mismatch against the dispatch order (A2)". A2's ratified text is not in this
repository — the queue item 34 M2 gap, flagged at the PROMPT 129 halt and still
open. What IS in the repository is the dispatch order's substance at
``docs/governance/DEC-0018_CANDIDATE_2026-08-17.md`` Part II, which binds
envelope ids to terminals. The operational reading implemented here is stated
so the chair can correct it rather than discover it:

  * TARGET must name a lane present in the driver config;
  * a base prompt number binds to the lane it first routed to, so a revision
    (``129R``, ``129R2``) addressed to a different lane is a mismatch;
  * an explicit ``dispatch_order`` map in config, where present, overrides both.

Usage::

    python scripts/queue_driver.py --selftest       # hermetic dry run, no Gmail
    python scripts/queue_driver.py --assert-lanes   # B1 assertion, then exit
    python scripts/queue_driver.py --once           # one live poll cycle
    python scripts/queue_driver.py                  # poll loop, 60s default

Exit status: 0 when the cycle completed with no refusal and no error, non-zero
otherwise. A refusal exits non-zero even though the driver handled it
correctly, because a cycle that refused a prompt is not a cycle that ran clean.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import dataclasses
import datetime as dt
import email
import email.policy
import hashlib
import json
import os
import re
import sys
import tempfile
import time
import urllib.parse
from dataclasses import dataclass, field
from email.message import EmailMessage
from pathlib import Path
from typing import Any, Callable

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

LABEL_RELEASED = "ARCAAI/RELEASED"
LABEL_CONSUMED = "ARCAAI/CONSUMED"
# QD-F2 mechanism (a), ruling 1 of the 22 Aug post-156 sheet. The terminal label
# for a REFUSED draft. It exists so the refusal path has the terminal state the
# success path already had: list_released_drafts queries label:RELEASED, so
# moving a refused draft off that label is what stops the next poll selecting it,
# re-refusing it and paging again. This adds no new CLASS of act -- relabel is
# the same act the consumed path performs, and DEC-0019's deletes-nothing
# property is untouched because a relabel removes no bytes.
LABEL_REFUSED = "ARCAAI/REFUSED"

SUBJECT_RE = re.compile(r"^ARCAAI-PROMPT-(\d{1,4})(R\d*)?$")
BODY_PROMPT_RE = re.compile(r"^\s*PROMPT\s+(\d{1,4})(R\d*)?\b")
TARGET_RE = re.compile(r"\bTARGET:\s*(T\d+)\b")
LANE_RE = re.compile(r"^T\d+$")
STATUS_RE = re.compile(r"^\s*STATUS:\s*([A-Z][A-Z-]*)\s*$")

COMPLETE = "COMPLETE"
BLOCKED_RULING = "BLOCKED-RULING"
RETRYING = "RETRYING"
ERROR = "ERROR"
STATUS_VOCABULARY = (COMPLETE, BLOCKED_RULING, RETRYING, ERROR)
# ntfy policy B6: these two page the chair. The other two deliberately do not.
PAGING_STATUSES = frozenset({BLOCKED_RULING, ERROR})

BOM = b"\xef\xbb\xbf"

DEFAULT_POLL_SECONDS = 60
DEFAULT_RETRIES = 3
DEFAULT_BACKOFF_BASE = 2.0

GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

# Closed log-action vocabulary, so the log can be counted and not merely read.
ACT_START = "START"
ACT_LANE_ASSERT = "LANE-ASSERT"
ACT_ROUTED = "ROUTED"
ACT_REFUSED = "REFUSED"
ACT_SWEPT = "SWEPT"
ACT_OUTCOMES_DRAFT = "OUTCOMES-DRAFT"
ACT_PAGED = "PAGED"
ACT_PAGE_FAILED = "PAGE-FAILED"
ACT_RETRY = "RETRY"
# QD-F2. Two new terminal-state actions, kept distinct in the vocabulary because
# the two mechanisms are separate and ruling 7 requires them separately
# evidenced: a log that collapsed them would make that evidence uncountable.
ACT_DEAD_LETTERED = "DEAD-LETTERED"
ACT_ARCHIVED = "ARCHIVED"

# QD-F2 sidecar schema id. Versioned because the sidecar is an evidence artefact
# a later reader must be able to parse without guessing which fields existed.
SIDECAR_SCHEMA = "arcaai.queue.dead-letter/v1"
ARCHIVE_SCHEMA = "arcaai.queue.archive/v1"


class QueueDriverError(RuntimeError):
    """A condition the driver refuses to route through. Never retried."""


class TransientError(RuntimeError):
    """A harness-level failure of the driver's own Gmail/network calls.

    Distinguished from :class:`QueueDriverError` because only this class is
    retried. A malformed envelope retried three times is still malformed, and
    the backoff would only postpone the page.
    """


# --------------------------------------------------------------------------
# Pure helpers — no I/O, individually testable
# --------------------------------------------------------------------------


def sha256_hex(data: bytes) -> str:
    """SHA256 over raw bytes (B2). Never over a decoded string."""
    return hashlib.sha256(data).hexdigest()


def utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def session_day(now: dt.datetime | None = None) -> str:
    """Session-day stamp, local date, ``YYYYMMDD``."""
    moment = now if now is not None else dt.datetime.now()
    return moment.strftime("%Y%m%d")


def strip_bom(data: bytes) -> tuple[bytes, list[str]]:
    """Remove a leading UTF-8 BOM. Requirement 5: driver-written files carry none."""
    if data.startswith(BOM):
        return data[len(BOM):], ["stripped UTF-8 BOM from draft body"]
    return data, []


def normalise_gmail_rewrites(data: bytes) -> tuple[bytes, list[str]]:
    """Undo Gmail's URL rewriting of bare paths, and say when it did.

    Only two forms are unwrapped, both reversible without guessing. Gmail's
    other manglings are NOT guessed at: an unwrap that has to infer the
    original would corrupt the byte-for-byte guarantee it exists to protect.
    """
    notes: list[str] = []

    def _unwrap_redirect(match: re.Match[bytes]) -> bytes:
        target = match.group(1).decode("ascii", "replace")
        return urllib.parse.unquote(target).encode("utf-8", "replace")

    redirect_re = re.compile(rb"https?://www\.google\.com/url\?q=([^\s&<>\"]+)[^\s<>\"]*")
    data, count = redirect_re.subn(_unwrap_redirect, data)
    if count:
        notes.append(f"unwrapped {count} google.com/url redirect wrapper(s)")

    angle_re = re.compile(rb"<((?:https?|file)://[^>\s]+)>")
    data, count = angle_re.subn(rb"\1", data)
    if count:
        notes.append(f"unwrapped {count} angle-bracket-wrapped URL(s)")

    return data, notes


def normalise_body(raw: bytes) -> tuple[bytes, list[str]]:
    """Apply the closed set of ruled transformations, returning notes for the log."""
    data, notes = strip_bom(raw)
    data, more = normalise_gmail_rewrites(data)
    return data, notes + more


def parse_subject(subject: str) -> tuple[str, str, str]:
    """Parse ``ARCAAI-PROMPT-NNN`` into (prompt_id, base_number, revision).

    Revision suffixes are first-class because the live queue carries them —
    ``127R3``, ``128R2``, ``129R`` — and because the lane-binding rule needs the
    base number to detect a revision addressed to the wrong lane.
    """
    match = SUBJECT_RE.match((subject or "").strip())
    if not match:
        raise QueueDriverError(
            f"malformed envelope: subject {subject!r} does not match ARCAAI-PROMPT-NNN"
        )
    base, revision = match.group(1), (match.group(2) or "")
    return f"{base}{revision}", base, revision


def parse_target(body_text: str, header_lines: int = 10) -> str:
    """Read TARGET from the envelope header block at the top of the body.

    Restricted to the header block on purpose: prompt bodies discuss other
    lanes in prose — PROMPT 129 names T1 in its dispatch discussion — and a
    whole-body scan would route on a mention. Two distinct TARGET values in the
    header are malformed rather than resolved by precedence.
    """
    head = "\n".join((body_text or "").splitlines()[:header_lines])
    found = TARGET_RE.findall(head)
    if not found:
        raise QueueDriverError(
            f"malformed envelope: no TARGET in the first {header_lines} lines of the body"
        )
    distinct = sorted(set(found))
    if len(distinct) > 1:
        raise QueueDriverError(
            f"malformed envelope: conflicting TARGET values in header: {distinct}"
        )
    target = distinct[0]
    if not LANE_RE.match(target):
        raise QueueDriverError(f"malformed envelope: TARGET {target!r} is not a lane id")
    return target


def check_body_prompt_number(body_text: str, prompt_id: str) -> list[str]:
    """Cross-check the body's own prompt number against the subject's.

    The subject is the naming authority. A body that disagrees with it is
    malformed — that is a prompt pasted into the wrong draft, and routing it
    would file one prompt's text under another's name. A body carrying no
    prompt token is accepted and noted, since nothing rules that it must.
    """
    lines = (body_text or "").splitlines()
    match = BODY_PROMPT_RE.match(lines[0]) if lines else None
    if not match:
        return ["body carries no leading PROMPT token; subject taken as authority"]
    body_id = f"{match.group(1)}{match.group(2) or ''}"
    if body_id != prompt_id:
        raise QueueDriverError(
            f"malformed envelope: subject says PROMPT {prompt_id}, body says PROMPT {body_id}"
        )
    return []


def parse_outcome_status(data: bytes) -> tuple[str, list[str]]:
    """Read ``STATUS:`` from line 1 of an outcome file.

    An unrecognised token is reported as ERROR rather than passed through. A
    status the vocabulary does not contain cannot be judged pageable or not,
    and treating the unjudgeable as non-pageable is how a blocked lane goes
    unnoticed.
    """
    text = data.decode("utf-8", "replace")
    lines = text.splitlines()
    match = STATUS_RE.match(lines[0]) if lines else None
    if not match:
        return ERROR, ["outcome file has no STATUS: on line 1; treated as ERROR"]
    token = match.group(1)
    if token not in STATUS_VOCABULARY:
        return ERROR, [f"outcome STATUS {token!r} outside vocabulary; treated as ERROR"]
    return token, []


def extract_plain_body(raw_message: bytes) -> bytes:
    """Return the text/plain payload of an RFC822 message as raw bytes."""
    message = email.message_from_bytes(raw_message, policy=email.policy.default)
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload is not None:
                    return payload
        raise QueueDriverError("malformed envelope: multipart draft has no text/plain part")
    payload = message.get_payload(decode=True)
    if payload is None:
        raise QueueDriverError("malformed envelope: draft body is empty")
    return payload


# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Lane:
    lane_id: str
    worktree: Path
    enabled: bool = True


@dataclass(frozen=True)
class Config:
    queue_root: Path
    lanes: dict[str, Lane]
    poll_interval_seconds: int = DEFAULT_POLL_SECONDS
    ntfy_server: str = "https://ntfy.sh"
    ntfy_topic: str = ""
    credentials_path: Path = Path("credentials.json")
    token_path: Path = Path("token.json")
    retries: int = DEFAULT_RETRIES
    backoff_base: float = DEFAULT_BACKOFF_BASE
    dispatch_order: dict[str, str] = field(default_factory=dict)

    @property
    def log_path(self) -> Path:
        return self.queue_root / "driver.log"

    def inbox(self, lane_id: str) -> Path:
        return self.queue_root / lane_id / "inbox"

    def outbox(self, lane_id: str) -> Path:
        return self.queue_root / lane_id / "outbox"

    def dead(self, lane_id: str | None) -> Path:
        """Terminal location for a refused envelope (QD-F2 (a); rulings 3, 6).

        ``lane_id`` is optional because a refusal can occur BEFORE the lane is
        known -- a malformed subject or an unparseable TARGET is refused with no
        lane to attribute it to. Filing such an item under a lane would be a
        fabrication, so it goes to a queue-root-level ``dead`` instead. Both
        forms sit inside the queue root and are therefore bounded by
        ``_assert_within_queue`` without that guard changing.
        """
        if lane_id is None:
            return self.queue_root / "dead"
        return self.queue_root / lane_id / "dead"

    def done(self, lane_id: str) -> Path:
        """Terminal location for a swept outcome file (QD-F2 (b); rulings 4, 5, 6)."""
        return self.queue_root / lane_id / "done"


def load_config(path: Path) -> Config:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise QueueDriverError(f"config not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise QueueDriverError(f"config is not valid JSON: {path}: {exc}") from exc

    lanes_raw = data.get("lanes") or {}
    if not lanes_raw:
        raise QueueDriverError("config declares no lanes; refusing to start")
    lanes = {
        lane_id: Lane(
            lane_id=lane_id,
            worktree=Path(spec["worktree"]),
            enabled=bool(spec.get("enabled", True)),
        )
        for lane_id, spec in lanes_raw.items()
    }
    base = path.parent

    def _resolve(value: str) -> Path:
        candidate = Path(value)
        return candidate if candidate.is_absolute() else (base / candidate)

    return Config(
        queue_root=Path(data["queue_root"]),
        lanes=lanes,
        poll_interval_seconds=int(data.get("poll_interval_seconds", DEFAULT_POLL_SECONDS)),
        ntfy_server=data.get("ntfy_server", "https://ntfy.sh"),
        ntfy_topic=os.environ.get("ARCAAI_NTFY_TOPIC", data.get("ntfy_topic", "")),
        credentials_path=_resolve(data.get("credentials_path", "credentials.json")),
        token_path=_resolve(data.get("token_path", "token.json")),
        retries=int(data.get("retries", DEFAULT_RETRIES)),
        backoff_base=float(data.get("backoff_base", DEFAULT_BACKOFF_BASE)),
        dispatch_order=dict(data.get("dispatch_order") or {}),
    )


# --------------------------------------------------------------------------
# Lane isolation assertion (DEC-0019 B1)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class LaneAssertion:
    lane_id: str
    outcome: str  # GREEN | RED | UNKNOWN
    detail: str
    gitdir: str = ""

    @property
    def routable(self) -> bool:
        return self.outcome == "GREEN"


def assert_lane_isolation(lane: Lane) -> LaneAssertion:
    """Establish that a lane path is its own linked git worktree, by reading only.

    B1 verbatim: "Each terminal runs in its own git worktree. At session open,
    each lane asserts its worktree path; the driver refuses to route to a lane
    whose asserted path collides with another lane's."

    Three outcomes, never two. A path that cannot be read is UNKNOWN and
    refuses, because an unreadable lane is not an isolated one — it is a lane
    whose isolation was not established.
    """
    root = lane.worktree
    try:
        if not root.exists():
            return LaneAssertion(lane.lane_id, "RED", f"worktree path absent: {root}")
        if not root.is_dir():
            return LaneAssertion(lane.lane_id, "RED", f"worktree path is not a directory: {root}")
        marker = root / ".git"
        if not marker.exists():
            return LaneAssertion(
                lane.lane_id, "RED", f"{root} contains no .git entry; not a git worktree"
            )
        if marker.is_dir():
            return LaneAssertion(
                lane.lane_id,
                "RED",
                f"{root} carries .git as a DIRECTORY, which is a main tree and not a linked "
                "worktree; this lane is UNISOLATED (DEC-0019 B1)",
            )
        content = marker.read_text(encoding="utf-8").strip()
    except OSError as exc:
        return LaneAssertion(lane.lane_id, "UNKNOWN", f"could not read {root}: {exc}")

    if not content.startswith("gitdir:"):
        return LaneAssertion(
            lane.lane_id, "UNKNOWN", f"{marker} is a file but carries no gitdir: pointer"
        )
    gitdir = content.split(":", 1)[1].strip()
    return LaneAssertion(
        lane.lane_id, "GREEN", f"{root} is a linked git worktree (gitdir: {gitdir})", gitdir
    )


def assert_all_lanes(config: Config) -> dict[str, LaneAssertion]:
    """Assert every lane, then downgrade any lane colliding with another."""
    results = {lane_id: assert_lane_isolation(lane) for lane_id, lane in config.lanes.items()}

    by_path: dict[str, list[str]] = {}
    for lane_id, lane in config.lanes.items():
        key = str(lane.worktree).rstrip("\\/").lower()
        by_path.setdefault(key, []).append(lane_id)
    for key, lane_ids in by_path.items():
        if len(lane_ids) > 1:
            for lane_id in lane_ids:
                others = sorted(set(lane_ids) - {lane_id})
                results[lane_id] = LaneAssertion(
                    lane_id, "RED", f"worktree path collides with {others}: {key}"
                )

    by_gitdir: dict[str, list[str]] = {}
    for lane_id, result in results.items():
        if result.routable and result.gitdir:
            by_gitdir.setdefault(result.gitdir.rstrip("\\/").lower(), []).append(lane_id)
    for key, lane_ids in by_gitdir.items():
        if len(lane_ids) > 1:
            for lane_id in lane_ids:
                results[lane_id] = LaneAssertion(
                    lane_id, "RED", f"gitdir pointer collides with {sorted(lane_ids)}: {key}"
                )
    return results


# --------------------------------------------------------------------------
# Append-only routing log, which is also the idempotency ledger
# --------------------------------------------------------------------------


class RoutingLog:
    """Append-only JSON Lines log at ``_queue/driver.log``.

    One file, two jobs, deliberately. Requirement 6 wants a routing log;
    requirement 5 wants idempotency keyed on draft id + prompt number. Keeping
    those in separate files would create two records that can disagree about
    whether a prompt was routed, and the disagreement would be discovered by
    routing something twice. JSON Lines is used so the rows a human greps are
    the rows the driver counts.
    """

    def __init__(self, path: Path) -> None:
        self.path = path

    def append(self, **row: Any) -> dict[str, Any]:
        entry = {
            "timestamp": row.pop("timestamp", utc_now_iso()),
            "prompt_no": row.pop("prompt_no", None),
            "target": row.pop("target", None),
            "action": row.pop("action"),
            "draft_id": row.pop("draft_id", None),
            "content_hash": row.pop("content_hash", None),
        }
        entry.update(row)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(entry, ensure_ascii=False) + "\n"
        with open(self.path, "a", encoding="utf-8", newline="\n") as handle:
            handle.write(line)
        return entry

    def rows(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        out: list[dict[str, Any]] = []
        with open(self.path, encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    # A corrupt row is skipped for parsing but never rewritten:
                    # the log is append-only, including when it is malformed.
                    continue
        return out

    def routed_keys(self) -> set[str]:
        return {
            f"{row.get('draft_id')}:{row.get('prompt_no')}"
            for row in self.rows()
            if row.get("action") == ACT_ROUTED
        }

    def lane_bindings(self) -> dict[str, str]:
        """Base prompt number -> the lane it first routed to."""
        bindings: dict[str, str] = {}
        for row in self.rows():
            if row.get("action") != ACT_ROUTED:
                continue
            base = str(row.get("base_no") or "")
            target = row.get("target")
            if base and target and base not in bindings:
                bindings[base] = str(target)
        return bindings

    def swept_outcomes(self) -> dict[str, dict[str, Any]]:
        out: dict[str, dict[str, Any]] = {}
        for row in self.rows():
            if row.get("action") == ACT_SWEPT and row.get("outcome_path"):
                out[str(row["outcome_path"])] = row
        return out

    def outcomes_draft_id(self, day: str) -> str | None:
        found = None
        for row in self.rows():
            if row.get("action") == ACT_OUTCOMES_DRAFT and row.get("session_day") == day:
                found = row.get("draft_id") or found
        return found

    def last_thread_id(self) -> str | None:
        found = None
        for row in self.rows():
            if row.get("action") == ACT_ROUTED and row.get("thread_id"):
                found = str(row["thread_id"])
        return found


# --------------------------------------------------------------------------
# Notification (ntfy) and retry
# --------------------------------------------------------------------------


class Notifier:
    def page(self, title: str, message: str, priority: str = "high") -> bool:
        raise NotImplementedError


class NtfyNotifier(Notifier):
    def __init__(self, server: str, topic: str) -> None:
        self.server = server.rstrip("/")
        self.topic = topic

    def page(self, title: str, message: str, priority: str = "high") -> bool:
        import requests  # imported here so the offline dry run needs no network stack

        url = f"{self.server}/{self.topic}"
        # Header values must be latin-1 encodable; titles are ASCII by construction.
        headers = {
            "Title": title.encode("ascii", "replace").decode("ascii"),
            "Priority": priority,
            "Tags": "warning",
        }
        try:
            response = requests.post(
                url, data=message.encode("utf-8"), headers=headers, timeout=20
            )
        except Exception as exc:
            raise TransientError(f"ntfy POST {url} failed: {exc}") from exc
        if response.status_code >= 400:
            raise TransientError(f"ntfy POST {url} returned {response.status_code}")
        return True


class RecordingNotifier(Notifier):
    """Used by the dry run: proves the ntfy POLICY without sending anything."""

    def __init__(self) -> None:
        self.pages: list[tuple[str, str, str]] = []

    def page(self, title: str, message: str, priority: str = "high") -> bool:
        self.pages.append((title, message, priority))
        return True


def retry_with_backoff(
    operation: Callable[[], Any],
    *,
    retries: int = DEFAULT_RETRIES,
    base: float = DEFAULT_BACKOFF_BASE,
    on_retry: Callable[[int, Exception], None] | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> Any:
    """Retry ONLY transient harness-level failures, then let the caller page.

    Requirement 4 gives 3 retries with exponential backoff. Only
    :class:`TransientError` is retried: a malformed envelope retried three
    times is still malformed, and the delay would only postpone the page.
    """
    attempt = 0
    while True:
        try:
            return operation()
        except TransientError as exc:
            attempt += 1
            if attempt > retries:
                raise
            if on_retry is not None:
                on_retry(attempt, exc)
            sleep(base**attempt)


# --------------------------------------------------------------------------
# Transports
# --------------------------------------------------------------------------


@dataclass
class DraftRecord:
    draft_id: str
    message_id: str
    thread_id: str
    subject: str
    raw: bytes


class Transport:
    """The Gmail surface the driver depends on, narrowed to three operations."""

    def ensure_authorised(self) -> None:
        """Acquire authorisation ONCE, outside every retried call path.

        The lazy-auth boundary. Authorisation is the one operation that can
        require a human, so it must happen where a human is expected to be:
        at start-up, once, before any retry loop begins. Everything after this
        point reuses the credential already held, and a transient network
        failure inside a retried call therefore cannot re-open a consent
        prompt. Source: the QD-F2 spec's defect register --
        "authorisation must move outside the retried call or any network flap
        re-prompts human consent."

        Implementations that need no credential may leave this a no-op; it is
        not optional for those that do.
        """
        return None

    def list_released_drafts(self) -> list[DraftRecord]:
        raise NotImplementedError

    def relabel_consumed(self, record: DraftRecord) -> None:
        raise NotImplementedError

    def relabel_refused(self, record: DraftRecord) -> None:
        """Terminal state for a refused draft (QD-F2 (a), ruling 1).

        Deliberately a separate operation from ``relabel_consumed`` rather than a
        parameter on it: a refused envelope and a consumed one are different
        outcomes, and a reader of the mailbox must be able to tell them apart
        without consulting the driver log.
        """
        raise NotImplementedError

    def upsert_outcomes_draft(
        self, subject: str, body: str, draft_id: str | None, thread_id: str | None
    ) -> str:
        raise NotImplementedError


class GmailTransport(Transport):
    """Real Gmail transport. Authorises lazily, on first use."""

    def __init__(self, credentials_path: Path, token_path: Path) -> None:
        self.credentials_path = credentials_path
        self.token_path = token_path
        self._service: Any = None
        self._labels: dict[str, str] = {}

    def ensure_authorised(self) -> None:
        """The ONE place interactive consent may happen. Called outside every retry.

        Idempotent: once the service is built it is reused for the life of the
        transport, so calling this again is free and acquires nothing.
        """
        if self._service is None:
            self._service = self._authorise(allow_interactive=True)

    def _authorise(self, allow_interactive: bool = False) -> Any:
        """Build the Gmail service, consenting only where consent is permitted.

        The ``allow_interactive`` default is FALSE, deliberately. The default is
        the safe side of the lazy-auth boundary: any caller that has not thought
        about it gets the non-interactive path and a loud refusal, rather than a
        consent prompt opened from somewhere a human may not be watching. Only
        :meth:`ensure_authorised` passes True, and it is called once at start-up.

        Refresh and consent sit on opposite sides of the line. A token refresh is
        non-interactive and may be retried; consent requires a human and may not.
        """
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build

        creds = None
        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(str(self.token_path), GMAIL_SCOPES)
        if creds is None or not creds.valid:
            if creds is not None and creds.expired and creds.refresh_token:
                # Non-interactive side of the boundary. A refresh that fails for
                # network reasons is transient and retryable; one that fails
                # because the grant is gone is not, and must not fall through to
                # the consent flow below -- that fall-through would turn a
                # revoked credential into a prompt in an unattended run.
                try:
                    creds.refresh(Request())
                except Exception as exc:
                    raise QueueDriverError(
                        f"token refresh failed for {self.token_path}: {exc}. Authorisation is "
                        "not re-attempted interactively from here; re-authorise deliberately."
                    ) from exc
            else:
                if not allow_interactive:
                    raise QueueDriverError(
                        "refusing to open an interactive OAuth consent flow outside start-up "
                        "authorisation: consent must be acquired by ensure_authorised(), once, "
                        "before any retried call. Reaching this point means the lazy-auth "
                        "boundary was crossed."
                    )
                if not self.credentials_path.exists():
                    raise QueueDriverError(
                        f"OAuth client secret not found at {self.credentials_path}. This is a "
                        "one-time operator act: create a Google Cloud OAuth client (Desktop "
                        "type), download the JSON, and place it there."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), GMAIL_SCOPES
                )
                creds = flow.run_local_server(port=0)
            self.token_path.write_text(creds.to_json(), encoding="utf-8")
        return build("gmail", "v1", credentials=creds, cache_discovery=False)

    @property
    def service(self) -> Any:
        """Reuse the held service. NEVER a consent point.

        This property is reached from inside retried calls, which is exactly why
        it must not authorise interactively: before the QD lazy-auth fix, a
        network flap on the first call re-entered here and could re-open the
        consent flow on every retry. It now takes the non-interactive path, so
        crossing the boundary produces a loud refusal instead of a prompt.
        """
        if self._service is None:
            self._service = self._authorise(allow_interactive=False)
        return self._service

    def _label_id(self, name: str) -> str:
        if not self._labels:
            listing = self.service.users().labels().list(userId="me").execute()
            self._labels = {item["name"]: item["id"] for item in listing.get("labels", [])}
        if name not in self._labels:
            raise QueueDriverError(
                f"Gmail label {name!r} does not exist. Create it before running the driver."
            )
        return self._labels[name]

    def list_released_drafts(self) -> list[DraftRecord]:
        try:
            listing = (
                self.service.users()
                .drafts()
                .list(userId="me", q=f"label:{LABEL_RELEASED}", maxResults=100)
                .execute()
            )
        except QueueDriverError:
            raise
        except Exception as exc:
            raise TransientError(f"drafts.list failed: {exc}") from exc

        records: list[DraftRecord] = []
        for stub in listing.get("drafts", []):
            try:
                draft = (
                    self.service.users()
                    .drafts()
                    .get(userId="me", id=stub["id"], format="raw")
                    .execute()
                )
            except Exception as exc:
                raise TransientError(f"drafts.get {stub['id']} failed: {exc}") from exc
            message = draft.get("message", {})
            try:
                raw = base64.urlsafe_b64decode(message.get("raw", "").encode("ascii"))
            except (binascii.Error, UnicodeEncodeError) as exc:
                raise QueueDriverError(
                    f"draft {stub['id']} raw payload undecodable: {exc}"
                ) from exc
            parsed = email.message_from_bytes(raw, policy=email.policy.default)
            records.append(
                DraftRecord(
                    draft_id=draft["id"],
                    message_id=message.get("id", ""),
                    thread_id=message.get("threadId", ""),
                    subject=str(parsed.get("Subject", "")),
                    raw=raw,
                )
            )
        return records

    def relabel_consumed(self, record: DraftRecord) -> None:
        self._relabel(record, LABEL_CONSUMED)

    def relabel_refused(self, record: DraftRecord) -> None:
        self._relabel(record, LABEL_REFUSED)

    def _relabel(self, record: DraftRecord, terminal_label: str) -> None:
        """Move a draft from RELEASED to a terminal label.

        Factored out when QD-F2 added the refusal terminal state, so that both
        outcomes travel the identical code path. Two near-copies would have been
        two places for the RELEASED removal to drift apart, and it is the removal
        -- not the addition -- that stops the next poll selecting the item.
        """
        body = {
            "addLabelIds": [self._label_id(terminal_label)],
            "removeLabelIds": [self._label_id(LABEL_RELEASED)],
        }
        try:
            self.service.users().messages().modify(
                userId="me", id=record.message_id, body=body
            ).execute()
        except QueueDriverError:
            raise
        except Exception as exc:
            raise TransientError(f"messages.modify {record.message_id} failed: {exc}") from exc

    def upsert_outcomes_draft(
        self, subject: str, body: str, draft_id: str | None, thread_id: str | None
    ) -> str:
        message = EmailMessage()
        message["Subject"] = subject
        message.set_content(body, charset="utf-8")
        encoded = base64.urlsafe_b64encode(message.as_bytes()).decode("ascii")
        payload: dict[str, Any] = {"message": {"raw": encoded}}
        if thread_id:
            payload["message"]["threadId"] = thread_id
        try:
            if draft_id:
                result = (
                    self.service.users()
                    .drafts()
                    .update(userId="me", id=draft_id, body=payload)
                    .execute()
                )
            else:
                result = (
                    self.service.users().drafts().create(userId="me", body=payload).execute()
                )
        except Exception as exc:
            raise TransientError(f"drafts upsert failed: {exc}") from exc
        return str(result["id"])


class FakeTransport(Transport):
    """In-memory transport for the dry run.

    The point of a fake rather than helper-level unit tests is that the dry run
    drives the SAME routing code the live driver runs, so the refusal paths and
    the hash verification are exercised rather than described.
    """

    def __init__(self, drafts: list[DraftRecord] | None = None) -> None:
        self.drafts = list(drafts or [])
        self.consumed: list[str] = []
        self.refused: list[str] = []
        self.outcome_drafts: dict[str, str] = {}
        self.fail_list_times = 0
        self._list_calls = 0
        self._counter = 0
        # Counted rather than inferred: the lazy-auth evidence at §2.2(a) is
        # "no second acquisition", and only a count can show that.
        self.auth_acquisitions = 0
        self.auth_fails_with: Exception | None = None

    def ensure_authorised(self) -> None:
        if self.auth_fails_with is not None:
            raise self.auth_fails_with
        self.auth_acquisitions += 1

    def list_released_drafts(self) -> list[DraftRecord]:
        self._list_calls += 1
        if self._list_calls <= self.fail_list_times:
            raise TransientError(f"synthetic transient failure #{self._list_calls}")
        # A refused draft is excluded exactly as a consumed one is. The real
        # transport achieves this by querying label:RELEASED, which a relabelled
        # draft no longer carries; the fake must model that or a test would show
        # the re-paging stopping when in production it would not.
        terminal = set(self.consumed) | set(self.refused)
        return [d for d in self.drafts if d.draft_id not in terminal]

    def relabel_consumed(self, record: DraftRecord) -> None:
        self.consumed.append(record.draft_id)

    def relabel_refused(self, record: DraftRecord) -> None:
        self.refused.append(record.draft_id)

    def upsert_outcomes_draft(
        self, subject: str, body: str, draft_id: str | None, thread_id: str | None
    ) -> str:
        if draft_id is None:
            self._counter += 1
            draft_id = f"fake-outcomes-{self._counter}"
        self.outcome_drafts[draft_id] = body
        return draft_id


def make_draft(
    subject: str, body: str, draft_id: str = "d1", thread_id: str = "t1"
) -> DraftRecord:
    """Build a DraftRecord carrying a real RFC822 message, for tests and dry runs."""
    message = EmailMessage()
    message["Subject"] = subject
    message["To"] = "arcaai@example.invalid"
    message.set_content(body, charset="utf-8")
    return DraftRecord(
        draft_id=draft_id,
        message_id=f"m-{draft_id}",
        thread_id=thread_id,
        subject=subject,
        raw=message.as_bytes(),
    )


# --------------------------------------------------------------------------
# The driver
# --------------------------------------------------------------------------


@dataclass
class CycleReport:
    routed: list[str] = field(default_factory=list)
    refused: list[str] = field(default_factory=list)
    swept: list[str] = field(default_factory=list)
    paged: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def clean(self) -> bool:
        return not self.refused and not self.errors


class QueueDriver:
    def __init__(
        self,
        config: Config,
        transport: Transport,
        notifier: Notifier,
        log: RoutingLog | None = None,
    ) -> None:
        self.config = config
        self.transport = transport
        self.notifier = notifier
        self.log = log or RoutingLog(config.log_path)
        self._lane_state: dict[str, LaneAssertion] = {}
        self._lane_asserted_day: str | None = None

    # -- guards ---------------------------------------------------------

    def _assert_within_queue(self, path: Path) -> Path:
        """Refuse any write outside the queue root, or inside a lane worktree."""
        root = Path(os.path.abspath(str(self.config.queue_root)))
        candidate = Path(os.path.abspath(str(path)))
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise QueueDriverError(
                f"refusing to write outside the queue root: {candidate} not under {root}"
            ) from exc
        for lane in self.config.lanes.values():
            worktree = Path(os.path.abspath(str(lane.worktree)))
            try:
                candidate.relative_to(worktree)
            except ValueError:
                continue
            raise QueueDriverError(
                f"refusing to write inside lane worktree {worktree}: {candidate}"
            )
        return candidate

    def _write_bytes(self, destination: Path, content: bytes) -> None:
        """The single byte-writing primitive, isolated so it can be corrupted on purpose.

        The B2 read-back verification below it is only evidence if something can
        make the write land bytes other than the ones asked for. Without this
        seam the verification passes whether or not it runs — a mutation probe
        on 2026-08-21 stubbed the comparison to always agree and the dry run
        stayed green, which is the check-method failure this repository tracks
        at queue item 8. The dry run now overrides this method to corrupt the
        write and requires the refusal.
        """
        with open(destination, "wb") as handle:
            handle.write(content)

    def ensure_lanes_asserted(self, force: bool = False) -> dict[str, LaneAssertion]:
        """Assert lane isolation at start, and before the first route of a session-day."""
        today = session_day()
        if force or self._lane_asserted_day != today or not self._lane_state:
            self._lane_state = assert_all_lanes(self.config)
            self._lane_asserted_day = today
            for lane_id in sorted(self._lane_state):
                result = self._lane_state[lane_id]
                self.log.append(
                    action=ACT_LANE_ASSERT,
                    target=lane_id,
                    outcome=result.outcome,
                    detail=result.detail,
                    session_day=today,
                )
        return self._lane_state

    # -- dispatch order -------------------------------------------------

    def check_dispatch_order(self, prompt_id: str, base_no: str, target: str) -> None:
        if target not in self.config.lanes:
            raise QueueDriverError(
                f"lane/TARGET mismatch: TARGET {target} is not a configured lane "
                f"({sorted(self.config.lanes)})"
            )
        if not self.config.lanes[target].enabled:
            raise QueueDriverError(f"lane/TARGET mismatch: lane {target} is disabled in config")

        declared = self.config.dispatch_order.get(prompt_id)
        if declared is None:
            declared = self.config.dispatch_order.get(base_no)
        if declared and declared != target:
            raise QueueDriverError(
                f"lane/TARGET mismatch: dispatch order assigns PROMPT {prompt_id} to "
                f"{declared}, envelope says {target}"
            )
        bound = self.log.lane_bindings().get(base_no)
        if bound and bound != target:
            raise QueueDriverError(
                f"lane/TARGET mismatch: PROMPT {base_no} is bound to lane {bound} by prior "
                f"routing, this envelope says {target}"
            )

    # -- inbound --------------------------------------------------------

    def route_draft(self, record: DraftRecord) -> str:
        """Route one released draft, or raise QueueDriverError to refuse it."""
        prompt_id, base_no, _revision = parse_subject(record.subject)
        body_raw = extract_plain_body(record.raw)
        body_text = body_raw.decode("utf-8", "replace")
        target = parse_target(body_text)
        notes = check_body_prompt_number(body_text, prompt_id)

        self.check_dispatch_order(prompt_id, base_no, target)

        lanes = self.ensure_lanes_asserted()
        assertion = lanes.get(target)
        if assertion is None or not assertion.routable:
            detail = assertion.detail if assertion else "lane not asserted"
            raise QueueDriverError(f"refusing to route to unisolated lane {target}: {detail}")

        content, transform_notes = normalise_body(body_raw)
        notes.extend(transform_notes)
        raw_hash = sha256_hex(body_raw)
        content_hash = sha256_hex(content)

        destination = self._assert_within_queue(
            self.config.inbox(target) / f"PROMPT-{prompt_id}.md"
        )

        if destination.exists():
            existing = destination.read_bytes()
            if sha256_hex(existing) == content_hash:
                # Idempotent: the bytes on disk are the bytes we would write.
                # Record and relabel, but do not rewrite.
                self.log.append(
                    action=ACT_ROUTED,
                    prompt_no=prompt_id,
                    base_no=base_no,
                    target=target,
                    draft_id=record.draft_id,
                    content_hash=content_hash,
                    raw_hash=raw_hash,
                    thread_id=record.thread_id,
                    path=str(destination),
                    notes=notes + ["already present with matching hash; not rewritten"],
                    verified=True,
                )
                self.transport.relabel_consumed(record)
                return prompt_id
            raise QueueDriverError(
                f"refusing to overwrite {destination}: a different PROMPT-{prompt_id}.md is "
                f"already present (on disk {sha256_hex(existing)[:16]}..., draft "
                f"{content_hash[:16]}...). The driver never deletes or overwrites."
            )

        destination.parent.mkdir(parents=True, exist_ok=True)
        self._write_bytes(destination, content)

        # B2 verification: read back from disk and hash what actually landed.
        landed_hash = sha256_hex(destination.read_bytes())
        if landed_hash != content_hash:
            raise QueueDriverError(
                f"content-hash verification FAILED for {destination}: expected {content_hash}, "
                f"file on disk hashes {landed_hash}"
            )

        self.log.append(
            action=ACT_ROUTED,
            prompt_no=prompt_id,
            base_no=base_no,
            target=target,
            draft_id=record.draft_id,
            content_hash=content_hash,
            raw_hash=raw_hash,
            thread_id=record.thread_id,
            path=str(destination),
            bytes=len(content),
            notes=notes,
            verified=True,
        )
        self.transport.relabel_consumed(record)
        return prompt_id

    def poll_inbound(self, report: CycleReport) -> None:
        drafts = retry_with_backoff(
            self.transport.list_released_drafts,
            retries=self.config.retries,
            base=self.config.backoff_base,
            on_retry=lambda n, exc: self.log.append(
                action=ACT_RETRY, detail=f"list_released_drafts attempt {n}: {exc}"
            ),
        )
        already = self.log.routed_keys()
        for record in drafts:
            key = ""
            try:
                prompt_id, _base, _rev = parse_subject(record.subject)
                key = f"{record.draft_id}:{prompt_id}"
            except QueueDriverError:
                key = ""
            if key and key in already:
                continue
            try:
                report.routed.append(self.route_draft(record))
            except QueueDriverError as exc:
                self.refuse(record, str(exc), report)
            except TransientError as exc:
                self.refuse(record, f"transient failure exhausted retries: {exc}", report)

    def _dead_letter(self, record: DraftRecord, reason: str) -> dict[str, Any]:
        """Write the refused envelope and its sidecar into the lane's ``dead`` dir.

        QD-F2 mechanism (a), rulings 2, 3, 6 and 12. Two files, deliberately:

        * the envelope, carrying the received body bytes and NOTHING else, so it
          stays independently hashable without parsing anything; and
        * a ``.sidecar.json`` carrying the hash, the origin, the refusal class
          and the timestamps.

        Ruling 2 chose this over a single file with a header block precisely
        because a header would have to be stripped before the preserved bytes
        could be hashed, and a hash that depends on a parser is a hash with a
        parser-shaped hole in it.

        Ruling 6's conditions are met in substance: the content hash is computed
        and recorded, and the origin is recorded. Note the origin here is a Gmail
        draft rather than a filesystem path -- at refusal time the envelope has
        not been written to any inbox, so there is nothing to rename. The
        envelope's summary calls this a "move"; for mechanism (a) it is a write
        of received bytes, which is what the design note's section 2.1 actually
        specifies. Recorded rather than silently reconciled.
        """
        lane_id: str | None = None
        prompt_id = ""
        try:
            prompt_id, _base, _rev = parse_subject(record.subject)
        except QueueDriverError:
            prompt_id = ""
        try:
            body_text = extract_plain_body(record.raw).decode("utf-8", "replace")
            candidate = parse_target(body_text)
            if candidate in self.config.lanes:
                lane_id = candidate
        except QueueDriverError:
            lane_id = None

        # The envelope bytes are the RAW received body: no BOM strip, no Gmail
        # unwrap. A dead-letter is evidence of what arrived, and normalising it
        # would destroy the very thing an investigator needs to see.
        try:
            envelope = extract_plain_body(record.raw)
        except QueueDriverError:
            envelope = record.raw
        content_hash = sha256_hex(envelope)
        stamp = utc_now_iso().replace(":", "").replace("-", "")
        slug = f"PROMPT-{prompt_id}" if prompt_id else f"UNPARSED-{record.draft_id}"
        base_name = f"{slug}.REFUSED-{stamp}"

        directory = self._assert_within_queue(self.config.dead(lane_id))
        directory.mkdir(parents=True, exist_ok=True)
        envelope_path = self._assert_within_queue(directory / f"{base_name}.md")
        sidecar_path = self._assert_within_queue(directory / f"{base_name}.sidecar.json")

        # Collision discipline, per the design note's "A collision case the design
        # must answer": the driver refuses on doubt rather than overwriting. The
        # timestamp makes a same-second second refusal the only way to collide,
        # and that case refuses rather than clobbering evidence.
        if envelope_path.exists() or sidecar_path.exists():
            raise QueueDriverError(
                f"refusing to overwrite an existing dead-letter record at {envelope_path}: "
                "the driver never deletes or overwrites"
            )

        self._write_bytes(envelope_path, envelope)
        landed = sha256_hex(envelope_path.read_bytes())
        if landed != content_hash:
            raise QueueDriverError(
                f"dead-letter content-hash verification FAILED for {envelope_path}: "
                f"expected {content_hash}, file on disk hashes {landed}"
            )

        sidecar = {
            "schema": SIDECAR_SCHEMA,
            "prompt_id": prompt_id or None,
            "subject": record.subject,
            "lane": lane_id,
            "refusal_reason": reason,
            "refused_at_utc": utc_now_iso(),
            "envelope_filename": envelope_path.name,
            "content_sha256": content_hash,
            "raw_message_sha256": sha256_hex(record.raw),
            "origin": {
                "kind": "gmail-draft",
                "draft_id": record.draft_id,
                "message_id": record.message_id,
                "thread_id": record.thread_id,
                "intended_path": (
                    str(self.config.inbox(lane_id) / f"PROMPT-{prompt_id}.md")
                    if lane_id and prompt_id
                    else None
                ),
            },
            "report": "ERROR page + driver.log row + this record (ruling 12)",
        }
        sidecar_bytes = json.dumps(sidecar, indent=2, sort_keys=True).encode("utf-8")
        self._write_bytes(sidecar_path, sidecar_bytes)

        return {
            "envelope_path": str(envelope_path),
            "sidecar_path": str(sidecar_path),
            "content_hash": content_hash,
            "lane": lane_id,
            "prompt_id": prompt_id,
        }

    def refuse(self, record: DraftRecord, reason: str, report: CycleReport) -> None:
        """Refuse a draft: dead-letter it, relabel it terminal, log, page. Never routed.

        QD-F2 changed the ORDER of business here, and the order is load-bearing.
        The dead-letter record is written FIRST, so that if the relabel fails the
        evidence already exists on disk; the item would then be re-refused on the
        next poll, which is the pre-QD-F2 behaviour and no worse. Relabelling
        first and failing the write would lose the evidence while silencing the
        alert -- the one ordering that trades a noisy defect for a quiet one.

        The refusal itself is still never retried, because none of the five
        refusal conditions is transient.
        """
        record_detail: dict[str, Any] = {}
        dead_letter_note = ""
        try:
            record_detail = self._dead_letter(record, reason)
            self.log.append(
                action=ACT_DEAD_LETTERED,
                prompt_no=record_detail.get("prompt_id") or (record.subject or "").strip(),
                target=record_detail.get("lane"),
                draft_id=record.draft_id,
                content_hash=record_detail.get("content_hash"),
                path=record_detail.get("envelope_path"),
                sidecar_path=record_detail.get("sidecar_path"),
            )
        except QueueDriverError as exc:
            # A dead-letter that cannot be written is itself reportable, and it
            # must not swallow the original refusal: the chair needs both the
            # reason the envelope was refused and the reason the evidence is
            # missing. Neither is allowed to mask the other.
            dead_letter_note = f" [dead-letter FAILED: {exc}]"
            self.log.append(
                action=ACT_DEAD_LETTERED,
                prompt_no=(record.subject or "").strip(),
                draft_id=record.draft_id,
                detail=f"dead-letter failed: {exc}",
                verified=False,
            )

        self.log.append(
            action=ACT_REFUSED,
            prompt_no=(record.subject or "").strip(),
            draft_id=record.draft_id,
            detail=reason,
            path=record_detail.get("envelope_path"),
        )
        report.refused.append(f"{record.subject}: {reason}{dead_letter_note}")

        # Ruling 1: the terminal relabel. This is the act that stops the next
        # poll selecting the draft, and therefore the act that closes the defect.
        relabel_note = ""
        try:
            self.transport.relabel_refused(record)
        except (QueueDriverError, TransientError) as exc:
            relabel_note = (
                f"\n\nWARNING: terminal relabel FAILED ({exc}). This item will be "
                "refused again on the next poll."
            )

        self.emit_page(
            ERROR,
            "ARCAAI queue driver: REFUSED",
            f"{record.subject or '(no subject)'}\n\n{reason}{dead_letter_note}{relabel_note}",
            report,
        )

    # -- outbound -------------------------------------------------------

    def _archive_outcome(self, path: Path, lane_id: str, content_hash: str) -> dict[str, Any]:
        """Move a swept outcome file into the lane's ``done`` dir.

        QD-F2 mechanism (b), rulings 4, 5 and 6. This is a genuine rename, which
        ruling 6 permits on two conditions, both met here: the content hash is
        computed before the move and re-verified from disk after it, and the
        origin path is recorded in the sidecar and in the log row.

        Why the archive rather than the log's existing ``swept_outcomes`` dedup:
        the log guard is state ABOUT the file, and it fails the moment the log is
        lost, rotated or replaced. The archive is state OF the file -- once the
        outcome is not in the outbox, no sweep can find it to re-alert on,
        whatever the log says. Ruling 4 chose the archive over a high-water mark;
        the log dedup survives underneath as a second line, not as the mechanism.
        """
        directory = self._assert_within_queue(self.config.done(lane_id))
        directory.mkdir(parents=True, exist_ok=True)

        destination = self._assert_within_queue(directory / path.name)
        if destination.exists():
            # Never clobber. A regenerated outcome of the same name is archived
            # beside its predecessor under a stamped name rather than replacing
            # it, because both are evidence and the driver deletes nothing.
            stamp = utc_now_iso().replace(":", "").replace("-", "")
            destination = self._assert_within_queue(
                directory / f"{path.stem}.{stamp}{path.suffix}"
            )
            if destination.exists():
                raise QueueDriverError(
                    f"refusing to overwrite an existing archived outcome at {destination}"
                )

        sidecar_path = self._assert_within_queue(
            destination.with_name(destination.name + ".sidecar.json")
        )
        origin = str(path)
        os.replace(str(path), str(destination))

        landed = sha256_hex(destination.read_bytes())
        if landed != content_hash:
            raise QueueDriverError(
                f"archive content-hash verification FAILED for {destination}: "
                f"expected {content_hash}, file on disk hashes {landed}"
            )

        sidecar = {
            "schema": ARCHIVE_SCHEMA,
            "lane": lane_id,
            "archived_at_utc": utc_now_iso(),
            "origin_path": origin,
            "archived_path": str(destination),
            "content_sha256": content_hash,
        }
        self._write_bytes(
            sidecar_path, json.dumps(sidecar, indent=2, sort_keys=True).encode("utf-8")
        )
        return {"archived_path": str(destination), "origin_path": origin}

    def sweep_outboxes(self, report: CycleReport) -> None:
        seen = self.log.swept_outcomes()
        day = session_day()
        fresh = 0

        for lane_id in sorted(self.config.lanes):
            outbox = self.config.outbox(lane_id)
            if not outbox.is_dir():
                continue
            for path in sorted(outbox.glob("*.outcome.md")):
                key = str(path)
                if key in seen:
                    continue
                data = path.read_bytes()
                status, notes = parse_outcome_status(data)
                content_hash = sha256_hex(data)
                self.log.append(
                    action=ACT_SWEPT,
                    prompt_no=path.name.replace(".outcome.md", ""),
                    target=lane_id,
                    content_hash=content_hash,
                    outcome_path=key,
                    status=status,
                    session_day=day,
                    notes=notes,
                )
                # QD-F2 (b): archive AFTER the swept row is durable. If the
                # archive fails, the sweep is still recorded and the outcome is
                # still in the outbox -- recoverable. The reverse order could
                # move the file and then fail to record where it went.
                try:
                    archived = self._archive_outcome(path, lane_id, content_hash)
                    self.log.append(
                        action=ACT_ARCHIVED,
                        prompt_no=path.name.replace(".outcome.md", ""),
                        target=lane_id,
                        content_hash=content_hash,
                        outcome_path=key,
                        path=archived["archived_path"],
                        session_day=day,
                    )
                except (QueueDriverError, OSError) as exc:
                    self.log.append(
                        action=ACT_ARCHIVED,
                        prompt_no=path.name.replace(".outcome.md", ""),
                        target=lane_id,
                        outcome_path=key,
                        detail=f"archive failed: {exc}",
                        verified=False,
                    )
                    report.refused.append(f"{lane_id}/{path.name}: archive failed: {exc}")
                fresh += 1
                report.swept.append(f"{lane_id}/{path.name} [{status}]")
                if status in PAGING_STATUSES:
                    self.emit_page(
                        status,
                        f"ARCAAI {lane_id}: {status}",
                        f"{path.name}\n\nStatus {status} swept from the {lane_id} outbox.",
                        report,
                    )

        if fresh:
            self.publish_outcomes_draft(day, report)

    def collect_day_outcomes(self, day: str) -> list[dict[str, Any]]:
        deduped: dict[str, dict[str, Any]] = {}
        for row in self.log.rows():
            if row.get("action") == ACT_SWEPT and row.get("session_day") == day:
                deduped[str(row.get("outcome_path"))] = row
        return [deduped[key] for key in sorted(deduped)]

    def render_outcomes_body(self, day: str) -> str:
        rows = self.collect_day_outcomes(day)
        lines = [
            f"ARCAAI OUTCOMES {day}",
            "",
            f"Consolidated by queue_driver.py at {utc_now_iso()}.",
            f"{len(rows)} outcome file(s) swept this session-day.",
            "",
        ]
        for row in rows:
            path = Path(str(row.get("outcome_path")))
            lines.append("=" * 70)
            lines.append(
                f"{row.get('prompt_no')}  [{row.get('status')}]  lane {row.get('target')}"
            )
            lines.append(f"path   : {path}")
            lines.append(f"sha256 : {row.get('content_hash')}")
            lines.append(f"swept  : {row.get('timestamp')}")
            lines.append("=" * 70)
            lines.append("")
            try:
                lines.append(path.read_text(encoding="utf-8", errors="replace"))
            except OSError as exc:
                lines.append(f"[outcome file unreadable at consolidation time: {exc}]")
            lines.append("")
        return "\n".join(lines)

    def publish_outcomes_draft(self, day: str, report: CycleReport) -> None:
        subject = f"ARCAAI-OUTCOMES-{day}"
        body = self.render_outcomes_body(day)
        existing = self.log.outcomes_draft_id(day)
        thread_id = self.log.last_thread_id()
        try:
            draft_id = retry_with_backoff(
                lambda: self.transport.upsert_outcomes_draft(subject, body, existing, thread_id),
                retries=self.config.retries,
                base=self.config.backoff_base,
                on_retry=lambda n, exc: self.log.append(
                    action=ACT_RETRY, detail=f"upsert_outcomes_draft attempt {n}: {exc}"
                ),
            )
        except TransientError as exc:
            report.errors.append(f"outcomes draft failed: {exc}")
            self.emit_page(
                ERROR, "ARCAAI queue driver: ERROR", f"outcomes draft failed: {exc}", report
            )
            return
        self.log.append(
            action=ACT_OUTCOMES_DRAFT,
            draft_id=draft_id,
            session_day=day,
            subject=subject,
            count=len(self.collect_day_outcomes(day)),
        )

    # -- paging ---------------------------------------------------------

    def emit_page(self, status: str, title: str, message: str, report: CycleReport) -> None:
        """Page only for BLOCKED-RULING and ERROR (B6). Never for the other two."""
        if status not in PAGING_STATUSES:
            return
        try:
            retry_with_backoff(
                lambda: self.notifier.page(title, message),
                retries=self.config.retries,
                base=self.config.backoff_base,
                on_retry=lambda n, exc: self.log.append(
                    action=ACT_RETRY, detail=f"ntfy attempt {n}: {exc}"
                ),
            )
        except Exception as exc:
            self.log.append(action=ACT_PAGE_FAILED, detail=f"{title}: {exc}")
            report.errors.append(f"page failed: {exc}")
            return
        self.log.append(action=ACT_PAGED, detail=title, status=status)
        report.paged.append(f"{status}: {title}")

    # -- cycle ----------------------------------------------------------

    def run_once(self) -> CycleReport:
        report = CycleReport()
        self.ensure_lanes_asserted()

        # The lazy-auth boundary, and the reason it is HERE: authorisation is
        # acquired once, before any retry loop, so that a transient failure
        # inside a retried call reuses the held credential instead of re-opening
        # a consent prompt. A hard auth failure fails the cycle LOUDLY through
        # the ruled channels -- ERROR page and log row, run halted -- rather than
        # being retried into a prompt, which is the failure mode that would make
        # an unattended run stop and silently wait for a human.
        try:
            self.transport.ensure_authorised()
        except (QueueDriverError, TransientError) as exc:
            self.log.append(action=ACT_REFUSED, detail=f"authorisation failed: {exc}")
            report.errors.append(f"authorisation failed: {exc}")
            self.emit_page(
                ERROR,
                "ARCAAI queue driver: ERROR",
                f"Authorisation failed; the cycle is halted before any queue work.\n\n{exc}",
                report,
            )
            return report

        try:
            self.poll_inbound(report)
        except TransientError as exc:
            report.errors.append(f"inbound poll failed: {exc}")
            self.emit_page(ERROR, "ARCAAI queue driver: ERROR", str(exc), report)
        try:
            self.sweep_outboxes(report)
        except OSError as exc:
            report.errors.append(f"outbox sweep failed: {exc}")
            self.emit_page(ERROR, "ARCAAI queue driver: ERROR", str(exc), report)
        return report

    def run_forever(self) -> None:
        while True:
            render_report(self.run_once())
            time.sleep(self.config.poll_interval_seconds)


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------


def render_report(report: CycleReport) -> None:
    print(
        f"[{utc_now_iso()}] routed={len(report.routed)} refused={len(report.refused)} "
        f"swept={len(report.swept)} paged={len(report.paged)} errors={len(report.errors)}"
    )
    for item in report.routed:
        print(f"  ROUTED  PROMPT {item}")
    for item in report.swept:
        print(f"  SWEPT   {item}")
    for item in report.paged:
        print(f"  PAGED   {item}")
    for item in report.refused:
        print(f"  REFUSED {item}")
    for item in report.errors:
        print(f"  ERROR   {item}")


def render_lane_assertions(results: dict[str, LaneAssertion]) -> bool:
    print("LANE ISOLATION ASSERTION (DEC-0019 B1)")
    all_green = True
    for lane_id in sorted(results):
        result = results[lane_id]
        print(f"  {lane_id}  {result.outcome:<8} {result.detail}")
        if not result.routable:
            all_green = False
    return all_green


# --------------------------------------------------------------------------
# Offline dry run
# --------------------------------------------------------------------------


def _seed_fake_worktree(root: Path, name: str) -> Path:
    """Create a directory shaped like a linked git worktree, without running git."""
    lane = root / name
    (lane).mkdir(parents=True, exist_ok=True)
    (lane / ".git").write_text(f"gitdir: {root}/.gitmeta/worktrees/{name}\n", encoding="utf-8")
    return lane


def run_selftest() -> int:
    """Hermetic offline dry run of every path the envelope's item 8 names.

    Runs entirely in a temporary directory with a fake transport: it does not
    read, write or even resolve the live queue, and sends no network traffic.
    That is deliberate — a dry run that mutates the real queue is not a dry run.
    """
    checks: list[tuple[str, bool, str]] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        checks.append((name, bool(condition), detail))

    with tempfile.TemporaryDirectory(prefix="arcaai-queue-dryrun-") as tmp:
        root = Path(tmp)
        queue_root = root / "_queue"
        lane_t1 = _seed_fake_worktree(root, "wt-t1")
        lane_t2 = _seed_fake_worktree(root, "wt-t2")
        main_tree = root / "wt-main"
        (main_tree / ".git").mkdir(parents=True, exist_ok=True)

        config = Config(
            queue_root=queue_root,
            lanes={
                "T1": Lane("T1", lane_t1),
                "T2": Lane("T2", lane_t2),
            },
            dispatch_order={"901": "T1", "902": "T2"},
            backoff_base=0.0,
        )

        # ---- 1. lane assertion, including the unisolated shape -------------
        lanes = assert_all_lanes(config)
        check("B1 lane T1 GREEN", lanes["T1"].routable, lanes["T1"].detail)
        check("B1 lane T2 GREEN", lanes["T2"].routable, lanes["T2"].detail)

        unisolated = assert_lane_isolation(Lane("TX", main_tree))
        check(
            "B1 refuses a main tree (.git is a directory)",
            unisolated.outcome == "RED" and "UNISOLATED" in unisolated.detail,
            unisolated.detail,
        )
        collide = assert_all_lanes(
            Config(queue_root=queue_root, lanes={"TA": Lane("TA", lane_t1),
                                                 "TB": Lane("TB", lane_t1)})
        )
        check(
            "B1 refuses two lanes sharing one path",
            not collide["TA"].routable and not collide["TB"].routable,
            collide["TA"].detail,
        )

        # ---- 2. the happy path, both lanes ---------------------------------
        body_t1 = "PROMPT 901 | TARGET: T1 | CLASS: synthetic\n\nBody for lane one.\n"
        body_t2 = "﻿PROMPT 902 | TARGET: T2 | CLASS: synthetic\n\nSee " \
                  "https://www.google.com/url?q=https%3A%2F%2Fexample.invalid%2Fa&sa=D now.\n"
        drafts = [
            make_draft("ARCAAI-PROMPT-901", body_t1, "draft-901"),
            make_draft("ARCAAI-PROMPT-902", body_t2, "draft-902"),
        ]
        transport = FakeTransport(drafts)
        notifier = RecordingNotifier()
        driver = QueueDriver(config, transport, notifier)
        report = driver.run_once()

        check("two synthetic prompts routed", sorted(report.routed) == ["901", "902"],
              f"routed={report.routed} refused={report.refused}")
        f901 = queue_root / "T1" / "inbox" / "PROMPT-901.md"
        f902 = queue_root / "T2" / "inbox" / "PROMPT-902.md"
        check("PROMPT-901.md landed in T1 inbox", f901.exists(), str(f901))
        check("PROMPT-902.md landed in T2 inbox", f902.exists(), str(f902))
        check("no BOM on driver-written file", not f902.read_bytes().startswith(BOM),
              f902.read_bytes()[:8].hex())
        check("google redirect wrapper unwrapped",
              b"example.invalid/a" in f902.read_bytes()
              and b"google.com/url" not in f902.read_bytes(),
              "")
        check("both drafts relabelled consumed", sorted(transport.consumed) ==
              ["draft-901", "draft-902"], str(transport.consumed))

        log = RoutingLog(config.log_path)
        routed_rows = [r for r in log.rows() if r["action"] == ACT_ROUTED]
        check("routing log carries all six required fields",
              all(all(k in r for k in ("timestamp", "prompt_no", "target", "action",
                                       "draft_id", "content_hash")) for r in routed_rows),
              f"{len(routed_rows)} ROUTED rows")
        check("content hash in log matches file on disk",
              all(sha256_hex(Path(r["path"]).read_bytes()) == r["content_hash"]
                  for r in routed_rows),
              "read-back verification")
        check("BOM strip was logged, not silent",
              any("BOM" in " ".join(r.get("notes", [])) for r in routed_rows), "")

        # ---- 3. idempotency ------------------------------------------------
        second = driver.run_once()
        check("re-poll routes nothing twice", second.routed == [], str(second.routed))

        # ---- 4. lane-mismatch refusal --------------------------------------
        mismatch = make_draft(
            "ARCAAI-PROMPT-901",
            "PROMPT 901 | TARGET: T2 | CLASS: synthetic\n\nWrong lane.\n",
            "draft-901-mismatch",
        )
        t_mis = FakeTransport([mismatch])
        n_mis = RecordingNotifier()
        d_mis = QueueDriver(config, t_mis, n_mis)
        r_mis = d_mis.run_once()
        check("lane/TARGET mismatch refused", len(r_mis.refused) == 1 and not r_mis.routed,
              r_mis.refused[0] if r_mis.refused else "")
        check("mismatch refusal cites the dispatch order",
              bool(r_mis.refused) and "dispatch order" in r_mis.refused[0], "")
        check("mismatch was NOT routed to disk",
              not (queue_root / "T2" / "inbox" / "PROMPT-901.md").exists(), "")
        check("mismatch paged ERROR", len(n_mis.pages) == 1, str(n_mis.pages[:1]))

        # ---- 5. malformed envelope -----------------------------------------
        malformed = make_draft(
            "ARCAAI-PROMPT-903", "PROMPT 903 | CLASS: synthetic\n\nNo target here.\n",
            "draft-903",
        )
        t_mal = FakeTransport([malformed])
        n_mal = RecordingNotifier()
        r_mal = QueueDriver(config, t_mal, n_mal).run_once()
        check("malformed envelope (no TARGET) refused",
              len(r_mal.refused) == 1 and not r_mal.routed,
              r_mal.refused[0] if r_mal.refused else "")
        check("malformed envelope paged ERROR", len(n_mal.pages) == 1, "")

        # ---- 6. overwrite refusal -------------------------------------------
        clash = make_draft(
            "ARCAAI-PROMPT-901",
            "PROMPT 901 | TARGET: T1 | CLASS: synthetic\n\nDIFFERENT BYTES.\n",
            "draft-901-clash",
        )
        before = f901.read_bytes()
        r_clash = QueueDriver(config, FakeTransport([clash]), RecordingNotifier()).run_once()
        check("differing rewrite of an existing prompt refused", len(r_clash.refused) == 1,
              r_clash.refused[0] if r_clash.refused else "")
        check("existing file untouched by the refusal", f901.read_bytes() == before, "")

        # ---- 7. ntfy policy across the whole vocabulary ----------------------
        for lane_id, prompt, status in (
            ("T1", "801", COMPLETE),
            ("T1", "802", RETRYING),
            ("T2", "803", BLOCKED_RULING),
            ("T2", "804", ERROR),
        ):
            outbox = config.outbox(lane_id)
            outbox.mkdir(parents=True, exist_ok=True)
            (outbox / f"PROMPT-{prompt}.outcome.md").write_text(
                f"STATUS: {status}\n\nSynthetic {status} outcome.\n", encoding="utf-8"
            )
        t_out = FakeTransport([])
        n_out = RecordingNotifier()
        d_out = QueueDriver(config, t_out, n_out)
        r_out = d_out.run_once()
        check("all four outcomes swept", len(r_out.swept) == 4, str(r_out.swept))
        paged_titles = " ".join(t for t, _m, _p in n_out.pages)
        check("BLOCKED-RULING paged", "BLOCKED-RULING" in paged_titles, paged_titles)
        check("ERROR paged", "ERROR" in paged_titles, paged_titles)
        check("COMPLETE did NOT page", "801" not in paged_titles and len(n_out.pages) == 2,
              f"{len(n_out.pages)} pages: {paged_titles}")
        check("RETRYING did NOT page", "802" not in paged_titles, paged_titles)
        check("one consolidated draft per session-day", len(t_out.outcome_drafts) == 1,
              str(list(t_out.outcome_drafts)))
        body = next(iter(t_out.outcome_drafts.values()))
        check("consolidated draft carries all four outcomes",
              all(f"PROMPT-{n}" in body for n in ("801", "802", "803", "804")), "")
        check("consolidated subject is ARCAAI-OUTCOMES-YYYYMMDD",
              any(r.get("subject") == f"ARCAAI-OUTCOMES-{session_day()}"
                  for r in d_out.log.rows() if r["action"] == ACT_OUTCOMES_DRAFT), "")

        # re-sweep must not duplicate
        r_out2 = d_out.run_once()
        check("re-sweep sweeps nothing twice", r_out2.swept == [], str(r_out2.swept))

        # ---- 8. retry with backoff -------------------------------------------
        t_flaky = FakeTransport([make_draft(
            "ARCAAI-PROMPT-905", "PROMPT 905 | TARGET: T2 | CLASS: synthetic\n\nx\n", "d-905")])
        t_flaky.fail_list_times = 2
        d_flaky = QueueDriver(config, t_flaky, RecordingNotifier())
        r_flaky = d_flaky.run_once()
        retries = [r for r in d_flaky.log.rows() if r["action"] == ACT_RETRY]
        check("transient failure retried then succeeded",
              r_flaky.routed == ["905"] and len(retries) >= 2, f"{len(retries)} retry rows")

        t_dead = FakeTransport([make_draft(
            "ARCAAI-PROMPT-906", "PROMPT 906 | TARGET: T2 | CLASS: synthetic\n\nx\n", "d-906")])
        t_dead.fail_list_times = 99
        n_dead = RecordingNotifier()
        r_dead = QueueDriver(config, t_dead, n_dead).run_once()
        check("exhausted retries raise ERROR and page",
              bool(r_dead.errors) and len(n_dead.pages) == 1, str(r_dead.errors))

        # ---- 9. B2 read-back verification actually fires ----------------------
        # A write that lands different bytes must be caught. Without this the
        # verification is unfalsifiable: expected and actual agree by
        # construction whether or not the comparison is performed.
        class CorruptingDriver(QueueDriver):
            def _write_bytes(self, destination: Path, content: bytes) -> None:
                super()._write_bytes(destination, content + b"CORRUPTION")

        t_corrupt = FakeTransport([make_draft(
            "ARCAAI-PROMPT-907", "PROMPT 907 | TARGET: T2 | CLASS: synthetic\n\nx\n", "d-907")])
        n_corrupt = RecordingNotifier()
        r_corrupt = CorruptingDriver(config, t_corrupt, n_corrupt).run_once()
        check("a write landing different bytes is REFUSED (B2 read-back fires)",
              len(r_corrupt.refused) == 1 and not r_corrupt.routed,
              r_corrupt.refused[0] if r_corrupt.refused else "routed without verification")
        check("the B2 refusal names hash verification",
              bool(r_corrupt.refused) and "verification FAILED" in r_corrupt.refused[0],
              r_corrupt.refused[0] if r_corrupt.refused else "")
        check("a corrupt write is never relabelled consumed",
              t_corrupt.consumed == [], str(t_corrupt.consumed))

        # ---- 10. write-scope guard -------------------------------------------
        guard_driver = QueueDriver(config, FakeTransport([]), RecordingNotifier())
        message = ""
        try:
            guard_driver._assert_within_queue(root / "outside.md")
        except QueueDriverError as exc:
            message = str(exc)
        check("refuses to write outside the queue root", "outside the queue root" in message,
              message)

        # The lane guard is only REACHABLE when a lane sits inside the queue
        # root; in the ordinary layout the guard above fires first. Asserting
        # it against the ordinary layout would pass on the other guard's
        # refusal — a check green for a reason other than its name.
        nested_lane = _seed_fake_worktree(queue_root, "nested-wt")
        nested_config = Config(
            queue_root=queue_root, lanes={"TN": Lane("TN", nested_lane)}, backoff_base=0.0
        )
        nested_driver = QueueDriver(nested_config, FakeTransport([]), RecordingNotifier())
        message = ""
        try:
            nested_driver._assert_within_queue(nested_lane / "evil.md")
        except QueueDriverError as exc:
            message = str(exc)
        check("refuses to write inside a lane worktree", "inside lane worktree" in message,
              message)

    print("=" * 78)
    print("QUEUE DRIVER OFFLINE DRY RUN  (hermetic temp dir; no Gmail, no network)")
    print("=" * 78)
    failed = 0
    for name, ok, detail in checks:
        mark = "PASS" if ok else "FAIL"
        if not ok:
            failed += 1
        print(f"  [{mark}] {name}")
        if detail and not ok:
            print(f"         {detail}")
    print("-" * 78)
    print(f"  {len(checks) - failed}/{len(checks)} checks passed, {failed} failed")
    if failed:
        print("  RESULT: RED")
        return 1
    print("  RESULT: GREEN")
    return 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ARCAAI Gmail <-> _queue driver")
    default_config = Path(__file__).with_name("queue_driver.config.json")
    parser.add_argument("--config", default=str(default_config), help="path to driver config JSON")
    parser.add_argument("--once", action="store_true", help="run a single poll cycle and exit")
    parser.add_argument("--interval", type=int, default=None, help="override poll interval")
    parser.add_argument(
        "--assert-lanes", action="store_true", help="run the B1 lane assertion and exit"
    )
    parser.add_argument("--print-config", action="store_true", help="print resolved config, exit")
    parser.add_argument(
        "--selftest", action="store_true", help="hermetic offline dry run; no Gmail, no network"
    )
    args = parser.parse_args(argv)

    # The dry run is hermetic and must not depend on a config file existing.
    if args.selftest:
        return run_selftest()

    try:
        config = load_config(Path(args.config))
        if args.interval is not None:
            config = dataclasses.replace(config, poll_interval_seconds=args.interval)
    except QueueDriverError as exc:
        print(f"CONFIG ERROR: {exc}", file=sys.stderr)
        return 2

    if args.print_config:
        print(json.dumps({
            "queue_root": str(config.queue_root),
            "poll_interval_seconds": config.poll_interval_seconds,
            "lanes": {k: str(v.worktree) for k, v in config.lanes.items()},
            "log_path": str(config.log_path),
            "ntfy_server": config.ntfy_server,
            "ntfy_topic_configured": bool(config.ntfy_topic),
            "credentials_path": str(config.credentials_path),
            "token_path": str(config.token_path),
            "dispatch_order": config.dispatch_order,
        }, indent=2))
        return 0

    if args.assert_lanes:
        return 0 if render_lane_assertions(assert_all_lanes(config)) else 1

    # Fail closed on the alerting path: a driver that cannot page is one whose
    # ERROR and BLOCKED-RULING outcomes reach nobody, which is worse than one
    # that refuses to start.
    if not config.ntfy_topic:
        print(
            "REFUSING TO START: no ntfy topic configured. Set ARCAAI_NTFY_TOPIC, or "
            "ntfy_topic in the config file. A driver that cannot page cannot report "
            "BLOCKED-RULING or ERROR, and would run unmonitored.",
            file=sys.stderr,
        )
        return 2

    driver = QueueDriver(
        config,
        GmailTransport(config.credentials_path, config.token_path),
        NtfyNotifier(config.ntfy_server, config.ntfy_topic),
    )
    results = driver.ensure_lanes_asserted(force=True)
    render_lane_assertions(results)
    driver.log.append(
        action=ACT_START,
        detail=f"driver start, interval {config.poll_interval_seconds}s",
        lanes={k: v.outcome for k, v in results.items()},
    )

    if args.once:
        report = driver.run_once()
        render_report(report)
        return 0 if report.clean else 1
    driver.run_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
