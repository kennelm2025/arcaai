"""B6 increment 4 tests: CI-safe units (prompt builder, validator,
stub-default graph) + self-skipping Ollama integration."""
import pytest

from agent.packaging import build_prompt, package_node, validate_prose

FIXTURE_STATE = {
    "query": "assess this transaction",
    "score": 0.9865,
    "provenance": {
        "sha256": "a" * 64,
        "platt_params": {"a": -1.0, "b": 0.5},
    },
}
SHA_PREFIX = "a" * 12


def test_build_prompt_embeds_facts():
    prompt = build_prompt(FIXTURE_STATE)
    assert "0.9865" in prompt
    assert SHA_PREFIX in prompt
    assert "yes" in prompt


def test_validate_rejects_missing_score():
    prose = (
        f"Note mentioning {SHA_PREFIX} only, padded out with enough "
        "additional words to comfortably pass the minimum length check."
    )
    with pytest.raises(ValueError, match="score"):
        validate_prose(prose, FIXTURE_STATE)


def test_validate_rejects_missing_sha():
    prose = (
        "The calibrated probability is 0.9865, padded out with enough "
        "additional words to comfortably pass the minimum length check."
    )
    with pytest.raises(ValueError, match="sha256"):
        validate_prose(prose, FIXTURE_STATE)


def test_stub_default_keeps_ci_offline():
    from agent.graph import build_graph
    g = build_graph()  # both flags False
    out = g.invoke({"query": "q", "transaction": {}})
    assert out["narrative"].startswith("[stub]")


def _ollama_has_model() -> bool:
    try:
        import ollama
        return any("llama3.1:8b" in m.model for m in ollama.list().models)
    except Exception:
        return False


@pytest.mark.skipif(not _ollama_has_model(), reason="Ollama/llama3.1:8b absent")
def test_package_node_live():
    out = package_node(FIXTURE_STATE)
    note = out["narrative"]
    assert "0.9865" in note
    assert SHA_PREFIX in note
    assert len(note.strip()) >= 80
