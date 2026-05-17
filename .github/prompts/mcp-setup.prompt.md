---
name: mcp-setup
description: "Design and install an MCP integration for VS Code or GitHub Copilot with a guided intake, strict topology decisions, and least-privilege verification steps."
agent: mcp-specialist
argument-hint: "goal=<what you want to connect> [host=<vscode|github-copilot|both>] [server=<local|remote>] [transport=<stdio|http>] [install=<workspace|user|remote>] [auth=<none|local|api|org-managed>]"
---


Argument handling:

- If arguments are provided, treat them as authoritative.
- If arguments are omitted, infer missing values from the current workspace, active file, and session context.
- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.
- Do not fail solely because arguments were omitted.

Apply the procedure from `.github/skills/mcp-integration/SKILL.md`.

Goal: turn an MCP integration request into a concrete, safe setup plan for VS Code and/or GitHub Copilot.

Inputs:

- goal: ${input:goal:what tool, service, or workflow should MCP expose}
- host: ${input:host:vscode | github-copilot | both}
- server: ${input:server:local | remote | unknown}
- transport: ${input:transport:stdio | http | unknown}
- install: ${input:install:workspace | user | remote | unknown}
- auth: ${input:auth:none | local | api | org-managed | unknown}

Single source of truth:

- MCP intake normalization, topology decisions, trust model, and verification design are defined in `mcp-integration`.
- Do not restate or redefine those procedures here.

Execution contract:

1. Normalize missing MCP inputs.
2. Decide topology and least-privilege posture.
3. Produce one concrete setup plan with minimal assumptions.
4. Provide copy/paste-ready configuration and safe verification steps.
5. Call out risks and controls explicitly.

Required output sections:

- MCP setup plan summary
- Intake summary and assumptions
- Recommended baseline and configuration
- Verification steps
- Risks, controls, and next step

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **mcp-specialist** | always - MCP setup intake | *(this prompt)* | MCP topology, config, and verification plan produced |
| 2 | **Router** | user is unsure which broader workflow to use next | `/route <follow-up request>` | Correct specialist agent/prompt selected |
| 3 | **PromptSmith** | MCP setup should become a reusable asset | `/new-agent` or `/new-skill` | Follow-up asset scaffolded cleanly |
