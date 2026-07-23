"""B6 increment 1: LLM smoke test (Llama 3.1 8B via local Ollama).

Skips cleanly when no Ollama server is reachable (CI has no GPU/Ollama;
this test is a local-environment gate, mirroring the promotion gate's
split between local and CI-side checks).

Model tag pinned per ruling TI7: llama3.1:8b. Re-pin via decision record only.
"""
import httpx
import pytest

OLLAMA_URL = "http://localhost:11434"
MODEL_TAG = "llama3.1:8b"  # TI7 pin


def _ollama_available() -> bool:
    try:
        return httpx.get(OLLAMA_URL, timeout=2.0).status_code == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _ollama_available(), reason="Ollama server not reachable (expected in CI)"
)


def test_llm_round_trip_exact():
    from langchain_ollama import ChatOllama

    model = ChatOllama(model=MODEL_TAG, temperature=0)
    reply = model.invoke("Reply with exactly: ARCAAI SMOKE OK")
    assert reply.content.strip() == "ARCAAI SMOKE OK"


def test_model_tag_present():
    tags = httpx.get(f"{OLLAMA_URL}/api/tags", timeout=5.0).json()
    names = [m["name"] for m in tags.get("models", [])]
    assert MODEL_TAG in names, f"TI7-pinned tag {MODEL_TAG} not in {names}"
