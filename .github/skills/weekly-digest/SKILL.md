---
name: weekly-digest
description: Produce a structured weekly tech watch digest — curated by topic, sourced from primaries, with actionable experiments.
argument-hint: "[topics] [week]"
user-invocable: true

## disable-model-invocation: false

# Tech Watch (Weekly Digest) (Elite)

## When to use

- Producing a weekly digest on tracked topics (dotnet, Kubernetes/AKS, observability, security, LLM tooling, etc.).

- Summarizing ecosystem changes with impact assessment and experiment proposals.

## Procedure

### 1. Define topics and priority order

| Priority | Topic | Signal sources |
|----------|-------|----------------|
| P1 | .NET / ASP.NET Core | GitHub releases, blog.dotnet.microsoft.com |
| P1 | Kubernetes / AKS | kubernetes.io/blog, AKS release notes |
| P2 | Observability | OpenTelemetry changelog, Grafana blog |
| P2 | Security | CVE feeds, GitHub security advisories, Semgrep blog |
| P3 | LLM tooling | GitHub Copilot changelog, model release notes |

Prioritize topics with `BREAKING` or `SECURITY` tags first.

### 2. Collect primary sources

Source qualification:

| Tier | Source type | Examples |
|------|------------|----------|
| Primary | Official release notes, papers, specs | GitHub releases, RFCs, CVEs |
| Secondary | Official blogs, docs | blog.dotnet.microsoft.com, kubernetes.io |
| Tertiary | Community summaries | Newsletters (reference with caveat) |

Do not use tertiary sources as primary evidence. If a claim comes from a tertiary source, label it as unverified.

### 3. Separate facts from interpretation

For each item:

| Fact | Interpretation | Confidence |
|------|---------------|------------|
| "Go 1.23 released with range-over-func" | "Enables more idiomatic iteration" | High |

Never present an interpretation as a fact.

### 4. Assess ecosystem risk

For items that affect current stack:

| Item | Breaking change? | Security impact? | Migration effort | Lock-in risk |
|------|-----------------|-----------------|------------------|--------------|

### 5. Draft the digest

```markdown
# Weekly Tech Watch — Week <N> (<YYYY-MM-DD>)

## 🚨 Breaking / Security
- <item>: <fact>. Impact: <interpretation>. Source: <link>.

## ⚡ Noteworthy
- <item>: <fact>. Why it matters: <interpretation>.

## 👀 On the radar
- <item>: <brief fact>.

## 🧪 Experiments this week
1. Hypothesis: ...
   Setup: ...
   Signal: ...
   Time-box: ...
```

### 6. Propose 1–3 experiments

For each experiment:

- **Hypothesis**: what do you expect to learn?

- **Setup**: minimal steps to run the experiment.

- **Signal**: what result confirms or refutes the hypothesis?

- **Time-box**: max time to invest (1–4 hours).

Prioritize experiments where confirmation has immediate team value.

## Self-check

- [ ] All facts sourced from Tier 1 or Tier 2 sources.

- [ ] Breaking / security items listed first.

- [ ] Facts and interpretations separated.

- [ ] Each experiment has hypothesis, setup, signal, and time-box.

- [ ] No tertiary source presented as primary evidence.

## Outputs

- Weekly digest (Markdown, copy/paste-ready).

- Experiments list (1–3) with hypothesis and time-box.

- Source list (primary preferred, labeled by tier).
