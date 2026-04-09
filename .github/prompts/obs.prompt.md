---
name: obs
description: "Observability incident triage — first response for latency spikes, error rate surges, log anomalies, and missing traces across Elastic APM, Kibana, and log pipelines."
agent: Reliability
argument-hint: "symptom=<description> service=<name> time-range=<window e.g. last 15m>"
---

## Observability Incident Triage

You are running as the **Reliability** agent performing first-response observability triage.

Apply the procedure from `.github/skills/elastic/SKILL.md`.
Apply the procedure from `.github/skills/apm/SKILL.md`.
Apply the procedure from `.github/skills/logs-alerts/SKILL.md`.

---

## Intake — collect these before starting

If not already provided in the argument, ask:

1. **Symptom** — What is broken or degraded? (latency spike / error rate surge / missing traces / alert fired)
2. **Service(s)** — Which service(s) are affected? (or "unknown")
3. **Time range** — When did it start? (exact timestamp or relative window)
4. **Baseline** — Is there a known-good reference window to compare against?

---

## Triage procedure

### Step 1 — Cluster + pipeline health (Elasticsearch)

```sh
GET _cluster/health?pretty
GET _cat/nodes?v&h=name,heap.percent,ram.percent,cpu,load_1m,node.role
GET _cat/shards?v&h=index,shard,prirep,state,node&s=state   # flag UNASSIGNED
```

Confirm: Elasticsearch is healthy before trusting absence of logs as signal.

### Step 2 — Error rate snapshot (Kibana / KQL)

Open the relevant index; set time range; run:

```kql
service.name: "<service>" AND event.outcome: failure
http.response.status_code >= 500
```

Record: error count and rate vs. baseline window.

### Step 3 — APM trace drill-down

- APM → Services → `<service>` → Transactions → sort by p99.
- Open the slowest/erroring trace; inspect span waterfall.
- Flag: which span is the bottleneck — DB, upstream call, internal logic?
- Check Correlations tab for distinguishing attributes (host, version, customer).

### Step 4 — Log correlation

- Cross-reference trace IDs found in APM with Kibana Discover.
- Look for log lines at the same timestamp with `error` or `warn` level.
- Check Kubernetes pod logs if applicable:

```kql
kubernetes.namespace: "production" AND log.level: error AND trace.id: "<id>"
```

### Step 5 — Ranked hypotheses

Produce a numbered list (ranked by likelihood based on evidence):

```text
1. [Hypothesis] — [Supporting evidence from APM/logs/ES metrics]
2. …
```

### Step 6 — Remediation options

For each top hypothesis, propose:

- Immediate mitigation (scale, rollback, circuit-break, rate-limit)
- Root cause fix (code, config, infra)
- Verification: which metric/query confirms the fix landed

---

## Delegation chain

| Task | Owner | Trigger |
|------|-------|---------|
| Code-level fix (app bug) | Backend .NET | Hypothesis points to application logic |
| Infrastructure / AKS / Helm rollback | DevOps/Cloud | Hypothesis points to deployment or infra change |
| Post-incident issue + postmortem | Delivery Lead | Incident confirmed resolved |
| Alerting rule update | Reliability | Alert did not fire or fired too late |
