---
name: "Helm Chart Hygiene"
description: "Helm chart conventions: renderability, values discipline, safe upgrades, and lint-friendly structure."

applyTo: "**/Chart.yaml"
---

# Helm Chart Hygiene

## Renderability

- Ensure the chart renders without errors via `helm template . -f values.yaml` with default values before every commit.

- Run `helm lint` in CI; treat warnings as errors for production charts.

- Use `helm unittest` for template unit tests when chart logic is non-trivial.

## Values discipline

- Keep values structured and documented; never rely on hidden implicit defaults.

- Every value that affects production behavior must have an inline YAML comment.

- Avoid deeply nested value trees; prefer flat or two-level groupings.

## Safe upgrades

- Avoid immutable field changes (e.g. Deployment selector labels) unless the resource is deleted and recreated explicitly.

- Use `helm.sh/resource-policy: keep` annotation for PVCs and secrets that must survive `helm uninstall`.

- If hooks are used, document their purpose, expected duration, and failure modes in `Chart.yaml` annotations or a `README`.

## Security

- Set `securityContext` defaults: `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`.

- Set resource `requests` and `limits` for every container; never leave them unbounded.

Example: values structure
---

```yaml
# values.yaml
image:
  repository: myapp
  tag: "1.0.0"   # Override in CI with the build SHA
  pullPolicy: IfNotPresent

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

# Set to true only in staging/prod; enables PodDisruptionBudget
ha:
  enabled: false
```

---

## 🏆 Elite Section — Top 5% Helm Practices

- **`helm-docs` for auto-generated docs**: Use `norwoodj/helm-docs` to generate `README.md` from values comments automatically. Enforce freshness in CI with `helm-docs --dry-run --diff`.

- **Schema validation with `values.schema.json`**: Define a JSON Schema for your `values.yaml`. Helm validates it on install/upgrade and rejects invalid inputs before they reach the cluster.

- **Immutable image tags in prod**: Never deploy `latest` to staging or production. Use immutable digest-pinned refs (`myapp@sha256:abc123`) via your CD pipeline.

- **Diff before upgrade**: Use `helm diff upgrade` (plugin) in CD pipelines to surface resource changes as a PR comment before applying them to production.

- **Multi-environment overlays with Helmfile**: Use `helmfile` to manage per-environment value overrides and release ordering instead of manual `--set` flags in CI scripts.

- **OPA/Gatekeeper policy compliance**: Validate rendered manifests against OPA policies (e.g. require `securityContext`, ban `hostNetwork`) in CI before deploying to any environment.
