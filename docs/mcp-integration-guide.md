# MCP Integration Guide

## Summary

This guide explains how CoDev models Model Context Protocol work for VS Code and GitHub Copilot. Use it when you need to design an MCP topology, install a new server safely, review an existing configuration, or debug MCP failures.

## What CoDev adds

CoDev exposes MCP as a first-class capability:

- capability: `mcp`

- agent: `mcp-specialist`

- prompts: `/mcp-setup`, `/mcp-analyze`, `/mcp-debug`

- skill: `mcp-integration`

The design goal is simple: keep MCP work isolated from generic editor guidance and route requests to one specialist that can create, analyze, and troubleshoot the integration.

## When to use which prompt

| Prompt | Use when | Output |
| --- | --- | --- |
| `/mcp-setup` | You want to install or design a new MCP integration | Guided intake, topology choice, configuration pattern, verification plan |
| `/mcp-analyze` | You already have config or a design and want a review | Findings, minimal changes, residual risk |
| `/mcp-debug` | MCP startup, discovery, auth, or invocation is failing | Ranked hypotheses, checks, likely fix, prevention |

`/mcp-setup` now treats six fields as first-class decisions: goal, host, server model, transport, install target, and auth/trust mode. If one is missing, the prompt asks for a normalized answer instead of inferring a risky default.

It then maps the setup to one of three output branches:

- `local-stdio-vscode`

- `remote-http-copilot`

- `both-hosts-split-surface`

## Topology model

For each MCP request, make these choices explicit:

| Decision | Options | Rule of thumb |
| --- | --- | --- |
| Host | VS Code chat, GitHub Copilot custom agent, or both | Match the actual surface where the user will invoke MCP |
| Server model | Local stdio, remote HTTP, or mixed | Prefer stdio for local single-user workflows; HTTP for shared services |
| Primitive type | Tools, resources, prompts, or mixed | Prefer resources for read-only context; tools for real actions |
| Install target | Workspace config, user profile, or remote environment | Workspace for project-specific setup; user for personal cross-project setup |

## Recommended flow

### Design or install

1. Run `/route set up an MCP server for VS Code and GitHub Copilot`.

2. Follow with `/mcp-setup` and provide the goal, host, server model, transport, install target, and auth mode if known.

3. Apply the smallest safe config.

4. Verify startup, discovery, and one safe request.

Expected intake normalization:

| Field | Allowed answers |
| --- | --- |
| Host | `vscode`, `github-copilot`, `both` |
| Server model | `local`, `remote` |
| Transport | `stdio`, `http`, `no preference` |
| Install target | `workspace`, `user`, `remote` |
| Auth/trust | `none`, `local`, `api`, `org-managed` |
| Primitive bias | `tools`, `resources`, `prompts`, `mixed` |

Snippet specialization rule:

- `install=workspace` -> emit `.vscode/mcp.json`

- `install=user` -> emit user-profile `mcp.json`

- `install=remote` -> explain which remote environment owns the configuration and whether the user still needs a local or agent-level surface

Expected output branching:

| Branch | Use when | Main config surface |
| --- | --- | --- |
| `local-stdio-vscode` | Local process, stdio, VS Code-first workflow | `mcp.json` |
| `remote-http-copilot` | Remote service, HTTP, role-scoped Copilot workflow | Custom-agent frontmatter |
| `both-hosts-split-surface` | The same integration must be explained for both surfaces | `mcp.json` plus custom-agent frontmatter |

For VS Code-first flows, the prompt should now distinguish between workspace and user-profile snippets explicitly instead of returning a generic `mcp.json` placeholder.

### Analyze existing setup

1. Run `/route analyze my MCP configuration`.

2. Use `/mcp-analyze` with the config path, agent file, or short design description.

3. Apply the minimal recommended changes.

### Debug failures

1. Run `/route debug mcp connection failure in copilot chat`.

2. Use `/mcp-debug` with the symptom and relevant config.

3. Work through the ranked checks in order.

## Safety rules

- Never hardcode secrets in MCP config.

- Treat local stdio servers as executable code on the host machine.

- Keep server exposure minimal.

- Use HTTPS for remote servers unless you have an explicit local-development exception.

- On Windows, do not assume local MCP sandboxing exists.

## Verification checklist

After any MCP change, confirm:

1. The server starts cleanly.

2. The expected tools, resources, or prompts are visible.

3. One safe sample request works end-to-end.

4. The configuration does not leak secrets or personal-only assumptions.

## Related assets

- `.github/agents/mcp-specialist.agent.md`

- `.github/prompts/mcp-setup.prompt.md`

- `.github/prompts/mcp-analyze.prompt.md`

- `.github/prompts/mcp-debug.prompt.md`

- `.github/skills/mcp-integration/SKILL.md`

- `.github/instructions/mcp.instructions.md`
