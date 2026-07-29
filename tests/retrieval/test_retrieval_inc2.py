"""inc2 suite: the ChromaDB adapter against real chromadb, offline.

Tests inject a deterministic embedding function (no network, no model
download) so the suite runs offline and fast; the pinned production
function is exercised only for its construction-time name check, not
its embedding path — the real first embed is an ingest-stage,
operator-visible event (inc3), and CI must not depend on a model
download succeeding.
"""

from __future__ import annotations

import hashlib
import math

from arcaai.platform.retrieval import chunk_document
from arcaai.platform.retrieval.chroma_store import (
    _PINNED_MODEL_NAME,
    EMBEDDING_MODEL,
    ChromaStore,
    supplied_model_name,
)


class HashEmbedding:
    """Deterministic 16-dim embedding from a sha256 of the text — a
    plain callable; the adapter wraps it, so this file imports no
    chromadb (CF-1/B7-a holds even for tests)."""

    def __call__(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for text in texts:
            digest = hashlib.sha256(text.encode("utf-8")).digest()
            vec = [b / 255.0 for b in digest[:16]]
            norm = math.sqrt(sum(v * v for v in vec)) or 1.0
            vectors.append([v / norm for v in vec])
        return vectors


def make_store() -> ChromaStore:
    return ChromaStore(
        collection_name="test_fraud_corpus",
        embedding_function=HashEmbedding(),
    )


PARA = ("alpha bravo charlie delta echo " * 10).strip()
DOC = "\n\n".join(
    f"Paragraph {i}. " + PARA for i in range(6)
)


def test_add_count_idempotent() -> None:
    store = make_store()
    chunks = chunk_document("SYN-TR-01", DOC)
    assert store.add_chunks(chunks) == len(chunks)
    assert store.count() == len(chunks)
    assert store.add_chunks(chunks) == 0  # idempotent on chunk_id
    assert store.count() == len(chunks)
    store.reset()


def test_query_returns_traceable_chunks_best_first() -> None:
    store = make_store()
    chunks = chunk_document("SYN-TR-01", DOC)
    store.add_chunks(chunks)
    exact = chunks[0].text  # identical text embeds identically
    hits = store.query(exact, top_k=3)
    assert hits
    assert hits[0].chunk.chunk_id == chunks[0].chunk_id  # self-match wins
    assert hits[0].chunk.doc_id == "SYN-TR-01"
    assert hits[0].chunk.chunker_version == chunks[0].chunker_version
    scores = [h.score for h in hits]
    assert scores == sorted(scores)  # distances ascend: best first
    store.reset()


def test_round_trip_preserves_chunk_fields() -> None:
    store = make_store()
    chunks = chunk_document("SYN-SG-02", DOC)
    store.add_chunks(chunks)
    hit = store.query(chunks[1].text, top_k=1)[0]
    assert hit.chunk == chunks[1]  # full dataclass equality
    store.reset()


def test_empty_store_query_and_empty_add() -> None:
    store = make_store()
    assert store.query("anything") == []
    assert store.add_chunks([]) == 0
    store.reset()


def test_reset_clears() -> None:
    store = make_store()
    store.add_chunks(chunk_document("D", DOC))
    assert store.count() > 0
    store.reset()
    assert store.count() == 0
    assert store.query("alpha") == []


def test_top_k_caps_at_count() -> None:
    store = make_store()
    chunks = chunk_document("D", DOC)
    store.add_chunks(chunks)
    hits = store.query(chunks[0].text, top_k=50)
    assert len(hits) == min(50, len(chunks))
    store.reset()


def test_embedding_pin_name_check() -> None:
    # The pin string records name + runtime + supplying package version,
    # and the class chromadb ships still names the pinned model.
    assert EMBEDDING_MODEL.startswith(_PINNED_MODEL_NAME + ";")
    assert "chromadb==1.5.9" in EMBEDDING_MODEL
    assert supplied_model_name() == _PINNED_MODEL_NAME
