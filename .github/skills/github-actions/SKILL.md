---
name: github-actions
description: Elite GitHub Actions CI/CD — security hardening, reusable workflows, quality gates, and structured debug methodology.
argument-hint: "[workflow-name] [trigger-event]"
user-invocable: true

## disable-model-invocation: false

# GitHub Actions (Elite CI/CD)

## When to use

- You need to build, harden, or troubleshoot a GitHub Actions pipeline.

- You want quality gates (lint / tests / docs / security) enforced on PRs.

- You need a reproducible, least-privilege, observable workflow.

## Procedure

### 1. Security hardening (mandatory)

**Pin all third-party actions to a full commit SHA, never a mutable tag:**

```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

**Set minimal `GITHUB_TOKEN` permissions at workflow and job level:**

```yaml
permissions:
  contents: read       # default — tighten per job
  pull-requests: write # only on jobs that post comments
```

**Use OIDC for cloud authentication — never store long-lived cloud credentials as secrets:**

```yaml
- uses: aws-actions/configure-aws-credentials@...
  with:
    role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
    aws-region: us-east-1
```

**Secret hygiene rules:**

- Never `echo` a secret; use `::add-mask::` if a derived value must be logged.

- Rotate secrets on a defined cadence; document rotation owner.

- Use environment secrets for deployment-scoped credentials (not repo-level).

### 2. Workflow structure

**PR checks (fast-first principle):**

```yaml
jobs:
  lint:          # < 2 min — fail fast
  unit-tests:    # < 5 min — parallelized matrix
  security-scan: # < 3 min — SAST / dependency audit
  docs-check:    # < 1 min — markdownlint, link check
```

**Release / main branch (separate, slower):**

```yaml
jobs:
  integration-tests:  # allowed to be slower
  publish:            # depends on all above; needs environment approval
```

Rules:

- Never mix PR quality-gate jobs with release/publish jobs in one workflow.

- Use `concurrency` to cancel stale PR runs:

  ```yaml
  concurrency:
    group: ${{ github.workflow }}-${{ github.ref }}
    cancel-in-progress: true
  ```

### 3. Reusable workflows

Extract shared logic into a called workflow:

```yaml
# .github/workflows/reusable-lint.yml
on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
```

Call from a composite workflow:

```yaml
jobs:
  lint:
    uses: ./.github/workflows/reusable-lint.yml
    with:
      node-version: "20"
```

### 4. Dependency caching

```yaml
- uses: actions/cache@...
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-npm-
```

- Always include a `restore-keys` fallback.

- Cache key must include a lockfile hash; avoid caching on branch name alone.

- Validate that cached artifacts do not carry stale build outputs across incompatible dependency versions.

### 5. Matrix builds

```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest, windows-latest]
    python-version: ["3.11", "3.12"]
```

- Use `fail-fast: false` when you want full coverage of all matrix entries even if one fails.

- Label jobs with `name: Test (${{ matrix.os }}, ${{ matrix.python-version }})` for readable run views.

### 6. Self-hosted runner isolation

- Run untrusted PR workflows on ephemeral, isolated runners only.

- Never grant self-hosted runners elevated cloud permissions scoped to production.

- Use labels to route: `runs-on: [self-hosted, linux, isolated]`.

### 7. Observability

- Always print tool versions at the start of each job:

  ```yaml

  - run: node --version; npm --version; python --version
  ```

- Use GitHub annotations for structured warnings/errors:

  ```bash
  echo "::error file=src/app.ts,line=42::Unhandled null reference"
  echo "::warning file=docs/guide.md,line=7::Broken link detected"
  ```

- Upload test reports and coverage as artifacts with explicit `retention-days`.

### 8. Failure debug procedure (structured)

1. **Reproduce locally first**: `act -j <job-name>` (if available) or reproduce step-by-step in a local container.

2. **Print environment**: add `env` step before the failing step.

3. **Isolate**: comment out steps below the failure point to narrow down.

4. **Check runner logs**: look for "OOM killed", "disk space", network timeouts.

5. **Check secret availability**: a blank `${{ secrets.X }}` means the secret is not set for that environment.

6. **Enable debug logging**: set `ACTIONS_STEP_DEBUG=true` as a repo/environment variable.

7. **Check action version pinning**: a SHA mismatch can cause unexpected behavior after a cache restore.

## Self-check

- [ ] All third-party actions pinned to full SHA with version comment.

- [ ] `permissions` set at workflow level; overridden (narrowed) per job.

- [ ] No long-lived cloud credentials stored as repo secrets; OIDC used.

- [ ] No `echo` of secret values; masking applied where needed.

- [ ] PR checks complete in ≤ 10 min total; slow jobs on separate workflow.

- [ ] `concurrency` group configured to cancel stale PR runs.

- [ ] Cache keys include lockfile hash; restore-keys fallback present.

- [ ] Tool versions printed at the start of each job.

- [ ] Test results and coverage uploaded as artifacts.

## Outputs

- Hardened workflow YAML (copy/paste-ready).

- Failure debug checklist.

- Reusable workflow structure recommendation.

- Security audit findings (pinning, permissions, secret hygiene).
