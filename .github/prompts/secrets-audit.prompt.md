---
name: secrets-audit
description: "Audit a file, PR diff, or codebase description for secrets, tokens, credentials, and private keys. Every finding is Critical — emit rotation guidance immediately."
agent: "Security"
argument-hint: "scope=<file path | PR diff | description of codebase area>"
---

Apply the procedure from `.github/skills/threat-modeling/SKILL.md`.

Act as the Security agent and perform a secrets audit on the provided scope.

## Critical rule

**Every finding in a secrets audit is automatically `Critical`.**
Do not wait until the end to flag findings — emit rotation guidance for each finding as soon as it is identified.

## Required inputs

Collect from the user (ask if missing):

- **Scope**: file path(s), PR diff, or a description of the codebase area to audit
- **Environment context**: which environment (dev / staging / prod) this secret may be active in
- **Secret types to prioritize**: API keys, database credentials, private keys, OAuth tokens, webhook secrets

## Procedure

### Step 1 — Pattern scan

Identify any of the following in the provided content:

| Type | Common patterns |
|---|---|
| API keys | `sk-`, `pk_`, `AKIA`, `ghp_`, long random strings in string literals |
| Database URLs | `postgres://`, `mysql://`, `mongodb+srv://` with embedded credentials |
| Private keys | `-----BEGIN RSA PRIVATE KEY-----`, `-----BEGIN EC PRIVATE KEY-----` |
| OAuth tokens | Bearer tokens, `access_token=`, `refresh_token=` in URLs or code |
| Webhook secrets | Hardcoded HMAC secrets, signing keys |
| Cloud credentials | AWS secret access keys, Azure connection strings, GCP service account JSON |
| Environment variable bypass | Secrets assigned inline (`API_KEY = "..."`) rather than via env |

### Step 2 — Confirm it is a real secret

Distinguish secrets from:

- Placeholder examples (`<YOUR_KEY_HERE>`, `REPLACE_ME`, `xxx`)
- Test/mock values in unit tests with clearly fake data (e.g. `"test-token-123"` in a test file)
- Public non-sensitive identifiers (e.g. public OAuth client IDs without secrets)

Document your reasoning for any ambiguous case.

### Step 3 — Emit findings immediately

For each confirmed finding:

1. Report location (file + line if available)
2. Type of secret
3. Severity: always `Critical`
4. **Rotation guidance** — specific steps to rotate this secret type
5. Remediation: how to replace with environment variable or secrets manager reference

### Step 4 — Root cause classification

After all findings:

- Was this a missing `.gitignore` entry?
- Was this a hardcoded value that should use `os.environ` / `IConfiguration` / Key Vault?
- Was this a test credential that escaped to production code?

### Step 5 — Prevention recommendations

Emit ≥1 concrete prevention control:

- `.gitignore` pattern to add
- Pre-commit hook (e.g. `detect-secrets`, `gitleaks`)
- CI gate rule
- Secrets manager migration path

## Output format

```markdown
## Secrets Audit — <scope>

### Findings

| # | Location | Secret type | Severity | Rotation action | Remediation |
|---|---|---|---|---|---|
| 1 | <file:line> | <type> | Critical | <rotate steps> | <env var / vault ref> |

> ⚠️ All findings are Critical. Rotate immediately before any other remediation step.

### Root cause
<classification from Step 4>

### Prevention
1. <concrete control>
2. <concrete control>

### Clean bill of health (if no findings)
No secrets detected in the provided scope. Recommend running `gitleaks` or `detect-secrets`
on the full commit history as a follow-up.
```

## Security constraints

- **Never echo back a found secret value** in the output — reference it by type and location only.
- Treat any ambiguous long random string (≥20 chars, high entropy) as a probable secret unless proven otherwise.
- Follow secrets hygiene rules from `security.instructions.md`.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Security** | always — secrets audit | *(this prompt)* | All findings reported, rotation guidance emitted per finding |
| 2 | **Security** | any finding confirmed | Emit rotation guidance immediately | Secret rotated in all environments before any other remediation |
| 3 | **Backend .NET** or **DevOps/Cloud** | remediation PR needed | `/dotnet-excellence` or `/automation-script` | Secret replaced with env var or secrets manager reference |
| 4 | **Reviewer** | remediation PR ready | `/pr-review` security focus | No new secrets, prevention controls added |
| 5 | **Delivery Lead** | PR approved | `/pr-review` | PR merged, secret no longer in git history (history rewrite if needed) |
