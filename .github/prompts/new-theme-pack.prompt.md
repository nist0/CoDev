---
name: new-theme-pack
description: "Generate a theme pack: 1 agent + 2 skills + 3 prompts + 1 scoped instruction, all consistent and reusable."
agent: promptsmith

## argument-hint: "theme=<text> primaryStack=<dotnet|ts|python|...> scope=<where it applies>"

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Inputs:

- theme: ${input:theme:ex Azure AKS}

- primaryStack: ${input:primaryStack:ex dotnet}

- scope: ${input:scope:ex **/*.cs}

Requirements:

- Before writing skill/agent content, gather ≥2 authoritative primary references for the theme domain and synthesise a non-contradictory union of best practices (reference-gathering gate — see `customization-governance.instructions.md`).

- Create:

  - 1 agent in `.github/agents/`

  - 2 skills in `.github/skills/`

  - 3 prompts in `.github/prompts/`

  - 1 instruction in `.github/instructions/` with applyTo=${input:scope}

- Integrate routing for the new theme:

  - add capability in `routing/capabilities.yaml`

  - add aliases in `routing/aliases.yaml`

  - add matrix rules in `routing/matrix.yaml`

  - add/update `routing/domains.yaml` when needed

- Keep everything concise and non-duplicated.

Output: plan + tree + contents + checklist.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **PromptSmith** | always — theme pack creation | *(this prompt)* | Agent + skills + prompts + instruction all created, routing YAMLs updated |
| 2 | **Router** | routing integration verification | `/route <theme-relevant phrase>` | Smoke test confirms correct capability+domain+agent returned |
| 3 | **Reviewer** | theme pack ready | `/pr-review` | No duplication, all 4 routing YAMLs consistent, `validate-route-smoke.py` passes |
| 4 | **Delivery Lead** | PR ready | `/pr-review` | PR merged, CI green, README updated |
