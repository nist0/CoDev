---
name: session-handoff
description: "Generate or load a zero-argument session handoff package, either inline, as a workspace file, or by initializing a new chat from an attached handoff file."
agent: "Project Orchestrator"
---

Apply the procedure from `.github/skills/project-orchestration/SKILL.md`.

Goal:

- Create or load a handoff package so a new Copilot chat can continue the current work with minimal re-discovery and no avoidable context loss.
- Work with no required arguments. Infer the task, status, and next step from the current session state or from an attached handoff file.
- Support two primary actions:
  - `capture` (default) - generate a new handoff from the current session
  - `setup` or `init` - load an attached or referenced handoff file and initialize the new session from it
- In capture mode, support two output modes:
  - `inline` (default) - return the handoff directly in chat
  - `file` (when requested) - write the handoff to a workspace file instead of repeating copy-paste blocks in chat

Context source:

- the current chat and latest active user request
- visible workspace and repository context
- open files, terminal state, and recent verification results
- decisions, blockers, and assumptions already established in the session

Requirements:

- Synthesize from the current chat, visible workspace context, open files, terminal state, and recent verification evidence.
- Do not require the user to pass `task=`, `status=`, or `next-step=`.
- If the user includes extra text after `/session-handoff`, treat it as optional clarification, not a required input.
- If the user says `setup` or `init`, switch to bootstrap mode instead of capture mode.
- In bootstrap mode, look for a handoff source in this order:
  - an attached Markdown handoff file
  - a file path or file name explicitly mentioned by the user
  - the active editor file if it is a handoff document such as `docs/session-handoffs/*.md`
- In bootstrap mode, read the handoff file and treat it as the primary continuity source for objective, status, next step, files that matter, constraints, and prior verification evidence.
- In bootstrap mode, do not regenerate the handoff unless the user asks; summarize the loaded state and continue from it.
- If no handoff file is available in bootstrap mode, ask for one path or attachment in a single short question.
- Capture only high-signal context:
  - workspace path, repo name, branch, OS, and active file when relevant
  - current objective and success criteria
  - what is already done
  - what remains
  - key findings, decisions, blockers, and assumptions
  - files, symbols, commands, or errors that matter for continuation
  - verification already completed versus still pending
- If a detail is unknown or may have changed, mark it as `verify live` instead of inventing it.
- Keep the handoff compact, structured, and reusable. Prefer bullets over long prose.
- Preserve the chosen brainstorm direction when brainstorming already happened.
- Include a restart checklist so the next assistant can resume without redoing completed work.
- If the user asks for file mode using phrases like `use files`, `save it`, `write the handoff`, or `put it in a file`, create one local workspace handoff file instead of returning the full handoff inline.
- Use `docs/session-handoffs/PROJECT_DATETIME_THEMA.md` as the default and preferred file path.
- Only use another path when:
  - the user explicitly requests a different path
  - the default path cannot be created
- When using the default path pattern:
  - replace `PROJECT` with the repository name, for example `CoDev`
  - replace `DATETIME` with the current session timestamp in `YYYYMMDD_HHMMSS` format
  - replace `THEMA` with a short lowercase kebab-case topic slug derived from the current objective, for example `session-handoff-prompt-engineering`
- Prefer creating a new handoff file under `docs/session-handoffs/` rather than overwriting unrelated tracked docs.
- Before writing to `docs/session-handoffs/`, ensure `.gitignore` contains `docs/session-handoffs/` so these handoff files remain local-only and are not committed or pushed.
- If that ignore rule is missing, add it first; if `.gitignore` cannot be updated, fall back to `.generated/session-handoff.md` and say why.
- After writing a file-based handoff, return only the file path, status, and a short summary unless the user also asks to print the full contents.

Output:

1. Inline capture mode:
   - a short handoff summary in bullets
   - a fenced `text` block containing the final copy-paste prompt for the next session
2. File capture mode:
   - create or update the handoff file
   - return the path, status, and a 2-4 bullet summary
3. Setup or init mode:
   - load the attached or referenced handoff file
   - return a concise bootstrap summary with objective, status, next step, files that matter, and `Verify live` items
   - then continue from the loaded context or ask one blocking question if needed
4. If needed, add a short `Verify live` list for anything stale or uncertain.

Output format:

### Inline mode

## Session handoff

### Summary

- Objective: <one line>
- Status: <one line>
- Next step: <one line>

```text
You are continuing an interrupted VS Code Copilot session in the same workspace. Do not restart from zero.

Project
- Workspace path: <path>
- Repository: <owner/repo>
- OS: <os>
- Branch: <branch>
- Active file: <file>

Current objective
- <goal>

What has already been done
- <done item>

What still needs to be done
- <pending item>

Key findings and constraints
- <important fact>
- <important instruction or limitation>

How to resume
1. Restate the task and current state briefly.
2. Inspect the relevant files before acting.
3. Continue from unfinished work only.
4. Verify before claiming completion.
5. End with either progress made or the single blocker.
```

### File mode

Use this when the user wants a reusable handoff file instead of inline copy-paste blocks.

Return:

```text
Mode: file
Path: docs/session-handoffs/CoDev_20260410_223800_session-handoff-prompt-engineering.md
Status: <created|updated>
```

Then add a short summary:

- Objective: <one line>
- Status: <one line>
- Next step: <one line>

### Setup or init mode

Use this when the user says `/session-handoff setup` or `/session-handoff init` and provides a handoff file or path.

Return:

## Session bootstrap

### Loaded handoff

- Source: <attached file or path>
- Objective: <one line>
- Status: <one line>
- Next step: <one line>

### Carry-over context

- Files that matter: <paths or symbols>
- Constraints: <important limits or instructions>
- Verify live: <what should be rechecked in the current workspace>

Then either continue with the loaded objective or ask one short blocking question if the file is missing or ambiguous.

Rules:

- Default to inline mode unless the user explicitly asks for a file-based handoff.
- When file mode is requested, default to `docs/session-handoffs/PROJECT_DATETIME_THEMA.md`.
- In file mode, ensure `.gitignore` contains `docs/session-handoffs/` before writing the handoff file; if not possible, use `.generated/session-handoff.md` and explain the fallback.
- If the user says `setup` or `init`, prefer bootstrap mode over capture mode.
- In bootstrap mode, use the attached handoff file as the primary source of truth, then verify the live workspace state before making new completion claims.
- Do not ask follow-up questions unless the objective is truly unclear.
- Do not pad the handoff with generic repo boilerplate that does not affect the next step.
- Do not claim live repo status unless it was verified in the current session.
- Optimize for fast, correct continuation in a new chat.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Project Orchestrator** | always - user wants to continue work in a fresh session | *(this prompt)* | Copy-paste handoff prompt produced with objective, state, pending work, and restart checklist |
| 2 | **Relevant specialist agent** | handoff pasted into a new session | best matching prompt for the task | Work resumes without re-discovery or repeated setup |
