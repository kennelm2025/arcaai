"""B6 increment 2: minimal deterministic graph (stubs only, CI-safe).

intake -> score_stub -> package_stub. No LLM, no BentoML call: pure
graph mechanics. Increments 3-4 replace the stubs with the real fraud
scoring call (B5 BentoML service) and the Llama 3.1 8B packaging node.
A named slot is reserved for the injection detector (selection deferred
to B8 per ruling BA8/DP5) - not wired in v0.
"""
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

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
    # Replaced in inc 3 by the B5 BentoML fraud-scoring call.
    return {"score": -1.0}


def package_stub(state: AgentState) -> dict:
    # Replaced in inc 4 by the Llama 3.1 8B packaging node (TI7).
    return {"narrative": f"[stub] score={state['score']}"}


# Reserved node name for B8: "injection_check" (sits between START and
# intake when selected). Documented here so the slot survives review.

def build_graph(live_scoring: bool = False):
    g = StateGraph(AgentState)
    g.add_node("intake", intake)
    g.add_node("score", score_node if live_scoring else score_stub)
    g.add_node("package", package_stub)
    g.add_edge(START, "intake")
    g.add_edge("intake", "score")
    g.add_edge("score", "package")
    g.add_edge("package", END)
    return g.compile()
