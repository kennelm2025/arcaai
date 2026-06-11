"""B1 smoke tests - prove the packages import and the version is coherent."""

import tomllib
from pathlib import Path


def test_packages_import() -> None:
    import agent  # noqa: F401
    import api  # noqa: F401
    import ingest  # noqa: F401
    import verticals  # noqa: F401


def test_version_matches_pyproject() -> None:
    from api.version import VERSION

    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["version"] == VERSION
