---
name: markdown-docops
description: Markdown doc operations for production, modification, linting, restructuring, conversion, import, and export.
argument-hint: "[operation] [scope]"
user-invocable: true

disable-model-invocation: false
---

# markdown-docops Skill (Elite)

## When to use

- You need to create or refactor Markdown documentation at scale.

- You need doc lint fixes, structure normalization, or format conversion.

- You need import/export workflows while preserving traceability.

## Procedure

### 1. Inventory existing docs first

- Reuse existing pages and sections where possible.

- Avoid duplicate topics; link or merge with existing references.

### 2. Apply DAM structure

- Organize by purpose (onboarding, architecture, runbook, reference).

- Keep headings consistent and lint-friendly.

- See: `doc-architecture-model` skill for the full DAM procedure.

### 3. Lint and quality checks

- Enforce heading hierarchy, fenced code block languages, and link validity.

- Preserve relative links and stable anchors.

- Run: `npx markdownlint-cli2 "**/*.md"` and `npx markdown-link-check`.

- See: `doc-qa` skill for the full lint procedure.

### 4. Conversion and migration

- When converting formats, preserve metadata and section intent.

- Keep a mapping log from source → target.

### 5. Publish-ready verification

- Confirm navigability and cross-links.

- Document what changed and why.

## Self-check

- [ ] No duplicate topic introduced.

- [ ] DAM structure respected (onboarding / architecture / runbook / reference).

- [ ] Conversion traceability preserved (source → target mapping logged).

- [ ] Lint passes (`markdownlint-cli2`) and no broken links.

- [ ] Relative links and stable anchors preserved.

## Deliverables

- Updated Markdown content.

- Restructure/conversion notes.

- Lint and link-check results.
