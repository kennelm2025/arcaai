"""Test-capability harness (WS-T2 under DEC-0015).

Package init only — deliberately empty of runtime code at D2.1.

Placement is TOR-directed, not a fresh architecture call: TOR Section 4
names the module path literally as ``python -m arcaai.harness run
--spec <file>`` (D2.2b). ADR-0009's platform/vertical boundary is
silent on the harness — its Decision 1 table governs ML lifecycle
capabilities, and a test harness appears in neither column — so this
sits as a third sibling of ``arcaai/platform/`` rather than inside it.
The harness is neither platform machinery serving a request nor
vertical business semantics; it is the thing that tests both.

What lives here at D2.1: the scenario spec schema, and nothing else.
The runner, the CLI and the pre-flight artefact are D2.2a/D2.2b's to
build under their own gates — the schema is the keystone every one of
them hangs off, and it is authored first on purpose (TOR Section 9,
proof-first sequencing).
"""
