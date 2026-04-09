---
name: mermaid-review
description: "Review an existing Mermaid diagram snippet for syntax errors, deprecated patterns, GitHub rendering compatibility, and best-practice violations. Returns structured verdict + improved version."
agent: mermaid-diagrammer
argument-hint: "snippet=<mermaid code block or file path>"
---

Inputs:

- snippet: ${input:snippet:paste your Mermaid code block or provide the file path}
- context: ${input:context:where will this diagram be used? e.g. GitHub README, ADR, wiki}

Requirements:

- Parse the diagram for: syntax errors, unclosed `subgraph`/`end`, missing arrows, undefined node references.
- Check for deprecated patterns: `graph LR` → should be `flowchart LR`; `stateDiagram` → should be `stateDiagram-v2`.
- Check GitHub rendering constraints: node count, beta features, special characters in labels (`<`, `>`, `&`).
- Check best practices: stable IDs, clear labels, correct direction, prose description present.
- Produce an improved version if issues are found.

Output:

1. **Verdict**: `approved` | `rework required`
2. **Issues found** (numbered list, or "None"):
   - Severity: `error` (breaks rendering) | `warning` (degrades quality) | `suggestion` (nice-to-have)
3. **Improved diagram** (if `rework required`): full corrected Mermaid code block
4. **Diff summary**: what changed and why
5. Self-check: [ ] no syntax errors, [ ] no deprecated syntax, [ ] GitHub-compatible, [ ] prose description present

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|---|---|---|---|---|
| 1 | **mermaid-diagrammer** | always — diagram review | *(this prompt)* | Verdict produced, improved version provided if needed |
| 2 | **mermaid-diagrammer** | verdict = rework required | `/mermaid-create` (re-generate) | Improved diagram passes review |
| 3 | **Delivery Lead** | reviewed diagram committed | `/pr-review` | PR approved |
