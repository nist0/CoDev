---
name: supply-chain
description: Software supply chain hardening — dependency pinning, SBOM, artifact signing, provenance, and policy enforcement.
argument-hint: "[repository] [risk-level]"
user-invocable: true

## disable-model-invocation: false

# Supply Chain & Artifact Security (Elite)

## When to use

- Hardening the CI/CD supply chain (SBOM, signing, provenance).

- Securing container image builds and artifact publishing.

- Responding to a supply chain security advisory or audit.

## Procedure

### 1. Audit current state

Collect:

| Item | Check | Tool |
|------|-------|------|
| Dependency pinning | Are all deps pinned to exact versions (not ranges)? | `npm list` / `pip freeze` / `dotnet list package` |
| CVE exposure | Any known vulnerabilities in current deps? | `npm audit` / `pip-audit` / `dotnet list package --vulnerable` |
| GitHub Actions pinning | Are all actions pinned to SHA (not tag)? | `grep -r 'uses:' .github/workflows/` |
| Secrets in workflows | Any secrets logged or interpolated in shell? | Manual review + `trufflehog` |
| OIDC usage | Are long-lived credentials replaced with OIDC? | Review workflow auth steps |

### 2. Pin all dependencies

- Pin to **exact versions** (not `^` or `~` or `latest`).

- For GitHub Actions: pin to **full commit SHA** (not `@v3`).

- Automate dependency updates via Dependabot or Renovate with PR review gate.

### 3. Sign container images with Cosign + OIDC

```yaml
- name: Sign image
  uses: sigstore/cosign-installer@<sha>
  with:
    cosign-release: 'v2.x.x'
- run: |
    cosign sign --yes $IMAGE_REF
```

- Use **keyless signing** (OIDC; no static private key).

- Sign immediately after push; verify signature in CD before deploy.

### 4. Generate SBOM

```bash
syft packages dir:. -o spdx-json > sbom.spdx.json
grype sbom:sbom.spdx.json --fail-on high
```

- Attach SBOM to GitHub Release as asset.

- Store SBOM in artifact registry alongside container image.

- Fail the pipeline if `grype` finds HIGH or CRITICAL CVEs (configurable threshold).

### 5. Verify provenance in CD

```bash
cosign verify \
  --certificate-identity-regexp="<your-workflow-url>" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
  $IMAGE_REF
```

- Every deployment step must verify the artifact signature before deploying.

- Fail immediately if verification fails; never deploy an unverified artifact.

### 6. Enforce policy gates

| Layer | Tool | Policy |
|-------|------|--------|
| Kubernetes admission | OPA/Gatekeeper or Kyverno | Require signed image; block `:latest` |
| Registry | Harbor, ACR with content trust | Require signed image |
| GitHub Actions | Branch protection + required checks | Require supply chain job to pass |

### 7. Incident response (supply chain compromise)

1. Immediately revoke compromised credentials or tokens.

2. Pin or remove the compromised dependency.

3. Rebuild and resign all affected artifacts.

4. Audit all workloads that used the compromised artifact.

5. Produce a postmortem (use `rca-kit` skill).

## Self-check

- [ ] All dependencies pinned to exact versions.

- [ ] All GitHub Actions pinned to full commit SHA.

- [ ] No long-lived credentials; OIDC used for all cloud auth.

- [ ] Container images signed with Cosign keyless.

- [ ] SBOM generated and attached to every release.

- [ ] Provenance verified in every CD pipeline step before deploy.

- [ ] Policy gate (OPA/Kyverno) blocks unsigned images.

## Outputs

- Supply chain hardening checklist.

- Signing and SBOM CI/CD snippets (copy/paste-ready).

- Policy gate configuration guidance.

- Dependency audit report.
