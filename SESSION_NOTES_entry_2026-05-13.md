## 2026-05-13 — First working session after scaffolding (Claude session 2)

### What was built / decided / produced

- Sized `ArcaAI_System_Architecture.docx` (v1.0) against exec deck v12 and the three foundational ADRs. Finding: ~15% MIGRATE-light, ~40% ADAPT-substantial, ~25% ARCHIVE, ~20% NET-NEW. Estimated 2-3 days of rework. CONTRADICTS all three ADRs in multiple places. Not a quick-edit job.
- Sized `ArcaAI_Banking_Architecture_v0_4.docx` against the same anchors. Finding: substantially better aligned — the five layers, the principles, and the eleven use cases are largely usable. Still pre-ADR in places (especially conflates LLM "starter kit" framing with predictive-model "reference model" framing per ADR-0001).
- Confirmed `ArcaAI v0grok audit.docx` is not an audit — it's a Grok-authored v0.3 rewrite that pre-dates v0.4. Set aside.
- Pivoted from "build a rationalisation framework first" to "draft specs against exec deck + ADRs, harvest from legacy docs as we go." Rationalisation map becomes a side artefact, not a primary deliverable.
- Produced **Spec 01 Working Brief v0.2** (`spec-01-working-brief.md`). Ten sections: purpose, audience tiering, Spec 01/02 boundary, inferred section roadmap, harvest map, three (now four) pieces of active work, open questions, sister specifications, definition of done, drafting effort estimate.
- Incorporated three pieces from an unsolicited ChatGPT review of the exec deck: a sharper single-sentence proposition ("sovereign AI intelligence layer..."), the need to position against four market categories (added consulting/services as the fourth), and the tiered-read pattern across the Describer Pack.

### Key reasoning that won't be obvious from the committed files

**On reframing away from the rationalisation map.** The session started intending to build a rationalisation framework. Two sizings in, the picture became clear: legacy docs are at varying distances from gold standard, and the right action is not to "rationalise then draft" but to "draft from exec deck + ADRs, harvesting where useful." This makes the legacy docs into harvest sources, not migration objects. SESSION_NOTES from session 1 framed the rationalisation map as the next substantive work; this session supersedes that — the map *emerges* from spec drafting rather than preceding it.

**On the gold-standard anchor being two things, not one.** Originally Mike framed the exec deck v12 as gold standard. Reading both legacy docs end-to-end, the sharper rule is: content is correct if it aligns with **both** the exec deck **and** the three foundational ADRs. The exec deck itself has places where it hasn't yet caught up to the ADRs (slide 21's "9 pre-trained starter models, signed and pinned" language is ADR-0001-pre, not ADR-0001-aligned). So the anchor is the pair, not a single document. This is the rationalisation rule for everything that follows.

**On why the brief stopped short of any spec prose.** The `specs/_template.md` was not uploaded this session. The Charter and SESSION_NOTES say the template has 11 sections with a non-negotiable section 4 sister-specifications discipline. Drafting prose against an assumed structure would have produced rework when the template arrived. The brief is robust to whatever the template requires; prose would not have been. This is the right discipline for session 2 — do the structural thinking, defer the prose.

**On selectively integrating the ChatGPT review.** The review scored ArcaAI 9.2/10 with no critical posture — that's a tell that it's a sympathetic readback, not an SME critique. Three pieces from it were genuinely useful (the sharper proposition language, the fourth market category, the tiered read pattern). Everything else (the scores, the Big Four comparisons, the commercial pricing recommendations, the SWOT, the "acquisition target" framing) was either out of design-phase scope per the Charter or insufficiently grounded. Important precedent: SME-class reviews need adversarial pressure to be useful. ChatGPT in its default register doesn't provide that; the Charter is right to cast Grok and DeepSeek for adversarial roles and to position ChatGPT as a secondary AI engineering critic, not a primary reviewer. Future sessions should treat unprompted "is this good?" reviews with caution.

**On the three pieces Spec 01 must actively advance beyond the legacy.** The brief names them: (a) sharpen ADR-0001 language to distinguish open-weight LLMs (inherited as-is) from predictive ML models (reference models, upskilled by the bank); (b) introduce the three-stage lifecycle by name in bank-reader prose; (c) position pipeline-as-platform in language that pre-empts the "why can't we just take the models?" objection. The fourth piece (positioning against consulting/services as a fourth category) was added late based on the ChatGPT review. These are the four places Spec 01 cannot just harvest — it must do new work. Future sessions drafting Spec 01 should not let harvest-mode dominate these four sections.

### Settled decisions — do NOT re-open

1. **The rationalisation map is not a primary deliverable.** It emerges from spec drafting. Future sessions should not propose building it as a standalone exercise.
2. **The gold-standard anchor is `(exec deck v12) AND (the three foundational ADRs)`.** Not the exec deck alone. Where they diverge, ADRs win; the exec deck gets revved.
3. **Spec 01 is drafted before any other spec.** Reason: it gates the audience and positioning that Specs 02-08 must align to.
4. **Eleven use cases, not nine.** Banking Architecture v0.4 §2 is the canonical list. Exec deck slide 11 (which lists nine) needs revving, not the other way around.
5. **Banking Architecture v0.4 §2 use case table is harvest-quality and will be lifted near-verbatim into Spec 01 §5** at draft time, with light editing.
6. **`ArcaAI_System_Architecture.docx v1.0` is not a Spec 01 source.** It is a Spec 02/03 source at best, and even there mostly contradicts. Do not return to it for Spec 01 drafting.

### Open questions surfaced in this session

- **ADR-0004 (Target Market Segment) — gates Spec 01 §6.** Working assumption proposed: UK + Ireland focus, EU follow. Spec 01 can be 80% drafted before ADR-0004 lands; §6 will be provisional. Trigger for resolution: Month 2 per original SESSION_NOTES plan, unchanged.
- **The exec deck v12 needs revving in three specific places** to align with the ADRs: slide 10 ("inherited base · bank-owned specialisation" — close but not ADR-0001-aligned); slide 11 (nine verticals — should be eleven); slide 21 ("9 pre-trained starter models, signed and pinned" — ADR-0001-pre framing). Trigger for resolution: after Spec 01 reaches v0.9, not before — the spec will sharpen the language and the exec deck rev follows.
- **5-slide Board Deck as a Describer Pack asset.** Plausibly missing from the current Implementation Pack design. Belongs to the Describer Pack workstream, not Spec 01. Flag for RFC when Describer Pack is scoped.
- **Whether SESSION_NOTES session-1 reference to "v0.6 architecture" was accurate or a misread.** The disk shows v0.4 as latest. Not material for now.

### Next concrete action

**Upload `specs/_template.md` at the start of next session.** Then draft Spec 01 against the working brief v0.2. Confirm or amend the four key calls in the brief (Spec 01/02 boundary, eleven use cases, ADR-0004 working assumption, four active-work pieces) before drafting begins. Expected drafting effort to v0.1: ~6 hours / two daily sessions.
