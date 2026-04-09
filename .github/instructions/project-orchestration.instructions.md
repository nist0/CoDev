---
name: "Project Orchestration Defaults"
description: "Whole-project delegation defaults: clarify, plan, dispatch, track, and review."
applyTo: "**"
---

# Project Orchestration Defaults

## Clarify before planning

- For whole-project requests, ask clarifying questions before planning.
- Required clarifications: scope, constraints, stakeholders, definition of done, timeline.
- Do not start implementation until the plan is acknowledged.

## Phased planning

- Produce phased plans with dependencies, risks, and acceptance criteria per phase.
- Keep plans to ≤10 bullets; link to detailed specs for each phase.
- Identify the critical path and flag tasks that block parallelism.

## Task delegation

- Dispatch tasks to specialist agents with explicit ownership.
- Use issue-ready task definitions: scope, done criteria, verification command.
- Recommend GitHub project Kanban states (`Backlog`, `In Progress`, `In Review`, `Done`) and WIP limits.

## Review gates

- Review each completed task with explicit verdict: **approved** or **rework required**.
- For `rework required`, state the exact gap and the evidence needed to close it.
- Keep outputs concise, deterministic, and checklist-oriented.

## Example: phased plan entry

```text
### Phase 2 — API layer (owner: engineering.backend-dotnet)
**Scope**: Implement `/api/orders` CRUD endpoints with OpenAPI docs.
**Dependencies**: Phase 1 (DB schema) complete.
**Acceptance criteria**:
  - All endpoints return `ProblemDetails` on error.
  - OpenAPI spec regenerated; no breaking changes vs. v1 contract.
  - Integration tests pass in CI.
**Verification**: `dotnet test --filter Category=Integration` exits 0.
**Risk**: EF migration on existing data — requires dry-run on staging before prod.
```

---

## 🏆 Elite Section — Top 5% Orchestration Practices

- **RACI matrix per phase**: For each phase, document Responsible, Accountable, Consulted, and Informed roles. Ambiguity in ownership is the #1 cause of delivery slippage.
- **Explicit WIP limits**: Cap the number of in-flight tasks per agent/team (e.g. max 2 `In Progress` per engineer). Exceeding the limit triggers a sync before new work starts.
- **Risk register**: Maintain a living risk register alongside the plan. Each risk has: probability (H/M/L), impact (H/M/L), owner, and mitigation. Review weekly.
- **Incremental delivery over big-bang**: Prefer shipping working software to staging after each phase rather than integrating everything at the end. Each phase produces a deployable artifact.
- **Retrospective cadence**: Run a retrospective at the end of each phase (not just at project end). Capture 3 things that went well, 3 to improve, and one immediate action item.
- **Decision log**: Record all significant architectural or scope decisions in `docs/decisions/NNNN-title.md` with date, options considered, rationale, and owner. Prevents re-litigating decisions.
