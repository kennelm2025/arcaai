"""B7 inc4: retrieval node - grounds the agent run in the governed
corpus and emits retrieval_performed through the governed context.

Depends on the RetrievalStore ABC only (ADR-0009; CF-1/B7-a) -
constructing a concrete adapter is a composition-root concern
(scripts/b7_run.py in the reference build). Emission follows the
RAT-02 node pattern (wrapper.py docstring): the node reaches the
active GovernedContext via current_governed_context() and emits a
typed event; with no active context (stubbed CI, unit tests) it emits
nothing and stays pure.

Latency is written to state (retrieval_ms) for CF-1/B7-d
transcription into B7_GATE - recorded, not gated, and deliberately
NOT an event field: adding one to RetrievalPerformed is a minor
schema version bump per events.py section 6.2, and the gate doc, not
the audit record, is where a measured-not-gated number belongs.
"""
from __future__ import annotations

import time
from collections.abc import Callable

from arcaai.platform.governance.events import RetrievalPerformed
from arcaai.platform.governance.wrapper import current_governed_context
from arcaai.platform.retrieval import RetrievalStore


def make_retrieve_node(
    store: RetrievalStore,
    *,
    manifest_version: str,
    top_k: int = 5,
) -> Callable[[dict], dict]:
    """Build the live retrieve node over an injected store.

    manifest_version is the corpus manifest version the store was
    loaded from - carried into every retrieval_performed event so the
    record answers eligibility-at-decision (events.py, B7 consumer
    note). The caller pins it at composition time; the node never
    guesses it.
    """

    def retrieve_node(state: dict) -> dict:
        t0 = time.perf_counter()
        results = store.query(state["query"], top_k=top_k)
        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        retrieved = [
            {
                "chunk_id": rc.chunk.chunk_id,
                "doc_id": rc.chunk.doc_id,
                "text": rc.chunk.text,
                "score": rc.score,
            }
            for rc in results
        ]

        ctx = current_governed_context()
        if ctx is not None:
            ctx.emit(
                RetrievalPerformed(
                    chunk_ids=[r["chunk_id"] for r in retrieved],
                    manifest_version=manifest_version,
                    top_k=top_k,
                    result_count=len(retrieved),
                )
            )

        return {"retrieved": retrieved, "retrieval_ms": elapsed_ms}

    return retrieve_node
