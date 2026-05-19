---
name: "GitHub Actions Defaults (YAML)"
description: "Same as .yml; provided separately for .yaml extension."

## applyTo: ".github/workflows/**/*.yaml"

# GitHub Actions Defaults (YAML)

## Permissions & secrets

- Use least-privilege permissions: set `permissions: {}` at workflow level and grant only what each job needs.

- Never echo secrets in `run` steps; use `::add-mask::` if a computed value is sensitive.

- Prefer OIDC federation for cloud auth over storing long-lived credentials as secrets.

## Reproducibility

- Pin action versions by SHA, not tag: `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683`.

- Print tool versions at the start of each job (`node --version`, `dotnet --version`).

- Use `cache:` with explicit `key` patterns tied to lockfile hashes for dependency caching.

## Job structure

- Keep steps explicit; prefer small composable jobs over one large job.

- Separate fast checks (lint, type-check) from slow ones (build, test, E2E) using `needs:`.

- Use matrix builds for testing multiple configurations (OS, runtime version).

- Set `timeout-minutes` on long-running jobs to prevent runaway billing.

## Maintainability

- Extract repeated step sequences into reusable workflows (`workflow_call`) or composite actions.

- For complex logic, move it into a script in the repo — not inline `run` YAML.

- Document how to run workflows locally using `act`.

## Example: minimal secure job

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
      - run: node --version
      - run: npm ci
      - run: npm run lint
```

---

## 🏆 Elite Section — Top 5% GitHub Actions Practices

- **`zizmor` for workflow security audit**: Run `zizmor` (or `actionlint`) in CI to detect workflow injection vulnerabilities, overly-permissive tokens, and insecure `pull_request_target` patterns.

- **Concurrency groups for branch workflows**: Add `concurrency: { group: ${{ github.ref }}, cancel-in-progress: true }` to prevent redundant runs when force-pushing to a branch.

- **Required status checks + branch protection**: Every quality gate (lint, test, type-check) must be a required status check on the default branch. PRs should never be mergeable without green CI.

- **Workflow dispatch for manual releases**: Add `workflow_dispatch` with typed `inputs` for controlled manual triggers; avoid ad-hoc script runs outside of CI for any deployment step.

- **Artifact attestation**: Use `actions/attest-build-provenance` to sign build artifacts with SLSA provenance. Attach attestation to container images and release assets.

- **Cost visibility**: Add `timeout-minutes` to every job and review GitHub Actions billing monthly. Flag jobs exceeding 10 min as candidates for optimization.
