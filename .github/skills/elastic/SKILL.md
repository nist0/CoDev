---
name: elastic
description: Elasticsearch/Kibana/ELK - KQL queries, dashboards, alerting rules, and log analysis workflow.
argument-hint: "[index pattern or log type]"
user-invocable: true

disable-model-invocation: false
---

# Elastic / Kibana / ELK (Elite)

## When to use

- Querying logs in Elasticsearch/Kibana.

- Building dashboards or alerting rules in Kibana.

- Using KQL or Lucene for log analysis.

## KQL Syntax Reference

| Pattern | Example |
|---------|---------|
| Exact match | `status: 500` |
| Wildcard | `message: *timeout*` |
| Range | `response_time > 1000` |
| AND/OR | `level: error AND service: api` |
| NOT | `NOT status: 200` |
| Phrase | `message: "connection refused"` |

## Workflow

### 1. Connect and orient

- Kibana > Discover or Lens.

- Select the correct index pattern and set time range to the incident window.

### 2. Apply KQL filters

- Start broad; narrow with `field:value`, `AND`/`OR`, wildcards.

- Pin useful filters for the session.

### 3. Drill into log entries

- Inspect individual log fields; look for correlation IDs, trace IDs.

- Use the `Fields` panel to identify high-cardinality fields.

### 4. Build visualization

- Use Lens for aggregation (count, avg, percentile), bucket, and metric charts.

- Save visualizations to a dashboard for the incident or recurring use.

### 5. Set up alert

- Kibana rule (Observability or Stack) or legacy Watcher.

- Alert on: error rate threshold, anomaly detection, SLO breach.

## Quick reference

### Elasticsearch REST API (Dev Tools / curl)

> Open Kibana ? **Dev Tools** ? Console, then paste these queries directly.

```sh
# --- Cluster health ---
GET _cluster/health?pretty
GET _cluster/stats?human&pretty
GET _cat/nodes?v&h=name,heap.percent,ram.percent,cpu,load_1m,node.role

# --- Index overview (sorted by size) ---
GET _cat/indices?v&s=store.size:desc&h=index,health,status,pri,rep,store.size,docs.count

# --- Shard state (find UNASSIGNED shards) ---
GET _cat/shards?v&h=index,shard,prirep,state,node&s=state

# --- Aliases ---
GET _cat/aliases?v

# --- Index settings + mapping ---
GET <index>/_settings
GET <index>/_mapping

# --- ILM (Index Lifecycle Management) ---
GET _ilm/policy/<policy>            # view a policy
GET <index>/_ilm/explain            # where an index sits in its lifecycle
POST <index>/_ilm/retry             # retry a failed ILM step

# --- Basic search (last 15 min) ---
GET <index>/_search
{
  "query": { "bool": {
    "filter": [{ "range": { "@timestamp": { "gte": "now-15m" } } }]
  }},
  "sort": [{ "@timestamp": { "order": "desc" } }],
  "size": 20
}

# --- Reindex / flush / refresh ---
POST <index>/_refresh
POST <index>/_flush
POST _reindex { "source": { "index": "old" }, "dest": { "index": "new" } }
```

### Elastic APM -- UI quick navigation

| Goal | Path in Kibana |
|------|----------------|
| Service inventory + error rate | APM ? Services ? pick service |
| Distributed trace (end-to-end) | APM ? Traces ? select trace ID |
| Slowest transactions by percentile | APM ? Services ? <service> ? Transactions ? sort by p99 |
| Error grouping with stack trace | APM ? Services ? <service> ? Errors |
| Correlate with anomaly / spike | APM ? Services ? <service> ? Correlations tab |
| Dependencies + downstream latency | APM ? Service Map |
| APM to Logs bridge | Trace view ? **Investigate ? View surrounding documents** |
| Active alerting rules | APM ? Services ? <service> ? Alerts |

### Common KQL patterns -- production incidents

```kql
# --- HTTP errors ---
http.response.status_code >= 500                        # all 5xx
http.response.status_code >= 400 AND NOT 404            # 4xx non-404
http.response.status_code: 502 OR 503 OR 504            # gateway errors

# --- Latency ---
transaction.duration.us > 5000000                       # > 5 s transactions
"slow" AND event.dataset: "apm.transaction"

# --- Service scope ---
service.name: "my-api" AND event.outcome: failure
labels.environment: production AND log.level: error

# --- Trace correlation ---
trace.id: "abc1234567890def"
transaction.id: "fedcba09876543210"

# --- Kubernetes context ---
kubernetes.namespace: "production" AND log.level: error
kubernetes.pod.name: <pod-prefix>*
```

## Self-check

- [ ] Time range scoped to the incident window (not "last 30 days" by default).

- [ ] Correlation ID or trace ID used to link requests across services.

- [ ] Unassigned shards checked via `_cat/shards` during degraded cluster state.

- [ ] ILM explain used when index growth or rollover looks stuck.

- [ ] Dashboard saved for repeatability.

- [ ] Alert threshold validated against baseline (not guessed).

- [ ] Alert notifications routed to correct channel (Slack, PagerDuty, etc.).

## Outputs

- KQL query examples.

- Elasticsearch REST API command set for cluster/shard triage.

- Dashboard setup checklist.

- Alert rule template.
