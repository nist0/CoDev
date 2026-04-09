---
name: pr-review
description: "Elite PR review: 8-pass analysis, instruction compliance, merge gate, downgrade-risk."
agent: "Delivery Lead"
argument-hint: "pr=<number or URL> focus=<security|perf|all>"
---

Act as a Delivery Lead and apply the full 8-pass elite PR review procedure from `.github/skills/pr-review/SKILL.md`.

## Pre-review setup

1. Load and follow `.github/skills/pr-review/SKILL.md` (all 8 passes).
2. Search the codebase before making any correctness claim.
3. Map changed file types to applicable instruction files (see Pass 3 of the skill).

## Required output sections (produce all; do not skip)

- **Summary of changes** — one paragraph in own words.
- **Correctness risks** — with file and line references; severity per finding.
- **Security concerns** — secrets scan result; permission changes; dependency CVE flags.
- **Performance concerns** — unbounded loops, missing caching, CI job duration.
- **Test coverage gaps** — missing unit tests, missing regression tests for bug fixes.
- **Documentation gaps** — missing release notes, README, routing entries.
- **Instruction compliance table** — per file type vs. applicable instruction file (✅/❌).
- **Framework downgrade-risk** — duplication, removal, contradiction findings.
- **Suggested improvements** — prioritized by severity (`blocker` first, then `major`, then `minor`).
- **Merge gate decision** — `ready` or `blocked` with explicit blocking checklist.
- **Merge action** — `do not merge` or `merge now (strategy: squash|merge|rebase)`.

## Verification commands to include

For `.github/` changes, always include these in the output:

```bash
python scripts/validate-route-smoke.py
python scripts/validate-customization-registry.py
python scripts/validate-readme-registry.py
```

## Constraints

- No finding without a concrete file reference or diff evidence.
- No secrets or credentials in any output.
- Keep output in English.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Delivery Lead** | always — PR review initiation | *(this prompt)* | 8-pass review complete, merge gate decision produced |
| 2 | **Reviewer** | formal verdict needed | *(inline verdict)* | (Agent: Reviewer) approved or rework required with exact gap |
| 3 | **Implementer** | verdict is rework required | Back to domain prompt (e.g. `/dotnet-excellence`) | All blocking findings resolved |
| 4 | **Delivery Lead** | all checks green, verdict approved | *(merge)* | PR merged, branch deleted |
