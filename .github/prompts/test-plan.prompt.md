---
name: test-plan
description: "Create a pragmatic test plan (scenarios → test type → rationale)."
agent: "Architect"

argument-hint: "scope=<file or module> stack=<language/framework>"
---

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Act as an Architect and create a test plan.

Output a table:

- Scenario

- Test type (unit/integration/contract/e2e)

- Why

- Notes (data, mocking, setup)

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Architect** | always — test plan creation | *(this prompt)* | Test plan table produced: scenario, type, rationale, notes |
| 2 | **Architect** | test plan approved | `/write-tests` | Tests authored, passing locally and in CI |
| 3 | **Reviewer** | tests ready for review | `/pr-review` | No flakiness, regression intent mapped, additive policy respected |
| 4 | **Delivery Lead** | tests merged | `/pr-review` | PR merged, coverage gate passes in CI |
