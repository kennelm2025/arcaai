"""Runner conformance to the accepted D1.1 Test Plan Rev C (queue item 36).

WHAT THIS COVERS. Rev C was ACCEPTED on 2026-08-16 and imposes obligations on
the runner build that the D2.2a spike predates. Queue item 36 confirmed six
fields ABSENT from the emitted result artefact by reading its keys, and a
seventh element was added when v0.3 landed: the load-time comparison of
``top_k`` against the scenario's own recorded cap. One test per element,
minimum, each naming the clause it implements.

WHAT THIS DELIBERATELY DOES NOT DO, following the discipline of
``test_runner_schema_selection.py``: it touches no vector store, no live
corpus and no index. Every element here is tested through a pure function or a
file write, so the suite keeps running in CI. The consequence is stated rather
than hidden — these tests prove the elements are COMPUTED CORRECTLY, not that
``run_scenario`` wires each into the result dict, which needs an index and
belongs to an integration test this increment does not add.
"""

from __future__ import annotations

import json

import pytest

from arcaai.harness import runner as R

# --------------------------------------------- C1 — §6.8.1 evaluator_version


def test_evaluator_version_exists_and_is_separate_from_the_runner_version():
    """Rev C §6.8.1 — the identity's FOURTH leg.

    The clause is explicit that evaluation logic is versioned INDEPENDENTLY of
    the runner, and that the runner version is deliberately NOT an identity
    leg. Two separate module attributes is the whole mechanism: a single
    constant used for both would mean a runner release that never touched
    evaluation still presented as an evaluator change, and — worse in the other
    direction — an evaluator change inside an unchanged runner release could
    hide behind an unmoved version string.
    """
    assert R.EVALUATOR_VERSION, "no evaluator version is declared"
    assert R.RUNNER_VERSION, "no runner version is declared"
    assert "EVALUATOR_VERSION" in vars(R), "evaluator version is not a module constant"
    assert "RUNNER_VERSION" in vars(R)


def test_halt_record_carries_the_evaluator_version(tmp_path):
    """The fourth leg travels on every artefact the runner writes, including
    the one written when a session does not finish."""
    path = R.write_halt_record(tmp_path, tmp_path / "spec.yaml", "test reason")
    record = json.loads(path.read_text(encoding="utf-8"))
    assert record["evaluator_version"] == R.EVALUATOR_VERSION


# ------------------------- C3 — §9.5 element 3, material_parameter_list_sha256


def test_material_parameter_list_includes_a_search_time_parameter():
    """Rev C §9.5 element 3, and the one membership question that was actually
    contested.

    DeepSeek's delta return held that the named list must include SEARCH-TIME
    parameters and not only index-build ones. The D2.2a spike's own list v0.1,
    authored the same day without sight of that return, independently carried
    ``hnsw_ef_search``. Two readings, one membership — this test is what stops
    a later tidy-up dropping it back to build-time parameters.
    """
    assert "hnsw_ef_search" in R.MATERIAL_PARAMETERS, (
        "the named list has lost its search-time parameter; §9.5 element 3 "
        f"is not satisfied by build-time parameters alone: {R.MATERIAL_PARAMETERS}"
    )


def test_material_parameter_list_hash_is_over_the_list_not_its_values():
    """The list carries its OWN hash, separate from the environment hash.

    They answer different questions: this one moves when the definition of
    'material' changes, the environment hash when the environment does.
    """
    first = R.material_parameter_list_sha256()
    assert len(first) == 64 and int(first, 16) >= 0
    assert first == R.material_parameter_list_sha256(), "list hash is not stable"


def test_material_parameter_list_hash_moves_when_the_list_changes(monkeypatch):
    """A widened or narrowed definition of 'material' must be visible.

    If this hash did not move, a list amendment would be indistinguishable
    from no change at all, and the list could be quietly narrowed to whatever
    the environment happened to expose.
    """
    before = R.material_parameter_list_sha256()
    monkeypatch.setattr(R, "MATERIAL_PARAMETERS", R.MATERIAL_PARAMETERS + ("added",))
    assert R.material_parameter_list_sha256() != before


# --------------------- C2 — §8.1 criterion 7, environment_config_sha256


def test_environment_hash_moves_with_the_values():
    """Rev C §8.1 criterion 7 — the environment identity tracks the values."""
    list_sha = R.material_parameter_list_sha256()
    a = R.environment_config_sha256({"embedding_model": "m1"}, list_sha)
    b = R.environment_config_sha256({"embedding_model": "m2"}, list_sha)
    assert a != b
    assert len(a) == 64


def test_environment_hash_moves_with_the_list_hash_too():
    """Criterion 7 names BOTH inputs, and the second is the load-bearing one.

    Over the values alone, adding a parameter to the named list would leave the
    hash unchanged whenever that parameter happened to be absent — a widened
    definition of 'material' that no instrument could detect. Including the
    list hash makes a definition change move the environment identity.
    """
    values = {"embedding_model": "m1"}
    assert R.environment_config_sha256(values, "a" * 64) != R.environment_config_sha256(
        values, "b" * 64
    )


def test_unreadable_parameters_record_UNKNOWN_and_never_a_default():
    """The three-outcome discipline, at the level that matters most here.

    A default recorded as though it had been read makes two environments that
    genuinely differ hash identically — the single failure an environment
    identity exists to prevent. A store exposing nothing must therefore produce
    UNKNOWNs, not a plausible-looking set of standard values.
    """

    class StoreExposingNothing:
        pass

    values = R.read_material_parameters(StoreExposingNothing(), "pinned-model")
    assert values["embedding_model"] == "pinned-model"
    unknown = [n for n, v in values.items() if v == R.UNKNOWN]
    assert "hnsw_ef_search" in unknown
    assert all(v == R.UNKNOWN for n, v in values.items() if n != "embedding_model")


def test_exposed_parameters_are_read_rather_than_assumed():
    """The other half: where the adapter DOES expose a parameter, the live
    value is used. Without this, the UNKNOWN test above would also pass on a
    reader that never read anything."""

    class StoreExposingMetadata:
        collection_metadata = {"distance_space": "l2", "hnsw_ef_search": 40}

    values = R.read_material_parameters(StoreExposingMetadata(), "pinned-model")
    assert values["distance_space"] == "l2"
    assert values["hnsw_ef_search"] == "40"


# ------------------------------------------- C4 — §12.3, confound single_chunk


def _manifest(docs):
    return {"documents": docs}


def test_single_chunk_expected_document_is_detected():
    """Rev C §12.3 — a result whose expected grounding set includes a
    single-chunk document carries ``confound: single_chunk``.

    Rev A required this at prose level only, with no field and no check, so
    omission was undetectable. Computing it from the manifest is what makes the
    confound real rather than a matter of author diligence.
    """
    manifest = _manifest(
        [
            {"id": "OGL-0001", "processing": {"chunk_count": 1}},
            {"id": "SYN-0002", "processing": {"chunk_count": 6}},
        ]
    )
    assert R.single_chunk_expected_documents(manifest, ["OGL-0001", "SYN-0002"]) == [
        "OGL-0001"
    ]


def test_no_confound_when_every_expected_document_is_multi_chunk():
    manifest = _manifest([{"id": "SYN-0002", "processing": {"chunk_count": 6}}])
    assert R.single_chunk_expected_documents(manifest, ["SYN-0002"]) == []


def test_expected_document_absent_from_the_manifest_is_not_called_single_chunk():
    """Unknown is not one. Treating a missing document as single-chunk would
    manufacture a confound out of a corpus bookkeeping error."""
    manifest = _manifest([{"id": "SYN-0002", "processing": {"chunk_count": 6}}])
    assert R.single_chunk_expected_documents(manifest, ["NOT-IN-MANIFEST"]) == []


# ------------------------------------------------ C5 — §8.3, session_status


def test_halted_is_a_distinct_class_from_refusal():
    """Rev C §8.3. A refusal happens BEFORE anything ran and writes no
    artefact; a halt happens DURING a run and must record partial work. One
    class for both would either discard a partial result or dress a refusal up
    as one."""
    assert not issubclass(R.Halted, R.Refusal)
    assert R.EXIT_HALTED != R.EXIT_OK


def test_halt_record_states_halted_status_reason_and_inadmissibility(tmp_path):
    """Partial results are RECORDED, not discarded, and are inadmissible for
    any purpose other than diagnosing the suspension."""
    path = R.write_halt_record(tmp_path, tmp_path / "s.yaml", "SIGTERM received mid-run")
    record = json.loads(path.read_text(encoding="utf-8"))
    assert record["session_status"] == "halted"
    assert record["halt_reason"] == "SIGTERM received mid-run"
    assert "diagnosing the suspension" in record["partial_result_admissibility"]
    assert "not resumption" in record["partial_result_admissibility"]


# -------------------------------------------- C6 — §9.8, invalidation_status


def test_invalidation_status_is_emitted_as_a_filterable_scalar(tmp_path):
    """Rev C §9.8 — the D2.5 ledger field, on which gate-evaluation and
    pre-flight tooling MUST filter.

    A scalar rather than a structure, because a field that must be filtered on
    has to be comparable. The caveat about the controlled vocabulary lives in
    an adjacent note field so it is visible without making the field itself
    unfilterable.
    """
    path = R.write_halt_record(tmp_path, tmp_path / "s.yaml", "reason")
    record = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(record["invalidation_status"], str)
    assert record["invalidation_status"] == "none_recorded"


# -------------------------------- C7 — §5.4/§5.5, top_k against the absolute cap


def _retrieval_spec(top_k, cap=None):
    block = {"top_k": top_k}
    if cap is not None:
        block["top_k_absolute_cap"] = cap
    return {"retrieval": block}


def test_top_k_within_its_cap_is_accepted_and_returns_the_cap():
    """Rev C §5.4 — the cap is recorded on every v0.3 scenario."""
    assert R.check_top_k_against_cap(_retrieval_spec(5, cap=7)) == 7


def test_top_k_exceeding_its_own_cap_is_refused_in_its_own_class():
    """The comparison JSON Schema cannot make.

    v0.3 records ``top_k_absolute_cap`` as a required field, but a schema
    cannot compare two sibling values, so a spec whose ``top_k`` exceeds its
    own cap validates cleanly. The runner is the only place the comparison can
    happen. It gets its own exit class because the spec is schema-VALID —
    reporting it as malformed would send the reader hunting a structural fault
    that does not exist.
    """
    with pytest.raises(R.Refusal) as excinfo:
        R.check_top_k_against_cap(_retrieval_spec(9, cap=7))
    refusal = excinfo.value
    assert refusal.code == R.EXIT_CAP_BREACH
    assert refusal.code != R.EXIT_SPEC_INVALID
    assert "§5.5" in str(refusal), "the ruled-variance route is not named"


def test_absent_cap_returns_none_rather_than_passing_silently():
    """v0.1 and v0.2 specs carry no cap and remain runnable.

    None is returned rather than a permissive sentinel so the result artefact
    can distinguish 'no cap recorded' from 'cap recorded and honoured' — absent
    and satisfied must not look alike.
    """
    assert R.check_top_k_against_cap(_retrieval_spec(50)) is None
