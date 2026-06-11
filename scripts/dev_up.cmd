@echo off
cd /d "%~dp0.."
docker compose -f infra\docker-compose.dev.yml up -d
echo.
echo Postgres: localhost:5432  ^|  MLflow UI: http://localhost:5000
docker compose -f infra\docker-compose.dev.yml ps
