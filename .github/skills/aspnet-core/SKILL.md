---
name: aspnet-core
description: ASP.NET Core REST API conventions -- routing, versioning, validation, error handling, auth, observability, and production readiness.
argument-hint: "[api-name] [concern]"
user-invocable: true

disable-model-invocation: false
---

# ASP.NET Core (REST API) (Elite)

## When to use

- Building or evolving an ASP.NET Core REST API.

- Defining API conventions: routing, versioning, validation, error handling, auth.

- Improving production readiness (health checks, rate limits, observability).

## Workflow

1) Define API shape

   - Resources, endpoints, HTTP verbs, status codes, pagination strategy.

   - Versioning strategy (URI or header) and backward compatibility rules.
2) Setup baseline project conventions

   - Global exception handling (ProblemDetails).

   - Validation (model validation / FluentValidation).

   - Authentication/authorization boundaries.
3) Add operational endpoints

   - Health checks, readiness/liveness, build info endpoint.
4) Observability defaults

   - Structured logging, correlation IDs, trace propagation.
5) Error handling & resiliency

   - Timeouts, cancellation tokens, retry/circuit breaker (where appropriate).
6) Documentation

   - OpenAPI with examples, auth schemes, and clear error responses.
7) Verification

   - Unit tests for business logic + integration tests for API endpoints.

## Self-check

- [ ] Global exception handler configured and returns `ProblemDetails`.

- [ ] FluentValidation (or equivalent) applied to all request DTOs.

- [ ] Versioning strategy documented and applied.

- [ ] Health/readiness/liveness endpoints present.

- [ ] Structured logging with correlation IDs in place.

- [ ] OpenAPI spec includes: auth schemes, error responses, examples.

- [ ] Integration tests cover: success + validation + authorization + failure paths.

## Outputs

- Recommended API conventions (routing/versioning/errors).

- Minimal middleware pipeline checklist.

- Implementation steps for production readiness.

- Verification checklist (tests + health + spec).

## Advanced patterns

- Use endpoint-level authorization policy names instead of scattered inline checks.

- Standardize error contract with `ProblemDetails` for consistency across services.

- Add request/response examples in OpenAPI for high-risk endpoints.

- Prefer idempotency keys for externally triggered create operations when replay risk exists.

## Example baseline checklist

- Global exception handler configured.

- Validation behavior defined and documented.

- Health/readiness/liveness endpoints included.

- OpenAPI auth schemes and error responses documented.

- Integration tests cover success + validation + authorization + failure paths.

## Microsoft references

- [ASP.NET Core fundamentals](https://learn.microsoft.com/aspnet/core/fundamentals/)

- [Routing](https://learn.microsoft.com/aspnet/core/fundamentals/routing)

- [Error handling](https://learn.microsoft.com/aspnet/core/fundamentals/error-handling)

- [Health checks](https://learn.microsoft.com/aspnet/core/host-and-deploy/health-checks)

- [Web API design](https://learn.microsoft.com/azure/architecture/best-practices/api-design)
