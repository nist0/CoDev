---
name: project-governance
description: Govern execution with GitHub issues + Kanban and review outcomes as approved or rework required.
agent: "Project Orchestrator"

argument-hint: "tasks=<list> board=<name>"
---

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Inputs:

- tasks: ${input:tasks:list of delegated tasks}

- board: ${input:board:github project board name}

Requirements:

- Propose issue structure for each task.

- Propose Kanban workflow and WIP policy.

- Review completed tasks and return verdicts: `approved` or `rework required`.

- In review verdicts, every line must begin with `(Agent: <name>)`.

- For each rework verdict, include explicit gap, owner, and verification needed to close it.

- If brainstorming is in scope, produce one issue draft that summarizes brainstorming participants, exchanges, decisions, and resulting tasks.

Output:

- issue draft set

- kanban setup

- review verdict table

- rework protocol table

- next iteration actions

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Project Orchestrator** | always -- governance execution | *(this prompt)* | Issues structured, Kanban workflow proposed, review verdicts produced |
| 2 | **Implementer** | verdict is rework required | Back to domain prompt | Gap closed, evidence provided |
| 3 | **Reviewer** | rework complete | `/pr-review` | Verdict updated to approved |
| 4 | **Project Orchestrator** | iteration complete | Repeat this prompt for next iteration | All in-flight tasks resolved, backlog reprioritized |
| 5 | **Delivery Lead** | sprint/phase complete | `/release-plan` (if release-gated) | Release plan produced and approved |
