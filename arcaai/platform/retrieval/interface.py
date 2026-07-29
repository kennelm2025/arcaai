"""Store-agnostic retrieval interface (platform machinery, ADR-0009).

CF-1/B7-a: the vector store is an implementation detail behind this
interface. ChromaDB serves the reference build; R5 fixes self-managed
OpenSearch for Phase 2 deployment. The relationship is: same interface,
different adapter — a swap, not a rewrite. No store-specific import may
appear in this module or anywhere outside a single adapter module
(enforced by tests/retrieval/test_import_boundary.py).

Chunk identity: chunk_id is deterministic — a function of the document
id, the chunk ordinal and the chunk text hash — so that a re-chunk of
identical content under the same chunker version yields identical ids.
Grounding (B7_GATE §3) traces claim → chunk_id → doc_id → manifest
entry; nothing in that chain may depend on store internals.
"""

from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


def make_chunk_id(doc_id: str, ordinal: int, text: str) -> str:
    """Deterministic chunk id: doc, position, and content-derived suffix.

    The 12-hex suffix ties the id to the exact text, so a chunker or
    content change is visible in the id itself (same discipline as the
    manifest's content addressing, DEC-0014).
    """
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    return f"{doc_id}#{ordinal:04d}-{digest}"


@dataclass(frozen=True)
class Chunk:
    """A unit of ingestable text, traceable to a manifest entry."""

    chunk_id: str
    doc_id: str
    ordinal: int
    text: str
    word_count: int
    chunker_version: str


@dataclass(frozen=True)
class RetrievedChunk:
    """A chunk returned by a query, with the store's relevance score.

    ``score`` semantics are adapter-defined (cosine distance, BM25, …)
    and are recorded, not compared across adapters.
    """

    chunk: Chunk
    score: float
    metadata: dict = field(default_factory=dict)


class RetrievalStore(ABC):
    """The platform's retrieval contract.

    Adapters implement exactly this surface. Vertical and agent code
    depend on this class only; constructing a concrete adapter is a
    composition-root concern.
    """

    @abstractmethod
    def add_chunks(self, chunks: list[Chunk]) -> int:
        """Index chunks. Returns the number added. Idempotent on
        chunk_id: re-adding an existing id is a no-op, not a duplicate."""

    @abstractmethod
    def query(self, text: str, top_k: int = 5) -> list[RetrievedChunk]:
        """Return the top_k most relevant chunks for ``text``,
        best-first. Empty list when the index is empty."""

    @abstractmethod
    def count(self) -> int:
        """Number of chunks currently indexed."""

    @abstractmethod
    def reset(self) -> None:
        """Remove all indexed chunks (test and re-ingest support)."""
