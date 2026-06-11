# Prompt templates

Versioned prompt templates per vertical (Blueprint S13.2). Populated from B6.
Layout: `<vertical>/system.yaml`, `<vertical>/output.yaml`, `shared/output_packaging.yaml`,
`shared/uncertainty.yaml`. Every MLflow model run logs `prompt_template_version` as a tag.
Changes require PR review - treated with the same seriousness as training-code changes.
