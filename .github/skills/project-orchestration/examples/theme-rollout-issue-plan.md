# Theme Rollout Issue Plan

## Goal

Extend and govern theme coverage with no duplication and strict instruction compliance.

## Epics

1. Docs & Diagram Ops theme coverage

2. Deep standards uplift for existing expert themes

3. Governance enforcement for routing and instructions

4. Review and acceptance gates

## Issue-ready tasks

### EPIC 1 — Docs & Diagram Ops

- **Issue 1.1**: Add diagram tooling skill + examples

  - Assigned agent: `engineering.delivery-lead`

  - Scope: create/maintain `diagram-tooling` assets

  - Acceptance: skill exists, examples exist, lint passes

- **Issue 1.2**: Add markdown doc operations skill + examples

  - Assigned agent: `engineering.delivery-lead`

  - Scope: create/maintain `markdown-docops` assets

  - Acceptance: no-duplication procedure included, lint passes

- **Issue 1.3**: Add prompts for diagram and markdown operations

  - Assigned agent: `engineering.delivery-lead`

  - Scope: `diagram-ops`, `markdown-ops`

  - Acceptance: prompt metadata valid, output formats deterministic

### EPIC 2 — Routing Integration

- **Issue 2.1**: Wire docs-system aliases and domain keywords

  - Assigned agent: `engineering.router`

  - Scope: `routing/aliases.yaml`, `routing/domains.yaml`

  - Acceptance: natural language phrases map to docs-system reliably

- **Issue 2.2**: Wire matrix rules for new prompts and skills

  - Assigned agent: `engineering.router`

  - Scope: `routing/matrix.yaml`

  - Acceptance: capability + domain and fallback routes both valid

### EPIC 3 — Governance Enforcement

- **Issue 3.1**: Add customization governance instruction

  - Assigned agent: `engineering.delivery-lead`

  - Scope: `.github/instructions/` governance file

  - Acceptance: mandates no-duplication and routing end-to-end updates

- **Issue 3.2**: Update PromptSmith + scaffold prompt requirements

  - Assigned agent: `promptsmith`

  - Scope: `promptsmith.agent.md`, `new-theme-pack.prompt.md`

  - Acceptance: routing updates required for all new themes

### EPIC 4 — Final Review

- **Issue 4.1**: Cross-theme review and gap closure

  - Assigned agent: `reviewer`

  - Scope: all modified assets

  - Acceptance: explicit verdict per task (approved/rework)

## Suggested PR batches

1. **PR A**: New skills/prompts for docs + diagram ops

2. **PR B**: Routing integration updates

3. **PR C**: Governance enforcement updates

4. **PR D**: Final polish and consistency pass

## Kanban policy

- Columns: Backlog -> Ready -> In Progress -> In Review -> Done

- WIP limits: In Progress <= 4, In Review <= 3

- Done criteria: verification evidence attached + review verdict approved
