"""CF-1/B7-c events-present leg, DB-backed: retrieval_performed is
recorded for a governed end-to-end graph run and carries the
eligibility-at-decision fields.

The audit store fixture is the app-role AuditStore from conftest -
the same grants path production takes. The retrieval store is an
owned fake (WS-E 57 discipline): chromadb plays no part here; the
adapter's own behaviour is covered by the retrieval suite.
"""
from agent.graph import build_graph
from arcaai.platform.governance.wrapper import governed_request
from arcaai.platform.retrieval import (
    Chunk,
    RetrievalStore,
    RetrievedChunk,
    make_chunk_id,
)


class _FakeStore(RetrievalStore):
    def __init__(self, results):
        self._results = results

    def add_chunks(self, chunks):
        return 0

    def query(self, text, top_k=5):
        return self._results[:top_k]

    def count(self):
        return len(self._results)

    def reset(self):
        self._results = []


def test_retrieval_performed_emitted_for_governed_run(store):
    text_ = "governed prose for the wiring test"
    chunk = Chunk(
        chunk_id=make_chunk_id("SYN-0001", 0, text_),
        doc_id="SYN-0001",
        ordinal=0,
        text=text_,
        word_count=6,
        chunker_version="para-pack-v1;target=220w;cap=380w",
    )
    fake = _FakeStore([RetrievedChunk(chunk=chunk, score=0.1)])
    graph = build_graph(
        live_retrieval=True,
        retrieval_store=fake,
        manifest_version="test-v1",
    )

    with governed_request(
        store,
        source="test_retrieval_wiring",
        corpus_version="test-v1",
        retrieval_config={"top_k": 5},
    ) as ctx:
        out = graph.invoke({"query": "assess", "transaction": {}})
        correlation_id = ctx.correlation_id

    events = store.events_for_run(correlation_id)
    retrievals = [
        e for e in events if e.event_type == "retrieval_performed"
    ]
    assert len(retrievals) == 1, (
        "exactly one retrieval_performed expected for a single-retrieve "
        f"run; got {len(retrievals)}"
    )
    payload = retrievals[0].payload
    assert payload["manifest_version"] == "test-v1"
    assert payload["chunk_ids"] == [chunk.chunk_id]
    assert payload["top_k"] == 5
    assert payload["result_count"] == 1
    # State and record agree on the grounding chain.
    assert out["retrieved"][0]["chunk_id"] == chunk.chunk_id
