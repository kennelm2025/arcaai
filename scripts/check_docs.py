#!/usr/bin/env python3
"""Lightweight structural checks for repository markdown.

Targets failure classes observed in the programme rather than general
style. Each check exists because something broke:

  1. Unbalanced ** — WS-E 48 (DEC-0010 and WS-E item 40 both shipped
     with bold unterminated to end of file).
  2. Unbalanced backtick — DEC-0010 closed a code span with an
     apostrophe.
  3. Dead internal path reference — nothing verifies that a path cited
     in a governance document exists; WS-E 41 was the same class caught
     by git rather than by review.
  4. CRLF in a tracked markdown file — house rule is LF.

Exit 1 on any finding. No third-party dependencies.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOTS = ("docs", "decisions")
ROOT_GLOB = "*.md"
FENCE = re.compile(r"```.*?```", re.DOTALL)
# repo-relative paths cited inside single backticks
PATH_REF = re.compile(r"`([A-Za-z0-9_][A-Za-z0-9_./-]*\.(?:md|py|yml|yaml|toml|json))`")
# Template forms are not real paths: BN_GATE.md, 0001-name.md,
# round-N-sme-name.md, YYYY-MM.md, B*_GATE.md
PLACEHOLDER = re.compile(
    r"(BN_|NNN|\*|<|\{|/\d+-name\.|-N-|YYYY|MM\.md|/_template\.)"
)
# The incident ledger cites incorrect paths by design - that is what the
# incidents are about (see WS-E 41, which quotes the wrong path it was
# logged for). Structural checks still apply; path existence does not.
NO_PATH_CHECK = {"docs/governance/WS-E_INCIDENTS.md"}
# DVC-managed outputs are never in the git tree; whether they exist on
# disk depends on whether `dvc pull` has run. Checking them makes the
# result environment-dependent - it passed locally and failed in CI on
# first run (WS-E 45). Path existence is only meaningful for paths git
# actually carries.
NO_PATH_PREFIX = ("data/",)


def targets(repo: Path) -> list[Path]:
    found: list[Path] = sorted(repo.glob(ROOT_GLOB))
    for root in ROOTS:
        d = repo / root
        if d.is_dir():
            found.extend(sorted(d.rglob("*.md")))
    return found


def check_file(repo: Path, path: Path) -> list[str]:
    findings: list[str] = []
    raw = path.read_bytes()
    rel = path.relative_to(repo).as_posix()

    if b"\r\n" in raw:
        findings.append(f"{rel}: CRLF line endings (house rule is LF)")

    text = raw.decode("utf-8")
    stripped = FENCE.sub("", text)

    bolds = stripped.count("**")
    if bolds % 2:
        findings.append(
            f"{rel}: unbalanced '**' ({bolds} occurrences) — a bold span "
            f"is unterminated (WS-E 48)"
        )

    ticks = stripped.count("`")
    if ticks % 2:
        findings.append(
            f"{rel}: unbalanced backtick ({ticks} occurrences) — a code "
            f"span is unterminated or closed with the wrong character"
        )

    if rel in NO_PATH_CHECK:
        return findings

    for ref in sorted(set(PATH_REF.findall(stripped))):
        if ref.startswith(("http", "www.")) or "/" not in ref:
            continue
        if PLACEHOLDER.search(ref):
            continue  # template form, e.g. docs/build/BN_GATE.md
        if ref.startswith(NO_PATH_PREFIX):
            continue  # DVC-managed, not in git
        if not (repo / ref).exists():
            findings.append(f"{rel}: cited path does not exist — {ref}")

    return findings


def load_baseline(repo: Path) -> set[str]:
    """Findings accepted at the time the check was introduced.

    Each line is a to-do, not a pardon: the check passes on the current
    tree so it can catch regressions, and the baseline shrinks as the
    underlying documents are corrected. A new finding is never added
    here without a CL or DEC recording why.
    """
    f = repo / "scripts" / "check_docs_baseline.txt"
    if not f.exists():
        return set()
    return {
        ln.strip()
        for ln in f.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.startswith("#")
    }


def main() -> int:
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    baseline = load_baseline(repo)
    files = targets(repo)
    if not files:
        print(f"No markdown found under {repo} — check the working directory.")
        return 1

    all_findings: list[str] = []
    for f in files:
        all_findings.extend(check_file(repo, f))

    findings = [f for f in all_findings if f not in baseline]
    accepted = len(all_findings) - len(findings)

    print(f"Checked {len(files)} markdown files under {repo}")
    if accepted:
        print(f"{accepted} baselined finding(s) suppressed "
              f"(see scripts/check_docs_baseline.txt)")
    if findings:
        print(f"\n{len(findings)} finding(s):\n")
        for f in findings:
            print(f"  - {f}")
        return 1
    print("No findings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
