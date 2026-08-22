"""Environment-identity surface on the ChromaDB adapter — queue item 36(a).

Before this surface existed, ``read_material_parameters`` found no
``collection_metadata`` on ``ChromaStore`` and four of the five material
parameters read UNKNOWN on every run: the environment identity was honest but
partial, and the queue item recorded it as such. (The queue text says three;
reading the code showed four, ``distance_space`` included. That correction is
owed against the record and is not made here.)

Design fork (iii) as ruled 2026-08-22: SET the index parameters at collection
construction, then READ BACK from the live collection and report the read-back.
The tests below exist to hold the two halves apart, because a surface that
echoes what it was handed passes a naive test just as well as one that reads —
and the difference is the whole point of the fork.

Tests inject a deterministic embedding function, following the inc2 pattern, so
the suite runs offline with no model download.
"""

from __future__ import annotations

import hashlib
import math

from arcaai.harness import runner as R
from arcaai.platform.retrieval.chroma_store import (
    _INDEX_PARAMETERS,
    EMBEDDING_MODEL,
    ChromaStore,
)

MATERIAL_INDEX_NAMES = (
    "distance_space",
    "hnsw_construction_ef",
    "hnsw_m",
    "hnsw_ef_search",
)


class HashEmbedding:
    """Deterministic 16-dim embedding — the inc2 helper, repeated rather than
    imported so this file does not depend on another suite's internals."""

    def __call__(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for text in texts:
            digest = hashlib.sha256(text.encode("utf-8")).digest()
            vec = [b / 255.0 for b in digest[:16]]
            norm = math.sqrt(sum(v * v for v in vec)) or 1.0
            vectors.append([v / norm for v in vec])
        return vectors


def make_store(collection_name: str = "test_env_identity") -> ChromaStore:
    return ChromaStore(
        collection_name=collection_name,
        embedding_function=HashEmbedding(),
    )


# ------------------------------------------------------- T1 exposure surface


def test_adapter_exposes_material_parameters_keyed_for_the_runner() -> None:
    """The surface exists and is keyed by the runner's MATERIAL_PARAMETERS
    names, not by chromadb's vocabulary. The runner keys on its own names; a
    dict keyed ``hnsw:M`` or ``max_neighbors`` would read as absent and every
    parameter would stay UNKNOWN while looking exposed."""
    store = make_store()
    metadata = store.collection_metadata

    assert isinstance(metadata, dict)
    for name in MATERIAL_INDEX_NAMES:
        assert name in metadata, f"{name} absent from the identity surface"
    assert metadata["embedding_model"] == EMBEDDING_MODEL
    assert set(metadata) <= set(R.MATERIAL_PARAMETERS)


# --------------------------------------------------- T2 read-back, not echo


def test_values_are_read_back_from_the_index_not_echoed_from_the_declaration()\
        -> None:
    """The fork-(iii) test, and the one a fork-(ii) implementation fails.

    A pre-existing collection keeps its own index configuration: chromadb
    ignores construction parameters when the collection already exists. So a
    second adapter opening the same collection while DECLARING different values
    must still report the values in force, not the ones it asked for. An
    implementation echoing ``collection.metadata`` — or returning
    ``_INDEX_PARAMETERS`` directly — reports the declaration and fails here.
    """
    name = "test_env_identity_readback"
    first = make_store(name)
    first.reset()
    baseline = first.collection_metadata

    # Open the SAME collection through an adapter whose declared parameters
    # differ from what the collection was built with.
    import arcaai.platform.retrieval.chroma_store as CS

    original = dict(CS._INDEX_PARAMETERS)
    try:
        CS._INDEX_PARAMETERS.update(
            {"hnsw:construction_ef": 321, "hnsw:M": 47, "hnsw:search_ef": 91}
        )
        second = ChromaStore(
            collection_name=name, embedding_function=HashEmbedding()
        )
        reported = second.collection_metadata
    finally:
        CS._INDEX_PARAMETERS.clear()
        CS._INDEX_PARAMETERS.update(original)

    assert reported == baseline, (
        "identity surface changed with the DECLARATION while the index did "
        "not change — the values are being echoed, not read back"
    )
    assert reported["hnsw_construction_ef"] != "321"
    assert reported["hnsw_m"] != "47"
    assert reported["hnsw_ef_search"] != "91"


def test_set_values_are_the_ones_actually_in_force_on_a_fresh_collection()\
        -> None:
    """The other half of the fork: the SET must actually take on a collection
    that does not yet exist, or the pinning half buys nothing. Read back and
    compare against what was declared, mapping chromadb's two vocabularies."""
    store = make_store("test_env_identity_fresh")
    store.reset()
    metadata = store.collection_metadata

    assert metadata["distance_space"] == str(_INDEX_PARAMETERS["hnsw:space"])
    assert metadata["hnsw_construction_ef"] == str(
        _INDEX_PARAMETERS["hnsw:construction_ef"]
    )
    assert metadata["hnsw_m"] == str(_INDEX_PARAMETERS["hnsw:M"])
    assert metadata["hnsw_ef_search"] == str(_INDEX_PARAMETERS["hnsw:search_ef"])


# ------------------------------------------- T3 three-outcome survives this


def test_unreadable_configuration_yields_omission_and_never_a_default() -> None:
    """A parameter that cannot be read is OMITTED, so the runner's UNKNOWN
    stands. The failure this guards is a default substituted for a reading,
    which makes two genuinely different environments hash identically."""

    class Broken:
        @property
        def configuration_json(self):
            raise RuntimeError("configuration unavailable")

    store = make_store("test_env_identity_broken")
    store._collection = Broken()
    metadata = store.collection_metadata

    for name in MATERIAL_INDEX_NAMES:
        assert name not in metadata, f"{name} supplied despite unreadable config"

    values = R.read_material_parameters(store, "pinned-model")
    unknown = [n for n, v in values.items() if v == R.UNKNOWN]
    for name in MATERIAL_INDEX_NAMES:
        assert name in unknown


def test_partial_configuration_reports_what_it_has_and_omits_the_rest() -> None:
    """Three outcomes, not two: a config carrying some keys reports those and
    stays silent on the others rather than defaulting them."""

    class Partial:
        configuration_json = {"hnsw": {"space": "cosine", "ef_search": 77}}

    store = make_store("test_env_identity_partial")
    store._collection = Partial()
    metadata = store.collection_metadata

    assert metadata["distance_space"] == "cosine"
    assert metadata["hnsw_ef_search"] == "77"
    assert "hnsw_construction_ef" not in metadata
    assert "hnsw_m" not in metadata


# ----------------------------------------------- T4 the hash actually moves


def test_environment_hash_moves_when_a_material_parameter_moves() -> None:
    """Without this the identity is decorative. Two environments differing in
    one material parameter must not hash alike."""
    store = make_store("test_env_identity_hash")
    list_sha = "c" * 64

    baseline = R.read_material_parameters(store, EMBEDDING_MODEL)
    moved = dict(baseline)
    moved["hnsw_ef_search"] = str(int(baseline["hnsw_ef_search"]) + 1)

    assert R.environment_config_sha256(
        baseline, list_sha
    ) != R.environment_config_sha256(moved, list_sha)


def test_unknown_and_read_do_not_collide_in_the_hash() -> None:
    """An UNKNOWN parameter must not hash as though it had been read with some
    value — otherwise a partial identity could impersonate a complete one."""
    store = make_store("test_env_identity_unknown_hash")
    read = R.read_material_parameters(store, EMBEDDING_MODEL)

    class Nothing:
        pass

    unknown = R.read_material_parameters(Nothing(), EMBEDDING_MODEL)
    assert R.environment_config_sha256(
        read, "d" * 64
    ) != R.environment_config_sha256(unknown, "d" * 64)


# ------------------------------------ T5 distance_space from the read surface


def test_query_reports_distance_space_from_the_surface_not_a_literal() -> None:
    """The retired literal. ``metadata={"distance_space": "l2", ...}`` was an
    assertion about the index rather than a reading of it — correct only while
    the collection used chromadb's default space, and silently wrong the moment
    it did not. The reported space must track the surface."""
    from arcaai.platform.retrieval import chunk_document

    store = make_store("test_env_identity_query")
    store.reset()
    store.add_chunks(chunk_document("SYN-TR-01", "alpha bravo charlie " * 40))

    results = store.query("alpha bravo", top_k=1)
    assert results, "expected at least one result to inspect"
    reported = results[0].metadata["distance_space"]

    assert reported == store.collection_metadata["distance_space"]
    assert results[0].metadata["store"] == "chromadb"
