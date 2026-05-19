---
name: rest-api-runtime-quality
description: Improve runtime quality for ASP.NET Core APIs through validation/error consistency, EF Core/PostgreSQL safety, security baselines, observability, and testing.

## user-invocable: true

# REST API Runtime Quality

## When to use

- Auditing an existing API before release.

- Improving reliability, security, and observability for API changes.

- Defining pragmatic quality gates for EF Core/PostgreSQL-backed APIs.

## Required inputs

- Target API scope (endpoints/resources).

- Current error handling and validation behavior.

- Current testing and deployment context.

## Optional inputs

- Production incident history.

- Existing dashboards/alerts.

- Performance constraints and SLOs.

## Procedure

1. Baseline current behavior.

   - Capture known failure modes and current status-code mapping.

   - Identify missing validation, error, or test coverage.

2. Standardize runtime contracts.

   - Centralize exception handling and `ProblemDetails` mapping.

   - Ensure validation errors are structured and client-safe.

3. Review persistence correctness.

   - Verify EF Core configuration boundaries and migration safety.

   - Check PostgreSQL indexing, constraints, and concurrency handling.

4. Apply security baseline.

   - Confirm authentication/authorization assumptions.

   - Review CORS, sensitive logging, and least-privilege data access.

5. Apply observability baseline.

   - Ensure structured logs, trace/correlation IDs, and health endpoints.

   - Define minimal alerts for errors, latency, and dependency failures.

6. Define test and verification gates.

   - Map required unit/integration/contract tests.

   - Provide exact commands and acceptance criteria.

## Self-check

- [ ] Global error handling produces consistent `ProblemDetails`.

- [ ] Validation paths are structured and client-friendly.

- [ ] EF Core/PostgreSQL behavior is reviewed with real relational semantics.

- [ ] Security assumptions and controls are explicit.

- [ ] Logs/traces/health checks are actionable.

- [ ] Quality gates include deterministic verification commands.

## Outputs

- Runtime risk summary.

- Prioritized remediation checklist.

- Test and observability acceptance checklist.

- Release readiness verdict with residual risks.

## Common mistakes to avoid

- Returning framework exception text directly to clients.

- Treating in-memory persistence tests as equivalent to PostgreSQL behavior.

- Missing correlation IDs across logs and error responses.

- Relying on permissive production CORS defaults.

## Sources

- ASP.NET Core error handling and problem details: <https://learn.microsoft.com/aspnet/core/fundamentals/error-handling>.

- ASP.NET Core health checks: <https://learn.microsoft.com/aspnet/core/host-and-deploy/health-checks>.

- EF Core documentation: <https://learn.microsoft.com/ef/core/>.

- PostgreSQL documentation: <https://www.postgresql.org/docs/current/index.html>.
