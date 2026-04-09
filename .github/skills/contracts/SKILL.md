---
name: contracts
description: Full-stack API contracts — ownership, versioning, schema generation, validation, and consumer-driven contract tests.
argument-hint: "[API name or bounded context]"
user-invocable: true
disable-model-invocation: false
---

# Full-stack Contracts (API <-> Client) (Elite)

## When to use

- You need stable contracts between backend and frontend.
- You want versioning, compatibility, and shared DTO strategy.

## Contract Governance Table

| Concern | Rule |
|---------|------|
| Ownership | Backend owns schema; consumers follow |
| Backward compat | Add fields (don't remove); mark deprecated, then remove |
| Breaking changes | Major version bump; deprecation notice >=30 days |
| Schema format | OpenAPI 3.x preferred; JSON Schema for event/message contracts |
| Client generation | Generate clients from OpenAPI when feasible |

## Workflow

### 1. Define contract ownership

- Backend owns the OpenAPI spec or schema; frontend/consumers are generated.
- Document ownership in the repo `CONTRIBUTING.md` or ADR.

### 2. Versioning strategy

- Backward-compatible changes: add optional fields, new endpoints.
- Deprecations: annotate with `deprecated: true` + removal timeline.
- Breaking changes: bump major version, communicate with consumers.

### 3. Schema generation

- Use OpenAPI/JSON Schema to generate typed clients.
- Automate client generation in CI when spec changes.

### 4. Validation and examples

- Provide request/response examples in the OpenAPI spec.
- Validate examples against schema in CI.

### 5. Contract tests

- Smoke tests for key endpoints.
- Consumer-driven contract tests (Pact) for high-traffic contracts.

## Self-check

- [ ] Contract ownership documented (backend owns schema).
- [ ] Deprecation timeline defined for removed fields.
- [ ] Client generation automated in CI.
- [ ] Examples provided and validated against schema.
- [ ] Contract tests cover at least happy path + key error cases.

## Outputs

- Contract governance rules.
- Versioning/deprecation policy.
- Verification plan (contract + integration tests).
