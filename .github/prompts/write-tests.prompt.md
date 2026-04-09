---
name: write-tests
description: "Write tests based on a test plan; include how to run locally and in CI."
agent: "Architect"
argument-hint: "scope=<file or module> framework=<vitest|jest|xunit|pytest|other>"
---
Apply the procedure from `.github/skills/test-strategy/SKILL.md`.

Act as an Architect and write tests.

Include:

- Test plan summary
- Test code (ready to paste)
- How to run locally
- CI notes
- Flakiness prevention notes
- Regression intent mapping (what failure each test prevents)
- Additive test policy (do not remove existing tests unless explicitly requested)

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Architect** | always — test authoring | *(this prompt)* | Tests written, regression intent mapped, flakiness prevention notes included |
| 2 | **Reviewer** | tests cover critical business logic or security paths | `/pr-review` | Assertions are precise, no test rot, coverage gate will pass |
| 3 | **Delivery Lead** | tests ready to merge | `/pr-review` | PR merged, CI test suite exits 0 |
