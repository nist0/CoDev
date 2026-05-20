---
name: openapi
description: OpenAPI/Swagger -- operation IDs, response schemas, auth documentation, error responses, and spec validation.
argument-hint: "[API name or endpoint group]"
user-invocable: true

disable-model-invocation: false
---

# OpenAPI / Swagger (Elite)

## When to use

- Generating or improving OpenAPI specs for ASP.NET Core APIs.

- Ensuring accurate schema, auth, examples, and error responses.

## Response Schema Checklist

| Status Code | Schema Required |
|-------------|----------------|
| 200/201 | Success response body schema + examples |
| 400 | `ProblemDetails` with validation errors |
| 401 | Auth error (no body typically) |
| 403 | Forbidden (no body typically) |
| 404 | `ProblemDetails` |
| 500 | `ProblemDetails` |

## Workflow

### 1. Define operation IDs, schemas, examples

- Unique `operationId` per endpoint: `CreateUser`, `GetOrderById`.

- Request/response schemas with examples using `[SwaggerRequestExample]`/`[ProducesResponseType]`.

### 2. Document auth schemes

- Bearer JWT: `SecuritySchemes: Bearer`.

- API key: `SecuritySchemes: ApiKey`.

- Apply globally via `AddSecurityRequirement` or per-operation.

### 3. Add error response schemas

- All error responses use `ProblemDetails` (RFC 7807).

- Add `[ProducesResponseType(typeof(ProblemDetails), 400)]` etc.

### 4. Validate and verify

- Lint spec: `npx @redocly/cli lint openapi.json`.

- Verify in Swagger UI or Redoc.

- Run example validation in CI.

## Self-check

- [ ] All operations have unique `operationId`.

- [ ] Request/response schemas documented with examples.

- [ ] Auth scheme documented and applied to secured endpoints.

- [ ] Error responses (400, 401, 403, 404, 500) all documented with `ProblemDetails`.

- [ ] Spec lint passes (`redocly lint` or `swagger-cli validate`).

## Outputs

- OpenAPI attribute guidance.

- Schema and example patterns.

- Auth configuration checklist.

- Validation steps.
