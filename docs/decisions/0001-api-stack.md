# ADR-0001: ASP.NET Core REST API Stack

**Status**: accepted
**Date**: 2026-03-07
**Stakeholders**: Backend .NET, Architect, PromptSmith

## Context

This decision establishes the default ASP.NET Core REST API stack recommended by
the `rest-api-bootstrap` skill and applied to all new .NET 8 / .NET 9 API projects.

Three key constraints drove the evaluation:

- **Solo maintainability**: the stack must stay comprehensible to a single
  developer who has not touched the repo in 90 days.
- **Production readiness**: structured logging, typed errors, JWT auth, and an
  interactive API reference must be available from day one.
- **Scaffolding speed**: a developer should reach a green `dotnet test` from
  zero in under 2 hours, including learning time.

The evaluation flow was:

1. Brainstorm in issue #160 (three options scored).
2. Spike A (#163): prove Option A end-to-end on .NET 8.
3. Spike B (#164): prove Option B end-to-end on .NET 8.
4. This ADR records the outcome.

## Options considered

| Option | Stack | EV score (from brainstorm) | Reversibility |
| --- | --- | --- | --- |
| A - Elite Minimal | FastEndpoints 8.x + FastEndpoints.Security + FastEndpoints.Swagger (NSwag) + Serilog + ErrorOr + Scalar.AspNetCore | **8.6 / 10** | High - FE endpoints are plain classes; swap to minimal-API syntax in hours |
| B - VSA + MediatR | MediatR 12 + Scrutor + Serilog + ErrorOr + Swashbuckle + Scalar.AspNetCore | 7.2 / 10 | Medium - MediatR pipeline behaviours accumulate over time; migration to Option A is a 1-day effort |
| C - Stock Minimal API | No external routing lib + Serilog + FluentValidation + Scalar.AspNetCore | 6.0 / 10 | High - least dependencies; but boilerplate grows with endpoint count |

### Option A — Elite Minimal (chosen)

**Pros**:

- Each endpoint is a self-contained class: Configure + Handle — zero ceremony.
- FastEndpoints.Security ships JWT wiring as a one-liner (`AddAuthenticationJwtBearer`).
- FastEndpoints.Swagger (NSwag) generates the OpenAPI spec without requiring MVC
  infrastructure; Scalar renders it as an interactive UI.
- Serilog + `JsonFormatter` gives production-grade structured logs in 3 lines.
- ErrorOr enforces typed error propagation at compile time.

**Cons**:

- FastEndpoints is not a Microsoft-maintained package — depends on a small OSS team.
- Major version upgrades can carry breaking changes (v5 to v8: send methods moved
  to `HttpContext.Response.*` extension methods).
- Learning curve for developers unfamiliar with the endpoint-class pattern.

**Spike A findings (net8, FastEndpoints 8.x)**:

- `dotnet test` exits 0 with 2 integration tests via `WebApplicationFactory`.
- `GET /orders` returns `200` + structured JSON in < 1 s.
- Structured JSON log lines confirmed from first boot.
- Package pitfalls documented:
  - Do NOT install `Microsoft.AspNetCore.OpenApi` without pinning to `8.*` on
    net8 targets — the floating resolution pulls a net10-only source generator.
  - Pin all `FastEndpoints.*` packages to the same major version.

### Option B — VSA + MediatR

**Pros**:

- Vertical Slice Architecture (one folder per feature) is widely understood.
- Scrutor eliminates all manual handler registration — 0 `AddScoped` calls in
  `Program.cs` confirmed in spike.
- MediatR pipeline behaviours (logging, validation) are a well-documented pattern.

**Cons**:

- More moving parts: MediatR + Scrutor + Swashbuckle + Scalar = 4 extra packages
  vs Option A's 5 FastEndpoints packages (comparable count, higher complexity).
- `app.MapGet(...)` + `IMediator.Send(...)` in `Program.cs` is more coupling
  than Option A's pure endpoint class.
- Swashbuckle requires `AddEndpointsApiExplorer()` on net8 minimal APIs;
  not needed on net9+ where the native OpenAPI provider is available.

**Spike B findings (net8)**:

- `dotnet test` exits 0 with 2 integration tests.
- `GET /orders` returns `200` + JSON.
- Zero manual DI registrations in `Program.cs` verified (`Select-String AddScoped` = 0 matches).

### Option C — Stock Minimal API

Not spiked. Ruled out during brainstorm (#160): boilerplate proliferates as
endpoint count grows, and there is no built-in typed error propagation or
JWT helper. Remains valid for micro-services with 1-3 endpoints.

## Decision

We adopt **Option A — Elite Minimal** as the default stack for new ASP.NET Core
REST API projects, as documented in `.github/skills/rest-api-bootstrap/SKILL.md`.

Primary reasons:

1. Highest EV score (8.6 / 10) in the brainstorm, confirmed viable by Spike A.
2. Least Program.cs ceremony: endpoint classes are self-registering — no `MapGet`
   wiring and no Scrutor scan required.
3. FastEndpoints.Security reduces JWT setup to a single builder call.
4. The spike confirmed the full stack boots, tests pass, and logs are structured
   JSON in under 90 minutes from zero.

This decision does **not** prohibit Option B for teams that already use MediatR or
have a large existing VSA codebase. The `rest-api-bootstrap` skill documents both
as valid choices.

This decision supersedes: none (first ADR).

## Consequences

**Positive**:

- New APIs receive structured logging, JWT auth, typed errors, and an interactive
  OpenAPI UI without any extra scaffolding decisions.
- The `rest-api-bootstrap` skill encodes the recommendation, making it
  discoverable via `/route` and `/rest-api-bootstrap`.

**Negative / trade-offs**:

- Projects lock in on FastEndpoints OSS; a future abandonment would require
  migrating endpoint classes to minimal-API syntax (estimated 1 day for a
  20-endpoint service).
- FastEndpoints major upgrades require attention to breaking changes (documented
  in issue #163).

**Risks and mitigations**:

| Risk | Likelihood | Mitigation |
| --- | --- | --- |
| FastEndpoints OSS abandoned | Low | Endpoint classes are thin wrappers; minimal-API migration is mechanical |
| net8 EOL forces net9+ upgrade | Certain (Nov 2026) | Pin `FastEndpoints.*` to same major; test on net9 before EOL |
| New dev unfamiliar with endpoint-class pattern | Medium | `rest-api-bootstrap` SKILL.md includes a complete example; onboarding guide links to it |

## Kill criteria

Revisit this ADR and consider switching if any of the following occur:

- FastEndpoints is formally unmaintained for > 6 months.
- A Microsoft-official replacement (e.g. native endpoint routing classes) ships
  with equivalent JWT + OpenAPI feature parity.
- A project team reports > 1 day of friction adopting the stack after reading
  the SKILL.md.

## Follow-up actions

| Action | Owner | Due | Linked issue |
| --- | --- | --- | --- |
| Keep `rest-api-bootstrap` SKILL.md version refs current on each FE major release | Backend .NET | Rolling | #162 |
| Evaluate net9 GA impact on this ADR (native OpenAPI provider) | Architect | 2026-06-01 | (new issue) |
| Add FE upgrade notes to CoDev onboarding guide | PromptSmith | 2026-04-01 | (new issue) |
