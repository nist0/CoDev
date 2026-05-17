---
name: mermaid-create
description: "Generate a Mermaid diagram from a natural-language description. Outputs a GitHub-ready fenced code block with prose context."
agent: mermaid-diagrammer
argument-hint: "type=<flowchart|sequence|class|er|state|gitGraph|gantt|mindmap|timeline|c4> description=<what to diagram>"
---


Argument handling:

- If arguments are provided, treat them as authoritative.
- If arguments are omitted, infer missing values from the current workspace, active file, and session context.
- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.
- Do not fail solely because arguments were omitted.

Inputs:

- type: ${input:type:flowchart|sequenceDiagram|classDiagram|erDiagram|stateDiagram-v2|gitGraph|gantt|mindmap|timeline|C4Context}
- description: ${input:description:describe what the diagram should show}
- direction: ${input:direction:LR|TD|RL|BT} (for flowcharts only, default: LR)

Requirements:

- Select the most appropriate Mermaid diagram type if `type` is not specified.
- Use stable, meaningful node IDs aligned with the described domain vocabulary.
- Apply `v2` variants (`stateDiagram-v2`, `flowchart` over `graph`).
- Keep node count ≤ 50 and depth ≤ 5 levels.
- Use subgraphs for logical grouping where appropriate.
- No deprecated syntax (`graph LR`, `stateDiagram` v1).
- No beta features that may not render on GitHub stable.
- Add a one-sentence prose description for accessibility.

Output:

1. Selected diagram type + rationale (1 line)
2. Mermaid code block (fenced with ` ```mermaid `)
3. Prose description (1–2 sentences)
4. Embedding snippet (ready to paste into a GitHub Markdown file)
5. Self-check: [ ] correct fencing, [ ] stable IDs, [ ] depth ≤ 5, [ ] no deprecated syntax, [ ] prose added

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|---|---|---|---|---|
| 1 | **mermaid-diagrammer** | always — diagram creation | *(this prompt)* | Diagram produced, self-check complete |
| 2 | **mermaid-diagrammer** | diagram > 10 nodes or complex logic | `/mermaid-review` | Review verdict: approved |
| 3 | **Delivery Lead** | diagram committed to repo | `/pr-review` | PR approved, rendering verified |
