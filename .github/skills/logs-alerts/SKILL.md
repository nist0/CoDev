---
name: logs-alerts
description: Log analysis and alerting — symptom identification, time-scoped filtering, correlation, and alert rule design.
argument-hint: "[service name or incident description]"
user-invocable: true
disable-model-invocation: false
---

# Logs & Alerts (Elite)

## When to use

- Analyzing structured logs or setting up alerting rules.
- Correlating logs with errors or latency spikes.

## Alert Design Table

| Property | Rule |
|----------|------|
| Threshold | Based on measured baseline, not guessed |
| Frequency | Alert fires when condition persists (avoid flapping) |
| Severity | P1: production down; P2: degraded; P3: warning |
| Runbook | Every alert links to a runbook or escalation path |
| Noise | If alert fires > 3x/week without action, re-tune it |

## Workflow

### 1. Identify the symptom

- Find the first error in logs (not just the last occurrence).
- Look for unusual patterns: error bursts, latency spikes, absence of expected logs.

### 2. Narrow time window and filter

- Scope to the incident window; filter by service, trace ID, or correlation ID.
- Use structured log fields (not just free-text search).

### 3. Correlate with changes

- Cross-reference with deployment events, config changes, and infrastructure changes.
- Check if the issue started exactly at a deploy or config push.

### 4. Extract signal for alert rule

- Define threshold from measured baseline (not intuition).
- Choose pattern: rate, count, absence of log, anomaly.

### 5. Define the alert

- Threshold, frequency, severity, runbook link.
- Test the alert fires correctly before closing the incident.

## Self-check

- [ ] First error found (not just last occurrence).
- [ ] Time window scoped to the incident (not "last 7 days").
- [ ] Correlation ID used to link log entries across services.
- [ ] Alert threshold validated against measured baseline.
- [ ] Alert links to a runbook or escalation path.

## Outputs

- Log query templates (KQL/Lucene/Elastic).
- Alert rule skeleton.
- Correlation checklist.
- Monitoring improvement suggestions.
