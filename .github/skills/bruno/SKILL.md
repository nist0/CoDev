---
name: bruno
description: Bruno API testing -- collection structure, environment strategy, request standardization, response validation, CI integration.
argument-hint: "[domain or endpoint group]"
user-invocable: true

disable-model-invocation: false
---

# Bruno (API Testing Client) (Elite)

## When to use

- You want to test REST APIs with a lightweight, git-friendly client.

- You want repeatable API checks locally and in CI.

## Collection Structure

```text
collections/
  auth/
    login.bru
    refresh-token.bru
  users/
    get-user.bru
    create-user.bru
  ...
environments/
  dev.bru
  staging.bru
  prod.bru
```

## Workflow

### 1. Organize by domain

- Group requests by bounded context (auth, users, orders, etc.).

- Keep one request per file with a descriptive name.

### 2. Environment strategy

- Separate `dev`, `staging`, `prod` environment files.

- Store secrets as references to env variables (never hardcode tokens).

- Use `{{base_url}}` / `{{auth_token}}` placeholders.

### 3. Standardize requests

- Consistent headers (`Content-Type`, `Accept`, correlation IDs).

- Name requests descriptively: verb + resource (e.g., `POST create-user`).

### 4. Validate responses

- Assert status codes (`expect(res.status).to.equal(201)`).

- Assert key response fields and error schemas.

- Test both happy path and error cases.

### 5. Version-control and CI

- Commit collections to the repo alongside the API code.

- Run in CI with `bru run --env staging`.

## Self-check

- [ ] Collections organized by domain, not by method or endpoint pattern.

- [ ] No secrets hardcoded in `.bru` files; all credentials via env vars.

- [ ] Error cases tested (4xx/5xx), not just happy path.

- [ ] Collections versioned in repo alongside source code.

- [ ] CI step confirmed to run collection against test environment.

## Outputs

- Collection structure recommendation.

- Environment variables strategy.

- Repeatable API validation checklist.
