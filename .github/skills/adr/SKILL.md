---
name: adr
description: Architecture Decision Records -- structured context, options, decision, consequences, and follow-up tasks.
argument-hint: "[decision-title] [stakeholders]"
user-invocable: true

disable-model-invocation: false
---

# ADR (Architecture Decision Records) (Elite)

## When to use

- You need to record an architectural decision with context and tradeoffs.

- You want traceability of "why" a choice was made over time.

- You are making a decision that affects: API boundaries, data models, infra patterns, security posture, or team workflows.

## Procedure

### 1. Define decision scope

- What **decision** is being made? (one sentence)

- What **is impacted**? (systems, services, teams, contracts)

- Who are the **stakeholders**? (who must review and approve?)

- What is the **decision deadline**? (when must this be resolved?)

### 2. Capture context

- What **constraints** make this decision necessary? (technical, business, compliance)

- What are the **goals** the decision must support?

- What has already been tried or ruled out?

### 3. Compare options

For each option:

| Option | Description | Pros | Cons | Risk | Cost |
|--------|-------------|------|------|------|------|
| A | ... | ... | ... | ... | ... |
| B | ... | ... | ... | ... | ... |

- Include the **status quo** (do nothing) as an explicit option.

- Include the **reversibility** of each option (easy to undo vs hard to change).

### 4. Record the decision

```markdown
## Decision

We will adopt **Option [X]** because:
- <primary reason>
- <secondary reason>

This decision supersedes: [ADR-NNN if applicable]
```

### 5. Document consequences

- **Positive consequences**: what this enables.

- **Negative consequences / trade-offs**: what we accept.

- **Risks**: what could go wrong and mitigations.

### 6. Define follow-up actions

| Action | Owner | Due | Linked issue |
|--------|-------|-----|--------------|
| Implement X | @person | YYYY-MM-DD | #N |
| Update docs | @person | YYYY-MM-DD | #N |

### 7. File the ADR

- File as `docs/decisions/adr-NNN-<kebab-title>.md`.

- Link from `docs/README.md` and related issues/PRs.

- Tag the PR that introduces this ADR with `type:architecture`.

## ADR template

```markdown
# ADR-NNN: <Title>

**Status**: proposed | accepted | superseded | deprecated
**Date**: YYYY-MM-DD
**Stakeholders**: @person1, @person2

## Context
<constraints and goals>

## Options considered
| Option | Pros | Cons | Risk |

## Decision
<chosen option and rationale>

## Consequences
- Positive: ...
- Negative: ...
- Risks: ...

## Follow-up actions
| Action | Owner | Due |
```

## Self-check

- [ ] Decision scope is one sentence (not vague).

- [ ] At least 2 options compared (including status quo).

- [ ] Reversibility noted for each option.

- [ ] Consequences include both positive and negative.

- [ ] Follow-up actions have owners and due dates.

- [ ] ADR filed in `docs/decisions/` and linked from issues/PRs.

## Outputs

- ADR document (copy/paste-ready Markdown).

- Options comparison table.

- Follow-up actions with owners.
