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
- Tools empty by default: `tools: []`
- Include: Mission / Non-negotiables / Boundaries / Output format

Output: plan + file content + checklist.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **PromptSmith** | always — agent creation | *(this prompt)* | .github/agents/<id>.agent.md created with mission, boundaries, output format |
| 2 | **Router** | agent needs routing matrix entry | update `routing/matrix.yaml` | New agent reachable via `/route` for intended capability+domain |
| 3 | **Reviewer** | agent ready | `/pr-review` | No boundary violations, `validate-customization-registry.py` passes |
| 4 | **Delivery Lead** | PR ready | `/pr-review` | PR merged, CI green, README updated |
