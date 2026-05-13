---
name: quickstart
description: "Interactive onboarding: gather role + domain + goal in one turn, then emit a personalized first-command card."
agent: "Router"
argument-hint: "role=<your role> domain=<tech stack> goal=<what you want to do>"
---
Apply the procedure from `.github/skills/canonical-routing/SKILL.md`.

Act as a friendly Router and onboard the user to the CoDev framework in ≤2 turns.

## Step 1 — Gather context

If `{{input}}` is empty, ask all three questions **in a single message** (never split them across turns):

1. **Role** — e.g. developer, DevOps engineer, tech lead, PM, open-source contributor
2. **Primary domain** — e.g. .NET backend, React/TypeScript frontend, Kubernetes/cloud, Python scripts, documentation
3. **First goal** — e.g. fix a bug, write tests, review a PR, brainstorm an idea, plan a release, start a new project

If `{{input}}` is provided, extract role / domain / goal directly from it and skip the questions.

## Step 2 — Match to the routing matrix

Map the gathered context to exactly one `capability` + optional `domain` using the canonical routing matrix:

| Goal signal | Capability |
|---|---|
| fix bug / crash / error | `debugging` |
| write / run tests, quality gate | `testing-quality` |
| explain / analyse code | `code-analysis` |
| PR review, commit, issue | `github-delivery` |
| release, tag, changelog | `release` |
| brainstorm, ideas, innovation | `brainstorming` |
| automate, script | `automation` |
| plan / orchestrate project | `project-orchestration` |
| generate / lint docs | `docs` (content/READMEs) or `docs-system` (standards/linting/architecture) |
| tech watch, digest | `tech-watch` |
| incident / postmortem | `postmortem` |
| unsure / general | `routing` |

## Step 3 — Emit a personalised quickstart card

Output exactly this structure, filled in (≤15 lines total):

```text
## Your CoDev quickstart

Role     : <role>
Domain   : <domain>
Goal     : <goal>

Recommended capability : <capability>
Recommended agent      : <agent>

First command:
  /<best first command for this goal>

  — or jump directly to:
  /<best-matching-prompt> <relevant args>

Useful prompts for your profile:
  - /<prompt1> — <one-line description>
  - /<prompt2> — <one-line description>
  - /<prompt3> — <one-line description>

Tip: `/route <anything>` always works as the universal entry point.
```

For the supported first-run scenarios in issue #39, prefer a direct first command instead of `/route`:

| Capability | Preferred first command |
| --- | --- |
| `debugging` | `/triage-error` |
| `testing-quality` | `/test-plan` |
| `github-delivery` | `/pr-review` |
| `release` | `/release-plan` |
| `brainstorming` | `/brainstorm` |
| `onboarding` or ambiguous intent | `/route <natural-language goal>` |
| any other capability not listed here | `/route <natural-language goal>` |

## Rules

- Ask all 3 questions in **one** message — no multi-step interrogation.
- Only reference capabilities from `routing/capabilities.yaml` and prompts from `.github/prompts/`.
- Recommend exactly one first command.
- Keep optional prompts to three items maximum.
- Optimise this prompt for the first-run scenarios covered by issue #39: fix a bug, write tests, and review a PR.
- If the goal is ambiguous, default to `routing` + `/route`.
- Keep the card concise; no marketing language.
- If the user provides partial context (e.g. only domain), infer what you can and flag the assumption.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Router** | always — onboarding | *(this prompt)* | Role, domain, and goal gathered; quickstart card produced |
| 2 | **Recommended specialist agent** | card produced | `/route <goal>` or `/<best-matching-prompt>` | User lands on the right agent and prompt for their first task |
