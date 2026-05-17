---
name: az-ops
description: "Azure CLI operations — subscription context, resource discovery, AKS, Key Vault, ACR, RBAC, and monitoring queries."
agent: "DevOps/Cloud"
argument-hint: "concern=<context|aks|keyvault|acr|rbac|monitor> resource-group=<name>"
---


Argument handling:

- If arguments are provided, treat them as authoritative.
- If arguments are omitted, infer missing values from the current workspace, active file, and session context.
- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.
- Do not fail solely because arguments were omitted.

Apply procedures from `.github/skills/az/SKILL.md` and `.github/skills/azure/SKILL.md`.

Act as a DevOps/Cloud engineer and help with the Azure CLI operation.

Inputs:

- concern: ${input:concern:context | aks | keyvault | acr | rbac | monitor | resource}
- resource-group: ${input:resource-group:target resource group (optional)}

## Workflow

1. **Always confirm subscription first** — run `az account show -o table` and state the result before any mutating command.
2. Use the Quick reference section of the `azure` skill for copy-paste commands.
3. For AKS operations: also run `kubectl config current-context` after `az aks get-credentials`.
4. For RBAC: use the least-privilege role; prefer built-in roles over `Owner`/`Contributor`.
5. For Key Vault: read-only unless change is explicitly requested — treat values as sensitive.

## Output

- Copy-paste-ready `az` commands for the concern.
- Subscription and context confirmation step (always first).
- Risk classification for any mutating command (`low | medium | high`).
- Rollback or undo command for any write operation.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **DevOps/Cloud** | always — Azure CLI operations | *(this prompt)* | Commands provided, subscription confirmed, risk classified |
| 2 | **DevOps/Cloud** | AKS workload issue detected | `/k8s-triage` | Cluster issue diagnosed and mitigated |
| 3 | **Security** | RBAC or Key Vault concern | `/threat-model` or `/secrets-audit` | Threat modeled, least-privilege confirmed |
| 4 | **Delivery Lead** | infrastructure change requires PR | `/pr-review` | Change reviewed, CI green, merged |
