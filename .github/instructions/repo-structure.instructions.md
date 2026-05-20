---
name: "Repository Structure & Generated File Placement"
description: "Deterministic directory conventions: every file type has a single canonical location; generated files are never placed arbitrarily."

applyTo: "**"
---

# Repository Structure

## Canonical directory map

Every file produced in or by this repository **must** land in the location below.
Before creating any file, look up its type in this table and use the mapped path -- no exceptions.

| File type | Canonical path | Notes |
| --- | --- | --- |
| Instruction files | `.github/instructions/<theme>.instructions.md` | One file per theme; see Naming below |
| Agent files | `.github/agents/<kebab-id>.agent.md` | Lowercase kebab-case |
| GitHub issue forms | `.github/ISSUE_TEMPLATE/<name>.yml` | Lowercase kebab-case issue form files |
| GitHub issue template config | `.github/ISSUE_TEMPLATE/config.yml` | Repository-wide issue chooser config |
| Prompt files | `.github/prompts/<kebab-id>.prompt.md` | Lowercase kebab-case |
| Skill files | `.github/skills/<theme>/SKILL.md` | One folder per skill; always named `SKILL.md` |
| Skill examples | `.github/skills/<theme>/examples/README.md` | Mandatory for every new skill |
| Routing YAML | `routing/<file>.yaml` | `capabilities.yaml`, `domains.yaml`, `aliases.yaml`, `matrix.yaml` only |
| Validator scripts | `scripts/validate-<topic>.py` | Python, named after what they validate |
| Developer scripts | `scripts/<verb>-<topic>.py` | Python, lowercase kebab-case |
| Tests | `tests/test_<module>.py` | Mirror `scripts/` module name |
| Automation hooks | `scripts/hooks/<hook-name>` | No extension for git hooks |
| Architecture decisions | `docs/decisions/<NNNN>-<slug>.md` | Zero-padded 4-digit counter |
| Repository memory files | `/memories/repo/<theme>.md` | Persistent repo-scoped knowledge; managed via memory tool |
| Session memory files | `/memories/session/<topic>.md` | Active session state and resumability notes; managed via memory tool |
| Session handoffs | `docs/session-handoffs/<date>_<slug>.md` | ISO date prefix `YYYYMMDD` |
| Developer documentation | `docs/<topic>.md` | Flat; subdirectories only for `decisions/` and `session-handoffs/` |
| Schemas | `schemas/<name>.schema.json` | JSON Schema files |
| Temporary / scratch files | `temp/` | **Never committed**; `.gitignore`-d |
| Reports (auto-generated) | `reports/<topic>-<timestamp>.<ext>` | Timestamp format `YYYYMMDDTHHMMSSZ` |

## Naming conventions

- All file and directory names: **lowercase kebab-case** (no spaces, no underscores except `SKILL.md`).

- Instruction themes must be single-concept nouns or noun-phrases: `repo-structure`, `session-continuity`, `security`, etc.

- Never use dates or author names in source-controlled file names (use git history for provenance).

## Rules enforced at all times

1. **No random placement** -- if a file type is not in the table above, stop and update this instruction before proceeding.

2. **No file creation outside the map** -- generated artefacts (reports, exports, rendered docs) go to `reports/` or `temp/`, never in `.github/` or the repo root.

3. **No duplicate paths** -- before creating a new file, search for an existing file of the same type and theme; extend it instead of creating a parallel file.

4. **New type = table update** -- every time a genuinely new file type is introduced, add a row to the table above as part of the same commit.

5. **`temp/` is ephemeral** -- files in `temp/` are never committed; use them only for transient work within a session.

6. **Generated vs. source** -- source-controlled files (`.github/`, `docs/`, `routing/`, `scripts/`, `schemas/`) are author-maintained and versioned. Generated outputs (validation reports, exports, renders, validation logs) go to `reports/` (timestamped, committed) or `temp/` (not committed). Never commit tool outputs or scratch work.

7. **Reasoning output has a home** -- durable facts, decisions, verified commands, and repo conventions discovered during work must be written to `/memories/repo/<theme>.md`; active working state belongs in `/memories/session/<topic>.md`; cross-session resumability belongs in `docs/session-handoffs/`.

8. **No chat-only state** -- if a future session would need a fact, decision, or next-step note, it must exist in the canonical memory or handoff location before the current session ends.

## Self-check before any file operation

- [ ] File type is in the canonical directory map.

- [ ] Path matches the mapped location exactly.

- [ ] No existing file of the same type+theme is being duplicated.

- [ ] If a new type is introduced, the table has been updated.

- [ ] Durable knowledge is going to `/memories/repo/`, active session state to `/memories/session/`, and resumability notes to `docs/session-handoffs/`.
