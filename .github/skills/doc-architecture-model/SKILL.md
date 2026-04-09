---
name: doc-architecture-model
description: Propose or enforce a Documentation Architecture Model (DAM) — purpose-driven doc tree, audience clarity, ownership, and lint compliance.
argument-hint: "[repo] [doc-types]"
user-invocable: true
disable-model-invocation: false
---

# Documentation Architecture Model (DAM) (Elite)

## When to use

- Proposing or enforcing a documentation structure for the repo.
- Reviewing docs for consistency, purpose, and audience clarity.
- Auditing a `docs/` tree for coverage gaps and orphaned documents.

## Procedure

### 1. Identify doc categories needed

| Category | Purpose | Audience | Location |
|----------|---------|----------|----------|
| Architecture | System design, ADRs | Engineers, architects | `docs/architecture/` |
| Onboarding | Setup, team conventions, first PR | New contributors | `docs/onboarding/` |
| Runbooks | Operational procedures, incident response | SRE, on-call | `docs/runbooks/` |
| Reference | API specs, config, CLI docs | All engineers | `docs/reference/` |
| Decisions | ADRs, RFCs | All | `docs/decisions/` |

Map each doc to exactly one category. If a doc spans categories: split it.

### 2. Propose the `docs/` tree

```text
docs/
  architecture/
    overview.md           # System architecture
    decisions/            # ADRs (adr-NNN-<title>.md)
  onboarding/
    README.md             # First-time setup
    team-conventions.md   # Branch naming, PR, commit format
  runbooks/
    incident-response.md
    <service>-runbook.md
  reference/
    api.md
    configuration.md
  README.md               # Docs index (links to all categories)
```

### 3. Ensure every doc has: purpose, audience, owner

At the top of every doc file:

```markdown
<!-- purpose: <one sentence> -->
<!-- audience: <engineer | new-contributor | on-call | all> -->
<!-- owner: @<handle> -->
```

### 4. Audit existing docs

For each existing doc:

| Doc | Category | Purpose defined? | Audience defined? | Owner defined? | Linked from index? |
|-----|----------|-----------------|-------------------|---------------|-------------------|

Flag: orphaned docs (not linked), docs with no purpose, duplicate coverage.

### 5. Verify lint compliance

Run:

```bash
npx markdownlint-cli2 "docs/**/*.md"
```

Requirements:

- Headings: no skipped levels (`#` then `##`, never jumping to `###`).
- Code blocks: all fenced with language identifier.
- Links: all valid (run link-checker or `mlc`).
- Line length: ≤ 120 chars (soft rule).

### 6. Produce templates per doc type

Provide a copy/paste-ready template for each category (Architecture, Onboarding, Runbook, Reference, ADR).

See: `doc-qa` skill for ongoing lint automation.

## Self-check

- [ ] Every top-level category has a defined purpose and audience.
- [ ] Every doc maps to exactly one category.
- [ ] Every doc has purpose / audience / owner metadata.
- [ ] `docs/README.md` links to all categories.
- [ ] Orphaned docs flagged.
- [ ] Lint check passes (`markdownlint-cli2`).

## Outputs

- Proposed `docs/` tree (copy/paste-ready).
- DAM compliance audit table.
- Template per doc type (Architecture, Onboarding, Runbook, Reference, ADR).
- Lint configuration (`markdownlint.json`) recommendation.
