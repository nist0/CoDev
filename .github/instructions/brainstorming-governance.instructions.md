---
name: "Brainstorming Governance"
description: "Mandatory brainstorm-first gate for all non-trivial tasks: require elite ideation quality, scored option portfolio, execution handoff, and named specialist reviews."

applyTo: "**"
---

# Brainstorming Governance

## Mandatory brainstorm-first gate

Brainstorming is **not opt-in**. It is the **required first phase** of any non-trivial task.

**Non-trivial threshold** -- this gate applies when ANY of the following is true:

- The task touches more than one file.

- The task introduces a new pattern, abstraction, or architectural concept.

- The task has user-facing or API-contract impact.

- The task has performance, security, or reliability implications.

- The task has an implementation duration > 30 minutes.

**Exempt tasks** (skip the gate only for these):

- Single-file typo or whitespace fix.

- Doc-only rewording with no structural change.

- Plain config toggle with zero logic change.

- Trivially reversible one-liner with no downstream effects.

**Gate enforcement**: Before creating any GitHub issue, opening any branch, or writing any code, produce a structured brainstorm output (>= 3 scored options). Only then proceed to issue creation.

## Asset-layer separation (non-duplication contract)

This framework separates concerns across three layers -- never duplicate policy between them:

| Layer | Asset | Role |
|---|---|---|
| **Procedure** | `elite-brainstorming` skill (`SKILL.md`) | Step-by-step how-to: framing, scoring, portfolio, spike plan |
| **Entry point** | `brainstorm` prompt | User-facing invocation, input gathering, output format |
| **Governance** | this instruction | Invariants that apply to *every* brainstorming session; enforces verdict format, portfolio shape, and handoff contract |

> **Rule**: if a brainstorming procedure detail belongs in the skill, do not repeat it here. This instruction enforces *invariants*, not steps.

## Governance invariants

- Require explicit objective, constraints, assumptions, and success metric before ideation begins.

- Produce a balanced option portfolio (safe, adjacent, bold) before selecting finalists.

- For finalists, require falsifiable hypothesis, evidence threshold, and kill criteria.

- Convert output into issue-ready tasks with owner agent, dependencies, acceptance criteria, and verification steps.

- Include GitHub project Kanban mapping for each task.

- Specialist review lines **must** start with `(Agent: <name>)` and include verdict (`approved` or `rework required`).

- For `rework required`, include exact gap and closure evidence -- no open-ended rework.

- Produce one brainstorming summary issue draft including:

  - all participating agents

  - key exchanges and decisions

  - shortlisted options and rationale

  - resulting tasks and project mapping

## Verdict contract (canonical tokens)

All agents producing reviews in a brainstorming session **must** use these exact tokens -- no variations:

```text
(Agent: <name>) approved -- <one-line rationale>
(Agent: <name>) rework required -- <exact gap> | closure evidence: <what must be shown>
```

Examples:

```text
(Agent: Reviewer) approved -- hypothesis is falsifiable; kill criteria are measurable.
(Agent: PromptSmith) rework required -- kill criteria missing for Option A | closure evidence: add explicit stop-condition metric before merge.
```

## Ideation quality checklist

Before presenting options, verify:

- [ ] At least one "safe" option (low risk, proven pattern)

- [ ] At least one "adjacent" option (moderate risk, emerging practice)

- [ ] At least one "bold" option (high risk, transformative potential)

- [ ] Each option has a named owner agent

- [ ] Each finalist has a falsifiable hypothesis and measurable success criterion

- [ ] Kill criteria defined: what signal would cause us to abandon this option?

Example: option portfolio entry
---

```markdown
### Option B -- Event-driven migration (adjacent)
**Hypothesis**: Migrating to event sourcing will reduce write latency by 40% under peak load.
**Evidence threshold**: p99 write latency < 80 ms at 2× current peak in load test.
**Kill criteria**: If after 2-week spike the p99 write latency does not improve by >=30%, abandon.
**Owner agent**: `engineering.backend-dotnet`
**Acceptance criteria**: Load test passes; schema migration rollback tested; no data loss in chaos test.
```

---

## U+1F3C6 Elite Section -- Top 5% Brainstorming Practices

- **Assumption mapping**: Before scoring options, list all assumptions made and assign confidence levels (high/medium/low). Low-confidence assumptions must become spikes before committing.

- **Reversibility bias**: Prefer reversible options over irreversible ones at equal expected value. Document irreversible consequences explicitly in the option entry.

- **Devil's advocate round**: After producing finalists, require one agent to argue the strongest case *against* each finalist. If no strong counter-argument exists, the option is likely underspecified.

- **Spike-then-decide pattern**: For high-uncertainty options, define a time-boxed spike (1-3 days) that produces a concrete artifact (benchmark, PoC, prototype) before committing to full implementation.

- **Innovation accounting**: Track brainstorming outcomes across sessions. Did shortlisted ideas get implemented? What was the actual outcome vs. the hypothesis? Feed back into future sessions to calibrate confidence.
