# COMMISSIONING SESSION RECORD — D2.2a runner spike

**RULED AND COMMITTED.** Claims **CL-27**, cited from the session register anchor:
`REPO_MANIFEST.md` regenerated 2026-08-13 12:00 UTC (DEC next 0018, ADR next 0011,
CL next 27, WS-E next 69, 0 divergences).

*This is a **record**, not a report. It carries no pass/fail summary. Under the
D2.0 commissioning frame, results recorded here are **permanently inadmissible
as gate evidence**, and the naming is deliberate: a report format invites
promotion by osmosis. First instance of the form, per the 2026-08-11 reporting
ruling at `docs/governance/SESSION_HANDOVER_2026-08-11d.md`.*

- **Date:** 2026-08-13 · **Session:** A · **Regime:** COMMISSIONING
- **Arc:** queue item 30, D2.2a runner spike, under DEC-0017 build-first right of way
- **Branch:** `commissioning/d22a-spike-cl27`, base `b7effc371429687ee9faefe8896536e85a943afc`
- **Runner commit:** `7bad3b71f44e56ba4138a562d93fd54c6d4e0948`

## 1. Exit criterion — stated before the evidence

**The scenario's own pass/fail is NOT an exit criterion. Reproducibility IS.**

Queue item 30 fixes the exit criterion as a result JSON reproducible from its
triple. RQA-001 scored recall_at_k 0.0 and that is recorded as a finding (F1),
not as a failure of this spike. Nothing was tuned to produce a match.

## 2. Rulings, verbatim

**Ruling 1 — arc naming (operator, 2026-08-13).** Discharges the `/session-open`
arc-selection task and the DEC-0017 arc-selection step.

> "Arc is queue item 30, D2.2a runner spike. If no D2.2a scenario spec exists on
> main, CC drafts a minimal scenario spec against spec schema v0.1 as a
> COMMISSIONING draft, clearly labelled, validated, and presented at the Step 6
> gate for Mike's ruling before any spike execution."

**Ruling 2 — four-part gate ruling (operator, verbatim).**

> "RULED: draft accepted for Commissioning; snapshot pin ruled in for this
> spike, schema question recorded; bit_identical accepted; scope restated as
> runner construction, proceed."

Consequences carried: RQA-001 is admissible for THIS spike only and remains
Claude Code authorship; the retrieval_snapshot_sha256 in-pin is spike-scoped;
the v0.2 mandatory question is a recorded finding, not settled; scope is runner
construction from nothing, minimal.

**Ruling 3 — arc close (operator, verbatim).** Recorded in full at section 9.

## 3. Entry criteria — four evidence lines

| # | Criterion | Evidence |
|---|---|---|
| 1 | Pre-flight GREEN | `scripts/d22a_preflight.py` 4/4 GREEN, exit 0: non-elevation corroborated by two methods (integrity label S-1-16-8192); cache traversal read 4096 bytes from model.onnx across 6 files; services — both containers up, port 5432 reachable, vector store exists, readable and writable; env identity arcaai, Python 3.11.15 |
| 2 | Corpus snapshot pinned and stated | SNAPSHOT PINNED: `2026-08-06.7` / `97ca36dda960ed31c368c1a4acde04b720926bf4e3ee92ae98b95d65cc340b6a` — read from `verticals/fraud/corpus/MANIFEST.yaml` via the DEC-0014 machinery, not from a summary. retrieval_snapshot_sha256 `878b3439e8261e850510c7ea7b5d0e67655ee2eb3b34427a8d7c2b256d6ab928`; 23 documents, 16 eligible. Governed store read directly: corpus_version row count 0 |
| 3 | Scenario spec schema-valid against v0.1 | SPEC VALID: `9cad22fc9cf3624c228907fb493bdfd6d08668ffe4dc2032910318b308daa1e8` — drafted under Ruling 1 because none existed (F3). Draft202012Validator reported 0 errors; all three pins recomputed against the live manifest and matched; validator discrimination proved by five deny-shaped mutations, all rejected |
| 4 | Working tree state recorded | TREE STATE: `b7effc371429687ee9faefe8896536e85a943afc`, CLEAN — `git status --porcelain` empty at gate time. The draft spec was written outside the repository, so no uncommitted artefact existed in the tree |

## 4. Runner construction

`arcaai/harness/runner.py`, 392 insertions, committed at `7bad3b7`. Before this
spike `arcaai/harness/` held only `arcaai/harness/__init__.py` and the v0.1
schema at `arcaai/harness/schema/scenario_spec_v0.1.schema.json` — no runner, no
validator entry point, no result writer (F3).

Four things, no more: validate a spec against schema v0.1; recompute the corpus
pins from the live manifest and compare; query the corpus at the pinned
snapshot; emit a result JSON.

**Boundary disciplines held, each verified rather than asserted:**

- **ChromaStore-only (CF-1/B7-a).** chromadb is not imported in the runner; the
  store arrives through ChromaStore, the single permitted adapter. The adapter
  import is deliberately deferred into the run path so that a spec or pin
  refusal does not pay the ONNX warm-up cost.
- **No vertical defaults (ADR-0009).** Nothing imports from the verticals tree.
  The manifest path, index path and output directory are all required
  arguments; the collection name is passed through only when the caller
  supplies one, so no vertical-shaped string appears in the file.
- **Distinct refusal codes.** 2 spec-invalid, 3 pin-diverged, 4 index-unusable,
  0 success only. A caller distinguishes refusal classes without parsing prose.
  A refusal writes no artefact.
- **Pins recomputed, never trusted.** The spec's pin values are copies; every
  run recomputes from the manifest. A stale-pinned spec is refused rather than
  run, because a result recording the spec's own claim about the corpus would
  be reproducible only in the sense that it repeats the same wrong claim.
- **Shared validation path.** Draft202012Validator, the same path
  `tests/harness/test_scenario_spec_schema.py` exercises, so the runner and the
  suite cannot disagree about what a valid spec is.
- **Acceptance deliberately not evaluated.** The threshold is carried into the
  result with an explicit not-evaluated marker and a stated reason. Emitting a
  pass/fail verdict under commissioning is how commissioning output gets
  promoted by osmosis.

Repo hygiene at the runner commit: ruff clean across the whole repo; the harness
suite 11 passed. Attribution asserted against the full printed commit bodies of
both the last commit and the branch range, 59 lines each, git exit 0 both:
0 lines asserting co-authorship.

## 5. Runs and reproducibility

Both runs: same spec, same manifest, same index, no changes between them.

| Run | Result artefact | Raw file sha256 | Comparable-content sha256 | Exit |
|---|---|---|---|---|
| 1 | result_RQA-001_20260813T121920997844+0000.json | `693e1c45f6997dcd321a8e58cdb70990e8d1b9abb0fa74291f25fbf0e24a97ae` | `4124f3359b584be1ba92397526e74828af79becd64302f0b437bdd3cc881b1a3` | 0 |
| 2 | result_RQA-001_20260813T121936933451+0000.json | `67408b0a791c687c968a410bbc737b793ee48e21d46dec2b2f0adcd3d8936b5c` | `4124f3359b584be1ba92397526e74828af79becd64302f0b437bdd3cc881b1a3` | 0 |

**Normalisation method.** The comparable-content hash is SHA256 over the result
object with exactly two keys removed — the generated timestamp, which varies by
construction, and the embedded comparable-content hash, which cannot cover
itself — canonicalised as sorted-key, fixed-separator UTF-8 JSON, the same
discipline the corpus manifest uses. **Scores are not normalised.** Rounding
floats to make runs agree would manufacture the reproducibility the hash exists
to test.

**REPRODUCIBLE: YES.**

Verified by a recompute external to the runner, because a component checking its
own printed self-report proves little: bodies compared by dict equality, true;
independently recomputed hashes equal, true; each matching its embedded
self-report, true; and the generated timestamp the only differing key across the
two complete artefacts. Raw float scores were therefore bit-identical, which is
affirmative evidence for the ruled bit_identical comparison rather than merely
consistent with it (F5).

Run 1 observations of record: index held 71 chunks; retrieved 5 chunks over 3
documents SYN-TY-02, SYN-DP-01 and SYN-DP-02; expected OGL-0001; matched empty;
recall_at_k 0.0; acceptance NOT EVALUATED.

## 6. Deny-shaped probe table

Every probe varied the spec only; manifest, index and output directory were held
constant. Paired with the allow-shaped runs in section 5, which succeeded — a
refusal-only result cannot distinguish a discriminating guard from one that
blocks everything.

| Probe | Fault injected | Output | Exit | Expected |
|---|---|---|---|---|
| P1 | top_k set to the string "five" | REFUSED: spec failed schema v0.1 validation with 1 error(s); `$.retrieval.top_k :: type :: 'five' is not of type 'integer'` | 2 | 2 PASS |
| P2 | manifest_sha256 replaced with 64 zeroes | REFUSED: 1 corpus pin(s) diverged from the live manifest; names manifest_sha256, printing pinned and live values | 3 | 3 PASS |
| P3 | manifest_version set to 1999-01-01.0 | REFUSED: 1 corpus pin(s) diverged from the live manifest; names manifest_version, pinned 1999-01-01.0 against live 2026-08-06.7 | 3 | 3 PASS |
| P4 | index path pointed at a nonexistent directory | REFUSED: index path does not exist | 4 | 4 PASS |

P4 was additional, beyond the three required. No probe ran where it must refuse.
**No RED findings.**

P2 and P3 were each isolated to a single wrong pin, so they demonstrate the
runner names the correct pin, not merely that it refuses. Refusals write
nothing, asserted by count rather than by inspection: result-artefact count 2
before the probes and 2 after.

## 7. Findings

**F1 — recall_at_k 0.0 on RQA-001. Recorded, explicitly NOT chased.**
The statute-grounding query, asking which statutory provision creates the
offence of fraud by false representation and what must be proved, returned
synthetic typology and data-protection chunks — SYN-TY-02, SYN-DP-01, SYN-DP-02
— while the expected grounding document OGL-0001, the Fraud Act 2006 s.2
extract, did not appear in the top 5. This is a retrieval-quality question
**routed to the Test Plan (D1.1)** by the close ruling, not a spike defect.
Under the D2.0 frame a scenario's own pass/fail is not an exit criterion, and
per operator standing note the query, spec, chunking and index were **not**
tuned to produce a match. It is nonetheless the most substantive thing the spike
surfaced: the corpus holds the statute, and a plainly-worded question about it
did not retrieve it.

**F2 — retrieval_snapshot_sha256 as a v0.2 mandatory field: recorded, OPEN.**
The v0.1 schema makes the field optional and its own comment defers the question
to this spike, asking whether retrieval-class scenarios should require it since
the spike is the first thing to run against a real index. RQA-001 pins it, ruled
in as spike-scoped only. The substantive argument for requiring it at v0.2: the
manifest hash excludes the processing facts — chunker version, embedding model,
chunk counts — that determine what the retriever actually sees, so a retrieval
scenario pinning only the manifest pair records a reproducibility claim narrower
than it appears. Not settled here; v0.1 is immutable once merged and a change is
a new versioned file. Opened as a queue item by the close ruling.

**F3 — No runner existed; scope restated to runner construction, ruled.**
The harness package contained only its `arcaai/harness/__init__.py` and the
schema. No D2.2a scenario spec existed on main either: searched by filename
across the tree, by content across every YAML and JSON file for the spec's
identifying keys, and by directory listing of the harness package and its test
tree. The only hits were the schema, five test fixtures whose own test file
states they carry no normative weight whatever, and an unrelated
`provenance_manifest.json`. Scope was restated at the gate ruling accordingly.

**F4 — DSN credential error, harness-side.** The first governed-store probe
invented a password for the runtime application role rather than reading one. It
failed authentication. No writes occurred and no state changed; the harness
never assumed the owner role and never elevated. Corrected by reading the real
default from `scripts/rehash_sweep.py`, lines 69 to 72, after which the store
returned a corpus_version row count of 0. Recorded rather than omitted because a
guessed credential in a governance repository is worth seeing, and because
guessing before reading the source inverts the correct order.

**F5 — Bit-identical retrieval observed across two runs.** The generated
timestamp was the only differing key across the two complete result artefacts,
so the raw float distance scores were identical. This is affirmative evidence
for the ruled bit_identical migration-diff comparison. Recorded with its limit
stated: two runs, one scenario, one machine, one session, index unchanged
between them. It is not a determinism guarantee for the vector store and should
not be cited as one.

**F6 — Ceremony writes the repo manifest inside the tree.**
`.claude/skills/session-open/SKILL.md` invokes the manifest generator with no
output argument, while the commands section of `CLAUDE.md` documents an explicit
output path outside the tree. Harmless in fact — the file is ignored by
`.gitignore` at line 33 and untracked, so the tree stayed clean — but the
ceremony and the documented invocation disagree, and only the ignore entry is
keeping that safe. Check-method family: a stated convention the mechanism does
not enforce. Routed by the close ruling as a rider on the Arc 2 combined pull
request, not as a separate queue item.

**F7 — Console encoding defeats artefact reads through the harness shell.**
The shell resolves to the Windows ANSI code page, so printing any repository
artefact containing an em-dash or arrow raises a Unicode encode error until
UTF-8 is forced. Cosmetic for reading, but it corrupts the rendering of the
runner's own stdout: the regime banner's em-dash appeared as a replacement
character in every captured run. Affects transcript fidelity, not artefact
content. Queued by the close ruling.

**F8 — Where a Commissioning Session Record lives is ruled only in part. NEW,
raised at close.** The 2026-08-11 reporting ruling commits the Regime 2 TEST
REPORT under `docs/governance/` and specifies the Regime 1 record's content by
reference to it, but states no location clause of its own for Regime 1 and no
filename convention for either. Separately, `CLAUDE.md` states that the governed
audit database holds the Commissioning Session Records from D2.2a onward. D2.5,
the results ledger that would reconcile a database ledger entry with a committed
document, is not yet built, and this runner writes no database rows. This record
is therefore filed under `docs/governance/` on the ruled directory for the
reporting-artefact family, with a filename following the house shape; both the
filename and the document-versus-database question are unruled and are raised
here rather than settled.

## 8. Artefact custody

In-tree:

- `arcaai/harness/runner.py` — committed at `7bad3b7`
- this record — committed by the act this section describes

Held outside the repository, **not committed**, custody by hash:

```
9cad22fc9cf3624c228907fb493bdfd6d08668ffe4dc2032910318b308daa1e8  d22a_scenario_RQA-001_COMMISSIONING-DRAFT.yaml
58de1b9daa9c9fa9f8eb21ef2e287037200ed011858cbe5176a02145a49ad739  probe_P1_schema_invalid.yaml
53f1f3154b7f1f2894c62c90d46eead6821e5797c23fe16430e087576d6a31e4  probe_P2_stale_manifest_sha.yaml
bc25409cb5e5418ca74ee16e33e711f5512e7b37f270746d6d226cae08bcde75  probe_P3_nonexistent_snapshot.yaml
693e1c45f6997dcd321a8e58cdb70990e8d1b9abb0fa74291f25fbf0e24a97ae  results/result_RQA-001_20260813T121920997844+0000.json
67408b0a791c687c968a410bbc737b793ee48e21d46dec2b2f0adcd3d8936b5c  results/result_RQA-001_20260813T121936933451+0000.json
```

The RQA-001 spec remains Claude Code authorship and admissible for this spike
only. Its promotion to a committed scenario, if wanted, is a separate governed
act.

## 9. Close ruling — operator, verbatim

> "RULED: record committed; PR opened for review, merge on my approval; CL-27
> closed; F1 to Test Plan; F2 opens as queue item; F6 rides Arc 2, F7 queued."

Discharged in this arc under that ruling: the record is committed by the act
this document describes; CL-27 is closed against it in the governance review
changelog; F1 is seeded to the Test Plan material; F2 and F7 are appended to the
queue; F6 is attached to the Arc 2 combined pull-request plan rather than
queued separately. The pull request is opened for review and **is not merged** —
the merge word is the operator's, following the operator's own GitHub review
approval.

F8 arose during the execution of this ruling and is therefore not covered by
it. It is raised for a future ruling and blocks nothing.
