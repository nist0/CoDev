---
name: cli-platform-init
description: "Guided CoDev submodule bootstrap for a .NET CLI platform repo — add submodule, codev init with extend strategy, author codev-overrides/ stub, verify, and commit. Phase 1 of the CLI platform onboarding workflow."
agent: "CLI Platform Onboarder"

## argument-hint: "repo=<clone-url-or-local-path> branch=<feat/bootstrap-codev>"

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Apply procedures from `.github/skills/cli-platform-bootstrap/SKILL.md` and `.github/skills/codev-submodule/SKILL.md`.

Inputs:

- repo: ${input:repo:path to the already-cloned repo root, or a clone URL}

- branch: ${input:branch:feat/bootstrap-codev}

Single source of truth:

- Bootstrap procedure and command sequence are defined in `cli-platform-bootstrap` and `codev-submodule`.

- Do not restate or redefine those steps here.

Execution contract:

1. Run Phase 1 bootstrap using the linked skills.

2. Show command, effect, verification, and rollback for each executed step.

3. Validate route smoke and customization registry before phase completion.

4. Emit phase status with outputs, blockers, and the next command.

5. Transition to `/cli-platform-analyze` after successful bootstrap.

Required outputs:

- Step-by-step execution log

- Verification results

- Phase status block

- Explicit next action

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **CLI Platform Onboarder** | always — Phase 1 Bootstrap | *(this prompt)* | All 7 bootstrap steps verified, `validate-route-smoke.py` passes, CI green |
| 2 | **CLI Platform Onboarder** | Phase 1 complete | `/cli-platform-analyze` | docs/project-context.md produced and committed (Phase 2) |
| 3 | **CLI Platform Onboarder** | Phase 2 complete | `/cli-platform-task task=<assigned task>` | Task executed, PR open, CI green (Phase 3) |
