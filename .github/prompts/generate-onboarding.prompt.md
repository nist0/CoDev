---
name: generate-onboarding
description: "Generate an onboarding guide for a repository."
agent: "Delivery Lead"
argument-hint: "repo=<name> stack=<technologies> audience=<new engineers|contractors|all>"
---

Inputs:

- repo: ${input:repo:repository name or path}
- stack: ${input:stack:main technologies and frameworks}
- audience: ${input:audience:new engineers|contractors|all}

Act as a Delivery Lead and generate an onboarding guide.

Include:

- Setup (local dev)
- Build/test commands
- Architecture overview (modules)
- How to change safely
- PR workflow

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Delivery Lead** | always — onboarding guide creation | *(this prompt)* | Onboarding guide produced covering setup, build, architecture, and PR workflow |
| 2 | **Reviewer** | guide reviewed by a new team member | `/pr-review` | Guide confirmed accurate and complete |
| 3 | **Delivery Lead** | guide ready to publish | `/pr-review` | PR merged, CI green |
