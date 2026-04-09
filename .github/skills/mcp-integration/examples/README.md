# mcp-integration - Examples

## Example 1 - Intake-aligned local stdio setup for VS Code

Normalized intake:

- Host: `vscode`
- Server model: `local`
- Transport: `stdio`
- Install target: `workspace`
- Auth/trust: `local`
- Primitive bias: `tools`

Use workspace config when the server is part of the project workflow and should be reviewed in git.

File: `.vscode/mcp.json`

```json
{
  "servers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@microsoft/mcp-server-playwright"]
    }
  }
}
```

Validation:

1. Run `MCP: List Servers`.
2. Start `playwright` and approve trust after reviewing the command.
3. Open chat and ask:

```text
Go to code.visualstudio.com, decline the cookie banner, and give me a screenshot of the homepage.
```

Expected outcome:

- Playwright tools appear in chat.
- VS Code requests approval for tool invocations as needed.
- A screenshot result is returned.

Expected setup branch:

- `local-stdio-vscode`

## Example 2 - Intake-aligned local stdio setup in user profile

Normalized intake:

- Host: `vscode`
- Server model: `local`
- Transport: `stdio`
- Install target: `user`
- Auth/trust: `local`
- Primitive bias: `resources`

Use user-profile config when the server is personal, reused across many repositories, and not meant to be committed with a project.

File: user-profile `mcp.json`

```json
{
  "servers": {
    "docs-cache": {
      "type": "stdio",
      "command": "node",
      "args": ["C:/tools/mcp/docs-cache-server.js"]
    }
  }
}
```

Validation:

1. Run `MCP: Open User Configuration` and confirm the server is defined there rather than in `.vscode/mcp.json`.
2. Start `docs-cache` from `MCP: List Servers`.
3. Open two different workspaces and confirm the same MCP server is available in both.

```text
Add the docs-cache resource and summarize the latest local documentation index.
```

Expected outcome:

- The MCP server is reusable across workspaces in the same VS Code profile.
- No project-local config is required.
- The answer distinguishes user-profile setup from workspace setup.

Expected setup branch:

- `local-stdio-vscode`

## Example 3 - Intake-aligned remote HTTP setup for GitHub Copilot

Normalized intake:

- Host: `github-copilot`
- Server model: `remote`
- Transport: `http`
- Install target: `remote`
- Auth/trust: `org-managed`
- Primitive bias: `resources`

Use agent-level config when the remote MCP server should be scoped to a Copilot role rather than exposed globally in VS Code.

File: `.github/agents/github-docs.agent.md`

```yaml
---
name: github-docs
description: Review internal GitHub documentation resources through an approved remote MCP service.
target: github-copilot
mcp-servers:
  - name: docs
    type: http
    url: https://docs.example.com/mcp
---

# GitHub Docs

Use the remote docs MCP server for read-only documentation lookup and summarization.
```

Validation:

1. Open the `github-docs` custom agent in Copilot.
2. Confirm the remote `docs` MCP server is available only in that role.
3. Run one safe request that reads documentation context.

```text
Summarize the deployment prerequisites from the docs resource for our release workflow.
```

Expected outcome:

- The server is reached over HTTP.
- The MCP surface stays scoped to the `github-docs` agent.
- No editor-global MCP exposure is required.

Expected setup branch:

- `remote-http-copilot`

## Example 4 - Intake-aligned both-hosts setup with split surfaces

Normalized intake:

- Host: `both`
- Server model: `remote`
- Transport: `http`
- Install target: `workspace`
- Auth/trust: `api`
- Primitive bias: `mixed`

Use split surfaces when both VS Code chat and a GitHub Copilot custom agent need the same remote MCP service, but not with identical trust and UX expectations.

Files:

- `.vscode/mcp.json`
- `.github/agents/release-ops.agent.md`

Workspace config:

```json
{
  "servers": {
    "release-docs": {
      "type": "http",
      "url": "https://release.example.com/mcp"
    }
  }
}
```

Agent config:

```yaml
---
name: release-ops
description: Investigate release state with approved MCP servers only.
target: github-copilot
mcp-servers:
  - name: release-docs
    type: http
    url: https://release.example.com/mcp
---

# Release Ops

Use the release MCP server for release diagnostics, documentation lookup, and controlled release tooling.
```

Validation:

1. In VS Code chat, confirm `release-docs` appears via workspace MCP config.
2. In the `release-ops` custom agent, confirm the same remote server is scoped to that role.
3. Run one safe request in each surface and compare behavior.

```text
Add the release-docs resource and summarize the current release checklist.
```

Expected outcome:

- VS Code chat has project-scoped MCP access through `mcp.json`.
- GitHub Copilot has role-scoped MCP access through agent frontmatter.
- The answer explains what is shared and what remains host-specific.

Expected setup branch:

- `both-hosts-split-surface`

## Example 5 - Resource-first design for read-only context

Use a resource instead of a tool when the model only needs context.

Better design:

```text
Resource: docs://release-notes/current
Prompt: /docs.publish-checklist
Optional tool: create_release_draft
```

Worse design:

```text
Tool: manage_release
Arguments: { "mode": "anything", "payload": "string" }
```

Why the first design is better:

- read-only context stays read-only
- write capability is isolated to one explicit action
- prompts remain user-invoked rather than silently triggered

## Example 6 - Troubleshooting flow for a missing tool list

Symptom:

```text
The server shows as installed, but no tools appear in chat.
```

Checklist:

1. Open `MCP: List Servers` and confirm the server is running.
2. Select the server and choose `Show Output`.
3. Check whether the server actually exposes `tools/list`.
4. Restart the server after any config change.
5. Retry with a single safe prompt that clearly requires one MCP tool.

Expected root-cause buckets:

- startup failure
- capability mismatch
- trust not granted
- wrong install target
- auth failure on a remote server
