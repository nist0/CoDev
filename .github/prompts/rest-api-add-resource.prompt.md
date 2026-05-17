---
name: rest-api-add-resource
description: Add a new resource to an existing ASP.NET Core REST API with consistent routes, DTOs, IMediator handlers, validation, and OpenAPI updates.
agent: REST API Engineer
argument-hint: "resource=<name> operations=<list> apiVersion=<v1|v2>"
---


Argument handling:

- If arguments are provided, treat them as authoritative.
- If arguments are omitted, infer missing values from the current workspace, active file, and session context.
- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.
- Do not fail solely because arguments were omitted.

Goal

Add a resource to an existing API without breaking architecture or contracts.

Inputs

- resource: ${input:resource:ex Products}
- operations: ${input:operations:ex create,getById,update,delete,list}
- apiVersion: ${input:apiVersion:ex v1}

Requirements

- Apply the procedure from `.github/skills/rest-api-design-governance/SKILL.md`.
- Apply runtime quality gates from `.github/skills/rest-api-runtime-quality/SKILL.md`.
- Keep controllers thin and IMediator-driven.
- Include DTOs, validators, command/query handlers, `ProblemDetails` mapping, and OpenAPI response documentation.
- Include pagination contract when list endpoints are requested.

Output format

- Files-to-change checklist.
- Endpoint and contract plan.
- Validation/error/OpenAPI update list.
- Compatibility and migration notes.
- Test plan and verification commands.

Constraints

- No action-style routes.
- No controller business logic.
- No direct EF entity exposure in request/response contracts.
