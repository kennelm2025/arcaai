# ArcaAI — Mechanical Rulings Record

Date: 2026-08-04 (mobile session, no machine access)
Operator: Mike Kennelly
Coordinator: Claude
Status: RULED — execution deferred to next machine session
Repo state at ruling: nothing landed; HEAD main b611044 (sandbox view); branch handover-2026-07-30 at e47c35a flagged, out of scope here

## Ruling

Operator ruling issued 2026-08-04: all six items approved as recommended, no divergence.

1. ci-mlops trigger gap — Variant A approved: bare scripts/** glob added to pull_request paths. Variant B set aside.

2. DEC-0014 item 7 — both options approved: Option 1 CI history sweep (verify/lift loader's append-only callable first; fetch-depth: 0) + Option 2 operator-machine rehash_sweep with DECISIONS addendum. Approach approved, not the draft script as-is — two marked assumptions (DB accessor helper name; corpus_version column names) verify on-machine before the script enters the repo.

3. dev_up.cmd Docker guard — approved as drafted: docker info fail-loud check at top of script.

4. repo_manifest.py count wording — approved as drafted: tail-construction variant, single rendering path.

5. Three WS-E footnotes — approved as drafted: renumber at paste; ride next ledger touch, no dedicated PR.

6. SESSION_PROTOCOLS — header redirect only approved: one-line currency note under H1 (paste-ready text in coordinator note of 2026-08-03); full rewrite rejected now, held for a WS-C pass.

## Landing plan (ratified with the ruling)

- PR A: items 1 + 3 + 4 + 6. All trigger-path safe; ci-mlops self-exercises on this PR. scripts\lint.cmd before push; Files Changed read before merge; post-merge diffstat eyeballed.
- PR B: item 2, after the two on-machine verifications, with DECISIONS addendum.
- Item 5: rides next ledger touch.

## Advisory trail

- 2026-08-03 (Grok, pass 1): pre-review of coordinator deliverables ZIP. Concurred with all coordinator recommendations, no splits. Recorded advisory.
- 2026-08-04 (Grok, pass 2): re-review via mobile rulings pack v1.0, four questions (Q1 divergence, Q2 PR A interaction risk, Q3 item-7 two-surface argument, Q4 branch-flag blocking). Full concurrence on all four; explicitly stated as concurrence-without-new-reasoning. Logged as advisory re-confirmation by the same reviewer — one reviewer across two passes, not two independent derivations (WS-E 36 class).
- ChatGPT: not consulted on this pack.

Operator ruling is the deciding act; reviewer input advisory throughout.

## Carried caveats

- WS-E 60 (newline divergence): coordinator sandbox hashes advisory in exactly the line-endings failure shape.
- Item 2 script assumptions: pre-landing verification items, named in the return queue.
- Branch handover-2026-07-30 resolution precedes all execution above.

## Corrections at repo paste (2026-08-06)

1. "HEAD main b611044 (sandbox view)" above was wrong: pre-merge main
   was 17ff32f. The branch flag itself dissolved on machine
   verification — PR #59 had been merged in-session on 30 Jul
   (12:57 GMT+1, all CI green); the 04 Aug manifest was generated
   without a prior fetch against a five-day-stale origin/main ref.
   No unrecorded merge; the mobile session's "no repo acts" statement
   was true.
2. "2026-08-03" references to the coordinator handover pack refer to
   the pack delivered as SESSION_HANDOVER_2026-08-04_coordinator —
   one pack, date reconciled to 2026-08-04.
3. Byte provenance: the mobile-session sandbox originals were
   unrecoverable; this file was reconstructed from the email transfer
   (content verified word-for-word, original emphasis/wrapping lost)
   and re-pinned 2026-08-06. Extension of the WS-E 60 shape:
   transform in transit, content intact.
