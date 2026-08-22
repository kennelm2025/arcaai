# F1 transport instances and mitigating conventions — 22 August 2026

## Provenance

| Field | Value |
| --- | --- |
| Carried by | PROMPT 158, lane T2 |
| Date | 22 August 2026 |
| Subject | Defect F1 — Gmail rewriting paths and URLs in transport — its instances to date, and the conventions adopted in mitigation |
| Register numbers consumed | None |

**Footnote — PR series is not the PROMPT series.** PR numbers are GitHub pull
requests; PROMPT numbers are queue envelopes. The two series are independent and
neither cites the other.

**Why this record exists.** The merged design note at
`docs/governance/QDF2_DESIGN_NOTE_2026-08-22.md` §4.1 names **two** F1 instances,
**both inbound**. A third class was observed after that note merged, on the
**return leg**, and it is not in the tree. F1's blast radius as recorded is
therefore understated by one leg, and this record corrects it.

---

## 1. Instances to date

### (i) 21 August 2026 — INBOUND

**What.** A bare outcome-file path in a staged draft was corrupted into an
invented `http://` redirect URL.

**Disposition.** Recorded in the QD-F2 spec and carried into the design note.
Notable because it occurred on the document that specifies its own register —
the defect reproduces on ordinary governance traffic, not on contrived input.

### (ii) 22 August 2026 — INBOUND, and a guard success

**What.** The PROMPT 156 release prompt's inbox path arrived wrapped in backtick
decoration.

**Disposition.** **Neutralised on arrival.** The release prompt carried an F1
guard instructing the reader to strip the formatting and treat the filename as
authoritative. The guard worked.

This is the first case in the family where the corruption was **anticipated in
the artefact** rather than discovered afterwards, and it is recorded as a success
as much as an instance. It also required a judgement the guard did not spell out:
an envelope's own authored backticks are content, not decoration, and stripping
them would corrupt the envelope. Distinguishing the two is part of applying the
guard.

### (iii) 22 August 2026 — OUTBOUND

**What.** Gmail applied the `google.com/url?q=` redirect wrapper to PR URLs in
lane outcome drafts written back to the Chair.

**Disposition.** Recorded here. **This is the instance absent from the merged
design note**, and the reason this file exists. The note characterises F1 as
corrupting envelopes arriving at the lane; it also corrupts reports leaving it,
and the driver's consolidated reply draft travels the same path.

---

## 2. The outbound instance, characterised further

Three facts observed while recording (iii), each of which widens the defect
beyond "bare paths get schemes invented".

**(a) It fires on PROSE, not only on paths.** A draft written to *describe* the
defect had the literal string naming the redirect wrapper linkified into the
wrapper itself. A document about F1 is a document that provokes F1.

**(b) The two F1 forms COMPOSE.** A bare filename appearing mid-sentence had a
scheme invented *and* was then redirect-wrapped — both forms applied to one
token, producing a doubly-corrupted string inside a filesystem path.

**(c) A proposed mitigation was TESTED AND FAILED, and is recorded as rejected.**
Citing PRs by number instead of by URL was floated as a candidate convention for
outbound reports. In the very draft that proposed it, it made matters worse:
avoiding URLs while naming the wrapper caused two further corruptions. The
lesson is that avoiding URLs is not the operative variable — **breaking the
trigger string so it cannot parse as a host** is, and that remains untested.

**(d) It is not new to 22 August.** The 21 August queue incident notes carry the
same corruption on four outcome filenames. The outbound instance count therefore
substantially exceeds what either the design note or item (iii) alone conveys.

---

## 3. Conventions adopted 22 August in mitigation

Listed with what each actually buys, because a convention whose limits are
unstated will be relied on beyond them.

**PR-by-number in outbound reports.** Reports cite pull requests as `#165`
rather than by URL. **Partial:** it removes the most common trigger and does not
address prose that names a host-like string — see 2(c), where this convention
was first proposed and immediately falsified as a general answer.

**Envelopes body-borne, with paths backticked.** Attachments are avoided because
the MCP Gmail connector is permission-blocked on draft attachments, so an
attachment-borne envelope cannot be self-carried at all. Backticking paths marks
them as content and makes decoration visible when it occurs.

**Extract-body-to-disk-then-hash — the standing self-carriage method.** The body
is written to a file first, then the carried file is compared against it. This
made carriage hash-verifiable where the earlier method could only check
structure. **Limit, now closed by the next convention:** it proved the carried
file matched the body Gmail *returned*, not that Gmail's stored body matched what
was composed.

**Hash-in-draft — the `BODY-SHA256` header line.** The staged draft carries the
SHA256 of its own body, so carriage can verify **composed against stored against
carried** in one comparison. First used by PROMPT 158.

**It earned its place on first use.** The initial transcription of PROMPT 158
hashed differently: 56 lines and 7553 bytes against an expected 57 and 7554 — a
single dropped trailing newline. **Every structural check passed on that
defective file**: CHAIR-FILL, sections present, header identity, tripwire, all
green on a file that was one byte wrong. The hash header was the only check
standing between a corrupt envelope and execution.

The practical conclusion, recorded so it is not re-derived later: **the hash is
the load-bearing check and the structural checks are supporting evidence**, not
the other way round.

---

## 4. What this record does not do

It does not amend the merged design note — that note's §4.1 stands as written,
with this file as the correction of record. It proposes no ruling, closes no
open item, and does not address the untested mitigation named at 2(c).
