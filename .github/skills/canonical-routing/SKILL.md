---
name: canonical-routing
description: Deterministic routing using capability + domain matrix — classification, fallback, and handoff.
argument-hint: "[user-request]"
user-invocable: true
disable-model-invocation: false
---

# Canonical Routing (Elite)

## When to use

- You want to decide which agent, prompt, and skills to use for a request.
- The request crosses multiple domains and needs a principled classification.
- You are building or validating routing rules in `routing/*.yaml`.

## Procedure

### 1. Request decomposition

1. Read the full request.
2. Extract the **primary intent** (the main action the user wants).
3. Extract the **context signals** (technology, repo area, platform, urgency).
4. If the request contains multiple distinct tasks: decompose and route each independently.

### 2. Capability classification

Match to a capability ID from `routing/capabilities.yaml`:

```text
engineering.debugging        → triage, crash, bug, stacktrace
engineering.code-analysis    → refactor, review, explain, architecture
engineering.testing-quality  → test, coverage, lint, quality gate
engineering.github-delivery  → PR, issue, review, merge, release
engineering.automation       → CI/CD, pipeline, workflow, script
engineering.docs             → onboarding, README, guide, doc
engineering.docs-system      → docs tree, DAM, doc architecture
engineering.postmortem       → incident, RCA, blameless, timeline
engineering.release          → tag, changelog, artifact, rollout
engineering.project-orchestration → project, plan, dispatch, kickoff
research.brainstorming       → brainstorm, alternatives, innovation
research.tech-watch          → digest, news, release notes, watch
```

### 3. Domain classification

Match to a domain ID from `routing/domains.yaml`:

```text
engineering.backend-dotnet   → .NET, C#, ASP.NET, EF Core, MediatR
engineering.frontend         → React, TypeScript, npm, CSS, Vite
engineering.devops-cloud     → AKS, Kubernetes, Helm, Docker, Azure
engineering.cicd             → GitHub Actions, workflows, pipeline
engineering.shell-automation → Bash, PowerShell, Python scripts, CLI
engineering.native           → C, C++, ASM, AVR, PIC, firmware
engineering.observability    → logs, traces, APM, Elastic, alerting
engineering.github-delivery  → issues, PRs, GitHub Projects
engineering.docs-system      → Markdown, onboarding, doc architecture
```

If context signals don’t match any domain: use `unknown`.

### 4. Matrix lookup

```text
routing/matrix.yaml
  try: capability + domain  → recommended agent, prompt(s), skill(s)
  fallback: capability only → recommended agent, prompt(s), skill(s)
  final fallback: project-orchestration → Project Orchestrator
```

Never invent a recommendation outside the matrix without noting it as a fallback.

### 5. Routing output

Always return:

- Selected capability ID.
- Selected domain ID (or `unknown`).
- Recommended agent.
- Recommended prompt(s).
- Recommended skill(s) (full path).
- Rationale: 1–3 bullets.
- Next actions: 1–3 concrete steps.

### 6. Routing maintenance

When a request cannot be routed (no matrix rule matches):

1. Flag the gap.
2. Propose a new rule: capability + domain → agent + prompts.
3. Provide a smoke-test phrase for `routing/route-smoke-tests.yaml`.
4. Handoff to PromptSmith to create the rule end-to-end.

## Smoke test validation

```bash
python scripts/validate-route-smoke.py
# Exit 0 = all smoke tests pass
# Exit 1 = routing gap or wrong agent recommended
```

## Self-check

- [ ] Capability matched to an ID in `routing/capabilities.yaml`.
- [ ] Domain matched to an ID in `routing/domains.yaml` (or `unknown` explicitly stated).
- [ ] Matrix rule exists; if not, gap flagged.
- [ ] Recommended agent exists in `.github/agents/`.
- [ ] Recommended prompt exists in `.github/prompts/`.
- [ ] Smoke tests pass after any routing change.

## Outputs

- Routing decision (capability + domain + agent + prompts + skills).
- Rationale and next actions.
- Routing gap report (if no matrix rule found).
- New rule proposal (when gap identified).
