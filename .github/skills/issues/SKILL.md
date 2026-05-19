---
name: issues
description: GitHub Issues triage — classification, labels, acceptance criteria, and planning integration.
argument-hint: "[issue title or area]"
user-invocable: true

## disable-model-invocation: false

# Issues (Triage, Labels, Quality) (Elite)

## When to use

- You need to triage incoming issues efficiently.

- You want consistent labels, priorities, and acceptance criteria.

## Label Taxonomy

| Dimension | Examples |
|-----------|----------|
| Type | `type: bug`, `type: feature`, `type: chore`, `type: docs` |
| Priority | `priority: critical`, `priority: high`, `priority: low` |
| Area | `area: api`, `area: ui`, `area: auth`, `area: infra` |
| Status | `status: needs-repro`, `status: blocked`, `status: in-progress` |

## Workflow

### 1. Triage quickly

- Classify: bug, feature, question, or chore?

- Assign type and area labels immediately.

### 2. Require minimum info

- Bug: repro steps, expected vs actual behavior, environment/version.

- Feature: problem to solve, success criteria, constraints.

- Close if not actionable after 14 days with a polite note.

### 3. Labeling system

- Apply type, priority, area, and status labels.

- Use priority labels consistently: `critical` = production down, `high` = significant user impact.

### 4. Definition of done

- Write acceptance criteria before implementation starts.

- Include: tests required, docs required, rollout notes.

### 5. Planning link

- Assign to milestone or project board.

- Add to sprint backlog with effort estimate (T-shirt size or story points).

## Self-check

- [ ] Issue classified and labeled (type + area).

- [ ] Minimum info present (repro steps for bugs; success criteria for features).

- [ ] Acceptance criteria written before work starts.

- [ ] Priority assigned with rationale.

- [ ] Linked to milestone or project board.

## Outputs

- Issue template checklist.

- Label taxonomy proposal.

- Triage workflow (fast + deep triage).
