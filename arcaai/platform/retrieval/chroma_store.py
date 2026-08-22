"""ChromaDB adapter — the ONLY module in the repository permitted to
import chromadb (CF-1/B7-a; enforced by
tests/retrieval/test_retrieval_inc1.py::test_chromadb_imported_only_in_allowlisted_adapter).

Store relationship (CF-1/B7-a written statement): ChromaDB serves the
reference build; R5 fixes self-managed on-premises OpenSearch for
Phase 2 deployment because rm_knowledge holds customer data. Both hold
simultaneously: the platform contract is
arcaai.platform.retrieval.interface.RetrievalStore, this module is one
adapter behind it, and the Phase 2 move is a second adapter — a swap,
not a rewrite. No code outside this module may depend on chromadb
types, exceptions or behaviour.

Embedding function (B7_GATE §2.1): chromadb's default embedding
function silently downloads an ONNX MiniLM model at first ``add()`` —
an unpinned model entering the pipeline as actual-not-intended, and a
network event inside the R7 latency path. This adapter NEVER invokes
the default. The embedding function is constructed explicitly and
pinned by name and packaging version (EMBEDDING_MODEL below, recorded
per document in the manifest's processing fields per DEC-0014, feeding
retrieval_snapshot_sha256). Construction performs a warm-up embed so
any first-use model download happens at adapter initialisation —
an ingest-time, operator-visible event — never inside a query.
"""

from __future__ import annotations

from collections.abc import Callable

import chromadb
from chromadb.api.types import EmbeddingFunction
from chromadb.utils import embedding_functions

from arcaai.platform.retrieval.interface import (
    Chunk,
    RetrievalStore,
    RetrievedChunk,
)

# Pinned by name + packaging version; parameters-in-string discipline as
# CHUNKER_VERSION. Any change to the model, its runtime, or the chromadb
# pin that supplies it MUST change this string.
EMBEDDING_MODEL = "all-MiniLM-L6-v2;onnx;chromadb==1.5.9"

_PINNED_MODEL_NAME = "all-MiniLM-L6-v2"

# Index parameters SET explicitly at collection construction, then READ BACK
# from the live collection and reported from the read-back (queue item 36(a),
# design fork (iii) as ruled 2026-08-22). Setting without reading back would
# report a declaration as though it were a measurement, which the runner's own
# rule forbids; reading back without setting would leave the environment at
# whatever default the installed chromadb happens to carry, so a version bump
# would move the environment identity silently.
#
# THE VALUES ARE THE CURRENT EFFECTIVE DEFAULTS, DELIBERATELY. Read from a live
# chromadb 1.5.5 collection created with no index parameters: space l2,
# ef_construction 100, max_neighbors 16, ef_search 100. Pinning them changes no
# retrieval result today — that is the point. Choosing a different space here
# would silently change every score and every ranking in the corpus, which is a
# retrieval decision and not this increment's to take.
_INDEX_PARAMETERS: dict[str, str | int] = {
    "hnsw:space": "l2",
    "hnsw:construction_ef": 100,
    "hnsw:M": 16,
    "hnsw:search_ef": 100,
}

# Effective-configuration key -> material-parameter name. The left side is
# chromadb's resolved `configuration_json["hnsw"]` vocabulary, which differs
# from the `hnsw:`-prefixed vocabulary used to SET the values above; the right
# side is the runner's MATERIAL_PARAMETERS naming. Mapping them here keeps
# chromadb's vocabulary inside this module, per the CF-1/B7-a boundary.
_EFFECTIVE_TO_MATERIAL = {
    "space": "distance_space",
    "ef_construction": "hnsw_construction_ef",
    "max_neighbors": "hnsw_m",
    "ef_search": "hnsw_ef_search",
}


def supplied_model_name() -> str | None:
    """The model name chromadb's MiniLM class currently ships — exposed
    so callers (tests included) can verify the pin without importing
    chromadb themselves, keeping the CF-1/B7-a boundary absolute."""
    return getattr(embedding_functions.ONNXMiniLM_L6_V2, "MODEL_NAME", None)


class _CallableEmbedding(EmbeddingFunction):
    """Adapt a plain ``list[str] -> list[list[float]]`` callable to
    chromadb's EmbeddingFunction interface. Exists so nothing outside
    this module ever subclasses or imports a chromadb type."""

    def __init__(self, fn: Callable[[list[str]], list[list[float]]], name: str):
        self._fn = fn
        self._name = name

    def __call__(self, input):
        return self._fn(list(input))

    def name(self) -> str:
        return self._name

    def get_config(self) -> dict:
        # Test/injection wrapper: not persistable configuration.
        return {"name": self._name, "persistable": False}

    @staticmethod
    def build_from_config(config: dict) -> object:
        # The NotImplemented sentinel is chromadb's documented signal
        # (EmbeddingFunction.is_legacy) that this function is not
        # rebuildable from config. Injected callables are test/dev
        # constructs; chromadb 1.5.9 emits a DeprecationWarning for
        # legacy functions, accepted deliberately under the hard pin.
        return NotImplemented


def pinned_embedding_function() -> embedding_functions.ONNXMiniLM_L6_V2:
    """Construct the pinned embedding function explicitly.

    Verifies at construction that the class chromadb supplies still
    names the pinned model — if a chromadb upgrade ever changes the
    underlying model, this fails loudly at init rather than silently
    re-embedding the corpus under a different model.
    """
    fn_cls = embedding_functions.ONNXMiniLM_L6_V2
    actual = supplied_model_name()
    if actual != _PINNED_MODEL_NAME:
        raise RuntimeError(
            f"Embedding model pin violated: expected {_PINNED_MODEL_NAME!r}, "
            f"chromadb supplies {actual!r}. Update EMBEDDING_MODEL and the "
            "B7_GATE §2.1 record deliberately, or restore the pin."
        )
    return fn_cls()


class ChromaStore(RetrievalStore):
    """RetrievalStore backed by ChromaDB.

    ``embedding_function=None`` selects the pinned function above.
    Tests inject a deterministic offline function; production code
    passes None and gets the pin.
    """

    def __init__(
        self,
        collection_name: str = "fraud_corpus",
        persist_directory: str | None = None,
        embedding_function: Callable[[list[str]], list[list[float]]]
        | None = None,
    ) -> None:
        if persist_directory is None:
            self._client = chromadb.EphemeralClient()
        else:
            self._client = chromadb.PersistentClient(path=persist_directory)
        if embedding_function is None:
            self._embedding = pinned_embedding_function()
        elif isinstance(embedding_function, EmbeddingFunction):
            self._embedding = embedding_function
        else:
            self._embedding = _CallableEmbedding(
                embedding_function, name="injected-callable"
            )
        self._collection_name = collection_name
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            embedding_function=self._embedding,
            metadata={"embedding_model": EMBEDDING_MODEL, **_INDEX_PARAMETERS},
        )
        # Warm-up: force any first-use model download to happen here,
        # at construction, not inside the first query (R7 path).
        self._embedding(["warm-up"])

    # -------------------------------------------------- environment identity

    @property
    def collection_metadata(self) -> dict[str, str]:
        """The material index parameters, READ BACK from the live collection.

        Consumed by ``arcaai.harness.runner.read_material_parameters`` through
        its duck-typed ``collection_metadata`` surface, which keys on the
        runner's MATERIAL_PARAMETERS names. Widening this surface is queue item
        36(a); before it existed, four of the five material parameters read
        UNKNOWN on every run and the environment identity was honest but
        partial.

        **Read back, not echoed.** The values come from chromadb's resolved
        ``configuration_json["hnsw"]``, never from ``collection.metadata``.
        The distinction is the whole of design fork (iii) and is not
        cosmetic: ``collection.metadata`` returns what this adapter PASSED IN,
        so reporting from it would report a declaration as though it had been
        measured — and for a collection that already existed with different
        parameters it would report values the index is not actually using.
        ``configuration_json`` reports what the index resolved to. Verified on
        chromadb 1.5.5: re-opening an existing collection with different
        metadata leaves both the stored metadata and the effective
        configuration unchanged, so only the read-back tells the truth.

        **Three outcomes, and the third is silence.** A parameter that cannot
        be read is OMITTED from the returned dict rather than defaulted. The
        runner initialises every parameter to UNKNOWN and only overwrites what
        this dict supplies, so an omission surfaces as UNKNOWN and is named in
        the result's ``unknown_parameters``. A documented default substituted
        here would make two genuinely different environments hash identically,
        which is the single failure the environment identity exists to
        prevent.
        """
        values: dict[str, str] = {"embedding_model": EMBEDDING_MODEL}
        try:
            configuration = self._collection.configuration_json
            hnsw = configuration["hnsw"]
        except Exception:  # noqa: BLE001 - unreadable config means UNKNOWN
            return values
        if not isinstance(hnsw, dict):
            return values
        for effective_key, material_name in _EFFECTIVE_TO_MATERIAL.items():
            value = hnsw.get(effective_key)
            if value is not None:
                values[material_name] = str(value)
        return values

    # ------------------------------------------------------------ contract

    def add_chunks(self, chunks: list[Chunk]) -> int:
        if not chunks:
            return 0
        ids = [c.chunk_id for c in chunks]
        existing = set(self._collection.get(ids=ids)["ids"])
        fresh = [c for c in chunks if c.chunk_id not in existing]
        if not fresh:
            return 0
        self._collection.add(
            ids=[c.chunk_id for c in fresh],
            documents=[c.text for c in fresh],
            metadatas=[
                {
                    "doc_id": c.doc_id,
                    "ordinal": c.ordinal,
                    "word_count": c.word_count,
                    "chunker_version": c.chunker_version,
                }
                for c in fresh
            ],
        )
        return len(fresh)

    def query(self, text: str, top_k: int = 5) -> list[RetrievedChunk]:
        if self.count() == 0:
            return []
        result = self._collection.query(
            query_texts=[text],
            n_results=min(top_k, self.count()),
        )
        # Read once per query rather than per chunk. UNKNOWN when the space
        # cannot be read: the same three-outcome rule the identity surface
        # follows, because a space asserted here and not actually in force is
        # exactly the defect retiring the literal was meant to close.
        distance_space = self.collection_metadata.get("distance_space", "UNKNOWN")
        out: list[RetrievedChunk] = []
        for chunk_id, document, metadata, distance in zip(
            result["ids"][0],
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
            strict=True,
        ):
            chunk = Chunk(
                chunk_id=chunk_id,
                doc_id=str(metadata["doc_id"]),
                ordinal=int(metadata["ordinal"]),
                text=document,
                word_count=int(metadata["word_count"]),
                chunker_version=str(metadata["chunker_version"]),
            )
            out.append(
                RetrievedChunk(
                    chunk=chunk,
                    score=float(distance),
                    metadata={
                        # Was the literal "l2" until queue item 36(a). A literal
                        # here is an assertion about the index rather than a
                        # reading of it: it happened to be correct while the
                        # collection used chromadb's default space, and would
                        # have gone on reporting "l2" unchanged if the space
                        # ever moved. Sourced from the read-back surface so the
                        # score's stated space is the space that produced it.
                        "distance_space": distance_space,
                        "store": "chromadb",
                    },
                )
            )
        return out

    def count(self) -> int:
        return self._collection.count()

    def reset(self) -> None:
        self._client.delete_collection(self._collection_name)
        self._collection = self._client.get_or_create_collection(
            name=self._collection_name,
            embedding_function=self._embedding,
            metadata={"embedding_model": EMBEDDING_MODEL, **_INDEX_PARAMETERS},
        )
