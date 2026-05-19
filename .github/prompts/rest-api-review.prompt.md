---
name: rest-api-review
description: Audit and improve an existing ASP.NET Core REST API for contract quality, error handling, EF Core/PostgreSQL correctness, security, observability, and tests.
agent: REST API Engineer

argument-hint: "scope=<api-area> focus=<comma-list>"
---

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Goal

Produce a risk-ranked API quality audit with a pragmatic remediation plan.

Inputs

- scope: ${input:scope:ex Products API v1}

- focus: ${input:focus:ex routes,problems,openapi,postgresql,security,observability,tests}

Requirements

- Apply the procedure from `.github/skills/rest-api-runtime-quality/SKILL.md`.

- Use `.github/skills/rest-api-design-governance/SKILL.md` to evaluate route and contract quality.

- Evaluate architecture boundaries, status-code consistency, validation shape, OpenAPI completeness, persistence safety, security assumptions, and observability.

- Return findings with severity and recommended sequencing.

Output format

- Audit scope and assumptions.

- Findings table (`severity`, `area`, `evidence`, `impact`).

- Prioritized remediation plan.

- Release-readiness verdict and residual risks.

- Verification commands.

Constraints

- Prefer additive, low-risk remediations first.

- Do not suggest unnecessary rewrites.

- Keep recommendations aligned with controller-based ASP.NET Core architecture.
