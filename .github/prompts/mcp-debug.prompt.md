---
name: mcp-debug
description: "Debug MCP startup, discovery, auth, or invocation failures in VS Code or GitHub Copilot with a repro-first troubleshooting flow."
agent: mcp-specialist

argument-hint: "symptom=<what is failing> [host=<vscode|github-copilot|both>] [target=<config path or server name>]"
---

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Apply the procedure from `.github/skills/mcp-integration/SKILL.md`.

Goal: triage an MCP failure and produce ranked hypotheses, exact checks, the smallest likely fix, and one prevention step.

Inputs:

- symptom: ${input:symptom:what is failing - startup, tool discovery, auth, or tool invocation}

- host: ${input:host:vscode | github-copilot | both | unknown}

- target: ${input:target:server name, config path, or short description}

Single source of truth:

- MCP troubleshooting workflow and hypothesis-to-fix flow are defined in `mcp-integration`.

- Do not restate or redefine those procedures here.

Execution contract:

1. Gather missing repro facts.

2. Classify the primary failure bucket.

3. Produce ranked hypotheses and exact checks.

4. Propose the smallest likely fix.

5. Provide verification and one prevention action.

Required output sections:

- MCP debug plan summary

- Ranked hypotheses

- Checks and likely fix

- Verification

- Prevention

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **mcp-specialist** | always - MCP troubleshooting | *(this prompt)* | Ranked MCP debug plan produced |
| 2 | **Router** | user needs a broader next workflow | `/route <follow-up request>` | Correct next agent/prompt selected |
| 3 | **Reliability** | failure is broader than MCP and points to runtime/service behavior | `/triage-error` | General incident triage continues |
