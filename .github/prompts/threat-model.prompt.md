---
name: threat-model
description: "Run a structured STRIDE threat model on a described system: enumerate assets, map trust boundaries, identify and score threats, define mitigations and residual risk."
agent: "Security"

argument-hint: "system=<description> boundaries=<list> actors=<list>"
---

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Apply the procedure from `.github/skills/threat-modeling/SKILL.md`.

Act as the Security agent and run a complete STRIDE threat model for the described system.

## Required inputs

Collect from the user (ask if missing):

- **System description**: what the system does, its components, and data it handles

- **Trust boundaries**: where privilege or authentication changes (e.g. browser->API, API->DB, user->admin)

- **External actors**: who/what interacts with the system (users, services, third-party APIs)

- **Data sensitivity**: what categories of data are processed (PII, credentials, financial, public)

## Procedure

### Step 1 -- Asset enumeration

List all significant assets: data stores, services, queues, secrets vaults, external integrations.

### Step 2 -- Trust boundary map

For each boundary, describe:

- What crosses it (data, credentials, commands)

- Which actors initiate the crossing

- What authentication/authorization controls exist today

### Step 3 -- STRIDE analysis per boundary

For each boundary, evaluate all six STRIDE categories:

| Category | Question to ask |
|---|---|
| **S**poofing | Can an attacker impersonate a legitimate actor? |
| **T**ampering | Can data be modified in transit or at rest? |
| **R**epudiation | Can actions be denied without an audit trail? |
| **I**nformation Disclosure | Can sensitive data leak to unauthorized parties? |
| **D**enial of Service | Can availability be disrupted? |
| **E**levation of Privilege | Can an actor gain more rights than intended? |

### Step 4 -- Threat scoring

For each identified threat, score: `likelihood (H/M/L) × impact (H/M/L)` -> severity `Critical | High | Medium | Low`.

### Step 5 -- Mitigation selection

For each High/Critical threat: name a specific control (API, pattern, config).

### Step 6 -- Residual risk statement

What remains after mitigations and why it is accepted.

## Output format

```markdown
## Threat Model -- <system name>

### Assets
| Asset | Type | Data sensitivity |
|---|---|---|

### Trust boundaries
| Boundary | What crosses | Actors | Current controls |
|---|---|---|---|

### STRIDE analysis
| Boundary | Category | Threat description | Severity | Mitigation | Residual risk |
|---|---|---|---|---|---|

### Summary
Critical: N | High: N | Medium: N | Low: N

### Recommended next steps
1. <highest-priority action>
```

## Security constraints (always apply)

- Never output secrets, tokens, or credentials -- even as examples.

- Flag any finding that involves credential exposure as `Critical` immediately.

- Follow the threat surface template from `security.instructions.md`.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Security** | always -- STRIDE threat model | *(this prompt)* | Assets, trust boundaries, STRIDE analysis, and residual risk documented |
| 2 | **Security** | CVE or known dependency threat found | `/vuln-triage` | Vulnerability triaged, fix timeline set |
| 3 | **Backend .NET** | app-level mitigations needed | `/dotnet-excellence` | Controls implemented (auth, input validation, audit logging) |
| 4 | **DevOps/Cloud** | infra-level mitigations needed | `/k8s-triage` or `/helm-triage` | Network policies, RBAC, secrets rotation applied |
| 5 | **Delivery Lead** | mitigations committed | `/pr-review` security focus | PR approved, residual risk documented and accepted |
