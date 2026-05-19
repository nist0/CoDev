---
name: e2e
description: End-to-End testing — critical flow selection, stable environments, flakiness prevention, and CI gating strategy.
argument-hint: "[application or user flow]"
user-invocable: true

disable-model-invocation: false
---

# End-to-End (E2E) Testing (Elite)

## When to use

- You need confidence that user-critical flows work across the whole stack.

- You're validating deployments and regressions.

## Test Type Allocation

| Scope | Tool | Gate |
|-------|------|------|
| Critical user flows | Playwright / Cypress | PR merge gate |
| Multi-browser regression | Playwright | Nightly / pre-release |
| API contract smoke | Playwright / Bruno | PR + deployment |
| Load and perf | k6 / Artillery | Pre-release only |

## Workflow

### 1. Select critical flows

- Login, checkout, core workflows; keep E2E scope small.

- Avoid testing every UI edge case (unit/integration tests do that).

### 2. Test environment

- Stable test data, isolated environment, deterministic setup.

- Use seeded DB or API mocks; avoid shared state between tests.

### 3. Tool choice

- Playwright preferred (cross-browser, API testing, trace viewer).

- Cypress for teams already using it.

### 4. Flakiness prevention

- Avoid sleeps (`await page.waitForTimeout()`); wait for specific conditions.

- Use `waitForSelector`, `waitForResponse`, role-based locators.

- Run flaky tests in retry mode; quarantine and fix within 1 sprint.

### 5. CI execution

- Split fast/slow suites; keep PR checks under 10 minutes.

- Run full suite nightly or on release candidate.

## Self-check

- [ ] Only user-critical flows in E2E scope; edge cases in unit/integration tests.

- [ ] Test environment is isolated with deterministic data.

- [ ] No `waitForTimeout` sleeps; condition-based waits used throughout.

- [ ] Flaky tests quarantined and tracked.

- [ ] CI suite split: fast (PR) vs full (nightly/release).

## 🏆 Elite Section — Top 5% E2E Testing Practices

- **Playwright trace viewer on failure**: Always configure `trace: 'on-first-retry'` in CI. Traces enable instant post-mortem debugging without needing to reproduce the failure locally.

- **Authenticated state via `storageState`**: Capture authentication tokens once with `browser.storageState()` and reuse across tests. Re-authenticating in every test multiplies suite time and flakiness.

- **Page Object Model (POM)**: Encapsulate all selectors and interaction logic in Page Objects. Never repeat a selector in multiple test files — one change breaks one place.

- **Test tagging for CI granularity**: Tag tests with `@smoke`, `@regression`, `@nightly`. Run only `@smoke` on PR (< 3 min); full `@regression` suite on main; `@nightly` on a schedule. Use `--grep` or Playwright `tags` to filter.

- **API seeding, never UI setup**: Seed test data via direct API calls or DB scripts before tests. Never click through setup screens — UI-driven setup is the #1 cause of E2E flakiness.

- **Parallel sharding in CI**: Use Playwright's built-in sharding (`--shard=1/4`) to distribute tests across CI workers. Target < 5 min wall-clock time for the `@smoke` suite on PRs.

## Outputs

- E2E scope + suite design.

- Flakiness prevention checklist.

- CI gating strategy.
