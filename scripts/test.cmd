@echo off
cd /d "%~dp0.."
REM Local/CI parity: CI lints before testing, so this script must too
REM (B4 inc2 lesson - an unused import passed local green, failed both PRs).
ruff check . || exit /b 1
pytest --cov --cov-report=term-missing
