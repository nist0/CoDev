# github-work-management -- Examples

## Copy/paste issue template

```markdown
## Context

<Why this work is needed. Link to epic #X or stakeholder request.>

## Scope

**In scope:**

- <item 1>
- <item 2>

**Out of scope:**

- <item>

## Assigned specialist

@<agent-name or team-member>

## Dependencies

- Blocks: #<issue-number>
- Blocked by: #<issue-number>

## Acceptance criteria

- [ ] <verifiable criterion -- observable outcome, not implementation detail>
- [ ] <verifiable criterion>

## Verification steps

1. `<local command to run>`
2. CI check: `<job name>` must be green.
3. <manual step if needed>

## Definition of Done

- [ ] Code reviewed and approved (reviewer verdict: approved)
- [ ] All acceptance criteria checked off above
- [ ] CI green: lint + unit tests + security scan
- [ ] Docs updated if public behavior changed
- [ ] Issue number linked in PR body (`Closes #<N>`)
- [ ] PR merged; branch deleted

## Review verdict

<!-- filled by reviewer after PR review -->

approved | rework required

<!-- if rework required, list exact gaps: -->
```

## Example -- feature issue

```markdown
## Context

Routing matrix does not cover the `research.brainstorming` capability when the domain is
`engineering.devops-cloud`. Users using `/route I need brainstorming for my k8s setup` get
no agent recommendation. Refs epic #10.

## Scope

**In scope:**

- Add a matrix rule for `research.brainstorming` + `engineering.devops-cloud`.
- Add a smoke test phrase covering this combo.

**Out of scope:**

- Changes to domain keywords or capability definitions.

## Assigned specialist

Innovator agent

## Dependencies

- Blocks: #31 (release v1.2.0)
- Blocked by: none

## Acceptance criteria

- [ ] `routing/matrix.yaml` contains a rule for `research.brainstorming` + `engineering.devops-cloud`.
- [ ] `routing/route-smoke-tests.yaml` includes a phrase that matches this combo and passes.
- [ ] `python scripts/validate-route-smoke.py` exits 0.

## Verification steps

1. `python scripts/validate-route-smoke.py`
2. `python scripts/validate-customization-registry.py`
3. Manual: run `/route I need brainstorming for my k8s deployment` and confirm Innovator is recommended.

## Definition of Done

- [ ] Code reviewed and approved
- [ ] All acceptance criteria checked off
- [ ] CI green
- [ ] README updated if new capability is surfaced
- [ ] Closes #28; PR merged

## Review verdict

approved
```

## Example -- bug fix issue

```markdown
## Context

`validate-route-smoke.py` crashes with `KeyError: 'agent'` when a matrix rule omits the
`agent` key. Reported in #33.

## Scope

**In scope:** Defensive check in the validation script; clear error message pointing to the
offending rule.

**Out of scope:** Changing matrix schema or adding new rules.

## Assigned specialist

Reliability agent

## Dependencies

- Blocks: none
- Blocked by: none

## Acceptance criteria

- [ ] Running the script with a matrix rule missing `agent` prints a human-readable error and exits 1.
- [ ] A regression test (or inline test phrase in the script) covers this scenario.

## Verification steps

1. Temporarily remove `agent` from a matrix rule; run `python scripts/validate-route-smoke.py`.
2. Confirm exit code 1 and error message includes the offending rule ID.
3. Restore the rule; confirm exit code 0.

## Definition of Done

- [ ] Code reviewed and approved
- [ ] Regression test added
- [ ] CI green
- [ ] Closes #33; PR merged

## Review verdict

approved
```

## Label taxonomy reference

```text
type:enh        type:fix        type:chore      type:docs       type:epic
area:routing    area:agents     area:skills     area:infra      area:ci
priority:p0     priority:p1     priority:p2
status:ready    status:blocked  status:in-review  status:rework
```

## Kanban setup -- GitHub CLI

```bash
# Create project
gh project create --owner @me --title "CoDev Sprint-01"

# Add columns (adjust project number after creation)
gh project field-create <project-number> --owner @me \
  --name "Status" --data-type SINGLE_SELECT \
  --single-select-options "Backlog,Ready,In Progress,In Review,Done"
```

## Progress rollup format

```markdown
## Sprint <N> -- Progress Rollup (<YYYY-MM-DD>)

**Done**: <count> -- #X title, #Y title
**In Progress**: <count> -- #Z title (ETA: <date>)
**Blocked**: <count> -- #W title (blocked by: #V, owner: @<person>)
**Scope added**: <count> -- #A title
**Scope removed / deferred**: <count> -- #B title (reason: <one-liner>)

### Risks

- <risk> -- mitigation: <action>, owner: @<person>

### Next cycle priorities

1. #<issue> -- <title>
2. #<issue> -- <title>
```
