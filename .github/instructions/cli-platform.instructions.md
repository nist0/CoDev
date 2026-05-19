---
name: "CLI Platform — Working Standards"
description: "Mandatory working standards for the .NET CLI platform project: three-phase workflow enforcement, context discipline, extension conventions, and infra/CI authoring rules."

## applyTo: "**"

# CLI Platform — Working Standards

## Three-phase workflow (mandatory, non-negotiable)

Every working session on the CLI platform project **must** follow this sequence in order:

1. **Bootstrap** (once per repo clone): CoDev submodule added, `validate-route-smoke.py` passes, `codev-overrides/` stub committed. Entry point: `/cli-platform-init`.

2. **Analysis** (once per sprint, or after any major merge): `docs/project-context.md` produced and committed. Entry point: `/cli-platform-analyze`.

3. **Execution** (per task): `docs/project-context.md` preloaded before every task prompt. Entry point: `/cli-platform-task task="<description>"`.

Skipping any phase or executing them out of order is a process violation.

## Context discipline

- Always load `docs/project-context.md` as context before invoking `/cli-platform-task`.

- If `docs/project-context.md` is older than one sprint (or any section is stale), re-run `/cli-platform-analyze` before starting a new task.

- Never make assumptions about CI/CD patterns, Bicep resources, or CLI command conventions — always derive from `docs/project-context.md`.

- When `docs/project-context.md` is updated, commit the update in the same PR as the change that caused it.

## Test-before-implement gate (non-negotiable)

- The test plan (`/test-plan`) output must be reviewed before implementation begins.

- This is the mandatory `⏸ REVIEW CHECKPOINT` in `/cli-platform-task`.

- Regression tests must fail before the fix and pass after — this is not optional and is verified during PR review.

- All CI gates must be green before a PR is opened.

## Extension conventions

- **New CLI command**: add a corresponding entry in `docs/cli-reference.md` in the same PR.

- **New extension point or plugin hook**: update `docs/architecture/extension-points.md` in the same PR.

- **New infrastructure resource**: update the `## Infrastructure & Deployment Topology` section of `docs/project-context.md` in the same PR.

- **New secret referenced in a workflow**: add it to the secrets inventory before merging.

## codev-overrides/ discipline

- All project-specific CoDev assets (agents, skills, prompts, instructions) live in `codev-overrides/` — never edit CoDev-managed files under `.github/` directly.

- Every file added to `codev-overrides/` must have a corresponding row in `codev-overrides/README.md` (purpose, owner, last-reviewed date).

- New skills must include `examples/README.md` with at least one concrete example.

- Override agents must not duplicate responsibilities already covered by existing CoDev agents.

## GitHub workflow authoring rules

- All third-party actions must be pinned to a full SHA — never a mutable tag (e.g. `@v3`).

- `GITHUB_TOKEN` permissions must be declared at the job level, scoped to the minimum required.

- Use OIDC for cloud authentication — no long-lived credentials stored as secrets.

- New workflow files must pass `validate-customization-registry.py` before merging.

## Bicep / infrastructure authoring rules

- All Bicep changes must pass `bicep build --lint` before commit.

- Parameter files must exist for all environments (dev, staging, prod) — no partial configs.

- Any new Azure resource must include a diagnostic setting pointing to the Log Analytics workspace.

- Role assignments must use the principle of least privilege — no `Owner` or `Contributor` for workloads; prefer purpose-specific built-in roles.

## Branch and PR hygiene

- Always work on a feature branch: `feat/<slug>`, `fix/<slug>`, `chore/<slug>`.

- Never commit directly to `main`.

- Every PR must reference its closing issue (`Closes #N`) and pass all CI gates before merge.

- PR descriptions for infrastructure or CI changes must include the threat surface summary from `security.instructions.md`.
