---
name: codev-init
description: Guided CoDev submodule initialization — step-by-step with mode detection, validation, and commit.
agent: CoDev Consumer

## argument-hint: "[strategy: extend|override] [submodule-path: tools/codev]"

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

# CoDev Init — Guided Bootstrap

Walk me through initializing CoDev as a Git submodule in this repository.

Inputs (use defaults if not provided):

- strategy: ${input:strategy:extend}

- submodule-path: ${input:submodule-path:tools/codev}

## What to produce

For each step, show:

1. The **exact command** to run (bash + PowerShell variants where they differ).

2. **What happens** — what files are created/modified.

3. **Verify** — exact command and expected output to confirm success.

4. **Rollback** — how to undo if it fails.

## Steps to cover

1. Add the submodule (`git submodule add` + `git submodule update --init --recursive`).

2. Run `codev init` with the chosen strategy.

3. Detect and confirm bootstrap mode (symlink vs. lockfile) — explain implications of each.

4. Run `validate-route-smoke.py` and confirm expected output.

5. Commit all bootstrap artefacts with a conventional commit message.

6. Push and confirm CI passes.

## Self-check at the end

- [ ] `validate-route-smoke.py` passed (all cases)

- [ ] `codev.json` committed and valid

- [ ] Symlinks verified OR `codev-lock.json` committed (depending on mode)

- [ ] Pre-commit hook active

- [ ] No managed files committed directly (only `codev-overrides/`)

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **CoDev Consumer** | always — submodule bootstrap | *(this prompt)* | CoDev submodule added, codev init run, bootstrap artefacts committed |
| 2 | **Router** | bootstrap complete | `/route <domain phrase>` | Smoke test passes, capability+domain correctly resolved |
| 3 | **Delivery Lead** | ready to push | `/pr-review` | PR merged, CI green, no managed files overwritten |
