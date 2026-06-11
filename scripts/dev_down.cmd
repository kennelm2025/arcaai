@echo off
cd /d "%~dp0.."
docker compose -f infra\docker-compose.dev.yml down
