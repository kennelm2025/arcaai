@echo off
cd /d "%~dp0.."
docker info >nul 2>&1
if errorlevel 1 (
    echo [dev_up] Docker Desktop is not running. Start it from the Start menu, wait for the tray whale, then re-run this script.
    exit /b 1
)
docker compose -f infra\docker-compose.dev.yml up -d
echo.
echo Postgres: localhost:5432  ^|  MLflow UI: http://localhost:5000
docker compose -f infra\docker-compose.dev.yml ps
