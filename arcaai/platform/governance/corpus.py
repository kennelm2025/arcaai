"""Corpus manifest machinery (DEC-0014).

The manifest at ``verticals/fraud/corpus/MANIFEST.yaml`` is the sole
governing artefact for corpus identity, licence, SA5 classification and
retrieval eligibility. This module is the platform-side machinery only:
schema validation, normative canonicalisation and hashing, the
mechanical append-only check, and the load snapshot. It holds no corpus
state; the ``corpus_version`` row is evidence that a version was loaded
and MUST NEVER be used to regenerate the manifest (DEC-0014 standing
constraint). If code in this module ever writes eligibility state into
Postgres, the hybrid has collapsed into the rejected four-table
anti-pattern — that is a defect, not an extension point.

ADR-0009: nothing here imports from ``verticals``; the manifest *path*
arrives as an argument.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import uuid
from typing import Any

import yaml
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import CorpusVersion

LICENCES = frozenset({"synthetic-arcaai", "OGL-v3.0"})  # DEC-0011
STATES = frozenset({"included", "pending_review", "withdrawn", "deprecated"})
_HEX64 = frozenset("0123456789abcdef")


class ManifestError(ValueError):
    """Schema or invariant violation in the manifest content."""


class AppendOnlyViolation(ManifestError):
    """A historical eligibility transition was deleted, modified or
    reordered (DEC-0014 rule: appending a later transition is the only
    valid change)."""


class HashPinMismatch(RuntimeError):
    """Manifest content does not match the hash pinned at a previous
    load of the same version label — the tamper-evidence hard failure
    (DEC-0014 item 7)."""


# ---------------------------------------------------------------- schema


def parse_manifest(text: str) -> dict[str, Any]:
    """Parse and validate; returns the manifest dict or raises
    ManifestError. Validation is exhaustive because the manifest is
    governed input — a lenient parser is an unenforced schema."""
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ManifestError("manifest root must be a mapping")
    if not isinstance(data.get("manifest_version"), str) or not data["manifest_version"].strip():
        raise ManifestError("manifest_version: non-empty string required")
    docs = data.get("documents")
    if not isinstance(docs, list) or not docs:
        raise ManifestError("documents: non-empty list required")

    seen_ids: set[str] = set()
    for i, doc in enumerate(docs):
        where = f"documents[{i}]"
        if not isinstance(doc, dict):
            raise ManifestError(f"{where}: mapping required")
        for field in ("id", "source", "licence", "sa5_classification", "content_sha256"):
            v = doc.get(field)
            if not isinstance(v, str) or not v.strip():
                raise ManifestError(f"{where}.{field}: non-empty string required")
        if doc["id"] in seen_ids:
            raise ManifestError(f"{where}: duplicate id {doc['id']!r}")
        seen_ids.add(doc["id"])
        if doc["licence"] not in LICENCES:
            raise ManifestError(
                f"{where}.licence: {doc['licence']!r} not in {sorted(LICENCES)} (DEC-0011)")
        sha = doc["content_sha256"].lower()
        if len(sha) != 64 or not set(sha) <= _HEX64:
            raise ManifestError(f"{where}.content_sha256: 64 lowercase hex chars required")

        trans = doc.get("eligibility")
        if not isinstance(trans, list) or not trans:
            raise ManifestError(f"{where}.eligibility: non-empty transition list required "
                                "(a mutable flag is prohibited)")
        prev_date: _dt.date | None = None
        for j, t in enumerate(trans):
            tw = f"{where}.eligibility[{j}]"
            if not isinstance(t, dict):
                raise ManifestError(f"{tw}: mapping required")
            if t.get("state") not in STATES:
                raise ManifestError(f"{tw}.state: {t.get('state')!r} not in {sorted(STATES)}")
            d = t.get("date")
            if isinstance(d, str):
                try:
                    d = _dt.date.fromisoformat(d)
                except ValueError as exc:
                    raise ManifestError(f"{tw}.date: not ISO format") from exc
            if not isinstance(d, _dt.date):
                raise ManifestError(f"{tw}.date: date required")
            if prev_date is not None and d < prev_date:
                raise ManifestError(f"{tw}: transitions out of chronological order")
            prev_date = d
            if not isinstance(t.get("reason"), str) or not t["reason"].strip():
                raise ManifestError(f"{tw}.reason: non-empty string required")

        proc = doc.get("processing")
        if proc is not None and not isinstance(proc, dict):
            raise ManifestError(f"{where}.processing: mapping or absent")
    return data


# ---------------------------------------------- canonicalisation + hashes


def canonicalise(manifest: dict[str, Any]) -> bytes:
    """Normative canonical form (DEC-0014 item 4): deterministic UTF-8
    serialisation with stable key ordering, LF endings, insignificant
    whitespace removed. JSON with sorted keys and fixed separators
    satisfies all three and is independent of YAML formatting choices,
    so reflowing the file without changing content does not change the
    hash."""
    return json.dumps(
        manifest, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, default=str,
    ).encode("utf-8")


def manifest_sha256(manifest: dict[str, Any]) -> str:
    return hashlib.sha256(canonicalise(manifest)).hexdigest()


def _latest_state(doc: dict[str, Any]) -> str:
    return doc["eligibility"][-1]["state"]


def eligible_documents(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [d for d in manifest["documents"] if _latest_state(d) == "included"]


def state_as_at(doc: dict[str, Any], as_at: _dt.date) -> str | None:
    """Eligibility state as at a date: latest transition on or before
    ``as_at``; None if the document had no state yet (B7_GATE §3 —
    eligibility as at the decision)."""
    state = None
    for t in doc["eligibility"]:
        d = t["date"]
        if isinstance(d, str):
            d = _dt.date.fromisoformat(d)
        if d <= as_at:
            state = t["state"]
        else:
            break
    return state


def eligible_set_sha256(manifest: dict[str, Any]) -> str:
    """Same documents? — hash of the sorted eligible (doc_id,
    content_sha256) pairs. Deliberately excludes processing facts
    (DEC-0014 item 3 / panel Q4)."""
    pairs = sorted((d["id"], d["content_sha256"].lower())
                   for d in eligible_documents(manifest))
    return hashlib.sha256(json.dumps(pairs).encode("utf-8")).hexdigest()


def retrieval_snapshot_sha256(manifest: dict[str, Any]) -> str:
    """Operationally identical retrieval? — the eligible pairs plus the
    processing facts that change what retrieval sees."""
    rows = sorted(
        (
            d["id"],
            d["content_sha256"].lower(),
            str((d.get("processing") or {}).get("chunker_version")),
            str((d.get("processing") or {}).get("embedding_model")),
            str((d.get("processing") or {}).get("chunk_count")),
        )
        for d in eligible_documents(manifest)
    )
    return hashlib.sha256(json.dumps(rows).encode("utf-8")).hexdigest()


# ------------------------------------------------- mechanical append-only


def check_append_only(old: dict[str, Any], new: dict[str, Any]) -> None:
    """DEC-0014 item 5: against the previously loaded manifest, hard-fail
    on deleted, modified or reordered historical transitions; the only
    valid eligibility change is appending a later transition. Also
    enforces document identity immutability and no document removal."""
    old_docs = {d["id"]: d for d in old["documents"]}
    new_docs = {d["id"]: d for d in new["documents"]}
    for doc_id, od in old_docs.items():
        nd = new_docs.get(doc_id)
        if nd is None:
            raise AppendOnlyViolation(
                f"{doc_id}: document removed — a revised or withdrawn document "
                "is a transition, never a deletion")
        for field in ("source", "licence", "sa5_classification", "content_sha256"):
            if od[field] != nd[field]:
                raise AppendOnlyViolation(
                    f"{doc_id}.{field}: identity field changed — a revised "
                    "source document is a NEW entry with a new sha256")
        ot, nt = od["eligibility"], nd["eligibility"]
        if len(nt) < len(ot):
            raise AppendOnlyViolation(f"{doc_id}: transition(s) deleted")
        for j, (a, b) in enumerate(zip(ot, nt)):
            if json.dumps(a, sort_keys=True, default=str) != json.dumps(b, sort_keys=True, default=str):
                raise AppendOnlyViolation(
                    f"{doc_id}.eligibility[{j}]: historical transition modified "
                    "or reordered")


# ------------------------------------------------------------ load / pin


def load_snapshot(session: Session, manifest: dict[str, Any]) -> CorpusVersion:
    """Idempotent load with hash-pinning (DEC-0014 item 7).

    Same content already loaded → the existing row. Same
    ``manifest_version`` label pinned with DIFFERENT content →
    HashPinMismatch, a hard failure: once loaded, a version's hash is
    pinned forever, and rewriting history produces this mismatch rather
    than silent corruption. New content under a new label → new row.
    ``eligible_doc_count`` is derived metadata cached for convenience;
    the manifest is authoritative.
    """
    m_sha = manifest_sha256(manifest)
    label = manifest["manifest_version"]

    existing = session.scalars(
        select(CorpusVersion).where(CorpusVersion.manifest_version == label)
    ).all()
    for row in existing:
        if row.manifest_sha256 == m_sha:
            return row
    if existing:
        raise HashPinMismatch(
            f"manifest_version {label!r} is pinned to "
            f"{existing[0].manifest_sha256} but current content hashes to "
            f"{m_sha}; refusing to load")

    row = CorpusVersion(
        version_id=uuid.uuid4(),
        manifest_version=label,
        manifest_sha256=m_sha,
        eligible_set_sha256=eligible_set_sha256(manifest),
        retrieval_snapshot_sha256=retrieval_snapshot_sha256(manifest),
        eligible_doc_count=len(eligible_documents(manifest)),
        loaded_at=_dt.datetime.now(_dt.timezone.utc),
    )
    session.add(row)
    session.commit()
    return row
