"""inc3 suite: content-addressed resolution and the surgical manifest
update. Offline: HashEmbedding via the adapter, tmp_path corpora. The
mini-manifest mirrors the real one's shape — comment header, version
notes, mixed eligible/pending entries — because the update is textual
and the tests must prove comments and untouched entries survive."""

from __future__ import annotations

import hashlib
import math
import pathlib

import pytest

from arcaai.platform.governance import corpus
from arcaai.platform.retrieval.chroma_store import ChromaStore
from arcaai.platform.retrieval.chunker import CHUNKER_VERSION
from arcaai.platform.retrieval.ingest import (
    IngestError,
    ingest_documents,
    resolve_documents,
    updated_manifest_text,
)

DOC_A = "Alpha paragraph one about typologies.\n\nAlpha paragraph two.\n"
DOC_B = "Bravo guidance text.\n\nBravo second paragraph, longer words.\n"
DOC_P = "Pending document text, not eligible yet.\n"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


MANIFEST = f"""# Governed corpus manifest — comment header that MUST survive
# the surgical update byte-for-byte.
#
# Version note (2026-07-28.1): seed.

manifest_version: 2026-07-28.5

documents:

  - id: SYN-A
    source: "SYNTHETIC — test. The Authority · A"
    licence: synthetic-arcaai
    sa5_classification: internal-sensitive
    content_sha256: "{sha(DOC_A)}"
    eligibility:
      - state: pending_review
        date: 2026-07-28
        reason: "authored"
      - state: included
        date: 2026-07-28
        reason: "operator inclusion"
    processing:
      chunker_version: null
      embedding_model: null
      chunk_count: null
      ingest_timestamp: null

  - id: SYN-B
    source: "SYNTHETIC — test. The Authority · B"
    licence: synthetic-arcaai
    sa5_classification: internal-sensitive
    content_sha256: "{sha(DOC_B)}"
    eligibility:
      - state: included
        date: 2026-07-28
        reason: "operator inclusion"
    processing:
      chunker_version: null
      embedding_model: null
      chunk_count: null
      ingest_timestamp: null

  - id: SYN-P
    source: "SYNTHETIC — test. The Authority · P"
    licence: synthetic-arcaai
    sa5_classification: internal-sensitive
    content_sha256: "{sha(DOC_P)}"
    eligibility:
      - state: pending_review
        date: 2026-07-28
        reason: "awaiting decision"
    processing:
      chunker_version: null
      embedding_model: null
      chunk_count: null
      ingest_timestamp: null
"""


class HashEmbedding:
    def __call__(self, texts: list[str]) -> list[list[float]]:
        out = []
        for t in texts:
            d = hashlib.sha256(t.encode()).digest()
            v = [b / 255.0 for b in d[:16]]
            n = math.sqrt(sum(x * x for x in v)) or 1.0
            out.append([x / n for x in v])
        return out


@pytest.fixture()
def docs_dir(tmp_path: pathlib.Path) -> pathlib.Path:
    d = tmp_path / "documents"
    d.mkdir()
    # deliberately unhelpful filenames: resolution is by content hash.
    # write_bytes, not write_text: on Windows, write_text translates
    # \n to \r\n and the bytes no longer hash to the manifest sha —
    # caught on the operator machine, 2026-07-29.
    (d / "zz-random-name.md").write_bytes(DOC_A.encode("utf-8"))
    (d / "another_file.txt").write_bytes(DOC_B.encode("utf-8"))
    (d / "pending.md").write_bytes(DOC_P.encode("utf-8"))
    return d


def test_resolution_is_content_addressed(docs_dir: pathlib.Path) -> None:
    m = corpus.parse_manifest(MANIFEST)
    resolved = resolve_documents(m, docs_dir)
    assert {r.doc_id for r in resolved} == {"SYN-A", "SYN-B"}  # eligible only
    by_id = {r.doc_id: r for r in resolved}
    assert by_id["SYN-A"].path.name == "zz-random-name.md"
    assert by_id["SYN-A"].text == DOC_A


def test_missing_eligible_file_hard_fails(docs_dir: pathlib.Path) -> None:
    (docs_dir / "zz-random-name.md").unlink()
    m = corpus.parse_manifest(MANIFEST)
    with pytest.raises(IngestError, match="SYN-A"):
        resolve_documents(m, docs_dir)


def test_ingest_counts_and_index(docs_dir: pathlib.Path) -> None:
    m = corpus.parse_manifest(MANIFEST)
    resolved = resolve_documents(m, docs_dir)
    store = ChromaStore(
        collection_name="inc3_test", embedding_function=HashEmbedding()
    )
    counts = ingest_documents(resolved, store)
    assert set(counts) == {"SYN-A", "SYN-B"}
    assert all(c >= 1 for c in counts.values())
    assert store.count() == sum(counts.values())
    # idempotent re-run: same counts, no growth
    assert ingest_documents(resolved, store) == counts
    assert store.count() == sum(counts.values())
    store.reset()


def _updated(counts: dict[str, int]) -> str:
    return updated_manifest_text(
        MANIFEST,
        counts,
        embedding_model="test-embedding;v0",
        new_version="2026-07-29.6",
        note_lines=["Version note (2026-07-29.6): test ingest."],
    )


def test_update_populates_processing_and_moves_only_snapshot_hash() -> None:
    old = corpus.parse_manifest(MANIFEST)
    new_text = _updated({"SYN-A": 2, "SYN-B": 2})
    new = corpus.parse_manifest(new_text)

    corpus.check_append_only(old, new)  # would raise on any history touch
    assert new["manifest_version"] == "2026-07-29.6"
    assert corpus.eligible_set_sha256(new) == corpus.eligible_set_sha256(old)
    assert (
        corpus.retrieval_snapshot_sha256(new)
        != corpus.retrieval_snapshot_sha256(old)
    )
    a = {d["id"]: d for d in new["documents"]}
    assert a["SYN-A"]["processing"]["chunk_count"] == 2
    assert a["SYN-A"]["processing"]["chunker_version"] == CHUNKER_VERSION
    # non-ingested pending doc untouched
    assert a["SYN-P"]["processing"]["chunk_count"] is None


def test_update_preserves_comments_and_appends_note() -> None:
    new_text = _updated({"SYN-A": 2, "SYN-B": 2})
    assert new_text.startswith(
        "# Governed corpus manifest — comment header that MUST survive"
    )
    assert "# Version note (2026-07-28.1): seed." in new_text
    assert "# Version note (2026-07-29.6): test ingest." in new_text
    assert new_text.index("2026-07-28.1") < new_text.index("2026-07-29.6")


def test_update_rejects_unknown_shape() -> None:
    mangled = MANIFEST.replace("      chunker_version: null", "", 1)
    with pytest.raises((IngestError, corpus.ManifestError)):
        updated_manifest_text(
            mangled,
            {"SYN-A": 2},
            embedding_model="e;v0",
            new_version="2026-07-29.6",
            note_lines=["note"],
        )
