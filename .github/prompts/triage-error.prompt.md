---
name: triage-error
description: "Triage an error: repro steps, ranked hypotheses, validation plan, fix options, verification checklist."
agent: "Reliability"
argument-hint: "error=<message or stack> env=<dev|staging|prod> service=<name>"
---
Act as a Reliability engineer and triage the error.

Include:

- Minimal reproduction steps (env, versions, input)
- 3–5 ranked hypotheses (likelihood × cost to validate)
- Validation steps per hypothesis
- Fix options (mitigation vs remediation)
- Verification checklist (local + CI)
- Observed facts versus assumptions split
- Escalation criteria if top hypotheses are invalidated

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Reliability** | always — error triage | *(this prompt)* | Ranked hypotheses produced, validation plan and fix options defined |
| 2 | **Backend .NET** | app-level root cause confirmed | `/dotnet-excellence` | Fix implemented, dotnet build -warnaserror + tests green |
| 3 | **DevOps/Cloud** | infra or config root cause confirmed | `/k8s-triage` or `/helm-triage` | Infra fix applied, error no longer reproducible |
| 4 | **Reliability** | P1 incident or significant user impact | `/postmortem` | Postmortem drafted, action items tracked |
| 5 | **Delivery Lead** | fix committed | `/pr-review` | PR approved, regression test passing, CI green |
