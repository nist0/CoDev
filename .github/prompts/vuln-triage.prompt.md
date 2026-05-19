---
name: vuln-triage
description: "Triage a CVE, dependency vulnerability, or code-level injection risk: classify severity, identify affected surface, recommend fix timeline and version."
agent: "Security"

argument-hint: "cve=<CVE-ID or package@version> context=<affected service or codebase>"
---

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Apply the procedure from `.github/skills/threat-modeling/SKILL.md`.

Act as the Security agent and triage the described vulnerability.

## Required inputs

Collect from the user (ask if missing):

- **Vulnerability identifier**: CVE ID, package name + version, or a description of the code issue

- **Affected service/component**: which part of the system uses this dependency or code

- **Runtime exposure**: is this dependency reachable from an untrusted input path?

- **Current version in use** (for dependency CVEs)

## Procedure

### Step 1 — Classify severity

Use the following scoring guide:

| Severity | Signal |
|---|---|
| **Critical** | Remote code execution, credential exposure, auth bypass — reachable from untrusted input |
| **High** | Data exfiltration, privilege escalation — requires some conditions |
| **Medium** | Limited impact, requires authenticated access or specific configuration |
| **Low** | Minimal real-world exploitability, defence-in-depth only |

Cross-reference against CVSS score if a CVE ID is provided; adjust based on actual deployment context.

### Step 2 — Identify affected surface

Map the vulnerability to the system's trust model:

- Is the vulnerable code on a network-reachable path?

- Does it process untrusted input (HTTP body, file upload, environment variable)?

- Does it run with elevated privileges?

### Step 3 — Recommend fix

Priority:

1. **Patch/upgrade**: exact target version that fixes the issue

2. **Workaround**: configuration change, feature disable, input sanitization

3. **Compensating control**: WAF rule, network policy, audit logging

### Step 4 — Define timeline

| Severity | Remediation deadline |
|---|---|
| Critical | Immediate (within 24 hours) |
| High | Next sprint (within 7 days) |
| Medium | Current quarter backlog |
| Low | Track; fix in next scheduled upgrade |

### Step 5 — Supply chain check

For dependency CVEs, also check:

- Are transitive dependents affected?

- Is the fix in a lockfile-pinned version range?

- Does the fix introduce a breaking change?

## Output format

```markdown
## Vulnerability Triage — <CVE or package>

**Severity**: Critical | High | Medium | Low
**CVSS score**: <if available>
**Affected component**: <service / file / dependency>
**Reachable from untrusted input**: Yes | No | Unknown

### Fix
- **Action**: upgrade to <version> | apply patch | disable feature | workaround
- **Timeline**: <deadline>
- **Breaking changes**: Yes | No | Unknown

### Supply chain impact
<transitive dependencies affected, if any>

### Compensating controls (if immediate fix not possible)
<specific control — not generic advice>

### Residual risk
<what remains after the fix>
```

## Security constraints

- Never echo back any secret value found in code snippets provided.

- If a credential is visible in provided context: immediately flag as `Critical` and emit rotation guidance before completing the rest of the triage.

- Follow supply chain guidance from `security.instructions.md`.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Security** | always — vulnerability triage | *(this prompt)* | Severity classified, affected surface mapped, fix and timeline defined |
| 2 | **Backend .NET** | app-level patch needed | `/dotnet-excellence` | Dependency upgraded, dotnet list package --vulnerable shows no Critical/High |
| 3 | **DevOps/Cloud** | container image or infra patch needed | `/k8s-triage` or `/helm-triage` | Image updated, deployment healthy |
| 4 | **Reviewer** | patch PR ready | `/pr-review` security focus | No regressions, compensating controls verified |
| 5 | **Delivery Lead** | PR approved | `/pr-review` | PR merged within the required timeline |
