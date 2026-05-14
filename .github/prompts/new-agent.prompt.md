---
name: new-agent
description: Create a new custom agent (.agent.md) with stable rules and boundaries.
agent: promptsmith
argument-hint: "agentId=<kebab> mission=<text>"
---

Inputs:

- agentId: ${input:agentId:ex azure-architect}
- mission: ${input:mission:1-2 lines}

Requirements:

- Create `.github/agents/${input:agentId}.agent.md`
- Omit `tools` unless the agent explicitly needs tools
- Include: Mission / Non-negotiables / Boundaries / Output format

Minimal happy path:

1. Run `/new-agent agentId=<kebab> mission=<text>`.
2. Save the generated file at `.github/agents/<id>.agent.md`.
3. If the new agent needs routing, update `routing/matrix.yaml` and related routing files in the same change.
4. Validate locally before PR review:
   - `python scripts/validate-customization-registry.py`
   - `python scripts/validate-readme-registry.py`
   - `python scripts/validate-markdown-lint.py`
   - `python scripts/validate-route-smoke.py` when routing changed

Minimal example:

- `/new-agent agentId=ux-guide mission="Owns contributor onboarding ergonomics for CoDev."`

Output: plan + file content + checklist.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **PromptSmith** | always — agent creation | *(this prompt)* | .github/agents/<id>.agent.md created with mission, boundaries, output format |
| 2 | **Router** | agent needs routing matrix entry | update `routing/matrix.yaml` | New agent reachable via `/route` for intended capability+domain |
| 3 | **Reviewer** | agent ready | `/pr-review` | No boundary violations, `validate-customization-registry.py` passes |
| 4 | **Delivery Lead** | PR ready | `/pr-review` | PR merged, CI green, README updated |
