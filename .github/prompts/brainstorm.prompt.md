---
name: brainstorm
description: "Elite multi-agent brainstorming workflow with idea portfolio scoring, execution handoff, and governance artifacts."
agent: "Innovator"

argument-hint: "topic=<text> constraints=<text> success-metric=<text>"
---

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If `{{input}}` is empty or missing, derive topic, constraints, success metric, and assumptions from session context first: active objective, open issue/PR references, active file focus, and recent repository activity.

- When inference is used, include a `Context used for review` section in the output that lists inferred values and confidence (high/medium/low) so the reviewer can validate scope.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- If confidence remains low, ask one concise clarification that unblocks the workshop.

- Do not fail solely because arguments were omitted.

**Guard**: If `{{input}}` is empty or missing, infer topic, constraints, success metric, and assumptions from the current workspace, active file, and session context first. If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

Apply the procedure from `.github/skills/elite-brainstorming/SKILL.md`.

Single source of truth:

- The brainstorming method, scoring rubric, portfolio design, falsifiability rules, review governance, self-check, and deliverables are defined in `elite-brainstorming`.

- Do not restate or redefine those steps here.

- If there is a conflict, follow the skill.

If `{{input}}` is empty and context inference is insufficient, ask the user for all four inputs **in a single message** before starting the workshop:

1. **Topic / objective** — what decision or challenge to brainstorm (e.g. "how to reduce deploy time", "new feature ideas for X")

2. **Constraints** — budget, timeline, team size, tech, policy, or any hard limits

3. **Success metric** — how will you know the chosen option worked? (measurable signal)

4. **Assumptions** — any known beliefs or constraints the user is starting with, and what would invalidate them

Proceed to the workshop when you have high-confidence values from either input, session context, or user clarifications.

If `{{input}}` is provided, extract topic, constraints, success metric, and assumptions directly from it and proceed to the workshop.

Act as an Innovator and run an elite brainstorming workshop for: {{input}}

Execution contract:

- Follow `elite-brainstorming` end to end.

- Produce all required deliverables defined by the skill.

- Keep outputs deterministic, issue-ready, and delegation-ready for `/project-dispatch` and `/project-governance`.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Innovator** | always — ideation workshop | *(this prompt)* | 3-option portfolio produced with EV scores, kill criteria, and spike plans |
| 2 | **Project Orchestrator** | shortlist approved, ready for execution | `/project-dispatch` | Tasks decomposed with owners, AC, and GitHub issue-ready definitions |
| 3 | **Project Orchestrator** | tasks dispatched | `/project-governance` | Kanban board configured, review verdict table produced |
| 4 | **Innovator** | spike results available | Re-run `/brainstorm` with spike findings | Hypothesis confirmed or option killed based on evidence |
