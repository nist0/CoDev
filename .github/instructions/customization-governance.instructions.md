---
name: "Customization Governance"
description: "Mandatory governance for agents/prompts/skills/instructions and routing consistency."

## applyTo: ".github/**/*.{md,yml,yaml}"

# Customization Governance

## Reference-gathering gate (mandatory)

When creating a new skill, agent, instruction, or theme pack on a domain or theme, the author **must** complete a domain research phase before writing any content:

1. **Identify the domain**: name it explicitly (e.g. "Kubernetes RBAC", "React hooks", "ASP.NET Core minimal APIs").

2. **Gather ≥2 primary sources**: official docs, language specs, RFC/standards, canonical style guides. Prioritise primary over secondary/aggregated sources.

3. **Read related CoDev assets**: scan all existing skills, agents, and instructions that touch the same domain to avoid contradictions and duplication.

4. **Synthesise non-contradictory best practices**: where sources conflict, explicitly document the choice — *"Source A recommends X; Source B recommends Y — using X because `<rationale>`."*

5. **Cite sources in the asset**: add a `## Sources` section at the bottom of `SKILL.md`; for agents and instructions, inline-link the primary reference in the relevant rule.

This rule is enforced by the `## Domain research` step in each authoring skill (`prompt-authoring`, `agent-authoring`, `instruction-authoring`).

> **Exception**: purely procedural/thin assets (e.g. orchestration prompts with no domain-specific rules) are exempt.

## Asset authoring rules

- Treat instruction files as mandatory constraints; do not bypass or weaken them.

- Before creating new assets, inventory existing agents/prompts/skills/instructions to avoid duplication.

- Prefer extending existing assets unless a clear gap exists.

- Default new agents to no `tools:` declaration unless tools are explicitly required; add only what is needed.

## Frontmatter attribute allowlists (MANDATORY — enforced by CI)

> **Source**: VS Code Copilot official docs (last verified 2026-03-04)
>
> - Prompt files: <https://code.visualstudio.com/docs/copilot/customization/prompt-files>
> - Agent files: <https://code.visualstudio.com/docs/copilot/customization/custom-agents>
> - Skill files: <https://code.visualstudio.com/docs/copilot/customization/agent-skills>
> - Instruction files: <https://code.visualstudio.com/docs/copilot/customization/custom-instructions>

**Every frontmatter attribute used in any framework file MUST appear on the allowlist below.
Unknown or deprecated attributes are treated as blocking violations (same severity as a failing CI gate).**

### `.prompt.md` — allowed frontmatter

| Attribute | Notes |
| --- | --- |
| `description` | Short description shown in `/` menu |
| `name` | Display name (defaults to file name) |
| `argument-hint` | Hint text shown in chat input |
| `agent` | `ask`, `agent`, `plan`, or a custom agent name |
| `model` | Model name string or array |
| `tools` | List of tool/tool-set names — omit entirely to inherit agent tools |

Forbidden in `.prompt.md`:

- `mode` — **DEPRECATED** → use `agent: ask` or `agent: agent`

- `skills` — not a valid attribute → reference skills in the prompt body

- `tools: []` — zeroes out all tools; omit the key entirely to inherit

### `.agent.md` — allowed frontmatter

| Attribute | Notes |
| --- | --- |
| `description` | Shown as placeholder text in chat input |
| `name` | Display name (defaults to file name) |
| `argument-hint` | Hint text shown in chat input |
| `tools` | List of tool/tool-set names |
| `agents` | Subagent allowlist; `*` = all, `[]` = none |
| `model` | Model name string or array |
| `user-invocable` | Boolean; `false` = hidden from agents dropdown (default `true`) |
| `disable-model-invocation` | Boolean; `true` = cannot be auto-invoked as subagent (default `false`) |
| `target` | `vscode` or `github-copilot` |
| `mcp-servers` | List of MCP server config (for `target: github-copilot`) |
| `handoffs` | List of handoff objects |

Forbidden in `.agent.md`:

- `infer` — **DEPRECATED** → use `user-invocable` and `disable-model-invocation`

### `SKILL.md` — allowed frontmatter

| Attribute | Required | Notes |
| --- | --- | --- |
| `name` | **Yes** | Lowercase, hyphens, max 64 chars; must match directory name |
| `description` | **Yes** | What the skill does and when to use it; max 1024 chars |
| `argument-hint` | No | Hint text for slash command invocation |
| `user-invocable` | No | Boolean; `false` = hidden from `/` menu (default `true`) |
| `disable-model-invocation` | No | Boolean; `true` = requires manual slash invocation (default `false`) |

Forbidden in `SKILL.md`:

- `user-invokable` — **DEPRECATED** → use `user-invocable`

### `.instructions.md` — allowed frontmatter

| Attribute | Notes |
| --- | --- |
| `name` | Display name shown in UI (defaults to file name) |
| `description` | Short description shown on hover |
| `applyTo` | Glob pattern for auto-apply; omit for manual-only |

No other attributes are valid for `.instructions.md` files.

## Routing consistency

- For new themes/capabilities, update routing end-to-end:

  - `routing/capabilities.yaml`

  - `routing/aliases.yaml`

  - `routing/matrix.yaml`

  - `routing/domains.yaml` when needed

- In routing/configuration files, agent references must match `.github/agents/*.agent.md` frontmatter `name` exactly (no capability-style aliases).

- Include routing smoke-test phrases and expected outcomes in every implementation summary.

## Validation scope (mandatory)

- When validating CoDev, inspect tracked and non-ignored repository files only.

- Never analyze `external/`.

- Never analyze any path excluded by `.gitignore` or Git's standard excludes.

- Prefer repository validators that already enforce this scope over ad hoc recursive globbing:

  - `python scripts/validate-markdown-lint.py`

  - `python scripts/validate-readme-registry.py`

  - `python scripts/validate-route-smoke.py`

  - `python scripts/validate-customization-registry.py`

- Broad workspace scans such as `**/*.md`, `**/*`, or recursive `rglob(...)` checks are non-compliant unless they are explicitly constrained to tracked and non-ignored files.

## Layering & information integrity

- Keep instruction layering additive and non-contradictory.

- Preserve examples, procedures, and existing information unless explicitly asked to remove.

- `applyTo` globs must be tight and non-overlapping; document the intent when globs are broad.

## Documentation updates (mandatory)

- Always maintain documentation for customization changes:

  - update `.github/copilot-instructions.md` when capabilities/domains/prompts/skills behavior changes

  - update `README.md` sections that enumerate capabilities/domains/prompts/skills when coverage changes

  - update `docs/` files when a procedure or developer workflow changes:

    - `docs/codev-dev-guide.md` — CLI walkthroughs, validator results, alias discovery examples

    - `docs/developer-tooling.md` — script reference, error-class tables

    - `docs/submodule-guide.md` — consumer getting-started steps

    - `docs/submodule-cli-contract.md` — CLI flag/exit-code contract

  - document verification steps (local + CI) for the new/updated behavior

## Naming conventions

- Agent IDs: `engineering.*` / `research.*` / kebab-case files.

- For new feature issues/PRs, use `enh: <title>` (not `Enhancement: <title>`).

- Skill directories: kebab-case theme name; always include `examples/README.md`.

## Pre-merge checklist

Before finalizing any customization change:

- [ ] **Issue body well-formed** — written via `--body-file`, no raw backslashes, all tables have separator rows, code blocks properly fenced (see `00-core.instructions.md` § *GitHub issue / PR body formatting*).

- [ ] **Issue created** for every task and sub-task (issues-first rule from `00-core.instructions.md`)

- [ ] **Branch used** — work is on a feature branch, not pushed directly to `main`

- [ ] **PR opened** — a PR is open and references the closing issue(s) (`Closes #N`)

- [ ] **All GitHub checks pass** — every CI status check is green before merge; failing checks block merge

- [ ] **Project board updated** — issue added to project board #2 (`gh project item-add`) and status moved to **Done** before or at close

- [ ] Scope and acceptance criteria defined

- [ ] Existing agent/skill/prompt reuse considered

- [ ] Routing updated in all needed YAMLs

- [ ] New/updated examples preserved or added (no info loss)

- [ ] Route smoke tests performed with representative phrases

- [ ] Validation commands inspect tracked and non-ignored repository files only (never `external/` or gitignored paths)

- [ ] Security + reliability + testing expectations verified

- [ ] `copilot-instructions.md` and `README.md` updated

## Example: smoke-test phrase entry

```yaml
# route-smoke-tests.yaml
- phrase: "write a postmortem for yesterday's outage"
  expected_capability: engineering.postmortem
  expected_domain: engineering.observability
  expected_agent: engineering.reliability
```

---

## 🏆 Elite Section — Top 5% Customization Practices

- **Instruction coverage map**: Maintain a table in `README.md` mapping every `applyTo` glob to its instruction file and the last review date. Stale instructions (>90 days without review) must be audited.

- **Automated registry validation in CI**: The `validate-customization-registry.py` and `validate-route-smoke.py` scripts must run on every PR that touches `.github/`. Failures block merge.

- **Versioned agent contracts**: When an agent's output contract changes (new required fields, changed format), bump a `version:` field in the agent frontmatter and update all callers.

- **Capability deprecation protocol**: Before removing a capability, add it to a `deprecated:` list in `capabilities.yaml` with a sunset date and migration path. Never delete without a redirect.

- **Single-session instruction hygiene**: At the end of every session that surfaces a recurring gap or a new rule, immediately update the most specific matching instruction file. Never defer codification to a follow-up task.

- **Cross-file consistency lint**: Write a script that asserts all `agent:` values in prompts exist as `.github/agents/*.agent.md` files and all capability IDs in `matrix.yaml` exist in `capabilities.yaml`. Run it in CI.
