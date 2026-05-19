---
name: azure
description: Azure operational basics — identity safety, resource navigation, secrets management, networking, and change verification.
argument-hint: "[resource-type] [resource-group]"
user-invocable: true

disable-model-invocation: false
---

# Azure (Operational Basics) (Elite)

## When to use

- You need a **complete Azure CLI command reference** across services (Key Vault, ACR, RBAC, Monitoring).

- You work on Azure resources and need safe operational defaults and common pitfalls.

> For Azure Static Web Apps, Azure Container Apps Consumption, Azure SQL Database Free Tier, and Cloudflare DNS workflows, use the [`cloud-web-hosting` skill](.github/skills/cloud-web-hosting/SKILL.md).
> For a step-by-step **procedural sequence** (identity confirmation -> AKS connect -> node pool ops -> failure triage), see the [`az` skill](.github/skills/az/SKILL.md).

## Workflow

1) Identity & subscription safety

   - Confirm account and subscription (`az account show`, `az account set`).
2) Resource navigation

   - Resource group, region, naming conventions.
3) AKS core operations (if applicable)

   - Get cluster details, credentials, node pools.
4) Secrets & configuration

   - Prefer managed identities/workload identity; avoid hard-coded secrets.
5) Networking

   - Ingress, load balancer, DNS; ensure correct routing.
6) Verify changes

   - Validate in staging; plan rollback in production.

## Self-check

- [ ] Subscription confirmed before any operation.

- [ ] No secrets or credentials hardcoded; managed identity used.

- [ ] Change validated in staging before production.

- [ ] Rollback plan documented.

## Quick reference

### Identity and context

```sh
az login                                          # interactive login
az account show -o table                          # confirm current subscription
az account list -o table                          # list all subscriptions
az account set --subscription "<name-or-id>"     # switch subscription
az account get-access-token                       # get a bearer token (debug)
```

### Resource discovery

```sh
az group list -o table
az resource list -g <rg> -o table
az resource list -g <rg> --resource-type <type> -o table
az tag list -o table                             # list all tag names in subscription
```

### AKS

```sh
az aks list -o table
az aks show -g <rg> -n <cluster> -o table
az aks get-credentials -g <rg> -n <cluster> --overwrite-existing
az aks nodepool list -g <rg> --cluster-name <cluster> -o table
```

### Key Vault

```sh
az keyvault list -o table
az keyvault secret list --vault-name <vault> -o table
az keyvault secret show --vault-name <vault> --name <secret>   # sensitive!
az keyvault certificate list --vault-name <vault> -o table
```

### Container Registry

```sh
az acr list -o table
az acr login --name <acr>                        # docker login via az
az acr repository list --name <acr> -o table
az acr repository show-tags --name <acr> --repository <repo> -o table
```

### RBAC

```sh
az role assignment list --assignee <user-or-sp> -o table
az role assignment create \
  --assignee <user-or-sp> \
  --role "<role-name>" \
  --scope "/subscriptions/<sub>/resourceGroups/<rg>"
az ad sp show --id <client-id>                   # look up a service principal
```

### Monitoring

```sh
az monitor metrics list --resource <resource-id> --metric <name> -o table
az monitor activity-log list -g <rg> --offset 24h -o table
az monitor log-analytics query \
  --workspace <ws-id> \
  --analytics-query "<KQL>" -o table
```

## Troubleshooting — failure buckets

Check these first when an operation fails unexpectedly:

| Symptom | Likely cause | Fix |
|---|---|---|
| Wrong resource returned / not found | Wrong subscription or resource group | Repeat identity check — `az account show` |
| 403 Forbidden | RBAC / permissions | Check role assignments — see *Quick reference / RBAC* |
| Network timeout / connection refused | Network policy, LB config, or DNS | Inspect ingress / NSG / DNS resolution |
| AKS instability after recent change | Cluster upgrade regression | Check node pool status, review upgrade changelog |
| `kubectl` targeting wrong cluster | Stale kubeconfig context | Re-run `az aks get-credentials` + verify `kubectl config current-context` |

> For the step-by-step operational sequence that prevents these issues, see the [`az` skill](.github/skills/az/SKILL.md).

## Outputs

- Full Azure CLI command reference across services.

- Common Azure pitfalls (wrong subscription/context, permissions, secrets hygiene).

- Verification and rollback guidance.
