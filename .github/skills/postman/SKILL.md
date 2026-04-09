---
name: postman
description: Postman API collections — domain organization, environment strategy, test assertions, and CI integration.
argument-hint: "[API name or domain]"
user-invocable: true
disable-model-invocation: false
---

# Postman (API Collections) (Elite)

## When to use

- You want repeatable API request collections with environments.
- You want to validate API contract behavior manually or in CI.

## Collection Structure

```text
Collections/
  Auth/
    Login.request
    RefreshToken.request
  Users/
    GetUser.request
    CreateUser.request
Environments/
  Dev.environment
  Staging.environment
  Prod.environment
```

## Workflow

### 1. Organize by domain

- Group requests by bounded context (auth, users, orders, etc.).
- Use folders with descriptive names.

### 2. Use environments

- Separate environments for `dev`, `staging`, `prod`.
- Use environment variables for `{{base_url}}`, `{{auth_token}}`.
- Never hardcode secrets in collections.

### 3. Add tests

```javascript
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("User id present", () => pm.expect(pm.response.json().id).to.be.a('string'));
```

- Status code assertions, key field assertions, schema checks where possible.

### 4. Documentation

- Include description and examples per request.
- Document required auth and headers.

### 5. Version control and CI

- Export collections; commit to repo if required.
- Run with Newman in CI: `newman run collection.json -e env.json`.

## Self-check

- [ ] Collections organized by domain, not by HTTP method.
- [ ] No secrets hardcoded; all credentials via environment variables.
- [ ] Tests cover happy path + key error cases (400, 401, 404).
- [ ] Collections committed to repo or stored in team workspace.
- [ ] Newman CI step confirmed to run against test environment.

## Outputs

- Collection structure suggestion.
- Environment variable strategy.
- Repeatable validation checklist.
