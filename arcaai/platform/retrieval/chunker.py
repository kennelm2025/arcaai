"""Deterministic paragraph-packing chunker.

CHUNKER_VERSION is a governed value: it is recorded per document in
the corpus manifest's processing fields and participates in
``retrieval_snapshot_sha256`` (DEC-0014 item 3, second hash). Any
change to the algorithm below that can alter chunk boundaries or text
MUST bump the version string — an unbumped behavioural change is
exactly the "actual not intended" nondeterminism the snapshot hash
exists to catch.

Algorithm (para-pack v1):
  1. Normalise line endings to LF; strip trailing whitespace per line.
  2. Split into paragraphs on blank lines.
  3. Pack consecutive whole paragraphs into a chunk until adding the
     next paragraph would exceed TARGET_WORDS; then start a new chunk.
  4. A single paragraph longer than HARD_CAP_WORDS is split on
     sentence boundaries (". " lookahead), packed to TARGET_WORDS.
  5. No overlap in v1 — regulatory prose is paragraph-structured and
     citation-dense; overlap is a measured decision for a later
     version, against the RAGAS baseline, not a default.

Deterministic by construction: no randomness, no environment input,
pure function of (doc_id, text).
"""

from __future__ import annotations

import re

from arcaai.platform.retrieval.interface import Chunk, make_chunk_id

CHUNKER_VERSION = "para-pack-v1;target=220w;cap=380w"

TARGET_WORDS = 220
HARD_CAP_WORDS = 380

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _paragraphs(text: str) -> list[str]:
    normalised = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in normalised.split("\n")]
    paras: list[str] = []
    buffer: list[str] = []
    for line in lines:
        if line.strip() == "":
            if buffer:
                paras.append("\n".join(buffer))
                buffer = []
        else:
            buffer.append(line)
    if buffer:
        paras.append("\n".join(buffer))
    return paras


def _split_oversize(paragraph: str) -> list[str]:
    """Split one oversized paragraph on sentence boundaries into
    pieces packed toward TARGET_WORDS."""
    sentences = _SENTENCE_SPLIT.split(paragraph)
    pieces: list[str] = []
    buffer: list[str] = []
    count = 0
    for sentence in sentences:
        words = len(sentence.split())
        if buffer and count + words > TARGET_WORDS:
            pieces.append(" ".join(buffer))
            buffer, count = [], 0
        buffer.append(sentence)
        count += words
    if buffer:
        pieces.append(" ".join(buffer))
    return pieces


def chunk_document(doc_id: str, text: str) -> list[Chunk]:
    """Chunk one document deterministically. Empty/whitespace-only
    input yields an empty list, never an empty chunk."""
    units: list[str] = []
    for para in _paragraphs(text):
        if len(para.split()) > HARD_CAP_WORDS:
            units.extend(_split_oversize(para))
        else:
            units.append(para)

    chunks: list[Chunk] = []
    buffer: list[str] = []
    count = 0

    def flush() -> None:
        nonlocal buffer, count
        if not buffer:
            return
        body = "\n\n".join(buffer)
        ordinal = len(chunks)
        chunks.append(
            Chunk(
                chunk_id=make_chunk_id(doc_id, ordinal, body),
                doc_id=doc_id,
                ordinal=ordinal,
                text=body,
                word_count=len(body.split()),
                chunker_version=CHUNKER_VERSION,
            )
        )
        buffer, count = [], 0

    for unit in units:
        words = len(unit.split())
        if buffer and count + words > TARGET_WORDS:
            flush()
        buffer.append(unit)
        count += words
    flush()
    return chunks
