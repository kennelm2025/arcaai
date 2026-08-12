#!/usr/bin/env python3
"""D2.2a pre-flight — the implementing artefact (CL-26).

Asserts the four entry criteria of the D2.0 commissioning frame
(``docs/governance/D2.0_COMMISSIONING_FRAME_2026-08-11.md``, RULED
2026-08-11) as one standalone invocable script, so that ceremony skills
CALL this rather than re-describe the procedure. Before this existed the
ONNX cache traversal check lived only as prose in ``CLAUDE.md`` and
``.claude/skills/session-open/SKILL.md``, with no script behind it and no
non-elevation assertion at all — which is the false-green this artefact
closes.

THREE OUTCOMES, NEVER TWO. Every assertion reports GREEN (evaluated and
positively evidenced), RED (evaluated and positively falsified) or
UNKNOWN (could not be evaluated). UNKNOWN exits non-zero and never
collapses into green: every false green catalogued at
``docs/governance/FINDINGS_2026-08-11_onnx-acl-root-cause.md`` was an
UNKNOWN rendered as a GREEN. A skipped assertion is said to be skipped
and also exits non-zero — silence is not a pass.

ORDERING IS LOAD-BEARING (findings section 4). Non-elevation is asserted
first and, if it is anything but GREEN, the remaining three are not
evaluated and are reported SKIPPED. They are all read through the token
whose privilege assertion one establishes; under an elevated token their
results are not merely unreliable, they are meaningless, and reporting
them would be asserting more than was evidenced.

EXIT CODES EVIDENCE NOTHING ON THEIR OWN (findings section 5). Two
observed defects are treated here as anti-patterns rather than described:
a structured exception handler wrapped around a native command is
unreachable, because native executables set an exit status rather than
raising — so every subprocess call below inspects ``returncode``
explicitly and treats a missing binary (OSError) as UNKNOWN rather than
as failure of the condition; and no command output is piped into an
early-terminating consumer, because closing a pipe early returns a
non-zero status from a command that fully succeeded.

REGIME. Anything this script informs is commissioning-regime under the
D2.0 frame: permanently inadmissible as gate evidence, not merely until
the Test Plan is ruled. Every rendering carries the COMMISSIONING marker.

Usage::

    python scripts/d22a_preflight.py           # human-readable
    python scripts/d22a_preflight.py --json    # machine-readable
    python scripts/d22a_preflight.py --provoke cache   # self-test

Exit status: 0 only when all four assertions are GREEN. Any RED, any
UNKNOWN and any SKIPPED yields a non-zero exit.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import socket
import subprocess
import sys

REGIME = "COMMISSIONING"
REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]

# The vector store is a local persistent directory resolved from a
# constant in scripts/b7_run.py, deliberately outside version control —
# so it is absent from a fresh checkout and cannot be assumed present.
INDEX_PATH = REPO_ROOT / "data" / "fraud" / "corpus_index"

# Pinned in arcaai/platform/retrieval/chroma_store.py. Never let chroma's
# default embedding function run: it silently downloads an unpinned model
# mid-query.
PINNED_MODEL_NAME = "all-MiniLM-L6-v2"

EXPECTED_CONDA_ENV = "arcaai"
EXPECTED_PYTHON = "3.11.15"
DB_HOST, DB_PORT = "localhost", 5432

GREEN, RED, UNKNOWN, SKIPPED = "GREEN", "RED", "UNKNOWN", "SKIPPED"


class Result:
    """One assertion's outcome plus the evidence for it.

    ``detail`` states what was actually evaluated, so the success line can
    name it. A Result carrying GREEN with an empty detail is a bug in this
    script, not a pass.
    """

    def __init__(self, name: str, outcome: str, detail: str) -> None:
        self.name = name
        self.outcome = outcome
        self.detail = detail

    def as_dict(self) -> dict:
        return {"assertion": self.name, "outcome": self.outcome,
                "detail": self.detail, "regime": REGIME}


def _run(cmd: list[str]) -> tuple[int | None, str, str]:
    """Run a native command and return (returncode, stdout, stderr).

    returncode is None when the binary could not be executed at all, which
    is an UNKNOWN for the caller and never a RED: a missing docker binary
    is not evidence that the container runtime is unhealthy. Output is
    captured whole — never piped into a consumer that could close the pipe
    early and turn a successful command into a non-zero status.
    """
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None, "", ""
    return proc.returncode, proc.stdout or "", proc.stderr or ""


# --------------------------------------------------------------------------
# Assertion 1 — non-elevation. Asserted FIRST and gates the rest.
# --------------------------------------------------------------------------
def assert_non_elevation() -> Result:
    """Two independent methods, and disagreement is UNKNOWN, not a vote.

    Method A is the Win32 elevation query; method B reads the token's
    mandatory integrity label. The findings record a degradation in which
    filtering the token's groups for the integrity SID range returned an
    empty string rather than an error — had that been the only method, the
    assertion would have produced neither green nor red but a blank, and a
    check comparing against an expected value would have read the blank as
    absence of a problem. Hence two methods, and hence a missing label is
    UNKNOWN here rather than "no high integrity found, therefore fine".
    """
    name = "non_elevation"
    if os.name != "nt":
        return Result(name, UNKNOWN,
                      "not Windows; this artefact's elevation methods are "
                      "Win32-specific and were not evaluated")

    # Method A — Win32 elevation query.
    method_a: bool | None
    try:
        import ctypes
        method_a = bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        method_a = None

    # Method B — mandatory integrity label from the process token.
    rc, out, _ = _run(["whoami", "/groups"])
    method_b: bool | None = None
    label_sid = None
    if rc == 0:
        for line in out.splitlines():
            if "Mandatory Label" in line or "S-1-16-" in line:
                for token in line.split():
                    if token.startswith("S-1-16-"):
                        label_sid = token
                        break
            if label_sid:
                break
        if label_sid is not None:
            try:
                level = int(label_sid.rsplit("-", 1)[1])
            except (ValueError, IndexError):
                level = None
            if level is not None:
                # 8192 medium, 12288 high, 16384 system. High or above is
                # elevated.
                method_b = level >= 12288

    if method_a is None and method_b is None:
        return Result(name, UNKNOWN,
                      "neither method could evaluate: Win32 elevation query "
                      "unavailable and no mandatory integrity label found in "
                      "the process token")
    if method_a is None or method_b is None:
        got = "A" if method_b is None else "B"
        return Result(name, UNKNOWN,
                      f"only method {got} could evaluate; a single method is "
                      "not sufficient to establish non-elevation")
    if method_a != method_b:
        return Result(name, UNKNOWN,
                      f"methods disagree (Win32 elevated={method_a}, "
                      f"integrity label {label_sid} elevated={method_b}); "
                      "disagreement is not resolved by vote")
    if method_a:
        return Result(name, RED,
                      f"shell IS elevated; corroborated by both methods "
                      f"(Win32 elevation query, integrity label {label_sid})")
    return Result(name, GREEN,
                  f"shell is NOT elevated; corroborated by two independent "
                  f"methods — Win32 elevation query returned false and the "
                  f"token's mandatory integrity label is {label_sid} "
                  f"(below high integrity)")


# --------------------------------------------------------------------------
# Assertion 2 — ONNX / chromadb cache traversal, by read and not by existence.
# --------------------------------------------------------------------------
def assert_cache_traversal() -> Result:
    """Traverse to the extracted model and READ bytes from it.

    Existence is not the claim. The fault this replaces was an ACL on the
    extracted cache directory: the path existed and stat'd fine while the
    bytes were unreadable to the normal identity, so any check asserting
    presence alone reported green on a cache that failed at first query.
    """
    name = "cache_traversal"
    try:
        from chromadb.utils import embedding_functions
    except Exception as exc:  # import failure is UNKNOWN, not RED
        return Result(name, UNKNOWN,
                      f"chromadb could not be imported, so the cache location "
                      f"could not be derived ({type(exc).__name__})")

    cls = getattr(embedding_functions, "ONNXMiniLM_L6_V2", None)
    if cls is None:
        return Result(name, UNKNOWN,
                      "chromadb.utils.embedding_functions has no "
                      "ONNXMiniLM_L6_V2; cache location underivable")

    # Derive rather than hardcode: a hardcoded path that has moved reports
    # a confident RED about a cache that is actually fine.
    download_path = getattr(cls, "DOWNLOAD_PATH", None)
    extracted = getattr(cls, "EXTRACTED_FOLDER_NAME", "onnx")
    if download_path is None:
        home = pathlib.Path.home()
        download_path = (home / ".cache" / "chroma" / "onnx_models"
                         / PINNED_MODEL_NAME)
    cache_dir = pathlib.Path(download_path) / extracted

    if not cache_dir.is_dir():
        return Result(name, RED,
                      f"extracted model directory absent at {cache_dir}")

    try:
        entries = sorted(p for p in cache_dir.rglob("*") if p.is_file())
    except OSError as exc:
        return Result(name, UNKNOWN,
                      f"could not traverse {cache_dir}: {exc.__class__.__name__} "
                      f"— traversal denied is not evidence about the model")
    if not entries:
        return Result(name, RED, f"{cache_dir} contains no files")

    model_files = [p for p in entries if p.suffix == ".onnx"]
    target = model_files[0] if model_files else entries[0]
    try:
        with target.open("rb") as fh:
            head = fh.read(4096)
    except OSError as exc:
        # This is the ACL fault's signature: traversable, not readable.
        return Result(name, RED,
                      f"{target} could not be READ ({exc.__class__.__name__}); "
                      f"the path exists but its bytes are not available to "
                      f"this identity")
    if not head:
        return Result(name, RED, f"{target} read returned zero bytes")

    return Result(name, GREEN,
                  f"traversed {cache_dir} ({len(entries)} file(s)) and read "
                  f"{len(head)} bytes from {target.name}; model {PINNED_MODEL_NAME}")


# --------------------------------------------------------------------------
# Assertion 3 — services: container runtime, database port, vector store.
# --------------------------------------------------------------------------
def _vector_store_triple() -> tuple[str, str]:
    """exists / readable / WRITABLE — three conditions, each failing apart.

    Availability for this store is not a reachability question. The engine
    requires write access to serve reads, so a check confirming only
    existence, or only readability, reports green on a store that will
    fail at the first query.
    """
    if not INDEX_PATH.is_dir():
        return RED, f"vector store absent at {INDEX_PATH} (exists: no)"
    try:
        listing = sorted(p for p in INDEX_PATH.iterdir())
    except OSError as exc:
        return UNKNOWN, (f"vector store at {INDEX_PATH} exists but could not "
                         f"be listed ({exc.__class__.__name__})")
    readable_file = None
    for candidate in listing:
        if candidate.is_file():
            try:
                with candidate.open("rb") as fh:
                    fh.read(1)
                readable_file = candidate
                break
            except OSError:
                return RED, (f"vector store at {INDEX_PATH} exists but "
                             f"{candidate.name} is not readable")
    # Writability is the condition most often skipped and the one the
    # engine actually needs.
    probe = INDEX_PATH / f".preflight_write_probe_{os.getpid()}"
    try:
        with probe.open("wb") as fh:
            fh.write(b"preflight")
        probe.unlink()
    except OSError as exc:
        return RED, (f"vector store at {INDEX_PATH} exists and is readable "
                     f"but is NOT WRITABLE ({exc.__class__.__name__}); the "
                     f"engine needs write access to serve reads")
    read_note = (f"read 1 byte from {readable_file.name}"
                 if readable_file else "no regular file present to read")
    return GREEN, (f"vector store at {INDEX_PATH}: exists, readable "
                   f"({read_note}), and writable (probe written and removed)")


def assert_services() -> Result:
    name = "services"
    rc, out, err = _run(["docker", "ps", "--format", "{{.Names}}"])
    if rc is None:
        return Result(name, UNKNOWN,
                      "docker binary could not be executed; container runtime "
                      "state could not be evaluated")
    if rc != 0:
        return Result(name, RED,
                      f"docker ps exited {rc}: {(err or out).strip()[:200]}")
    containers = [ln.strip() for ln in out.splitlines() if ln.strip()]
    if not containers:
        return Result(name, RED,
                      "docker responded but no containers are running")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        sock.connect((DB_HOST, DB_PORT))
    except OSError as exc:
        return Result(name, RED,
                      f"database port {DB_HOST}:{DB_PORT} not reachable "
                      f"({exc.__class__.__name__}); containers running: "
                      f"{', '.join(containers)}")
    finally:
        sock.close()

    outcome, detail = _vector_store_triple()
    if outcome != GREEN:
        return Result(name, outcome,
                      f"container runtime up ({len(containers)} container(s)) "
                      f"and {DB_HOST}:{DB_PORT} reachable, but {detail}")
    return Result(name, GREEN,
                  f"container runtime up ({', '.join(containers)}); "
                  f"{DB_HOST}:{DB_PORT} reachable; {detail}")


# --------------------------------------------------------------------------
# Assertion 4 — conda environment identity.
# --------------------------------------------------------------------------
def assert_env_identity() -> Result:
    name = "env_identity"
    env = os.environ.get("CONDA_DEFAULT_ENV")
    version = ".".join(str(p) for p in sys.version_info[:3])
    if env is None:
        return Result(name, UNKNOWN,
                      f"CONDA_DEFAULT_ENV is unset, so environment identity "
                      f"could not be evaluated (interpreter reports {version})")
    if env != EXPECTED_CONDA_ENV or version != EXPECTED_PYTHON:
        return Result(name, RED,
                      f"expected env {EXPECTED_CONDA_ENV} / Python "
                      f"{EXPECTED_PYTHON}; found {env} / {version}")
    return Result(name, GREEN,
                  f"conda env {env}, Python {version}, interpreter "
                  f"{sys.executable}")


ASSERTIONS = [
    ("non_elevation", assert_non_elevation),
    ("cache_traversal", assert_cache_traversal),
    ("services", assert_services),
    ("env_identity", assert_env_identity),
]


def evaluate(provoke: str | None = None) -> list[Result]:
    """Run the assertions in ruled order, gating on assertion one.

    ``provoke`` forces one named assertion to UNKNOWN. It is a self-test
    facility for demonstrating that UNKNOWN does not collapse into green,
    and it can only ever degrade an outcome — there is no code path by
    which it makes any assertion greener, so it cannot manufacture a pass.
    """
    results: list[Result] = []
    gate_failed = False
    for name, fn in ASSERTIONS:
        if gate_failed:
            results.append(Result(
                name, SKIPPED,
                "not evaluated: non-elevation was not GREEN, and this "
                "assertion is read through that same token"))
            continue
        if provoke == name:
            res = Result(name, UNKNOWN,
                         "forced UNKNOWN by --provoke (self-test of the "
                         "non-collapse property)")
        else:
            res = fn()
        results.append(res)
        if name == "non_elevation" and res.outcome != GREEN:
            gate_failed = True
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", action="store_true",
                        help="machine-readable output")
    parser.add_argument("--provoke", choices=[n for n, _ in ASSERTIONS],
                        help="force one assertion to UNKNOWN (self-test)")
    args = parser.parse_args()

    results = evaluate(args.provoke)
    counts = {o: sum(1 for r in results if r.outcome == o)
              for o in (GREEN, RED, UNKNOWN, SKIPPED)}
    ok = counts[GREEN] == len(ASSERTIONS)

    if args.json:
        print(json.dumps({
            "regime": REGIME,
            "admissibility": "INADMISSIBLE as gate evidence, permanently",
            "results": [r.as_dict() for r in results],
            "counts": counts,
            "exit": 0 if ok else 1,
        }, indent=2))
    else:
        print(f"D2.2a PRE-FLIGHT [{REGIME}] — results are permanently "
              f"inadmissible as gate evidence")
        for r in results:
            print(f"  {r.outcome:<7} {r.name}: {r.detail}")
        if ok:
            print(f"PASS: 4/4 assertions GREEN — non-elevation corroborated "
                  f"by two methods, cache read not merely present, vector "
                  f"store exists/readable/writable, env identity confirmed "
                  f"[{REGIME}, inadmissible as gate evidence]")
        else:
            print(f"FAIL: {counts[GREEN]}/{len(ASSERTIONS)} GREEN "
                  f"(RED {counts[RED]}, UNKNOWN {counts[UNKNOWN]}, "
                  f"SKIPPED {counts[SKIPPED]}) — an UNKNOWN or SKIPPED "
                  f"assertion is not a pass and does not become one")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
