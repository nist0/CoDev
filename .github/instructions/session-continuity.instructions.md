---
name: "Session Continuity & Theme-Based Knowledge Files"
description: "Maintain persistent, theme-scoped knowledge files with no redundancy so every new chat session can resume from an exact, up-to-date state."

## applyTo: "**"

# Session Continuity

## Principle

Knowledge and decisions produced during a session **must** be externalised into permanent,
theme-scoped files before the session ends.
A new session must be able to reach full context by reading only these files — no inference,
no re-discovery, no repeated analysis.

### Why theme-scoped files matter

- **Reusability**: future sessions on this repo inherit exact project state without re-running discovery.

- **No redundancy**: each fact lives in exactly one file; a reader finds it once and trusts it completely.

- **Maintenance**: updates are additive and cumulative; stale facts are pruned, not duplicated.

- **Session hygiene**: work-in-progress notes go to `/memories/session/` (ephemeral); permanent insights go to `/memories/repo/` (durable and cross-session).

## Where knowledge files live

All persistent knowledge files are managed via the memory tool under `/memories/repo/`.
Each file covers exactly one theme (see Naming below).

Important visibility note:

- `/memories/` is a tool-managed memory space, not a normal workspace folder. Its contents may not appear in the VS Code file explorer even when they exist and are being updated correctly.

- Because of that, every non-trivial session must also maintain a visible workspace handoff in `docs/session-handoffs/` so the user can inspect the saved state directly from the repository.

This continuity model has three mandatory layers that work together:

1. `/memories/repo/` for durable, theme-scoped knowledge that must survive every chat.

2. `/memories/session/` for the active working state of the current chat.

3. `docs/session-handoffs/` for resumable handoff snapshots when a chat is ending or nearing context limits.

| Scope | Path pattern | Managed by | Survives session? |
| --- | --- | --- | --- |
| Repository facts | `/memories/repo/<theme>.md` | memory tool (`create` / `str_replace`) | Yes — scoped to this repo |
| User preferences | `/memories/<theme>.md` | memory tool | Yes — cross-workspace |
| Session working notes | `/memories/session/<topic>.md` | memory tool | No — cleared after session |

## Naming themes

- One file per theme, lowercase kebab-case: `routing.md`, `testing.md`, `build-commands.md`, `decisions.md`.

- Never split one theme across multiple files.

- Never merge two distinct themes into one file.

## Mandatory maintenance rules (non-negotiable)

1. **Update on every change** — whenever a fact, decision, command, or convention changes,
   update the relevant theme file in the same operation. Never defer.

2. **No redundancy** — a fact appears in exactly one theme file.
   If information is relevant to two themes, store it in the more specific one and cross-reference.

3. **Append, do not overwrite** — use `str_replace` to add or update individual entries;
   never replace the whole file unless performing a deliberate restructure.

4. **Prune stale entries** — when a fact becomes outdated (e.g. a command changes),
   replace the old entry; do not leave both old and new side by side.

5. **Maintain a live session note** — every non-trivial task must keep an actively updated `/memories/session/<topic>.md` note with current objective, in-flight decisions, blockers, verification status, and exact next step.

6. **No chat-only reasoning** — if reasoning produced a durable outcome (decision, discarded option, verified command, convention, or next-step dependency), write it to `/memories/repo/` or `/memories/session/`; do not leave it only in chat history.

7. **Visible handoff is mandatory** — every non-trivial session must create or refresh a corresponding `docs/session-handoffs/<date>_<slug>.md` file, not only memory-tool notes, so there is always a user-visible continuity artefact in the workspace.

8. **Session close** — at the natural end of a session, before `task_complete`, or whenever context limits are near,
   review `/memories/session/`, flush any durable facts to the appropriate repo or user file, and refresh the resumable handoff record.

## Mandatory session workflow

### Start of session

1. Read `/memories/repo/` directory listing.

2. Load every repo memory file relevant to the task.

3. Read the latest relevant file in `docs/session-handoffs/` when continuing prior work.

4. If active work will span multiple steps, ensure there is a matching `/memories/session/<topic>.md` file and use it as the live working log.

5. Ensure there is a matching visible handoff file in `docs/session-handoffs/` for the session once the objective is stable.

### During the session

1. Update the session note after each significant decision, scope change, validation result, or blocker.

2. Promote durable conclusions from the session note into the correct `/memories/repo/<theme>.md` file as soon as they become stable.

3. Keep reasoning partitioned by theme; if one session touches multiple themes, update multiple repo memory files rather than mixing concerns.

4. Record the exact next action whenever work pauses, even temporarily.

5. Refresh the visible handoff file in `docs/session-handoffs/` whenever the session state changes materially.

### End of session or context-pressure handoff

1. Flush stable facts from `/memories/session/` into `/memories/repo/`.

2. Update or create the relevant `docs/session-handoffs/<date>_<slug>.md` file with current status, completed work, open questions, and exact next steps.

3. Ensure the handoff references the authoritative theme files rather than duplicating them.

4. Delete or trim stale session-only notes once their durable content has been promoted.

## Content guidelines

- Use concise bullet points or short code blocks — not prose paragraphs.

- Every entry must be actionable: a reader must be able to act on it without further context.

- Include exact commands, paths, and option flags — not vague descriptions.

- Tag decisions with a date in ISO format (`YYYY-MM-DD`) so staleness is self-evident.

- Separate temporary working state from durable knowledge: `/memories/session/` captures motion; `/memories/repo/` captures settled truth.

## Minimum required contents

Every active `/memories/session/<topic>.md` file should contain, at minimum:

- Current objective

- Active plan or current step

- Decisions made and why

- Blockers or risks

- Last validation result

- Exact next action

Every `docs/session-handoffs/<date>_<slug>.md` file should contain, at minimum:

- Scope being continued

- What is already done

- What remains

- Relevant repo memory files to read first

- Exact first next step for the new chat

## What to externalize to `/memories/repo/`

**Include** (durable patterns, conventions, decisions):

- Build/test commands that work and are verified

- Repo-specific conventions (naming, structure, CI patterns)

- Known issues, gotchas, and workarounds

- Decision outcomes: why a pattern was chosen, what alternatives were considered

- Architecture facts: entry points, key dependencies, module topology

- Verified tool versions and configuration patterns

- Links to key documentation or ADRs

- Commands that are run frequently in this repo

**Do NOT include** (transient, one-off, or discoverable):

- Timestamps of when things last happened

- Temporary debug notes from a single session

- One-off commands used for a single PR

- Analysis that should live in GitHub issues or ADRs instead

- Exact line numbers (they change; reference function/section names instead)

## Session initialisation (mandatory)

At the start of every new session on this repository:

1. Read `/memories/repo/` directory listing.

2. Load every file relevant to the task at hand.

3. If a session-handoff file exists in `docs/session-handoffs/`, read the latest relevant one.

4. If an active `/memories/session/` note exists for the task, resume from it before doing new analysis.

5. Do not re-derive facts that are already recorded — trust the files.

## Example: well-formed theme file entry

```markdown
## Build commands
- Run all tests: `python -m pytest tests/ -v` (verified 2026-05-08)
- Validate routing: `python scripts/validate-route-smoke.py`
- Validate registry: `python scripts/validate-customization-registry.py`
```

## Self-check before ending a session

- [ ] Every new fact or decision is written to the correct theme file (or explicitly deemed transient/one-off).

- [ ] No information exists only in the chat — durable insights are in `/memories/repo/` files.

- [ ] No duplicate entries introduced across theme files.

- [ ] Stale entries replaced (old fact removed, new fact added — never both side by side).

- [ ] Active session note in `/memories/session/` is up to date with latest decisions, validation, and next step.

- [ ] Session working files in `/memories/session/` reviewed — facts flushed to `/memories/repo/`, scratch work deleted.

- [ ] Relevant `docs/session-handoffs/` file exists and is updated for this non-trivial session.

- [ ] Each `/memories/repo/` file has a clear theme (no mixed concerns).

- [ ] Each entry is actionable without additional context (a new session reader can execute it immediately).
