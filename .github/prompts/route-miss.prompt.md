---
name: route-miss
description: "Feedback loop: capture a routing miss, diagnose root cause, propose an additive fix, and emit a ready-to-open GitHub issue."
agent: "Router"

argument-hint: "request=<original request that was misrouted> expected=<what you expected> got=<what you got>"
---

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Apply the procedure from `.github/skills/canonical-routing/SKILL.md`.

Act as a Router performing a blameless routing retrospective.

## Input

Parse from `{{input}}`:

- **request** — the original free-text request that produced a wrong or empty route

- **expected** — what the user expected (capability / agent / prompt)

- **got** — what the router actually returned (or "nothing" / "wrong agent")

Single source of truth:

- Routing-retrospective diagnosis flow and additive-fix policy are defined in `canonical-routing`.

- Do not restate or redefine those procedures here.

Execution contract:

1. Reconstruct request, expected route, and actual route.

2. Identify the first failing routing layer.

3. Propose the smallest additive fix in routing assets.

4. Emit a ready-to-open GitHub issue draft.

5. Include validation commands and acceptance checks.

Required output sections:

- Routing miss summary

- Root cause and minimal fix

- Issue draft body

- Validation checklist

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Router** | always — routing retrospective | *(this prompt)* | Root cause layer identified, minimal additive fix proposed, GitHub issue draft produced |
| 2 | **PromptSmith** | fix requires new/updated prompt or skill | `/new-skill`, `/prompt-from-theme`, or direct edit | New asset created and validated |
| 3 | **Router** | routing YAML updated | Run python scripts/validate-route-smoke.py | New smoke-test case passes, no existing cases broken |
| 4 | **Delivery Lead** | fix ready | `/pr-review` | PR merged, routing coverage improved |
