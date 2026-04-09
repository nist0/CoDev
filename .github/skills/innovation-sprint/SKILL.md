---
name: innovation-sprint
description: Short structured ideation sprint — constrained diverge, cluster, score, falsifiable shortlist, and spike plans.
argument-hint: "[problem] [constraints] [success-criteria]"
user-invocable: true
disable-model-invocation: false
---

# Innovation Sprint (Elite)

## When to use

- You need new ideas or alternative designs in a bounded timebox.
- You want a structured ideation session with scored, falsifiable outputs.
- You want to feed results into a full `elite-brainstorming` session or a project plan.

## Procedure

### 1. Define the problem and constraints

Before generating ideas:

- **Objective**: what outcome must the solution achieve?
- **Constraints**: what is non-negotiable (time, budget, tech stack, compliance)?
- **Assumptions**: what are we assuming is true? (Make explicit.)
- **Success metric**: how will we know we picked the right idea?
- **Kill criteria**: what would make us stop and restart?

### 2. Apply top-tier reasoning before ideating

Use at least 2 of:

- **Inversion**: what would guarantee failure? Avoid those properties.
- **Reference-class**: what have similar projects done? What succeeded?
- **Second-order**: what happens after the obvious solution? Second consequences?
- **Pre-mortem**: 12 months from now, the project failed. Why?

### 3. Generate 8–12 ideas (no filtering)

- Time-box this step to 15 minutes.
- Quantity over quality; defer judgment.
- Mix safe, adjacent, and bold options.
- Each idea: 1–2 sentences only.

### 4. Cluster and select top 3

- Group similar ideas into themes.
- Score each theme (not each idea) on:

| Theme | Expected value (EV) | Feasibility | Confidence | Reversibility |
|-------|---------------------|-------------|------------|---------------|
| ... | 1–5 | 1–5 | 1–5 | 1–5 |

Select the top 3 highest-scoring themes.

### 5. Produce falsifiable shortlist

For each of the top 3:

```text
Option: <name>
Hypothesis: We believe <option> will achieve <outcome> because <reasoning>.
Evidence threshold: We will be confident if <measurable signal>.
Kill criteria: We will stop if <condition>.
Rollback: If this fails, we revert to <alternative>.
Spike plan:
  - Step 1: ...
  - Step 2: ...
  - Time-box: <1–4 hours>
  - Output: <what we will have at the end>
```

### 6. Produce portfolio balance check

| Mix | Target | Actual |
|-----|--------|--------|
| Safe (low risk, proven) | 1 | |
| Adjacent (moderate risk, adjacent tech) | 1 | |
| Bold (high risk, high upside) | 1 | |

If all 3 shortlisted options are in the same category: force diversity.

### 7. Hand off to delivery

- Convert shortlisted options to GitHub issues (use `github-work-management` skill).
- Assign a spike owner and time-box.
- Schedule a readout after the spike.

## Self-check

- [ ] Problem, constraints, success metric, and kill criteria defined before ideating.
- [ ] At least 2 top-tier reasoning techniques applied.
- [ ] 8–12 ideas generated before filtering.
- [ ] Top 3 scored on EV, feasibility, confidence, reversibility.
- [ ] Each option has a falsifiable hypothesis and evidence threshold.
- [ ] Portfolio mix includes safe/adjacent/bold.
- [ ] Spike plans are ≤ 4 hours each.

## Outputs

- Idea list (raw, unfiltered).
- Scored cluster table.
- Top 3 shortlist with falsifiable options and spike plans.
- Portfolio balance check.
- GitHub issue set for spikes.
