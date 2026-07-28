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

GRANT CONNECT ON DATABASE arcaai_audit TO arcaai_app;
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
