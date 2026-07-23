"""B6 increments 2-4: agent graph. intake -> score -> package.

Increment 2 laid the deterministic stub-only skeleton (CI-safe).
Increment 3 added the real fraud scoring call (B5 BentoML service,
live_scoring flag). Increment 4 adds the Llama 3.1 8B packaging node
(TI7, live_packaging flag). Defaults keep CI fully stubbed and offline.
A named slot is reserved for the injection detector (selection deferred
to B8 per ruling BA8/DP5) - not wired in v0.
"""
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from agent.packaging import package_node
from agent.scoring import score_node


class AgentState(TypedDict):
    query: str
    transaction: dict
    score: float
    provenance: dict
    narrative: str


def intake(state: AgentState) -> dict:
    if not state.get("query"):
        raise ValueError("empty query")
    return {}


def score_stub(state: AgentState) -> dict:
    # Replaced by agent.scoring.score_node when live_scoring=True.
    return {"score": -1.0}


def package_stub(state: AgentState) -> dict:
    # Replaced by agent.packaging.package_node when live_packaging=True.
    return {"narrative": f"[stub] score={state['score']}"}


# Reserved node name for B8: "injection_check" (sits between START and
# intake when selected). Documented here so the slot survives review.

def build_graph(live_scoring: bool = False, live_packaging: bool = False):
    g = StateGraph(AgentState)
    g.add_node("intake", intake)
    g.add_node("score", score_node if live_scoring else score_stub)
    g.add_node("package", package_node if live_packaging else package_stub)
    g.add_edge(START, "intake")
    g.add_edge("intake", "score")
    g.add_edge("score", "package")
    g.add_edge("package", END)
    return g.compile()
