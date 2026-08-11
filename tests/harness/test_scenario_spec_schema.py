"""D2.1 — scenario spec schema v0.1 conformance.

The schema at ``arcaai/harness/schema/scenario_spec_v0.1.schema.json``
is the SOLE authority on what a valid spec is. The YAML files under
``fixtures/`` carry no normative weight whatever: they are exercise
material, and they are safe to keep beside the schema only because CI
validates them on every run, so they cannot drift into a second,
silently-wrong account of the rules. Nothing here defines the schema;
everything here interrogates it.

The negative cases matter more than the positive ones. A schema that
accepts every valid spec but rejects nothing is the purest false green
available — it would report "spec schema-valid" while asserting almost
nothing, which is exactly the failure shape the check-method defect
family exists to name. So each rejection test asserts WHICH rule fired
and WHERE, not merely that validation raised.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCHEMA_PATH = (
    _REPO_ROOT / "arcaai" / "harness" / "schema" / "scenario_spec_v0.1.schema.json"
)
_FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _load_schema() -> dict:
    return json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))


def _load_fixture(name: str) -> dict:
    return yaml.safe_load((_FIXTURES / name).read_text(encoding="utf-8"))


def _errors(instance: dict) -> list:
    """All validation errors, deepest-first, for substance assertions."""
    validator = Draft202012Validator(_load_schema())
    return sorted(validator.iter_errors(instance), key=lambda e: str(e.json_path))


def _rules(instance: dict) -> set[str]:
    """The set of validation keywords that fired, including nested
    context from if/then and oneOf branches — a top-level allOf failure
    reports the branch generically, so the specific rule often lives in
    ``.context``."""
    found: set[str] = set()

    def walk(err) -> None:
        if err.validator is not None:
            found.add(str(err.validator))
        for sub in err.context or []:
            walk(sub)

    for err in _errors(instance):
        walk(err)
    return found


def _messages(instance: dict) -> str:
    parts: list[str] = []

    def walk(err) -> None:
        parts.append(f"{err.json_path}:{err.message}")
        for sub in err.context or []:
            walk(sub)

    for err in _errors(instance):
        walk(err)
    return " | ".join(parts)


# --------------------------------------------------------------- schema itself


def test_schema_is_itself_a_valid_2020_12_schema():
    """Before the schema can judge anything, it must be well-formed."""
    Draft202012Validator.check_schema(_load_schema())


def test_schema_is_closed_at_top_level():
    """additionalProperties false is load-bearing: an unknown field that
    validates is a spec whose hash does not describe what ran."""
    assert _load_schema()["additionalProperties"] is False


# ------------------------------------------------------------- accepts valid


@pytest.mark.parametrize(
    "fixture",
    ["valid_retrieval_gap_detection.yaml", "valid_scoring_typology.yaml"],
)
def test_valid_fixtures_validate(fixture):
    assert _errors(_load_fixture(fixture)) == [], _messages(_load_fixture(fixture))


def test_semantic_distance_retrieval_variant_validates():
    """Both retrieval scoring methods must be expressible at v0.1. The
    committed fixture exercises gap detection; this derives the
    semantic-distance form from it rather than committing a third file."""
    spec = copy.deepcopy(_load_fixture("valid_retrieval_gap_detection.yaml"))
    spec["retrieval"] = {
        "retrieval_kind": "corpus_qa",
        "query": spec["retrieval"]["query"],
        "top_k": 5,
        "expected_document_ids": ["FIXTURE-0004"],
        "scoring_method": "semantic_distance",
    }
    spec["acceptance"] = {"metric": "recall_at_k", "operator": ">=", "value": 0.9}
    assert _errors(spec) == [], _messages(spec)


# ------------------------------------------------------------ rejects invalid


def test_scoring_class_without_generator_seed_is_rejected():
    """Amendment 6: generator_seed is mandatory for scoring-class
    scenarios. Its absence must hard-reject, not warn."""
    spec = _load_fixture("invalid_scoring_missing_generator_seed.yaml")
    assert _errors(spec), "schema accepted a scoring spec with no generator_seed"
    assert "required" in _rules(spec)
    assert "generator_seed" in _messages(spec)


def test_unknown_scenario_class_is_rejected():
    """The class set is closed at v0.1. A third class arrives by a new
    schema version, never by a spec asserting one."""
    spec = _load_fixture("invalid_unknown_scenario_class.yaml")
    errors = _errors(spec)
    assert errors, "schema accepted a scenario of neither ruled class"
    assert "enum" in _rules(spec)
    assert any(e.json_path == "$.scenario_class" for e in errors), _messages(spec)


def test_wrong_typed_top_k_is_rejected():
    """top_k is arithmetic — every scoring formula is evaluated over the
    top-k set — so a string must fail at the gate, not inside scoring."""
    spec = _load_fixture("invalid_wrong_typed_top_k.yaml")
    errors = _errors(spec)
    assert errors, "schema accepted a non-integer retrieval cut-off"
    assert "type" in _rules(spec)
    assert any(
        e.json_path == "$.retrieval.top_k" for e in errors
    ), _messages(spec)


def test_retrieval_class_carrying_generator_seed_is_rejected():
    """Amendment 6's other side: retrieval scenarios do not invoke the
    generator, so a seed recorded against one is a reproducibility claim
    with nothing behind it."""
    spec = copy.deepcopy(_load_fixture("valid_retrieval_gap_detection.yaml"))
    spec["generator_seed"] = 1
    assert _errors(spec), "schema accepted generator_seed on a retrieval spec"
    assert "generator_seed" in _messages(spec)


def test_tolerance_comparison_without_tolerance_block_is_rejected():
    """Amendment 3: a scenario declaring tolerance comparison must state
    the tolerance, or the migration diff has no rule to apply."""
    spec = copy.deepcopy(_load_fixture("valid_scoring_typology.yaml"))
    spec["migration_diff"] = {"comparison": "tolerance"}
    assert _errors(spec), "schema accepted tolerance comparison with no bounds"
    assert "required" in _rules(spec)
    assert "tolerance" in _messages(spec)


def test_bit_identical_comparison_carrying_tolerance_is_rejected():
    """The contradiction is rejected rather than resolved by precedence:
    a bit-identical claim plus a tolerance is two different rules."""
    spec = copy.deepcopy(_load_fixture("valid_scoring_typology.yaml"))
    spec["migration_diff"] = {
        "comparison": "bit_identical",
        "tolerance": {"metric": "roc_auc", "max_abs_delta": 0.01},
    }
    assert _errors(spec), "schema accepted bit_identical with a tolerance block"
