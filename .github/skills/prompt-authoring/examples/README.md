# prompt-authoring Examples

Each subfolder contains a concrete example produced using this skill.

---

## Example 1 — `triage-error.prompt.md` (analysis prompt, `ask` mode)

**Goal**: Given an error message, produce a ranked hypothesis list and minimal repro steps.

**Why this is a good example**:

- Uses `ask` mode (analysis only, no file edits).
- Single required input (`${input:error:paste the error message or stack trace}`).
- Output format is fully specified (ranked table + repro template).
- Self-check is present.
- No delegation chain (Q&A-style, produces no artifact that requires follow-on).

**Frontmatter**:

```yaml
---
description: "Given an error message or stack trace, produce ranked hypotheses and minimal repro steps."
name: triage-error
argument-hint: "error=<paste error>"
agent: ask
---
```

**Body excerpt**:

```markdown
## Task
You are a reliability engineer. Given the error below, produce:
1. A ranked list of 3–5 hypotheses (most likely first).
2. For each hypothesis: one-line rationale + minimal repro command.
3. A recommended first investigation step.

Error: ${input:error:paste the error message or stack trace}

## Output format
### Hypotheses (ranked)
| Rank | Hypothesis | Rationale | Repro command |
| --- | --- | --- | --- |

### Recommended first step
<one sentence>

## Self-check
- [ ] At least 3 hypotheses listed.
- [ ] Each hypothesis has a concrete repro command.
- [ ] Recommended first step is actionable (not vague).
```

---

## Example 2 — `write-tests.prompt.md` (execution prompt, `agent` mode)

**Goal**: Generate unit tests for a given function or module, write them to disk.

**Why this is a good example**:

- Uses `agent` mode (writes files).
- Two required inputs (`${input:target}`, `${input:framework}`).
- Includes an agent delegation chain (Reviewer + Delivery Lead follow-on).
- Self-check is present.

**Frontmatter**:

```yaml
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
