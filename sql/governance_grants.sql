-- Governance trio + corpus snapshot — roles and grants
-- (RAT-02 spec section 5; corpus_version per DEC-0014).
--
-- Two roles:
--   arcaai_owner : owns the schema, runs DDL. Not used at runtime.
--   arcaai_app   : the application role. SELECT and INSERT only —
--                  no UPDATE, no DELETE, on any audit table. This is
--                  the append-only property as a database fact rather
--                  than a code-review convention; the test suite
--                  asserts an UPDATE under this role fails.
--
-- Run as a superuser (or the database owner) against the target
-- database after the tables exist. Passwords here are placeholders for
-- the reference build; a deployment sets its own.
--
-- Idempotent: safe to re-run.

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'arcaai_owner') THEN
        CREATE ROLE arcaai_owner LOGIN PASSWORD 'owner_dev';
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'arcaai_app') THEN
        CREATE ROLE arcaai_app LOGIN PASSWORD 'app_dev';
    END IF;
END
$$;

-- Database-level grant resolved at run time, not hardcoded (DEC-0016).
-- This file is applied both to the governed database arcaai_audit and
-- to the disposable arcaai_audit_test that the governance suite
-- targets; a literal name grants CONNECT on the wrong database when the
-- file is applied to the other, and the app role then survives only on
-- PUBLIC's default CONNECT. One artefact serves both databases — a
-- forked copy is the duplication failure DEC-0014's consequences
-- already fixed once here.
DO $$
BEGIN
    EXECUTE format('GRANT CONNECT ON DATABASE %I TO arcaai_app', current_database());
END
$$;
GRANT USAGE ON SCHEMA public TO arcaai_app;

-- The whole runtime grant. Nothing else.
GRANT SELECT, INSERT
    ON audit_run, audit_run_terminal, audit_event, audit_payload,
       corpus_version
    TO arcaai_app;

-- Belt and braces: strip anything wider that may have accumulated.
REVOKE UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER
    ON audit_run, audit_run_terminal, audit_event, audit_payload,
       corpus_version
    FROM arcaai_app;

-- No default privileges leaking future width to the app role.
ALTER DEFAULT PRIVILEGES FOR ROLE arcaai_owner IN SCHEMA public
    GRANT SELECT, INSERT ON TABLES TO arcaai_app;
