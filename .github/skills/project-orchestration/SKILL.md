---
name: project-orchestration
description: End-to-end orchestration workflow for idea clarification, deep planning, specialist dispatch, and delivery governance.
argument-hint: "[goal] [constraints]"
user-invocable: true

disable-model-invocation: false
---

# project-orchestration Skill (Elite)

## When to use

- A user wants to delegate a whole project lifecycle.

- Work must be coordinated across multiple specialist agents.

- You need structured governance with explicit review verdicts.

## Procedure

### 1. Clarify the goal

- Ask targeted questions (outcomes, constraints, timeline, non-goals, stakeholders).

- If unanswered: list explicit assumptions and flag for confirmation.

- Define **success metric** (how will we know the project succeeded?).

### 2. Inventory existing assets (codebase-first)

- Scan existing agents, prompts, skills, and instructions before proposing new ones.

- Reuse and extend existing assets to avoid duplication.

- Treat instruction files as mandatory constraints for all work.

### 3. Gather specialist perspectives

- Request viewpoints from relevant specialists:

  - Architect (boundaries, design risks).

  - Reliability (failure modes, observability needs).

  - Reviewer (quality gates, compliance).

  - Innovator (if brainstorming is in scope).

- Each perspective: <= 3 bullets. Every line starts with `(Agent: <name>)`.

### 4. Build a deep phased plan

For each phase:

```text
Phase N: <name>
  Duration: <estimate>
  Dependencies: <phases that must complete first>
  Milestone: <deliverable>
  Risks: <and mitigations>
  Acceptance criteria: <list of falsifiable criteria>
```

### 5. Dispatch execution

Split plan into atomic tasks (<= 3 days effort each):

| Task | Owner agent | Dependencies | Deliverable | Acceptance criteria | Verification |
|------|-------------|-------------|-------------|---------------------|-------------|

- Flag critical path tasks explicitly.

- Note parallelizable tasks.

### 6. GitHub issues + Kanban

- Open one issue per task (use `github-work-management` skill).

- Apply labels, milestone, Kanban column.

- Enforce WIP limits: <= 2 In Progress per person.

### 7. Govern completion

For each completed task:

```text
(Agent: <name>) approved | rework required
  -- reason / gap
  -- closure evidence required: <what must be shown>
```

- Re-review is mandatory after rework.

- `priority:p0` tasks require two approvals.

### 8. Capture brainstorming continuity (when in scope)

Produce one issue-ready summary:

- All participating agents.

- Key exchanges and decisions.

- Shortlisted options and rationale.

- Resulting tasks and GitHub project status mapping.

## Self-check

- [ ] Clarifying questions asked and answered (or assumptions stated).

- [ ] No duplicate assets created; existing reused.

- [ ] Every task has: owner + acceptance criteria + verification.

- [ ] Critical path identified; parallelizable tasks noted.

- [ ] Review verdicts explicit for all completed tasks.

- [ ] Brainstorming summary produced (when brainstorming was in scope).

- [ ] WIP limits respected.

## Deliverables

- Clarification log with assumptions.

- Phased project plan.

- Dispatch matrix (task -> agent -> deliverable).

- GitHub issue set + Kanban setup.

- Review decisions + next actions.

- Brainstorming summary issue draft (when in scope).
