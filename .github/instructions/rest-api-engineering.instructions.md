---
name: "REST API Engineering"
description: "Controller-first REST API governance for ASP.NET Core controllers: resource routes, thin controllers, IMediator flow, ProblemDetails, and contract discipline."
applyTo: "**/*Controller.cs"
---

# REST API Engineering

- Use resource-oriented routes with nouns and HTTP verbs; avoid action-style routes.
- Keep controllers thin: orchestrate input/output and delegate use cases to IMediator.
- Keep business rules out of controllers; implement them in handlers/domain services.
- Use explicit request/response DTOs; never expose EF Core entities directly.
- Return standardized `ProblemDetails`/`ValidationProblemDetails` for error contracts.
- Include `CancellationToken` in async controller actions and pass it downstream.
- Document response contracts with `[ProducesResponseType]` and keep OpenAPI accurate.
- Follow Microsoft API controller guidance: <https://learn.microsoft.com/aspnet/core/web-api/>.
- Follow RFC 7807 for problem details: <https://www.rfc-editor.org/rfc/rfc7807>.
