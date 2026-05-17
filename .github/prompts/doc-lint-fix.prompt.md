---
name: doc-lint-fix
description: "Rewrite Markdown to satisfy lint rules and match the doc architecture model."
agent: "Delivery Lead"
argument-hint: "scope=<file or folder> constraints=<style rules>"
---


Argument handling:

- If arguments are provided, treat them as authoritative.
- If arguments are omitted, infer missing values from the current workspace, active file, and session context.
- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.
- Do not fail solely because arguments were omitted.

Inputs:

- scope: ${input:scope:file path or folder to lint-fix}
- constraints: ${input:constraints:style constraints, preserve-all-content}

Act as a Delivery Lead and rewrite the provided Markdown to satisfy doc standards.

Constraints:

- Preserve meaning
- Improve structure and headings
- Fix link style (relative intra-repo)
- Fix code fences (language identifiers where possible)
- Do not remove existing information, procedures, or examples
- If content is reorganized, preserve traceability (source section → target section)
- When validating CoDev docs, use tracked and non-ignored repository files only; never inspect `external/` or gitignored paths

Output:

- lint-fixed Markdown content
- list of changes made
- link and heading hierarchy verification checklist

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Delivery Lead** | always — lint and rewrite | *(this prompt)* | Lint-fixed Markdown produced, no info lost |
| 2 | **Reviewer** | significant restructuring occurred | `/pr-review` | Content integrity confirmed, heading hierarchy valid |
| 3 | **Delivery Lead** | changes ready to merge | `/pr-review` | PR approved, markdownlint passes in CI |
