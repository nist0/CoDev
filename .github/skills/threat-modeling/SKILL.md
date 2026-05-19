---
name: threat-modeling
description: "Step-by-step STRIDE threat modeling playbook: enumerate assets, map trust boundaries, identify and score threats, define mitigations, document residual risk."
argument-hint: "[system description] [trust boundaries]"
user-invocable: true

disable-model-invocation: false
---

# Threat Modeling — SKILL

## Trigger conditions

Use this skill when:

- Starting design on a new feature that handles sensitive data, authentication, or external inputs.

- Reviewing a PR that adds a new API endpoint, queue consumer, or external integration.

- Conducting a security review before a release.

- Investigating a security incident to understand the blast radius.

- Running `/threat-model` or `/vuln-triage` prompts.

---

## Procedure

### Step 1 — Asset enumeration

List all significant system assets before any threat analysis:

| Asset | Type | Data sensitivity |
|---|---|---|
| User database | Data store | PII, credentials |
| Payment API | External integration | Financial |
| JWT signing key | Secret | Critical |

**Asset types**: `data store`, `service`, `queue`, `secret`, `external API`, `file system`, `cache`

**Sensitivity levels**: `Public`, `Internal`, `Confidential`, `Critical`

---

### Step 2 — Trust boundary mapping

A trust boundary is any point where the privilege level, authentication context, or
network zone changes.

For each boundary, document:

```text
Boundary: <name>
  Crosses: <what data or commands traverse it>
  Initiating actors: <who/what starts the interaction>
  Current controls: <auth mechanism, encryption, rate limits>
  Missing controls: <gaps observed>
```

**Common boundaries**:

- Browser → Backend API (public internet)

- API → Database (internal network, credential-based)

- Service → External API (egress, API key or OAuth)

- User role → Admin role (privilege escalation path)

- CI pipeline → Production secrets (secret injection)

---

### Step 3 — STRIDE analysis per boundary

Evaluate all six STRIDE categories for every trust boundary identified in Step 2.

| Category | Threat question | Example |
|---|---|---|
| **S**poofing | Can an attacker impersonate a legitimate actor or service? | JWT without `iss` validation; DNS spoofing |
| **T**ampering | Can data be modified in transit or at rest without detection? | Missing HMAC on webhook; no DB integrity check |
| **R**epudiation | Can a user deny an action with no audit trail? | No structured audit log; log deletion possible |
| **I**nformation Disclosure | Can sensitive data reach unauthorized parties? | Stack traces in API responses; over-fetching |
| **D**enial of Service | Can availability be disrupted by resource exhaustion or flooding? | No rate limiting; unbounded query results |
| **E**levation of Privilege | Can an actor gain more rights than their role allows? | IDOR; missing authorization on admin endpoints |

For each applicable threat, record:

- Description of the concrete attack scenario

- Attack vector (network, physical, adjacent, local)

- Required attacker capability (unauthenticated, authenticated user, privileged insider)

---

### Step 4 — Threat scoring

Score each threat on a `likelihood × impact` matrix:

| | Impact: Low | Impact: Medium | Impact: High |
|---|---|---|---|
| **Likelihood: Low** | Low | Low | Medium |
| **Likelihood: Medium** | Low | Medium | High |
| **Likelihood: High** | Medium | High | Critical |

**Severity → action**:

| Severity | Action |
|---|---|
| Critical | Fix before release; escalate immediately |
| High | Fix in current sprint |
| Medium | Add to backlog; fix within quarter |
| Low | Document; fix in next scheduled hardening pass |

---

### Step 5 — Mitigation selection

For each `High` or `Critical` threat, select a specific, named control:

| Threat category | Concrete mitigations |
|---|---|
| Spoofing | Mutual TLS; strict JWT `iss`/`aud` validation; PKCE for OAuth |
| Tampering | HMAC signatures on messages; database-level row versioning; signed cookies |
| Repudiation | Structured audit log (actor, timestamp, resource, result); immutable log sink |
| Info Disclosure | Structured error responses (no stack traces); field-level encryption; least-privilege DB roles |
| DoS | Rate limiting per user/IP; circuit breakers; query result pagination with max-limit |
| Elevation of Privilege | RBAC enforcement on every endpoint; IDOR prevention via resource-scoped tokens |

**Rule**: every mitigation must name a specific API, pattern, or configuration — no generic advice.

---

### Step 6 — Residual risk statement

After mitigations are applied, document what remains and why it is accepted:

```text
Residual risk: <what threat remains>
Reason accepted: <business justification or compensating control>
Owner: <team or person responsible>
Review date: <when to re-evaluate>
```

---

### Step 7 — Output artifact: threat register

Produce the threat register table as the final deliverable:

| # | Asset | Boundary | STRIDE | Threat description | Severity | Mitigation | Residual risk |
|---|---|---|---|---|---|---|---|

---

## 🏆 Elite defaults — apply in every session

- **Assumption mapping**: before scoring, list all assumptions (e.g. "internal network is trusted") and assign confidence (H/M/L). Low-confidence assumptions become spikes.

- **Attack narrative**: for every Critical/High threat, write a one-paragraph attacker narrative ("An unauthenticated user sends a crafted JWT to..."). Narratives reveal gaps that tables miss.

- **Defense-in-depth layering**: for every Critical threat, require ≥2 independent controls. Single-control mitigations are insufficient.

- **Threat model as living document**: store the threat register in the repo (e.g. `docs/security/threat-model.md`); link it from the PR description for every feature that changes a trust boundary.

- **Insider threat layer**: always evaluate at least one threat scenario where the attacker is an authenticated insider with legitimate access. This surfaces missing audit controls and privilege-separation gaps.

---

Quick-reference: STRIDE mnemonic

> **S**poofing identity → authenticate everything
> **T**ampering with data → sign and verify
> **R**epudiation → audit every action
> **I**nformation disclosure → least privilege, encrypt in transit and at rest
> **D**enial of service → rate-limit, circuit-break
> **E**levation of privilege → authorize every request, not just authenticate
