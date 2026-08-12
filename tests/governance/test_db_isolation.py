"""The test/governed store separation, exercised rather than asserted in
prose (CL-24, ruled at DEC-0016; mechanism recorded at WS-E 65).

These tests deliberately need no database. ``create_engine`` does not
connect, so the guard can be put under a real target it must refuse
without anyone having to point a live suite at the governed store to
find out. WS-E 64 is the case for exercising a control rather than
describing it: there, a guard's stated coverage was a claim about its
patterns rather than about its wiring, and the wiring was absent for
three days.
"""

from __future__ import annotations

import pytest
from conftest import (
    APP_DSN,
    OWNER_DSN,
    TEST_DB_NAME,
    _refuse_unless_disposable,
    _split_grant_statements,
)
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url

GOVERNED_DB_NAME = "arcaai_audit"


def _engine_for(database: str):
    """An engine pointed at ``database``. Never connected — construction
    is enough for the guard, which reads the URL."""
    return create_engine(f"postgresql+psycopg://arcaai_owner:owner_dev@localhost:5432/{database}")


@pytest.mark.parametrize("dsn,label", [(OWNER_DSN, "owner"), (APP_DSN, "app")])
def test_resolved_dsn_is_the_disposable_store(dsn: str, label: str) -> None:
    """Whatever the environment resolves to, it is not the governed store.

    Asserted on the resolved DSN rather than on the default string: an
    override is exactly the case that matters, and the default is
    structurally guaranteed by being built from TEST_DB_NAME.
    """
    database = make_url(dsn).database
    assert database == TEST_DB_NAME, f"{label} DSN resolved to {database!r}"
    assert database != GOVERNED_DB_NAME


def test_guard_refuses_the_governed_store() -> None:
    with pytest.raises(RuntimeError) as excinfo:
        _refuse_unless_disposable(_engine_for(GOVERNED_DB_NAME))
    message = str(excinfo.value)
    # The refusal has to name what it refused and what it wanted, or the
    # operator reads a stack trace instead of an instruction.
    assert GOVERNED_DB_NAME in message
    assert TEST_DB_NAME in message


def test_guard_refuses_a_neighbouring_name() -> None:
    """Equality, not a substring test. ``arcaai_audit_test_scratch``
    contains the permitted name and is still not it."""
    with pytest.raises(RuntimeError):
        _refuse_unless_disposable(_engine_for(f"{TEST_DB_NAME}_scratch"))


def test_guard_accepts_the_disposable_store() -> None:
    _refuse_unless_disposable(_engine_for(TEST_DB_NAME))


def test_grant_splitter_keeps_every_do_block_whole() -> None:
    """Two DO blocks now, and the splitter's single-block ``if`` would
    have fed the second through the plain semicolon split (DEC-0016)."""
    sql = """
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'r') THEN
            CREATE ROLE r LOGIN PASSWORD 'p';
        END IF;
    END
    $$;

    GRANT SELECT ON t TO r;

    DO $$
    BEGIN
        EXECUTE format('GRANT CONNECT ON DATABASE %I TO r', current_database());
    END
    $$;
    """
    statements = _split_grant_statements(sql)
    blocks = [s for s in statements if s.startswith("DO $$")]
    assert len(blocks) == 2, statements
    # A fragment is the failure mode: a bare BEGIN or a dangling END IF
    # standing alone as its own statement.
    assert not [s for s in statements if s in {"BEGIN", "END", "END IF"}], statements
    assert any(s.startswith("GRANT SELECT") for s in statements)


def test_grant_file_carries_no_hardcoded_database_name() -> None:
    """The database-level GRANT resolves through current_database(), so
    one grants artefact serves both stores instead of forking."""
    import pathlib

    grants = (
        pathlib.Path(__file__).resolve().parents[2] / "sql" / "governance_grants.sql"
    ).read_text(encoding="utf-8")
    body = "\n".join(
        ln for ln in grants.splitlines() if not ln.strip().startswith("--")
    )
    assert "current_database()" in body
    assert f"ON DATABASE {GOVERNED_DB_NAME}" not in body
