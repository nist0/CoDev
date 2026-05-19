---
name: session-handoff
description: "Generate or load a zero-argument session handoff package, either inline, as a workspace file, or by initializing a new chat from an attached handoff file."
agent: "Project Orchestrator"

## argument-hint: "[action=<capture|setup|init>] [mode=<inline|file>] [source=<handoff-file-path>]"

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

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

Single source of truth:

- Session continuity and orchestration behavior are defined in `project-orchestration` and active repository instructions.

- Do not restate or redefine those procedures here.

Execution contract:

1. Detect mode: capture (default) or setup/init.

2. Infer task state from session context when arguments are omitted.

3. In setup/init mode, load provided handoff source and continue from it.

4. In capture mode, emit inline or file output based on user intent.

5. Keep handoff concise, high-signal, and continuation-ready.

6. For file mode, default to `docs/session-handoffs/<repo>_<timestamp>_<topic>.md`; if unavailable, use `.generated/session-handoff.md` and state the fallback.

Required outputs:

- Session handoff summary

- Inline or file handoff artifact

- Bootstrap summary in setup/init mode

- Verify-live list for uncertain context

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Project Orchestrator** | always - user wants to continue work in a fresh session | *(this prompt)* | Copy-paste handoff prompt produced with objective, state, pending work, and restart checklist |
| 2 | **Relevant specialist agent** | handoff pasted into a new session | best matching prompt for the task | Work resumes without re-discovery or repeated setup |
