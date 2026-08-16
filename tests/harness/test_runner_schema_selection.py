"""D2.2a runner — schema selection by the spec's declared version.

THE RUNNER'S FIRST TEST COVERAGE. Until this file, ``arcaai/harness/
runner.py`` had none: grepping the test tree for the module or either of
its two entry functions returned nothing but an unrelated import-boundary
test. The runner was built under the D2.2a commissioning frame, where
results are permanently inadmissible, and commissioning explains why a
spike shipped without tests — it does not extend to a change made after
the spike, so the change that introduces v0.2 brings the coverage with
it.

WHAT THIS FILE IS FOR, and what it deliberately leaves alone. It covers
version dispatch only: which schema a given spec is judged by, and how
the runner refuses when it cannot tell. It does not touch retrieval,
the vector store, pin verification against a live manifest, or result
writing — those need an index and a corpus, and a test that quietly
acquired those dependencies would stop running in CI.

THE FAILURE THIS EXISTS TO PREVENT is specific. Each schema file pins
``schema_version`` with a const, so a v0.2 spec validated against the
v0.1 file is rejected — but rejected for the WRONG REASON, reported as a
malformed spec when the truth is a runner that cannot read that version.
A rejection naming the wrong cause is worse than no rejection: it sends
the reader to fix a spec that was correct all along.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from arcaai.harness.runner import (
    EXIT_SPEC_INVALID,
    SCHEMA_BY_VERSION,
    Refusal,
    load_and_validate_spec,
)

_FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _fixture(name: str) -> dict:
    return yaml.safe_load((_FIXTURES / name).read_text(encoding="utf-8"))


def _write(tmp_path, spec: dict, name: str = "spec.yaml"):
    path = tmp_path / name
    path.write_text(yaml.safe_dump(spec, sort_keys=False), encoding="utf-8")
    return path


# ------------------------------------------------------------- the mapping


def test_every_declared_version_maps_to_a_file_that_exists():
    """A mapping entry pointing at nothing would fail at read time, deep
    inside validation, as an unhandled OSError rather than a refusal."""
    assert SCHEMA_BY_VERSION, "the runner knows no schema versions at all"
    for version, path in SCHEMA_BY_VERSION.items():
        assert path.exists(), f"schema for version {version!r} missing at {path}"


def test_every_ruled_version_is_known():
    assert set(SCHEMA_BY_VERSION) >= {"0.1", "0.2", "0.3"}


def test_runner_and_suite_version_maps_agree():
    """The version-to-path mapping exists TWICE and must not drift.

    ``SCHEMA_BY_VERSION`` in the runner decides what actually gets
    validated; ``_SCHEMA_PATHS`` in the schema-conformance suite decides
    what the suite believes it validated. Adding a version to one and not
    the other produces a suite reporting green about a file the runner
    never reaches — a check whose stated subject is not its real subject,
    which is the defect family this repository names most often.

    The duplication is recorded rather than refactored away; this test is
    what makes the duplication safe until it is.
    """
    from tests.harness.test_scenario_spec_schema import _SCHEMA_PATHS

    assert dict(SCHEMA_BY_VERSION) == dict(_SCHEMA_PATHS), (
        "the runner's schema map and the suite's have diverged: "
        f"runner={sorted(SCHEMA_BY_VERSION)} suite={sorted(_SCHEMA_PATHS)}"
    )


# ------------------------------------------------------- dispatch, accepted


def test_v0_1_spec_is_accepted_and_judged_by_v0_1(tmp_path):
    """A v0.1 retrieval spec WITHOUT the snapshot pin still runs.

    This is the compatibility half of the immutability guarantee: v0.2
    tightened retrieval-class scenarios, and v0.1 specs must be unaffected
    by that. If this fails, existing specs were broken by a new file.
    """
    spec = _fixture("valid_retrieval_gap_detection.yaml")
    del spec["corpus_snapshot"]["retrieval_snapshot_sha256"]
    loaded, spec_sha = load_and_validate_spec(_write(tmp_path, spec))
    assert loaded["schema_version"] == "0.1"
    assert len(spec_sha) == 64


def test_v0_2_spec_with_the_pin_is_accepted(tmp_path):
    spec = _fixture("valid_retrieval_v0_2_pinned.yaml")
    loaded, _ = load_and_validate_spec(_write(tmp_path, spec))
    assert loaded["schema_version"] == "0.2"


# ------------------------------------------------------- dispatch, refusals


def test_v0_2_spec_missing_the_pin_is_refused_naming_its_own_version(tmp_path):
    """Refused as a v0.2 failure, not a v0.1 one.

    The version in the refusal is the assertion that matters: it is the
    only thing distinguishing 'your spec breaks the rule that applies to
    it' from 'your spec was judged by rules it never claimed'.
    """
    spec = _fixture("invalid_retrieval_v0_2_missing_snapshot_pin.yaml")
    with pytest.raises(Refusal) as excinfo:
        load_and_validate_spec(_write(tmp_path, spec))
    refusal = excinfo.value
    assert refusal.code == EXIT_SPEC_INVALID
    assert "v0.2" in str(refusal), str(refusal)
    assert any("retrieval_snapshot_sha256" in line for line in refusal.detail), (
        refusal.detail
    )


def test_missing_schema_version_is_refused_as_such(tmp_path):
    """No default is applied. A runner that picked one would be deciding
    which rules the spec was written against, on the spec's behalf."""
    spec = _fixture("valid_retrieval_v0_2_pinned.yaml")
    del spec["schema_version"]
    with pytest.raises(Refusal) as excinfo:
        load_and_validate_spec(_write(tmp_path, spec))
    assert excinfo.value.code == EXIT_SPEC_INVALID
    assert "no schema_version" in str(excinfo.value)


def test_unknown_schema_version_is_refused_as_unreadable_not_invalid(tmp_path):
    """The third outcome, kept distinct from the other two.

    An unknown version is not a malformed spec and must not read as one.
    The refusal names the versions the runner does know, so the reader
    learns whether to upgrade the runner or fix the spec.
    """
    spec = _fixture("valid_retrieval_v0_2_pinned.yaml")
    spec["schema_version"] = "9.9"
    with pytest.raises(Refusal) as excinfo:
        load_and_validate_spec(_write(tmp_path, spec))
    message = str(excinfo.value)
    assert excinfo.value.code == EXIT_SPEC_INVALID
    assert "9.9" in message
    assert "0.1" in message and "0.2" in message, message
    assert "not an invalid spec" in message, message


def test_scoring_class_is_refused_after_dispatch_not_before(tmp_path):
    """Order matters, and this is what pins it.

    The v0.2 scoring fixture is schema-VALID; the runner still refuses it,
    because only retrieval is implemented for D2.2a. A refusal mentioning
    scenario_class rather than schema failure proves the spec was
    dispatched to its schema and passed validation first. If dispatch had
    silently mis-routed it, this would fail as a schema error instead.
    """
    spec = _fixture("valid_scoring_v0_2_snapshot_unpinned.yaml")
    with pytest.raises(Refusal) as excinfo:
        load_and_validate_spec(_write(tmp_path, spec))
    message = str(excinfo.value)
    assert "scenario_class" in message, message
    assert "failed schema" not in message, message
