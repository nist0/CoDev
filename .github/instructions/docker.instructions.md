---
name: "Dockerfile Production Authoring"
description: "Production-grade Dockerfile authoring guardrails for secure, reproducible, and cache-efficient images."

applyTo: "**/Dockerfile*"
---

# Dockerfile Production Authoring

> Boundary: This instruction governs Docker image build authoring only. Do not duplicate Kubernetes/Helm runtime deployment guidance here.

## Required rules

- Use **multi-stage builds** to separate build tooling from runtime and keep final images minimal.

- Create and run as a **non-root user** in the runtime stage (`USER <uid>:<gid>`), and ensure app files are accessible to that user.

- Include a repository-level **`.dockerignore`** to exclude build artifacts, VCS metadata, secrets, and local cache directories.

- Never bake secrets into image layers (`ENV`, `ARG`, or `RUN` with tokens). Use BuildKit secret mounts or runtime secret injection.

- Use `COPY --chown=<user>:<group>` (or equivalent ownership fix-up) to avoid root-owned artifacts in runtime layers.

- **Pin base image tags** (and prefer digest pinning for production) to guarantee reproducible builds.

- Order layers for cache efficiency: copy lockfiles/manifests first, install deps, then copy source.

- Ensure CI includes an **image scanning step** (e.g., Trivy or Grype) before publish/deploy.

## Procedure

- Follow the end-to-end implementation/checklist in `.github/skills/docker/SKILL.md`.
