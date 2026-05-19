---
name: codev-update
description: Guided CoDev submodule update — sync after git submodule update, re-run bootstrap, validate, and commit.
agent: CoDev Consumer

## argument-hint: "[target-ref: main|<commit-sha>]"

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

# CoDev Update — Guided Sync

Walk me through updating the CoDev submodule to the latest version (or a specific ref).

Input (use default if not provided):

- target-ref: ${input:target-ref:origin/main}

## What to produce

For each step, show:

1. The **exact command** to run (bash + PowerShell variants).

2. **What changes** — which files are updated.

3. **Verify** — exact command and expected output.

4. **Rollback** — how to revert to the previous pinned commit.

## Steps to cover

1. Fetch the latest commits inside the submodule.

2. Checkout the target ref (`git checkout ${input:target-ref}`).

3. Run `codev update` to re-sync bootstrap artefacts.

4. Check for breaking changes in the CoDev changelog (link to release notes).

5. Run `validate-route-smoke.py` — if it fails, diagnose before committing.

6. Commit the updated submodule pointer + changed bootstrap artefacts.

7. Push and confirm CI passes.

## Failure diagnosis

If `validate-route-smoke.py` fails after update:

- Show which phrases failed and what was expected vs. actual.

- Suggest: check CoDev CHANGELOG for routing changes, pin to previous commit if blocking.

## Self-check at the end

- [ ] Submodule pointer updated in `.gitmodules` / parent repo

- [ ] `codev update` ran without errors

- [ ] `validate-route-smoke.py` passed

- [ ] `codev-lock.json` updated (lockfile mode) or symlinks verified (symlink mode)

- [ ] Commit pushed; CI green

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **CoDev Consumer** | always — submodule update | *(this prompt)* | Submodule updated to target ref, codev update run, artefacts synced |
| 2 | **Router** | `validate-route-smoke.py` fails after update | `/route-miss` | Root cause diagnosed, fix applied or submodule pinned to safe commit |
| 3 | **Delivery Lead** | update validated | `/pr-review` | PR merged, submodule pointer committed, CI green |
