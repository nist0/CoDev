---
name: markdown-ops
description: "Produce, modify, lint, restructure, convert, import, and export Markdown docs with no info loss."
agent: "Delivery Lead"
argument-hint: "operation=<produce|modify|lint|restructure|convert|import|export> scope=<path>"
---


Argument handling:

- If arguments are provided, treat them as authoritative.
- If arguments are omitted, infer missing values from the current workspace, active file, and session context.
- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.
- Do not fail solely because arguments were omitted.

Inputs:

- operation: ${input:operation:produce|modify|lint|restructure|convert|import|export}
- scope: ${input:scope:docs path or file list}
- constraints: ${input:constraints:no info loss, style constraints, deadlines}

Requirements:

- Inventory existing docs first and prevent duplication.
- Preserve information while restructuring.
- Return lint-friendly Markdown and link integrity checks.

Output:

- plan
- affected docs map
- updated structure/content actions
- lint/link verification checklist

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Delivery Lead** | always — Markdown operation | *(this prompt)* | Operation complete, no info lost, lint-friendly output produced |
| 2 | **Reviewer** | structural changes or content migration | `/pr-review` | Content integrity confirmed, link integrity checked |
| 3 | **Delivery Lead** | changes ready | `/pr-review` | PR merged, markdownlint CI gate green |
