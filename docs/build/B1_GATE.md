# B1 gate — Foundation

Per Build & Quality Plan v1.0. All boxes ticked = GATE PASSED in BUILD_TRACKER.md.

- [x] `pip install -e ".[dev]"` clean on Python 3.11
- [x] `scripts\lint.cmd` — ruff clean
- [x] `scripts\test.cmd` — all tests pass, coverage ≥ 60%
- [x] `scripts\dev_up.cmd` — postgres healthy, MLflow healthy
- [x] MLflow UI reachable at http://localhost:5000 (create experiment `arcaai-fraud`)
- [x] `scripts\dvc_init.cmd` run; `.dvc/` committed
- [x] CI: ci-devops + ci-mlops green on a test PR (or on main push)
- [x] BUILD_TRACKER.md B1 row updated; CURRENT_STATE.md updated; committed from repo
