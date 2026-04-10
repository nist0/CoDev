---
name: prompt-from-theme
description: Generate a high-quality prompt file for a given theme, using stable structure and inputs/outputs.
agent: promptsmith
argument-hint: "theme=<text> intent=<what the prompt should do>"
---

Inputs:

- theme: ${input:theme:ex Azure AKS}
- intent: ${input:intent:ex generate a troubleshooting checklist}

Requirements:

- Create a `.github/prompts/<kebab>.prompt.md`
- Include: Goal / Inputs / Requirements / Output format / Acceptance criteria

Output: plan + file content + checklist.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **PromptSmith** | always — prompt creation | *(this prompt)* | .github/prompts/<kebab>.prompt.md created with inputs, requirements, output format, and AC |
| 2 | **Router** | prompt needs routing registration | update `routing/matrix.yaml` + smoke test | `/route <theme phrase>` returns the new prompt |
| 3 | **Reviewer** | prompt ready for review | `/pr-review` | No duplication with existing prompts, `validate-customization-registry.py` passes |
| 4 | **Delivery Lead** | PR ready | `/pr-review` | PR merged, README updated |
