---
name: kubernetes
description: Kubernetes workload triage — workload spec review, resource limits, probes, RBAC, logs, and rollback.
argument-hint: "[namespace] [workload]"
user-invocable: true
disable-model-invocation: false
---

# Kubernetes (K8s) (Elite)

## When to use

- Deploying, updating, or troubleshooting Kubernetes workloads.
- Defining resource limits, probes, and RBAC.

## Procedure

### 1. Confirm context (always first)

```bash
kubectl config current-context
kubectl config get-contexts
```

Never operate without confirming the cluster and namespace.

### 2. Review workload state

```bash
kubectl get deploy,rs,po -n <ns> -o wide
kubectl get events -n <ns> --sort-by=.lastTimestamp | tail -20
```

### 3. Inspect failing workload

```bash
kubectl describe pod <pod> -n <ns>   # probes, mounts, events, image
kubectl logs <pod> -n <ns> --previous  # last crash logs
kubectl logs <pod> -n <ns> -c <container>  # if multi-container
```

Common failure modes:

| Symptom | Cause | Fix |
|---------|-------|-----|
| `CrashLoopBackOff` | App crash / bad config | Check logs, env vars |
| `OOMKilled` | Memory limit too low | Increase `resources.limits.memory` |
| `Pending` / unschedulable | No nodes with capacity | Check `kubectl describe pod` for resource fit |
| `ImagePullBackOff` | Registry auth / wrong image | Check imagePullSecrets, image tag |
| `ReadinessProbe` failing | App not ready | Check probe path, port, initial delay |

### 4. Check workload spec

```yaml
# Required for every workload:
resources:
  requests: { cpu: "100m", memory: "128Mi" }
  limits:   { cpu: "500m", memory: "512Mi" }
readinessProbe: { httpGet: { path: /health/ready, port: 8080 }, initialDelaySeconds: 5 }
livenessProbe:  { httpGet: { path: /health/live,  port: 8080 }, initialDelaySeconds: 15 }
```

### 5. Check RBAC and network policies

```bash
kubectl auth can-i <verb> <resource> -n <ns> --as=system:serviceaccount:<ns>:<sa>
kubectl get networkpolicy -n <ns>
```

### 6. Rollback

```bash
kubectl rollout history deploy/<name> -n <ns>
kubectl rollout undo deploy/<name> -n <ns>           # undo last
kubectl rollout undo deploy/<name> -n <ns> --to-revision=<N>  # undo to N
kubectl rollout status deploy/<name> -n <ns>         # verify
```

## Self-check

- [ ] Context confirmed before any command.
- [ ] All workloads have resource requests AND limits.
- [ ] Readiness and liveness probes defined.
- [ ] Pod events reviewed for scheduling/image errors.
- [ ] RBAC checked if access issues.
- [ ] Rollback verified with `rollout status`.

## Outputs

- Triage checklist.
- Common failure modes + fixes table.
- Rollback procedure.
- Workload spec requirements.
