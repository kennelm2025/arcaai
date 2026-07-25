"""Execution metadata — the reproducibility fingerprint (RAT-02 spec section 4).

Captured once at wrapper entry, immutable thereafter, written to the run
record, and consumed directly by the B9 nondeterminism register.

Two disciplines from the spec, both load-bearing:

* **Unpopulated fields are ``None`` (SQL ``NULL``), never ``""`` and
  never a sentinel.** Downstream code must be able to distinguish "this
  stage had not landed when the run executed" from "a value was recorded
  and it was blank". The one deliberate exception is ``code_sha``, whose
  fallback value ``"unknown"`` is legible only because
  ``code_sha_source`` records that the fallback was taken.
* ``code_sha`` is injected at build time via ``ARCAAI_CODE_SHA``; where
  it cannot be resolved the value is ``"unknown"`` and
  ``code_sha_source`` is ``"fallback"`` — a run whose provenance is
  unknown must be identifiable as such rather than indistinguishable
  from one that was never asked.

Note the import below: ``platform`` here is the *standard library*
module. It resolves correctly precisely because this package lives at
``arcaai.platform.governance`` rather than top-level ``platform`` —
DEC-0013 exists so that this line can work.
"""

from __future__ import annotations

import os
import platform  # stdlib — see module docstring / DEC-0013
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from .events import SCHEMA_VERSION

#: Environment variable carrying the build-time code SHA (spec section 10.2).
CODE_SHA_ENV_VAR = "ARCAAI_CODE_SHA"

#: Environment variable naming the active conda env, set by conda itself.
CONDA_ENV_VAR = "CONDA_DEFAULT_ENV"


class ExecutionMetadata(BaseModel):
    """Frozen fingerprint of a governed run (spec section 4 table)."""

    model_config = ConfigDict(frozen=True)

    code_sha: str
    code_sha_source: str  # "build" | "fallback"
    env_id: str
    schema_version: str = SCHEMA_VERSION

    # Nullable-until-available (spec section 4): declared now, populated
    # as stages land, so the schema does not change under B7 and B8.
    model_artifacts: Mapping[str, Any] | None = None  # from B5 provenance
    llm_pin: str | None = None  # TI7 pin, actual not intended
    prompt_version: str | None = None  # null until B8 prompt registry
    corpus_version: str | None = None  # null until B7 corpus manifest
    retrieval_config: Mapping[str, Any] | None = None  # null until B7


def utcnow() -> datetime:
    """UTC now at microsecond resolution (spec section 4: timestamps are UTC)."""
    return datetime.now(UTC)


def capture_execution_metadata(
    *,
    model_artifacts: Mapping[str, Any] | None = None,
    llm_pin: str | None = None,
    prompt_version: str | None = None,
    corpus_version: str | None = None,
    retrieval_config: Mapping[str, Any] | None = None,
    environ: Mapping[str, str] | None = None,
) -> ExecutionMetadata:
    """Capture the fingerprint. Called exactly once, by the wrapper, at entry.

    ``environ`` is injectable for tests; production callers leave it
    defaulted to ``os.environ``.
    """
    env = os.environ if environ is None else environ

    code_sha = env.get(CODE_SHA_ENV_VAR)
    if code_sha:
        code_sha_source = "build"
    else:
        # Never a silent blank (spec section 4): the fallback is a value,
        # and the fact it was taken is itself recorded.
        code_sha = "unknown"
        code_sha_source = "fallback"

    conda_env = env.get(CONDA_ENV_VAR) or "unknown-env"
    env_id = f"{conda_env}/py{platform.python_version()}"

    return ExecutionMetadata(
        code_sha=code_sha,
        code_sha_source=code_sha_source,
        env_id=env_id,
        model_artifacts=model_artifacts,
        llm_pin=llm_pin,
        prompt_version=prompt_version,
        corpus_version=corpus_version,
        retrieval_config=retrieval_config,
    )


__all__ = [
    "CODE_SHA_ENV_VAR",
    "CONDA_ENV_VAR",
    "ExecutionMetadata",
    "capture_execution_metadata",
    "utcnow",
]
