"""B6 increment 4: packaging node - Llama 3.1 8B (TI7) turns score +
provenance into governed analyst prose. Platform-side per ADR-0009;
imports nothing from verticals.*. Fail-loud: prose failing fact
validation raises ValueError - no fallback text (same philosophy as
the -1.0 score sentinel and the no-fallback-score rule in scoring).
"""
from langchain_ollama import ChatOllama

MODEL = "llama3.1:8b"

PROMPT_TEMPLATE = """You are a fraud-analysis assistant producing a short \
internal note for a bank analyst. Write 3-5 sentences of plain professional \
prose. State ONLY the facts below. Do not invent transaction details, \
customer information, amounts, or causes. Do not speculate. Do not \
include a To line, Subject line, salutation, or sign-off - body \
prose only.

Facts:
- Fraud probability (Platt-calibrated): {score}
- Model artifact sha256 (prefix): {sha_prefix}
- Calibration parameters present: {platt_present}

The note must quote the probability value {score} exactly as written, and \
must include the artifact prefix {sha_prefix} exactly as written."""


def build_prompt(state: dict) -> str:
    """Pure function - unit-testable without Ollama."""
    prov = state["provenance"]
    return PROMPT_TEMPLATE.format(
        score=f"{state['score']:.4f}",
        sha_prefix=prov["sha256"][:12],
        platt_present="yes" if prov.get("platt_params") else "no",
    )


def validate_prose(prose: str, state: dict) -> None:
    """Hallucination tripwire. Raises ValueError - no fallback prose."""
    score_str = f"{state['score']:.4f}"
    sha_prefix = state["provenance"]["sha256"][:12]
    if score_str not in prose:
        raise ValueError(
            f"packaging validation failed: score {score_str} "
            "absent from generated prose"
        )
    if sha_prefix not in prose:
        raise ValueError(
            f"packaging validation failed: sha256 prefix {sha_prefix} "
            "absent from generated prose"
        )
    if len(prose.strip()) < 80:
        raise ValueError("packaging validation failed: prose implausibly short")


def package_node(state: dict) -> dict:
    """Replaces package_stub when live_packaging=True. Writes `narrative`."""
    llm = ChatOllama(model=MODEL, temperature=0)
    prose = llm.invoke(build_prompt(state)).content
    validate_prose(prose, state)
    return {"narrative": prose}
