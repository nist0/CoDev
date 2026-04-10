---
name: route-miss
description: "Feedback loop: capture a routing miss, diagnose root cause, propose an additive fix, and emit a ready-to-open GitHub issue."
agent: "Router"
argument-hint: "request=<original request that was misrouted> expected=<what you expected> got=<what you got>"
---
Apply the procedure from `.github/skills/canonical-routing/SKILL.md`.

Act as a Router performing a blameless routing retrospective.

## Input

Parse from `{{input}}`:

- **request** — the original free-text request that produced a wrong or empty route
- **expected** — what the user expected (capability / agent / prompt)
- **got** — what the router actually returned (or "nothing" / "wrong agent")

If any field is missing, ask for it before proceeding.

## Step 1 — Reproduce the miss

Restate the original request and the actual route result side by side:

```text
Request  : <request>
Expected : <expected capability + agent + prompt>
Got      : <actual capability + agent + prompt, or "no match">
```

## Step 2 — Diagnose root cause

Check each layer in order and identify the first failure:

| Layer | Check | Likely fix |
|---|---|---|
| **Alias** | Is there an alias in `routing/aliases.yaml` that matches this request's intent? | Add alias to existing capability |
| **Capability** | Does a capability exist for this kind of work? | Add a new capability |
| **Domain** | Is the domain signal present but not mapped to a dedicated rule? | Add domain-specific rule in matrix |
| **Matrix fallback** | Does the fallback agent handle this well, or would a specialist be materially better? | Add domain-specific matrix rule |
| **Prompt** | Is the right capability matched but the wrong prompt suggested? | Update prompts list in matrix rule |
| **Skill** | Is the agent correct but the skill set incomplete? | Add skill to existing rule |

State the root cause layer and the minimal fix.

## Step 3 — Propose the fix

Output a concrete, copy/paste-ready diff description (no actual diff syntax needed):

```text
Root cause : <layer> — <one-line explanation>

Proposed fix:
  File      : routing/<file>.yaml
  Change    : <add / update / remove>
  Detail    : <exact alias / rule / capability to add>

Additive only: this fix must not remove or modify existing rules.
```

## Step 4 — Emit a GitHub issue draft

Output a ready-to-open issue (English, markdown):

```markdown
<!-- Issue title: fix: routing miss — <short slug of original request> -->

**Symptom**
Request: `<request>`
Expected: `<expected>`
Got: `<got>`

**Root cause**
<one-paragraph diagnosis>

**Proposed fix**
- [ ] File: `routing/<file>.yaml`
- [ ] Change: <description>

**Acceptance criteria**
- [ ] `python scripts/validate-route-smoke.py` passes with a new case covering this request
- [ ] `python scripts/validate-customization-registry.py` passes
- [ ] `python scripts/validate-readme-registry.py` passes
- [ ] `python scripts/validate-routing-coverage.py` passes
- [ ] No existing smoke test broken

**Labels**: `routing`, `feedback-loop`, `good first issue`
```

## Rules

- Never delete or alter existing rules — additive fixes only.
- If the miss is genuinely ambiguous (multiple valid routes), say so and propose the tie-breaker heuristic.
- If no fix is needed (e.g. the "wrong" result is actually correct), explain why and close with "No change needed."
- Keep the issue draft under 30 lines — concise and actionable.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Router** | always — routing retrospective | *(this prompt)* | Root cause layer identified, minimal additive fix proposed, GitHub issue draft produced |
| 2 | **PromptSmith** | fix requires new/updated prompt or skill | `/new-skill`, `/prompt-from-theme`, or direct edit | New asset created and validated |
| 3 | **Router** | routing YAML updated | Run python scripts/validate-route-smoke.py | New smoke-test case passes, no existing cases broken |
| 4 | **Delivery Lead** | fix ready | `/pr-review` | PR merged, routing coverage improved |
