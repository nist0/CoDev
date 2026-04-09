---
name: perf-regression
description: Performance regression triage — measure-first, baseline comparison, ranked hypotheses, mitigation, and alerting.
argument-hint: "[endpoint-or-service] [metric-and-threshold]"
user-invocable: true
disable-model-invocation: false
---

# Performance Regression Triage (Elite)

## When to use

- Latency p95/p99 increased, throughput dropped, CPU/memory spiked.
- You suspect a regression after a deployment or dependency upgrade.
- You need a measure-first plan (no speculative micro-optimizations).

## Procedure

### 1. Define the regression precisely

| Dimension | Value |
|-----------|-------|
| Metric | p50 / p95 / p99 latency / throughput / error rate / saturation |
| Before (baseline) | <value> at <timestamp or version> |
| After (current) | <value> at <timestamp or version> |
| Delta | <absolute and %> |
| Trigger | Deployment / config change / traffic spike / dependency upgrade |

Do not start investigation without a confirmed metric delta.

### 2. Establish scope

- Is the regression **global** (all endpoints / all users) or **scoped** (one tenant, one region, one endpoint)?
- Scope narrows the hypothesis space dramatically.

| Scope question | Tool |
|----------------|------|
| Which endpoint? | APM trace grouping |
| Which tenant/region? | Log filtering by tenant/region |
| Which pod/node? | `kubectl top pod` / Grafana node panel |

### 3. Collect profiling data

| Signal type | Tool | What to look for |
|-------------|------|------------------|
| Distributed traces | APM (Jaeger / Datadog / App Insights) | Top-duration spans |
| Logs | Log aggregation (ELK / Loki) | Timeouts, retries, errors |
| CPU / memory | `kubectl top` / node exporter | Throttling, OOM, GC |
| DB query plan | `EXPLAIN ANALYZE` / Query store | Sequential scans, missing indexes |
| External calls | APM dependency map | Slow downstream services |

### 4. Rank hypotheses

Order by `likelihood × (1 / cost to validate)`:

| Rank | Hypothesis | Validation step | Likely? |
|------|-----------|-----------------|--------|
| 1 | N+1 query introduced | Check APM DB span count per request | High |
| 2 | Missing DB index | `EXPLAIN ANALYZE` new query | High |
| 3 | Dependency slowdown | Compare external call duration before/after | Medium |
| 4 | CPU throttling (container limits) | `kubectl top pod` vs limits | Medium |
| 5 | GC pressure | Memory metrics, GC pause time | Low |

### 5. Choose fix approach

| Approach | Action | When |
|----------|--------|------|
| Mitigation | Rollback deploy / scale out / disable feature flag / add cache | Users impacted now |
| Remediation | Code fix / query optimization / index / config tuning | Root cause confirmed |
| Hardening | Alert / threshold / load test | Prevention |

Always lead with mitigation if users are impacted; ship remediation through PR review.

### 6. Verify fix

1. Confirm metrics return to baseline (same percentiles, same load).
2. Run a load test against the fix before promoting to production.
3. Add a performance regression test (baseline assertion in CI).
4. Add or update alert for this metric with threshold.

## Self-check

- [ ] Regression defined with before/after metric values and %delta.
- [ ] Scope established (global vs scoped).
- [ ] Profiling data collected before hypothesizing.
- [ ] Hypotheses ranked by likelihood × validation cost.
- [ ] Mitigation applied if users were impacted.
- [ ] Fix verified against baseline metrics.
- [ ] Performance regression test added.
- [ ] Alert configured.

## Outputs

- Regression definition + evidence (metric table).
- Top ranked hypotheses + validation steps.
- Mitigation plan + rollback option.
- Remediation approach.
- Verification checklist + alerting improvements.
