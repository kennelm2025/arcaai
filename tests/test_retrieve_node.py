"""B7 inc4: retrieve node unit tests - fake store, no chromadb, no DB.

The node is pure without an active governed context (emission is
conditional on current_governed_context()); the emission leg is
exercised by the governance-side wiring test against the dev Postgres
stack (inc4-b), not here. The fake implements the RetrievalStore ABC
exactly - the owned-fixture discipline of WS-E 57.
"""
import pytest

from agent.graph import build_graph
from agent.retrieval import make_retrieve_node
from arcaai.platform.retrieval import (
    Chunk,
    RetrievalStore,
    RetrievedChunk,
    make_chunk_id,
)


class FakeStore(RetrievalStore):
    def __init__(self, results):
        self._results = results
        self.queries = []

    def add_chunks(self, chunks):
        return 0

    def query(self, text, top_k=5):
        self.queries.append((text, top_k))
        return self._results[:top_k]

    def count(self):
        return len(self._results)

    def reset(self):
        self._results = []


def _chunk(doc_id, ordinal, text):
    return Chunk(
        chunk_id=make_chunk_id(doc_id, ordinal, text),
        doc_id=doc_id,
        ordinal=ordinal,
        text=text,
        word_count=len(text.split()),
        chunker_version="para-pack-v1;target=220w;cap=380w",
    )


def test_retrieve_node_writes_state_and_ids():
    c = _chunk("SYN-0001", 0, "some governed prose about monitoring")
    store = FakeStore([RetrievedChunk(chunk=c, score=0.12)])
    node = make_retrieve_node(store, manifest_version="test-v1", top_k=3)
    out = node({"query": "assess"})
    assert out["retrieved"][0]["chunk_id"] == c.chunk_id
    assert out["retrieved"][0]["doc_id"] == "SYN-0001"
    assert out["retrieved"][0]["score"] == 0.12
    assert out["retrieval_ms"] >= 0.0
    assert store.queries == [("assess", 3)]


def test_retrieve_node_empty_index_returns_empty_list():
    store = FakeStore([])
    node = make_retrieve_node(store, manifest_version="test-v1")
    out = node({"query": "assess"})
    assert out["retrieved"] == []


def test_retrieve_node_no_context_is_pure():
    # No governed_request active: the node must not raise and must not
    # require any governance plumbing to run.
    c = _chunk("SYN-0002", 1, "further governed prose")
    store = FakeStore([RetrievedChunk(chunk=c, score=0.3)])
    node = make_retrieve_node(store, manifest_version="test-v1")
    out = node({"query": "assess"})
    assert len(out["retrieved"]) == 1


def test_graph_default_is_stubbed_and_offline():
    g = build_graph()
    out = g.invoke({"query": "assess", "transaction": {}})
    assert out["retrieved"] == []
    assert out["retrieval_ms"] == -1.0
    assert out["score"] == -1.0


def test_graph_live_retrieval_requires_store_and_version():
    with pytest.raises(ValueError):
        build_graph(live_retrieval=True)
    with pytest.raises(ValueError):
        build_graph(live_retrieval=True, retrieval_store=FakeStore([]))


def test_graph_live_retrieval_with_fake_store_runs_end_to_end():
    c = _chunk("SYN-0003", 0, "prose the packaging stage will consume")
    store = FakeStore([RetrievedChunk(chunk=c, score=0.2)])
    g = build_graph(
        live_retrieval=True,
        retrieval_store=store,
        manifest_version="test-v1",
        retrieval_top_k=2,
    )
    out = g.invoke({"query": "assess", "transaction": {}})
    assert out["retrieved"][0]["chunk_id"] == c.chunk_id
    assert store.queries == [("assess", 2)]
