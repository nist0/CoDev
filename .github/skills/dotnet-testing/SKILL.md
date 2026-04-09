---
name: dotnet-testing
description: .NET unit and integration testing — xUnit, WebApplicationFactory, testcontainers, FluentAssertions, and CI gating.
argument-hint: "[service] [test-type]"
user-invocable: true
disable-model-invocation: false
---

# .NET Testing (Unit + Integration) (Elite)

## When to use

- You need tests for ASP.NET Core APIs, EF Core, or application services.
- You want deterministic tests and good coverage for critical paths.

## Workflow

1) Choose test types
   - unit tests for pure logic; integration for API + DB behavior.
2) Integration testing approach
   - `WebApplicationFactory` for API integration.
   - Prefer real Postgres via testcontainers when DB behavior matters.
3) Test data strategy
   - builders/fixtures; isolate tests; avoid shared mutable state.
4) Assertions
   - verify behavior and contracts (status codes, response bodies).
5) CI integration
   - fast PR suite + full suite on main.

## Self-check

- [ ] Test pyramid explicit: unit (logic) → integration (API/DB) → minimal E2E smoke.
- [ ] Bug fixes include a regression test that fails before and passes after.
- [ ] No time-sensitive assertions; clock abstractions used where needed.
- [ ] Shared mutable state eliminated; tests are isolated.
- [ ] testcontainers used for DB-specific behavior.

## Test coverage matrix

- Application service behavior → unit tests.
- HTTP contract/status/error mapping → API integration tests.
- EF provider-specific behavior → Postgres testcontainers tests.
- Serialization/auth/versioning compatibility → integration contract tests.

## Outputs

- Test plan table (scenario → test type).
- Recommended tooling (xUnit/NUnit, FluentAssertions, testcontainers).
- Flakiness prevention checklist.

## Microsoft references

- [Integration tests in ASP.NET Core](https://learn.microsoft.com/aspnet/core/test/integration-tests)
- [Unit testing in .NET](https://learn.microsoft.com/dotnet/core/testing/)
- [Testcontainers for .NET](https://dotnet.testcontainers.org/)
