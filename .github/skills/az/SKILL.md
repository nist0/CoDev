---
name: az
description: Azure CLI operational playbook — identity safety, context confirmation, AKS ops, and safe command patterns.
argument-hint: "[subscription] [resource-group]"
user-invocable: true
disable-model-invocation: false
---

# Azure CLI (az) Operational Playbook (Elite)

## When to use

- You need a **safe, step-by-step operational sequence** for Azure CLI + AKS operations.
- You need to avoid "wrong subscription / wrong cluster" mistakes.
- You want failure-bucket awareness before running AKS commands.

> For Azure Static Web Apps, Azure Container Apps Consumption, Azure SQL Database Free Tier, and Cloudflare DNS workflows, use the [`cloud-web-hosting` skill](.github/skills/cloud-web-hosting/SKILL.md).
> For full Azure CLI command syntax across all services (Key Vault, ACR, RBAC, Monitoring, Identity, Resource discovery), see the [`azure` skill](.github/skills/azure/SKILL.md).

## Workflow

1) **Identity and context safety** — always first
   - Confirm current subscription before anything else.
   - Command reference: see `azure` skill → *Quick reference / Identity and context*.
   - Always confirm **again** after switching: `az account show -o table`

2) **Resource discovery**
   - Enumerate resource groups and resources in scope.
   - Command reference: see `azure` skill → *Quick reference / Resource discovery*.
   - Use sparingly; `az resource list -g <rg>` can return a large payload.

3) **AKS essentials**
   - Get cluster credentials and verify context:
     ```sh
     az aks get-credentials -g <rg> -n <cluster> --overwrite-existing
     kubectl config current-context   # always verify after getting credentials
     ```
   - Full command reference: see `azure` skill → *Quick reference / AKS*.

4) **Node pool and scaling** — proceed with caution
   ```sh
   az aks nodepool list -g <rg> --cluster-name <cluster> -o table
   az aks nodepool show -g <rg> --cluster-name <cluster> -n <pool> -o table
   ```
   Record the current state before any scaling operation.

5) **Failure buckets** — check these first when something is wrong
   - Wrong subscription / context → repeat step 1.
   - RBAC / permissions issues → check role assignments (see `azure` skill → *Quick reference / RBAC*).
   - Network policies / LB / DNS issues.
   - Cluster upgrade regressions.

6) **Safe operations principles**
   - Prefer read-only commands first.
   - For scaling/changes: record current state and plan rollback before executing.

## Self-check

- [ ] `az account show` confirmed BEFORE any mutating command.
- [ ] `kubectl config current-context` verified before any `kubectl` operation.
- [ ] Read-only commands used first; write operations reviewed explicitly.
- [ ] Rollback plan defined before scaling or upgrading.

## See also

- [`azure` skill](.github/skills/azure/SKILL.md) — full Azure CLI command reference (Key Vault, ACR, RBAC, Monitoring, Identity, Resource discovery, Secrets)

## Outputs

- Safe command sequence to confirm identity and target before any operation.
- Repeatable AKS "connect + verify" procedure.
- Failure bucket checklist for structured triage.
