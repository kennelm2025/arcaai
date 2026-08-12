-- Governance audit databases: the governed store and the disposable
-- test store (DEC-0016).
--
--   arcaai_audit       the governed store. Real audit events, real
--                      corpus_version pins, and from D2.2a the
--                      Commissioning Session Records. Never a test
--                      target.
--   arcaai_audit_test  what tests/governance/* targets. The suite drops
--                      and recreates its schema on every run, so this
--                      database is disposable by construction.
--
-- Both existed only out-of-band before this file: arcaai_audit was
-- created by hand on the operator machine and by a CREATE DATABASE line
-- in .github/workflows/ci-devops.yml, and nothing in the dev stack
-- created it — a fresh pgdata volume produced a stack the governance
-- suite could not run against, with no artefact saying why. This file
-- closes that gap on the pattern 01-create-mlflow-db.sql already set.
--
-- IMPORTANT — this runs ONLY on a fresh pgdata volume. Postgres executes
-- /docker-entrypoint-initdb.d exclusively at cluster initialisation, so
-- an existing volume never sees it. On a machine whose stack predates
-- this file, create the missing database once, by hand:
--
--   docker exec arcaai-dev-postgres-1 psql -U arcaai -d postgres \
--     -c "CREATE DATABASE arcaai_audit_test OWNER arcaai_owner;"
--
-- Roles first: CREATE DATABASE ... OWNER requires the role to exist.
-- Idempotent, and deliberately the same shape as the block in
-- sql/governance_grants.sql, which applies the table-level grants once
-- the tables exist.
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

-- CREATE DATABASE has no IF NOT EXISTS and cannot run inside a DO
-- block; on the fresh volume this file is written for, neither exists.
CREATE DATABASE arcaai_audit OWNER arcaai_owner;
CREATE DATABASE arcaai_audit_test OWNER arcaai_owner;
