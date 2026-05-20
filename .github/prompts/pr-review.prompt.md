---
name: pr-review
description: "Elite PR review: 8-pass analysis, instruction compliance, merge gate, downgrade-risk."
agent: "Delivery Lead"

argument-hint: "pr=<number or URL> focus=<security|perf|all>"
---

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Act as a Delivery Lead and apply the full 8-pass elite PR review procedure from `.github/skills/pr-review/SKILL.md`.

## Pre-review setup

1. Load and follow `.github/skills/pr-review/SKILL.md` (all 8 passes).

2. Search the codebase before making any correctness claim.

3. Map changed file types to applicable instruction files (see Pass 3 of the skill).

4. If any CI check is failing or requires action (`action_required`), inspect workflow runs and job logs before finalizing the merge gate.

## Required output format (produce all; do not skip)

Use the output format template in `.github/skills/pr-review/SKILL.md` without changing its required headings or verdict tokens. Ensure the final review includes:

- `## PR Review`

- `**Verdict**: approved | rework required`

- `### Findings` table with severity, file, finding, and required fix

- `### Instruction compliance` table

- `### Framework downgrade-risk`

- `### Merge gate`

- `### Merge action`

## Verification commands to include

For `.github/` changes, always include these in the output:

```bash
python scripts/validate-route-smoke.py
python scripts/validate-customization-registry.py
python scripts/validate-readme-registry.py
```

Treat these commands as CoDev-scoped validators: they must operate on tracked and non-ignored repository files only, and review findings must ignore `external/` plus any gitignored path.

## Constraints

- No finding without a concrete file reference or diff evidence.

- No secrets or credentials in any output.

- Keep output in English.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Delivery Lead** | always -- PR review initiation | *(this prompt)* | 8-pass review complete, merge gate decision produced |
| 2 | **Reviewer** | formal verdict needed | *(inline verdict)* | (Agent: Reviewer) approved or rework required with exact gap |
| 3 | **Implementer** | verdict is rework required | Back to domain prompt (e.g. `/dotnet-excellence`) | All blocking findings resolved |
| 4 | **Delivery Lead** | all checks green, verdict approved | *(merge)* | PR merged, branch deleted |
