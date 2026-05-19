---
name: aks
description: AKS cluster operations — health checks, node pool management, networking triage, and safe upgrade procedure.
argument-hint: "[cluster] [resource-group]"
user-invocable: true

disable-model-invocation: false
---

# AKS (Azure Kubernetes Service) (Elite)

## When to use

- Managing or troubleshooting an AKS cluster.

- Configuring node pools, managed identity, or networking.

- Planning a cluster upgrade or scale operation.

## Procedure

### 1. Confirm identity and subscription (always first)

```bash
az account show -o table
az account set --subscription "<subIdOrName>"
az account show -o table   # confirm again
```

### 2. Check cluster health

```bash
az aks show -g <rg> -n <cluster> -o table
az aks get-credentials -g <rg> -n <cluster> --overwrite-existing
kubectl config current-context
kubectl get nodes -o wide
kubectl get pods -A | grep -v Running | grep -v Completed
```

### 3. Review node resource utilization

```bash
kubectl top nodes
kubectl top pods -A --sort-by=cpu | head -20
```

Flags:

- CPU throttling → check container `resources.limits.cpu`.

- Memory pressure → check `OOMKilled` in pod events.

### 4. Inspect control plane logs

```bash
az aks show -g <rg> -n <cluster> --query "addonProfiles"
# Enable Azure Monitor if not already:
az aks enable-addons --addons monitoring -g <rg> -n <cluster>
```

In Azure Monitor: query `KubePodInventory`, `ContainerLog`, `KubeEvents`.

### 5. Verify networking

```bash
kubectl get ingress -A
kubectl get svc -A | grep LoadBalancer
kubectl get endpoints -n <ns>
nslookup <service-name>.<ns>.svc.cluster.local
```

Common networking failures:

- LB not provisioned → check Azure quota.

- DNS not resolving → check CoreDNS pod health.

- Network policy blocking traffic → `kubectl get networkpolicy -A`.

### 6. Upgrade or scale safely

**Before any change**:

- [ ] Record current state (node count, versions, resource limits).

- [ ] Define rollback plan.

- [ ] Notify stakeholders.

```bash
# Node pool scaling
az aks nodepool scale -g <rg> --cluster-name <cluster> -n <pool> --node-count <n>
# Cluster upgrade (node pool rolling)
az aks upgrade -g <rg> -n <cluster> --kubernetes-version <version> --node-image-only
```

## Self-check

- [ ] Subscription confirmed before any operation.

- [ ] `kubectl config current-context` verified before changes.

- [ ] Node health and resource utilization reviewed.

- [ ] Rollback plan defined before upgrade or scale.

- [ ] Post-change: all pods Running, endpoints populated, smoke tests pass.

## Outputs

- AKS health checklist.

- Common failure patterns and fixes.

- Upgrade/scale procedure with rollback.

- Azure CLI command reference.
