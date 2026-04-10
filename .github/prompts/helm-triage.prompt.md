---
name: helm-triage
description: "Helm triage: chart rendering, values sanity, diff/upgrade failures, rollback and verification."
agent: "DevOps/Cloud"
argument-hint: "chart=<name> release=<name> namespace=<ns> symptom=<text>"
---
Apply the procedure from `.github/skills/helm/SKILL.md`.

Act as a DevOps/Cloud engineer and triage the Helm issue.

Include:

- Context to collect (chart name/version, release, namespace, values source, upgrade time)
- Render validation (`helm lint`, `helm template`) and what to inspect
- Common failure modes (hooks, CRDs, immutable fields, RBAC, schema/mapping, missing secrets)
- Upgrade strategy (atomic, timeout, wait, hooks)
- Diff and rollback plan (helm history / rollback)
- Verification steps (pods ready, endpoints, smoke checks)
- Risk classification (`low|medium|high`) for proposed actions
- Explicit go/no-go criteria before upgrade and rollback

Output format:

- Observed facts
- Ranked failure modes
- Mitigation versus remediation recommendation
- Verification, rollback, and escalation checklist

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **DevOps/Cloud** | always — Helm triage | *(this prompt)* | Failure mode ranked, go/no-go criteria established |
| 2 | **DevOps/Cloud** | fix identified | Apply fix inline or via `/automation-script` | Release/rollback applied, pods healthy |
| 3 | **Reliability** | P1 or P2 incident | `/postmortem` | Blameless postmortem drafted, action items created |
| 4 | **Delivery Lead** | fix committed | `/pr-review` | PR approved, CI green |
