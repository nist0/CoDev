---
name: brainstorm
description: "Elite multi-agent brainstorming workflow with idea portfolio scoring, execution handoff, and governance artifacts."
agent: "Innovator"
argument-hint: "topic=<text> constraints=<text> success-metric=<text>"
---
Apply the procedure from `.github/skills/elite-brainstorming/SKILL.md`.

If `{{input}}` is empty, ask the user for all three inputs **in a single message** before starting the workshop:

1. **Topic / objective** — what decision or challenge to brainstorm (e.g. "how to reduce deploy time", "new feature ideas for X")
2. **Constraints** — budget, timeline, team size, tech, policy, or any hard limits
3. **Success metric** — how will you know the chosen option worked? (measurable signal)

If `{{input}}` is provided, extract topic, constraints, and success metric directly from it and proceed to the workshop.

Act as an Innovator and run an elite brainstorming workshop for: {{input}}

Use this workflow:

1. Clarify objective, constraints, and success metric (state assumptions explicitly).
2. Generate 12 ideas across varied archetypes (incremental, contrarian, platform, automation, UX, distribution, moat, operational excellence).
3. Apply top-tier practices:
   - first-principles decomposition
   - inversion (how this fails)
   - reference-class thinking (similar bets and outcomes)
   - second-order effects (what this changes later)
   - pre-mortem + key risk controls
   - expected-value thinking under uncertainty
   - confidence calibration (what would change your mind)
   - reversibility classification (one-way vs two-way door)
4. Remove weak options and keep the strongest 3.
5. Build a portfolio mix across the 3 options:
   - 1 safe bet
   - 1 adjacent bet
   - 1 bold bet
6. For each shortlisted option, define:
   - measurable hypothesis
   - evidence threshold
   - kill criteria
   - rollback posture
7. Convert the shortlist into delivery artifacts:
   - issue-ready tasks assigned to specialist agents
   - GitHub project Kanban placement per task
   - review plan with named specialist reviewers

Output format (strict):

- Objective + assumptions
- 12 ideas (one line each, no fluff)
- Top 3 shortlist, each with:
  - Value (user/business impact)
  - Feasibility (time/cost/dependency realism)
  - Risks (execution + adoption + technical)
  - Why now (timing edge)
  - EV score (0-10), confidence (0-10), reversibility (one-way/two-way)
  - Hypothesis + evidence threshold
  - Kill criteria (clear stop conditions)
  - Rollback posture
  - 1–2h spike plan (steps, expected evidence, decision after spike)
- Specialist dispatch map:
  - task
  - owner agent
  - dependencies
  - acceptance criteria
  - verification
- Specialist review plan:
  - each review line MUST start with `(Agent: <name>)`
  - include verdict (`approved` or `rework required`) and exact requested fix if rework
- Brainstorming ticket draft (single issue body):
  - context + participants (agents involved)
  - key exchanges and decisions
  - shortlisted options and rationale
  - tasks to open and project board status suggestions
- Final recommendation:
  - rank #1/#2/#3
  - explain trade-off in 3 bullets
  - define next 48h action plan

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Innovator** | always — ideation workshop | *(this prompt)* | 3-option portfolio produced with EV scores, kill criteria, and spike plans |
| 2 | **Project Orchestrator** | shortlist approved, ready for execution | `/project-dispatch` | Tasks decomposed with owners, AC, and GitHub issue-ready definitions |
| 3 | **Project Orchestrator** | tasks dispatched | `/project-governance` | Kanban board configured, review verdict table produced |
| 4 | **Innovator** | spike results available | Re-run `/brainstorm` with spike findings | Hypothesis confirmed or option killed based on evidence |
