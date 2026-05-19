---
name: "MCP Configuration Safety"
description: "Authoring rules for MCP configuration files: least privilege, trust boundaries, transport choice, and verification."

applyTo: "**/mcp*.json"
---

# MCP Configuration Safety

Sources:

- [VS Code - Add and manage MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)

- [Model Context Protocol - Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)

## Secrets and trust

- Never hardcode API keys, bearer tokens, or other secrets in MCP configuration.

- Treat every local stdio server as executable code on the host machine; review `command` and `args` before enabling it.

- Only use trusted publishers and trusted command lines for local servers.

## Transport and install target

- Prefer `stdio` for single-user local workflows.

- Prefer HTTP only when the server is shared, centrally operated, or requires service-side auth.

- Use workspace config for project-specific MCP servers.

- Use user-profile config for personal cross-project MCP servers.

## Least privilege

- Keep the server list minimal; do not enable unrelated servers by default.

- Prefer resources for read-only context and tools only for real actions.

- Avoid broad or opaque tool surfaces when a narrower server or schema is possible.

## Platform constraints

- Do not rely on sandboxing for local MCP servers on Windows.

- Use HTTPS for remote MCP servers unless there is an explicit local-development reason not to.

## Verification

- After changing MCP config, verify startup, tool/resource discovery, and one safe request.

- If a config is meant to be shared in source control, ensure it is safe for the whole team and does not encode personal-only assumptions.
