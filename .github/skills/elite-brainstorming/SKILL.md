---
name: elite-brainstorming
description: High-rigor brainstorming playbook that converts ideas into testable bets, delegated execution, and named specialist reviews.
argument-hint: "[objective] [constraints]"
user-invocable: true

disable-model-invocation: false
---

# elite-brainstorming Skill

## When to use

- A user asks for brainstorming with implementation intent.

- You must turn ideation into issue-ready execution quickly.

- You need expert-level decision quality (not generic idea lists).

## Procedure

### 1. Frame decision quality first

- Define **objective** (measurable success), **scope**, **constraints**, and **success metric**.

- Record all **assumptions** and the evidence that would invalidate each one.

- State what is explicitly **out of scope** to prevent scope creep.

### 2. Generate option portfolio (8–12 ideas)

- Produce ideas across distinct archetypes (no two ideas with the same mechanism):

  - Incremental, contrarian, platform/leverage, automation, UX/distribution, moat, operational excellence, bold/moonshot.

- One-liner per idea: no elaboration at this stage.

- No filtering yet — volume first.

### 3. Apply top-tier reasoning before scoring

For each candidate:

- **Inversion**: how does this fail catastrophically?

- **Reference-class thinking**: where has a similar bet been made? Outcome?

- **Second-order effects**: what does this change 6 months from now?

- **Pre-mortem**: if this fails in 3 months, what was the most likely cause?

- **Reversibility**: one-way door (hard to undo) or two-way door (easy to reverse)?

### 4. Score and filter

Score each idea:

| Dimension | Score 0–10 |
|-----------|----------|
| EV (user/business value) | |
| Feasibility (time/cost/dependency realism) | |
| Confidence (how certain are we?) | |
| Reversibility (1 = one-way, 10 = two-way) | |

Keep top 3; discard weak options with explicit one-line reason.

### 5. Build a portfolio mix

- 1 **safe bet**: high confidence, lower EV — can ship now.

- 1 **adjacent bet**: medium confidence, medium EV — spike in 1 week.

- 1 **bold bet**: lower confidence, high EV — spike in 1–2h to validate.

### 6. Make each shortlisted option falsifiable

For each option:

- **Hypothesis**: `If we do X, we expect Y within Z`.

- **Evidence threshold**: what signal confirms the hypothesis?

- **Kill criteria**: what result triggers abandonment?

- **Rollback posture**: how to reverse if it fails.

- **1–2h spike plan**: steps, expected output, decision the spike enables.

### 7. Convert to delivery artifacts

- Create atomic issue-ready tasks: owner agent, dependencies, acceptance criteria, verification steps.

- Map each task to Kanban column (Backlog / Ready / In Progress / In Review / Done).

### 8. Enforce review governance

- Every specialist review line **must** start with `(Agent: <name>)`.

- Verdict: `approved` or `rework required`.

- `rework required` → exact gap + closure evidence required.

### 9. Publish brainstorming continuity ticket

Produce one issue body:

- Participants (agents involved).

- Key exchanges and decisions.

- Shortlisted options and ranking rationale.

- Resulting tasks and Kanban mapping.

## Self-check

- [ ] Objective, constraints, success metric, and assumptions stated.

- [ ] 8–12 ideas generated across distinct archetypes.

- [ ] Top-tier reasoning (inversion, reference-class, second-order, pre-mortem) applied.

- [ ] Top 3 scored on EV, feasibility, confidence, reversibility.

- [ ] Portfolio has safe + adjacent + bold bet.

- [ ] Each option has: hypothesis, evidence threshold, kill criteria, rollback, spike plan.

- [ ] Tasks are atomic and have owner + acceptance criteria + verification.

- [ ] Specialist review lines use `(Agent: <name>)` format.

- [ ] Brainstorming continuity ticket captures all agents and key decisions.

## Deliverables

- Objective and assumptions ledger.

- Idea portfolio and scored shortlist.

- Spike plans with kill criteria.

- Issue-ready execution tasks.

- Named specialist review plan.

- Brainstorming summary ticket draft.
