#!/usr/bin/env python3
"""DEC-0014 item 7 — Option 1: CI history-walk append-only sweep.

Ruled 2026-08-04 (RULINGS_RECORD_2026-08-04 item 2: both options
approved); precondition verified 2026-08-06 — the loader's mechanical
check exists standalone as
``arcaai.platform.governance.corpus.check_append_only(old, new)``
(corpus.py line 191) and is reused here unmodified, so CI and the
loader enforce one rule from one implementation.

Walks every consecutive pair of historical MANIFEST.yaml versions in
git and runs the loader's own append-only check across each pair:
deleted, modified or reordered eligibility transitions anywhere in
history hard-fail the job. This is the CI half of the item-7 split
(the operator-machine half is scripts/rehash_sweep.py, PR #61): CI
catches history rewrites before release; the boot-ritual sweep
catches pin corruption at session cadence.

Designed exemption (single, auditable): the 2026-07-28.1 ->
2026-07-28.2 transition REPLACED two schema-establishing
placeholders, which the .2 version note records as legal only
because no manifest version had ever been loaded. The pair whose
OLDER version carries manifest_version 2026-07-28.1 is therefore
skipped with a notice; if the epoch manifest predates the schema and
fails to parse, the same exemption applies to the root commit only.
Every other parse failure or violation is a hard failure — a
historical version that stops parsing is itself a tamper signal.

Run: python scripts/manifest_history_check.py
     (repo root; requires full history — CI must check out with
     fetch-depth: 0, or the walk sees one commit and passes
     vacuously; the script fails loudly if it sees fewer than two.)
Exit: 0 all pairs pass; 1 any violation, parse failure, or
     insufficient history.
"""

from __future__ import annotations

import subprocess
import sys

from arcaai.platform.governance import corpus

MANIFEST_PATH = "verticals/fraud/corpus/MANIFEST.yaml"
EPOCH_LABEL = "2026-07-28.1"  # replacement exemption; see docstring


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, check=True
    ).stdout


def main() -> int:
    shas = _git(
        "log", "--format=%H", "--reverse", "--", MANIFEST_PATH
    ).split()
    print(f"manifest_history_check: {len(shas)} commit(s) touch "
          f"{MANIFEST_PATH}")
    if len(shas) < 2:
        print("manifest_history_check: FAIL — fewer than two versions "
              "in visible history; is fetch-depth: 0 set?")
        return 1

    failures = 0
    for i in range(len(shas) - 1):
        old_sha, new_sha = shas[i], shas[i + 1]
        pair = f"{old_sha[:7]} -> {new_sha[:7]}"

        try:
            old = corpus.parse_manifest(
                _git("show", f"{old_sha}:{MANIFEST_PATH}"))
        except Exception as exc:  # noqa: BLE001 — any parse failure matters
            if i == 0:
                print(f"manifest_history_check: skip  {pair} — root "
                      f"version unparseable; schema-epoch exemption "
                      f"({type(exc).__name__})")
                continue
            print(f"manifest_history_check: FAIL  {pair} — older "
                  f"version unparseable: {exc}")
            failures += 1
            continue

        if old.get("manifest_version") == EPOCH_LABEL:
            print(f"manifest_history_check: skip  {pair} — "
                  f"{EPOCH_LABEL} replacement exemption (.2 version "
                  f"note; pre-first-load)")
            continue

        try:
            new = corpus.parse_manifest(
                _git("show", f"{new_sha}:{MANIFEST_PATH}"))
        except Exception as exc:  # noqa: BLE001
            print(f"manifest_history_check: FAIL  {pair} — newer "
                  f"version unparseable: {exc}")
            failures += 1
            continue

        try:
            corpus.check_append_only(old, new)
        except corpus.AppendOnlyViolation as exc:
            print(f"manifest_history_check: FAIL  {pair} — {exc}")
            failures += 1
            continue

        print(f"manifest_history_check: ok    {pair}  "
              f"({old.get('manifest_version')} -> "
              f"{new.get('manifest_version')})")

    if failures:
        print(f"manifest_history_check: {failures} pair(s) FAILED")
        return 1
    print("manifest_history_check: all pairs pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
