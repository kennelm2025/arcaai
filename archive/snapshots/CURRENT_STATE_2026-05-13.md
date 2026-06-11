# Current State

**Last updated:** 2026-05-13, end of working session 2
**Phase:** Design — Month 1, Week 1

---

## What just happened

Second working session after scaffolding. Pivoted from "build a rationalisation framework" to "draft specs from exec deck + ADRs, harvest from legacy docs as we go." Produced **Spec 01 Working Brief v0.2** — the structural brief that gates Spec 01 drafting.

Sized two legacy docs against the gold-standard anchor (exec deck v12 + the three ADRs):
- `ArcaAI_System_Architecture.docx v1.0` — heavily out of date, ~2-3 days of rework, CONTRADICTS all three ADRs in multiple places
- `ArcaAI_Banking_Architecture_v0_4.docx` — substantially aligned, harvest-quality for Spec 01 §1-2 and §5

## What's in flight

| Item | State | Blocked on |
|---|---|---|
| Spec 01 Working Brief | v0.2 drafted, ready for review | Mike's read of brief, especially §6 (the four active-work pieces) |
| Spec 01 draft | Not started | `specs/_template.md` upload; brief confirmation |
| ADR-0004 (Target Market Segment) | Deferred to Month 2 per session 1 plan | — |
| ADR-0005 (Data Strategy) | Deferred to Month 2 per session 1 plan | — |
| Exec deck v13 rev | Deferred until Spec 01 reaches v0.9 | Spec 01 §7 reaching draft state |
| Other seven specs | Not started | Spec 01 reaching v0.9 |

## What's blocked

- **Spec 01 §6 (Who ArcaAI is for)** — needs ADR-0004 working assumption confirmed (UK + Ireland focus, EU follow). Brief proposes drafting around this; Mike to confirm at next session start.
- **Spec 01 drafting overall** — needs `specs/_template.md` uploaded. Brief is template-agnostic by design; prose drafting is not.

## What's changed in the risk register

- **Mid-task chat exhaustion (Risk 1):** monitored this session — closed at ~95 min in a 100 min window with intact closure. Working.
- **Re-argued decisions (Risk 3):** session re-opened the question of "rationalisation map first vs spec draft first" — concluded that the original SESSION_NOTES-session-1 intention (build rationalisation map) was wrong, and the new approach (drafts lead, map emerges) supersedes it. **This is a settled decision in SESSION_NOTES session 2; future sessions must not re-litigate.**
- **New risk surfaced:** SME-style reviews without adversarial pressure (e.g. the ChatGPT exec deck review at 9.2/10) can produce false confidence. Charter's casting of Grok and DeepSeek as adversarial reviewers becomes more important than it looked at scaffolding time. Mitigation: when sympathetic reviews land, treat them as input not validation; require adversarial pressure separately.

## Next session opening

Per Session Opening Protocol — Mike's opening message should:
1. Confirm Claude Project knowledge is current OR re-upload the scaffold
2. State: *"Today we draft Spec 01 Product Definition against the working brief v0.2."*
3. **Upload `specs/_template.md`** — non-negotiable, brief explicitly waits on this
4. Optionally upload `ArcaAI_ML_Pipeline_v0.2.docx` if drafting will reach §5 (eleven use cases) and we want to cross-check use case detail

Expected next-session length: full 3-hour daily session minimum. Spec 01 v0.1 is ~6 hours of drafting total — two sessions, or one focused day if available.
