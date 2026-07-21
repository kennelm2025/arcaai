# Governance Review — Workstream C outcome

**Specifications currency. Run 21 Jul 2026. Panel: founder + Claude (audit).**
Method: full inventory of docs/ spec-regime artefacts; currency audit against
/DECISIONS.md (the operative regime); content disposition of the sole
substantive pre-lockdown artefact; remediation in this PR. Change record:
DEC-0007. CL ledger: GOVERNANCE_REVIEW_CHANGELOG.md (declared canonical
per DEC-0007).

## Findings

**F-C01 — Orphaned spec regime.** docs/specs/ (README + eight section
folders + template) described an eight-spec / three-SME-round regime
superseded by the June 2026 lockdown before any spec was drafted. No
tombstone existed; a reader would conclude ArcaAI has no specifications
when it has seven locked documents. *Remediated: tombstones in place on
the README and all eight section READMEs, pointing at /DECISIONS.md.
Folders retained so stale links fail loudly.*

**F-C02 — Stale working brief.** working-briefs/spec-01-working-brief-
v0.2.md (13 May) fed the dead regime. Content dispositioned at
retirement: superseded items enumerated in its tombstone; section 6a
re-homed as CL-19 (model-kinds distinction; glossary already carries the
canonical language); section 6d re-homed as CL-20 (fourth competitive
category, consulting/services); section 7e consciously dropped to WS3.1
scoping (board-deck / reader-tiers observation), no CL item. *Remediated:
tombstone with full disposition.*

**F-C03 — Stale tail in DECISIONS.md.** Closing line asserted a build
position ("Next: build stages B1-B2") in a document whose own ruling
(EB8) places build status in BUILD_TRACKER.md. *Remediated: line now
points at the tracker, removing the staleness class, not just the
instance.*
**F-C04 — Same-vintage documents, per-document verdicts.**
docs/rfcs/: RETIRED — the RFC mechanism was never used; operative change
control is DEC entries + ADRs (precedent DEC-0005/ADR-0009). Tombstoned;
template retained. docs/glossary/README.md: OPERATIVE — fifteen live
definitions consistent with ADR-0001/0002/0003 and ruling R9; light
currency pass applied (regime references retired, R3 control-layer
strapline added to the ArcaAI definition, SA line retargeted at the
locked suite). DESIGN_PHASE_CHARTER.md: HISTORICAL — the phase completed
at lockdown (build entry gate PASSED); header added; not superseded,
finished.

**F-C05 — Observation (WS-E ledger candidate, no WS-C action).** ~2MB of
binary Office documents version-controlled by filename suffix inside
git, in a repo with a prior LFS incident. Workable while the suite is
locked (no churn); flagged for WS-E awareness.

**F-C06 — CL ledger unnamed.** The full CL-01..CL-18 series lived in
GOVERNANCE_REVIEW_CHANGELOG.md with state and cross-references, but
nothing declared it canonical; handovers restated the backlog from
memory and B5_GATE.md scoped CL-12/13 without pointing home.
*Remediated: declared canonical in the changelog and in DEC-0007;
CL-19/20 appended there and nowhere else.*

## Not findings

The locked suite's content ageing relative to the build (B1-B5) is
governed by design: DEC entries record deviations, CL-17 carries the
DEC-0006 wording rule to next revisions. That is the regime working.

## Session incidents (for WS-E ledger)

11. **Notepad markdown-view mangle (recurrence).** Markdown pasted into
Notepad was re-serialised with escaped asterisks/dashes and doubled
blank lines on save (57 insertions / 36 deletions on a 10-line edit;
caught by git diff --stat eyeball). Recovered via git checkout of the
file. Consequence: all WS-C markdown edits executed via PowerShell
[IO.File] writes (UTF-8 no-BOM); Notepad not used for markdown this
session. Candidate house-rule amendment for WS-E: prefer scripted
writes with git-diff verification over Notepad for .md files.

Also observed: one fused-paste parser error and one truncated
here-string paste (both refused/caught loudly, no damage) — the
single-commands rule and small-paste discipline re-earning their
place; one (base)-shell start caught by the prompt eyeball
(incident-8 tell).

## Exit

WS-C CLOSED. All findings remediated in this PR or re-homed to the CL
ledger. Next governance session: WS-D (Build & Quality Plan).