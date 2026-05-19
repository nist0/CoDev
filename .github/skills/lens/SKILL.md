---
name: lens
description: Lens Kubernetes UI - cluster context confirmation, workload inspection, config review, and fix validation.
argument-hint: "[namespace or workload]"
user-invocable: true

disable-model-invocation: false
---

# Lens (Kubernetes Cluster Explorer) (Elite)

## When to use

- You need a richer UI to explore workloads, configs, and cluster resources.

- You want to correlate object configuration with runtime status quickly.

## Navigation Map

| Section | What to check |
|---------|---------------|
| Workloads > Pods | Restart count, readiness, container images |
| Workloads > Deployments | Desired vs ready replicas, rollout state |
| Configuration > ConfigMaps | App config values |
| Configuration > Secrets | (redacted) secret presence and mounts |
| Network > Services | Port mapping and selector match |
| Network > Ingress | Host rules, TLS config |
| Network > Endpoints | Populated endpoints (routing readiness) |
| Events | Scheduling failures, probe failures, image pull errors |

## Workflow

### 1. Confirm cluster context

- Verify the cluster at the top of Lens before any action.

- Avoid wrong-cluster operations (especially destructive ones).

### 2. Navigate to workloads

- Workloads > Deployments/Pods.

- Configuration > ConfigMaps/Secrets.

- Network > Services/Ingress/Endpoints.

- Events and metrics views.

### 3. Diagnose

- Identify failing pods (restarts, readiness).

- Review environment variables and config mounts.

- Inspect service selectors vs pod labels (label mismatch = no traffic).

### 4. Validate fix

- Rollout status green.

- Endpoints ready and populated.

- Basic smoke test passes.

## Self-check

- [ ] Cluster context confirmed before any action.

- [ ] Pod restart count and previous logs inspected.

- [ ] Service selector vs pod labels verified (no mismatch).

- [ ] Endpoints populated after deployment.

- [ ] Fix validated with rollout status + smoke test.

## Outputs

- A UI-driven diagnostic path that maps to kubectl commands.

- A before/after verification checklist.
