"""Unit coverage for the governance guard's deny layer.

FIRST TEST COVERAGE THIS MODULE HAS EVER HAD. Every deny in this
repository lives in ``DENY_COMMAND_RES`` in ``.claude/hooks/
governance_guard.py`` — force push, history rewrite, recursive force
delete, force branch delete — and until this file none of them was
asserted by a test. The enforcement path was verified only by live
probes, which are the stronger evidence but do not run in CI and cannot
catch a regression introduced between sessions.

Written for the Option B pairing ruled 2026-08-14 (queue item 27 arc).
Amendment 3 restored the read-class families deferred at amendment 2,
and two of them are not reads: ``find`` reaches deletion and arbitrary
execution, ``sort`` reaches file creation. The ruling was to grant them
as deferred and pair each with a deny on its write forms.

AUTHORING EVIDENCE IS NOT PROBE EVIDENCE, and this file must not be
read as closing the loop. A test asserts that a pattern matches a
string; it says nothing about whether the guard is wired, whether the
matcher routes the tool, or whether an allow rule pre-empts the deny.
WS-E 64 is three days of a guard that was correct and unreachable. The
live probes are owed at Phase 2 and are ruled, not optional.

BOTH DIRECTIONS ARE TESTED, because this repository's defect register
carries both polarities. A deny that misses a mid-line flag is the
false green H-11 exists to prevent; a deny that fires on an innocent
filename is a false red, and item 25 records one of those shipping in
``check_docs.py``.

Known limitations are asserted as tests rather than described in prose,
so that a change in behaviour fails loudly instead of quietly widening
or narrowing the deny. See ``test_known_limitation_*`` below.
"""

from __future__ import annotations

import importlib.util
import pathlib

import pytest

GUARD_PATH = (
    pathlib.Path(__file__).resolve().parents[2]
    / ".claude" / "hooks" / "governance_guard.py"
)


def _load_guard():
    """Load the guard by path.

    It is a hook script rather than an importable package member, so
    there is no module path to import. Resolved from this file's own
    location, never from the working directory — the guard itself made
    that correction at WS-E 68, where an ambient cwd changed what an
    enforcement path resolved against.
    """
    spec = importlib.util.spec_from_file_location("governance_guard", GUARD_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


guard = _load_guard()


def denied_by(command: str) -> str | None:
    """Return the refusal message a command would draw, or None.

    Mirrors the loop in ``main`` so that the assertion is about the same
    structure the hook actually walks, rather than about one regex
    lifted out of it.
    """
    for pattern, message in guard.DENY_COMMAND_RES:
        if pattern.search(command):
            return message
    return None


# Write forms. Each MUST be denied. Mid-line placement is represented
# throughout, because a prefix-shaped rule would pass the first case of
# each family and miss the rest — which is why these denies are regexes
# in the guard and not permission rules in settings.json.
WRITE_FORMS = [
    "find . -delete",
    "find /tmp -type f -delete",
    "find . -name '*.tmp' -delete",
    "find . -exec rm {} ;",
    "find . -type f -exec rm {} +",
    "find . -execdir rm {} ;",
    "sort -o out.txt in.txt",
    "sort in.txt -o out.txt",
    "sort in.txt --output out.txt",
    "sort in.txt --output=out.txt",
]

# Read forms. Each MUST be allowed through, or the grant the pairing
# was built to protect is worthless.
READ_FORMS = [
    "find . -name '*.py'",
    "find . -type f",
    "find . -maxdepth 2 -name README.md",
    "sort in.txt",
    "sort -u in.txt",
    "sort -n in.txt",
    "grep -o pattern file.txt",
    "grep -rn pattern .",
    "head -20 in.txt",
    "wc -l in.txt",
]

# Adversarial near-misses: the flag text appears, but not as a flag.
# A deny that fires on any of these is a false red on ordinary work.
NEAR_MISSES = [
    "find /tmp -name file-delete.txt",
    "find . -name '*-delete*'",
    "find . -name deleted.txt",
    "find . -name exec-notes.txt",
    "sort report-o.txt",
    "sort my-output.txt",
    "sort outputs.txt",
    "ls -o",
]


@pytest.mark.parametrize("command", WRITE_FORMS)
def test_write_forms_are_denied(command: str) -> None:
    assert denied_by(command) is not None, (
        f"write form was NOT denied: {command!r}. A deny that misses a "
        f"mid-line flag is the false green H-11 exists to prevent."
    )


@pytest.mark.parametrize("command", READ_FORMS)
def test_read_forms_are_not_denied(command: str) -> None:
    assert denied_by(command) is None, (
        f"read form was denied: {command!r}. The read-class grant is the "
        f"point of the pairing; denying reads defeats it."
    )


@pytest.mark.parametrize("command", NEAR_MISSES)
def test_near_misses_are_not_denied(command: str) -> None:
    assert denied_by(command) is None, (
        f"flag text inside an ordinary token was treated as a flag: "
        f"{command!r}. That is a false red on innocent filenames."
    )


def test_known_limitation_quoted_flag_text_still_matches() -> None:
    """A flag inside a quoted argument matches. Documented, not fixed.

    A regex cannot see quoting. This is the false-red direction, which
    is the safe one for a deny — the operator route is named in the
    refusal message — and it is asserted here so that any future change
    to the pattern surfaces as a failing test rather than as a silent
    change in what the guard blocks.
    """
    assert denied_by('sort "notes -o draft.txt"') is not None


def test_known_limitation_combined_short_flags_not_matched() -> None:
    """``sort -ro out.txt`` reaches the output flag and is NOT denied.

    The ruled spec is short form plus long form. Covering clustered
    short flags means matching any cluster ending in ``o``, which
    false-reds on a leading-dash filename, so widening it is a decision
    rather than a patch. Asserted so the gap is visible in the suite
    instead of resting in a comment nobody runs.
    """
    assert denied_by("sort -ro out.txt") is None


# Regression cover for the denies that already existed. Not exhaustive:
# enough that an edit to the list which broke one of them fails here.
PRE_EXISTING_DENIES = [
    "git push --force origin main",
    "git push --force-with-lease origin main",
    "git filter-branch --tree-filter true HEAD",
    "rm -rf build",
    "git branch -D feature",
    "git branch --delete --force feature",
]


@pytest.mark.parametrize("command", PRE_EXISTING_DENIES)
def test_pre_existing_denies_still_fire(command: str) -> None:
    assert denied_by(command) is not None


def test_lowercase_branch_delete_is_not_denied() -> None:
    """``-d`` stays permitted; only ``-D`` and the long force form deny.

    The guard's own comment marks this pattern as case-sensitive on
    purpose: folding case here would silently revoke the ruled
    cleandown grant. This asserts the boundary that comment claims.
    """
    assert denied_by("git branch -d feature") is None
