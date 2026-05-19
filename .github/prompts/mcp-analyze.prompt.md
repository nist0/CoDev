---
name: mcp-analyze
description: "Analyze an existing MCP design or configuration for topology correctness, least privilege, and VS Code or GitHub Copilot fit."
agent: mcp-specialist

argument-hint: "target=<mcp.json path, agent file, or design description> [host=<vscode|github-copilot|both>]"
---

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Apply the procedure from `.github/skills/mcp-integration/SKILL.md`.

Goal: review an existing MCP setup and return the smallest safe set of changes needed to make it correct, least-privilege, and verifiable.

Inputs:

- target: ${input:target:mcp.json path, agent file path, or design description}

- host: ${input:host:vscode | github-copilot | both | unknown}

Single source of truth:

- MCP review methodology and analysis criteria are defined in `mcp-integration`.

- Do not restate or redefine those procedures here.

Execution contract:

1. Gather only missing MCP review context.

2. Analyze topology, least privilege, and host fit.

3. Recommend the smallest safe set of changes.

4. Provide verification steps and residual risk.

Required output sections:

- MCP review summary and verdict

- Findings

- Recommended changes

- Verification

- Residual risk

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **mcp-specialist** | always - MCP config/design review | *(this prompt)* | MCP review and minimal changes produced |
| 2 | **Router** | broader workflow unclear after review | `/route <follow-up request>` | Correct next agent/prompt selected |
| 3 | **Reviewer** | MCP framework asset changes are proposed | `/pr-review` | Review verdict issued |
