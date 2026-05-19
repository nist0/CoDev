---
name: generate-docs-tree
description: "Propose a docs/ tree aligned with the Documentation Architecture Model."
agent: "Delivery Lead"

## argument-hint: "scope=<repo or module> existing-docs=<path>"

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Act as a Delivery Lead and propose a `docs/` tree aligned with the DAM.

Include:

- Tree (folders/files)

- Templates per doc type

- Migration plan (phased)

- No-removal preservation notes for existing documentation content

- Anti-duplication mapping (existing docs → target canonical location)

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Delivery Lead** | always — docs tree proposal | *(this prompt)* | Tree structure proposed, migration plan and anti-duplication map produced |
| 2 | **Delivery Lead** | content migration needed | `/markdown-ops` | Content moved, no info loss, links intact |
| 3 | **Reviewer** | new docs structure merged | `/pr-review` | Structure approved, no dead links |
| 4 | **Delivery Lead** | approved | `/pr-review` | PR merged, docs/ structure committed |
