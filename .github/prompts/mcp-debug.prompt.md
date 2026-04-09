---
name: mcp-debug
description: "Debug MCP startup, discovery, auth, or invocation failures in VS Code or GitHub Copilot with a repro-first troubleshooting flow."
agent: mcp-specialist
argument-hint: "symptom=<what is failing> [host=<vscode|github-copilot|both>] [target=<config path or server name>]"
---

Apply the procedure from `.github/skills/mcp-integration/SKILL.md`.

Goal: triage an MCP failure and produce ranked hypotheses, exact checks, the smallest likely fix, and one prevention step.

Inputs:

- symptom: ${input:symptom:what is failing - startup, tool discovery, auth, or tool invocation}
- host: ${input:host:vscode | github-copilot | both | unknown}
- target: ${input:target:server name, config path, or short description}

## Step 1 - Gather the repro facts

If details are missing, ask for them in one message only:

1. Exact symptom and expected behavior
2. Host: VS Code chat, GitHub Copilot custom agent, or both
3. Server model: local stdio or remote HTTP
4. Relevant config path or snippet
5. Any error output or logs already observed

## Step 2 - Classify the failure

Classify it as one primary bucket:

- startup failure
- discovery failure
- auth failure
- invocation failure
- trust/approval problem
- wrong-host or wrong-install-target problem

## Step 3 - Emit the debug plan

Output exactly this structure:

```markdown
## MCP debug plan

**Symptom**: <symptom>
**Host**: <vscode | github-copilot | both | unknown>
**Primary bucket**: <startup | discovery | auth | invocation | trust | wrong target>

### Ranked hypotheses
1. <hypothesis>
2. <hypothesis>

### Checks
1. <exact check>
2. <exact check>

### Likely fix
1. <smallest fix>

### Verification
1. <exact step>
2. <safe sample request>

### Prevention
- <one regression-prevention step>
```

## Rules

- Keep the troubleshooting flow repro-first and MCP-specific.
- Separate facts from hypotheses.
- Prefer the smallest fix that explains all observed symptoms.
- Call out trust and secret-handling problems explicitly.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **mcp-specialist** | always - MCP troubleshooting | *(this prompt)* | Ranked MCP debug plan produced |
| 2 | **Router** | user needs a broader next workflow | `/route <follow-up request>` | Correct next agent/prompt selected |
| 3 | **Reliability** | failure is broader than MCP and points to runtime/service behavior | `/triage-error` | General incident triage continues |
