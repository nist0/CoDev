---
name: cli-platform-task
description: "Execute an assigned task on the .NET CLI platform project using docs/project-context.md as preloaded context — routes, gathers task context, plans tests, implements, and ships. Phase 3 of the CLI platform onboarding workflow."
agent: "CLI Platform Onboarder"

## argument-hint: "task=<description of assigned task>"

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Apply procedures from `.github/skills/cli-platform-analysis/SKILL.md`, `.github/skills/dotnet-testing/SKILL.md`, `.github/skills/dotnet-cli/SKILL.md`, `.github/skills/delivery/SKILL.md`, and `.github/skills/github-actions/SKILL.md`.

Inputs:

- task: ${input:task:describe the assigned task exactly as given to you}

**Prerequisites**:

- Phase 1 (Bootstrap) verified.

- Phase 2 (Analysis) complete — `docs/project-context.md` exists and is committed.

**Preload `docs/project-context.md` now** before any analysis below.

Act as a CLI Platform Onboarder coordinating **Phase 3 (Task Execution)** for the provided `task` input.

Single source of truth:

- Task routing, context extraction, test planning, implementation quality gates, and shipping flow are defined in the linked skills.

- Do not restate or redefine those procedures here.

Execution contract:

1. Route the task and confirm capability/domain handoff.

2. Derive scoped context from `docs/project-context.md`.

3. Produce and review a test plan before implementation.

4. Implement using .NET, delivery, and CI security conventions from the linked skills.

5. Run review and release gates as required.

6. Emit final phase status with outputs, blockers, and next action.

Required outputs:

- Routing summary

- Task context summary

- Approved test plan

- Verification results

- Phase status block

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **CLI Platform Onboarder** | always — task routing | `/route <task>` | Capability + domain + agent confirmed |
| 2 | **Architect** | test plan required | `/test-plan` | Test plan table reviewed and approved |
| 3 | **Backend .NET** | implementation phase | *(inline in Step 4)* | Code implemented, dotnet build -warnaserror + dotnet test green |
| 4 | **Delivery Lead** | implementation complete | `/pr-review` | All CI gates green, PR approved |
| 5 | **Delivery Lead** | release-gated task | `/release-plan` | Release plan produced and approved |
| 6 | **CLI Platform Onboarder** | task complete | Next `/cli-platform-task` | Phase status emitted, next task assigned |
