---
name: mcp-analyze
description: "Analyze an existing MCP design or configuration for topology correctness, least privilege, and VS Code or GitHub Copilot fit."
agent: mcp-specialist
argument-hint: "target=<mcp.json path, agent file, or design description> [host=<vscode|github-copilot|both>]"
---

Apply the procedure from `.github/skills/mcp-integration/SKILL.md`.

Goal: review an existing MCP setup and return the smallest safe set of changes needed to make it correct, least-privilege, and verifiable.

Inputs:

- target: ${input:target:mcp.json path, agent file path, or design description}
- host: ${input:host:vscode | github-copilot | both | unknown}

## Step 1 - Gather missing review context

If the input is incomplete, ask in one message for the missing facts only:

1. The current MCP config or design snippet
2. Where it is used: VS Code chat, GitHub Copilot custom agent, or both
3. Whether the server is local or remote
4. Whether the current behavior is acceptable, failing, or risky

## Step 2 - Analyze the current state

Assess explicitly:

- host, client, server model
- tools vs resources vs prompts choice
- transport fit: stdio vs HTTP
- install target fit: workspace, user, or remote config
- trust posture and secret handling
- whether MCP is appropriately scoped to the current role or workflow

## Step 3 - Emit the review

Output exactly this structure:

```markdown
## MCP review

**Target**: <target>
**Intent**: analyze
**Host**: <vscode | github-copilot | both | unknown>
**Verdict**: approved | rework required

### Findings
- <fact or issue>

### Recommended changes
1. <minimal change>

### Verification
1. <exact step>
2. <safe sample request>

### Residual risk
- <what remains after the changes>
```

## Rules

- Keep the review MCP-specific.
- Prefer the smallest safe delta over redesigning the whole setup.
- Flag over-broad tool exposure explicitly.
- Flag secret-handling problems explicitly.
- If the setup belongs in generic `vscode` guidance rather than MCP, say so.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **mcp-specialist** | always - MCP config/design review | *(this prompt)* | MCP review and minimal changes produced |
| 2 | **Router** | broader workflow unclear after review | `/route <follow-up request>` | Correct next agent/prompt selected |
| 3 | **Reviewer** | MCP framework asset changes are proposed | `/pr-review` | Review verdict issued |
