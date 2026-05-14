---
name: agent-authoring
description: Create stable custom agents (.agent.md) with clear mission, boundaries, and repeatable workflow.
argument-hint: "[role] [boundaries]"
user-invocable: true
disable-model-invocation: false
---

# agent-authoring Skill (Elite)

## When to use

- Creating a new agent in `.github/agents/`.
- Updating an existing agent to add procedure, output format, or self-check.
- Upgrading a thin agent definition to elite standard.

## Minimal extension workflow

Use this path when you want the shortest safe route from idea to a validated agent file:

1. Run `/new-agent agentId=<kebab> mission=<text>`.
2. Save the generated file as `.github/agents/<id>.agent.md`.
3. If the agent must be reachable through `/route`, update `routing/matrix.yaml` plus any required capability, alias, or domain entries in the same change.
4. Validate locally before opening a PR:

    - `python scripts/validate-customization-registry.py`
    - `python scripts/validate-readme-registry.py`
    - `python scripts/validate-markdown-lint.py`
    - `python scripts/validate-route-smoke.py` when routing changed

Minimal example:

```text
/new-agent agentId=ux-guide mission="Owns contributor onboarding ergonomics for CoDev."
```

This path is additive: it reuses the existing prompt, routing files, and validators instead of introducing a second template system.

## Procedure

### Domain research (mandatory for new domains/themes)

Before writing any content, gather authoritative references for the domain or theme this agent covers:

1. **Identify the domain**: name it explicitly (e.g. "Kubernetes operations", "ASP.NET Core APIs", "GitHub Actions CI/CD").
2. **Gather ≥2 primary sources**: official documentation, language specs, RFC/standards, canonical style guides. Prioritise primary over aggregated/secondary sources.
3. **Read related CoDev assets**: scan existing agents, skills, and instructions that touch the same domain to avoid contradiction and duplication.
4. **Synthesise best practices**: extract the non-contradictory union. Where sources conflict, document the choice — *"Source A recommends X; Source B recommends Y — using X because `<rationale>`."*
5. **Cite sources**: inline-link primary references in the agent's `## Procedure` or `## Non-negotiables` sections where domain-specific rules are stated.

> Skip only for purely orchestration agents that contain no domain-specific rules.

### 1. Check for existing agents first

1. List `.github/agents/` directory.
2. Read the mission of any overlapping agents.
3. If overlap exists: extend the existing agent; do not create a duplicate.
4. Check `routing/matrix.yaml` — does the role map to an existing agent ID?

### 2. Define the agent contract

**Official attribute reference** — [VS Code custom-agents docs](https://code.visualstudio.com/docs/copilot/customization/custom-agents) (verified 2026-03-04):

| Attribute | Required | Allowed values / notes |
| --- | --- | --- |
| `description` | No | Shown as placeholder text in chat input |
| `name` | No | Display name (defaults to file name) |
| `argument-hint` | No | Hint shown in chat input field |
| `tools` | No | List of tool/tool-set names |
| `agents` | No | List of subagent names; `*` = all; `[]` = none |
| `model` | No | Model name string or array |
| `user-invocable` | No | Boolean; `false` = hidden from picker (default `true`) |
| `disable-model-invocation` | No | Boolean; `true` = cannot be auto-invoked as subagent (default `false`) |
| `target` | No | `vscode` or `github-copilot` |
| `mcp-servers` | No | List of MCP server config |
| `handoffs` | No | List of handoff objects (`label`, `agent`, `prompt`, `send`, `model`) |

**Interaction constraint** — when both `agents` and `tools` are specified in the
frontmatter, the `agent` tool **must** be included in the `tools` list. Without it
VS Code cannot invoke the listed subagents. If only `agents` is set (no `tools`),
the constraint does not apply because the default tool set already includes `agent`.

**Deprecated attributes** — do not use:

| Attribute | Status | Replacement |
| --- | --- | --- |
| `infer` | Deprecated | Use `user-invocable` + `disable-model-invocation` instead |

Write the frontmatter:

```yaml
---
name: <agent-id>                    # kebab-case; used in matrix.yaml
description: "<one sentence: what this agent does, when it is chosen>"
# tools: [...]                      # start minimal; add only what is needed
# agents: [...]                     # if set alongside tools, tools must include 'agent'
# user-invocable: false             # uncomment to hide from the agents dropdown
# disable-model-invocation: true    # uncomment to prevent auto-invocation as subagent
---
```

### 3. Write the mission statement

1–2 sentences max:

- **Role**: what kind of expert is this agent?
- **Scope**: what decisions/tasks is it responsible for?
- **Non-scope**: what should other agents handle?

### 4. Define the procedure (numbered, actionable)

For each step:

- Number it explicitly (`### 1.`, `### 2.`, …).
- Add: exact action, tool or file to use, output of this step.
- Prefer: read → analyze → plan → implement → verify pattern.

All agents must include:

- **Context gathering step** (read before acting).
- **Separation of facts from assumptions**.
- **Verification step** (how to confirm the output is correct).

### 5. Define non-negotiables (constraints)

- Rules the agent must always follow regardless of user request.
- Reference relevant instruction files as mandatory constraints.
- At minimum: security (no secrets), quality gates, instruction compliance.

### 6. Define the output format

Precise output template the agent must produce:

```markdown
## Output format

### Findings
<structure>

### Recommended action
<structure>

### Self-check
- [ ] ...
```

### 7. Add a self-check section

At minimum 5 items checking:

- Context was gathered before acting.
- Instruction files were honored.
- Output format was followed.
- Verification step was performed.
- No secrets or credentials appear in output.

### 8. Register in routing

- Add agent ID to `routing/matrix.yaml` (capability + domain → agent).
- If the agent covers a new capability: update `routing/capabilities.yaml`.
- Add natural language alias triggers to `routing/aliases.yaml`.
- Run smoke test: `python scripts/validate-route-smoke.py`.
- Run registry check: `python scripts/validate-customization-registry.py`.

## Self-check (authoring)

- [ ] Existing agents checked before creating a new one.
- [ ] Frontmatter complete with `name`, `description`, `tools: []`.
- [ ] Mission in 1–2 sentences (role + scope + non-scope).
- [ ] Procedure is numbered with read → analyze → verify pattern.
- [ ] Non-negotiables section includes security and instruction compliance.
- [ ] Output format template provided.
- [ ] Self-check section with ≥ 5 items included.
- [ ] If `agents` and `tools` are both set, `agent` tool is in the `tools` list.
- [ ] Agent registered in `routing/matrix.yaml` and `capabilities.yaml`.
- [ ] `validate-route-smoke.py` passed.

## Outputs

- New or updated `.github/agents/*.agent.md` file.
- Routing update in `routing/matrix.yaml` (and `capabilities.yaml` if needed).
- Registry validation result.

- Add a `handoffs` section to the agent definition, listing all key workflow handoffs (PR Review, Rework Implementation, Release Risk Assessment, Docs Lint/Fix, Release Readiness Check, Project Board Sync, etc.).
- Include an explicit delegation chain table in the agent definition, showing step-by-step agent handoff, trigger, prompt, and done criteria.
- Reference the delegation chain and handoffs as required sections in the agent authoring procedure.
- Validate that all new/updated agents include these sections and that they are up to date with current workflow best practices.
- Add a self-check item for handoffs/delegation chain coverage.
