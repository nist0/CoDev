---
name: linters-stack
description: "Design or improve polyglot linter strategy and CI quality gates across C/C++/C#/Python/Bash/Markdown."
agent: "Automation/Scripting"
argument-hint: "stack=<list> scope=<paths> ci=<github-actions|other>"
---

Inputs:

- stack: ${input:stack:C/C++, C#, Python, Bash, Markdown}
- scope: ${input:scope:repo paths or modules}
- ci: ${input:ci:github-actions|other}

Requirements:

- Propose linters and formatters per language with rationale.
- Provide local commands and CI job sequencing (fast fail first).
- Include baseline/adoption strategy for legacy repos.
- Include false-positive management and suppression policy.

Output:

- linter matrix (language → tools → command)
- adoption plan (phase 1/2/3)
- CI quality-gate plan
- verification and rollback checklist

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Automation/Scripting** | always — linter strategy | *(this prompt)* | Linter matrix, CI quality-gate plan, and adoption plan produced |
| 2 | **Automation/Scripting** | CI job authoring needed | `/automation-script` | Linter jobs added to CI workflow |
| 3 | **Reviewer** | linter config ready | `/pr-review` | No false positives in baseline, suppression policy reviewed |
| 4 | **Delivery Lead** | changes ready | `/pr-review` | PR merged, all CI gates green |
