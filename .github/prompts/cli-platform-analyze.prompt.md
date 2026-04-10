---
name: cli-platform-analyze
description: "Full static analysis of a .NET CLI platform project — reads GH workflow files, Bicep/infra, solution structure, CLI surface, test projects, and existing docs — produces docs/project-context.md as the living context document. Phase 2 of the CLI platform onboarding workflow."
agent: "CLI Platform Onboarder"
argument-hint: "repo-root=<path, default: .>"
---

Apply procedures from `.github/skills/cli-platform-analysis/SKILL.md`, `.github/skills/repo-understanding/SKILL.md`, and `.github/skills/github-actions/SKILL.md`.

Inputs:

- repo-root: ${input:repo-root:.}

**Prerequisite**: Phase 1 (Bootstrap) must be verified — `validate-route-smoke.py` must have passed.

Act as a CLI Platform Onboarder and execute **Phase 2 (Analysis)** using the `cli-platform-analysis` skill.

Run all 7 analysis steps in order, reading files statically — do not execute any project code:

1. **GitHub Workflow Analysis** — scan every file in `.github/workflows/`
2. **Infrastructure Analysis** — scan every `*.bicep`, ARM `*.json`, `*.tf`, `*.tfvars` file
3. **Solution Structure Analysis** — read `.sln`, every `.csproj`, `Program.cs`, `Directory.Build.props`
4. **CLI Surface Analysis** — catalog every command, handler, and side-effect
5. **Test Infrastructure Analysis** — identify test projects, frameworks, coverage gaps
6. **Existing Docs Analysis** — inventory `README.md`, `docs/`, `CHANGELOG`
7. **Produce `docs/project-context.md`** — combine all sections using the canonical structure from the skill

## Output requirements

- Produce `docs/project-context.md` with all 7 sections populated.
- Flag any gaps found during analysis as explicit items (not silent omissions).
- For each gap that represents a risk (undocumented secret, unpinned action, uncovered test area), note it with an ⚠️ marker and suggest a GitHub issue title.

## After producing the file, emit

```text
Phase: Analysis
Status: verified
Outputs: [docs/project-context.md]
Next action: /cli-platform-task task="<assign your task here>"
Blockers: <none | list any files that could not be read or sections that are incomplete>
```

## Then present the ≤10-line summary

```text
CI/CD toolchain   : <deduce from Step 1>
Deploy target     : <deduce from Steps 1+2>
CLI framework     : <deduce from Step 3>
Solution layers   : <deduce from Step 3>
Persistence       : <deduce from Step 3>
Environments      : <deduce from Step 2>
Test coverage     : <deduce from Step 5: good | partial | minimal>
Monitoring        : <deduce from Steps 1+2>
Top risk area     : <the most critical gap found>
Next action       : /cli-platform-task task="<your assigned task>"
```

## Self-check

- [ ] All 7 steps completed; no section is placeholder-only.
- [ ] CLI Surface table has at least one row per top-level command.
- [ ] Test Infrastructure section identifies gaps explicitly.
- [ ] All `${{ secrets.* }}` names captured (values never logged).
- [ ] All deployment environments identified.
- [ ] `docs/project-context.md` committed on the current branch.
- [ ] ≤10-line summary presented for review.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **CLI Platform Onboarder** | always — Phase 2 Analysis | *(this prompt)* | All 7 analysis steps complete, docs/project-context.md committed, ≤10-line summary presented |
| 2 | **CLI Platform Onboarder** | analysis complete | `/cli-platform-task task=<assigned task>` | Task routed and executed (Phase 3) |
| 3 | **Security** | ⚠️ gaps found (undocumented secrets, unpinned actions) | `/secrets-audit` or `/threat-model` | Gap issues opened, risk mitigated |
