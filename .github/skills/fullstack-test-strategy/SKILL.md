---
name: fullstack-test-strategy
description: Full-stack test pyramid — risk mapping, unit/integration/contract/E2E allocation, data strategy, CI gating, and flakiness control.
argument-hint: "[system-name] [risk-areas]"
user-invocable: true
disable-model-invocation: false
---

# Full-stack Test Strategy (Elite)

## When to use

- You need a test pyramid for a full-stack system (frontend + backend + infra).
- You want to align unit/integration/contract/E2E tests with actual risk areas.
- You need CI gate definitions for a multi-layer application.

## Procedure

### 1. Write the test plan before tests

Define for each risk area:

- **What**: what behavior is being tested.
- **Why**: what failure mode does this test prevent.
- **How**: test type, framework, assertion strategy.

### 2. Identify critical behaviors and risks

| Risk area | Layer | Priority |
|-----------|-------|----------|
| Core business logic | Backend / domain | P1 |
| API contracts (request/response shape) | Backend ↔ Frontend | P1 |
| Authentication/authorization | Backend + infra | P1 |
| Data mutations and persistence | Backend + DB | P1 |
| Key user flows (checkout, login, etc.) | Frontend + backend | P2 |
| UI rendering and accessibility | Frontend | P2 |
| Performance baselines | All | P2 |

### 3. Allocate test types per layer

| Layer | Unit | Integration | Contract | E2E |
|-------|------|------------|---------|-----|
| Domain / business logic | ✅ Primary | ✔ Limited | — | — |
| Application services | ✅ | ✅ | — | — |
| API endpoints | ✔ | ✅ | ✅ | — |
| Frontend components | ✅ | ✔ | └ API mocks | ✅ Critical paths only |
| Infra / DB / queue | ✔ | ✅ TestContainers | — | — |

### 4. Contract tests (API boundary)

- Use **Pact** or **Schemathesis** / **Spectral** for API contract tests.
- Consumer defines the contract; provider verifies.
- Contract tests run on every PR that touches the API.
- Break the contract → block merge.

### 5. E2E test discipline

- **Only critical user paths** (login, checkout, key workflows).
- Use `data-testid` selectors; never XPath or position-based.
- Seed test data via API or DB directly; never rely on prior test state.
- E2E tests run on merge to main and on staging; never block a PR alone.

### 6. Data strategy

| Test type | Data strategy |
|-----------|---------------|
| Unit | In-memory builders / fakers |
| Integration | TestContainers (fresh per test run) |
| Contract | Minimal JSON fixtures |
| E2E | API seeding via test helper endpoint |

Never use production data. Never share mutable state between tests.

### 7. CI gate configuration

| Gate | Trigger | Suite | Max duration |
|------|---------|-------|--------------|
| Fast gate | Every PR commit | Unit + contract | 3 min |
| Standard gate | PR ready-for-review | Unit + integration + contract | 10 min |
| Full gate | Merge to main | All + E2E | 30 min |
| Nightly | Scheduled | Full + performance | 60 min |

### 8. Measure and improve

- Track: test runtime, flakiness rate, coverage by module.
- Alert if E2E suite exceeds 30 min or flakiness rate > 2%.
- Delete or fix any flaky test within 1 sprint (no quarantine purgatory).

## Self-check

- [ ] Test plan written before tests (what/why/how).
- [ ] All P1 risk areas covered with at least one test type.
- [ ] Contract tests in place for all API boundaries shared between frontend and backend.
- [ ] E2E tests limited to critical paths; using stable selectors.
- [ ] Data strategy defined per test type; no shared mutable state.
- [ ] CI gates defined with triggers and time budgets.
- [ ] Flakiness measurement in place.

## Outputs

- Test pyramid recommendation per layer.
- Test plan table (scenario → type → why).
- Data strategy summary.
- CI gate configuration table.
- Flakiness prevention checklist.
