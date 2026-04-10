---
name: k8s-triage
description: "Kubernetes/AKS triage: fast cluster checks, pod/service/ingress diagnosis, rollback and verification."
agent: "DevOps/Cloud"
argument-hint: "cluster=<name> namespace=<ns> workload=<name> symptom=<text>"
---
Apply procedures from `.github/skills/kubernetes/SKILL.md` and `.github/skills/kubectl/SKILL.md`.

Act as a DevOps/Cloud engineer and triage the Kubernetes/AKS issue.

Include:

- Context to collect (cluster, namespace, workload, image tag, deployment time)
- Fast checks (kubectl get/describe/logs/events)
- Hypotheses (config vs image vs infra vs dependency)
- Mitigation vs remediation options
- Rollback plan (helm rollback / kubectl rollout undo)
- Verification commands (readiness, probes, basic smoke checks)
- Risk classification (`low|medium|high`) for each mitigation/remediation option
- Stop conditions that indicate escalation is required

Output format:

- Observed facts
- Ranked hypotheses
- Immediate mitigation plan
- Durable remediation plan
- Verification and rollback checklist

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **DevOps/Cloud** | always — Kubernetes/AKS triage | *(this prompt)* | Ranked hypotheses produced, mitigation and remediation plans defined |
| 2 | **DevOps/Cloud** | mitigation identified | Apply inline or `/automation-script` | Workload healthy, readiness probes passing |
| 3 | **Reliability** | P1 incident or data loss | `/postmortem` | Postmortem drafted, corrective actions tracked |
| 4 | **Delivery Lead** | remediation committed | `/pr-review` | PR approved, CI green |
