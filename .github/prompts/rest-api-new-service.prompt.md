---
name: rest-api-new-service
description: Design a new controller-based ASP.NET Core REST API with CQRS + IMediator, DTO contracts, EF Core/PostgreSQL boundaries, and production quality gates.
agent: REST API Engineer
argument-hint: "apiName=<name> resources=<comma-list> constraints=<text>"
---

Goal

Design a reusable, production-ready REST API blueprint for a new service.

Inputs

- apiName: ${input:apiName:ex CatalogApi}
- resources: ${input:resources:ex Products,Categories}
- constraints: ${input:constraints:ex net8-lts + route-versioning + postgres}

Requirements

- Apply the procedure from `.github/skills/rest-api-design-governance/SKILL.md`.
- Apply runtime quality gates from `.github/skills/rest-api-runtime-quality/SKILL.md`.
- Default to controller-based ASP.NET Core APIs with CQRS + IMediator.
- Keep architecture pragmatic: avoid unnecessary projects or abstractions.
- Include route design, DTO policy, validation/error policy, persistence boundaries, security assumptions, observability baseline, and test strategy.

Output format

- API blueprint summary.
- Proposed project structure (`src/` and `tests/`).
- Resource route table and command/query map.
- Contract and `ProblemDetails` standards.
- Verification checklist with exact commands.

Constraints

- Do not default to Minimal APIs or FastEndpoints.
- Do not place business logic in controllers.
- Do not expose EF entities in API responses.
