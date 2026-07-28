#!/usr/bin/env python3
"""Generate corpus manifest 'documents:' entries from the documents tree.

Run from the repo root:

    python scripts/corpus_manifest_entries.py

Walks verticals/fraud/corpus/documents/, computes each file's sha256,
verifies the synthetic marker on every SYN-* document, and prints
manifest entries to stdout for review and paste into MANIFEST.yaml.
It also cross-checks the CURRENT manifest: any listed document whose
on-disk hash differs from its manifest content_sha256 is reported as a
DRIFT error, and the script exits non-zero — a manifest entry whose
hash no longer matches its file is the stale-artefact class (WS-E 53).

This script WRITES NOTHING. The manifest is governed and edited by a
person; the script computes, verifies and reports (DEC-0014).
"""

from __future__ import annotations

import hashlib
import pathlib
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parents[1]
DOCS = REPO / "verticals" / "fraud" / "corpus" / "documents"
MANIFEST = REPO / "verticals" / "fraud" / "corpus" / "MANIFEST.yaml"

MARKER = ("SYNTHETIC — arcaai test corpus. Not issued by any real "
          "authority. Licence: synthetic-arcaai.")


def main() -> int:
    if not DOCS.is_dir():
        print(f"No documents directory: {DOCS}", file=sys.stderr)
        return 1

    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    listed = {d["id"]: d for d in manifest.get("documents", [])}

    drift: list[str] = []
    for f in sorted(DOCS.iterdir()):
        if not f.is_file():
            continue
        doc_id = f.stem
        data = f.read_bytes()
        sha = hashlib.sha256(data).hexdigest()

        if doc_id.startswith("SYN-"):
            first = data.decode("utf-8", errors="replace").splitlines()[0].strip()
            if first != MARKER:
                print(f"ERROR {f.name}: first line is not the synthetic "
                      f"marker", file=sys.stderr)
                return 1
            licence = "synthetic-arcaai"
            source_hint = "<synthetic — set the issuing-frame source line>"
        else:
            licence = "OGL-v3.0"
            source_hint = "<legislation.gov.uk URL — Crown copyright, OGL v3.0>"

        entry = listed.get(doc_id)
        if entry is not None:
            if entry["content_sha256"].lower() != sha:
                drift.append(f"{doc_id}: manifest says "
                             f"{entry['content_sha256'][:12]}…, file is {sha[:12]}…")
            continue  # already listed and matching — nothing to print

        print(f"  - id: {doc_id}")
        print(f"    source: \"{source_hint}\"")
        print(f"    licence: {licence}")
        print(f"    sa5_classification: internal-sensitive")
        print(f"    content_sha256: \"{sha}\"")
        print(f"    eligibility:")
        print(f"      - state: pending_review")
        print(f"        date: <today>")
        print(f"        reason: \"authored; awaiting review\"")
        print(f"    processing:")
        print(f"      chunker_version: null")
        print(f"      embedding_model: null")
        print(f"      chunk_count: null")
        print(f"      ingest_timestamp: null")
        print()

    if drift:
        print("DRIFT — manifest hash does not match file:", file=sys.stderr)
        for d in drift:
            print(f"  {d}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
