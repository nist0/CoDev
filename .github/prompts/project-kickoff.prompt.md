---
name: project-kickoff
description: "Clarify project intent and produce a deep phased plan with risks and acceptance criteria."
agent: "Project Orchestrator"

## argument-hint: "goal=<text> constraints=<text> timeline=<text>"

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Inputs:

- goal: ${input:goal:what success looks like}

- constraints: ${input:constraints:budget/time/tech/policy constraints}

- timeline: ${input:timeline:target dates or phases}

Requirements:

- Ask clarifying questions first.

- Then produce assumptions, phased plan, dependencies, acceptance criteria, and risks.

- If the request is a brainstorming initiative, include a workshop summary section with agents involved and key decisions.

- Include an initial issue creation plan and GitHub project board mapping.

Output:

- questions

- phased plan

- milestone checklist

- verification checklist

- brainstorming summary (when applicable)

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Project Orchestrator** | always — project kickoff | *(this prompt)* | Clarifying questions answered, phased plan produced with AC and risks |
| 2 | **Innovator** | request is a brainstorming initiative | `/brainstorm` | Option portfolio produced, shortlist with kill criteria defined |
| 3 | **Project Orchestrator** | plan approved | `/project-dispatch` | Tasks decomposed, owners assigned, GitHub issues opened |
| 4 | **Project Orchestrator** | tasks dispatched | `/project-governance` | Kanban board configured, WIP limits set |
