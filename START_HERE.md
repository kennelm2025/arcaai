# START HERE

Entry path for any new session — human or AI. Read in this order:

1. **README.md** — what ArcaAI is, repo map, current phase
2. **DECISIONS.md** — the rulings (R1–R13) and ADRs that bind everything
3. **BUILD_TRACKER.md** — live stage status; find the next NOT STARTED gate
4. **CURRENT_STATE.md** — narrative state + open items as of last update
5. **docs/governance/ArcaAI_Build_and_Quality_Plan_v1.0.docx** — stage definitions B1–B12
6. The locked suite in `docs/governance/` as needed (Banking Architecture v1.0b is the
   reference architecture; Engineering Blueprint v1.1 is the ML Pipeline sister document)

## Session protocol (founder + AI pairing)

- Work the next unpassed gate in BUILD_TRACKER.md; don't skip stages
- Any deviation from a locked document → entry in DECISIONS.md before the code merges
- Update BUILD_TRACKER.md and CURRENT_STATE.md at session end; commit from the repo
  (never edit governance files outside `D:\ArcaAI-repo\arcaai`)
- SESSION_NOTES.md gets a dated entry per significant session; snapshots → archive/snapshots/
