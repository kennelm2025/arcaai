"""Platform retrieval machinery (ADR-0009): store-agnostic interface
and deterministic chunker. Store adapters live beside this package,
one module per store, and are the only permitted location for
store-specific imports (CF-1/B7-a)."""

from arcaai.platform.retrieval.chunker import CHUNKER_VERSION, chunk_document
from arcaai.platform.retrieval.interface import (
    Chunk,
    RetrievalStore,
    RetrievedChunk,
    make_chunk_id,
)

__all__ = [
    "CHUNKER_VERSION",
    "Chunk",
    "RetrievalStore",
    "RetrievedChunk",
    "chunk_document",
    "make_chunk_id",
]
