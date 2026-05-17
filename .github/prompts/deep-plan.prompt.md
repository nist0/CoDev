---
name: deep-plan
description: "Elite planning entry point: runs a mandatory brainstorm (≥ 3 scored options), produces a ranked implementation plan, and emits a GitHub issue draft with full sub-task checklist — for any domain."
agent: plan
argument-hint: "goal=<what you want to build or fix> [constraints=<time/tech/scope>]"
---


Argument handling:

- If arguments are provided, treat them as authoritative.
- If arguments are omitted, infer missing values from the current workspace, active file, and session context.
- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.
- Do not fail solely because arguments were omitted.

Apply the procedure from `.github/skills/elite-brainstorming/SKILL.md`.
Apply the procedure from `.github/skills/github-work-management/SKILL.md`.
Single source of truth:

- Brainstorming method, scoring, shortlist selection, and falsifiability rules are defined in `elite-brainstorming`.
- Issue lifecycle, Kanban flow, and review governance are defined in `github-work-management`.
- Do not redefine those procedures here.

Execution contract:

1. Run mandatory brainstorming first (safe, adjacent, bold options) using the skill.
2. Select one finalist with explicit rationale and risk trade-off.
3. Produce a ranked implementation plan with assumptions, files, steps, risks, acceptance criteria, and verification commands.
4. Emit one copy/paste-ready GitHub issue body with sub-tasks and progress log starter.
5. Keep output deterministic and ready for direct handoff to implementation.

Required output sections:

- Objective and constraints
- Scored option portfolio and finalist
- Ranked implementation plan
- GitHub issue draft (complete body)
- Delegation chain and next action

## Delegation chain

| Task | Owner | Trigger |
|------|-------|---------|
| Brainstorm portfolio review | Innovator | Phase 1 is ambiguous or needs deeper ideation |
| Implementation | implement agent | Plan + issue accepted by user |
| PR review | reviewer agent | Branch pushed, CI green |
| Issue + project tracking | Delivery Lead | Any multi-day / multi-PR scope |
