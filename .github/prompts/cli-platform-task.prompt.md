---
name: cli-platform-task
description: "Execute an assigned task on the .NET CLI platform project using docs/project-context.md as preloaded context — routes, gathers task context, plans tests, implements, and ships. Phase 3 of the CLI platform onboarding workflow."
agent: "CLI Platform Onboarder"
argument-hint: "task=<description of assigned task>"
---

Apply procedures from `.github/skills/cli-platform-analysis/SKILL.md`, `.github/skills/dotnet-testing/SKILL.md`, `.github/skills/dotnet-cli/SKILL.md`, `.github/skills/delivery/SKILL.md`, and `.github/skills/github-actions/SKILL.md`.

Inputs:

- task: ${input:task:describe the assigned task exactly as given to you}

**Prerequisites**:

- Phase 1 (Bootstrap) verified.
- Phase 2 (Analysis) complete — `docs/project-context.md` exists and is committed.

**Preload `docs/project-context.md` now** before any analysis below.

Act as a CLI Platform Onboarder coordinating **Phase 3 (Task Execution)** for:

> **Task**: `{{task}}`

---

## Step 1 — Task routing

```text
/route <task description>
```

Output: capability + domain + recommended agent + skills. Confirm before proceeding.

---

## Step 2 — Task context (using docs/project-context.md)

Using the `## CLI Surface`, `## Solution Structure`, `## Test Infrastructure`, and `## Deduced Task Patterns` sections of `docs/project-context.md`, answer:

1. Which CLI commands and handlers are in scope?
2. Which extension points and domain models are touched?
3. Which existing tests already cover this area?
4. What is the minimal change surface — the files to read before writing any code?
5. What are the top 2 risk areas (breaking existing commands, schema changes, CI regressions, monitoring gaps)?
6. What observability is already emitted in this area, and what new instrumentation is needed?

---

## Step 3 — Test plan

```text
/test-plan scope=<area identified in Step 2> stack=".NET C# CLI"
```

Produce a test plan table: scenario → test type → why → notes.

---

## ⏸ REVIEW CHECKPOINT

**Do not proceed to Step 4 until the test plan above has been reviewed.**
The test plan must be approved (by you or a reviewer) before implementation begins.
Regression tests must be written to fail before the fix and pass after.

---

## Step 4 — Implementation

```text
@backend-dotnet Implement the changes identified in Step 2.

Conventions:
- Architecture direction: handler → application → domain → infrastructure. No domain logic in handlers.
- Apply dotnet.instructions.md and cli-platform.instructions.md for all C# files.
- Regression tests: must fail before the fix, pass after — non-negotiable.
- After implementation: dotnet build -warnaserror && dotnet test --no-build

If this task touches CI/CD workflows: apply github-actions skill security standards (SHA-pinned actions, minimal GITHUB_TOKEN permissions).
If this task touches Bicep files: run bicep build --lint before committing.
```

---

## Step 5 — Review and ship

```text
/pr-review
```

Verify all CI gates are green:

- [ ] `dotnet build -warnaserror` exits 0
- [ ] `dotnet test` exits 0
- [ ] `dotnet format --verify-no-changes` exits 0
- [ ] `dotnet list package --vulnerable` shows no Critical/High

Open the PR referencing the GitHub issue (`Closes #N`). Body written via `--body-file`.

If this task is release-gated:

```text
/release-plan scope=<feature> target-env=prod version=<vX.Y.Z>
```

---

## Phase status on completion

```text
Phase: Task Execution
Status: verified
Outputs: [<list changed files>, PR #N]
Next action: await next task assignment → /cli-platform-task task="<next task>"
Blockers: none
```

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **CLI Platform Onboarder** | always — task routing | `/route <task>` | Capability + domain + agent confirmed |
| 2 | **Architect** | test plan required | `/test-plan` | Test plan table reviewed and approved |
| 3 | **Backend .NET** | implementation phase | *(inline in Step 4)* | Code implemented, dotnet build -warnaserror + dotnet test green |
| 4 | **Delivery Lead** | implementation complete | `/pr-review` | All CI gates green, PR approved |
| 5 | **Delivery Lead** | release-gated task | `/release-plan` | Release plan produced and approved |
| 6 | **CLI Platform Onboarder** | task complete | Next `/cli-platform-task` | Phase status emitted, next task assigned |
