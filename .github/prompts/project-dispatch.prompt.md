---
name: project-dispatch
description: Convert a project plan into delegated specialist tasks with clear ownership and issue-ready definitions.
agent: "Project Orchestrator"

## argument-hint: "plan=<summary> stack=<text>"

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

**Guard**: If both `plan` and `stack` are missing, infer them from the current workspace, active file, and session context first. If they still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

Inputs:

- plan: ${input:plan:project plan summary}

- stack: ${input:stack:main technologies and domains}

Requirements:

- Split into atomic tasks.

- Assign each task to the best specialist agent.

- Include objective, scope, dependencies, acceptance criteria, and verification steps.

- Include critical path and parallelization notes.

- For each task, suggest initial GitHub project column: Backlog, Ready, In Progress, In Review, or Done.

- Define specialist review owners and require review entries in this exact format: `(Agent: <name>) <approved|rework required> - <notes>`.

Output:

- dispatch table

- issue-ready task definitions

- sequencing and parallelization notes

- review ownership matrix

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Project Orchestrator** | always — task decomposition | *(this prompt)* | Dispatch table produced, each task has owner agent, AC, and verification |
| 2 | **Domain specialist** (Backend .NET / DevOps / Frontend / etc.) | per task assigned | relevant domain prompt | Task implemented, CI green |
| 3 | **Reviewer** | per task, when implementation complete | `/pr-review` | Verdict approved for each task |
| 4 | **Project Orchestrator** | all tasks dispatched | `/project-governance` | Kanban board set up, WIP limits enforced, verdicts recorded |
