"""B6 increments 2-4 + B7 inc4: agent graph.
intake -> score -> retrieve -> package.

Increment 2 laid the deterministic stub-only skeleton (CI-safe).
Increment 3 added the real fraud scoring call (B5 BentoML service,
live_scoring flag). Increment 4 added the Llama 3.1 8B packaging node
(TI7, live_packaging flag). B7 inc4 adds the retrieve node
(live_retrieval flag) between score and package: retrieval is placed
after scoring so the query can later be composed from what scoring
established, and before packaging because the narrative is the
consumer. Defaults keep CI fully stubbed and offline.
A named slot is reserved for the injection detector (selection deferred
to B8 per ruling BA8/DP5) - not wired in v0.
"""
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from agent.packaging import package_node
from agent.retrieval import make_retrieve_node
from agent.scoring import score_node


class AgentState(TypedDict):
    query: str
    transaction: dict
    score: float
    provenance: dict
    retrieved: list
    retrieval_ms: float
    narrative: str


def intake(state: AgentState) -> dict:
    if not state.get("query"):
        raise ValueError("empty query")
    return {}


def score_stub(state: AgentState) -> dict:
    # Replaced by agent.scoring.score_node when live_scoring=True.
    return {"score": -1.0}


def retrieve_stub(state: AgentState) -> dict:
    # Replaced by agent.retrieval.make_retrieve_node(...) when
    # live_retrieval=True. Sentinel latency, same convention as the
    # -1.0 score sentinel.
    return {"retrieved": [], "retrieval_ms": -1.0}


def package_stub(state: AgentState) -> dict:
    # Replaced by agent.packaging.package_node when live_packaging=True.
    return {"narrative": f"[stub] score={state['score']}"}


# Reserved node name for B8: "injection_check" (sits between START and
# intake when selected). Documented here so the slot survives review.

def build_graph(
    live_scoring: bool = False,
    live_packaging: bool = False,
    live_retrieval: bool = False,
    retrieval_store=None,
    manifest_version: str | None = None,
    retrieval_top_k: int = 5,
):
    if live_retrieval:
        if retrieval_store is None or manifest_version is None:
            raise ValueError(
                "live_retrieval=True requires retrieval_store and "
                "manifest_version (composition-root concerns; the graph "
                "never guesses either)"
            )
        retrieve = make_retrieve_node(
            retrieval_store,
            manifest_version=manifest_version,
            top_k=retrieval_top_k,
        )
    else:
        retrieve = retrieve_stub

    g = StateGraph(AgentState)
    g.add_node("intake", intake)
    g.add_node("score", score_node if live_scoring else score_stub)
    g.add_node("retrieve", retrieve)
    g.add_node("package", package_node if live_packaging else package_stub)
    g.add_edge(START, "intake")
    g.add_edge("intake", "score")
    g.add_edge("score", "retrieve")
    g.add_edge("retrieve", "package")
    g.add_edge("package", END)
    return g.compile()
