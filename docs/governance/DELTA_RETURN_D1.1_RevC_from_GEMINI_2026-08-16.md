# DELTA RETURN — D1.1 Test Plan RevC — GEMINI

**Delta round · Received 2026-08-16 (session of 2026-08-15)**
**Reviewed hash:** `9d6ab3b0da21d5e6603f7fa505d48a892da9acf11dba60725b83e5a8c590e88c` (per delta pack §1; this return did not restate it)
**Scope:** F-GEM-REG-01 (as ruled down to MATERIAL), F-GEM-REG-02, F-GEM-REG-03, F-GEM-REG-04 (composite with F-DS-11) — residual MATERIALs per delta pack §5

*Provenance: received via the coordinator conversation and transcribed
verbatim by the coordinator; transported to disk by the operator.*

*Exchange note, recorded for the trail: the reviewer's first two
responses were document summaries containing no verdicts and were
rejected as non-responsive. This return was produced on the third
prompt, a structured verdict-template prompt naming the prior failure.
The verdicts below are the reviewer's own, produced against the
implementing text; the two rejected summaries were not landed and are
not part of the round's evidence.*

---

F-GEM-REG-01: DISCHARGED
Reasons: Rev C §2.4 explicitly bars Regime-2 evidence from being cited externally as typology coverage until the manifest typology field and controlled vocabulary land. Furthermore, Appendix B item 15 establishes the manifest typology field as a required pre-B7-exit owed item. This faithfully incorporates the Chair's adopted remedy regarding external citation restrictions without imposing an execution hard gate.

F-GEM-REG-02: DISCHARGED
Reasons: Rev C §5.4 incorporates an absolute `top_k` cap per scenario class alongside the existing 10% ratio calculation. The text explicitly mandates that any corpus expansion pushing a scenario's `top_k` beyond this capped ceiling requires a formal, ruled variance. The implementing text fully satisfies the requirements of the adopted remedy.

F-GEM-REG-03: DISCHARGED
Reasons: Rev C §9.8 adds a machine-readable `invalidation_status` field to the D2.5 ledger schema. The section mandates that gate-evaluation and pre-flight tools filter out any entries flagged as invalidated during automated checks. This fulfills the Chair's adopted remedy without requiring cryptographic revocation signatures.

F-GEM-REG-04: DISCHARGED
Reasons: Rev C §9.5 element 3 restricts execution parameters to a named material-parameter list managed by the runner build whose hash is embedded in the environment identity. Additionally, Rev C §8.1 adds `environment_config_sha256` as an explicit pre-flight verification criterion. Together, these sections fully implement the composite remedy for F-GEM-REG-04 and F-DS-11.

Dissent: NONE
