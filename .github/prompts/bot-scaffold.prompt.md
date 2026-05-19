---
name: bot-scaffold
description: "Scaffold a production-ready bot project for Teams, Telegram, WhatsApp or other platforms in C# or Python. Gathers requirements and emits exact setup steps, project structure, and security baseline."
agent: Bot Engineer

## argument-hint: "platform=<teams|telegram|whatsapp|discord|slack|multi> language=<csharp|python> [ai=<none|llm-chat|function-calling|semantic-kernel|rag>] [state=<stateless|redis|cosmosdb>] [deploy=<app-service|container-apps|docker|other>]"

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

# Bot Scaffold

## Goal

You are asked to scaffold a new bot project.

## Requirements

Apply the procedure from `.github/skills/bot-architecture/SKILL.md`.

For Teams bots, apply the procedure from `.github/skills/teams-bot/SKILL.md`.

For Telegram bots, apply the procedure from `.github/skills/telegram-bot/SKILL.md`.

For WhatsApp bots, apply the procedure from `.github/skills/whatsapp-bot/SKILL.md`.

Enforce all rules from `.github/instructions/bot.instructions.md`.
Single source of truth:

- Scaffold procedure, platform-specific implementation details, and security baseline are defined in the linked bot skills and bot instructions.

- Do not restate or redefine those procedures here.

Execution contract:

1. Normalize platform, language, AI, state, and deployment intent.

2. Apply the relevant bot skills by platform.

3. Generate a runnable scaffold with secure defaults.

4. Provide setup commands, core files, and verification commands.

5. Include a security checklist mapped to bot instructions.

Required output sections:

- Architecture summary

- Required secrets and storage

- Project structure

- Setup steps

- Core runnable files

- Security checklist

- Verification steps

## Constraints

- Do NOT use Bot Framework SDK v4 (`Microsoft.Bot.Builder`). It is archived (EOL Dec 31 2025).

- Do NOT hardcode tokens or secrets.

- Do NOT use in-memory state for production scaffolds.

- Produce runnable code, not pseudocode.
