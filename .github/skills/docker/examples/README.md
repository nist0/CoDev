# Docker skill -- examples

## Worked example 1: .NET API (multi-stage, digest-pinned, non-root)

**User request**: "write a production Dockerfile for my .NET 8 web API"

**Expected routing**: capability `automation`, domain `devops-cloud`, agent `DevOps/Cloud`, skill `docker`

### Result: `Dockerfile`

```dockerfile
# syntax=docker/dockerfile:1.7
FROM mcr.microsoft.com/dotnet/sdk:8.0@sha256:<pin-digest-here> AS build
WORKDIR /src

# 1 - Restore dependencies separately for layer-cache reuse
COPY src/MyApi/*.csproj src/MyApi/
RUN dotnet restore src/MyApi/MyApi.csproj --locked-mode

# 2 - Copy source and publish
COPY . .
RUN dotnet publish src/MyApi/MyApi.csproj \
    -c Release -o /out --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:8.0@sha256:<pin-digest-here> AS runtime
WORKDIR /app

# 3 - Non-root user
RUN addgroup --system app && adduser --system --ingroup app app
COPY --chown=app:app --from=build /out ./
USER app

EXPOSE 8080

# 4 - Health check so orchestrators can verify liveness
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:8080/healthz || exit 1

ENTRYPOINT ["dotnet", "MyApi.dll"]
```

### Result: `.dockerignore`

```
.git
.github
.vscode
.vs
**/.DS_Store
**/bin
**/obj
**/*.user
**/node_modules
**/.env
**/*.pfx
**/*.key
**/*.pem
```

**Why each rule exists**:
- Layer order: `csproj` copied first so NuGet restore is cached when only source changes.
- Digest-pinned base image: `@sha256:...` guarantees reproducible builds and prevents upstream surprise updates.
- Non-root user: limits blast radius of any container escape or RCE.
- `.dockerignore`: excludes `.git` history, local secrets, and build artefacts from the build context, reducing context size and preventing accidental secret leakage.

---

## Worked example 2: Node.js app (multi-stage, non-root)

**User request**: "create a multi-stage Dockerfile for a Node 20 Express service"

```dockerfile
# syntax=docker/dockerfile:1.7
FROM node:20.5.0-bullseye-slim@sha256:<pin-digest-here> AS build
WORKDIR /src
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20.5.0-bullseye-slim@sha256:<pin-digest-here> AS runtime
WORKDIR /app
COPY --from=build /src/dist ./dist
COPY --from=build /src/node_modules ./node_modules
RUN groupadd --gid 1000 app \
 && useradd --uid 1000 --gid 1000 --no-create-home app
USER app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health',(r)=>process.exit(r.statusCode===200?0:1))"
CMD ["node", "dist/index.js"]
```

---

## Anti-patterns quick reference

| Anti-pattern | Risk | Fix |
| --- | --- | --- |
| `FROM node:latest` | Non-reproducible; surprise CVEs | Pin explicit tag + digest |
| Single stage with SDK+runtime | Larger image, bigger attack surface | Split build/runtime stages |
| `RUN apt-get install ... && rm ...` in runtime | Dev tools in runtime image | Install only in build stage |
| `ENV API_KEY=abc123` | Secret baked into image history | Inject at runtime or use BuildKit `--secret` |
| Missing USER instruction | Process runs as root | Create and switch to non-root user |
| `COPY . .` before `npm install` | Cache invalidated on any source change | Copy manifests first, install, then source |
| Missing `.dockerignore` | `.git`, `node_modules`, secrets in context | Always provide a `.dockerignore` |

---

## Expected routing shape

- Domain: `devops-cloud`
- Capability: `automation` (for authoring new Dockerfiles) or `code-analysis` (for reviewing existing ones)
- Agent: `DevOps/Cloud`
- Skill invoked: `docker`

