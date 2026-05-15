# Examples - rest-api-runtime-quality

## API readiness review

```text
/rest-api-review scope="Products API v1" focus="validation,error-handling,openapi,security,observability,tests"
```

Expected output:

- Risk-ranked findings.
- Specific remediation plan.
- Verification commands and release verdict.

## Runtime hardening pass

```text
/rest-api-review scope="Orders endpoints" focus="postgresql-concurrency,rate-limits,health-checks"
```

Expected output:

- Persistence/concurrency findings.
- Security and observability gaps.
- Concrete acceptance criteria for merge.
