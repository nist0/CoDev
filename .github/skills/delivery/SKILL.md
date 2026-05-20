---
name: delivery
description: End-to-end delivery discipline -- Definition of Done, PR hygiene, CI quality gates, release readiness, and post-release verification.
argument-hint: "[feature-or-fix] [environment]"
user-invocable: true

disable-model-invocation: false
---

# Delivery (Execution, Quality Gates, Release Readiness) (Elite)

## When to use

- You want consistent delivery practices: from planning to PR to release.

- You need quality gates and release readiness checklists.

- You need a Definition of Done for a feature, bug fix, or project.

## Procedure

### 1. Define Done (before writing code)

For every task, define done criteria upfront:

- [ ] Acceptance criteria written and agreed.

- [ ] Tests identified (unit / integration / e2e).

- [ ] Docs identified (changelog, ADR, runbook, API doc).

- [ ] Rollout notes written (feature flag, migration, config change).

- [ ] Rollback plan defined.

### 2. PR discipline

| Rule | Why |
|------|-----|
| PRs <= 400 lines changed | Reviewers can be thorough |
| One logical change per PR | Easy to revert cleanly |
| PR description links issue | Traceability |
| PR description explains why (not just what) | Context for reviewers |
| Draft PR while WIP | No premature review |
| Conventional Commits title | Changelog automation |

PR description template:

```markdown
## Context
<Why this change is needed>

## Changes
<What changed; bullet list>

## Testing
<How was this tested locally>

## Links
Closes #<issue>
```

### 3. Quality gates (CI)

| Gate | Tool | Failure action |
|------|------|----------------|
| Compile / build | Language toolchain | Block merge |
| Unit tests | Test runner | Block merge |
| Linting | ESLint / Roslyn / flake8 | Block merge |
| Security scan | Semgrep / CodeQL | Block merge on HIGH |
| Integration tests | Test runner + test containers | Block merge |
| Docs lint | markdownlint | Block merge |
| Dependency audit | npm audit / pip-audit | Warn; block on CRITICAL |

### 4. Release readiness checklist

- [ ] All CI checks green on the release commit.

- [ ] Version bumped (SemVer).

- [ ] CHANGELOG updated (Conventional Commits).

- [ ] Release notes reviewed by team.

- [ ] Staging smoke tests passed.

- [ ] Feature flags configured for progressive rollout.

- [ ] Rollback plan documented and tested.

- [ ] On-call briefed (for P0/P1 risk releases).

### 5. Post-release verification

1. Monitor error rate for 15 min post-deploy; compare vs pre-deploy baseline.

2. Check SLO dashboard: latency p50/p95/p99, availability, error budget.

3. Confirm all alerts are in normal state.

4. Close milestone and linked issues in GitHub.

5. Send team update (Slack / email) with release notes link.

## Self-check

- [ ] Done criteria defined before implementation started.

- [ ] PR is <= 400 lines and covers one logical change.

- [ ] PR description includes context, changes, testing, and issue link.

- [ ] All CI gates pass before merge.

- [ ] Release readiness checklist completed before tagging.

- [ ] Post-release monitoring performed for >= 15 min.

## Outputs

- Definition of Done checklist.

- PR readiness checklist.

- Release readiness checklist.

- Post-release monitoring runbook.
