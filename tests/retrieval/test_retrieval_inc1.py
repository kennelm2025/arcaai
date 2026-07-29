"""inc1 suite: chunker determinism and the CF-1/B7-a import boundary.

The import-boundary test is the mechanical form of CF-1/B7-a's
conforms-if condition: ``chromadb`` imported in one adapter module and
nowhere else. At inc1 the allowlist is empty — no adapter exists yet;
inc2 adds exactly one path to ALLOWED_CHROMADB_IMPORTERS and nothing
else may ever join it without a recorded CF-1 deviation.
"""

from __future__ import annotations

import pathlib
import re

import pytest

from arcaai.platform.retrieval import (
    CHUNKER_VERSION,
    Chunk,
    RetrievalStore,
    chunk_document,
    make_chunk_id,
)

# ---------------------------------------------------------------- chunker

PARA = "word " * 50  # 50-word paragraph


def doc(n_paras: int) -> str:
    return "\n\n".join(PARA.strip() for _ in range(n_paras))


def test_deterministic() -> None:
    a = chunk_document("SYN-TR-01", doc(10))
    b = chunk_document("SYN-TR-01", doc(10))
    assert a == b
    assert [c.chunk_id for c in a] == [c.chunk_id for c in b]


def test_chunk_ids_carry_doc_ordinal_and_content() -> None:
    chunks = chunk_document("SYN-TR-01", doc(10))
    for i, c in enumerate(chunks):
        assert c.ordinal == i
        assert c.chunk_id.startswith(f"SYN-TR-01#{i:04d}-")
        assert c.chunk_id == make_chunk_id("SYN-TR-01", i, c.text)


def test_content_change_changes_id_suffix_only_where_changed() -> None:
    a = chunk_document("D", doc(10))
    b = chunk_document("D", doc(9) + "\n\n" + PARA.strip() + " altered")
    assert a[0].chunk_id == b[0].chunk_id  # untouched early chunk stable
    assert a[-1].chunk_id != b[-1].chunk_id  # altered tail moves


def test_packing_respects_target() -> None:
    chunks = chunk_document("D", doc(20))
    # 50-word paragraphs pack 4 to a 220-word target
    assert all(c.word_count <= 220 for c in chunks)
    assert len(chunks) == 5


def test_oversize_paragraph_sentence_split() -> None:
    sentences = " ".join(
        f"Sentence number {i} has exactly six words." for i in range(80)
    )
    chunks = chunk_document("D", sentences)
    assert len(chunks) > 1
    assert all(c.word_count <= 380 for c in chunks)
    # no sentence is broken mid-way: every chunk ends at a boundary
    assert all(c.text.rstrip().endswith(".") for c in chunks)


def test_whole_paragraphs_never_split_under_cap() -> None:
    text = doc(3)
    joined = "\n\n".join(c.text for c in chunk_document("D", text))
    for para in text.split("\n\n"):
        assert para in joined


def test_empty_and_whitespace_input() -> None:
    assert chunk_document("D", "") == []
    assert chunk_document("D", "   \n\n  \n") == []


def test_crlf_normalised() -> None:
    lf = chunk_document("D", "alpha beta\n\ngamma delta")
    crlf = chunk_document("D", "alpha beta\r\n\r\ngamma delta")
    assert lf == crlf


def test_version_string_present_on_every_chunk() -> None:
    for c in chunk_document("D", doc(6)):
        assert c.chunker_version == CHUNKER_VERSION


# -------------------------------------------------------------- interface


class _FakeStore(RetrievalStore):
    """Minimal in-memory implementation proving the ABC is complete
    and implementable without any store-specific dependency."""

    def __init__(self) -> None:
        self._chunks: dict[str, Chunk] = {}

    def add_chunks(self, chunks: list[Chunk]) -> int:
        added = 0
        for c in chunks:
            if c.chunk_id not in self._chunks:
                self._chunks[c.chunk_id] = c
                added += 1
        return added

    def query(self, text: str, top_k: int = 5):
        from arcaai.platform.retrieval import RetrievedChunk

        hits = [c for c in self._chunks.values() if text in c.text]
        return [RetrievedChunk(chunk=c, score=1.0) for c in hits][:top_k]

    def count(self) -> int:
        return len(self._chunks)

    def reset(self) -> None:
        self._chunks.clear()


def test_interface_idempotent_add_and_query() -> None:
    store = _FakeStore()
    chunks = chunk_document("D", doc(8))
    assert store.add_chunks(chunks) == len(chunks)
    assert store.add_chunks(chunks) == 0  # idempotent on chunk_id
    assert store.count() == len(chunks)
    assert store.query("word", top_k=2)
    store.reset()
    assert store.count() == 0
    assert store.query("word") == []


def test_abc_rejects_partial_implementation() -> None:
    class Partial(RetrievalStore):  # missing everything
        pass

    with pytest.raises(TypeError):
        Partial()  # type: ignore[abstract]


# ------------------------------------------------- CF-1/B7-a import boundary

ALLOWED_CHROMADB_IMPORTERS: set[str] = {
    "arcaai/platform/retrieval/chroma_store.py",  # the one adapter (inc2)
}

_IMPORT_RE = re.compile(r"^\s*(import\s+chromadb|from\s+chromadb)", re.MULTILINE)


def test_chromadb_imported_only_in_allowlisted_adapter() -> None:
    repo_root = pathlib.Path(__file__).resolve().parents[2]
    offenders = []
    for path in repo_root.rglob("*.py"):
        rel = path.relative_to(repo_root).as_posix()
        if rel.startswith(("archive/", ".venv/", "node_modules/")):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if _IMPORT_RE.search(text) and rel not in ALLOWED_CHROMADB_IMPORTERS:
            offenders.append(rel)
    assert offenders == [], (
        "chromadb imported outside the allowlisted adapter (CF-1/B7-a): "
        f"{offenders}"
    )
