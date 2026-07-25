# B7 GATE — Fraud RAG (ChromaDB, 50+ seed docs, RAGAS)

**Status: NOT STARTED — entry criteria open (2 of 5 outstanding).**
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
      **Specified and ratified**:
      `docs/governance/RAT-02_GOVERNANCE_TRIO_SPEC.md` and ADR-0010
      (`decisions/0010-governance-instrumentation.md`). **Not yet
      built** — the criterion requires the trio landed, not designed.
      Largest open entry item.
- [ ] **ChromaDB in the `arcaai` env, version pinned** *(self)* — added
      to `pyproject.toml`, pinned, installed, import verified from
      outside the repo root per the B5 packaging precedent. Local
      install; no cloud provisioning — see CF-1/B7-a at §1.1.
- [x] **Corpus sourcing decision recorded as a DEC. No ingest before it
      exists.** *(was external — licence terms are not ours)* **Met.**
      DEC-0011 on main, merged in PR #28. Synthetic corpus plus a named
      OGL subset; local-only ingest outside the repo considered and
      rejected, because a private vector index is itself the restricted
      artefact under the FCA Handbook terms. The criterion moved from
      externally dependent to self-resolvable on adoption, which was
      the point of adopting it.
- [x] **CF-1 conformance spot-check design agreed** *(self)* — **Met.**
      `docs/governance/CF-1_SPOT_CHECK_METHOD.md`, ratified 25 Jul
      2026. Nominations for this stage at §1.1.

### 1.1 CF-1 conformance nominations

Nominated 25 Jul 2026, **before B7 code exists**, per CF-1 method §3.
Evidenced at exit in the Gate Acceptance Record (§6). Four nominations,
one expected to be awkward.

**CF-1/B7-a — R5 vector store *(the awkward one)*.**
R5 fixes the Phase 2 vector store as self-managed on-premises
OpenSearch, explicitly excluding managed-cloud stores because
`rm_knowledge` holds customer data. The Build & Quality Plan specifies
ChromaDB for B7. Both can hold — ChromaDB for the reference build,
OpenSearch for deployment — but the relationship is recorded nowhere.
The substantive risk is not the naming: it is whether B7 scatters
ChromaDB-specific calls through the retrieval path, making the Phase 2
move a rewrite rather than a swap. Under ADR-0009 the retrieval
framework is platform machinery; the store is an implementation of it.

- *Conforms if:* a retrieval interface with the store behind it;
  `chromadb` imported in one adapter module and nowhere else; a written
  statement of the ChromaDB-now / OpenSearch-later relationship.
- *Deviation looks like:* `chromadb` imported across retrieval,
  ingestion and agent code.

**CF-1/B7-b — SA5 RAG data classification.**
SA5 classifies `fraud_knowledge` as internal-sensitive. DEC-0011 makes
the corpus synthetic plus an OGL subset, so classification is trivially
satisfied — but it must appear in the manifest, not merely be true in
fact.

- *Conforms if:* a classification field per manifest entry.
- *Deviation looks like:* manifest carries licence but not
  classification.

**CF-1/B7-c — ADR-0010 emit coverage.**
Retrieval is the first new decision point since the governance trio was
built, and therefore the first real test of whether the emit interface
is used rather than bypassed under time pressure.

- *Conforms if:* `retrieval_performed` events present in the audit
  trail for a live end-to-end run; no direct writes to audit tables
  from vertical code.
- *Deviation looks like:* retrieval happening outside a wrapper
  context.

**CF-1/B7-d — R7 retrieval latency rung.**
R7 sets retrieval below 100 ms; B6 deferred this rung to B7.

- *Conforms if:* measurement recorded in this document.
- *Deviation:* above 100 ms is **a finding to record, not a gate
  blocker** — latency is deliberately absent from the not-allowed list
  at §5, because a gate blocked on latency invites the number to be
  massaged, whereas a measured slow retrieval is a known quantity.

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
      **SA5 data classification**, sha256, ingest date, chunk count,
      and **retrieval eligibility state** (included / pending review /
      withdrawn / deprecated), recorded as **dated transitions rather
      than a mutable flag** — B9 replay needs eligibility as at the
      decision, and a boolean that flips in place destroys that fact.
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
- [ ] CF-1 spot-check result — all four nominations at §1.1 evidenced.
      → *evidence:*

**Supporting** — recorded, not gate-blocking.

- [ ] RAGAS baseline: scores as committed JSON alongside the run config
      and eval set. Offline. Recording the baseline is required;
      passing a threshold is not — B7 establishes the number later
      stages are measured against.
      → *evidence:*
- [ ] Retrieval latency measured against the R7 ladder (< 100 ms rung,
      carried forward from B6). Recorded, not gated — G9 was the
      latency gate and closed at B5. See CF-1/B7-d.
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

- corpus manifest with provenance, licence status, SA5 classification
  and time-versioned eligibility
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
- **CF-1 nomination outcomes** (§1.1) — one of *Conforms* / *Deviation,
  recorded as DEC-NNNN* / *New ADR required*, per nomination:
  - CF-1/B7-a (R5 vector store):
  - CF-1/B7-b (SA5 classification):
  - CF-1/B7-c (ADR-0010 emit coverage):
  - CF-1/B7-d (R7 retrieval latency):
- **Producer statement:**
- **Approver statement:** *(same person permitted; both statements
  mandatory)*
- **Residual risks accepted into B8:**
- **Decision:** Pass / Conditional Pass / Fail
- **Approval date:**
