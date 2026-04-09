---
name: helm-cli
description: Helm CLI operational cheatsheet - inspect, render, upgrade, rollback, and diff workflows.
argument-hint: "[release-name] [namespace]"
user-invocable: true
disable-model-invocation: false
---

# Helm CLI Cheatsheet (Operational) (Elite)

## When to use

- You need fast, correct Helm commands (install/upgrade/status/history/rollback).
- You want deterministic chart rendering and debugging.

## Workflow

### 1. Inspect releases

```sh
helm list -A
helm status <release> -n <ns>
helm history <release> -n <ns>
```

### 2. Get rendered state

```sh
helm get manifest <release> -n <ns>
helm get values <release> -n <ns> -a
```

### 3. Render locally (debug)

```sh
helm lint <chartDir>
helm template <release> <chartDir> -n <ns> -f values.yaml --debug > rendered.yaml
```

### 4. Upgrade patterns

```sh
# Standard upgrade
helm upgrade --install <release> <chartDir> -n <ns> -f values.yaml --wait --timeout 10m

# Safer: atomic (auto-rollback on failure)
helm upgrade --install --atomic <release> <chartDir> -n <ns> -f values.yaml --timeout 10m
```

### 5. Rollback

```sh
helm rollback <release> <rev> -n <ns> --wait --timeout 10m
```

### 6. Diff (helm-diff plugin)

```sh
helm diff upgrade <release> <chartDir> -n <ns> -f values.yaml
```

## Self-check

- [ ] `helm lint` passes before upgrade.
- [ ] `helm diff` reviewed before applying to production.
- [ ] `--atomic` used for production upgrades (auto-rollback on failure).
- [ ] `helm history` checked after upgrade to confirm success.
- [ ] Rollback tested in staging before production promotion.

## Outputs

- A minimal set of commands for triage.
- A repeatable render -> inspect -> upgrade -> verify flow.
