---
name: github-work-management
description: Elite delivery governance — issue lifecycle, Kanban discipline, traceability, WIP enforcement, and review gates.
argument-hint: "[project-name] [milestones]"
user-invocable: true
disable-model-invocation: false
---

# GitHub Work Management (Elite)

## When to use

- Work needs issue-level traceability and Kanban visibility.
- A project requires governance with explicit approved/rework-required decisions.
- You need a dependency graph, milestone hierarchy, or WIP limit enforcement.

## Procedure

### 1. Epic / milestone hierarchy

```text
Epic (GitHub issue labeled `type:epic`)
  └─ Milestone (sprint or release cycle, e.g. v1.2.0 / Sprint-04)
       └─ Task issues (atomic, ≤ 3 days effort each)
            └─ Sub-tasks (checkboxes inside the issue body)
```

- Epics are tracking issues; they do not carry implementation — only links to task issues.
- Every task issue must belong to exactly one milestone.
- Milestone due dates are hard limits; move scope, not dates.

### 2. Issue modeling (mandatory fields)

**Before creating any issue for a non-trivial task, a brainstorm must be complete** (≥ 3 scored options produced by the Innovator agent or `/brainstorm`). The finalist rationale feeds directly into `## Technical approach`.

Every task issue body must include **all** of the following sections. This is a living document — update it as work evolves; do not treat it as a one-shot creation:

```markdown
## Summary
<Why this work is needed; what problem it solves; link to epic or stakeholder request.>

## Technical approach
<How the problem will be solved. Write the initial plan here before branching.
Update this section when the approach is refined mid-implementation.>

## Files to modify
- `path/to/file.ext` — what change and why
<!-- Update this list as scope is discovered or changes -->

## Sub-tasks
<!-- Use - [ ] for atomic inline tasks; open child issues (linked below) for tasks spanning >1 PR -->
- [ ] Sub-task 1 (`path/to/file.ext`) — brief description
- [ ] Sub-task 2
<!-- Child issues: Part of #N -->

## Dependencies
- Blocks: #<issue>
- Blocked by: #<issue>

## Acceptance criteria
- [ ] <verifiable criterion 1>
- [ ] <verifiable criterion 2>

## Verification steps
1. <exact local command or CI check expected to pass>
2. <second check>

## Progress log
<!-- Append dated entries as work evolves: scope changes, blockers, decisions, discoveries -->
<!-- Format: YYYY-MM-DD — <what changed / was decided / was discovered> -->

## Definition of Done
- [ ] Code reviewed and approved
- [ ] All acceptance criteria checked
- [ ] CI green (lint + tests + security)
- [ ] Docs updated if public behavior changed
- [ ] Issue linked in PR and PR merged

## Review verdict
<!-- filled by reviewer -->
approved | rework required
```

**Living issue protocol** — the issue is amended throughout the task lifecycle:

| Trigger | Required update |
| --- | --- |
| Approach refined or changed | Update `Technical approach` + append to `Progress log` |
| New file discovered in scope | Add to `Files to modify` |
| Blocker found | Add `Blocked by: #N`, apply `status:blocked` label, append to `Progress log` |
| Scope reduced or deferred | Strike out or remove items; append rationale to `Progress log` |
| AC checkbox passed | Tick the box with `gh issue edit <N> --body-file <path>` |
| Mid-task decision recorded | Append dated entry to `Progress log` |

Use `gh issue edit <N> --body-file <path>` (single-quoted heredoc) for all updates — never inline `--body` in PowerShell.

Issue title conventions:

- Feature work: `enh: <title>`
- Bug fix: `fix: <title>`
- Chore / maintenance: `chore: <title>`
- Documentation: `docs: <title>`
- **Never use** `Enhancement: <title>`

### 3. Label taxonomy

```text
type:enh        type:fix        type:chore      type:docs
area:routing    area:agents     area:skills     area:infra    area:ci
priority:p0     priority:p1     priority:p2
status:ready    status:blocked  status:in-review  status:rework
```

Apply `priority:p0` for production incidents or milestone-blocking issues.

### 4. Kanban flow

```text
Backlog → Ready → In Progress → In Review → Done
```

Column entry criteria:

| Column      | Entry criteria                                              |
| ----------- | ----------------------------------------------------------- |
| Ready       | Issue has scope + acceptance criteria + no unresolved dependencies |
| In Progress | Assignee confirmed; branch created following `git` skill convention |
| In Review   | PR opened, linked to issue, CI passing                      |
| Done        | PR merged; verification evidence recorded; issue closed     |

WIP limits (enforced):

- **In Progress**: ≤ 2 per person / ≤ 5 per team.
- **In Review**: ≤ 3 per reviewer at a time.
- Exceeding WIP limits: finish before starting; escalate blockers to lead.

### 5. Dependency graph management

When opening a new issue, map it against open issues:

1. List all issues it **blocks** (add `Blocks: #X` to body).
2. List all issues it is **blocked by** (add `Blocked by: #X` to body).
3. Add `status:blocked` label to issues that cannot start.
4. Update the blocking issue body with a `Blocks: #Y` reference.
5. On issue close: remove `status:blocked` from unblocked issues; add `status:ready`.

### 6. Review governance

For each issue reaching "In Review":

1. Reviewer runs the `pr-review` skill (8-pass procedure).
2. Verdict must be explicit:

   - **approved** → PR can merge; move issue to Done.
   - **rework required** → list exact gap checklist; move back to In Progress; apply `status:rework` label.

3. Re-review is mandatory after rework; do not self-approve after your own rework.
4. `priority:p0` issues require two approvals before merge.

### 7. Progress rollup format

Publish at the end of each sprint/cycle:

```markdown
## Sprint <N> — Progress Rollup (<date>)

**Done**: <count> issues — <titles or links>
**In Progress**: <count> — <titles, ETA>
**Blocked**: <count> — <titles, blocking reason, owner>
**Scope added**: <count> — <titles>
**Scope removed / deferred**: <count> — <titles, reason>

### Risks
- <risk description> — mitigation: <action>

### Next cycle priorities
1. <issue link>
2. <issue link>
```

### 8. Traceability audit

Run periodically to verify governance health:

```bash
# Issues without milestone
gh issue list --state open --json number,title,milestone \
  | jq '.[] | select(.milestone == null)'

# Issues without assignee
gh issue list --state open --json number,title,assignees \
  | jq '.[] | select(.assignees | length == 0)'

# Open PRs not linked to an issue
gh pr list --state open --json number,title,body \
  | jq '.[] | select(.body | test("Closes #|Refs #"; "i") | not)'
```

## Self-check

- [ ] No issue without: owner + scope + acceptance criteria + verification steps.
- [ ] All issues belong to a milestone with a due date.
- [ ] Dependencies mapped (blocks / blocked by) and labels applied.
- [ ] WIP limits respected; no queue pileup in In Review.
- [ ] Review verdicts are explicit (approved / rework required with gap list).
- [ ] Done items carry verification evidence before close.
- [ ] Progress rollup published at end of each cycle.

## Deliverables

- Copy/paste-ready issue template (see `examples/README.md`).
- Kanban column policy.
- Label taxonomy.
- Review verdict checklist.
- Progress rollup format.
- Traceability audit commands.
