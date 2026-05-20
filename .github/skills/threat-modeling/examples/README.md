# Threat Modeling -- Examples

This directory contains worked examples for the `threat-modeling` skill.

---

## Example: REST API with PostgreSQL database

### System description

A simple order management service:

- React SPA (browser)

- ASP.NET Core REST API (public, HTTPS)

- PostgreSQL database (private subnet)

- Stripe payment API (external egress)

- JWT-based authentication (RS256, issued by an identity provider)

---

### Step 1 -- Assets

| Asset | Type | Sensitivity |
|---|---|---|
| Orders table | Data store | Confidential (PII + financial) |
| Users table | Data store | Confidential (PII, hashed passwords) |
| JWT signing key (public) | Secret | Internal |
| Stripe API secret key | Secret | Critical |
| ASP.NET API | Service | Internal |
| Stripe payment API | External API | Confidential |

---

### Step 2 -- Trust boundaries

```text
Boundary: Browser -> API
  Crosses: HTTP requests (JWT in Authorization header, JSON body)
  Actors: Anonymous users, authenticated users
  Current controls: HTTPS, JWT RS256 validation, CORS policy
  Missing controls: Rate limiting on auth endpoints

Boundary: API -> PostgreSQL
  Crosses: SQL queries, connection string with credentials
  Actors: ASP.NET Core application pool identity
  Current controls: Private subnet, parameterized queries (EF Core)
  Missing controls: Row-level security not enforced

Boundary: API -> Stripe
  Crosses: HTTPS POST with payment intent, Stripe secret key in header
  Actors: ASP.NET Core background service
  Current controls: HTTPS, Stripe API key in environment variable
  Missing controls: Webhook signature verification missing

Boundary: User role -> Admin role
  Crosses: Role claim in JWT
  Actors: Authenticated users
  Current controls: [Authorize(Roles = "Admin")] on admin endpoints
  Missing controls: Privilege audit log absent
```

---

### Step 3 + 4 -- STRIDE analysis and scoring

| # | Boundary | STRIDE | Threat | Likelihood | Impact | Severity |
|---|---|---|---|---|---|---|
| T1 | Browser -> API | S | Forged JWT with crafted `sub` claim if `iss` validation is missing | Medium | High | **High** |
| T2 | Browser -> API | D | Auth endpoint flooded without rate limiting -> account lockout or CPU exhaustion | High | Medium | **High** |
| T3 | API -> PostgreSQL | I | Row-level isolation missing: user A can query user B's orders via crafted `orderId` (IDOR) | Medium | High | **High** |
| T4 | API -> Stripe | T | Stripe webhook payload tampered (signature not verified) -> fraudulent order confirmation | Low | High | **Medium** |
| T5 | API -> Stripe | I | Stripe secret key logged in structured log output | Low | Critical | **High** |
| T6 | User -> Admin | E | Authenticated user accesses admin endpoint if role check is bypassable | Low | High | **Medium** |

---

### Step 5 -- Mitigations

| Threat | Mitigation | Specific control |
|---|---|---|
| T1 | Strict JWT validation | Validate `iss`, `aud`, `exp`; use `Microsoft.AspNetCore.Authentication.JwtBearer` with `ValidIssuer` + `ValidAudience` set |
| T2 | Rate limiting | `app.UseRateLimiter()` (.NET 7+); 5 requests/minute per IP on `/auth/login` and `/auth/refresh` |
| T3 | IDOR prevention | Scope all order queries to `WHERE UserId = @currentUserId`; add integration test asserting cross-user access returns 403 |
| T4 | Webhook signature | `StripeClient.ConstructEvent(payload, sigHeader, webhookSecret)` -- reject events without valid signature |
| T5 | Secret redaction | Add `Stripe` to structured log destructuring policy; never log `Authorization` headers |
| T6 | Authorization audit | Log all admin endpoint accesses (actor, endpoint, timestamp, result) to append-only audit table |

---

### Step 6 -- Residual risk

| Threat | Residual risk | Accepted because |
|---|---|---|
| T2 | Distributed DoS from multiple IPs still possible | WAF-level rate limiting is out of scope for this service; mitigated by cloud provider DDoS protection |
| T4 | Replay of valid Stripe events within the 5-min tolerance window | Stripe's tolerance window is non-configurable; idempotency key on order creation prevents duplicate processing |

---

### Threat register (final artifact)

| # | Asset | Boundary | STRIDE | Threat | Severity | Mitigation | Residual |
|---|---|---|---|---|---|---|---|
| T1 | JWT | Browser->API | S | Forged `sub` claim | High | Strict `iss`/`aud` validation | None after fix |
| T2 | Auth endpoints | Browser->API | D | Flood without rate limit | High | `UseRateLimiter` 5 req/min | DDoS at scale |
| T3 | Orders table | API->PostgreSQL | I | IDOR cross-user query | High | Scope queries to `UserId` | None after fix |
| T4 | Stripe webhook | API->Stripe | T | Payload tamper | Medium | `ConstructEvent` signature check | Replay within 5 min |
| T5 | Stripe key | API->Stripe | I | Key logged | High | Redact in log policy | None after fix |
| T6 | Admin endpoints | User->Admin | E | Role bypass | Medium | Audit log admin access | Insider with stolen admin token |
