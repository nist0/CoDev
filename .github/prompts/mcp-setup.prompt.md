---
name: mcp-setup
description: "Design and install an MCP integration for VS Code or GitHub Copilot with a guided intake, strict topology decisions, and least-privilege verification steps."
agent: mcp-specialist
argument-hint: "goal=<what you want to connect> [host=<vscode|github-copilot|both>] [server=<local|remote>] [transport=<stdio|http>] [install=<workspace|user|remote>] [auth=<none|local|api|org-managed>]"
---

Apply the procedure from `.github/skills/mcp-integration/SKILL.md`.

Goal: turn an MCP integration request into a concrete, safe setup plan for VS Code and/or GitHub Copilot.

Inputs:

- goal: ${input:goal:what tool, service, or workflow should MCP expose}
- host: ${input:host:vscode | github-copilot | both}
- server: ${input:server:local | remote | unknown}
- transport: ${input:transport:stdio | http | unknown}
- install: ${input:install:workspace | user | remote | unknown}
- auth: ${input:auth:none | local | api | org-managed | unknown}

## Step 1 - Normalize the MCP intake

Treat these six decisions as required before producing a setup plan:

1. Goal - what capability the MCP server should expose
2. Host - VS Code chat, GitHub Copilot custom agent, or both
3. Server model - local process or remote service
4. Transport - stdio or HTTP
5. Install target - workspace config, user profile, or remote environment
6. Auth/trust mode - none, local machine trust, API auth, or org-managed service

If any required field is unknown, do not guess silently.

Ask for the missing facts in one message only, using this normalized questionnaire:

```markdown
## Missing MCP setup facts

Reply with one line per item:

- Host: vscode | github-copilot | both
- Server model: local | remote
- Transport: stdio | http | no preference
- Install target: workspace | user | remote
- Auth/trust: none | local | api | org-managed
- Primitive bias: tools | resources | prompts | mixed
```

If the input already contains enough detail, do not ask questions.

## Step 2 - Apply the decision rules

Decide and state explicitly:

- participant model: host, client, server
- primitive choice: tools vs resources vs prompts
- transport choice: stdio vs HTTP
- install target: workspace, user profile, or remote config
- trust posture: what must be reviewed before enabling it

Use these rules:

- prefer resources for read-only context
- prefer tools only for real actions
- prefer stdio for single-user local workflows
- prefer HTTP for shared or centrally operated services
- never hardcode secrets in configuration examples
- keep tool exposure least-privilege and role-scoped where possible

Apply these stricter compatibility checks:

- if `server=local`, prefer `transport=stdio` unless the user explicitly needs a local HTTP bridge
- if `server=remote`, prefer `transport=http`
- if `host=vscode` only, prefer `mcp.json` over agent frontmatter
- if `host=github-copilot` only, prefer custom-agent frontmatter over global editor config
- if `host=both`, explain what is shared and what is host-specific
- if `install=workspace`, call out team-safety and review implications
- if `install=user`, prefer user-profile `mcp.json` and call out cross-workspace reuse plus lower team visibility
- if `install=remote`, explain which remote environment owns the config and why local config is insufficient
- if `auth=api` or `auth=org-managed`, call out where secrets or trust are expected without embedding them

If the user leaves a decision unspecified and you must proceed, record it under assumptions and keep the baseline minimal.

## Step 3 - Emit the setup plan

First, classify the request into exactly one setup branch:

- `local-stdio-vscode` - local server, stdio transport, VS Code as the primary host
- `remote-http-copilot` - remote server, HTTP transport, GitHub Copilot custom agent as the primary host
- `both-hosts-split-surface` - both VS Code and GitHub Copilot are in scope and the answer must explain what is shared vs host-specific

If the request does not fit cleanly, choose the closest branch and state the mismatch under assumptions.

Output exactly this structure:

```markdown
## MCP setup plan

**Goal**: <goal>
**Host**: <vscode | github-copilot | both>
**Server model**: <local stdio | remote http | mixed>
**Recommended primitives**: <tools/resources/prompts with rationale>
**Install target**: <workspace/user/remote>

### Intake summary
- Known facts: <normalized decisions>
- Assumptions: <only if still needed>
- Unsafe assumptions avoided: <what you refused to guess>

### Recommended baseline
- Config surface: <mcp.json | custom-agent frontmatter | both>
- Trust/auth posture: <summary>
- Setup branch: <local-stdio-vscode | remote-http-copilot | both-hosts-split-surface>
- Install variant: <workspace | user | remote>

### Topology-specific baseline
<one branch template selected from below>

### Configuration
<copy/paste-ready config snippet specialized for the chosen install variant>

### Verification
1. <exact step>
2. <exact step>
3. <exact safe sample request>

### Risks and controls
- Risk: <risk>
  Control: <mitigation>

### Escalation / next step
- <when to use `vscode`, `agent-authoring`, or other related assets>
```

Use exactly one of these topology-specific baseline templates:

```markdown
Branch: local-stdio-vscode
- Why this branch fits: <reason>
- Preferred config surface: workspace or user `mcp.json`
- Shared assumptions: local runtime exists, machine trust is acceptable
- Avoided alternative: custom-agent frontmatter is unnecessary unless role scoping is required
- Install variant rule: if `install=workspace`, emit `.vscode/mcp.json`; if `install=user`, emit user-profile `mcp.json`
```

```markdown
Branch: remote-http-copilot
- Why this branch fits: <reason>
- Preferred config surface: GitHub Copilot custom-agent frontmatter
- Shared assumptions: remote service exists, HTTPS/auth are handled outside the snippet
- Avoided alternative: global VS Code config would overexpose the integration
- Install variant rule: if `install=remote`, explain which managed environment owns the remote service contract; do not fall back to user-profile config unless the user explicitly asks for editor-wide exposure
```

```markdown
Branch: both-hosts-split-surface
- Why this branch fits: <reason>
- Shared surface: <what can be common across hosts>
- VS Code-specific surface: <what belongs in `mcp.json`>
- GitHub Copilot-specific surface: <what belongs in agent frontmatter>
- Avoided alternative: one merged config that hides host-specific trust differences
- Install variant rule: explain separately whether the VS Code side belongs in workspace or user config
```

## Rules

- Keep the answer MCP-specific; do not restate generic VS Code or agent-authoring guidance.
- Prefer one minimal working setup over multiple speculative variants.
- Do not emit configuration until the topology and install target are either explicit or captured as assumptions.
- Do not mix multiple topology branches in the same baseline section unless the branch is `both-hosts-split-surface`.
- Do not emit a generic `mcp.json` label without stating whether it is workspace or user-profile configuration.
- If the request implies write-capable or privileged tools, call out approval and trust implications explicitly.
- If the user asks for GitHub Copilot custom-agent integration, include an agent-frontmatter example with `target: github-copilot` and `mcp-servers`.
- If the user asks only for VS Code chat setup, prefer `mcp.json` examples.
- Always include one safe verification request.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **mcp-specialist** | always - MCP setup intake | *(this prompt)* | MCP topology, config, and verification plan produced |
| 2 | **Router** | user is unsure which broader workflow to use next | `/route <follow-up request>` | Correct specialist agent/prompt selected |
| 3 | **PromptSmith** | MCP setup should become a reusable asset | `/new-agent` or `/new-skill` | Follow-up asset scaffolded cleanly |
