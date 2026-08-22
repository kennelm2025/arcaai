# QD-F2 bounded trial — evidence record, 22 August 2026

## Provenance

**Chair authorisation, verbatim as carried in the PROMPT 159 release prompt:**

> Chair-authorised bounded trial: exactly 10 consecutive polls of the live queue
> driver at the 60-second cadence, attended, solely to generate criterion-1
> evidence for the design note's 5.1 acceptance criteria. Withholding remains in
> force for all other purposes. No other scope.

| Field | Value |
| --- | --- |
| Carried by | PROMPT 159, lane T2 |
| Executed | 22 August 2026, 12:24:29Z – 12:34:19Z |
| Subject | First live exercise of both QD-F2 mechanisms, against the design note's §5.1 criteria |
| Precedent | The 21 August commissioning trial — temporary, purpose-limited, Chair-supervised, then closed |
| Register numbers consumed | None |

**Footnote — PR series is not the PROMPT series.** PR numbers are GitHub pull
requests; PROMPT numbers are queue envelopes. The two are independent.

**No recommendation on the lift is made here.** This record states what was
observed. The DEC-0020 ruling is the Chair's.

---

## 1. Pre-state

| Location | Count |
| --- | --- |
| T1 inbox / outbox / dead / done | 9 / 8 / 1 / 2 |
| T2 inbox / outbox / dead / done | 14 / 14 / absent / absent |
| queue-root dead | absent |

`driver.log`: 53 rows, SHA256 `5cf58472fd515aec615fe3b2c28159cf8bc8414fcabcc0c255871eab04602c82`.
HEAD `7546bb65f63b9431406333ca64df23750418986c`. Anchors DEC-0019 / ADR-0010 /
CL-31 / WS-E 77.

### 1.1 Two blockers found at pre-flight and cleared before the run

Both were found by pre-flight rather than by consuming the single authorised
run, which is the reason they are recorded as pre-state rather than as trial
failures.

**(a) Four outcome files were malformed and would have aborted the trial.**
`parse_outcome_status` requires `STATUS:` on line 1. The four F-out files for
PROMPTs 155–158 began with a markdown heading, so all four parsed as `ERROR` —
a paging status. Poll 1 would therefore have emitted 4 sweep pages plus the
intentional trial page, **5 in one poll**, exceeding the envelope's abort
threshold of more than 3. Repaired under Chair ruling by prepending
`STATUS: COMPLETE` as line 1, every subsequent byte unaltered and verified
byte-identical. Predicted poll-1 pages fell to 0 from sweeps.

**(b) The `ARCAAI/REFUSED` label did not exist.** Mechanism (a) relabels a
refused draft to that label; `_label_id` raises when a label is absent, so the
relabel would have failed, the draft would have stayed RELEASED, and it would
have re-paged on every poll — producing a **failing criterion (a) for an
environmental reason rather than a mechanism reason**. Created by the Chair
before the run, together with removal of a stale RELEASED label from
`ARCAAI-PROMPT-9003`.

**Finding carried at Chair direction.** Mechanism (a) landed with an unmet live
prerequisite. The green test suite could not see it because `FakeTransport`
models labels as plain lists and never resolves a label id, so 126 passing tests
said nothing about whether the label existed in the mailbox. **A WS-E item
follows at the next sitting.** Recorded here because the trial is where it
surfaced.

---

## 2. The run

**Fixture.** One deliberately refusable draft, subject `ARCAAI-PROMPT-9099`,
body carrying no `TARGET` header, clearly marked TRIAL in its text, labelled
`ARCAAI/RELEASED`.

**Method and its bound.** The driver has no poll-count flag — `--once` runs a
single cycle and the bare form loops. `--once` ten times was **rejected as
non-equivalent**: each invocation is a fresh process, so authorisation would be
acquired ten times and criterion (c) would be answered wrongly. The run was
therefore loop mode with attended termination, bounded by a 590-second wall
clock against a 60-second cadence.

**Observed:** start 12:24:29Z, terminated 12:34:19Z, elapsed 590s, exit 124
(timeout-bounded, as intended). All queue activity is stamped 12:24:29Z–12:24:32Z,
i.e. within poll 1; no further rows were written for the remaining ~9.6 minutes.

### 2.1 Per-poll table, and an honest limit on it

| Poll | Time | Actions | Pages |
| --- | --- | --- | --- |
| 1 | 12:24:29–12:24:32Z | lane assert ×2; refuse + dead-letter `9099`; 10 × (sweep + archive); outcomes draft | **1** |
| 2–10 | 12:25:29Z onward, at 60s cadence | none logged | **0** |

**The limit, stated plainly rather than rounded up.** Polls 2 onward wrote **no
log rows**, because the driver logs only actions and those polls had none to
take. The absence of rows is therefore consistent with "nine quiet polls" and
also with "the process died after poll 1". The poll count is **inferred from a
590-second runtime at a 60-second cadence**, not proven per poll.

Stdout would have carried a rendered report per poll, but the process was
terminated by signal and Python's block buffering discarded the unflushed
buffer, so no stdout survived. **Recorded as a method defect of this trial**, and
the corrective for any future run is to capture flushed output rather than rely
on the log for liveness.

**This is itself a finding for the unattended model: a healthy loop is
indistinguishable from a dead one in the log.** Nothing positively evidences
liveness while nothing is happening, which is precisely the condition an
unattended run spends most of its time in.

---

## 3. Findings against the §5.1 criteria as drafted

### (a) A refused item pages exactly once — **SATISFIED, with the count caveat above**

Raw log excerpt, rows 57–59:

```
DEAD-LETTERED  9099                 D:\arcaai-repo\_queue\dead\PROMPT-9099.REFUSED-20260822T122431Z.md
REFUSED        ARCAAI-PROMPT-9099   malformed envelope: no TARGET in the first 10 lines of the body
PAGED                               ARCAAI queue driver: REFUSED
```

Exactly **one** `PAGED` row for the trial item across the whole run, and no
second `REFUSED` row. Corroborated in the mailbox: `ARCAAI/REFUSED` moved from
0 to 1 message and `ARCAAI/RELEASED` from 1 to 0, so the terminal relabel
executed against live Gmail — the act that stops the next poll selecting the
item, and therefore the act that closes the defect.

The dead-letter landed at the **queue-root** `_queue\dead\`, not under a lane,
because a body with no `TARGET` has no determinable lane. That is the disposition
disclosed at the PROMPT 157 report §5(c) and affirmed as ruled by the Chair, now
exercised live.

**Ruling 2 verified against the artefact, not the intention:** the envelope file
is 643 bytes hashing to `600a41f636d01d596c34b9b334268a85d7adf3d510c2a1fe2ae9e15e0291534d`,
and the sidecar's own `content_sha256` records that same value — so the preserved
bytes are independently hashable without parsing the sidecar.

### (b) A swept outcome alerts exactly once, and archives — **SATISFIED**

Ten fresh outcome files swept and archived, each as a `SWEPT` + `ARCHIVED` pair
(rows 60–79): T1 `PROMPT-132`, `132R`, `154`; T2 `PROMPT-130`, `131`, `139`,
`155`, `156`, `157`, `158`. Twelve previously-swept files were correctly skipped.
**Zero alerts**, all ten parsing `COMPLETE` after the pre-flight repair.

**Ruling 6's two conditions verified per file, by re-hashing after the move:**
all ten archived files hash-match their sidecar `content_sha256`, and all ten
record an `origin_path`. **10 match, 0 mismatch.**

This is the **first live exercise of the archive**. T2 `done` went from absent to
14 files (10 archived items plus their sidecars, less T1's share) and T1 `done`
from 2 to 8; the two outboxes fell from 14 and 8 to 7 and 5.

### (c) Authorisation acquired exactly once across the run — **NOT DIRECTLY EVIDENCED**

**Stated as a shortfall rather than claimed.** The driver logs no row for
authorisation, so the log cannot count acquisitions. What the run does establish
is weaker and worth having: a single process ran for 590 seconds across roughly
ten polls and completed its Gmail work, and no interactive consent prompt
appeared at any point — which it would have, visibly, had the boundary been
crossed, since the OAuth token had **expired on 2026-08-21T13:26:03Z** and only a
successful non-interactive refresh could have kept the run alive.

So the 158 boundary's refresh-side behaviour is **corroborated** by the run
completing at all, and the acquisition count is **not measured**. The
invocation-count evidence for that criterion remains the test-level count from
PROMPT 158, not this trial.

### (d) Nothing outside `_queue` touched — **SATISFIED**

Every path in the 27 new log rows resolves under the queue root. This is
structural rather than incidental: the driver never imports `subprocess` and
never runs git, asserted by `tests/harness/test_queue_driver.py`, and every write
passes `_assert_within_queue` immediately before the write.

---

## 4. Post-state

| Location | Before | After |
| --- | --- | --- |
| T1 outbox / done | 8 / 2 | 5 / 8 |
| T2 outbox / done | 14 / absent | 7 / 14 |
| queue-root dead | absent | 2 |
| `driver.log` rows | 53 | 80 |

`ARCAAI/RELEASED` 0 messages; `ARCAAI/REFUSED` 1; `ARCAAI/CONSUMED` unchanged at 2.

---

## 5. What this evidence does and does not establish

The trial establishes, against live Gmail and the live queue, that a refused
draft reaches a terminal state and pages once rather than repeatedly; that its
preserved bytes are independently hash-verifiable beside a parseable sidecar;
that swept outcomes archive with hash preserved and origin recorded on every one
of ten files; and that no byte left the queue root — the first live exercise of
both mechanisms, and the behaviours §5.1 criterion 1 was written to require. It
does **not** establish the poll count by direct observation, since quiet polls
write no rows and the terminating signal discarded the buffered stdout that would
have shown them, so ten polls is inferred from a 590-second runtime at a
60-second cadence; it does **not** measure authorisation acquisitions, which
remain evidenced only at test level from PROMPT 158; and it establishes nothing
about behaviour beyond ten polls or unattended, the run having been attended
throughout under a bounded authorisation that expired with it.
