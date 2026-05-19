---
name: test-strategy
description: Test pyramid design — risk mapping, test type selection, data strategy, CI gate definition, and flakiness prevention.
argument-hint: "[service-or-feature] [risk-areas]"
user-invocable: true

disable-model-invocation: false
---

# Test Strategy (Elite)

## When to use

- You need to define a test pyramid for a new feature or service.

- You want to decide which test types apply (unit/integration/contract/e2e).

- You want a CI gate configuration that balances speed and coverage.

## Procedure

### 1. Write the test plan before tests

Define:

- **What** is being tested (feature, component, integration).

- **Why** (what risk does this test guard against).

- **How** (test type, framework, assertion strategy).

### 2. Identify risk areas

| Risk area | Examples | Priority |
|-----------|---------|----------|
| Core business logic | Calculations, rules, workflows | High |
| External integrations | APIs, queues, databases | High |
| Data integrity | Migrations, schema changes | High |
| UI/UX flows | Form submission, navigation | Medium |
| Performance | Latency, throughput | Medium |
| Edge cases | Null, empty, boundary values | Medium |

### 3. Map risk areas to test types

| Test type | Scope | Speed | Confidence | When to use |
|-----------|-------|-------|------------|-------------|
| Unit | Single function/class | Fastest | Logic | Always; core logic |
| Integration | Component + dependency | Fast | Wiring | DB, queue, HTTP client |
| Contract | API boundary | Fast | Interface | Microservices, shared APIs |
| E2E | Full stack | Slow | User journey | Critical paths only |
| Regression | Confirmed bug | Fast | Non-recurrence | Every bug fix |
| Snapshot | UI or serialization | Fast | Drift detection | Stable output formats |

### 4. Define data strategy

| Technique | Use for | Avoid when |
|-----------|---------|------------|
| In-memory builders/fakers | Unit and integration tests | Production-like volume tests |
| Fixtures (seeded DB) | Integration tests | Tests that mutate fixtures |
| Test containers | Real DB/queue locally | Slow pipelines or no Docker |
| Mocks/stubs | External APIs | Core business logic |
| Production snapshots | Performance tests | PII / sensitive data |

### 5. Define CI gates

| Gate | Trigger | Suite | Max duration |
|------|---------|-------|--------------|
| Fast gate | Every PR commit | Unit + contract | 3 min |
| Standard gate | PR ready-for-review | Unit + integration + contract | 10 min |
| Full gate | Merge to main | All tests including e2e | 30 min |
| Nightly | Scheduled | Full + performance | 60 min |

### 6. Flakiness prevention rules

- No `Thread.Sleep` / `time.sleep`: use retry with backoff or deterministic waits.

- No time-dependent logic: freeze/mock clocks.

- No shared mutable state between tests: isolate test data.

- Test containers: always start fresh; never reuse between runs.

- E2E tests: use stable selectors (data-testid, aria, not XPath).

- Flag flaky tests immediately (`[Flaky]` / `skip` + issue opened).

### 7. Regression test rule

For every bug fix:

1. Write a test that **fails** on the current code.

2. Apply the fix.

3. Confirm the test **passes**.

4. Add a comment in the test linking the issue number.

## Self-check

- [ ] Test plan written before tests (what/why/how).

- [ ] Risk areas identified and prioritized.

- [ ] Test type chosen for each risk area with rationale.

- [ ] Data strategy documented per test type.

- [ ] CI gates defined with triggers and time budgets.

- [ ] Flakiness prevention rules applied.

- [ ] Regression test intent included for every bug fix.

## Outputs

- Test plan table (scenario → type → rationale).

- Test pyramid diagram (text).

- Data strategy summary per test type.

- CI gate configuration table.

- Flakiness prevention checklist.
