---
name: diagram-ops
description: "Produce, modify, validate, and convert architecture diagrams using PlantUML/Mermaid and open-source workflows."
agent: "Delivery Lead"

argument-hint: "operation=<create|modify|convert|validate> format=<plantuml|mermaid>"
---

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Inputs:

- operation: ${input:operation:create|modify|convert|validate}

- format: ${input:format:plantuml|mermaid}

- scope: ${input:scope:files or module scope}

Requirements:

- Keep source diagram files as canonical artifacts.

- Provide deterministic render/export guidance.

- Include QA checks for readability and stale references.

- When `format=mermaid`: delegate to `mermaid-diagrammer` via the appropriate Mermaid prompt.

Output:

- plan

- files/sections impacted

- diagram operations performed

- validation checklist

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Delivery Lead** | always -- diagram operation (PlantUML / convert / validate) | *(this prompt)* | Diagram produced/modified, validation checklist complete |
| 1b | **mermaid-diagrammer** | `format=mermaid` + operation=create | `/mermaid-create` | Mermaid diagram generated, self-check complete |
| 1c | **mermaid-diagrammer** | `format=mermaid` + operation=validate/modify | `/mermaid-review` | Verdict produced, improved version provided if needed |
| 1d | **mermaid-diagrammer** | `format=mermaid` + operation=embed in Markdown | `/mermaid-embed` | Diagram embedded with prose context and accessibility note |
| 2 | **Architect** | new architecture diagram (PlantUML) created | `/explain-code` (for narrative) | Diagram accuracy confirmed by domain expert |
| 3 | **Delivery Lead** | diagram committed to repo | `/pr-review` | PR approved, stale-reference check passed |
