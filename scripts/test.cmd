@echo off
cd /d "%~dp0.."
pytest --cov --cov-report=term-missing
