"""B7 corpus edge check (skeleton v0.2 section 6, mechanical leg).

Two modes, both read verticals/fraud/corpus/EDGES.yaml:

  python scripts/corpus_edges_check.py
      Design mode: assert closure, asymmetry and immutability over the
      planned edge list. Runs before any authoring lands.

  python scripts/corpus_edges_check.py --docs verticals/fraud/corpus/documents
      Docs mode: additionally check every authored NEW document found
      in the directory (SYN-<ID>.md for ids in the design): marker
      line byte-exact per register, every planned outbound edge
      present in prose, no angle-bracket placeholders, and every
      actual citation register-legal. Extra (unplanned) citations are
      reported for panel visibility, not failed.

Same discipline as the seed's marker-line check; exit code non-zero
on any failure.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
EDGES_PATH = REPO_ROOT / "verticals" / "fraud" / "corpus" / "EDGES.yaml"

AUTHORITY_MARKER = (
    "SYNTHETIC — arcaai test corpus. Not issued by any real authority. "
    "Licence: synthetic-arcaai."
)
FIRM_MARKER = (
    "SYNTHETIC — arcaai test corpus. Not issued by any real authority "
    "or firm. Licence: synthetic-arcaai."
)

ID_PATTERN = re.compile(
    r"\b(?:TR|SG|TY|DL|DP|CV|FW|PL|OP|CS)-\d{2}\b|\bOGL-\d{4}\b"
)


def load_design() -> tuple[dict, dict]:
    data = yaml.safe_load(EDGES_PATH.read_text(encoding="utf-8"))
    return data["register"], data["edges"]


def check_design(register: dict, edges: dict) -> list[str]:
    errors: list[str] = []
    authority = set(register["authority"])
    firm = set(register["firm"])
    existing = set(register["existing"])
    statute = set(register["statute"])
    new_docs = authority | firm
    universe = new_docs | existing | statute

    for doc, targets in edges.items():
        if doc not in new_docs:
            errors.append(f"{doc}: edges declared for a non-new document")
        for t in targets:
            if t not in universe:
                errors.append(f"{doc} -> {t}: target not in the 54-doc universe")
            if t == doc:
                errors.append(f"{doc}: self-citation")
        # Asymmetry: an Authority document never cites a firm document.
        if doc in authority:
            bad = [t for t in targets if t in firm]
            if bad:
                errors.append(f"{doc} (Authority) cites firm doc(s): {bad}")
        # Immutability: inbound to new docs only from new docs - i.e.
        # no edges are declared FOR existing docs (checked above), so
        # any new-doc inbound in this file is from a new doc by
        # construction. Statutes emit nothing:
    for s in statute | existing:
        if s in edges:
            errors.append(f"{s}: existing/statute document declares outbound edges")

    # Closure over the synthetic set: every new doc cites >=1 and is
    # cited >=1 (inbound from new docs only); every existing SYN doc
    # gains >=1 new inbound; every statute is cited into.
    inbound: dict[str, int] = {d: 0 for d in universe}
    for doc, targets in edges.items():
        if not targets:
            errors.append(f"{doc}: no outbound citations")
        for t in targets:
            if t in inbound:
                inbound[t] += 1
    for d in new_docs:
        if inbound[d] == 0:
            errors.append(f"{d}: no inbound citations in the design")
    for d in existing:
        if inbound[d] == 0:
            errors.append(f"{d} (existing): gains no new inbound")
    for s in statute:
        if inbound[s] == 0:
            errors.append(f"{s} (statute): never cited into")
    return errors


def check_docs(
    register: dict, edges: dict, docs_dir: Path
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []
    authority = set(register["authority"])
    firm = set(register["firm"])
    universe = (
        authority | firm | set(register["existing"]) | set(register["statute"])
    )

    for doc_id in sorted(authority | firm):
        path = docs_dir / f"SYN-{doc_id}.md"
        if not path.exists():
            continue  # unauthored batches are not failures
        text = path.read_text(encoding="utf-8")
        first_line = text.splitlines()[0] if text else ""
        expected = FIRM_MARKER if doc_id in firm else AUTHORITY_MARKER
        if first_line != expected:
            errors.append(f"{path.name}: marker line not byte-exact for register")
        if "<" in text and re.search(r"<[a-zA-Z][^>\n]*>", text):
            errors.append(f"{path.name}: angle-bracket placeholder present")
        cited = set(ID_PATTERN.findall(text)) - {doc_id}
        missing = [t for t in edges.get(doc_id, []) if t not in cited]
        if missing:
            errors.append(f"{path.name}: planned edge(s) absent from prose: {missing}")
        illegal = [t for t in cited if t not in universe]
        if illegal:
            errors.append(f"{path.name}: cites unknown id(s): {sorted(illegal)}")
        if doc_id in authority:
            firm_cites = [t for t in cited if t in firm]
            if firm_cites:
                errors.append(
                    f"{path.name}: Authority doc cites firm doc(s): {firm_cites}"
                )
        extras = sorted(cited - set(edges.get(doc_id, [])))
        if extras:
            notes.append(f"{path.name}: extra citations (panel note): {extras}")
        words = len(text.split())
        notes.append(f"{path.name}: {words} words")
    return errors, notes


def main() -> None:
    parser = argparse.ArgumentParser(description="B7 corpus edge check")
    parser.add_argument("--docs", default=None, help="authored documents dir")
    args = parser.parse_args()

    register, edges = load_design()
    errors = check_design(register, edges)
    print(f"design: {len(edges)} documents with edges, "
          f"{sum(len(v) for v in edges.values())} edges")

    notes: list[str] = []
    if args.docs:
        doc_errors, notes = check_docs(register, edges, Path(args.docs))
        errors.extend(doc_errors)

    for n in notes:
        print("note:", n)
    if errors:
        for e in errors:
            print("FAIL:", e)
        sys.exit(1)
    print("OK: closure, asymmetry, immutability, and authored-doc checks pass")


if __name__ == "__main__":
    main()
