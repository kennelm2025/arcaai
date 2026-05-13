# Archive

This directory holds legacy ArcaAI documents that have been retired but whose provenance and content remain useful as reference. Nothing in this directory is canonical — the canonical specifications live in `/specs/`.

## Why an archive?

ArcaAI has accumulated a substantial body of work over the months preceding this design phase:

- Banking Architecture v0.6 (Word document)
- ML Pipeline v0.3 (Word document)
- Engineering Blueprint (Word document)
- System Architecture (Word document)
- Technical Infrastructure (Word document)
- Executive Presentation v12 (PowerPoint)
- Plus various earlier versions, working drafts, and side documents

These documents contain real value — analysis, decisions, language, design choices — that must not be lost. But they cannot be the source of truth going forward. The design phase rationalises this body of work into the eight canonical specifications.

Documents that are retired into this archive have:

1. Had their useful content extracted into the new specifications
2. Been recorded in the rationalisation map (`rationalisation-map.md`, to be created) showing what migrated where
3. Been committed to this archive at their final state with a brief note explaining when and why they were retired

Future contributors who want to understand "where did this design choice come from" can trace it back through the rationalisation map to the originating document in this archive.

## What goes here

- Final versions of retired documents in their original formats (`.docx`, `.pptx`, etc.) with a `.md` companion summarising what they contained and when they were archived
- The rationalisation map showing what migrated to which specification

## What does not go here

- Working drafts of current specifications (those live in the relevant `/specs/` folder on a feature branch)
- Old versions of current specifications (those live in git history; that's what versioning is for)
- Personal notes, side documents, ephemera (those don't belong in the repository at all)

## Rationalisation map

To be created in the first week of Month 1 of the design phase, once existing documents are made available to the team for review. The map will list every existing ArcaAI document, what it contains, and which specification(s) consume its content.

The rationalisation map is itself a specification-grade deliverable — it provides the audit trail for every claim that migrates from the legacy corpus into the canonical specs.

## Initial state

Empty. Legacy documents will be added in Week 2 of the design phase.
