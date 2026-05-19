# Prompt Engineering Examples

## Example 1: Single-skill prompt

```yaml
---
name: summarize-issue
description: "Summarize a GitHub issue or PR."
agent: summarizer
argument-hint: "Paste the issue or PR URL"
---
Goal: Summarize the content of ${input:url}.
Apply the procedure from `.github/skills/summarize-github-issue-pr-notification/SKILL.md`.
Output format:
- Markdown summary with key points.
```

## Example 2: Multi-skill prompt

```text
---
name: triage-error
description: "Diagnose and suggest fixes for errors."
agent: triager
argument-hint: "Paste error log"
---
Goal: Triage the error in ${input:log}.
Apply the procedures from:
- `.github/skills/triage/SKILL.md`
- `.github/skills/logs-alerts/SKILL.md`
Output format:
- Hypotheses table
- Suggested fix steps
```

## Example 3: Tool-enabled prompt

```yaml
---
name: apply-patch
description: "Apply a patch to a file."
agent: patcher
argument-hint: "Paste patch"
---
Goal: Apply the provided patch to the workspace.
Apply the procedure from `.github/skills/patch-application/SKILL.md`.
Output format:
- Success/failure message
- Patch summary
Note: Ensure the agent has the `apply_patch` tool enabled.
```

## Example 4: Argument handling

```text
---
name: generate-report
description: "Generate a report from input data."
agent: reporter
argument-hint: "Paste data"
---
Goal: Generate a report from ${input:data}.
Output format:
- Markdown report with sections: Summary, Details, Recommendations
```

---
**Tips:**

- Always reference skills in the body, not frontmatter.

- Use `argument-hint` for better UX.

- Add comments to explain why each pattern works.
_Last reviewed: 2026-05-19_
