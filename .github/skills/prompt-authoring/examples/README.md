description: "Given an error message or stack trace, produce ranked hypotheses and minimal repro steps."
# Prompt Authoring Examples
## Example 1: Minimal prompt
```yaml
---
name: hello-world
description: "Say hello to the user."
agent: greeter
---
Goal: Greet the user.
Output format:
- "Hello, user!"
```
## Example 2: Prompt with argument
```text
---
name: greet-user
description: "Greet a user by name."
agent: greeter
argument-hint: "Enter user name"
---
Goal: Greet ${input:name}.
Output format:
- "Hello, ${input:name}!"
```
## Example 3: Prompt referencing a skill
```yaml
---
name: summarize-text
description: "Summarize input text."
agent: summarizer
argument-hint: "Paste text"
---
Goal: Summarize the following text: ${input:text}
Apply the procedure from `.github/skills/summarize/SKILL.md`.
Output format:
- Markdown summary
```
---
**Tips:**
- Always use `argument-hint` for better UX.
- Reference skills in the body for reusable logic.
- Use explicit output formats for determinism.
_Last reviewed: 2026-05-19_
```text
---
description: "Generate and write unit tests for a target file or function. Use after implementing a feature or fixing a bug."
name: write-tests
argument-hint: "target=<file or function> framework=<xUnit|Jest|pytest>"
agent: agent
---
```
**Body excerpt** (delegation chain):
```markdown
## Agent delegation chain
| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **implement** | always — test file creation | *(this prompt)* | Test file written, all tests pass locally |
| 2 | **Reviewer** | tests written | `/pr-review` | Coverage meets threshold, no flaky patterns |
| 3 | **Delivery Lead** | review approved | — | PR merged, CI green |
```
