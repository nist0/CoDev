---
name: explain-code
description: "Explain code and produce documentation-ready explanations."
agent: "Architect"
argument-hint: "scope=<file or module> depth=<summary|detailed>"
---


Argument handling:

- If arguments are provided, treat them as authoritative.
- If arguments are omitted, infer missing values from the current workspace, active file, and session context.
- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.
- Do not fail solely because arguments were omitted.

Apply the procedure from `.github/skills/repo-understanding/SKILL.md`.

Inputs:

- scope: ${input:scope:file path or module to explain}
- depth: ${input:depth:summary|detailed}

Output:

- Summary
- Key flows
- Invariants/assumptions
- Risks/edge cases
- Doc-ready snippet (Markdown)

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Architect** | always — code explanation | *(this prompt)* | Summary, flows, invariants, and risks documented |
| 2 | **Delivery Lead** | documentation update needed | `/generate-docs-tree` or `/markdown-ops` | Doc-ready snippet integrated into docs/ |
| 3 | **Architect** | test coverage gap identified | `/test-plan` then `/write-tests` | Missing tests authored and passing |
| 4 | **Delivery Lead** | changes committed | `/pr-review` | PR approved, CI green |
