---
name: new-skill
description: Create a new reusable skill folder (SKILL.md + minimal assets) following repo conventions.
agent: promptsmith
argument-hint: "skillId=<kebab> theme=<text> scope=<when-to-use>"
---

Goal: create a NEW skill skeleton.

Inputs:

- skillId: ${input:skillId:ex dotnet-ef-core}
- theme: ${input:theme:ex Backend .NET}
- scope: ${input:scope:when to use this skill}

Requirements:

- Create folder: `.github/skills/${input:skillId}/`
- `SKILL.md` frontmatter `name` MUST equal `${input:skillId}`.
- Provide: When to use / Procedure / Self-check
- Create `examples/README.md`

Output:

1) Plan
2) File tree
3) Full contents of each file
4) Self-review checklist

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **PromptSmith** | always — skill creation | *(this prompt)* | SKILL.md + examples/README.md created with procedure and self-check |
| 2 | **Router** | skill referenced from matrix | update `routing/matrix.yaml` | Skill reachable via routing, smoke test passes |
| 3 | **Reviewer** | skill ready for review | `/pr-review` | No duplication, examples are concrete and runnable |
| 4 | **Delivery Lead** | PR ready | `/pr-review` | PR merged, `validate-customization-registry.py` and `validate-readme-registry.py` pass |
