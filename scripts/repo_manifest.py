#!/usr/bin/env python3
"""Generate REPO_MANIFEST.md — session boot context for a fresh chat.

Run from the repo root:

    python scripts/repo_manifest.py

Writes REPO_MANIFEST.md and prints a one-line summary. Attach or paste
the file at the start of a session so structure, register numbering and
gate state come from the repository rather than from recollection.

Everything here is derived. Nothing is hand-maintained, because a
hand-maintained structure file is the parallel document that RAT-01 §2
exists to prevent — and a stale manifest is worse than none, since it
is trusted.

Stdlib only. Safe to run at any time; read-only apart from its output.
"""

from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Directories listed file-by-file — the ones whose contents get cited.
DETAIL_DIRS = ["docs", "decisions", "scripts", ".github/workflows"]
# Directories summarised by count — code, where names change constantly.
COUNT_DIRS = ["agent", "api", "contracts", "verticals", "platform",
              "ingest", "infra", "monitoring", "tests", "frontend"]
SKIP = {".git", ".dvc", "__pycache__", ".pytest_cache", ".ruff_cache",
        "node_modules", ".venv", "data", ".mypy_cache", ".idea"}


def git(repo: Path, *args: str) -> str:
    try:
        out = subprocess.run(["git", "-C", str(repo), *args],
                             capture_output=True, text=True, timeout=10)
        return out.stdout.strip() if out.returncode == 0 else "?"
    except Exception:
        return "?"


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


def next_number(values: list[int], label: str, width: int = 4) -> str:
    if not values:
        return f"{label}: none found"
    hi = max(values)
    return f"{label}: highest {hi:0{width}d} → next {hi + 1:0{width}d}"


def registers(repo: Path) -> list[str]:
    out: list[str] = []

    dec = read(repo / "DECISIONS.md")
    out.append(next_number(
        [int(m) for m in re.findall(r"DEC-(\d{4})", dec)], "DEC"))

    adr_dir = repo / "decisions"
    adrs = [int(m.group(1)) for f in sorted(adr_dir.glob("*.md"))
            if (m := re.match(r"(\d{4})-", f.name))] if adr_dir.is_dir() else []
    out.append(next_number(adrs, "ADR"))

    cl = read(repo / "docs" / "governance" / "GOVERNANCE_REVIEW_CHANGELOG.md")
    out.append(next_number(
        [int(m) for m in re.findall(r"CL-(\d+)", cl)], "CL", width=2))

    wse = read(repo / "docs" / "governance" / "WS-E_INCIDENTS.md")
    items = [int(m) for m in re.findall(r"^(\d+)\.\s", wse, re.M)]
    out.append(next_number(items, "WS-E item", width=2))

    return out


def open_cls(repo: Path) -> list[str]:
    cl = read(repo / "docs" / "governance" / "GOVERNANCE_REVIEW_CHANGELOG.md")
    found = re.findall(r"^- \[ \] \*\*(CL-\d+)\*\*(.{0,70})", cl, re.M)
    return [f"{n} —{t.strip().rstrip('*')}" for n, t in found]


def gates(repo: Path) -> list[str]:
    tracker = read(repo / "BUILD_TRACKER.md")
    rows: list[str] = []
    for line in tracker.splitlines():
        if not re.match(r"^\|\s*B\d", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        stage = cells[0]
        statuses = [c for c in cells if c in
                    ("GATE PASSED", "NOT STARTED", "IN PROGRESS",
                     "COMPLETE")]
        gate = statuses[-1] if statuses else "?"
        date = cells[-1] or "—"
        doc = next((c for c in cells if "GATE.md" in c or "entry" in c), "")
        rows.append(f"{stage:<5} {gate:<12} {date:<10} {doc}")
    return rows


def tree(repo: Path) -> list[str]:
    lines: list[str] = []

    root_files = sorted(f.name for f in repo.iterdir()
                        if f.is_file() and f.suffix in (".md", ".toml", ".cfg"))
    lines.append("(root)")
    lines.extend(f"    {n}" for n in root_files)

    for d in DETAIL_DIRS:
        p = repo / d
        if not p.is_dir():
            continue
        lines.append(f"\n{d}/")
        for f in sorted(p.rglob("*")):
            if any(part in SKIP for part in f.parts):
                continue
            if f.is_file():
                lines.append(f"    {f.relative_to(p).as_posix()}")

    counts: list[str] = []
    for d in COUNT_DIRS:
        p = repo / d
        if not p.is_dir():
            continue
        n = sum(1 for f in p.rglob("*.py")
                if not any(part in SKIP for part in f.parts))
        counts.append(f"{d}/ ({n} .py)")
    if counts:
        lines.append("\ncode directories: " + ", ".join(counts))

    return lines


def main() -> int:
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not (repo / ".git").exists():
        print(f"Not a git repository: {repo}")
        return 1

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    dirty = "\n".join(
        ln for ln in git(repo, "status", "--porcelain").splitlines()
        if "REPO_MANIFEST.md" not in ln
    )

    body = [
        "# REPO_MANIFEST",
        "",
        f"*Generated {stamp} by `scripts/repo_manifest.py`. Derived from the",
        "repository — do not hand-edit. Regenerate before pasting into a",
        "session; a stale manifest is worse than none.*",
        "",
        "## Git state",
        "",
        f"- branch: `{git(repo, 'rev-parse', '--abbrev-ref', 'HEAD')}`",
        f"- HEAD: `{git(repo, 'rev-parse', '--short', 'HEAD')}` — "
        f"{git(repo, 'log', '-1', '--pretty=%s')}",
        f"- working tree: {'DIRTY' if dirty else 'clean'}"
        + (f" ({len(dirty.splitlines())} entries)" if dirty else ""),
        "",
        "## Register numbering",
        "",
    ]
    body += [f"- {line}" for line in registers(repo)]

    ocl = open_cls(repo)
    body += ["", "## Open CLs", ""]
    body += [f"- {c}" for c in ocl] if ocl else ["- none parsed"]

    g = gates(repo)
    body += ["", "## Build stages", "", "```"]
    body += g if g else ["(no stage rows parsed from BUILD_TRACKER.md)"]
    body += ["```", "", "## Structure", "", "```"]
    body += tree(repo)
    body += ["```", ""]

    out = "\n".join(body)
    (repo / "REPO_MANIFEST.md").write_text(out, encoding="utf-8", newline="\n")
    print(f"Wrote REPO_MANIFEST.md ({len(out)} bytes) — "
          f"{len(g)} stages, {len(ocl)} open CLs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
