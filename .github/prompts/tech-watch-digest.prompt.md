---
name: tech-watch-digest
description: "Tech watch digest: what changed, why it matters, what to try next week."
agent: "Tech Scout"

## argument-hint: "topics=<comma-separated list> period=<week|month>"

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

If `{{input}}` is empty, ask the user for the following in a **single message** before producing the digest:

1. **Topics** — comma-separated list of technologies, frameworks, or areas to cover (e.g. ".NET 10, GitHub Actions, Kubernetes")

2. **Period** — time window for the digest (`week` or `month`)

Do not produce the digest until the user has provided both topics and period.

If `{{input}}` is provided, extract topics and period directly from it.

Act as a Tech Scout and produce a digest for topics: {{input}}

Format:

- What changed

- Why it matters

- What to try next week (1–3 experiments)

- Primary sources preferred

- Facts vs interpretation split

- For each experiment: hypothesis, expected signal, and kill criteria

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Tech Scout** | always — digest production | *(this prompt)* | Digest produced: what changed, why it matters, experiments to try |
| 2 | **Project Orchestrator** | Action: Spike or Action: Adopt items found | `/project-dispatch` | GitHub issues opened for each actionable item within 48 hours |
| 3 | **Innovator** | bold/transformative technology identified | `/brainstorm` | Option portfolio with EV scores and kill criteria produced |
| 4 | **Security** | CVE advisory or Action: Migrate (security) | `/vuln-triage` | Vulnerability triaged, remediation timeline set |
