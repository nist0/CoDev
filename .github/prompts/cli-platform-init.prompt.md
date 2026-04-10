---
name: cli-platform-init
description: "Guided CoDev submodule bootstrap for a .NET CLI platform repo — add submodule, codev init with extend strategy, author codev-overrides/ stub, verify, and commit. Phase 1 of the CLI platform onboarding workflow."
agent: "CLI Platform Onboarder"
argument-hint: "repo=<clone-url-or-local-path> branch=<feat/bootstrap-codev>"
---

Apply procedures from `.github/skills/cli-platform-bootstrap/SKILL.md` and `.github/skills/codev-submodule/SKILL.md`.

Inputs:

- repo: ${input:repo:path to the already-cloned repo root, or a clone URL}
- branch: ${input:branch:feat/bootstrap-codev}

Act as a CLI Platform Onboarder and execute **Phase 1 (Bootstrap)** using the `cli-platform-bootstrap` skill.

## What to produce

For every step in the skill, show:

1. **Exact command** — PowerShell and bash variants where they differ.
2. **What happens** — which files are created or modified.
3. **Verify** — exact command and expected output to confirm success.
4. **Rollback** — exact command to undo if the step fails.

## Steps to cover

1. Clone the repo and create the feature branch (if not already done).
2. Add CoDev as a git submodule at `tools/codev`.
3. Run `codev init --strategy extend` — explain symlink vs lockfile mode implications.
4. Author the `codev-overrides/` stub and mandatory `README.md`.
5. Run `validate-route-smoke.py` and `validate-customization-registry.py`.
6. Commit all bootstrap artefacts with conventional commit message.
7. Push and confirm CI passes on the branch.

## After each verification passes, emit a step status

```text
Step N: <name>
Status: verified
Output: <file(s) created>
```

## When all steps are verified, emit the phase status block

```text
Phase: Bootstrap
Status: verified
Outputs: [tools/codev/, codev.json, codev-lock.json, codev-overrides/README.md, .pre-commit-config.yaml, .gitmodules]
Next action: /cli-platform-analyze repo-root=.
Blockers: none
```

Then automatically transition by invoking `/cli-platform-analyze`.

## Self-check at the end

- [ ] `validate-route-smoke.py` passed (all cases).
- [ ] `validate-customization-registry.py` passed (no errors).
- [ ] `codev.json` committed and valid.
- [ ] Symlinks verified OR `codev-lock.json` committed.
- [ ] Pre-commit hook active.
- [ ] `codev-overrides/README.md` committed with correct table structure.
- [ ] No managed `.github/` files overwritten.
- [ ] CI green on the pushed branch.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **CLI Platform Onboarder** | always — Phase 1 Bootstrap | *(this prompt)* | All 7 bootstrap steps verified, `validate-route-smoke.py` passes, CI green |
| 2 | **CLI Platform Onboarder** | Phase 1 complete | `/cli-platform-analyze` | docs/project-context.md produced and committed (Phase 2) |
| 3 | **CLI Platform Onboarder** | Phase 2 complete | `/cli-platform-task task=<assigned task>` | Task executed, PR open, CI green (Phase 3) |
