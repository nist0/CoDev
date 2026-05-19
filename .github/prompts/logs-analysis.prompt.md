---
name: logs-analysis
description: "Logs/APM analysis: extract the first symptom, correlate traces, propose next queries and fixes."
agent: "Reliability"

argument-hint: "logs=<paste or path> service=<name> time-range=<window>"
---

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Apply the procedure from `.github/skills/logs-alerts/SKILL.md`.

Act as a Reliability engineer and analyze the logs/APM/traces.

Output:

- First symptom (earliest/most causal)

- Likely failure mode categories (app, dependency, infra, config)

- Next queries to run (Kibana/Elastic/APM-style)

- Fix options and verification steps

- Monitoring/alerting improvements to prevent recurrence

- Facts versus assumptions split

- Mitigation versus remediation recommendation with risk level

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Reliability** | always — log/APM analysis | *(this prompt)* | Root symptom identified, hypotheses ranked, fix options produced |
| 2 | **Reliability** | error with stack trace found | `/triage-error` | Ranked hypotheses validated, reproduction steps confirmed |
| 3 | **Backend .NET** | app-level root cause confirmed | `/dotnet-excellence` | Fix implemented, tests green |
| 4 | **DevOps/Cloud** | infra root cause confirmed | `/k8s-triage` or `/helm-triage` | Infra fix applied |
| 5 | **Delivery Lead** | fix ready | `/pr-review` | PR approved, CI green |
