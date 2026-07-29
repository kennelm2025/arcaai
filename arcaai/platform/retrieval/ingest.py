"""Corpus ingest machinery (B7 inc3).

Drives DEC-0014's processing fields: chunk every eligible document,
index the chunks through a RetrievalStore, and produce the new manifest
text with processing facts populated — after which
``retrieval_snapshot_sha256`` diverges from ``eligible_set_sha256`` for
the first time, which is the two-hash design doing its job.

Three disciplines:

1. **Content-addressed resolution.** Document files are matched to
   manifest entries by sha256 of their bytes, never by filename. A file
   that matches IS the manifested document; an eligible entry with no
   matching file is a hard failure before any indexing.
2. **Surgical manifest edit.** The manifest is comment-rich governed
   YAML; a parse→dump round-trip would destroy its version notes and
   formatting. Processing fields are therefore updated textually,
   per-document, and the result is re-parsed, hash-checked and passed
   through check_append_only against the input before it is returned.
   This module never writes the file — the caller (operator CLI) does,
   after seeing the verification output.
3. **No database writes.** Loading the new version's snapshot row is a
   separate governed act (the existing load procedure), not a side
   effect of ingest.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import pathlib
import re
from dataclasses import dataclass
from typing import Any

from arcaai.platform.governance import corpus
from arcaai.platform.retrieval.chunker import CHUNKER_VERSION, chunk_document
from arcaai.platform.retrieval.interface import RetrievalStore


class IngestError(RuntimeError):
    """Resolution or update failure; nothing was indexed or written."""


@dataclass(frozen=True)
class ResolvedDoc:
    doc_id: str
    path: pathlib.Path
    content_sha256: str
    text: str


def resolve_documents(
    manifest: dict[str, Any], docs_dir: pathlib.Path
) -> list[ResolvedDoc]:
    """Match every ELIGIBLE manifest entry to a file in docs_dir by
    content hash. Hard-fails listing every unmatched id; hard-fails on
    two manifest entries hashing identically (ids must differ but the
    same bytes under two ids is a manifest defect worth stopping for).
    """
    by_hash: dict[str, pathlib.Path] = {}
    for path in sorted(docs_dir.rglob("*")):
        if not path.is_file():
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        by_hash.setdefault(digest, path)  # first match wins; dupes benign

    resolved: list[ResolvedDoc] = []
    missing: list[str] = []
    seen_hashes: dict[str, str] = {}
    for doc in corpus.eligible_documents(manifest):
        sha = doc["content_sha256"].lower()
        if sha in seen_hashes:
            raise IngestError(
                f"{doc['id']} and {seen_hashes[sha]} share content_sha256 "
                f"{sha[:12]}… — one text under two ids is a manifest defect"
            )
        seen_hashes[sha] = doc["id"]
        path = by_hash.get(sha)
        if path is None:
            missing.append(f"{doc['id']} ({sha[:12]}…)")
            continue
        resolved.append(
            ResolvedDoc(
                doc_id=doc["id"],
                path=path,
                content_sha256=sha,
                text=path.read_text(encoding="utf-8"),
            )
        )
    if missing:
        raise IngestError(
            "eligible documents with no matching file in "
            f"{docs_dir}: {', '.join(missing)}"
        )
    return resolved


def ingest_documents(
    resolved: list[ResolvedDoc], store: RetrievalStore
) -> dict[str, int]:
    """Chunk and index every resolved document. Returns chunk counts
    per doc_id. Idempotent via the store's chunk_id semantics."""
    counts: dict[str, int] = {}
    for doc in resolved:
        chunks = chunk_document(doc.doc_id, doc.text)
        if not chunks:
            raise IngestError(f"{doc.doc_id}: chunker produced no chunks")
        store.add_chunks(chunks)
        counts[doc.doc_id] = len(chunks)
    return counts


_PROCESSING_TEMPLATE = """    processing:
      chunker_version: {chunker}
      embedding_model: {embedding}
      chunk_count: {count}
      ingest_timestamp: {stamp}"""

_PROCESSING_BLOCK_RE = re.compile(
    r"    processing:\n"
    r"      chunker_version: .*\n"
    r"      embedding_model: .*\n"
    r"      chunk_count: .*\n"
    r"      ingest_timestamp: .*"
)


def updated_manifest_text(
    manifest_text: str,
    counts: dict[str, int],
    embedding_model: str,
    new_version: str,
    note_lines: list[str],
    ingested_at: _dt.datetime | None = None,
) -> str:
    """Produce the new manifest text: version bump, appended header
    note, processing blocks populated for ingested documents. Purely
    textual — comments and formatting above each edit survive intact.

    Verifies before returning: parses, passes check_append_only against
    the input, and every ingested document's processing fields read
    back exactly as written. Raises IngestError otherwise; the caller
    writes the file only on a clean return.
    """
    old = corpus.parse_manifest(manifest_text)
    stamp = (ingested_at or _dt.datetime.now(_dt.timezone.utc)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    version_line = f"manifest_version: {old['manifest_version']}"
    if manifest_text.count(version_line) != 1:
        raise IngestError("manifest_version line not found exactly once")
    note = "".join(f"# {line}\n" for line in note_lines)
    text = manifest_text.replace(
        version_line, f"{note}\nmanifest_version: {new_version}"
    )

    # Per-document processing update: split on document starts so each
    # replacement is scoped to exactly one entry.
    parts = re.split(r"(?m)(^  - id: .+$)", text)
    for i in range(1, len(parts), 2):
        doc_id = parts[i].removeprefix("  - id: ").strip()
        if doc_id not in counts:
            continue
        block, n = _PROCESSING_BLOCK_RE.subn(
            _PROCESSING_TEMPLATE.format(
                chunker=f'"{CHUNKER_VERSION}"',
                embedding=f'"{embedding_model}"',
                count=counts[doc_id],
                stamp=f'"{stamp}"',
            ),
            parts[i + 1],
        )
        if n != 1:
            raise IngestError(
                f"{doc_id}: expected exactly one processing block, found {n}"
            )
        parts[i + 1] = block
    new_text = "".join(parts)

    new = corpus.parse_manifest(new_text)
    corpus.check_append_only(old, new)
    for doc in new["documents"]:
        if doc["id"] not in counts:
            continue
        proc = doc.get("processing") or {}
        if (
            proc.get("chunker_version") != CHUNKER_VERSION
            or proc.get("embedding_model") != embedding_model
            or proc.get("chunk_count") != counts[doc["id"]]
            or proc.get("ingest_timestamp") != stamp
        ):
            raise IngestError(f"{doc['id']}: processing read-back mismatch")
    if new["manifest_version"] != new_version:
        raise IngestError("manifest_version read-back mismatch")
    return new_text
