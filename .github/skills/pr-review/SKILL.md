---
name: pr-review
description: Elite PR review — multi-pass analysis, severity classification, instruction compliance, merge gate decision.
argument-hint: "[pr-number] [target-branch]"
user-invocable: true
disable-model-invocation: false
---

# PR Review (Elite)

## When to use

- You are reviewing a PR for correctness, security, and delivery readiness.
- You need a structured, evidence-based review with an explicit merge gate verdict.
- You want instruction/skill compliance checked per changed file type.

## Procedure

### Pass 1 — Orientation (understand before judging)

1. Read the PR description: does it clearly explain what, why, and how to verify?
2. Link to a GitHub issue; if missing, flag as `minor` blocker until added.
3. Note target branch (main/develop/release); apply stricter gates for `main`.
4. Skim file list: identify changed domains (infra, tests, docs, framework config, runtime code).

### Pass 2 — Correctness & logic

For each changed file:

1. Does the change match the stated intent in the PR description?
2. Are edge cases and failure paths handled (nulls, empty collections, auth failures)?
3. Are new dependencies justified? Check license compatibility.
4. Are there breaking changes to public interfaces? Flag as `blocker` if undocumented.
5. Does logic regress any existing behavior? Cross-reference with test suite.

### Pass 3 — Instruction compliance

Map `applyTo` globs from `.github/instructions/*.instructions.md` to changed files:

| File pattern  | Instruction file                         |
| ------------- | ---------------------------------------- |
| `**/*.cs`     | `dotnet.instructions.md`                 |
| `**/*.ts`     | `typescript.instructions.md`             |
| `**/*.tsx`    | `react.instructions.md`                  |
| `**/*.py`     | `python.instructions.md`                 |
| `**/*.sh`     | `bash.instructions.md`                   |
| `**/*.ps1`    | `powershell.instructions.md`             |
| `**/*.md`     | `docs-system.instructions.md`            |
| `.github/**`  | `customization-governance.instructions.md` |
| `workflows/`  | `github-actions.instructions.md`         |

For each applicable instruction: pass ✅ or fail ❌ with exact note.

### Pass 4 — Security & data handling

- No secrets, tokens, or credentials in diff (any file type).
- No sensitive data in logs or error messages.
- Least-privilege: new permissions are explicitly justified.
- Dependency additions: check for known CVEs (`npm audit`, `pip-audit`, `dotnet list package --vulnerable`).
- For `.github/` changes: verify no escalation of workflow permissions.

### Pass 5 — Tests

- Is there a test for the new or changed behavior?
- For bug fixes: does a regression test exist that fails before the fix?
- Are tests deterministic (no random seeds without fixed value, no time-dependent logic)?
- Is coverage maintained or improved?

### Pass 6 — Framework downgrade-risk check (for `.github/` changes only)

- Does this change remove or weaken any existing guidance, example, or skill procedure? → `blocker`
- Does this introduce duplication of an existing skill/agent/prompt? → `major`
- Does this contradict an existing instruction layer? → `blocker`
- Are routing files updated end-to-end (capabilities + matrix + aliases + domains when needed)? → `blocker` if incomplete.
- Review evidence and validator output must be scoped to tracked and non-ignored repository files only; ignore `external/` and all gitignored paths.

### Pass 7 — Performance & observability

- Do new code paths have sufficient logging/tracing at appropriate levels?
- Are there obvious O(n²) or unbounded loops introduced?
- Are expensive operations cached or deferred where appropriate?

### Pass 8 — Documentation & release notes

- Are public API/behavior changes documented in the appropriate docs file?
- Does the PR description include a "release notes" section if this is a user-facing change?
- Are new skills/agents/prompts registered in `README.md` and routing?

## Severity classification

| Severity  | Definition                                                                 | Merge policy             |
| --------- | -------------------------------------------------------------------------- | ------------------------ |
| `blocker` | Correctness bug, security issue, missing required gate, contradiction/removal | Must fix before merge   |
| `major`   | Important quality gap, missing tests for critical path, duplication        | Fix or accepted risk documented |
| `minor`   | Style, naming, optional improvement, non-critical doc gap                  | Fix or defer             |

## Merge gate decision

**Ready** when:

- [ ] No `blocker` findings remain.
- [ ] PR description links to a GitHub issue.
- [ ] All CI checks pass (lint, tests, security scan).
- [ ] Instruction compliance: all applicable files pass.
- [ ] For `.github/` changes: routing smoke tests pass (`python scripts/validate-route-smoke.py`).
- [ ] For `.github/` changes: customization registry valid (`python scripts/validate-customization-registry.py`).
- [ ] For `.github/` changes: README registry valid (`python scripts/validate-readme-registry.py`).

**Blocked** when any of the above are unmet. List exact blocking items.

## Output format (copy/paste-ready)

```markdown
## PR Review

**Verdict**: approved | rework required

### Summary of changes
<one paragraph>

### Findings

| # | Severity | File | Finding | Required fix |
|---|----------|------|---------|--------------|
| 1 | blocker  | path/to/file.ts | Missing null check on line X | Add guard before call |

### Instruction compliance

| Instruction file | Files checked | Result |
|-----------------|---------------|--------|
| dotnet.instructions.md | Foo.cs | ✅ pass |

### Framework downgrade-risk
none | <description if flagged>

### Merge gate
blocked: <list of blockers> | ready

### Merge action
do not merge | merge now (strategy: squash)
```

## Self-check

- [ ] All 8 passes completed; no pass skipped without stated reason.
- [ ] Every finding has a severity, file reference, and required fix.
- [ ] Instruction compliance table produced.
- [ ] Merge gate decision is explicit and justified.
- [ ] No claims made without evidence (file search or diff line reference).
- [ ] Validation scope respected: tracked and non-ignored files only, never `external/` or gitignored paths.

## Outputs

- Structured review notes (severities, file-level fixes).
- Instruction compliance table.
- Merge gate verdict with blocking reasons.
- Framework downgrade-risk assessment.
