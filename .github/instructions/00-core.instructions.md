---
name: "Copilot Dev Framework - Core"
description: "Core working agreement: deterministic steps, copy/paste-ready outputs, non-contradictory layering."

applyTo: "**"
---

# Core Rules (Framework)

## Output quality

- Prefer copy/paste-ready outputs: commands, file content, checklists.

- If you suggest changes, include verification steps (local + CI).

- When generating multiline text for GitHub comments/issues/PR bodies, preserve real new lines (do not emit literal `\n` sequences).

- For any newly published external content (GitHub issues, PRs, reviews, comments), use English.

- Structure outputs as: **Plan -> Changed files -> Rationale -> Self-check** for any non-trivial task.

- **NEVER use non-ASCII or special Unicode characters** (arrows, box-drawing characters, emoji, etc.) in any output — including terminal commands, verification steps, checklists, code comments, and prose. Use plain ASCII equivalents only (e.g. `->` not `→`, `-` not `•`, `(check)` not `✓`).

## GitHub issue / PR body formatting (mandatory)

Every GitHub issue, PR description, and comment body **must** comply with these rules — no exceptions:

### Content rules

- Use standard GitHub Flavored Markdown only: `##` headings, fenced code blocks (triple backticks with language tag), `|`-delimited tables with a separator row, `-` / `1.` lists.

- Every Markdown table **must** include a separator row: `| --- | --- |` (one cell per column). Missing separators cause columns to render as plain text.

- Code blocks **must** open and close with triple backticks on their own lines. Never embed inline code spans for multi-line shell commands.

- Do **not** wrap section titles or values in backslashes (e.g. `\frontend\` is wrong — use plain `frontend`).

- Do **not** use literal `\n` sequences; use real line breaks.

### Authoring rules (CLI)

> **⛔ BLOCKING — read before every `gh` command that publishes content:**
> Never pass a multi-line body inline with `--body "..."` in PowerShell.
> PowerShell treats backtick (`` ` ``) as its escape character inside double-quoted
> strings, so every inline code span (e.g. `` `value` ``) is silently corrupted
> (the backtick is consumed and adjacent characters may be eaten too).
> **Always write the body to a file and pass it with `--body-file <path>`.**

- **Always use `--body-file <path>`** when creating or editing issues/PRs via `gh` CLI with multi-line bodies. Never use `--body "..."` for multi-line content — PowerShell and shell escaping will corrupt backslashes and eat leading characters.

- Write the body to a temporary `.md` file using a **single-quoted** PowerShell heredoc (`@'...'@`) so no escaping occurs, then pass it via `--body-file`.

- After publication, **always** spot-check with `gh pr view <N>` or `gh issue view <N>` before considering the task done. If any cell or word starts with `\`, or any backtick code span is missing, the body was corrupted — close and re-create.

- Delete the temp file immediately after the `gh` command.

### Example: correct CLI pattern

```powershell
# Single-quoted heredoc — backticks and backslashes are never interpreted
$body = @'
## Summary
Adds 7 new routing rules.

## Acceptance criteria
- Coverage threshold updated from 59 to 52.
- All validators pass (`validate-routing-coverage.py`, pytest 9/9).
- All GitHub CI checks green.

Closes #N.
'@
$body | Set-Content -Path "$env:TEMP\body.md" -Encoding UTF8
gh issue create --title "feat: add routing rules" --body-file "$env:TEMP\body.md"
Remove-Item "$env:TEMP\body.md"

# Mandatory spot-check — look for stray backslashes or missing backtick spans
gh issue view <N>
```

### Self-check before publishing

- [ ] No raw backslashes before words (e.g. `\frontend` → `frontend`).

- [ ] All tables have a separator row.

- [ ] Code blocks open/close with triple backticks on their own lines.

- [ ] Body written to a file using a **single-quoted** heredoc (`@'...'@`) and passed via `--body-file`.

- [ ] Spot-checked with `gh pr view <N>` or `gh issue view <N>` after creation — no stray `\` chars, no missing backtick spans.

## Todo list synchronization (mandatory)

The todo list **must** be kept synchronized at all times — no exceptions:

- **Before starting any task**: mark it `in-progress`. Never start work on an unmarked item.

- **Immediately after completing a task**: mark it `completed`. Never batch completions.

- **One in-progress at a time**: only one todo may carry the `in-progress` state simultaneously.

- **Session hygiene**: at the start of a new session, initialize the list from the current state before doing anything else.

- **Never defer**: updating the todo list is not optional and not "cleanup" — it is part of the task itself.

> **Enforcement**: failing to synchronize the todo list is treated as a process violation, equivalent to skipping a CI gate.

## Engineering defaults

- Prefer deterministic, verifiable steps.

- Keep instructions additive: do not contradict other instruction layers.

- For complex multi-file tasks: explore first, produce a short plan (≤10 bullets), then implement.

- Choose the right interaction pattern for the task:

  - quick edits/completions → focused edits

  - questions/research → chat/ask

  - multi-file implementation → agent workflow with planner/implementer/reviewer split

- State acceptance criteria before coding: tests, expected outputs, or concrete checks.

- After implementation, always include verification guidance (local + CI) and key risks.

- Never leave TODO/FIXME in generated code without a linked issue or inline rationale.

## Mandatory development workflow (non-negotiable)

Every piece of work — no matter how small — **must** follow this sequence:

0. **Brainstorm first** (mandatory for non-trivial tasks): before creating any issue, opening any branch, or writing any code, produce a structured brainstorm with ≥ 3 scored options (safe / adjacent / bold).

   - **Non-trivial** = touches more than one file, introduces a new pattern, has user-facing impact, performance/security implications, or takes longer than 30 minutes.

   - **Exempt**: single-file typo fix, doc-only reword, plain config toggle with zero logic change.

   - Output: a scored option table with rationale for the chosen finalist. This becomes the `## Technical approach` section of the issue.

   - Use the Innovator agent or `/brainstorm` to run the brainstorm. Do not skip this gate silently.

1. **Create a detailed issue first**: open a GitHub issue for every task and subtask **before writing any code**.
   The issue body **must** include all of the following sections:

   ```markdown

## Summary

   <Why this work is needed; what problem it solves.>

## Technical approach

   <How the problem will be solved. Include the brainstorm finalist rationale. Update as the approach is refined.>

## Files to modify

   - `path/to/file.ext` — what change and why

## Sub-tasks

   <!-- Use checkboxes for inline sub-tasks; open child issues (linked below) for multi-PR sub-tasks -->

   - [ ] Sub-task 1 (`path/to/file.ext`)

   - [ ] Sub-task 2
   <!-- Child issues: Part of #N -->

## Acceptance criteria

   - [ ] <verifiable criterion 1>

   - [ ] <verifiable criterion 2>

## Verification steps

   1. <exact local command or CI check expected to pass>

## Progress log

   <!-- Append dated entries as work evolves: scope changes, blockers, decisions -->
   ```

   - Link sub-tasks to a parent with `Part of #N`; link sibling tasks with `Blocks #N` / `Blocked by #N`.

   - **The issue is a living document**: amend `Technical approach`, `Files to modify`, and `Progress log`
     as the work evolves. Every significant scope change, blocker, or decision must be logged here.
     Use `gh issue edit <N> --body-file <path>` to update.

   - **Project board** (mandatory): immediately after creating the issue, add it to the CoDev project Kanban board (project #2) and keep its status column in sync throughout the lifecycle:

     - *Created* → **Todo**: `gh project item-add 2 --owner nist0 --url <issue-url>`

     - *Branch created / work started* → **In Progress**: `gh project item-edit --id <item-id> --field-id PVTSSF_lAHOAOYJIs4BQzk2zg-0dUk --project-id PVT_kwHOAOYJIs4BQzk2 --single-select-option-id 47fc9ee4`

     - *PR merged / issue closed* → **Done**: `gh project item-edit --id <item-id> --field-id PVTSSF_lAHOAOYJIs4BQzk2zg-0dUk --project-id PVT_kwHOAOYJIs4BQzk2 --single-select-option-id 98236657`

2. **Plan in the issue**: document the approach, scope, and risks in the issue body before branching.
   If the approach changes mid-implementation, update the issue immediately — do not wait until merge.

3. **Work on a branch**: create a feature branch from the default branch (`main`).
   Branch naming convention: `feat/<slug>`, `fix/<slug>`, `chore/<slug>`.

4. **Open a Pull Request**: push the branch and open a PR that references the issues it closes (`Closes #N`).
   Never push commits directly to `main`.

5. **Review before merge**: every PR requires at least one review (agent or human).
   Document the review verdict explicitly (`approved` or `rework required`).

6. **All checks must pass**: **NEVER merge a branch to main when GitHub checks are not all green.**
   All GitHub status checks must pass before merging. This includes lint, tests, validators, and any CI gate.
   If checks are failing, the issues **must** be fixed on the branch **BEFORE** merging.
   Never merge with failing checks; never skip or suppress checks.

7. **Verify acceptance criteria before closing**: before an issue is closed (manually or via PR merge),
   **always check the Acceptance criteria and tick them** in the issue body.
   Update unchecked boxes with `gh issue edit <N> --body-file <path>`.
   Never leave unchecked boxes on a closed issue.

> **Enforcement**: violating any step above (e.g. pushing to main, merging with failing checks) is
> a blocking finding in any code review and must be corrected before the work is considered done.

## Routing

- When uncertain, recommend using `/route` to select the right agent/prompt/skill.

- Use `/route <free-form request>` for classification before any large task.

## Context & safety

- Keep context relevant and minimal; avoid polluting sessions with unrelated tasks.

- Prefer explicit file/symbol references when possible.

- Avoid secrets or credentials in prompts, examples, and generated outputs.

- Review generated changes for security, error handling, and edge cases before finalizing.

## Mandatory customization compliance

- For changes to instructions, prompts, agents, skills, or tools/MCP config, follow `docs/copilot-vscode-best-practices.md`.

- Do not finalize those changes until the enforced checklist in that document is satisfied.

- Keep tools/MCP scope least-privilege and only enable what is required for the task.

Example: well-formed task response
---

```text
**Plan** (3 steps)
1. Add `UserService.CreateAsync()` with input validation.
2. Add unit test covering happy path + null input.
3. Update OpenAPI docs.

**Changed files**
- src/Services/UserService.cs (new method)
- tests/Services/UserServiceTests.cs (2 new tests)
- docs/openapi.yaml (new endpoint schema)

**Rationale** — Follows IOptions<T> pattern; errors use ProblemDetails contract.

**Self-check** — Run `dotnet test` and `dotnet build -warnaserror`; zero new warnings.
```

---

## 🏆 Elite Section — Top 5% Practitioner Habits

> These habits separate senior engineers who ship reliably from those who ship often.

- **Pre-mortem before PR**: Before opening a PR, explicitly list the 3 most likely failure modes and confirm each is handled or documented.

- **Acceptance criteria as code**: Write failing tests (or assertions) that encode the acceptance criteria before implementation begins.

- **Zero-assumption handoffs**: When handing a task to another agent or human, include exact repro commands, not just descriptions.

- **Signal over noise in verification**: Verification steps must be deterministic (exact commands, expected exit codes, expected log lines) — not "should look fine".

- **Layered review**: After coding, apply at minimum: (1) correctness, (2) security, (3) observability, (4) backward compatibility — in that order.

- **Instruction hygiene**: After each session that surfaces a recurring gap, update the relevant instruction file immediately. Never defer codification.
