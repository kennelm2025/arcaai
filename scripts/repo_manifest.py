#!/usr/bin/env python3
"""Generate REPO_MANIFEST.md — session boot context for a fresh chat.

Run from the repo root:

    python scripts/repo_manifest.py --out D:/Downloads

Writes REPO_MANIFEST.md to --out (default: the repo root) and prints a
one-line summary. Attach it at the start of a session, alongside the
session handover, so structure, register numbering and gate state come
from the repository rather than from recollection.

The output is a disposable snapshot for chat startup, not a repo
artefact — the handover is the durable record. Writing it outside the
tree keeps it out of the working directory entirely, where an untracked
markdown file makes local tooling see a different file set from CI.

Everything here is derived. Nothing is hand-maintained, because a
hand-maintained structure file is the parallel document that RAT-01 §2
exists to prevent — and a stale manifest is worse than none, since it
is trusted.

DERIVED STATE IS RECONCILED, NOT ASSERTED (2026-07-27). Every register
and gate state has two sources: a narrative document (BUILD_TRACKER.md,
the CL ledger, DECISIONS.md) and the filesystem. Where they disagree,
this script reports BOTH and raises a divergence — it never silently
prefers one. The v1 script preferred the narrative, and so reported
"B7 NOT STARTED — to be created at entry" while listing
docs/build/B7_GATE.md two sections later, and "CL next 23" while
listing CL-23_policy-as-code.md. A boot artefact that contradicts
itself, silently, is the parallel-document failure in a new costume.

Stdlib only. Safe to run at any time; read-only apart from its output.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Directories listed file-by-file — the ones whose contents get cited.
DETAIL_DIRS = ["docs", "decisions", "scripts", "sql", ".github/workflows"]
# Code directories are DISCOVERED, not listed. A hardcoded list is one
# more parallel document: DEC-0013 moved platform/ to arcaai/platform/
# and the hardcoded list kept reporting the old empty path, hiding the
# entire RAT-02 trio from the boot artefact that exists to show it.
SKIP = {".git", ".dvc", "__pycache__", ".pytest_cache", ".ruff_cache",
        "node_modules", ".venv", "data", ".mypy_cache", ".idea",
        "dist", "build", "site-packages", ".eggs"}

# Files whose names carry a known hygiene defect. Each pattern exists
# because an instance of it reached a commit.
HYGIENE = [
    (re.compile(r"~\$"), "Word lock file — needs `~$*` ignore + rm --cached"),
    (re.compile(r" \(\d+\)(?=\.[^.]+$|$)"), "download-suffix duplicate"),
]

STATUS_WORDS = ("GATE PASSED", "NOT STARTED", "IN PROGRESS", "COMPLETE")


def git(repo: Path, *args: str) -> str:
    try:
        out = subprocess.run(["git", "-C", str(repo), *args],
                             capture_output=True, text=True, timeout=10)
        return out.stdout.strip() if out.returncode == 0 else "?"
    except Exception:
        return "?"


def git_raw(repo: Path, *args: str) -> str:
    """git() strips, which eats the leading space of a ` M path` porcelain
    code and so corrupts the first dirty entry. Column-significant output
    is read unstripped."""
    try:
        out = subprocess.run(["git", "-C", str(repo), *args],
                             capture_output=True, text=True, timeout=10)
        return out.stdout.rstrip("\n") if out.returncode == 0 else ""
    except Exception:
        return ""


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


# --------------------------------------------------------------------
# git working state
# --------------------------------------------------------------------

def porcelain(repo: Path) -> dict[str, str]:
    """Path -> two-char status code. -uall so untracked files are named
    individually; the v1 script counted them and named none, which is
    why an untracked CL draft was indistinguishable from a merged one."""
    out = git_raw(repo, "status", "--porcelain", "-uall")
    if not out:
        return {}
    states: dict[str, str] = {}
    for ln in out.splitlines():
        if len(ln) < 4:
            continue
        code, path = ln[:2], ln[3:].strip().strip('"')
        if " -> " in path:                      # rename
            path = path.split(" -> ", 1)[1]
        states[path] = code
    return states


def branch_position(repo: Path, branch: str) -> list[str]:
    """Ahead/behind vs main and origin/main. A boot artefact generated
    on an unmerged working branch must say so — the boot ritual's
    `git switch main` silently discards nothing, but it does hide
    everything the branch is carrying."""
    lines: list[str] = []
    for ref in ("main", "origin/main"):
        if branch == ref or git(repo, "rev-parse", "--verify", ref) == "?":
            continue
        counts = git(repo, "rev-list", "--left-right", "--count",
                     f"{ref}...HEAD")
        if counts == "?" or "\t" not in counts:
            continue
        behind, ahead = counts.split("\t")
        if behind == "0" and ahead == "0":
            lines.append(f"- vs `{ref}`: identical")
        else:
            lines.append(f"- vs `{ref}`: {ahead} ahead, {behind} behind"
                         + ("  **← unmerged work on this branch**"
                            if ahead != "0" else ""))
    return lines


# --------------------------------------------------------------------
# registers, each reconciled against the filesystem
# --------------------------------------------------------------------

def registers(repo: Path, div: list[str],
              states: dict[str, str]) -> list[str]:
    out: list[str] = []
    gov = repo / "docs" / "governance"

    # DEC — ledger is DECISIONS.md; cross-check against citations
    # anywhere in docs/ and decisions/. A DEC that rode with a PR but
    # never reached the ledger is exactly the CL-08 capture gap.
    dec_text = read(repo / "DECISIONS.md")
    dec_ledger = [int(m) for m in re.findall(r"DEC-(\d{4})", dec_text)]
    out.append(next_number(dec_ledger, "DEC"))
    cited = set()
    for d in ("docs", "decisions"):
        for f in (repo / d).rglob("*.md") if (repo / d).is_dir() else []:
            cited.update(int(m) for m in re.findall(r"DEC-(\d{4})", read(f)))
    orphan_dec = sorted(n for n in cited if dec_ledger and n > max(dec_ledger))
    if orphan_dec:
        div.append(f"**DEC** — cited but above the DECISIONS.md high-water "
                   f"mark: {', '.join(f'DEC-{n:04d}' for n in orphan_dec)}. "
                   f"Ledger entry missing.")

    # ADR — filesystem IS the register here; cross-check citations.
    adr_dir = repo / "decisions"
    adrs = [int(m.group(1)) for f in sorted(adr_dir.glob("*.md"))
            if (m := re.match(r"(\d{4})-", f.name))] if adr_dir.is_dir() else []
    out.append(next_number(adrs, "ADR"))

    # CL — the ledger is canonical per DEC-0007, but a CL with a
    # standalone artefact file and no ledger line is invisible to the
    # ledger reader and vice versa. Report both.
    cl_text = read(gov / "GOVERNANCE_REVIEW_CHANGELOG.md")
    cl_ledger = [int(m) for m in re.findall(r"CL-(\d+)", cl_text)]
    out.append(next_number(cl_ledger, "CL", width=2))
    cl_files = {}
    if gov.is_dir():
        for f in sorted(gov.glob("CL-*")):
            if (m := re.match(r"CL-(\d+)", f.name)):
                cl_files[int(m.group(1))] = f.relative_to(repo).as_posix()
    nxt = max(cl_ledger) + 1 if cl_ledger else 1
    for n in sorted(n for n in cl_files if n not in set(cl_ledger)):
        rel = cl_files[n]
        # Graded by commit status. An UNTRACKED artefact with no ledger
        # line is an unfinished state, consistent with itself — the work
        # simply has not landed. A COMMITTED artefact with no ledger line
        # is a wrong register: the ledger DEC-0007 declares canonical is
        # missing an item the repo carries. Reporting both as one thing
        # was the original defect wearing a new hat.
        if states.get(rel) == "??":
            div.append(f"**CL-{n}** *(pending)* — draft on disk (`{rel}`, "
                       f"UNTRACKED) and no CL-{n} line in the canonical "
                       f"ledger. Consistent — neither has landed. Both go "
                       f"in the same commit, or the ledger entry is lost "
                       f"to a working copy.")
        else:
            div.append(f"**CL-{n}** — artefact COMMITTED (`{rel}`) but no "
                       f"CL-{n} line in the canonical ledger "
                       f"`docs/governance/GOVERNANCE_REVIEW_CHANGELOG.md` "
                       f"(DEC-0007). Register reads next {nxt}; it is wrong.")

    # WS-E — ledger high-water vs highest item cited elsewhere.
    wse_text = read(gov / "WS-E_INCIDENTS.md")
    items = [int(m) for m in re.findall(r"^(\d+)\.\s", wse_text, re.M)]
    out.append(next_number(items, "WS-E item", width=2))
    if items:
        wse_cited = set()
        for f in (gov.rglob("*.md") if gov.is_dir() else []):
            if f.name == "WS-E_INCIDENTS.md":
                continue
            wse_cited.update(int(m) for m in
                             re.findall(r"WS-E\s*(?:item\s*)?(\d{1,2})\b",
                                        read(f)))
        beyond = sorted(n for n in wse_cited if n > max(items))
        if beyond:
            div.append(f"**WS-E** — items cited elsewhere but absent from the "
                       f"ledger: {', '.join(str(n) for n in beyond)}.")

    return out


def open_cls(repo: Path) -> list[str]:
    cl = read(repo / "docs" / "governance" / "GOVERNANCE_REVIEW_CHANGELOG.md")
    found = re.findall(r"^- \[ \] \*\*(CL-[A-Z]?\d+)\*\*(.{0,70})", cl, re.M)
    return [f"{n} —{t.strip().rstrip('*')}" for n, t in found]


# --------------------------------------------------------------------
# gate state — tracker AND gate documents
# --------------------------------------------------------------------

def gate_doc_path(repo: Path, stage: str) -> Path | None:
    for name in (f"{stage}_GATE.md", f"{stage.replace('.', '_')}_GATE.md"):
        p = repo / "docs" / "build" / name
        if p.is_file():
            return p
    return None


def gate_doc_status(p: Path) -> str:
    """First **Status: ...** line of the gate document. The gate doc is
    the authority on its own stage (RAT-01 §2 — the tracker links, it
    does not restate), so its status line is quoted, not inferred."""
    m = re.search(r"^\*\*Status:\s*(.+?)\*\*", read(p), re.M | re.S)
    if not m:
        return ""
    return " ".join(m.group(1).split())


def gates(repo: Path, div: list[str]) -> list[str]:
    tracker = read(repo / "BUILD_TRACKER.md")
    rows: list[str] = []
    for line in tracker.splitlines():
        if not re.match(r"^\|\s*\**\s*B\d", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        stage = cells[0].strip("*` ")
        statuses = [c for c in cells if c in STATUS_WORDS]
        tracker_state = statuses[-1] if statuses else "?"
        date = cells[-1] or "—"

        doc = gate_doc_path(repo, stage)
        if tracker_state == "GATE PASSED":
            state = "GATE PASSED"
        elif doc is not None:
            state = "ENTERED"
        else:
            state = "NOT STARTED"

        if doc is not None:
            note = doc.relative_to(repo).as_posix()
            if (st := gate_doc_status(doc)):
                note += f" — {st}"
        else:
            note = "*no gate doc*"

        rows.append(f"{stage:<5} {state:<12} {date:<10} {note}")

        if tracker_state == "NOT STARTED" and doc is not None:
            div.append(
                f"**{stage}** — BUILD_TRACKER.md says NOT STARTED; "
                f"`{doc.relative_to(repo).as_posix()}` exists"
                + (f" and reads *{gate_doc_status(doc)}*"
                   if gate_doc_status(doc) else "")
                + ". Tracker row needs updating at entry sign-off.")
        elif tracker_state == "GATE PASSED" and doc is None:
            div.append(f"**{stage}** — tracker says GATE PASSED but no gate "
                       f"document exists at `docs/build/`. Evidence trail "
                       f"has no home.")
    return rows


# --------------------------------------------------------------------
# structure
# --------------------------------------------------------------------

def mark(rel: str, states: dict[str, str]) -> str:
    code = states.get(rel)
    if code is None:
        return ""
    if code == "??":
        return "    ← UNTRACKED"
    return f"    ← {code.strip()}"


def code_dirs(repo: Path) -> list[str]:
    """Discovered, not declared. Any top-level directory that is not
    detail-listed and not skipped, reported with its .py count and one
    level of package breakdown."""
    detail_roots = {d.split("/")[0] for d in DETAIL_DIRS}
    out: list[str] = []
    for p in sorted(repo.iterdir()):
        if not p.is_dir() or p.name in SKIP or p.name in detail_roots:
            continue
        if p.name.startswith(".") or p.name.endswith(".egg-info"):
            continue
        pys = [f for f in p.rglob("*.py")
               if not any(part in SKIP for part in f.parts)]
        subs = []
        for sub in sorted(x for x in p.iterdir() if x.is_dir()):
            if sub.name in SKIP:
                continue
            n = sum(1 for f in sub.rglob("*.py")
                    if not any(part in SKIP for part in f.parts))
            if n:
                subs.append(f"{sub.name}/ {n}")
        tail = f" incl. {', '.join(subs[:5])}" if subs else ""
        out.append(f"{p.name}/ ({len(pys)} .py){tail}")
    return out


def shadow_report(repo: Path, dup: Path, pat,
                  states: dict[str, str]) -> str:
    """A download-suffix duplicate is trivia when it is byte-identical to
    its base and a governance defect when it is not. The operator's next
    action differs completely between those two cases, so the manifest
    decides it rather than reporting the filename and leaving it open.
    Written after `GOVERNANCE_REVIEW_CHANGELOG (1).md` was found holding
    the only copy of a CL entry the canonical ledger did not have."""
    base = dup.with_name(pat.sub("", dup.name))
    if not base.is_file():
        return " — no base file of that name; orphan, not a shadow"
    a, b = read(base), read(dup)
    how = ("delete (untracked)" if states.get(dup.relative_to(repo).as_posix())
           == "??" else "`git rm`")
    if a == b:
        return (f" — byte-identical to `{base.relative_to(repo).as_posix()}`;"
                f" safe to {how}")
    only = sorted(set(re.findall(r"CL-[A-Z]?\d+", b))
                  - set(re.findall(r"CL-[A-Z]?\d+", a)))
    detail = (f"; items present ONLY in the shadow: {', '.join(only)}"
              if only else "")
    return (f" — **content DIFFERS** from "
            f"`{base.relative_to(repo).as_posix()}`{detail}. Reconcile "
            f"before you {how}.")


def tree(repo: Path, states: dict[str, str], div: list[str]) -> list[str]:
    lines: list[str] = []
    hygiene: list[str] = []

    def check_hygiene(f: Path, rel: str) -> None:
        for pat, why in HYGIENE:
            if pat.search(f.name):
                extra = (shadow_report(repo, f, pat, states)
                         if "duplicate" in why else "")
                hygiene.append(f"`{rel}` — {why}{extra}")
                return

    root_files = sorted(f for f in repo.iterdir()
                        if f.is_file() and f.suffix in (".md", ".toml", ".cfg"))
    lines.append("(root)")
    for f in root_files:
        check_hygiene(f, f.name)
        lines.append(f"    {f.name}{mark(f.name, states)}")

    for d in DETAIL_DIRS:
        p = repo / d
        if not p.is_dir():
            continue
        lines.append(f"\n{d}/")
        for f in sorted(p.rglob("*")):
            if any(part in SKIP for part in f.parts):
                continue
            if f.is_file():
                rel = f.relative_to(repo).as_posix()
                check_hygiene(f, rel)
                lines.append(f"    {f.relative_to(p).as_posix()}"
                             f"{mark(rel, states)}")

    cd = code_dirs(repo)
    if cd:
        lines.append("\ncode directories: " + ", ".join(cd))

    for h in hygiene:
        div.append(f"**Hygiene** — {h}")
    return lines


# --------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Generate session boot context from the repository.")
    ap.add_argument("repo", nargs="?", default=".",
                    help="repository root (default: current directory)")
    ap.add_argument("--out", default=None, metavar="DIR",
                    help="directory to write REPO_MANIFEST.md into "
                         "(default: the repo root). Point this outside "
                         "the tree, e.g. --out D:\\Downloads")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    out_dir = Path(args.out).resolve() if args.out else repo
    if not (repo / ".git").exists():
        print(f"Not a git repository: {repo}")
        return 1

    div: list[str] = []
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    states = porcelain(repo)
    states.pop("REPO_MANIFEST.md", None)
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD")

    body = [
        "# REPO_MANIFEST",
        "",
        f"*Generated {stamp} by `scripts/repo_manifest.py`. Derived from the",
        "repository — do not hand-edit. Regenerate before pasting into a",
        "session; a stale manifest is worse than none.*",
        "",
        "## Git state",
        "",
        f"- branch: `{branch}`",
        f"- HEAD: `{git(repo, 'rev-parse', '--short', 'HEAD')}` — "
        f"{git(repo, 'log', '-1', '--pretty=%s')}",
        f"- working tree: {'DIRTY' if states else 'clean'}"
        + (f" ({len(states)} entries)" if states else ""),
    ]
    body += branch_position(repo, branch)
    if states:
        body += [""] + [f"    {c}  {p}" for p, c in sorted(states.items())]

    body += ["", "## Divergences", ""]
    div_slot = len(body)          # filled after every section has run

    body += ["## Register numbering", ""]
    body += [f"- {line}" for line in registers(repo, div, states)]

    ocl = open_cls(repo)
    body += ["", "## Open CLs", ""]
    body += [f"- {c}" for c in ocl] if ocl else ["- none parsed"]

    g = gates(repo, div)
    body += ["", "## Build stages", "", "```"]
    body += g if g else ["(no stage rows parsed from BUILD_TRACKER.md)"]
    body += ["```", "", "## Structure", "", "```"]
    body += tree(repo, states, div)
    body += ["```", ""]

    body[div_slot:div_slot] = (
        [f"{i}. {d}" for i, d in enumerate(div, 1)] + [""]
        if div else
        ["*None. Narrative registers and the filesystem agree.*", ""])

    if not out_dir.is_dir():
        print(f"Output directory does not exist: {out_dir}")
        return 1

    out = "\n".join(body)
    target = out_dir / "REPO_MANIFEST.md"
    target.write_text(out, encoding="utf-8", newline="\n")
    print(f"Wrote {target} ({len(out)} bytes) — {len(g)} stages, "
          f"{len(ocl)} open CLs, {len(div)} divergence(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
