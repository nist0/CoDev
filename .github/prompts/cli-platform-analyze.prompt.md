---
name: cli-platform-analyze
description: "Full static analysis of a .NET CLI platform project -- reads GH workflow files, Bicep/infra, solution structure, CLI surface, test projects, and existing docs -- produces docs/project-context.md as the living context document. Phase 2 of the CLI platform onboarding workflow."
agent: "CLI Platform Onboarder"

argument-hint: "repo-root=<path, default: .>"
---

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Apply procedures from `.github/skills/cli-platform-analysis/SKILL.md`, `.github/skills/repo-understanding/SKILL.md`, and `.github/skills/github-actions/SKILL.md`.

Inputs:

- repo-root: ${input:repo-root:.}

**Prerequisite**: Phase 1 (Bootstrap) must be verified -- `validate-route-smoke.py` must have passed.

Single source of truth:

- Analysis workflow and section-by-section method are defined in `cli-platform-analysis`.

- Repository and workflow interpretation patterns are defined in `repo-understanding` and `github-actions`.

- Do not restate or redefine those procedures here.

Execution contract:

1. Execute Phase 2 analysis statically (no runtime execution).

2. Produce `docs/project-context.md` using the canonical skill structure.

3. Surface material gaps explicitly, including risk-tagged findings.

4. Emit a phase status block and a concise summary for handoff.

5. Provide the next command `/cli-platform-task task="<assigned task>"`.

Required outputs:

- `docs/project-context.md`

- Gap list and risk notes

- Phase status block

- <=10-line summary and next action

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **CLI Platform Onboarder** | always -- Phase 2 Analysis | *(this prompt)* | All 7 analysis steps complete, docs/project-context.md committed, <=10-line summary presented |
| 2 | **CLI Platform Onboarder** | analysis complete | `/cli-platform-task task=<assigned task>` | Task routed and executed (Phase 3) |
| 3 | **Security** | U+26A0U+FE0F gaps found (undocumented secrets, unpinned actions) | `/secrets-audit` or `/threat-model` | Gap issues opened, risk mitigated |
