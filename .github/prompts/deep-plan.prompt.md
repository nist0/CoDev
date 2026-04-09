---
name: deep-plan
description: "Elite planning entry point: runs a mandatory brainstorm (≥ 3 scored options), produces a ranked implementation plan, and emits a GitHub issue draft with full sub-task checklist — for any domain."
agent: plan
argument-hint: "goal=<what you want to build or fix> [constraints=<time/tech/scope>]"
---

## Deep Planning — Brainstorm → Plan → Issue with Sub-tasks

You are running as the **plan** agent with the **Innovator** brainstorming procedure.

Apply the procedure from `.github/skills/elite-brainstorming/SKILL.md`.
Apply the procedure from `.github/skills/github-work-management/SKILL.md`.

---

## Phase 1 — Brainstorm (mandatory, non-skippable)

Before producing any plan, generate a scored option portfolio.

### 1.1 Frame the decision

State explicitly:

- **Objective**: what does success look like, measurably?
- **Constraints**: tech stack, time budget, team size, non-negotiables.
- **Assumptions**: list each; flag confidence (high / medium / low).
- **Success metric**: single falsifiable statement (e.g. "p99 latency < 200 ms at 2× current load").

### 1.2 Generate ≥ 3 options (safe / adjacent / bold)

| # | Option | Risk | Reversibility | EV (0-10) | Feasibility (0-10) |
|---|--------|------|---------------|-----------|--------------------|
| A | Safe — improve what exists | Low | High | | |
| B | Adjacent — apply proven pattern from nearby domain | Medium | Medium | | |
| C | Bold — non-obvious high-upside approach | High | Low | | |

For each option apply:

- **Inversion**: how does this fail catastrophically?
- **Pre-mortem**: if it fails after 4 weeks, what was the most likely cause?
- **Kill criteria**: what measurable signal would cause us to abandon it?

### 1.3 Select finalist

State the chosen option and the rationale (≤ 3 sentences). This becomes `## Technical approach` in the issue.

---

## Phase 2 — Implementation plan

With the finalist confirmed, produce a numbered plan:

```markdown
## Plan: <goal>

### Assumptions
- <explicit assumption 1>
- <explicit assumption 2>

### Files affected
| File | Action | Change description |
|------|--------|--------------------|
| path/to/file.ext | modify | <what and why> |
| path/to/new-file.ext | create | <what and why> |

### Steps
1. <exact action> → `path/to/file.ext` → verifiable outcome: <how to confirm>
2. <exact action> → ...

### Risks
| Step | Risk | Mitigation |
|------|------|-----------|
| 2 | Migration may corrupt existing data | Dry-run on staging first |

### Acceptance criteria
- [ ] <falsifiable criterion 1>
- [ ] <falsifiable criterion 2>

### Verification
1. `<exact command>` exits 0
2. `<second command / CI check>` passes
```

---

## Phase 3 — GitHub issue draft (emit as copy/paste-ready block)

Emit the full issue body (ready for `gh issue create --body-file`):

```markdown
## Summary
<Why this work is needed; what problem it solves.>

## Technical approach
<Brainstorm finalist rationale from Phase 1.3. Options considered: A (safe), B (adjacent), C (bold). Chose B because ....>

## Files to modify
- `path/to/file.ext` — what change and why

## Sub-tasks
<!-- Inline sub-tasks (≤1 day each); for multi-PR work open child issues -->
- [ ] Sub-task 1: <action> (`path/to/file.ext`)
- [ ] Sub-task 2: <action>
- [ ] Sub-task 3: tests + validation
- [ ] Sub-task 4: PR review + merge

## Acceptance criteria
- [ ] <verifiable criterion 1>
- [ ] <verifiable criterion 2>

## Verification steps
1. `<exact command>` exits 0
2. `<second check>`

## Progress log
<!-- Append dated entries as work evolves -->
<today> — Issue created from /deep-plan output. Brainstorm completed: options A/B/C scored; finalist: <option>.
```

---

## Delegation chain

| Task | Owner | Trigger |
|------|-------|---------|
| Brainstorm portfolio review | Innovator | Phase 1 is ambiguous or needs deeper ideation |
| Implementation | implement agent | Plan + issue accepted by user |
| PR review | reviewer agent | Branch pushed, CI green |
| Issue + project tracking | Delivery Lead | Any multi-day / multi-PR scope |
