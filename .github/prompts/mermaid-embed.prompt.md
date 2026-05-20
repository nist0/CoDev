---
name: mermaid-embed
description: "Embed a Mermaid diagram into an existing Markdown file (GitHub README, ADR, wiki, PR description). Handles correct fencing, placement, prose context, and accessibility."
agent: mermaid-diagrammer

argument-hint: "file=<path or description of target markdown> diagram=<mermaid snippet or description> section=<heading to embed under>"
---

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Inputs:

- file: ${input:file:path to target Markdown file, or describe it}

- diagram: ${input:diagram:existing Mermaid snippet to embed, or description to generate one}

- section: ${input:section:heading or section name to embed the diagram under}

- generate: ${input:generate:yes|no} (generate a new diagram if none provided)

Requirements:

- Locate the target section in the Markdown file (by heading text).

- If `diagram` is a description (not code), invoke diagram generation first.

- Insert the diagram with correct fencing (` ```mermaid ... ``` `).

- Add a one-paragraph prose description immediately after the heading and before the diagram.

- Add a one-sentence summary after the diagram for accessibility.

- Do not embed duplicate diagrams -- check if an equivalent diagram already exists in the section.

- Do not modify any content outside the target section.

Output:

1. **Target location**: file path + heading anchor

2. **Prose context** (before diagram): 1-3 sentence description

3. **Mermaid code block** (fenced, ready to paste)

4. **Accessibility summary** (after diagram): 1 sentence

5. **Full updated section** (Markdown snippet, ready to replace)

6. Self-check: [ ] correct fencing, [ ] prose before + after, [ ] no duplicate diagram, [ ] only target section modified

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|---|---|---|---|---|
| 1 | **mermaid-diagrammer** | always -- diagram embedding | *(this prompt)* | Embedding snippet produced |
| 2 | **mermaid-diagrammer** | diagram not provided / needs generation | `/mermaid-create` | New diagram generated and reviewed |
| 3 | **mermaid-diagrammer** | existing snippet provided | `/mermaid-review` | Snippet approved before embedding |
| 4 | **Delivery Lead** | file updated | `/pr-review` | PR approved, diagram renders correctly |
