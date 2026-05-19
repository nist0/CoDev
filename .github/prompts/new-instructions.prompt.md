---
name: new-instructions
description: Create a new scoped instruction file with applyTo and concise rules.
agent: promptsmith

## argument-hint: "file=<name>.instructions.md applyTo=<glob> rules=<text>"

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Inputs:

- file: ${input:file:ex python.instructions.md}

- applyTo: ${input:applyTo:ex **/*.py}

- rules: ${input:rules:bullet rules}

Requirements:

- Create `.github/instructions/${input:file}`

- Must include frontmatter `applyTo: ...`

- Keep rules short; avoid duplicates

Output: plan + file content + checklist.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **PromptSmith** | always — instruction file creation | *(this prompt)* | .github/instructions/<file> created with correct `applyTo` and concise rules |
| 2 | **Reviewer** | rules touch security, routing, or testing standards | `/pr-review` | No contradictions with existing instruction layers |
| 3 | **Delivery Lead** | instruction file ready | `/pr-review` | PR merged, `validate-customization-registry.py` passes |
