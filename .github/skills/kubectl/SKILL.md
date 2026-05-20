---
name: kubectl
description: kubectl operational cheatsheet -- context/namespace management, workload triage, logs, events, and rollouts.
argument-hint: "[namespace or resource name]"
user-invocable: true

disable-model-invocation: false
---

# kubectl Cheatsheet (Operational) (Elite)

## When to use

- You need fast commands for triage and verification.

- You want consistent, copy/paste-friendly kubectl usage.

## Workflow

### 1. Context and namespaces

```sh
kubectl config current-context
kubectl config use-context <context>  # switch context
kubectl get ns
```

### 2. Workloads

```sh
kubectl get deploy,rs,po -n <ns> -o wide
kubectl get po -n <ns> --watch  # live watch
```

### 3. Describe and logs

```sh
kubectl describe po <pod> -n <ns>
kubectl logs <pod> -n <ns> -c <container>        # current
kubectl logs <pod> -n <ns> -c <container> --previous  # previous (crashed)
```

### 4. Events

```sh
kubectl get events -n <ns> --sort-by=.lastTimestamp | tail -n 50
```

### 5. Rollouts

```sh
kubectl rollout status deploy/<name> -n <ns>
kubectl rollout history deploy/<name> -n <ns>
kubectl rollout undo deploy/<name> -n <ns>  # rollback
```

### 6. Exec and port-forward (debug)

```sh
kubectl exec -it <pod> -n <ns> -- /bin/sh
kubectl port-forward svc/<svc> 8080:80 -n <ns>
```

### 7. Resource usage (live)

```sh
kubectl top nodes
kubectl top pods -n <ns> --sort-by=cpu
kubectl top pods -n <ns> --sort-by=memory
```

### 8. Scale workloads

```sh
kubectl scale deploy/<name> --replicas=<n> -n <ns>
kubectl scale statefulset/<name> --replicas=<n> -n <ns>
# Emergency scale-to-zero (incident mitigation)
kubectl scale deploy/<name> --replicas=0 -n <ns>
```

### 9. Patch resources in-place

```sh
# Patch a single field (strategic merge)
kubectl patch deploy/<name> -n <ns> -p '{"spec":{"template":{"spec":{"containers":[{"name":"<c>","image":"<new-image>"}]}}}}'
# Set image directly (easier)
kubectl set image deploy/<name> <container>=<image>:<tag> -n <ns>
# Set env var
kubectl set env deploy/<name> MY_VAR=value -n <ns>
```

### 10. Ephemeral debug containers

```sh
# Attach a debug sidecar to a running pod (K8s >= 1.23)
kubectl debug -it <pod> -n <ns> --image=busybox --target=<container>
# Clone pod with debug shell (without disrupting original)
kubectl debug pod/<pod> --copy-to=debug-pod --image=busybox -n <ns> -- sh
```

### 11. Copy files to/from pods

```sh
kubectl cp <pod>:/path/to/file ./local-file -n <ns>
kubectl cp ./local-file <pod>:/path/to/file -n <ns>
```

### 12. Secrets and ConfigMaps

```sh
# List
kubectl get secrets -n <ns>
kubectl get configmaps -n <ns>
# Decode a secret value (base64)
kubectl get secret <name> -n <ns> -o jsonpath='{.data.<key>}' | base64 -d
# Create opaque secret quickly
kubectl create secret generic <name> --from-literal=key=value -n <ns>
# Create from file
kubectl create secret generic <name> --from-file=./secret.txt -n <ns>
```

### 13. Node operations

```sh
kubectl get nodes -o wide
kubectl describe node <node>
# Cordon (prevent scheduling) + drain (evict pods) for maintenance
kubectl cordon <node>
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data
# Uncordon after maintenance
kubectl uncordon <node>
# Check node pressure / conditions
kubectl get node <node> -o json | jq '.status.conditions'
```

### 14. Resource quotas and limits

```sh
kubectl get resourcequota -n <ns>
kubectl describe resourcequota -n <ns>
kubectl get limitrange -n <ns>
```

### 15. Labels, annotations and field-selectors

```sh
# Filter by label
kubectl get pods -l app=<name>,env=prod -n <ns>
# Add / overwrite label
kubectl label pod <pod> env=debug -n <ns>
# Add annotation
kubectl annotate pod <pod> debug/reason="incident-2026-03-06" -n <ns>
# Field selector (e.g. only Running pods)
kubectl get pods --field-selector=status.phase=Running -n <ns>
```

### 16. Apply, diff and delete safely

```sh
# Always diff before applying
kubectl diff -f manifest.yaml
kubectl apply -f manifest.yaml --dry-run=server   # server-side dry run
kubectl apply -f manifest.yaml

# Delete with confirmation (never --force unless truly stuck)
kubectl delete pod <pod> -n <ns> --grace-period=30
# Force-delete a stuck terminating pod (last resort)
kubectl delete pod <pod> -n <ns> --grace-period=0 --force
```

### 17. Service and endpoint inspection

```sh
kubectl get svc -n <ns> -o wide
kubectl get endpoints <svc> -n <ns>
kubectl describe ingress -n <ns>
# Quick DNS resolution test from a pod
kubectl run dnstest --image=busybox --restart=Never -n <ns> --rm -it -- nslookup <svc>.<ns>.svc.cluster.local
```

## Self-check

- [ ] Context confirmed before any destructive action (`kubectl config current-context`).

- [ ] Previous container logs checked (not just current) for crash loop analysis.

- [ ] Events reviewed in the incident time window.

- [ ] Rollout status confirmed after upgrade (`rollout status`).

- [ ] `kubectl diff` run before `kubectl apply` on any manifest.

- [ ] `kubectl drain` used (not delete) before node maintenance.

- [ ] Secret values decoded only in trusted shell; never logged.

## Outputs

- A minimal "triage command set".

- Rollout and rollback commands.
