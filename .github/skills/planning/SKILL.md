---
name: planning
description: Elite GitHub delivery planning — milestones, roadmaps, prioritization, and cadence governance.
argument-hint: "[project-name] [horizon]"
user-invocable: true
disable-model-invocation: false
---

# Planning (Elite Delivery)

## When to use

- You need to set up or review a project's delivery planning model.
- You want consistent triage → prioritization → execution → release mapping.
- You need milestone structure, Kanban policy, or a roadmap horizon.

## Procedure

### 1. Choose the right planning granularity

| Artifact | Scope | Horizon |
|----------|-------|---------|
| Roadmap | Strategic themes | 3–12 months |
| Milestone | Release or sprint | 1–6 weeks |
| GitHub Project | Workflow tracking | ongoing |
| Issue | Atomic task | 1–3 days |
| Sub-task (checkbox) | Step within a task | < 1 day |

### 2. Prioritization model

Score each candidate issue:

| Dimension | Weight | Signal |
|-----------|--------|--------|
| User/business impact | 40% | Revenue, retention, SLO, complaints |
| Effort | 20% | T-shirt size: S (< 1d) / M (1–3d) / L (> 3d) |
| Dependencies / blockers | 20% | Issues or people that must complete first |
| Risk if deferred | 20% | Security, tech debt accumulation, contractual |

Priority labels:

- `priority:p0` — production incident or milestone-blocking. Must start now.
- `priority:p1` — high-impact, next available slot.
- `priority:p2` — standard queue.

### 3. Milestone structure

Each milestone must have:

- **Goal**: one-sentence statement of what "done" looks like.
- **Due date**: hard limit (move scope, not date).
- **Scope**: list of issue references.
- **Exit criteria**: measurable conditions before closing the milestone.
- **Risk log**: 1–3 risks with owners and mitigations.

### 4. Execution cadence

| Cadence | Activity |
|---------|----------|
| Weekly | Planning session: groom backlog, move to Ready, set WIP |
| Daily async | Status update in GitHub issue or Slack thread |
| PR-based | All deliverables land via PR; no direct-to-main pushes |
| End of milestone | Retrospective + progress rollup (see `github-work-management` skill) |

### 5. Roadmap governance

- Roadmap is a living document; update at the end of each milestone.
- Each roadmap theme maps to a capability in `routing/capabilities.yaml` (for framework work).
- Defer items explicitly (record reason + target milestone) rather than silently dropping them.
- Communicate roadmap changes to stakeholders before the next milestone start.

### 6. Delivery metrics

Track at the end of each milestone:

| Metric | How to measure |
|--------|----------------|
| Cycle time | Issue opened → PR merged (median days) |
| Throughput | Issues closed per week |
| Blocked ratio | Issues in `status:blocked` / total open |
| Scope added | Issues added after milestone start |
| Scope completed | Issues closed within planned scope |

## Self-check

- [ ] Every issue has: owner, priority label, milestone, acceptance criteria.
- [ ] Milestone has: goal, due date, scope, exit criteria, risk log.
- [ ] `priority:p0` items have immediate assignee.
- [ ] Roadmap updated at end of each milestone; deferred items logged with reason.
- [ ] Delivery metrics captured and shared.

## Outputs

- Milestone structure (goal, scope, exit criteria, risk log).
- Prioritized backlog (scored issues).
- Roadmap horizon map (themes → milestones).
- Delivery cadence checklist.
- Delivery metrics dashboard template.
