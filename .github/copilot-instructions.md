# Copilot Instructions (CoDev)

## 1) Fast start (always do this first)

- Use `/route` to classify the request via capability + domain.

- Then follow the recommended agent, prompt, and skills from routing.

- Prefer deterministic outputs: plan -> files changed -> rationale -> self-check.
Example:

```text
/route I need to debug a CrashLoopBackOff on my AKS pod
```

## 2) What this repository is

- This repo is a Copilot customization framework (not an application runtime).

- The core system is YAML-driven routing: capability + domain -> agent/prompt/skills.

- Treat `routing/*.yaml` as source-of-truth; avoid hardcoding behavior in ad hoc docs.

## 3) Architecture map (big picture)

- `routing/` = classification and recommendation engine.

- `capabilities.yaml`: what kind of work is requested.

- `domains.yaml`: where it applies (keywords/context).

- `aliases.yaml`: natural-language triggers.

- `matrix.yaml`: final handoff mapping and precedence.

- `.github/agents/*.agent.md` = role contracts (responsibilities + output format).

- `.github/prompts/*.prompt.md` = slash-command entry points bound to agents.

- `.github/skills/<theme>/SKILL.md` = reusable procedural knowledge.

- `.github/instructions/*.instructions.md` = always-on standards by `applyTo` glob.

## 4) Routing behavior that matters

- Routing precedence is deterministic:

1. try capability + domain rule

2. fallback to capability-only rule

3. if no capability can be classified, fallback to `Project Orchestrator`

- Canonical implementation references:

- `.github/prompts/route.prompt.md`

- `.github/agents/router.agent.md`

- `routing/matrix.yaml`

### Natural-language routing (important)

- Natural-language routing is operational when using `/route` with free-form requests.

- Users do **not** need to explicitly call an agent in normal flow.

- Users do **not** need exact keywords, but matching terms from `routing/aliases.yaml` and `routing/domains.yaml` improves classification confidence.

- Recommended pattern for deterministic results:

- `/route <request>` -> follow suggested agent/prompt/skills.

- Explicit agent invocation is optional and mainly useful when the user already knows the exact specialist they want.

## 5) Project-specific authoring conventions

- Keep framework assets modular:

- prefer skills/prompts over bloating agents/instructions.

- Follow frontmatter and structure patterns in scaffold prompts:

- `.github/prompts/new-agent.prompt.md`

- `.github/prompts/new-skill.prompt.md`

- `.github/prompts/new-instructions.prompt.md`

- Omit `tools` on new agents unless tools are explicitly required.

- Keep IDs and naming consistent: short kebab-case IDs (no `engineering.` / `research.` prefix), kebab-case files.

## 6) Change workflow for framework updates

1. Start with a short plan (<=10 bullets).

2. Use small, reviewable diffs.

3. For capability changes, update all related routing files together:

- `routing/capabilities.yaml`

- `routing/domains.yaml` (if domain changes)

- `routing/aliases.yaml`

- `routing/matrix.yaml`

4. If adding a skill, include `examples/README.md`.

5. Re-check cross-links:

- prompt `agent:` value exists in `.github/agents/`

- matrix agent IDs and prompt names exist

- instructions `applyTo` scope is tight and non-overlapping

## 7) Validation workflow (no hidden build system)

- Validate behavior with routing smoke tests using realistic phrases:

- "bug in AKS"

- "write tests for React"

- "release plan"

- "generate docs tree"

- For each phrase, verify:

- selected capability is expected

- selected domain is expected

- handoff agent/prompt/skills match `routing/matrix.yaml`

- Run validation scripts before PR:

- `python scripts/validate-route-smoke.py`

- `python scripts/validate-customization-registry.py`

- `python scripts/validate-readme-registry.py`

- `python scripts/validate-routing-coverage.py`

- Validation scope is mandatory: when validating CoDev, analyze tracked and non-ignored repository files only. Never analyze `external/` or any gitignored path.

## 8) Existing capabilities (source: `routing/capabilities.yaml`)

- `routing`

- `debugging`

- `postmortem`

- `code-analysis`

- `docs`

- `docs-system`

- `testing-quality`

- `github-delivery`

- `release`

- `automation`

- `mcp`

- `project-orchestration`

- `brainstorming`

- `tech-watch`

- `codev-management`

- `bot-engineering`

- `rest-api-engineering`

## 9) Existing domains (source: `routing/domains.yaml`)

- `backend-dotnet`

- `devops-cloud`

- `observability`

- `native`

- `frontend`

- `scripting`

- `shell-automation`

- `cicd`

- `github-delivery`

- `project-orchestration`

- `docs-system`

- `bot-platforms`

## 10) Prompts and procedures worth reusing

- `/route`

- use planner/implementer/reviewer split for multi-step work

- `/triage-error`, `/logs-analysis`, `/apm-analysis`, `/postmortem`

- `/k8s-triage`, `/helm-triage`

- `/test-plan`, `/write-tests`, `/linters-stack`, `/pr-review`, `/release-plan`

- `/project-kickoff`, `/project-dispatch`, `/project-governance`

- `/generate-onboarding`, `/generate-docs-tree`, `/doc-lint-fix`

- `/mcp-setup` - gather MCP topology, install target, trust/auth constraints, and emit a concrete setup plan for VS Code or GitHub Copilot

- `/rest-api-new-service` - design a controller-first ASP.NET Core REST API blueprint with CQRS + IMediator and quality gates

- `/rest-api-add-resource` - add a new resource to an existing API with contract consistency and OpenAPI updates

- `/rest-api-review` - audit and improve API quality across validation, ProblemDetails, persistence, security, observability, and tests

- `/mcp-analyze` - review an existing MCP design or configuration for topology, least privilege, and host fit

- `/mcp-debug` - troubleshoot MCP startup, discovery, auth, and invocation failures

- `/diagram-ops`, `/markdown-ops`

- `/new-agent`, `/new-skill`, `/new-instructions`, `/new-theme-pack`, `/prompt-from-theme`

- `cloud-web-hosting` - reusable skill for Azure Static Web Apps, Azure Container Apps Consumption, Azure SQL Database Free Tier, and Cloudflare DNS workflows

- `/quickstart` — onboard a new user: gather role + domain + goal, select a contributor profile, and emit a first-command card

- `/session-handoff` - package the current chat into a copy-paste or file-based continuation handoff, or initialize a new session from a saved handoff file

- `/route-miss` — feedback loop: diagnose a bad route and emit a ready-to-open fix issue
Routing boundary for brainstorming-heavy work:

- Start with `Innovator` + `/brainstorm` for idea generation, portfolio scoring, and spikes.

- Hand off to `Project Orchestrator` when you need issue decomposition, Kanban governance, and execution review gates.

## 11) Safety and quality defaults

- `/dotnet-excellence`

- `/rest-api-new-service`, `/rest-api-add-resource`, `/rest-api-review`

- Never add secrets/tokens/keys (including examples).

- Keep instruction layering additive and non-contradictory.

- For bug fixes: include regression-test intent and verification steps.

- Include concise rationale and quick self-check with framework edits.

- For brainstorming requests: include agent-participant summary, issue-ready tasks, project mapping, and specialist review lines that start with `(Agent: <name>)`.

- For any new GitHub publication (issues, PR descriptions, comments, reviews), use English.

## 11a) GitHub CLI body authoring — BLOCKING rule

>
> ⛔ **Never use `--body "..."` for any multi-line `gh` command in PowerShell.**
>
> PowerShell's backtick (`` ` ``) is its escape character inside double-quoted strings.
>
> Every inline code span (e.g. `` `value` ``) is silently mangled — the backtick is
>
> consumed and adjacent letters may be eaten (e.g. `` `backend-dotnet` `` → `ackend-dotnet`).
**Mandatory pattern for every `gh issue create`, `gh pr create`, `gh pr edit`, `gh issue comment`:**

```text
## 1. Single-quoted heredoc — nothing is ever escaped or interpreted
$body = @'
## Your markdown here
Tables, `backtick spans`, and \backslashes all survive intact.
'@
## 2. Write to a temp file
$body | Set-Content -Path "$env:TEMP\body.md" -Encoding UTF8
## 3. Pass via --body-file
gh issue create --title "..." --body-file "$env:TEMP\body.md"
## 4. Clean up
Remove-Item "$env:TEMP\body.md"
## 5. MANDATORY spot-check — look for stray \ or missing backtick spans
gh issue view <N>   # or: gh pr view <N>
```

If the spot-check reveals corruption: close the issue/PR immediately and re-create using this pattern.

## 11b) Mandatory dev workflow (enforced — no exceptions)

Every change, regardless of size, **must** follow this sequence:

0. **Brainstorm first** (mandatory for non-trivial tasks) — before any issue, branch, or code.
   Non-trivial = touches >1 file, new pattern, user-facing impact, or >30 min effort.
   Run the Innovator agent or `/brainstorm`. Produce ≥ 3 scored options (safe/adjacent/bold).
   The chosen finalist's rationale becomes `## Technical approach` in the issue.
   Exempt: single-file typo, doc-only reword, plain config toggle.

1. **Create a detailed GitHub issue** before writing any code (task + sub-tasks).
   The issue body **must** include: `## Summary`, `## Technical approach`, `## Files to modify`,
`## Sub-tasks`, `## Acceptance criteria`, `## Verification steps`, and `## Progress log`.
   See the full required template in `00-core.instructions.md` § Mandatory development workflow.

- **Project board** (mandatory): immediately after creating the issue, add it to the CoDev project Kanban board (project #2) and keep its status column in sync throughout the lifecycle:

```text
 - *Created* → **Todo**: `gh project item-add 2 --owner nist0 --url <issue-url>`
 - *Branch created / work started* → **In Progress**: `gh project item-edit --id <item-id> --field-id PVTSSF_lAHOAOYJIs4BQzk2zg-0dUk --project-id PVT_kwHOAOYJIs4BQzk2 --single-select-option-id 47fc9ee4`
 - *PR merged / issue closed* → **Done**: `gh project item-edit --id <item-id> --field-id PVTSSF_lAHOAOYJIs4BQzk2zg-0dUk --project-id PVT_kwHOAOYJIs4BQzk2 --single-select-option-id 98236657`
```

2. **The issue is a living document** — amend `Technical approach`, `Files to modify`, and `Progress log`
   whenever scope, approach, or blockers change. Use `gh issue edit <N> --body-file <path>` for updates.

3. **Work on a branch** — `feat/<slug>`, `fix/<slug>`, `chore/<slug>`. **Never commit directly to `main`.**

4. **Open a PR** — reference the closing issue(s) with `Closes #N`.

5. **Review before merge** — explicit verdict: `approved` or `rework required`.

6. **All GitHub checks must be green** — no PR merges with any failing check (lint, tests, CI gates, markdown lint, validators). Fix the root cause; do not skip or suppress checks.

7. **Verify AC before closing** — before an issue is closed (manually or via PR merge), confirm every acceptance-criteria checkbox in the issue body is ticked. Update unchecked boxes with `gh issue edit <N> --body-file <path>`. Never leave unchecked boxes on a closed issue.

> Violations (direct push to `main`, merge with failing checks) are blocking findings in any review.
>

## 12) Quick extension checklist (copy/paste)

- [ ] Brainstorm completed (≥ 3 scored options) before any issue or code — skipped only for exempt tasks

- [ ] GitHub issue(s) created with all required sections (Summary, Technical approach, Files to modify, Sub-tasks, AC, Verification steps, Progress log) — body written via `--body-file` (single-quoted heredoc), spot-checked with `gh issue view`

- [ ] Issue added to project board #2 (`gh project item-add 2 --owner nist0 --url <issue-url>`) and status kept in sync (Todo → In Progress → Done)

- [ ] Issue updated (living document) whenever scope, approach, or blockers changed during implementation

- [ ] Working on a feature branch (not `main`)

- [ ] PR open, references closing issue(s) — body written via `--body-file`, spot-checked with `gh pr view`

- [ ] All GitHub checks passing (zero failures)

- [ ] All AC checkboxes ticked in every issue being closed — updated via `gh issue edit` if needed

- [ ] Scope and acceptance criteria defined

- [ ] Existing agent/skill/prompt reuse considered

- [ ] Routing updated in all needed YAMLs

- [ ] New/updated examples preserved or added (no info loss)

- [ ] Route smoke tests performed with representative phrases

- [ ] Security + reliability + testing expectations verified
