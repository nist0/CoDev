---
name: onboarding-factory
description: Generate a developer onboarding guide — setup, architecture, conventions, and contribution workflow.
argument-hint: "[repo-name] [team-conventions]"
user-invocable: true

disable-model-invocation: false
---

# Onboarding Factory (Elite)

## When to use

- Generating a developer onboarding guide for a repository.

- Documenting setup, architecture, and team conventions for new contributors.

- Reviewing and updating an existing onboarding guide.

## Procedure

### 1. Scan the repository

Collect:

| Item | Where to find |
|------|---------------|
| README | Root `README.md` |
| Setup steps | `README.md`, `Makefile`, `scripts/`, `docker-compose.yml` |
| Build/test commands | `package.json`, `Makefile`, `.github/workflows/` |
| Code structure | `src/`, top-level directories |
| CI configuration | `.github/workflows/` |
| Conventions | `.github/instructions/`, `.editorconfig`, `.github/copilot-instructions.md` |
| Dependencies | `package.json`, `*.csproj`, `pyproject.toml`, `go.mod` |
| Secret management | `.env.example`, vault/OIDC references |

### 2. Extract key content

- **Setup steps**: ordered, copy/paste-ready commands.

- **Build/test commands**: exact commands for local dev and CI.

- **Key modules**: top-level directories + 1-sentence description each.

- **Entry points**: `main`, API controllers, event handlers.

- **Team conventions**: branch naming, commit format, PR size limits, review SLA.

### 3. Draft the onboarding guide

Structure:

```markdown
# Onboarding: <Repo Name>

## Quick start
1. Clone: `git clone <url>`
2. Install deps: `<command>`
3. Copy env: `cp .env.example .env`
4. Run: `<command>`
5. Test: `<command>`

## Architecture overview
<module map>

## Key concepts
<glossary of domain terms>

## How to contribute
- Branch naming: ...
- Commit format: ...
- PR process: ...
- Code review expectations: ...

## Team conventions
- ...

## Troubleshooting
- Common issue 1: ...
- Common issue 2: ...
```

### 4. Add architecture overview

Produce a text diagram or Mermaid flowchart:

- Top-level modules and their responsibilities.

- Key data flows (request → handler → service → DB).

- External integrations (queues, APIs, identity providers).

### 5. Add PR workflow

- How to open a PR (branch from main, PR template, label).

- Review expectations (who reviews, SLA, number of approvals).

- Merge strategy (squash, rebase, or merge commit).

- CI gates to pass before merge.

### 6. Verify accuracy

- Follow the setup steps from scratch in a clean environment (or ask a new joiner to).

- Check that all commands are correct.

- Check that conventions reflect current team practice.

## Self-check

- [ ] All setup steps copy/paste-ready and verified.

- [ ] Architecture overview covers all top-level modules.

- [ ] Key data flows documented.

- [ ] Team conventions sourced from actual config files (not assumed).

- [ ] PR workflow matches current CI gates.

- [ ] Troubleshooting section covers the top 3 common issues.

## Outputs

- Onboarding guide (Markdown, copy/paste-ready).

- Setup checklist (numbered, verified).

- Architecture overview (text diagram or Mermaid).

- PR workflow summary.
