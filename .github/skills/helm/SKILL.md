---
name: helm
description: Helm chart operations -- lint, template rendering, diff, safe upgrade, rollback, and verification.
argument-hint: "[release] [chart] [namespace]"
user-invocable: true

disable-model-invocation: false
---

# Helm (Elite)

## When to use

- Creating, upgrading, or troubleshooting Helm chart releases.

- Debugging template rendering or values failures.

## Workflow

1) Lint the chart: `helm lint`.
2) Render templates: `helm template` and inspect output.
3) Diff before upgrade: `helm diff upgrade` (plugin).
4) Upgrade safely: `--atomic`, `--timeout`, `--wait`.
5) Rollback: `helm rollback <release> <revision>`.
6) Verify: pod readiness, endpoint smoke checks.

## Self-check

- [ ] `helm lint` passes with no errors.

- [ ] `helm template` output reviewed before upgrade.

- [ ] `helm diff upgrade` reviewed; no unexpected changes.

- [ ] Upgrade uses `--atomic` or rollback plan is documented.

- [ ] Pod readiness and endpoint smoke checks run post-upgrade.

## Quick reference

For a full copy-paste command cheatsheet, apply `.github/skills/helm-cli/SKILL.md`.

```sh
# State overview
helm list -A
helm status <release> -n <ns>
helm history <release> -n <ns>

# Render and inspect
helm get manifest <release> -n <ns>
helm get values   <release> -n <ns> -a
helm template <release> <chart> -n <ns> -f values.yaml

# Diff before upgrade (requires helm-diff plugin)
helm diff upgrade <release> <chart> -n <ns> -f values.yaml

# Upgrade (atomic = auto-rollback on failure)
helm upgrade --install --atomic <release> <chart> -n <ns> -f values.yaml --timeout 10m

# Rollback
helm rollback <release> <rev> -n <ns> --wait

# Uninstall
helm uninstall <release> -n <ns>
```

## Outputs

- Triage checklist.

- Template rendering verification steps.

- Upgrade/rollback procedure.

- Common failure modes.
