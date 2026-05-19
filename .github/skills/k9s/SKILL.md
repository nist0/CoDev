---
name: k9s
description: k9s Kubernetes triage UI — fast incident triage, pod/log/event inspection, and rollout verification.
argument-hint: "[namespace or workload name]"
user-invocable: true

## disable-model-invocation: false

# k9s (Kubernetes Triage UI) (Elite)

## When to use

- You need faster feedback than raw kubectl during an incident.

- You want to inspect pods/logs/events interactively across namespaces.

## High-Signal Views

| View | Signal |
|------|--------|
| Pods | CrashLoopBackOff, restart count, readiness |
| Events | Scheduling failures, image pull errors, probe failures |
| Deployments | Rollout state (desired vs ready) |
| ReplicaSets | Rollout history |
| Services/Endpoints | Routing readiness (endpoints populated?) |

## Workflow

### 1. Start and confirm context

- Run `k9s`

- Confirm current context/namespace at the top bar before any action.

- Switch context: `:ctx`, switch namespace: `:ns <name>`.

### 2. High-signal views

- Pods: crashloop, restarts, readiness.

- Events: recent failures, scheduling, image pull.

- Deployments/ReplicaSets: rollout state.

- Services/Endpoints: routing readiness.

### 3. Investigate a failing workload

- Open pod logs (current and previous with `p`).

- Describe pod for probes, mounts, env vars, image (`d`).

- Check events for "why" (`e`).

### 4. Rollout verification

- Confirm pods become Ready.

- Confirm endpoints populated.

- Confirm error rate reductions (tie back to observability).

## Self-check

- [ ] Context/namespace confirmed before taking any action.

- [ ] Previous logs inspected (not just current container logs).

- [ ] Events checked for root cause (not just pod status).

- [ ] Endpoints verified to be populated after deployment.

- [ ] Findings tied back to observability (metrics/traces/alerts).

## Outputs

- A rapid triage checklist using k9s views.

- A short list of the most useful screens and signals during incidents.
