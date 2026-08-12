"""Fixtures for the governance trio + corpus suite.

Two engines, two roles — mirroring production:

* ``owner_engine`` (``arcaai_owner``): DDL, schema create/drop.
* ``app_engine`` (``arcaai_app``): runtime; SELECT + INSERT only.

DSNs default to the local dev values and are overridable for another
environment::

    ARCAAI_AUDIT_OWNER_DSN=postgresql+psycopg://arcaai_owner:...@localhost/arcaai_audit_test
    ARCAAI_AUDIT_APP_DSN=postgresql+psycopg://arcaai_app:...@localhost/arcaai_audit_test

The suite runs against ``arcaai_audit_test`` and never against the
governed ``arcaai_audit`` (DEC-0016). Until 2026-08-12 these defaults
named the governed database and the session-scoped schema fixture below
ran ``drop_all`` against it as ``arcaai_owner``, so every run of the
mandatory battery erased every audit event and every corpus_version row
*before the first test executed* — WS-E 65, which corrects WS-E 61's
reading of the same residue as tests failing to clean up afterwards.
They did not fail to clean up; they destroyed beforehand.

The default is not the control. A default is a value an environment may
override, and an override pointing back at the governed database would
re-arm exactly the destruction this separation removes.
``_refuse_unless_disposable`` is the control.

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

# The suite's own store, disposable by construction. The governed store
# is ``arcaai_audit`` and is never a target here (DEC-0016).
TEST_DB_NAME = "arcaai_audit_test"

OWNER_DSN = os.environ.get(
    "ARCAAI_AUDIT_OWNER_DSN",
    f"postgresql+psycopg://arcaai_owner:owner_dev@localhost:5432/{TEST_DB_NAME}",
)
APP_DSN = os.environ.get(
    "ARCAAI_AUDIT_APP_DSN",
    f"postgresql+psycopg://arcaai_app:app_dev@localhost:5432/{TEST_DB_NAME}",
)

# The grants file, resolved from the repo root (three levels up from
# tests/governance/conftest.py). One source; no inline copy.
GRANTS_FILE = pathlib.Path(__file__).resolve().parents[2] / "sql" / "governance_grants.sql"


def _split_grant_statements(sql: str) -> list[str]:
    """Comments removed FIRST — a semicolon inside a comment must never
    manufacture a statement (the 2026-07-28 first cut split before
    stripping and executed comment fragments, aborting the
    transaction). Then every DO $$ block as one unit, then plain splits.

    The loop replaced a single-block ``if`` on 2026-08-12 (DEC-0016),
    when the grants file gained a second DO block for the run-time
    CONNECT grant. The ``if`` would have passed the second block through
    the plain semicolon split and executed its fragments — a parser
    correct only for the shape it was written against, which is the
    check-method defect family in miniature.
    """
    text = "\n".join(
        ln for ln in sql.splitlines() if not ln.strip().startswith("--")
    )
    statements: list[str] = []
    while "DO $$" in text:
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


def _refuse_unless_disposable(engine) -> None:
    """Fail closed unless this engine points at the disposable test
    database — CL-24 scope part (b), the write-path guard, ruled at
    DEC-0016.

    Checked on the engine's own URL rather than on the DSN constants
    above. The constants record what we intended to connect to; the URL
    is what will actually be dropped or written, and WS-E 65 is an
    incident in which the two were assumed to be the same thing. An
    environment override aimed at the governed database is the expected
    way this fires, and it must fire loudly rather than proceed.
    """
    name = engine.url.database or "<no database in URL>"
    if name != TEST_DB_NAME:
        raise RuntimeError(
            f"governance suite refused to run against database {name!r}. This suite "
            f"drops and recreates its schema, so it may target {TEST_DB_NAME!r} and "
            f"nothing else; the governed store is never a test target. Point "
            f"ARCAAI_AUDIT_OWNER_DSN and ARCAAI_AUDIT_APP_DSN at the test database, "
            f"creating it per infra/postgres-init/02-create-audit-databases.sql if it "
            f"does not exist. See DEC-0016 and WS-E 65."
        )


@pytest.fixture(scope="session")
def owner_engine():
    engine = create_engine(OWNER_DSN)
    _refuse_unless_disposable(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def _schema(owner_engine):
    """Fresh schema per test session; grants applied from the file."""
    # Guarded again at the destructive site, not only at engine
    # construction. WS-E 64's lesson is that stated coverage is a claim
    # about wiring: the check belongs where the damage would be done.
    _refuse_unless_disposable(owner_engine)
    AuditBase.metadata.drop_all(owner_engine)
    AuditBase.metadata.create_all(owner_engine)
    _apply_grants(owner_engine)
    yield


@pytest.fixture(scope="session")
def app_engine(_schema):
    engine = create_engine(APP_DSN)
    # The app role cannot drop, but it can INSERT, and app-role inserts
    # into the governed store are precisely the fixture rows WS-E 61
    # found there.
    _refuse_unless_disposable(engine)
    yield engine
    engine.dispose()


@pytest.fixture()
def store(app_engine) -> AuditStore:
    return AuditStore(app_engine)
