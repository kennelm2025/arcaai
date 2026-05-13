# Diagrams

All diagrams used in ArcaAI specifications live here as **source files**, not as rendered images. Source files are version-controlled, editable, and reviewable. Image files are not.

## Tooling

Two diagram tools are supported, in this order of preference:

1. **Mermaid** (`.mmd`) — preferred for most diagrams. Renders directly in GitHub. Wide tool support. Lower friction.
2. **PlantUML** (`.puml`) — for diagrams Mermaid cannot express well (complex sequence diagrams, advanced layouts, certain notation requirements).

Other tools (Lucidchart, Draw.io, Visio, etc.) are **not** used. They produce binary or proprietary formats that cannot be diffed or reviewed properly.

## Conventions

### File naming

`<spec-id>-<short-descriptive-name>.<ext>`

Examples:
- `02-five-layer-architecture.mmd`
- `04-three-stage-lifecycle.mmd`
- `06-integration-topology.puml`

For diagrams not tied to a single spec, use:
`platform-<short-name>.<ext>`

### Colour palette

To be defined as the first diagrams are produced. The provisional palette inherits from existing ArcaAI design work and should be defined in a `style-guide.md` file added when the first diagrams are committed.

### Component naming in diagrams

Components named in diagrams must match the component names used in the relevant specifications. The shared glossary (`/glossary/`) is the source of truth for component names.

## Rendering for releases

Diagrams are rendered to PNG and SVG at Implementation Pack release time, not committed to `main`. The release workflow renders all diagrams, includes them in the release artefact, and discards the renderings.

This means:
- The repository stays clean (no binary blobs proliferating)
- Diagrams in releases always match the source at release time
- Rendering is reproducible — anyone with the source can produce the same image

## How to add a diagram

1. Create the source file in this directory
2. Reference it in the relevant specification by filename and figure number
3. Open a PR including both the source file and the specification change
4. Review covers both the diagram and the specification

## How to update a diagram

1. Edit the source file
2. Update the figure caption in the referencing specification if relevant
3. Open a PR
4. The diff makes the change reviewable — which is the whole point of source-controlled diagrams
