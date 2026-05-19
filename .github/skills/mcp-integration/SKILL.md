---
name: mcp-integration
description: MCP integration for VS Code and GitHub Copilot - design, install, secure use, and troubleshoot client/server workflows.
argument-hint: "[local|remote] [stdio|http] [goal]"
user-invocable: true

disable-model-invocation: false
---

# mcp-integration Skill (Elite)

## When to use

- You need to design an MCP topology before wiring it into VS Code or GitHub Copilot.

- You need to choose between local and remote servers, or between stdio and HTTP transport.

- You need to install and verify MCP servers in VS Code chat.

- You need to expose MCP capabilities safely to GitHub Copilot custom agents.

- You need a repeatable troubleshooting flow for discovery, trust, auth, or tool-call failures.

Use the existing `vscode` skill for generic workspace bootstrap and reload flows.
Use `agent-authoring` when the main task is designing a custom agent contract.
Use `prompt-engineering` when the main task is writing task prompts rather than MCP integration.

## Theme-pack composition

This skill is the durable knowledge layer for the MCP theme pack.

Expected companion assets:

- `mcp-specialist` agent for routed MCP work

- `/mcp-setup` for creation and installation

- `/mcp-analyze` for design and config review

- `/mcp-debug` for troubleshooting

- `mcp.instructions.md` for MCP configuration safety rules

## Scope boundaries

This skill covers MCP-specific concerns only:

- host/client/server roles

- tools, resources, prompts, and when to expose each

- transport choice and trust boundary

- VS Code `mcp.json` installation and verification

- GitHub Copilot custom-agent integration boundaries

- least-privilege and validation guidance

This skill does not replace:

- generic VS Code customization guidance

- generic agent or prompt authoring guidance

- repo-wide security or governance instructions

## Architecture reference

### Participant model

| Participant | Responsibility | Practical implication |
| --- | --- | --- |
| MCP host | AI application coordinating MCP usage | In this workflow, VS Code is the MCP host |
| MCP client | Connection manager for one server | Each configured server gets its own client/session |
| MCP server | Program exposing capabilities | Can run locally or remotely |

Rule: model the host, client, and server separately before choosing tools or writing config.

### Primitive selection

| Primitive | Use when | Avoid when | Trigger model |
| --- | --- | --- | --- |
| Tools | The model must take an action or call an external system | The need is read-only context | Model-controlled |
| Resources | The application needs read-only context from files, APIs, or schemas | You need side effects | Application-controlled |
| Prompts | You want a user-invoked template or guided workflow | You expect the model to call it automatically | User-controlled |

Rule: default to resources for read-only context, then add tools only for actions that justify the risk.

### Transport selection

| Choice | Best for | Strengths | Risks |
| --- | --- | --- | --- |
| `stdio` | Local tools on the same machine | Simple startup, low latency, no network dependency | Runs arbitrary local code; machine trust is critical |
| Streamable HTTP | Shared remote services | Centralized hosting, multi-client access, standard auth | Network/auth complexity and higher blast radius |

Rule: prefer `stdio` for single-user local workflows. Prefer HTTP only when the server must be shared, centrally operated, or protected behind service-side auth.

### Install target selection

| Target | When to choose it | Trade-off |
| --- | --- | --- |
| User profile `mcp.json` | Personal tools reused across many workspaces | Fast reuse, less team visibility |
| Workspace `.vscode/mcp.json` | Shared project workflow | Reviewable in git, but affects all contributors |
| Remote user/workspace config | Server must run in a remote environment | Better environment locality, more setup complexity |

Rule: if the server depends on workspace files or project-local tooling, put it in workspace config. If it is personal or cross-project, use user config.

## Procedure

### 1. Frame the topology before installing anything

Capture these inputs first:

- host: VS Code chat, GitHub Copilot custom agent, or both

- server location: local process or remote service

- transport: `stdio` or HTTP

- trust boundary: personal machine, repo workspace, org-managed service

- primitive mix: tools only, resources only, prompts only, or combination

- write risk: read-only, low-risk write, or privileged action

Minimum design output:

```text
Host: VS Code chat
Server type: Local stdio
Primary primitives: resources + 1 safe tool
Trust boundary: local developer workstation
Install target: workspace .vscode/mcp.json
Verification: tools list visible in chat; one sample call succeeds
```

Do not start with config syntax. Start with topology and trust.

### 2. Design the server surface with least privilege

Apply these rules:

- expose the smallest useful tool set

- split read-only context into resources when possible

- keep tool inputs narrow and schema-driven

- prefer one clear operation per tool

- require human approval or explicit confirmation for write-capable tools

- name tools with stable, specific identifiers

Good pattern:

```text
resources/read -> schema, docs, release notes
tools/call -> create_release_draft, not release_everything
prompts/get -> /release.checklist for user-invoked flow
```

Bad pattern:

```text
tool: do_anything
arguments: { "payload": "string" }
```

### 3. Choose install target and server source

For VS Code, choose one of these supported paths:

- `.vscode/mcp.json` for workspace-shared server config

- user-profile `mcp.json` opened through `MCP: Open User Configuration`

- remote user config when working over VS Code remote environments

Server source options:

- install from the MCP gallery in Extensions view with `@mcp`

- add manually with `MCP: Add Server`

- manage config directly in `mcp.json`

Trust rules:

- review publisher and launch command before first start

- do not hardcode secrets in `mcp.json`

- use trusted sources only for local stdio servers

- remember that sandboxing for local stdio servers is not available on Windows

### 4. Configure VS Code MCP servers

Workspace example:

```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp"
    },
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@microsoft/mcp-server-playwright"]
    }
  }
}
```

Validation checklist after editing `mcp.json`:

1. Start or restart the server from `MCP: List Servers`.

2. Approve the trust prompt only after reviewing the config.

3. Confirm the server shows installed/running status.

4. Open chat and inspect the tool list.

5. Run one safe request that exercises a single tool.

If config changes frequently, consider enabling automatic restart with `chat.mcp.autoStart` after the setup is stable.

### 5. Integrate MCP into GitHub Copilot custom agents

Use a custom agent when MCP access should be bundled with a role, tool scope, or handoff workflow.

Practical rule set:

- use VS Code `mcp.json` when the goal is general chat availability

- use agent-level MCP config when the goal is role-scoped Copilot behavior

- keep MCP servers out of generic agents unless they are needed for that role

- do not make privileged MCP tools globally available by default

Example frontmatter pattern for a GitHub Copilot custom agent:

```yaml
---
name: release-ops
description: Investigate release state with approved MCP servers only.
target: github-copilot
mcp-servers:
  - name: github
    type: http
    url: <https://api.githubcopilot.com/mcp>
  - name: docs
    type: stdio
    command: node
    args:
      - dist/server.js
---
```

Boundary rule: if the agent mostly needs repo instructions and normal tools, do not force MCP into the design. Add MCP only when it materially improves the workflow.

### 6. Use MCP capabilities in chat deliberately

In VS Code chat, MCP servers can surface:

- tools for model-invoked actions

- resources through `Add Context > MCP Resources`

- prompts via `/<server>.<prompt>`

- interactive apps when the server supports MCP Apps

Usage flow:

1. Start with a request that clearly names the action or context needed.

2. Confirm the correct tool or resource is available.

3. Allow only the minimum necessary tool calls.

4. Review outputs before chaining multiple actions.

Examples:

```text
Use the Playwright MCP tools to open code.visualstudio.com and take a screenshot.
```

```text
Add the release-notes resource from the docs server, then summarize changes since last week.
```

```text
/docs.publish-checklist target=docs/site
```

### 7. Verify end-to-end behavior

Run verification in this order:

1. Config validity - `mcp.json` loads without startup errors

2. Trust and launch - the server starts successfully

3. Discovery - tools/resources/prompts are visible

4. Safe invocation - one read-only or low-risk call succeeds

5. Role scoping - custom agents expose only the intended MCP servers

6. Repeatability - restart VS Code or the server and confirm the setup survives reload

Definition of done for an MCP integration:

- topology documented

- install target justified

- server trust reviewed

- one safe example request works

- privileged operations remain opt-in

- troubleshooting path documented

## Troubleshooting matrix

| Symptom | Likely cause | Check first | Fix |
| --- | --- | --- | --- |
| Server does not start | Bad command or missing runtime | `MCP: List Servers` and output log | Validate `command` and `args`, install missing runtime |
| Tools not visible in chat | Discovery failed or server not running | MCP server status and output log | Restart the server and confirm trust approval |
| Resource browser is empty | Server exposes no resources or wrong expectation | Server capability design | Add resources support or use tools instead |
| Prompt is missing | Server exposes no prompts or wrong invocation syntax | `prompts/list` support and chat syntax | Use `/<server>.<prompt>` after verifying prompts exist |
| HTTP server connects but calls fail | Auth/header mismatch or service-side rejection | Remote server logs and client output | Fix auth and retry with one minimal request |
| Repeated approval prompts | High-risk unsandboxed tools | Tool design and trust posture | Reduce write scope or keep approvals explicit |
| Windows local sandbox expected | Unsupported platform assumption | Host OS | Remove sandbox expectation; use trust review and least privilege instead |

VS Code debug path:

- Chat error indicator -> `Show Output`

- `MCP: List Servers` -> select server -> `Show Output`

- inspect whether failure is startup, discovery, or invocation

## Security and design rules

- never hardcode tokens, API keys, or secrets in MCP config

- treat local stdio servers as executable code with machine-level trust implications

- prefer read-only resources over write-capable tools where possible

- keep tool schemas narrow and typed

- isolate high-risk actions behind explicit approvals

- review publisher, install source, and command line before first launch

- share workspace `mcp.json` only when the server is appropriate for the whole team

## Self-check

- [ ] Host, client, and server roles are explicitly identified.

- [ ] Primitive choice is intentional: tools vs resources vs prompts.

- [ ] Transport choice is justified with trust and operational trade-offs.

- [ ] Install target is correct: user, workspace, or remote config.

- [ ] No secrets are hardcoded in MCP configuration examples or real config.

- [ ] At least one safe end-to-end validation step is defined.

- [ ] Custom-agent integration is role-scoped rather than globally exposed.

- [ ] The workflow does not duplicate generic `vscode`, `agent-authoring`, or `prompt-engineering` guidance.

## Outputs

- MCP topology decision: host, client, server, transport, and install target.

- Least-privilege primitive choice: tools, resources, prompts, or mixed.

- Copy/paste-ready VS Code or GitHub Copilot MCP configuration patterns.

- Verification and troubleshooting checklist for startup, discovery, and invocation.

## Sources

- [Model Context Protocol - Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)

- [Model Context Protocol - Understanding MCP servers](https://modelcontextprotocol.io/docs/learn/server-concepts)

- [Visual Studio Code - Add and manage MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)

- [Visual Studio Code - Custom agents in VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-agents)

Conflict resolution used for this skill:

- MCP protocol semantics come from the MCP architecture and server-concepts documentation.

- VS Code installation, trust, and management behavior comes from the VS Code MCP server documentation.

- GitHub Copilot custom-agent integration guidance uses the VS Code custom-agent documentation for `target: github-copilot` and `mcp-servers` behavior.
