---
name: npm
description: npm Node tooling -- install strategy, standard scripts, lockfile discipline, CI gating, and troubleshooting.
argument-hint: "[project name or script task]"
user-invocable: true

disable-model-invocation: false
---

# npm (Node Tooling) (Elite)

## When to use

- You need consistent install/build/test scripts for JS/TS projects.

- You want reproducible CI runs.

## Standard Scripts Reference

```json
{
  "scripts": {
    "lint": "eslint . --max-warnings 0",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest",
    "build": "vite build",
    "ci": "npm run lint && npm run typecheck && npm run test && npm run build"
  }
}
```

## Workflow

### 1. Install strategy

- Use `npm ci` in CI for reproducibility (uses exact lockfile).

- Use `npm install` locally when adding/updating packages.

### 2. Scripts

- Standard scripts: `lint`, `typecheck`, `test`, `build`, `ci`.

- Keep CI script as a single gate: `npm run ci`.

### 3. Lockfile discipline

- Commit `package-lock.json`; review it in PRs.

- Avoid lockfile drift: never use `--no-package-lock`.

- Use `npm audit` in CI to catch vulnerabilities.

### 4. Troubleshooting

- Clear cache carefully: `npm cache clean --force` only when needed.

- Check node/npm versions match `.nvmrc` or `engines` field.

- `npm ls <package>` to find duplicate/conflicting versions.

### 5. CI gating

- Run lint + typecheck + tests on PR.

- Run build on main/release branches.

## Self-check

- [ ] `npm ci` used in CI (not `npm install`).

- [ ] `package-lock.json` committed and reviewed in PRs.

- [ ] `npm audit` runs in CI with a severity threshold.

- [ ] Node version pinned in `.nvmrc` or `engines` in `package.json`.

- [ ] All standard scripts (`lint`, `typecheck`, `test`, `build`) defined.

## Outputs

- Recommended npm scripts set.

- CI install/build/test checklist.

- Troubleshooting checklist.
