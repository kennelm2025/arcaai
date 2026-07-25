# B7 GATE — Fraud RAG (ChromaDB, 50+ seed docs, RAGAS)

**Status: NOT STARTED — entry criteria open.**
Created at stage entry 25 Jul 2026 per DEC-0010 / RAT-01. Exit evidence
is blank by design and is filled as it lands. Entry criteria are signed
before the first commit of the stage.

*Entry sign-off: [unsigned]*
*Source of criteria: `docs/governance/WS-D_RAT-01_GATE_PLAN.md` §5, B7.
Where this document and the plan diverge, the plan is corrected — the
criteria are not restated from memory.*

---

## 1. Entry criteria

Each carries a dependency flag: *self* = clearable by working on it;
*external* = dependent on a third party, licence, regulator or another
person's availability, and therefore needing lead time.

- [x] **B6 gate passed.** *(self)* — GATE PASSED Jul 2026,
      `docs/build/B6_GATE.md`. Agent graph exposes the retrieval slot;
      R7 retrieval rung explicitly carried forward to this gate.
- [ ] **RAT-02 governance trio landed as pre-B7 work** *(self)* — audit
      logging, execution metadata, request wrapper. All three, not two.
      Specification not yet written; this is the largest open entry
      item.
- [ ] **ChromaDB in the `arcaai` env, version pinned** *(self)* — added
      to `pyproject.toml`, pinned, installed, import verified from
      outside the repo root per the B5 packaging precedent.
- [ ] **Corpus sourcing decision recorded as a DEC. No ingest before it
      exists.** *(external — licence terms are not ours)* Drafted as
      DEC-0011 (synthetic corpus plus a named OGL subset; local-only
      ingest considered and rejected because a private vector index is
      itself the restricted artefact under the FCA Handbook terms).
      **Drafted, not yet committed** — this criterion is not met until
      the DEC is in `DECISIONS.md` on main.
- [ ] **CF-1 conformance spot-check design agreed** *(self)* — WS-D
      item 2. Standing gate question already established; retrospective
      audit rejected. The design is what remains.

## 2. Scope

From Build & Quality Plan v1.0, verbatim:

> Fraud RAG (ChromaDB, 50+ seed docs, RAGAS)

Scope changes require a DEC, referenced here. None at entry.

## 3. Exit evidence

*Blank at entry. Each item is filled with a **path @ commit SHA**, or a
CI result transcribed as text — workflow name, run number, conclusion,
date, and the commit SHA it ran against. Never a bare path, never
`main`, never a link alone (RAT-01 §3.1).*

**Required** — these are the not-allowed deferrals at §5; absence
blocks the gate.

- [ ] Corpus manifest, per document: id, source, licence status,
      sha256, ingest date, chunk count, and **retrieval eligibility
      state** (included / pending review / withdrawn / deprecated),
      recorded as **dated transitions rather than a mutable flag** —
      B9 replay needs eligibility as at the decision, and a boolean
      that flips in place destroys that fact.
      → *evidence:*
- [ ] Grounding test: every generated claim carries a chunk id; a
      response containing an uncited assertion fails.
      → *evidence:*
- [ ] Negative test: a query with no supporting document returns the
      fallback, not a fluent answer.
      → *evidence:*
- [ ] Confidence threshold + "insufficient evidence" fallback
      implemented; threshold value recorded with its reasoning.
      → *evidence:*
- [ ] CF-1 conformance spot-check result.
      → *evidence:*

**Supporting** — recorded, not gate-blocking.

- [ ] RAGAS baseline: scores as committed JSON alongside the run config
      and eval set. Offline. Recording the baseline is required;
      passing a threshold is not — B7 establishes the number later
      stages are measured against.
      → *evidence:*
- [ ] Retrieval latency measured against the R7 ladder (< 100 ms rung,
      carried forward from B6). Recorded, not gated — G9 was the
      latency gate and closed at B5.
      → *evidence:*

## 4. Gate questions

**Standing checklist:** `docs/governance/WS-D_RAT-01_GATE_PLAN.md` §4.
Not restated here. Answered in prose in the Gate Acceptance Record.

**Stage-specific:**

1. Can every claim in a generated narrative be traced to a retrieved
   chunk, and thence to a manifest entry, by a reviewer with repo
   access and no help from the author?
2. Does the manifest carry licence status per document, and would that
   status survive a client's procurement review?

## 5. Deferrals

**Allowed** — may be pushed to a later stage without reopening this
gate:

- reranker
- hybrid / BM25 search
- corpus beyond 50 documents
- any RAGAS pass threshold
- retrieval latency optimisation
- per-query RAGAS in the request path — rejected outright, not merely
  deferred (step-change candidate 4)

**Not allowed** — absence blocks the gate regardless of what else
landed. This list is exhaustive as written and is the required-evidence
list at §3:

- corpus manifest with provenance, licence status and time-versioned
  eligibility
- grounding test
- negative test
- insufficient-evidence fallback
- CF-1 spot-check result

## 6. Gate Acceptance Record

*Per BUILD_TRACKER.md, binding from B7. Blank until gate close.*

- **Evidence list** (path @ SHA):
- **CI results** (workflow · run number · conclusion · date · SHA,
  transcribed as text):
- **Standing checklist answers** (RAT-01 §4, in prose):
- **Stage-specific answers** (§4 above, in prose):
- **Producer statement:**
- **Approver statement:** *(same person permitted; both statements
  mandatory)*
- **Residual risks accepted into B8:**
- **Decision:** Pass / Conditional Pass / Fail
- **Approval date:**
