"""B7 ingest run (inc3) — operator CLI over the platform machinery.

Dry-run by default: resolves, chunks, indexes, and prints the full
verification summary WITHOUT touching the manifest. Re-run with
--write to update MANIFEST.yaml in place; the git diff is then the
operator eyeball before commit. Loading the new version's snapshot row
stays a separate governed act (the existing load procedure).

The first real run downloads the pinned ONNX MiniLM model at store
construction (adapter warm-up) — an expected, one-time, visible
network event at ingest time, per B7_GATE §2.1. Subsequent runs use
the local cache.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

from arcaai.platform.governance import corpus
from arcaai.platform.retrieval.chroma_store import EMBEDDING_MODEL, ChromaStore
from arcaai.platform.retrieval.chunker import CHUNKER_VERSION
from arcaai.platform.retrieval.ingest import (
    ingest_documents,
    resolve_documents,
    updated_manifest_text,
)

NEW_VERSION = "2026-07-29.6"
NOTE_LINES = [
    "Version note (2026-07-29.6): first ingest run (B7 inc3). Processing",
    "fields populated for all sixteen eligible documents: chunker and",
    "embedding versions per the platform pins, chunk counts as produced,",
    "one timestamp for the run. Identity fields and eligibility history",
    "untouched; retrieval_snapshot_sha256 diverges from eligible_set_sha256",
    "from this version, per the DEC-0014 two-hash design.",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest", default="verticals/fraud/corpus/MANIFEST.yaml"
    )
    parser.add_argument(
        "--docs-dir", default="verticals/fraud/corpus/documents"
    )
    parser.add_argument(
        "--index-dir",
        default="data/fraud/corpus_index",
        help="ChromaDB persistent directory (kept out of git)",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="update the manifest in place (default: dry run, print only)",
    )
    args = parser.parse_args()

    manifest_path = pathlib.Path(args.manifest)
    manifest_text = manifest_path.read_text(encoding="utf-8")
    manifest = corpus.parse_manifest(manifest_text)

    print(f"manifest          : {manifest['manifest_version']}")
    print(f"manifest_sha256   : {corpus.manifest_sha256(manifest)}")
    print(f"eligible          : {len(corpus.eligible_documents(manifest))}")
    print(f"chunker           : {CHUNKER_VERSION}")
    print(f"embedding         : {EMBEDDING_MODEL}")
    print()

    resolved = resolve_documents(manifest, pathlib.Path(args.docs_dir))
    print(f"resolved by content hash: {len(resolved)} documents")

    store = ChromaStore(persist_directory=args.index_dir)
    counts = ingest_documents(resolved, store)
    for doc_id in sorted(counts):
        print(f"  {doc_id:12s} chunks: {counts[doc_id]:3d}")
    print(f"total chunks      : {sum(counts.values())}")
    print(f"index count       : {store.count()}")
    print()

    new_text = updated_manifest_text(
        manifest_text,
        counts,
        embedding_model=EMBEDDING_MODEL,
        new_version=NEW_VERSION,
        note_lines=NOTE_LINES,
    )
    new = corpus.parse_manifest(new_text)
    print(f"new manifest      : {new['manifest_version']}")
    print(f"new manifest_sha  : {corpus.manifest_sha256(new)}")
    print(f"eligible_set_sha  : {corpus.eligible_set_sha256(new)}"
          "  (expect UNCHANGED)")
    print(f"retrieval_snapshot: {corpus.retrieval_snapshot_sha256(new)}"
          "  (expect MOVED)")

    if args.write:
        manifest_path.write_text(new_text, encoding="utf-8", newline="\n")
        print(f"\nWROTE {manifest_path} — eyeball git diff before commit")
    else:
        print("\nDRY RUN — manifest not written; re-run with --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
