---
name: "Security & Compliance"
description: "Secure-by-default coding: secrets hygiene, least-privilege, threat modeling, supply chain."

applyTo: "**/*"
---

# Security & Compliance

## Secrets hygiene

- Never add secrets, tokens, API keys, or private keys -- even as placeholder examples.

- Use environment variables or secrets managers (e.g. Azure Key Vault, GitHub Secrets) -- never hardcode.

- Rotate any credential accidentally committed immediately; treat the commit as compromised.

## Input & data safety

- Validate all external input at the boundary (HTTP body, CLI args, env vars, config files).

- Sanitize before rendering to HTML, SQL, shell, or logs.

- Avoid logging PII, tokens, or stack traces in production-level verbosity.

## Least-privilege

- Scope IAM roles, DB permissions, and API scopes to the minimum required.

- Default to deny; explicitly allow only what is required.

- Isolate secrets per environment (dev != staging != prod).

## Dependency & supply chain

- Pin dependency versions in lockfiles (`package-lock.json`, `poetry.lock`, `packages.lock.json`).

- Enable Dependabot or Renovate for automated vulnerability alerts.

- Review changelogs for security fixes before upgrading major versions.

## Threat surface summary (include in PR descriptions for security-relevant changes)

```text
Threat surface changed: [auth / data access / secrets / network / dependency]
Risk: [Low / Medium / High]
Mitigation: [description of control added]
Residual risk: [what remains and why it is accepted]
```

## Examples

U+2705 Correct -- secret via environment:

```python
import os
api_key = os.environ["MY_SERVICE_API_KEY"]
```

U+274C Wrong -- hardcoded secret:

```python
api_key = "sk-abc123"  # NEVER do this
```

U+2705 Correct -- parameterized SQL:

```csharp
var user = await db.Users.FirstOrDefaultAsync(u => u.Id == userId, ct);
```

U+274C Wrong -- string interpolation in SQL:

```csharp
var sql = $"SELECT * FROM Users WHERE Id = '{userId}'"; // SQL injection
```

---

## U+1F3C6 Elite Section -- Top 5% Security Practices

- **Threat model every feature**: For any new data flow, draw a minimal data-flow diagram and identify trust boundaries. Document at least one abuse case per boundary.

- **Secrets rotation by design**: Services must tolerate secret rotation without restart -- use `IOptionsMonitor<T>` / dynamic reload patterns.

- **Zero-trust internal traffic**: Even internal service-to-service calls must be authenticated (mTLS, OIDC tokens) -- never assume internal = trusted.

- **Audit trail for sensitive operations**: Write, delete, and permission-change operations must produce structured audit log entries with actor, timestamp, resource, and result.

- **SAST in CI, not just PR**: Run static analysis (e.g. CodeQL, Semgrep) on every push to default branch -- not only on PRs.

- **Dependency hash pinning for CI actions**: Pin GitHub Actions by SHA, not tag: `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683`.
