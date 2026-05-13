# Current State

**Last updated:** 13 May 2026 (end of Claude session 1)
**Updated by:** Mike + Claude
**Cadence:** Weekly, every Friday end-of-week (plus end of each working session)

This file captures what is happening *right now*. It changes frequently. For stable context, see `PROJECT_CONTEXT.md`. For the reasoning behind decisions, see `SESSION_NOTES.md`.

---

## Phase

**Design phase, Week 1 — Scaffolding complete.**

The first chat session of the design phase has completed. The repository scaffold has been built, including continuity protocols for future sessions. Ready to push to GitHub.

## What just happened (Claude session 1)

The full repository scaffold was built in one continuous session, including:

- 9 root-level files (README, START_HERE, CONTRIBUTING, CHANGELOG, PROJECT_CONTEXT, CURRENT_STATE, SESSION_NOTES, SESSION_PROTOCOLS, DESIGN_PHASE_CHARTER)
- 3 foundational ADRs ratified
- Templates: ADR, RFC, spec
- 8 specification folder READMEs (placeholders)
- Full governance layer: document register, SME panel, review protocols, 5 SME prompt primers
- Supporting: diagrams README, glossary, archive, PR template

Total: 38 files. See `SESSION_NOTES.md` for the reasoning behind specific choices.

## Open this week (week 1 closeout)

| Item | Status | Owner | Notes |
|---|---|---|---|
| Repository scaffold | Complete | Claude | Built and packaged |
| Three foundational ADRs | Drafted, awaiting GitHub commit | Mike | ADR-0001, 0002, 0003 |
| SME panel composition | Documented | Claude | See governance/sme-panel.md |
| SME prompt primers | Drafted (5 primers) | Claude | One per SME |
| Design Phase Charter | Drafted | Claude | Lean constitution |
| Session protocols | Drafted | Claude | Opening + closure rituals |
| Push to GitHub | Pending | Mike | Private repo `github.com/<handle>/arcaai` |
| Claude Project setup | Pending | Mike | Attach stable scaffold files as Project Knowledge |

## Pending Mike decisions

| Decision | Why it's open | Target date |
|---|---|---|
| Target market segment | Strategic question, deferred from ADR-0003 conversation | Month 2, will become ADR-0004 |
| Data strategy details | Linked to target market | Month 2, will become ADR-0005 |
| First spec to draft | Suggested order: Product Definition first | Next session |
| Existing-doc rationalisation | Needs Mike to share existing docs with next Claude session | Next session |

## In SME review

Nothing in review yet. First SME review round runs once the first spec section is drafted, expected end of Week 2.

## Blocked / waiting

- Rationalisation of existing ArcaAI documents (v0.6 architecture, ML Pipeline, Engineering Blueprint, exec deck v12, System Architecture, Technical Infrastructure) — needs Mike to share these into a next working session
- GitHub repository creation — Mike to do, before next working session
- Claude Project setup — Mike to do, before next working session

## Risks being watched

| Risk | Current concern | Mitigation |
|---|---|---|
| Process-over-product trap | Spending weeks on governance before producing specs | Charter is time-boxed; Week 2 starts spec writing |
| SME review latency | Reviews could block production if serial | Three specs in flight in parallel max |
| Context drift across chats | Claude loses thread between sessions | SESSION_PROTOCOLS.md ritual + SESSION_NOTES.md reasoning trail + Claude Project setup |
| Strategic questions left open | Target market, data strategy not yet locked | Will resolve in Month 2 as part of Product Definition |
| Chat exhaustion mid-task | Production session hits context limit before closure | Chat health check protocol in SESSION_PROTOCOLS.md |

## Next session — concrete starting action

When Mike opens the next chat (Claude session 2):

1. Mike applies the Session Opening Protocol from `SESSION_PROTOCOLS.md`
2. The specific task is: **produce the rationalisation map of existing ArcaAI documents**
3. Mike will share the existing docs (v0.6 Banking Architecture, ML Pipeline, Engineering Blueprint, exec deck v12, System Architecture, Technical Infrastructure) at the start of the session
4. Claude reads them and produces `archive/rationalisation-map.md` showing what content migrates from each legacy doc into which of the eight canonical specs

After the rationalisation map, the next substantive work begins: drafting Product Definition (spec 01), with ADR-0004 (target market) and ADR-0005 (data strategy) addressed as the strategic questions inside that spec require.

## Next milestone

End of Month 1 — Foundations complete. Definition of "complete":

- All scaffold files reviewed and ratified
- Existing-doc rationalisation map produced
- SME panel process tested on a small piece (likely the Charter itself, sent through one review round)
- First spec (Product Definition) drafted to ~50% completeness
- Strategic questions on target market and data strategy resolved as ADR-0004 and ADR-0005
