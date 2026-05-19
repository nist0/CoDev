---
name: "Reliability Defaults"
description: "Repro-first debugging, measurement-first performance, blameless postmortems, observability standards."

applyTo: "**"
---

# Reliability Defaults

## Debugging workflow

Always follow this sequence — never skip to fix before reproducing:

1. **Reproduce** — get a minimal, deterministic repro (exact command, inputs, env).

2. **Observe** — collect logs, traces, and metrics from the failing state.

3. **Hypothesize** — list 2–4 ranked hypotheses with rationale.

4. **Validate** — test the top hypothesis; discard if it doesn't explain all symptoms.

5. **Fix** — make the smallest change that addresses root cause.

6. **Verify** — confirm fix with the original repro; run regression suite.

7. **Prevent regression** — add a test or alert so this failure class is detected automatically.

## Performance

- Measure first; avoid speculative micro-optimizations.

- Capture baseline metric before any change (latency p50/p99, throughput, memory).

- Document the before/after delta alongside the PR.

- Use load tests or benchmarks (e.g. `k6`, `BenchmarkDotNet`) for infrastructure-level changes.

## Observability standards

- Every service must emit: structured logs, distributed traces (with correlation IDs), and RED metrics (Rate, Errors, Duration).

- Alerts must be actionable: each alert must have a runbook link.

- Prefer histogram/percentile metrics over averages for latency.

## Postmortems

- Blameless: focus on systems, not individuals.

- Required sections: timeline, impact, root cause, contributing factors, action items.

- Action items must have owner and due date; track in the project backlog.

- Share postmortem within 5 business days of incident resolution.

Example: minimal repro template
---

```text
**Environment**: Docker / local / prod-like
**Repro steps**:
  1. `docker compose up -d`
  2. `curl -X POST http://localhost:8080/api/orders -d '{"qty":-1}'`
**Expected**: 400 Bad Request with validation error
**Actual**: 500 Internal Server Error, no body
**Logs**: [paste relevant log lines here]
```

---

## 🏆 Elite Section — Top 5% Reliability Practices

- **SLO-driven development**: Define SLO (e.g. 99.9% availability, p99 < 300 ms) before shipping a feature. Every alert threshold derives from the error budget.

- **Chaos engineering cadence**: Run controlled fault-injection experiments (e.g. Chaos Monkey, `toxiproxy`) on a scheduled basis — not only after incidents.

- **Instrumented rollbacks**: Every deployment must have a documented, tested rollback procedure that is faster than the incident SLA.

- **Correlation-ID end-to-end**: Trace IDs must flow from client request through every downstream call and appear in every log line — no orphaned log entries.

- **Canary + feature flags**: Release new behavior behind flags; route 1–5% of traffic before full rollout. Never do big-bang deploys for stateful changes.

- **Game days**: Conduct quarterly game days where the team deliberately breaks systems to validate runbooks, alerts, and on-call readiness.
