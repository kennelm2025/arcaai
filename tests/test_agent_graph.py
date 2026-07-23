"""B6 increment 2: graph mechanics tests. No LLM, no network - CI-safe."""
import pytest

from agent.graph import build_graph


def test_graph_end_to_end_stub():
    result = build_graph().invoke(
        {"query": "assess txn", "transaction": {"amount": 100.0}}
    )
    assert result["score"] == -1.0
    assert result["narrative"].startswith("[stub]")


def test_intake_rejects_empty_query():
    with pytest.raises(ValueError, match="empty query"):
        build_graph().invoke({"query": "", "transaction": {}})


def test_node_order_is_deterministic():
    compiled = build_graph()
    nodes = list(compiled.get_graph().nodes)
    assert nodes.index("intake") < nodes.index("score") < nodes.index("package")
