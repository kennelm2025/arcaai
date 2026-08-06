"""DEC-0014 item 7 — operator-machine re-hash sweep (Option 2).

Ruled 2026-08-04 (RULINGS_RECORD_2026-08-04, item 2: both options
approved; approach approved, script pending on-machine verification).
Draft assumptions verified on the operator machine 2026-08-06:

  ASSUMPTION 1 (connection) — RESOLVED. No shared session helper
  exists; the operational pattern is scripts/b7_run.py's
  ``create_engine(APP_DSN)`` with the ``ARCAAI_AUDIT_APP_DSN`` env
  var and the app-role dev default. This script mirrors that pattern
  (same DSN source, same role — a consumer of the grants per
  sql/governance_grants.sql, read-only here).

  ASSUMPTION 2 (schema) — CORRECTED. corpus_version columns confirmed
  (manifest_version, manifest_sha256) but ``version_id`` is a UUID
  primary key, not a sequence — the draft's ``ORDER BY version_id``
  is not a chronology. Ordering is by ``loaded_at`` instead.

Purpose: at session open (boot ritual, after repo_manifest.py), read
every pinned row in ``corpus_version``, recompute each pinned
manifest_sha256 against the manifest content in git history, and
hard-fail on any pin whose manifest content cannot be located —
pin-row corruption detected at session cadence rather than waiting
for the next load. Companion CI leg (Option 1, history-walk
append-only sweep) is ruled to land separately.

Run: python scripts/rehash_sweep.py            (from repo root,
     conda arcaai, normal shell, Docker dev stack up — this touches
     the DB, so the Docker-before-DB rule applies)
Exit: 0 all pins verified; 1 any pin whose manifest content cannot
     be located in git history, or any DB/git failure.
"""

from __future__ import annotations

import os
import subprocess
import sys

from sqlalchemy import create_engine, text

from arcaai.platform.governance import corpus

MANIFEST_PATH = "verticals/fraud/corpus/MANIFEST.yaml"

# Mirror of scripts/b7_run.py — runtime app role, never owner: this
# sweep is a consumer of the grants, and needs (and must hold) no
# write grant.
APP_DSN = os.environ.get(
    "ARCAAI_AUDIT_APP_DSN",
    "postgresql+psycopg://arcaai_app:app_dev@localhost:5432/arcaai_audit",
)


def manifest_hashes_in_history() -> dict[str, str]:
    """Map of manifest_sha256 -> commit for every historical version.

    Content-addressed lookup per DEC-0014 item 6's replay chain: the
    pin stores no git commit; we walk history and index by recomputed
    hash. Duplicate hashes across commits are fine (same content —
    first-seen commit recorded).
    """
    shas = subprocess.run(
        ["git", "log", "--format=%H", "--", MANIFEST_PATH],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    out: dict[str, str] = {}
    for sha in shas:
        content = subprocess.run(
            ["git", "show", f"{sha}:{MANIFEST_PATH}"],
            capture_output=True, text=True, check=True,
        ).stdout
        m = corpus.parse_manifest(content)
        out.setdefault(corpus.manifest_sha256(m), sha)
    return out


def pinned_rows() -> list[tuple[str, str, str]]:
    """(version_id, manifest_version, manifest_sha256) per loaded
    version, oldest first by loaded_at. Read-only SELECT on the app
    role."""
    engine = create_engine(APP_DSN)
    try:
        with engine.connect() as conn:
            rows = conn.execute(text(
                "SELECT version_id, manifest_version, manifest_sha256 "
                "FROM corpus_version ORDER BY loaded_at"
            )).all()
        return [(str(r[0]), r[1], r[2]) for r in rows]
    finally:
        engine.dispose()


def main() -> int:
    print(f"rehash_sweep: audit DSN (host) : {APP_DSN.split('@')[-1]}")
    history = manifest_hashes_in_history()
    print(f"rehash_sweep: manifest versions in git history: {len(history)}")
    pins = pinned_rows()
    print(f"rehash_sweep: pinned corpus_version rows: {len(pins)}")
    failures = 0
    for version_id, label, msha in pins:
        commit = history.get(msha)
        if commit is None:
            failures += 1
            print(
                f"rehash_sweep: FAIL  {label} ({version_id}) — pinned "
                f"manifest_sha256 {msha} not reproducible from any "
                f"historical {MANIFEST_PATH}"
            )
        else:
            print(
                f"rehash_sweep: ok    {label} ({version_id}) — "
                f"{msha[:12]}… reproduced at {commit[:7]}"
            )
    if failures:
        print(f"rehash_sweep: {failures} pin(s) FAILED verification")
        return 1
    print("rehash_sweep: all pins verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
