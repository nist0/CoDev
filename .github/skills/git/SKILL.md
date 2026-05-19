---
name: git
description: Elite Git workflow — branching discipline, conventional commits, safe rebasing, history hygiene, and conflict resolution.
argument-hint: "[branch-name] [issue-number]"
user-invocable: true

## disable-model-invocation: false

# Git (Elite Workflow)

## When to use

- You need consistent branching, commit, and PR habits enforced across a team.

- You need safe rebasing, conflict resolution, and audit-grade history hygiene.

- You are setting up or reviewing a Git governance baseline for a project.

## Procedure

### 1. Branch naming

Follow `<type>/<issue-id>-<slug>` exactly:

| Type      | Prefix     | Example                        |
| --------- | ---------- | ------------------------------ |
| Feature   | `feat/`    | `feat/42-add-routing-matrix`   |
| Bug fix   | `fix/`     | `fix/57-null-ref-on-dispatch`  |
| Chore     | `chore/`   | `chore/88-update-deps`         |
| Docs      | `docs/`    | `docs/14-skill-readme`         |
| Hotfix    | `hotfix/`  | `hotfix/99-prod-crash`         |
| Release   | `release/` | `release/v1.4.0`               |

Rules:

- Never commit directly to `main`/`master` or `develop`.

- Branches must be short-lived (close within the sprint/cycle).

- Delete remote branch after merge; prune stale local refs with `git remote prune origin`.

### 2. Commit hygiene (Conventional Commits)

Format: `<type>(<scope>): <imperative summary>` — max 72 chars subject line.

```text
feat(routing): add capability fallback rule to matrix
fix(reviewer): handle missing agent frontmatter gracefully
docs(skills): add elite procedures to pr-review SKILL.md
chore(deps): bump actions/checkout to v4.2.0
```

Rules:

- Use imperative mood ("add", not "added" or "adds").

- Reference issue in footer: `Closes #42` or `Refs #57`.

- No secrets, tokens, or credentials in any commit message or diff.

- Sign commits when repo policy requires it: `git commit -S`.

- Keep commits atomic: one logical change per commit.

- Amend or squash WIP commits before pushing for review.

### 3. Sync strategy

**Default: rebase onto target branch before opening a PR.**

```bash
git fetch origin
git rebase origin/main
# resolve any conflicts, then:
git rebase --continue
```

When to use merge instead:

- Long-lived integration branches where shared history matters.

- Explicitly required by team policy (`git merge --no-ff`).

Never force-push to shared branches (`main`, `develop`, release branches).

### 4. Pre-push quality gate (local hooks)

Recommended `.git/hooks/pre-push` actions (or use `pre-commit` / `husky`):

1. Run linter: `<linter> --check`

2. Run unit tests: `<test-runner> --fast`

3. Validate no secrets: `git diff HEAD --name-only | xargs detect-secrets-hook` (if installed)

### 5. Conflict resolution (step-by-step)

1. Start: `git status` — identify conflicting files.

2. For each conflict: open file, find `<<<<<<<`/`=======`/`>>>>>>>` markers.

3. Understand both sides before picking; do not blindly accept "ours" or "theirs".

4. Resolve: edit file to desired final state; remove all markers.

5. Stage: `git add <file>`.

6. Continue: `git rebase --continue` or `git merge --continue`.

7. Run full test suite before pushing.

8. If stuck: `git rebase --abort` or `git merge --abort` to reset safely.

### 6. Emergency hotfix procedure

```bash
git checkout main
git pull --rebase
git checkout -b hotfix/<issue-id>-<slug>
# apply minimal fix, test locally
git commit -S -m "fix(<scope>): <summary> — Closes #<id>"
# open PR targeting main with [HOTFIX] label
# after merge, tag: git tag -s v<x>.<y>.<z+1> -m "hotfix: <summary>"
git push origin --tags
```

### 7. History hygiene — audit commands

```bash
# Review last N commits
git log --oneline -20

# Who last changed a line
git blame -L <start>,<end> <file>

# Find when a regression was introduced
git bisect start
git bisect bad HEAD
git bisect good <known-good-sha>

# Check for large blobs that should not be committed
git rev-list --objects --all | sort -k 2 | uniq -f1 -d | sort -rn -k1
```

## Self-check

- [ ] Branch follows `<type>/<issue-id>-<slug>` convention.

- [ ] All commits use Conventional Commits format and reference an issue.

- [ ] No direct commits to protected branches.

- [ ] Branch rebased onto target before PR; no merge-commit noise.

- [ ] Pre-push local quality gate passed (lint + tests).

- [ ] No secrets or credentials in diff or commit messages.

- [ ] Conflict resolution verified with full test suite.

- [ ] Stale branch deleted after merge.

## Outputs

- Recommended branching and merge strategy for the project.

- Conflict resolution checklist (copy/paste-ready).

- PR hygiene checklist (link to `pr-review` skill).

- Hotfix runbook.
