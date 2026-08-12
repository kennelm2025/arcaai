# PILOT RECORD — corpus-lister fan-out, 2026-08-12

**Status: pilot record, not a report.** A bounded first exercise of the
`corpus-lister` subagent installed at PR #98. It produced no listing and consumed
no register number. Its purpose was to test the mechanism, and the mechanism is
what it found defects in. Recorded here so that the corrections made in the same
PR cite evidence on the record rather than session memory.

Nothing in this document lists anything. Listing into `MANIFEST.yaml` remains a
separate governed act on operator command (CLAUDE.md working protocol item 3).

## Scope, as ruled

Three documents, three concurrent agents, one document each. Drafts only,
written to a scratchpad path outside the repository tree. Nothing committed from
the pilot itself; the three drafts remain in the operator's scratchpad for
spot-check.

**Selection basis.** SYN-SG-07, SYN-SG-08 and SYN-SG-09 — the three where
listing debt is already ruled at queue item 5, and the three largest documents in
the corpus (10.7 KB, 9.7 KB, 12.7 KB), giving variety in size and structure.

**Variety was not available across document families.** Every unlisted document
is SG-series. The listed set already covers CV, DL, DP, TR, TY and the four OGL
documents, so variety could only be sought within SG.

**SYN-SG-03..06 were deliberately excluded**, though also unlisted, because
queue item 9 carries an open scope decision on whether they sit inside the
batch-2 panel circulation. Drafting listings for them would have pre-empted an
operator decision.

## The three proposed entries, verbatim

### SYN-SG-07

```yaml
  - id: SYN-SG-07
    source: "SYNTHETIC — arcaai test corpus. Not issued by any real authority. Licence: synthetic-arcaai. The Authority · Sector Guidance series · SG-07"
    licence: synthetic-arcaai
    sa5_classification: internal-sensitive
    content_sha256: "FM2-UNEVALUATED-see-listing-draft-section-3"
    eligibility:
      - state: pending_review
        date: FM2-UNEVALUATED
        reason: "FM2-UNEVALUATED — see listing draft section 4"
    processing:
      chunker_version: FM2-UNEVALUATED
      embedding_model: FM2-UNEVALUATED
      chunk_count: FM2-UNEVALUATED
      ingest_timestamp: FM2-UNEVALUATED
```

### SYN-SG-08

```yaml
  - id: SYN-SG-08
    source: "SYNTHETIC — arcaai test corpus. Not issued by any real authority. Licence: synthetic-arcaai. The Authority · Sector Guidance series · SG-08"
    licence: synthetic-arcaai
    sa5_classification: internal-sensitive
    content_sha256: "<<UNCOMPUTED — failure mode 2; see §3.1>>"
    eligibility:
      - state: pending_review
        date: <<UNDERIVABLE — failure mode 2; see §3.2>>
        reason: "<<UNDERIVABLE — failure mode 2; see §3.2>>"
    processing:
      chunker_version: null
      embedding_model: null
      chunk_count: null
      ingest_timestamp: null
```

### SYN-SG-09

```yaml
  - id: SYN-SG-09
    source: "SYNTHETIC — arcaai test corpus. Not issued by any real authority. Licence: synthetic-arcaai. The Authority · Sector Guidance series · SG-09"
    licence: synthetic-arcaai
    sa5_classification: internal-sensitive
    content_sha256: "<UNCOMPUTED — failure mode 2, see note 1; DO NOT PASTE>"
    eligibility:
      - state: pending_review
        date: 2026-08-10
        reason: "authored (PR #81, 2026-08-10; batch-2 authoring complete at 7/7); batch-2 panel circulation not yet run; awaiting review and operator inclusion decision"
    processing:
      chunker_version: null
      embedding_model: null
      chunk_count: null
      ingest_timestamp: null
```

All three placeholders are deliberately malformed so that a paste-through
hard-fails `parse_manifest()` at its `content_sha256: 64 lowercase hex chars
required` check, rather than loading a plausible but fabricated identity.

## Success lines, verbatim

**SYN-SG-07:** "FAIL (failure mode 2 — check could not evaluate): drafted
listing for SYN-SG-07 is INCOMPLETE; content hash NOT computed and no value
offered; 4 of 7 schema fields populated, 3 of 7 reported FM2."

**SYN-SG-08:** "PARTIAL — failure mode 2 (check could not evaluate) on the hash.
Draft written; not paste-ready." … "Field count: 7 required; 5 populated, 1
partial, 1 blocked."

**SYN-SG-09:** "FAILURE MODE 2 (check could not evaluate) — drafted listing for
SYN-SG-09 …; content hash NOT computed — no first-8 characters to quote …; 6 of
7 top-level schema fields populated …; 0 of 4 `processing` sub-values derivable."

## Collation verdict

The lead recomputed every hash independently from file bytes rather than
accepting any reported figure. **Method validated by positive control before
use:** SYN-SG-01, already listed, hashed to `b724eae328f8…`, matching its
committed manifest value exactly — which establishes that `content_sha256` is
taken over raw file bytes with no normalisation.

| Document | Lead's recomputed hash (first 8) | Agent's claimed hash | Verdict |
| --- | --- | --- | --- |
| SYN-SG-07 | `05381505` | none offered (FM2) | no mismatch possible |
| SYN-SG-08 | `3ade667f` | none offered (FM2) | no mismatch possible |
| SYN-SG-09 | `56adb90e` | none offered (FM2) | no mismatch possible |

No STOP was triggered. There was nothing to disagree with: the correct behaviour
was an honest absence, and all three delivered it.

**Field-by-field against the exemplar:** all three drafts carry exactly the seven
fields in exemplar order — `id`, `source`, `licence`, `sa5_classification`,
`content_sha256`, `eligibility`, `processing` — with the four `processing`
subkeys in the exemplar's order. Nothing invented, nothing omitted, in any of the
three. All three flagged `sa5_classification` as convention-inherited rather than
a document fact, the documents carrying no classification marking.

**One collation defect, visible only because the batch ran three-wide.** The
three agents treated identical blocked fields three different ways: SG-08 and
SG-09 wrote `processing: null` citing the SYN-TY-03..09 precedent, while SG-07
wrote `FM2-UNEVALUATED` strings; on eligibility, SG-07 blocked date and reason,
SG-08 blocked both, SG-09 supplied both with PR #81 provenance. Same
specification, three shapes. A single agent could not have revealed this.

## Mechanism assessment

**Success lines stated what was checked.** Each named the blocked field, why the
check could not run, what it did *not* do — no guess, no copy from a neighbouring
entry — and a field count. This is check-method Rule 2 applied without being
prompted, and it is the strongest artefact the pilot produced.

**No agent exceeded its limits.** The repository tree stayed clean; the newest
write anywhere under `verticals/fraud/corpus/` remained 10 Aug, so nothing in the
corpus was touched; exactly three files appeared in the override path, one per
agent, correctly named. No manifest write, no register touch, no git, no
elevation.

**The blocking finding: the agent cannot perform its own core function.** The
definition orders hashes "computed — not guessed" while granting `Read, Grep,
Glob, Write` — no execution tool. `Get-FileHash`, `hashlib` and `sha256sum` are
all unreachable, and the Read tool returns decoded line-numbered text rather than
bytes. Every invocation will report failure mode 2 on the identity field. Three
of three did.

### Findings corroborated independently by the lead

The missing cross-referenced documents are genuinely absent: SG-07 cites TR-05
(§2.2) and DL-06 (§5.2); SG-08 cites TR-03 (§2.3) and CV-05 (§5.2). The corpus
holds only TR-01/02, DL-01/02 and CV-01/02. **These are precisely the sections
already named in queue item 15**, so the agents rediscovered a tracked item
rather than finding a new defect — a useful confirmation that item 15 is
accurately scoped.

The listing debt is **seven documents wide, not three**: SYN-SG-03 through
SYN-SG-09 are all unlisted. Two agents flagged this independently and the lead's
own manifest read confirms it.

### Held for operator ruling — design questions, deliberately not fixed

These are improvements rather than transcription repairs, and are therefore
excluded from the corrective PR:

1. **Whether `corpus-lister` should hold an execution tool at all.** Granting one
   would widen a subagent's permissions, which is a design and permission
   decision, not a defect repair. The alternative taken in the PR is to correct
   the instruction to match the observed capability and point at the repository's
   existing governed producer.
2. **Whether fan-out is the right instrument for this work.**
   `scripts/corpus_manifest_entries.py` already emits a complete entry, hash
   included, for every unlisted document in one pass, drift-checks the listed set
   in the same run, and writes nothing. The mechanical fields want a script. What
   the agents added was governance judgment — precedent selection, eligibility
   reasoning, and refusal to fabricate — and that is what a fan-out should be
   scaled for.
3. **The divergent shapes must be pre-ruled before scaling:** `processing` as
   `null` versus placeholder, and whether the eligibility date is the authoring
   act or the listing act. Both validate against the parser, so the choice is a
   governance one rather than a mechanical one.
4. **SYN-SG-03..06 remain excluded** pending the queue item 9 scope decision.

Scaling to five or eight concurrent before items 1 to 3 are ruled would multiply
failure-mode-2 reports rather than throughput.
