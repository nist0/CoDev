---
name: "CoDev Consumer — Override Authoring"
description: "Rules for authoring assets in codev-overrides/: naming, non-duplication, safety, and validation."

applyTo: "codev-overrides/**"
---

# CoDev Consumer — Override Authoring Rules

## Purpose

Files in `codev-overrides/` extend or replace CoDev-managed assets for this specific host
repository. These rules ensure overrides are safe, non-duplicating, and maintainable.

## Structure contract

```text
codev-overrides/
├── copilot-instructions.override.md   # Extends/overrides copilot-instructions.md
├── agents/                            # Host-specific agents (.agent.md)
├── skills/<theme>/                    # Host-specific skills (SKILL.md + examples/)
├── prompts/                           # Host-specific prompts (.prompt.md)
├── instructions/                      # Host-specific instructions (.instructions.md)
└── README.md                          # REQUIRED: documents every override and its rationale
```

## Mandatory rules

- **Never edit** files outside `codev-overrides/` to customize CoDev behavior. The pre-commit hook enforces this.

- **Always maintain** `codev-overrides/README.md` documenting every override file: purpose, owner, and last-reviewed date.

- **No secrets** in any override file — use environment variables or secrets managers.

- **Additive only**: overrides may add new behavior but must not silently remove or weaken CoDev's core guidance.

## Naming conventions

| Asset type | Convention | Example |
| --- | --- | --- |
| Agent | kebab-case, domain-specific | `order-management.agent.md` |
| Skill directory | kebab-case theme | `order-domain/` |
| Prompt | kebab-case action | `generate-order-report.prompt.md` |
| Instruction | kebab-case scope | `order-api.instructions.md` |

## Quality gates for override files

### Agents

- Include frontmatter: `name`, `description`; omit `tools` unless the agent explicitly needs tools.

- Define: mission, responsibilities, output format, handoff behavior.

- Do not duplicate responsibilities already covered by an existing CoDev agent.

### Skills

- Follow the standard SKILL.md structure: frontmatter + when-to-use + procedure + self-check + elite section.

- Always include `examples/README.md` with at least one concrete example.

- State explicitly which CoDev skills this extends (if any).

### Prompts

- `agent:` must reference an existing agent `name` (CoDev or host-specific).

- Include `argument-hint` for any user inputs.

- Produce a concrete, actionable output — not vague guidance.

### Instructions

- `applyTo` must be scoped tightly to avoid overriding CoDev-wide instructions unintentionally.

- Keep layering additive: do not contradict CoDev's core or security instructions.

## Validation

After adding or modifying any override asset, run:

```bash
python tools/codev/scripts/validate-customization-registry.py
python tools/codev/scripts/validate-route-smoke.py
```

Both must pass before committing.

Example: `codev-overrides/README.md` template
---

```markdown
# CoDev Overrides — This Repository

## Active overrides

| File | Purpose | Owner | Last reviewed |
| --- | --- | --- | --- |
| `copilot-instructions.override.md` | Project conventions appended to CoDev base | @me | 2026-03-05 |
| `agents/order-management.agent.md` | Order domain expert | @me | 2026-03-05 |

## Override strategy

Strategy: `extend` — CoDev base is preserved; override content is appended.

## Proposing upstream changes

If any override fixes a bug or adds generally useful functionality, consider upstreaming it
to CoDev. See `codev-contributing` skill or run `/codev-contribute`.
```
