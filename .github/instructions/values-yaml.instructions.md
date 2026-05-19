---
name: "Helm values.yaml Hygiene"
description: "Values file clarity: documentation, naming consistency, safe defaults."

applyTo: "**/values*.{yml,yaml}"
---

# values*.yml / values*.yaml Hygiene

## Naming & structure

- Keep value names consistent with their corresponding template references (`{{ .Values.image.tag }}`).

- Group related values under a common key (`image`, `service`, `autoscaling`) — no more than two nesting levels.

- Use `camelCase` for value keys; avoid underscores and hyphens in value names.

## Documentation

- Document every non-obvious value with an inline comment explaining what it controls and valid options.

- Document boolean toggles with their effect on production behavior (e.g. `# Set to true to enable HPA`).

- Mark required overrides explicitly: `# REQUIRED: set to your container registry URL`.

## Safe defaults

- Prefer safe, minimal-footprint defaults (small resource requests, replicas: 1, features disabled).

- Avoid surprising side effects when a feature toggle is enabled; document them.

- Never hardcode environment-specific values (registry URL, domain, TLS cert) in `values.yaml`; use environment-specific override files.

Example: well-documented values block
---

```yaml
# Number of pod replicas. Increase to 2+ for production HA.
replicaCount: 1

image:
  # REQUIRED: container registry and image name (e.g. ghcr.io/org/myapp)
  repository: myapp
  # Image tag. Override in CD pipeline with the build SHA.
  tag: "latest"
  pullPolicy: IfNotPresent

# Resource constraints. Tune per environment; never leave limits unset in prod.
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

---

## 🏆 Elite Section — Top 5% Values File Practices

- **`values.schema.json` as contract**: Maintain a JSON Schema alongside `values.yaml`. This provides IDE autocompletion, validates inputs at `helm install` time, and documents types/constraints formally.

- **Environment layering strategy**: Maintain a base `values.yaml` with safe defaults, and explicit per-environment files (`values.staging.yaml`, `values.prod.yaml`) that override only what differs. Never duplicate settings.

- **Secret references, not secret values**: Never put actual secrets in any values file. Reference secret names only (e.g. `secretName: myapp-db-creds`); store secrets in a vault, not in Git.

- **Change diff in PRs**: Use `helm diff` output as a required PR comment for any values change that affects production. Reviewers must approve the rendered diff, not just the YAML change.

- **Renovate for image tag bumps**: Configure Renovate with a `helm-values` manager to automate image tag update PRs when new container images are published.
