---
name: js-testing
description: JavaScript/TypeScript testing — tooling selection, unit/component/E2E patterns, CI integration, and flakiness prevention.
argument-hint: "[component or module to test]"
user-invocable: true
disable-model-invocation: false
---

# JavaScript/TypeScript Testing (Elite)

## When to use

- Testing React components, hooks, or TypeScript utilities.
- Setting up a JS/TS test suite from scratch.

## Tooling Reference

| Layer | Tool | When to use |
|-------|------|-------------|
| Unit | Vitest | New projects; fast HMR; Vite ecosystem |
| Unit | Jest | Existing project with Jest config |
| Component | React Testing Library (RTL) | User-behavior focused component tests |
| Integration | MSW (Mock Service Worker) | Mock HTTP at network level |
| E2E | Playwright | Cross-browser, full-stack flows |
| E2E | Cypress | Teams already using Cypress |

## Workflow

### 1. Choose tooling

- Prefer Vitest for new projects (fast, ESM native).
- Always pair with RTL for component tests.

### 2. Unit tests

- Pure functions, reducers, selectors, utils.
- Test behavior, not implementation details.

### 3. Component tests

- Render + user interaction via RTL.
- Use `userEvent` (not `fireEvent`) for realistic interactions.
- Assert on what the user sees, not internal state.

### 4. E2E (optional, scoped)

- Critical user flows only (login, checkout, key workflows).
- See `e2e` skill for full guidance.

### 5. CI integration

- Fast unit/component tests on PR (< 5 min).
- Full suite (including E2E) on main or release candidate.

## Self-check

- [ ] Tooling matches project ecosystem (Vitest for Vite; Jest for legacy).
- [ ] RTL used for component tests (not Enzyme or direct DOM assertions).
- [ ] Tests assert on user-visible behavior, not implementation details.
- [ ] No `waitFor` with `setTimeout` hacks; use proper async utilities.
- [ ] CI gate defined: fast on PR, full on main/release.

## 🏆 Elite Section — Top 5% JS/TS Testing Practices

- **Accessibility assertions by default**: Add `jest-axe` (Jest) or `vitest-axe` (Vitest) to every component test suite — run `expect(await axe(container)).toHaveNoViolations()`. Never defer a11y to manual review.
- **MSW for realistic network mocking**: Use [Mock Service Worker](https://mswjs.io/) to intercept HTTP at the network level instead of mocking modules. Tests run against realistic request/response shapes.
- **Visual regression for UI components**: Pair Storybook with Chromatic (or Playwright screenshot tests) to catch unintended visual diffs before merge.
- **`data-testid` as a stable contract**: Use `data-testid` attributes as the primary selector in tests. Class names and DOM structure are implementation details; `data-testid` is a stable interface.
- **Mutation testing for critical logic**: Run [Stryker.js](https://stryker-mutator.io/) quarterly on critical hooks and reducers. A suite that passes with mutated code is not actually verifying behavior.
- **Contract tests for API boundaries**: Use Pact or openapi-typescript-generated schemas to verify frontend-backend contracts. Break the contract → block merge.

## Outputs

- Tooling recommendations.
- Test patterns for components and hooks.
- CI job configuration.
- Flakiness prevention checklist.
