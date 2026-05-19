---
name: rca-kit
description: Blameless postmortem and root cause analysis — 5-Whys, timeline, action items, and prevention tracking.
argument-hint: "[incident-title] [severity]"
user-invocable: true

disable-model-invocation: false
---

# RCA Kit (Elite Postmortem)

## When to use

- Conducting a blameless postmortem after a production incident.

- Producing a structured RCA document with timeline, root cause, and action items.

- Tracking prevention actions across multiple incidents.

## Procedure

### 1. Establish facts before analysis

- Do not start the postmortem with a conclusion.

- Collect raw data: logs, traces, metrics, alerts, on-call notes, deployment records.

- Separate **what happened** (facts) from **why it happened** (analysis).

### 2. Build the timeline

Chronological table (UTC timestamps):

| Time (UTC) | Event | Source |
|------------|-------|--------|
| HH:MM | Anomaly first appeared | APM alert |
| HH:MM | On-call paged | PagerDuty |
| HH:MM | Mitigation applied | Deployment log |
| HH:MM | Service restored | Monitoring |

- Include: detection, escalation, mitigation, resolution, and all significant events.

- Note gaps: what information was missing and when?

### 3. Root cause analysis (5 Whys)

```text
Symptom: <observable failure>
  Why 1: <direct cause>
    Why 2: <cause of cause>
      Why 3: <systemic cause>
        Why 4: <process/design gap>
          Why 5: <root cause>
```

Stop at the level where a **systemic fix is actionable**. Avoid stopping at "human error" — ask why the system allowed human error to cause an outage.

### 4. Contributing factors

Beyond root cause, list factors that made the incident worse or detection slower:

- Missing alert for X.

- Runbook did not cover Y scenario.

- Deployment happened during peak traffic window.

- Log message was ambiguous.

### 5. Impact assessment

| Dimension | Value |
|-----------|-------|
| Duration | <start> → <end> (total minutes) |
| Users affected | <count or %> |
| Error rate peak | <% or count/min> |
| SLO breach | Yes / No (if yes: ∆ error budget consumed) |
| Data integrity | Not affected / Affected (describe) |
| Revenue impact | <estimate if known> |

### 6. Corrective actions (immediate)

| Action | Type | Owner | Due date | Status |
|--------|------|-------|----------|--------|
| <action> | mitigation \| remediation | @person | YYYY-MM-DD | open |

### 7. Preventative actions (systemic)

| Action | Type | Owner | Due date |
|--------|------|-------|----------|
| Add alert for X | alert | @person | YYYY-MM-DD |
| Add regression test | test | @person | YYYY-MM-DD |
| Update runbook | runbook | @person | YYYY-MM-DD |
| Architecture review | design | @person | YYYY-MM-DD |

### 8. Review and publish

- Review draft with all responders before publishing (catch factual errors).

- Publish within 48h of incident resolution for P0/P1.

- Share with broader team (link in Slack/email); do not post blame.

- Schedule follow-up review to track action item completion (2–4 weeks).

## Blameless postmortem template

```markdown
# Postmortem: <title>

**Severity**: P0 | P1 | P2
**Date**: YYYY-MM-DD
**Duration**: <minutes>
**Status**: draft | reviewed | published

## Summary
<2–3 sentences: what happened, impact, how resolved>

## Impact
- Users affected: ...
- Error rate: ...
- SLO breach: ...

## Timeline (UTC)
| Time | Event | Source |

## Root cause
<one clear sentence>

## 5-Whys chain
Symptom → Why 1 → ... → Root cause

## Contributing factors
- ...

## Corrective actions
| Action | Type | Owner | Due |

## Preventative actions
| Action | Type | Owner | Due |

## Lessons learned
- ...
```

## Self-check

- [ ] Timeline is fact-based (no interpretation in the events column).

- [ ] 5-Whys chain reaches a systemic root cause (not "human error").

- [ ] Every corrective action has: owner, due date, type.

- [ ] Every preventative action has: alert / test / runbook / design category.

- [ ] Postmortem reviewed by all responders before publishing.

- [ ] Published within 48h (P0/P1) or 5 days (P2).

## Outputs

- Postmortem document (copy/paste-ready Markdown).

- Action items table with owners and due dates.

- Prevention tracking follow-up checklist.
