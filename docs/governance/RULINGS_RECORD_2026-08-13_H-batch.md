# RULINGS RECORD — H-batch, Test Plan skeleton open rulings (2026-08-13)

Twelve dispositions ruled by the operator on 2026-08-13, in one act, against the
open-rulings table of the D1.1 Test Plan skeleton.

**Why this file exists.** The skeleton that raised these questions is a draft
held outside the repository, and before this record the twelve dispositions
existed only in a session transcript and in the body of PR #111. A twelve-part
ruling living in a pull-request description is the shape that goes missing:
descriptions are not registers, are not indexed, and are read once. Committed
here at operator ruling — "the twelve H-dispositions committed to a governed
home".

Register anchor: `REPO_MANIFEST.md` regenerated 2026-08-13, 0 divergences. **No
register number is consumed by this record.** It is a rulings record, not a DEC,
an ADR or a CL; where a disposition below implies a numbered artefact, the
number is read live at the arc that creates it.

## The ruling, verbatim

> "RULED: H-11 hardening in by mechanism; H-6 confirmed hard precondition; H-5
> opens v0.2 as versioned question; H-4 fresh authorship, RQA-001
> reference-only; H-9 and H-10 mechanical/machine-asserted; H-1 blindness
> mechanically verified, mechanism specified at topology ruling; H-2 sequenced
> as ADR-0011 arc before lane one hardens; H-3, H-7, H-8, H-12 deferred to
> proper stops."

## Dispositions

Each row restates the question in full, so this record is readable without the
skeleton that raised it.

### H-1 — Builder / spec-blind test-author separation

**Question.** TOR Rev C section 6 names three roles and is SILENT on any
separation between a builder and a spec-blind test-author. Is the separation
ruled, and is blindness merely asserted or mechanically verified?

**RULED: blindness mechanically verified; the mechanism is specified at the
topology ruling.** Assertion is not sufficient. A tool grant restricts writes
and does not prevent a read of implementation files, so a separation that
matters for evidence needs a mechanism rather than an instruction. What that
mechanism is belongs to H-2 and is not settled here.

**Consequence.** The `test-author` agent definition exists and is operational
while the topology authorising it is a draft. That ordering is now explicit
rather than tacit, and is resolved by H-2 landing first.

### H-2 — Agentic topology

**Question.** Does the topology land as ADR-0011, or as an extension of
ADR-0009? `docs/governance/ADR-candidate_agentic-topology_2026-08-12.md` is a
DRAFT candidate and ADR-0011 is unallocated.

**RULED: sequenced as an ADR-0011 arc, before lane one hardens.** The number is
allocated at that arc from the live register, never in advance.

### H-3 — DEC-0011 paraphrase scope

**Question.** Does DEC-0011's prohibition on paraphrasing OGL material reach
authored synthetic documents that restate statute in their own words, or only
the OGL extracts themselves? Raised as F-C at
`docs/governance/FINDINGS_2026-08-13_sg-listing-corpus-findings.md`.

**RULED: deferred to its proper stop.** Not blocking. Recorded as recurring —
it will arise for every synthetic document that characterises a statutory
provision, which is most of the corpus.

### H-4 — RQA-001 disposition

**Question.** Is RQA-001 promoted to a committed scenario, or is the first
committed scenario authored fresh under the ruled Test Plan?

**RULED: fresh authorship. RQA-001 is reference-only.** It remains Claude Code
authorship, admissible for the D2.2a spike alone, and is not promoted. Its
value is as an exemplar of shape.

### H-5 — `retrieval_snapshot_sha256` mandatory for retrieval-class

**Question.** Should the field, optional at schema v0.1, become mandatory for
retrieval-class scenarios? Raised as F2 in the CL-27 Commissioning Session
Record; carried at `CLAUDE.md` queue item 31.

**RULED: opens v0.2 as a versioned question.** Not an edit to v0.1, which is
immutable once merged; a new versioned schema file. The question is opened, not
answered — v0.2's content is decided at the arc that authors it.

### H-6 — Vector-store ownership repair

**Question.** Is repair of the `BUILTIN\\Administrators`-owned vector store
directory a hard precondition to the first Regime 2 run? Observed-not-raised in
the CL-27 record, where the writability probe succeeded only through an
inherited grant to authenticated users.

**RULED: confirmed hard precondition.** A store writable only by inheritance is
not an environment anybody deliberately configured, and Regime 2 asserts the
environment as an entry criterion. **The repair is an operator act at the
operator's own terminal** — the harness never elevates and never assumes the
owner role.

### H-7 — Inclusion act for SG-03..09

**Question.** Does the first Regime 2 run wait on the inclusion act for the
seven newly listed sector-guidance documents, or proceed on the eligible 16?

**RULED: deferred to its proper stop.** Note the current state: manifest
`2026-08-13.8` lists 30 documents with 16 eligible; SG-03..09 are at
`pending_review`, and inclusion is a separate governed act.

### H-8 — Acceptance evaluation under Regime 2

**Question.** What evaluates a scenario's `acceptance` threshold under Regime 2,
and where is the verdict recorded? The runner currently carries the threshold
with `evaluated: false` and a stated reason, correct under commissioning where
pass/fail is not an exit criterion.

**RULED: deferred to its proper stop.** Becomes live when Regime 2 does.

### H-9 — Regime-marker immutability

**Question.** Is the commissioning/formal regime marker immutable mechanically,
or by convention? TOR 5A requires the marker and is silent on its mutability.

**RULED: mechanical.** Convention is insufficient here for the same reason it is
insufficient anywhere in this repository: the marker is the sole barrier against
a commissioning result being read as gate evidence, and TOR 5A makes
inadmissibility permanent with no promotion path. A marker a process can edit is
a promotion path.

**Consequence.** Binds the D2.5 results ledger at its design, not afterwards.

### H-10 — Run-record obligations under Regime 2

**Question.** Must the three run-record obligations — corpus snapshot pinned and
stated, spec schema-valid, working tree state recorded — be machine-asserted
under Regime 2, or is an operator record sufficient as it was under Regime 1?

**RULED: machine-asserted.** Pre-flight green is one of four entry criteria and
the other three are currently human records. Under Regime 2 they are asserted by
the instrument.

**Consequence.** Runner work: the entry criteria become executable checks with
the same three-outcome discipline as the pre-flight, UNKNOWN exiting non-zero.

### H-11 — `-d` / `-D` matcher casing

**Question.** The Tier 1 grant of `git branch -d` (PR #109) assumed the matcher
distinguishes case. If it folds case, the grant reaches the force form, and a
Tier 1 allow pre-empts a Tier 2 guard ask.

**RULED: hardening in by mechanism. DISCHARGED at PR #111, merged `891caeb`.**
Force delete is now a guard DENY covering both `-D` and the long
`--delete --force` spelling in either order; the lowercase form remains granted.
Probed live and paired: the force form returned the guard's refusal, the
lowercase form ran.

**What the discharge does NOT establish, recorded so it is not later assumed:**
whether the matcher folds case remains open. Either the force form matched no
allow rule and the deny was uncontested, or it matched and the deny won. Only
the second would settle allow-versus-deny precedence, which `CLAUDE.md` records
as untested; the observation cannot separate the two. The practical risk is
closed under both readings.

**A standing-rule consequence, raised and not resolved.** `CLAUDE.md` says never
allow-list a command family that carries a deny. `git branch` now carries both a
Tier 1 allow and a deny — the first instance of the shape that rule warns
against, sanctioned by this ruling and with the deny observed to hold. Whether
the rule is amended, narrowed to families where allow and deny could match the
same string, or left as written with this recorded as its exception, is
undecided.

### H-12 — Amendment 9's actual content

**Question.** TOR Rev C attributes two different requirements to amendment 9:
defect routing at its line 49, and pinning to the corpus snapshot current at
spike time at its line 57. Which is it?

**RULED: deferred to its proper stop.** Resolvable only against
`docs/governance/RULINGS_RECORD_2026-08-10_TOR-test-capability.md`, which has
not been read in full and is binding on D1.1 — the nine amendments are accepted
onto D1.1/D2.1 requirements and this skeleton knows them only through the TOR's
parenthetical summaries.

## Summary

| # | Subject | Disposition | State |
|---|---|---|---|
| H-1 | spec-blind separation | blindness mechanically verified | mechanism at H-2 |
| H-2 | agentic topology | ADR-0011 arc, before lane one hardens | sequenced |
| H-3 | DEC-0011 paraphrase scope | deferred | open |
| H-4 | RQA-001 | fresh authorship, reference-only | closed |
| H-5 | snapshot pin at v0.2 | opens v0.2 as versioned question | open, scoped |
| H-6 | vector-store ownership | confirmed hard precondition | operator act owed |
| H-7 | SG-03..09 inclusion | deferred | open |
| H-8 | acceptance evaluation | deferred | open |
| H-9 | regime-marker immutability | mechanical | binds D2.5 design |
| H-10 | run-record obligations | machine-asserted | binds runner work |
| H-11 | `-d` / `-D` casing | hardening in by mechanism | **DISCHARGED, PR #111** |
| H-12 | amendment 9 content | deferred | open |

One of twelve discharged. Two bind future design (H-9, H-10). Two are sequenced
(H-1, H-2). One is an operator act (H-6). Four are deferred (H-3, H-7, H-8,
H-12). One is closed by decision (H-4). One is scoped open (H-5).
