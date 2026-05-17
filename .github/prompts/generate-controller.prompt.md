---
name: generate-controller
description: Generate a production-ready ASP.NET Core CRUD controller from a description, OpenAPI JSON contract, or resource theme.
agent: Backend .NET
argument-hint: "input-mode=<description|openapi|theme> [resource=<text>] [contract=<path-or-inline-json>]"
---


Argument handling:

- If arguments are provided, treat them as authoritative.
- If arguments are omitted, infer missing values from the current workspace, active file, and session context.
- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.
- Do not fail solely because arguments were omitted.

Use the `rest-api-controller-gen` skill to generate a complete, production-grade ASP.NET Core CRUD controller.

## Parameters

- **input-mode** *(required)*: one of `description`, `openapi`, or `theme`
- **resource** *(required for `description` and `theme` modes)*: the resource name and, for `description` mode, the field specification
- **contract** *(required for `openapi` mode)*: path to an OpenAPI JSON file, or an inline JSON snippet

## Input formats

### `description` mode

```text
/generate-controller input-mode=description resource="Products with Id (Guid), Name (string, required, max 200), Price (decimal > 0), CategoryId (Guid)"
```

### `openapi` mode

```text
/generate-controller input-mode=openapi contract="./openapi.json"
```

or paste an OpenAPI JSON snippet directly after `contract=`.

### `theme` mode

```text
/generate-controller input-mode=theme resource=Orders
```

A default resource shape is assumed (`Id`, `Name`, `CreatedAt`, `UpdatedAt`). Add domain-specific fields after scaffolding.

## Output (always generated)

1. **DTOs** — `sealed record` request and response types.
2. **FluentValidation validator** — one `AbstractValidator<TRequest>` per write DTO.
3. **MediatR commands and queries** — one per CRUD operation.
4. **Handler stubs** — one handler per command/query with DI constructor and mapping method.
5. **Controller class** — `[ApiController]`, versioned route, `[ProducesResponseType]` on each action, `CancellationToken` threaded through, `ProblemDetails` error contract.
6. **Authorization hooks** — `[Authorize]` / `[AllowAnonymous]` stubs per action.
7. **OpenAPI annotations** — XML doc comments (`<summary>`, `<response>`) + `[Produces("application/json")]`.
8. **Integration-test checklist** — `WebApplicationFactory<Program>` test class with all CRUD + error-path test method stubs.

## Rationale

- Inputs are validated against the `rest-api-controller-gen` skill before code is emitted.
- All generated code follows the conventions from the `aspnet-core` and `mediatr` skills: `ProblemDetails`, `FluentValidation`, `ISender`, no naked entity exposure.
- Three input modes enable generation from any entry point: whiteboard → code, contract-first, or rapid prototyping.

## Self-check (verify before shipping)

- [ ] DTOs use `sealed record` — no mutable class exposed.
- [ ] Validator covers all `required` and constraint rules from input.
- [ ] All actions have `[ProducesResponseType]` for every documented status code.
- [ ] `CancellationToken` passed to every `_sender.Send(...)` call.
- [ ] XML doc comment on every controller action.
- [ ] `CreatedAtAction` used on `POST` — `Location` header is set.
- [ ] Authorization attribute present on every action (explicit, never implicit).
- [ ] Integration test stubs present for all 4 operations + error paths.
