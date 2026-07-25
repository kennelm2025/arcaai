"""Fixtures for the governance trio suite.

Two engines, two roles — mirroring production:

* ``owner_engine`` (``arcaai_owner``): DDL, schema create/drop.
* ``app_engine`` (``arcaai_app``): runtime; SELECT + INSERT only.

DSNs default to the local dev values and are overridable for another
environment (e.g. Mike's B1 Postgres on Windows)::

    ARCAAI_AUDIT_OWNER_DSN=postgresql+psycopg://arcaai_owner:...@localhost/arcaai_audit
    ARCAAI_AUDIT_APP_DSN=postgresql+psycopg://arcaai_app:...@localhost/arcaai_audit
"""

from __future__ import annotations

import os

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

GRANT_SQL = """
GRANT USAGE ON SCHEMA public TO arcaai_app;
GRANT SELECT, INSERT
    ON audit_run, audit_run_terminal, audit_event, audit_payload
    TO arcaai_app;
REVOKE UPDATE, DELETE, TRUNCATE
    ON audit_run, audit_run_terminal, audit_event, audit_payload
    FROM arcaai_app;
"""


@pytest.fixture(scope="session")
def owner_engine():
    engine = create_engine(OWNER_DSN)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def _schema(owner_engine):
    """Fresh schema per test session, grants applied per sql/governance_grants.sql."""
    AuditBase.metadata.drop_all(owner_engine)
    AuditBase.metadata.create_all(owner_engine)
    with owner_engine.begin() as conn:
        for statement in GRANT_SQL.strip().split(";"):
            if statement.strip():
                conn.execute(text(statement))
    yield


@pytest.fixture(scope="session")
def app_engine(_schema):
    engine = create_engine(APP_DSN)
    yield engine
    engine.dispose()


@pytest.fixture()
def store(app_engine) -> AuditStore:
    return AuditStore(app_engine)
