---
name: codev-contribute
description: Guided upstream contribution to CoDev -- issue, fork, branch, fix, PR, review, and post-merge sync.
agent: CoDev Consumer

argument-hint: "[type: bug|enhancement|new-skill|new-agent] [issue-title: <short description>]"
---

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

# CoDev Contribute -- Guided Upstream PR

Walk me through contributing a change back to the CoDev repository.

Inputs:

- type: ${input:type:bug}

- issue-title: ${input:issue-title:describe what you want to fix or add}

## Decision gate (run first)

Before anything else, determine whether this change belongs upstream or in `codev-overrides/`:

| Question | Yes | No |
| --- | --- | --- |
| Would other CoDev consumers benefit from this change? | Continue | Use `codev-overrides/` instead |
| Is it specific to my host project's domain? | Use `codev-overrides/` | Continue |
| Does it introduce a breaking change to existing skills? | Open RFC issue first | Continue |

## What to produce

For each step, show exact commands (bash + PowerShell) + expected outputs.

## Steps to cover

1. **Open a GitHub issue** on `nist0/CoDev` with:

   - What / Why / Acceptance criteria

   - Proposed approach (required for new capabilities)

   - Use `--body-file` pattern (never `--body "..."`)

2. **Fork** `nist0/CoDev` and add as a remote inside `tools/codev/`.

3. **Branch** from `origin/main` using `<type>/<slug>` convention.

4. **Implement** the change following CoDev conventions:

   - Skills: SKILL.md + examples/README.md + self-check + elite section

   - Routing: all 4 YAMLs updated atomically

   - README: tables updated if new assets added

5. **Validate locally** -- all 5 validators must pass (show exact commands + expected exit codes).

6. **Open PR** to `nist0/CoDev` via `--body-file` with smoke-test phrases, verification commands, `Closes #N`.

7. **Address review** -- respond to `(Agent: Reviewer) rework required` with exact gap closure.

8. **Post-merge sync** -- update the submodule pointer in the host repo + run `codev update` + verify + commit.

## Self-check at the end

- [ ] GitHub issue opened on `nist0/CoDev` and linked in PR

- [ ] All 5 validators passed locally

- [ ] PR body uses `--body-file` (no corrupted backtick spans)

- [ ] Smoke-test phrases added / updated for routing changes

- [ ] README updated for new agents/skills/prompts

- [ ] Post-merge: submodule updated, `validate-route-smoke.py` passed, committed, CI green

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **CoDev Consumer** | always -- upstream contribution | *(this prompt)* | Issue opened, fork created, branch branched, change implemented |
| 2 | **Router** | routing or matrix changes made | `/route <smoke-test phrase>` | All 5 validators pass, smoke-test phrases updated |
| 3 | **Reviewer** | PR opened on nist0/CoDev | `/pr-review` | (Agent: Reviewer) approved verdict recorded |
| 4 | **CoDev Consumer** | PR merged upstream | Post-merge sync steps | Submodule pointer updated, `validate-route-smoke.py` passes, CI green |
