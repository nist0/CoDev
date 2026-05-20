---
name: apm
description: APM trace analysis -- latency hotspots, span breakdown, error correlation, and instrumentation improvements.
argument-hint: "[service] [time-range]"
user-invocable: true

disable-model-invocation: false
---

# APM (Application Performance Monitoring) (Elite)

## When to use

- Analyzing traces and transaction performance.

- Finding latency hotspots and correlating errors.

- Designing or improving instrumentation.

## Procedure

### 1. Set context

| Item | Value |
|------|-------|
| Service | <name> |
| Time range | <start> -> <end> |
| Trigger | Incident / regression / routine review |
| Baseline | Normal p95 latency: <value> |

### 2. Review transaction overview

```text
APM UI -> select service -> Transactions
```

- Sort by: p95 latency (descending) or error rate (descending).

- Identify: top 3 slowest transactions or highest error rate.

- Note: volume (req/min), p50/p95/p99, error %.

### 3. Drill into a slow trace

```text
Transaction -> select a slow sample trace -> span timeline
```

- Identify: **total duration** vs **sum of span durations** (gap = queuing/waiting).

- Find the **top contributing spans** by duration.

- Note: span type (DB, HTTP, queue, internal).

### 4. Identify top latency contributors

| Rank | Span | Type | Duration | % of total |
|------|------|------|----------|------------|
| 1 | SELECT * FROM ... | DB | 800ms | 40% |

For DB spans:

- Check SQL; run `EXPLAIN ANALYZE`.

- Look for: N+1 patterns (many identical queries), sequential scans, missing indexes.

For HTTP spans:

- Check: external API response time, timeout, retries.

For queue spans:

- Check: consumer lag, message processing time.

### 5. Correlate errors with trace IDs

```text
Filter by: error = true
Select error trace -> inspect exception and stack trace
Copy trace ID -> search in log aggregation (ELK/Loki/Log Analytics)
```

- Find first error in the chain (not the last propagated exception).

- Correlate with recent deployments or config changes.

### 6. Propose instrumentation improvements

| Gap | Improvement |
|-----|-------------|
| Missing custom spans | Add `Activity.StartActivity("name")` for key operations |
| No DB query text in span | Enable statement sanitization in APM agent config |
| Missing correlation ID | Propagate `X-Correlation-ID` header through HTTP clients |
| No user/tenant context | Add `baggage` or span attribute |

## Self-check

- [ ] Time range and service identified before analysis.

- [ ] Baseline latency established (before vs after comparison).

- [ ] Top 3 slow transactions identified.

- [ ] Span breakdown examined for slowest trace.

- [ ] Errors correlated with log entries via trace ID.

- [ ] Instrumentation gaps identified.

## Outputs

- Latency analysis summary (top transactions + percentiles).

- Top span contributors table.

- Error correlation findings.

- Instrumentation improvement checklist.
