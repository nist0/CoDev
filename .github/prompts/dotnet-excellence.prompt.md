---
name: dotnet-excellence
description: "Apply advanced .NET best practices with concrete examples, Microsoft references, and verification guidance."
agent: "Backend .NET"

## argument-hint: "scope=<module|files> goal=<hardening|refactor|performance|reliability>"

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Inputs:

- scope: ${input:scope:project/module/files to improve}

- goal: ${input:goal:hardening|refactor|performance|reliability}

- constraints: ${input:constraints:runtime/team/deadline constraints}

Requirements:

- Produce .NET best-practice recommendations grounded in repository conventions.

- Include concrete before/after examples where applicable.

- Include Microsoft documentation references for each major recommendation.

- Provide verification steps (local + CI) and rollback notes for risky changes.

- Label each recommendation with risk level and expected impact.

- Distinguish immediate remediation actions from follow-up hardening actions.

Output:

- prioritized improvement plan

- concrete examples

- references map (topic → Microsoft link)

- verification and rollback checklist

- facts versus assumptions split for diagnostics-driven recommendations

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Backend .NET** | always — .NET improvement | *(this prompt)* | Prioritized improvement plan produced with before/after examples |
| 2 | **Architect** | architecture-level recommendation triggered | `/explain-code` | Code review confirms no structural regression |
| 3 | **Architect** | test coverage gaps identified | `/test-plan` then `/write-tests` | New tests passing in CI |
| 4 | **Reviewer** | changes touch business-critical paths | `/pr-review` | No blocker findings |
| 5 | **Delivery Lead** | PR ready | `/pr-review` | PR approved, `dotnet build -warnaserror` exits 0 |
