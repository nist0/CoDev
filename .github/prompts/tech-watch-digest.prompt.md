---
name: tech-watch-digest
description: "Tech watch digest: what changed, why it matters, what to try next week."
agent: "Tech Scout"
argument-hint: "topics=<comma-separated list> period=<week|month>"
---
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
