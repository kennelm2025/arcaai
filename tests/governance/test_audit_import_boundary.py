"""CF-1/B7-c mechanical leg: direct audit access is a composition-root
concern. The audit module (AuditStore and friends) may be imported
only from the governance package itself, composition roots (the api
service layer, the operator runner), and tests. Vertical and agent
code reach governance exclusively through events/wrapper - so no
vertical or agent module can write audit records directly, which is
the conforms-if of CF-1/B7-c made grep-mechanical.

Same discipline and shape as tests/retrieval/test_import_boundary.py
(CF-1/B7-a, chromadb).
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Composition roots and the package itself. Everything else is an
# offender, agent/ and verticals/ above all.
ALLOWED_PREFIXES = (
    "arcaai/platform/governance",
    "api",
    "scripts",
    "tests",
)

PATTERN = re.compile(
    r"from\s+arcaai\.platform\.governance\.audit\s+import"
    r"|import\s+arcaai\.platform\.governance\.audit"
    r"|from\s+arcaai\.platform\.governance\s+import\s+[^\n]*\bAuditStore\b"
)

SCAN_DIRS = (
    "agent",
    "api",
    "arcaai",
    "contracts",
    "ingest",
    "scripts",
    "verticals",
)


def _allowed(rel: str) -> bool:
    return any(
        rel == p or rel.startswith(p + "/") for p in ALLOWED_PREFIXES
    )


def test_audit_imports_only_from_composition_roots():
    offenders = []
    for d in SCAN_DIRS:
        base = REPO_ROOT / d
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            rel = path.relative_to(REPO_ROOT).as_posix()
            if _allowed(rel):
                continue
            if PATTERN.search(path.read_text(encoding="utf-8")):
                offenders.append(rel)
    assert offenders == [], (
        "direct audit imports outside composition roots: "
        f"{offenders} - vertical and agent code reaches governance "
        "through events/wrapper only (CF-1/B7-c)"
    )
