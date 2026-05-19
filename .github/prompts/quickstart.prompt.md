---
name: quickstart
description: "Interactive onboarding: gather role + domain + goal in one turn, then emit a personalized contributor-profile quickstart card."
agent: "Router"

argument-hint: "role=<your role> domain=<tech stack> goal=<what you want to do>"
---

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

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

## Step 3 — Select the contributor profile

Pick exactly one contributor profile before you emit the card.

| Profile | Use when | Designated agent | Prompt sequence | Validation | Rollback |
|---|---|---|---|---|---|
| `maintenance` | repo upkeep, validators, governance, and low-risk cleanup | `Delivery Lead` | `/quickstart` -> `/pr-review` -> `/route <maintenance task>` | touched validators, plus route smoke when routing changes | fall back to `/route <task>` if the work stops being maintenance |
| `fast-feature` | additive feature work with a clear target and low coordination overhead | `Architect` | `/quickstart` -> `/route <feature request>` -> `/<best-matching prompt>` | targeted tests plus touched validators | switch to `safe-refactor` if the change must preserve behaviour first |
| `safe-refactor` | behaviour-preserving cleanup, restructuring, or risk-controlled change | `Architect` | `/quickstart` -> `/test-plan` -> `/route <refactor request>` | regression coverage plus touched validators | narrow to `maintenance` if the change becomes hygiene-only |
| `doc-only` | README, docs, prompt copy, and instruction wording changes that should stay documentation-scoped | `Delivery Lead` | `/quickstart` -> `/doc-lint-fix` -> `/route <docs task>` | markdown lint plus README registry when inventories change | fall back to `/route <task>` if docs work uncovers code or routing edits |

Profile selection rules:

- If the input explicitly names one of the four profiles, keep it unless the goal clearly conflicts with it.

- Prefer `doc-only` for README, docs, prompt wording, and instruction wording work.

- Prefer `safe-refactor` for refactors, cleanup, migrations, or any request that emphasises safety or behaviour preservation.

- Prefer `maintenance` for upkeep, validation, hygiene, release readiness, registry fixes, and governance tasks.

- Prefer `fast-feature` for additive work that introduces a new prompt, skill, route, automation, or repo capability.

- If signals conflict, choose the safer profile and mention the assumption.

## Step 4 — Emit a personalised quickstart card

Output exactly this structure, filled in (≤20 lines total):

```text
## Your CoDev quickstart

Role     : <role>
Domain   : <domain>
Goal     : <goal>
Profile  : <profile>

Recommended capability : <capability>
Recommended agent      : <agent>
Profile sequence       : /<prompt> -> /<prompt> -> /<prompt>
Validation             : <short validation guidance>
Rollback               : <one-line fallback>

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

- Always choose exactly one profile from `maintenance`, `fast-feature`, `safe-refactor`, or `doc-only`.

- Recommend exactly one first command.

- Keep optional prompts to three items maximum.

- Optimise this prompt for the first-run scenarios covered by issue #39: fix a bug, write tests, and review a PR.

- When the user explicitly asks for a contributor profile, keep the request on `onboarding` and tailor the card instead of routing directly to a specialist.

- If the goal is ambiguous, default to `routing` + `/route`.

- Keep the card concise; no marketing language.

- If the user provides partial context (e.g. only domain), infer what you can and flag the assumption.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Router** | always — onboarding | *(this prompt)* | Role, domain, and goal gathered; quickstart card produced |
| 2 | **Recommended specialist agent** | card produced | `/route <goal>` or `/<best-matching-prompt>` | User lands on the right agent and prompt for their first task |
