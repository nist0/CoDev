---
name: docker
description: Docker production practices from Dockerfile authoring to CI image scanning, SBOM, and secure runtime defaults.
argument-hint: "[service] [context] [registry]"
user-invocable: true

disable-model-invocation: false
---

# Docker Skill

## 1) Dockerfile authoring

- Use multi-stage builds (`builder` → `runtime`) so compilers and package managers never ship in runtime layers.

- Order layers for cache reuse: copy dependency manifests first, restore/install, then copy source and build.

- Use `ARG` for build-time configurables and `ENV` only for safe runtime defaults; never place secrets in either.

- Keep `.dockerignore` strict (`.git`, `node_modules`, `bin`, `obj`, test artifacts, local secrets) to reduce context size and leak risk.

## 2) Base image selection

- Prefer minimal runtime images (distroless or Alpine where compatible) and validate libc/runtime compatibility.

- Pin base image by immutable digest for production (`image:tag@sha256:...`) and document update cadence.

- Track upstream CVE updates and refresh base images on a regular patch window (for example weekly).

- Keep builder and runtime image versions aligned (e.g., same major runtime version) to avoid ABI/runtime mismatches.

## 3) Docker Compose (local development only)

> Boundary: This section covers local development and integration-test usage only. Do not use Docker Compose for production orchestration — use Kubernetes/Helm instead.

- Declare explicit `depends_on` with health checks for startup ordering rather than sleep loops.

- Use named volumes for persistent state and bind mounts only for local development loops.

- Separate environment config per stage (`.env.dev`, `.env.staging`, `.env.prod`) and avoid committing secrets.

- Include restart policies and resource constraints suitable for local integration testing.

## 4) Security baseline

- Run as non-root and set least-privilege file ownership with `COPY --chown`.

- Prefer read-only root filesystem where the workload allows; mount writable tmp paths explicitly when required.

- Manage secrets externally (runtime secret stores, orchestrator secret objects, BuildKit secrets); never via `ENV` in Dockerfile.

- Add image scanning in CI (Trivy/Grype) with fail thresholds for critical/high findings.

## 5) CI integration

- Use `docker/build-push-action` with BuildKit cache (`cache-from`/`cache-to`) for faster incremental builds.

- Generate and publish SBOM/provenance attestations as part of release pipelines.

- Gate publish on tests + scan success; push tags only after all quality/security checks pass.

- Pin GitHub Actions versions and configure registry auth via OIDC or scoped tokens.

## Canonical Dockerfile template

```Dockerfile
# syntax=docker/dockerfile:1.7
FROM mcr.microsoft.com/dotnet/sdk:8.0@sha256:<pin-me> AS build
WORKDIR /src

# Cache-friendly dependency restore
COPY src/MyApi/*.csproj src/MyApi/
RUN dotnet restore src/MyApi/MyApi.csproj

# Copy source and publish
COPY . .
RUN dotnet publish src/MyApi/MyApi.csproj -c Release -o /out --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:8.0@sha256:<pin-me> AS runtime
WORKDIR /app
RUN addgroup --system app && adduser --system --ingroup app app
COPY --chown=app:app --from=build /out ./
USER app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/healthz || exit 1
ENTRYPOINT ["dotnet", "MyApi.dll"]
```

> Also define a `.dockerignore` file to exclude VCS history, local build artifacts, and secret files from build context.

## Anti-patterns and fixes

| Anti-pattern | Why it is risky | Recommended fix |
|---|---|---|
| `FROM <image>:latest` | Non-reproducible builds and surprise regressions | Pin explicit tag and digest |
| Single-stage Dockerfile with SDK/runtime together | Larger attack surface and image size | Split into build and runtime stages |
| Running as root in final image | Privilege escalation blast radius | Create non-root user and `USER` switch |
| `ENV API_KEY=...` in Dockerfile | Secret persists in image history | Inject at runtime or use BuildKit secrets |
| `COPY . .` before dependency install | Poor layer cache reuse, slower CI | Copy manifests first, install deps, then source |
| Missing `.dockerignore` | Secret/file leakage and large contexts | Add strict `.dockerignore` with denylist |
