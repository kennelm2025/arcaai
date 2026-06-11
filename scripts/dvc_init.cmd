@echo off
rem One-time DVC initialisation with a local remote (B1). MinIO replaces this later.
cd /d "%~dp0.."
dvc init
dvc remote add -d localstore .dvcstore
git add .dvc .dvcignore
echo DVC initialised with local remote .dvcstore (gitignored). Commit when ready.
