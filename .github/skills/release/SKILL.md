---
name: release
description: End-to-end release pipeline — SemVer tagging, artifact signing, changelog, smoke test, and rollback.
argument-hint: "[version] [target-environment]"
user-invocable: true
disable-model-invocation: false
---

# Release CI/CD (Elite)

## When to use

- Creating a release pipeline (tag → build → artifact → publish).
- Defining SemVer tagging and changelog automation.
- Validating a release is safe before promoting to production.

## Procedure

### 1. Pre-release gate

Before cutting a release:

- [ ] All CI checks green on target commit.
- [ ] No open `priority:p0` or `priority:p1` bugs in milestone.
- [ ] CHANGELOG draft reviewed (conventional commits parsed).
- [ ] Dependencies audited (`npm audit` / `dotnet list package --vulnerable` / `pip-audit`).
- [ ] Security scan clean.
- [ ] Staging smoke tests passed.

### 2. Define the trigger

| Strategy | Trigger | Use when |
|----------|---------|----------|
| Tag push | `vX.Y.Z` push to main | Most common; automated |
| Manual dispatch | `workflow_dispatch` with version input | Controlled / hotfix |
| Scheduled | cron on main | Nightly / preview releases |

### 3. Build and sign artifacts

1. Build a **deterministic** artifact (same inputs → same hash).
2. Generate SBOM (`syft` or language-native tool).
3. Sign artifact with **Cosign + OIDC** (no long-lived keys).
4. Publish signature to transparency log (Rekor).
5. Verify signature before any deployment step.

### 4. Generate changelog

- Use Conventional Commits (`feat:`, `fix:`, `BREAKING CHANGE:`).
- Map commits to SemVer bump: `BREAKING CHANGE` → major, `feat` → minor, `fix` → patch.
- Format: `## [vX.Y.Z] — YYYY-MM-DD\n### Added | Changed | Fixed | Removed | Security`.
- Auto-generate via `git-cliff`, `release-please`, or `conventional-changelog-cli`.

### 5. Publish to target

| Target | Tooling | Verification |
|--------|---------|-------------|
| GitHub Release | `gh release create` | Asset hashes in release body |
| Container registry | `docker push` + `cosign sign` | `cosign verify` post-push |
| NuGet / PyPI / npm | `dotnet pack` / `twine` / `npm publish` | Provenance attestation |
| Helm chart | `helm package` + OCI push | `helm pull` + `cosign verify` |

### 6. Post-release verification

1. Run release smoke tests against the published artifact.
2. Confirm version is resolvable from all target environments.
3. Verify signature chain end-to-end.
4. Monitor error rates and latency for 15 min post-deploy.

### 7. Rollback plan (document before releasing)

| Scenario | Action |
|----------|--------|
| Bad artifact published | Delete artifact; revert tag; re-publish prior artifact |
| Deployment failed mid-way | Revert config (GitOps); re-deploy prior version |
| Post-deploy regression | Trigger rollback workflow; alert on-call |

## Self-check

- [ ] Pre-release gate passed before tagging.
- [ ] Artifact signed with OIDC-based Cosign (no static key).
- [ ] SBOM generated and attached to GitHub Release.
- [ ] Changelog follows Conventional Commits format.
- [ ] Smoke tests verify artifact post-publish.
- [ ] Rollback plan documented and tested.

## Outputs

- Release workflow YAML template.
- Changelog (copy/paste-ready).
- Artifact signing checklist.
- Post-release verification runbook.
- Rollback procedure.
