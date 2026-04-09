---
name: apm-analysis
description: "APM analysis: trace/transaction breakdown, latency hotspots, error correlation, next instrumentation steps."
agent: "Reliability"
argument-hint: "service=<name> time-range=<window> symptom=<description>"
---

Inputs:

- service: ${input:service:service name or APM app}
- time-range: ${input:time-range:e.g. last 15m / 2024-01-01T10:00}
- symptom: ${input:symptom:latency spike|error rate|missing traces}

Act as a Reliability engineer and analyze the APM data (traces/transactions/spans).

Output:

- First symptom and most likely causal chain
- Top latency contributors (by span/operation)
- Error correlation (exceptions/status codes <-> trace IDs)
- Next queries to run (transactions, traces, breakdowns)
- Fix options (app/dependency/infra/config) + verification
- Instrumentation improvements (labels, sampling, correlation IDs)
- Facts versus assumptions split
- Escalation criteria if verification fails

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Reliability** | always — analysis phase | *(this prompt)* | Causal chain identified, facts vs. assumptions documented |
| 2 | **Backend .NET** | app-level root cause confirmed | `/dotnet-excellence` | Fix implemented, `dotnet build -warnaserror` + tests green |
| 3 | **DevOps/Cloud** | infra or dependency root cause confirmed | `/k8s-triage` or `/helm-triage` | Infra fix applied, service healthy |
| 4 | **Automation/Scripting** | monitoring or instrumentation gaps found | `/automation-script` | Alerting/instrumentation improvements deployed |
| 5 | **Delivery Lead** | any fix implemented | `/pr-review` | PR approved, CI green, merged |
