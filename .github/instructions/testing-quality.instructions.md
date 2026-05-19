---
name: "Testing & Quality Gates"
description: "Test plans, regression tests for bug fixes, and lint/quality gate practices."

## applyTo: "**"

# Testing & Quality Gates

## Test planning

- Write a test plan before writing tests: what is tested, why it matters, and how to verify.

- Follow the test pyramid: many unit tests, fewer integration tests, minimal E2E tests.

- For bug fixes, add a regression test that **fails before** the fix and **passes after**.

- Prefer stable tests: avoid flakiness from time-dependent logic, unordered maps, or shared state.

## Quality gates

- Enforce linting and test runs in CI on every PR; fail fast on issues.

- Require minimum code coverage for new code paths (e.g. 80% line coverage for business logic).

- Include static analysis (e.g. CodeQL, ESLint, `dotnet analyze`) as a CI gate.

- Mention how to run tests locally and in CI in every PR description.

## Test plan template

```text
## Test plan — <feature or fix name>

**What**: [describe the behavior under test]
**Why**: [risk or user impact if this breaks]
**How**:
  - Unit: [what units, with what edge cases]
  - Integration: [which components interact, what boundary is exercised]
  - E2E / manual: [scenario, expected result]
**Not tested**: [explicit exclusions and rationale]
**CI gate**: `<exact command>` exits 0
```

## Example: regression test pattern

```python
# Before fix: this raised ValueError incorrectly
def test_parse_empty_string_returns_none_not_error():
    result = parse_value("")  # used to raise ValueError
    assert result is None    # after fix: returns None gracefully
```

## Coverage expectations by layer

| Layer | Coverage target | Primary tool |
|---|---|---|
| Pure functions / domain logic | ≥90% | unit tests |
| Service / use-case layer | ≥80% | unit + integration |
| HTTP controllers / endpoints | key paths | integration / contract |
| Infrastructure adapters | happy + failure paths | integration |
| E2E flows | top 3–5 critical journeys | E2E suite |

---

## 🏆 Elite Section — Top 5% Quality Practices

- **Mutation testing**: Run mutation testing (e.g. Stryker.NET, `mutmut`) quarterly. A test suite that passes with mutated code is not actually verifying behavior.

- **Contract testing for APIs**: Use consumer-driven contracts (e.g. Pact) for service boundaries instead of integration tests that require live services.

- **Property-based testing**: For pure business logic with many input combinations, use property-based testing (e.g. `Hypothesis` for Python, `FsCheck` for .NET) to discover edge cases automatically.

- **Test data factories**: Use factory functions or builder patterns (not magic strings) to create test data; this prevents "copy-paste test rot".

- **Flakiness budget**: Track flaky test count as a metric. Any test that flakes 3+ times in a month must be fixed or deleted within one sprint.

- **Coverage is a floor, not a ceiling**: 80% coverage with weak assertions is worse than 60% coverage with precise assertions. Always review the quality of assertions, not just the count.
