---
name: automation-script
description: "Create or improve automation scripts and CLI workflows."
agent: "Automation/Scripting"

## argument-hint: "task=<description> language=<bash|ps1|python|other>"

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Apply procedures from `.github/skills/bash/SKILL.md` and `.github/skills/powershell/SKILL.md`.

Inputs:

- task: ${input:task:what to automate}

- language: ${input:language:bash|ps1|python|other}

- constraints: ${input:constraints:idempotency, environment, safety constraints}

Act as the Automation/Scripting engineer and help with practical automation.
Output:

- script or workflow proposal

- safety/idempotency notes

- usage and verification steps

- risk level and rollback trigger

- failure modes and recovery notes

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Automation/Scripting** | always — script authoring | *(this prompt)* | Script produced, safety and idempotency notes included |
| 2 | **Reviewer** | script touches production systems or CI pipelines | `/pr-review` | No blocking findings, risk accepted |
| 3 | **Delivery Lead** | script merged into repo | `/release-plan` (if release-gated) | PR merged, CI green |
