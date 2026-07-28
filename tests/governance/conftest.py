"""Fixtures for the governance trio + corpus suite.

Two engines, two roles — mirroring production:

* ``owner_engine`` (``arcaai_owner``): DDL, schema create/drop.
* ``app_engine`` (``arcaai_app``): runtime; SELECT + INSERT only.

DSNs default to the local dev values and are overridable for another
environment::

    ARCAAI_AUDIT_OWNER_DSN=postgresql+psycopg://arcaai_owner:...@localhost/arcaai_audit
    ARCAAI_AUDIT_APP_DSN=postgresql+psycopg://arcaai_app:...@localhost/arcaai_audit

Grants are applied by EXECUTING ``sql/governance_grants.sql`` — the file
CI and a deployment apply — not a copy of it. The previous conftest
carried a duplicate GRANT_SQL block while its docstring claimed the
file; if the two had drifted, the suite would have stayed green while
the database differed (2026-07-27 handover, observed item 1; fixed
per DEC-0014 consequences). Statements the runtime role cannot
prepare against a fresh test database (CREATE ROLE under a DO block,
database-level GRANT, DEFAULT PRIVILEGES) are executed best-effort:
they are bootstrap idempotent by design and may already hold.
"""

from __future__ import annotations

import os
import pathlib

import pytest
from sqlalchemy import create_engine, text

from arcaai.platform.governance.audit import AuditStore
from arcaai.platform.governance.models import AuditBase

OWNER_DSN = os.environ.get(
    "ARCAAI_AUDIT_OWNER_DSN",
    "postgresql+psycopg://arcaai_owner:owner_dev@localhost:5432/arcaai_audit",
)
APP_DSN = os.environ.get(
    "ARCAAI_AUDIT_APP_DSN",
    "postgresql+psycopg://arcaai_app:app_dev@localhost:5432/arcaai_audit",
)

# The grants file, resolved from the repo root (three levels up from
# tests/governance/conftest.py). One source; no inline copy.
GRANTS_FILE = pathlib.Path(__file__).resolve().parents[2] / "sql" / "governance_grants.sql"


def _split_grant_statements(sql: str) -> list[str]:
    """Comments removed FIRST — a semicolon inside a comment must never
    manufacture a statement (the 2026-07-28 first cut split before
    stripping and executed comment fragments, aborting the
    transaction). Then the DO $$ block as one unit, then plain splits."""
    text = "\n".join(
        ln for ln in sql.splitlines() if not ln.strip().startswith("--")
    )
    statements: list[str] = []
    if "DO $$" in text:
        pre, block_and_rest = text.split("DO $$", 1)
        block, text = block_and_rest.split("$$;", 1)
        statements.extend(pre.split(";"))
        statements.append("DO $$" + block + "$$")
    statements.extend(text.split(";"))
    return [s.strip() for s in statements if s.strip()]


def _apply_grants(engine) -> None:
    statements = _split_grant_statements(GRANTS_FILE.read_text(encoding="utf-8"))
    # The table-level GRANT and REVOKE are what the suite depends on;
    # they must apply and a failure raises. Bootstrap statements (role
    # creation, database-level grant, default privileges) may already
    # hold or be unexecutable in a given environment — each runs in its
    # own transaction so a benign failure cannot poison the rest.
    for statement in statements:
        critical = statement.upper().startswith(("GRANT SELECT", "REVOKE"))
        try:
            with engine.begin() as conn:
                conn.execute(text(statement))
        except Exception:
            if critical:
                raise


@pytest.fixture(scope="session")
def owner_engine():
    engine = create_engine(OWNER_DSN)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def _schema(owner_engine):
    """Fresh schema per test session; grants applied from the file."""
    AuditBase.metadata.drop_all(owner_engine)
    AuditBase.metadata.create_all(owner_engine)
    _apply_grants(owner_engine)
    yield


@pytest.fixture(scope="session")
def app_engine(_schema):
    engine = create_engine(APP_DSN)
    yield engine
    engine.dispose()


@pytest.fixture()
def store(app_engine) -> AuditStore:
    return AuditStore(app_engine)
