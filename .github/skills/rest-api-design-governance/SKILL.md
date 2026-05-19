---
name: rest-api-design-governance
description: Design and govern ASP.NET Core REST APIs with resource-first contracts, controller boundaries, CQRS + IMediator, versioning, and OpenAPI quality.

## user-invocable: true

# REST API Design Governance

## When to use

- Designing a new controller-based ASP.NET Core API.

- Adding a new resource while keeping route and contract consistency.

- Reviewing API design choices for long-term maintainability.

## Required inputs

- API goal and resource scope.

- Target .NET version and project constraints.

- Existing route/versioning/error conventions.

## Optional inputs

- Existing OpenAPI document.

- Existing DTOs/handlers/entities.

- Client compatibility constraints.

## Procedure

1. Confirm boundaries and assumptions.

   - Identify API host, Application, Domain, and Infrastructure responsibilities.

   - Record assumptions when context is missing.

2. Define the resource model and routes.

   - Use noun-based resource routes and standard HTTP verbs.

   - Decide route versioning and deprecation posture.

3. Define contracts.

   - Use explicit request/response DTOs.

   - Define list/pagination/sorting/filtering contracts.

4. Define application flow.

   - Map controller actions to IMediator commands and queries.

   - Keep business rules in handlers/domain, not controllers.

5. Define error and OpenAPI quality gates.

   - Map expected failures to status codes and `ProblemDetails`.

   - Ensure OpenAPI includes response/error schemas and operation intent.

6. Produce final design artifact.

   - Provide route table, DTO list, handler list, and acceptance checks.

## Self-check

- [ ] Routes are resource-oriented and version-consistent.

- [ ] Controllers are thin and IMediator-based.

- [ ] DTOs are explicit and EF entities are not exposed.

- [ ] Error contract uses `ProblemDetails` consistently.

- [ ] OpenAPI completeness and usefulness are verified.

- [ ] Architecture choices are justified without over-engineering.

## Outputs

- API design summary.

- Route and contract table.

- CQRS command/query map.

- OpenAPI + validation/error quality checklist.

## Common mistakes to avoid

- Action-style routes (`/create`, `/get-all`) instead of resource routes.

- Business logic inside controllers.

- Reusing EF entities as API contracts.

- Versioning strategy that is implicit or inconsistent.

## Sources

- ASP.NET Core web API guidance: <https://learn.microsoft.com/aspnet/core/web-api/>.

- ASP.NET Core model validation and problem details: <https://learn.microsoft.com/aspnet/core/web-api/handle-errors>.

- OpenAPI specification: <https://spec.openapis.org/oas/latest.html>.

- RFC 9110 HTTP semantics: <https://www.rfc-editor.org/rfc/rfc9110>.
