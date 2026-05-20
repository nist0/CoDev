# Contracts Skill -- Examples

## 1. OpenAPI Contract Skeleton

```yaml
openapi: 3.0.0
info:
title: Sample API
version: 1.0.0
paths:
/users:
get:
responses:
'200':
description: OK
```

## 2. Validate OpenAPI Contract (swagger-cli)

```text
npx swagger-cli validate api.yaml
```

## 3. Pact Contract Verification

```sh
npx pact-verifier --provider-base-url=http://localhost:8080 --pact-urls=./pacts/consumer-provider.json
```
