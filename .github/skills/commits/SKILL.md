---
name: commits
description: Conventional Commits — type/scope/subject rules, commit size, merge strategy, and message quality checklist.
argument-hint: "[change description or commit scope]"
user-invocable: true

## disable-model-invocation: false

# Commits (Hygiene, Conventional Commits) (Elite)

## When to use

- You want consistent commit messages and history.

- You want readable changelogs and safe backports.

## Conventional Commit Types

| Type | When to use |
|------|-------------|
| `feat` | New feature visible to users |
| `fix` | Bug fix visible to users |
| `refactor` | Code change with no behavior change |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `docs` | Documentation only |
| `chore` | Maintenance (deps, CI, tooling) |
| `ci` | CI/CD pipeline changes |

## Format

```text
<type>(<scope>): <subject>

[body]

[footer]
```

- **Subject**: imperative mood, lowercase, ≤72 chars, no period.

- **Body**: explain *what* and *why*, not *how*.

- **Footer**: reference issues (`Closes #123`), breaking changes (`BREAKING CHANGE:`).

## Merge Strategy Reference

| Strategy | When to use |
|----------|-------------|
| Squash | Feature branch → clean history, single intent |
| Rebase | Linear history preferred, commits are atomic |
| Merge commit | Long-lived branches, preserve context |

## Workflow

### 1. Choose convention

- Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`

- Use scope for bounded contexts: `feat(api): ...`

### 2. Commit size

- Prefer small, focused commits; avoid "mega commits".

- One commit = one logical change; if message needs "and", split it.

### 3. History strategy

- Decide merge strategy: squash vs merge commits vs rebase.

- Document team choice in `CONTRIBUTING.md`.

### 4. Write and review

- Subject: imperative, ≤72 chars, no period.

- Body: explain motivation; link to issue or RFC.

- Footer: `Closes #N`, `BREAKING CHANGE: <description>`.

### 5. Verification

- CI green; link commits to issues where relevant.

## Self-check

- [ ] Type is from the standard list (see table).

- [ ] Subject is imperative mood, ≤72 chars, no trailing period.

- [ ] Commit represents a single logical change.

- [ ] Breaking changes marked with `BREAKING CHANGE:` in footer.

- [ ] Issues referenced in footer (`Closes #N`).

## Outputs

- Commit message template and examples.

- Recommended merge strategy options.

- Checklist for clean history.
