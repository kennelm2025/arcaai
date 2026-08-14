"""D2.1 — scenario spec schema conformance, v0.1 and v0.2.

Each schema file is the SOLE authority on what a valid spec of ITS
version is. The YAML files under
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

v0.2 ADDS ONE REQUIREMENT and must add no others. It makes
``retrieval_snapshot_sha256`` mandatory for retrieval-class scenarios.
Two guards below matter more than the positive case and are the reason
this file grew rather than a second file appearing. First, v0.1 must be
UNCHANGED — a retrieval spec without the pin still validates there, and
if that test ever fails an immutable schema has been edited. Second, the
new requirement must not reach scoring-class scenarios, which may pin a
corpus snapshot without ever querying an index; a schema that bound them
too would import the exact defect v0.1 forbids at ``generator_seed``.
Over-reach is invisible to a positive test, so it has its own fixture.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCHEMA_DIR = _REPO_ROOT / "arcaai" / "harness" / "schema"
_SCHEMA_PATHS = {
    "0.1": _SCHEMA_DIR / "scenario_spec_v0.1.schema.json",
    "0.2": _SCHEMA_DIR / "scenario_spec_v0.2.schema.json",
}
_VERSIONS = sorted(_SCHEMA_PATHS)
_FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _load_schema(version: str = "0.1") -> dict:
    return json.loads(_SCHEMA_PATHS[version].read_text(encoding="utf-8"))


def _load_fixture(name: str) -> dict:
    return yaml.safe_load((_FIXTURES / name).read_text(encoding="utf-8"))


def _errors(instance: dict, version: str | None = None) -> list:
    """All validation errors, deepest-first, for substance assertions.

    The schema is chosen from the instance's OWN declared version, which
    is what the runner does. A helper that validated every fixture against
    one hardcoded schema would put a v0.2 spec through v0.1's rules and
    then report the verdict confidently — the schema equivalent of
    checking the wrong subject and calling the answer green.
    """
    chosen = version or instance.get("schema_version", "0.1")
    validator = Draft202012Validator(_load_schema(chosen))
    return sorted(validator.iter_errors(instance), key=lambda e: str(e.json_path))


def _rules(instance: dict, version: str | None = None) -> set[str]:
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

    for err in _errors(instance, version):
        walk(err)
    return found


def _messages(instance: dict, version: str | None = None) -> str:
    parts: list[str] = []

    def walk(err) -> None:
        parts.append(f"{err.json_path}:{err.message}")
        for sub in err.context or []:
            walk(sub)

    for err in _errors(instance, version):
        walk(err)
    return " | ".join(parts)


# --------------------------------------------------------------- schema itself


@pytest.mark.parametrize("version", _VERSIONS)
def test_schema_is_itself_a_valid_2020_12_schema(version):
    """Before a schema can judge anything, it must be well-formed."""
    Draft202012Validator.check_schema(_load_schema(version))


@pytest.mark.parametrize("version", _VERSIONS)
def test_schema_is_closed_at_top_level(version):
    """additionalProperties false is load-bearing: an unknown field that
    validates is a spec whose hash does not describe what ran."""
    assert _load_schema(version)["additionalProperties"] is False


@pytest.mark.parametrize("version", _VERSIONS)
def test_schema_pins_its_own_version(version):
    """Each file declares the one version it judges, as a const.

    This is what makes cross-version validation impossible by accident
    rather than by convention: a spec routed to the wrong schema fails on
    this const before any other rule is reached.
    """
    assert _load_schema(version)["properties"]["schema_version"]["const"] == version


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


# ----------------------------------------- v0.2: the retrieval snapshot pin


def test_v0_1_still_accepts_a_retrieval_spec_without_the_pin():
    """THE IMMUTABILITY GUARD, and the most important test in this section.

    v0.1 is immutable once merged. If this ever fails, the v0.2 change was
    made by editing v0.1 rather than by adding a file — which is the one
    thing the prototype convention forbids outright, and which no amount
    of green elsewhere would make acceptable.
    """
    spec = copy.deepcopy(_load_fixture("valid_retrieval_gap_detection.yaml"))
    del spec["corpus_snapshot"]["retrieval_snapshot_sha256"]
    assert spec["schema_version"] == "0.1"
    assert _errors(spec) == [], _messages(spec)


def test_v0_2_accepts_a_retrieval_spec_carrying_the_pin():
    fixture = _load_fixture("valid_retrieval_v0_2_pinned.yaml")
    assert _errors(fixture) == [], _messages(fixture)


def test_v0_2_rejects_a_retrieval_spec_missing_the_pin():
    """The requirement itself, asserted by rule and by location.

    Asserting only that validation raised would pass equally if the spec
    failed for some unrelated reason, which is how a test comes to certify
    a rule it never exercised.
    """
    spec = _load_fixture("invalid_retrieval_v0_2_missing_snapshot_pin.yaml")
    assert _errors(spec), "v0.2 accepted a retrieval spec with no snapshot pin"
    assert "required" in _rules(spec)
    messages = _messages(spec)
    assert "retrieval_snapshot_sha256" in messages, messages
    assert "corpus_snapshot" in messages, messages


def test_v0_2_accepts_a_scoring_spec_pinning_a_snapshot_without_the_pin():
    """THE OVER-REACH GUARD. The requirement is retrieval-class only.

    A scoring-class scenario may legitimately pin a corpus snapshot — v0.1
    records it as one leg of the scoring reproducibility identity — and
    never queries an index. Requiring the retrieval pin there would be a
    pin describing something the scenario never touched, which is exactly
    what v0.1 forbids at generator_seed. A positive test cannot see this
    failure; only this fixture can.
    """
    fixture = _load_fixture("valid_scoring_v0_2_snapshot_unpinned.yaml")
    assert _errors(fixture) == [], _messages(fixture)


def test_v0_2_carries_forward_the_generator_seed_prohibition():
    """v0.2 adds one requirement and must relax nothing."""
    spec = copy.deepcopy(_load_fixture("valid_retrieval_v0_2_pinned.yaml"))
    spec["generator_seed"] = 1
    assert _errors(spec), "v0.2 accepted generator_seed on a retrieval spec"
    assert "generator_seed" in _messages(spec)


def test_v0_2_carries_forward_the_scoring_generator_seed_requirement():
    spec = copy.deepcopy(_load_fixture("valid_scoring_v0_2_snapshot_unpinned.yaml"))
    del spec["generator_seed"]
    assert _errors(spec), "v0.2 accepted a scoring spec with no generator_seed"
    assert "generator_seed" in _messages(spec)


def test_v0_2_rejects_a_spec_declaring_another_version():
    """Cross-version routing fails closed at the const, not silently.

    Validated against v0.2 explicitly rather than by the instance's own
    declaration, because the point is what happens when a spec reaches the
    wrong schema — which is the failure the runner's version selection
    exists to prevent, tested here at the schema layer.
    """
    spec = copy.deepcopy(_load_fixture("valid_retrieval_v0_2_pinned.yaml"))
    spec["schema_version"] = "0.1"
    errors = _errors(spec, version="0.2")
    assert errors, "v0.2 accepted a spec declaring a different version"
    assert "const" in _rules(spec, version="0.2")
    assert any(e.json_path == "$.schema_version" for e in errors), _messages(
        spec, version="0.2"
    )
