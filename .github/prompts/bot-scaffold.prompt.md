---
name: bot-scaffold
description: "Scaffold a production-ready bot project for Teams, Telegram, WhatsApp or other platforms in C# or Python. Gathers requirements and emits exact setup steps, project structure, and security baseline."
agent: Bot Engineer
---

# Bot Scaffold

## Goal

You are asked to scaffold a new bot project.

Gather the following inputs from the user (if not already provided):

1. **Platform(s)**: Teams, Telegram, WhatsApp, Discord, Slack, or multi-channel.
2. **Language**: C# (.NET 8+) or Python (3.10+).
3. **AI features needed**: yes/no, and if yes which (LLM chat, function calling, Semantic Kernel, RAG).
4. **State requirements**: stateless, short-lived (Redis), or durable (CosmosDB).
5. **Deployment target**: Azure App Service, Azure Container Apps, Docker standalone, or other.

## Requirements

Apply the procedure from `.github/skills/bot-architecture/SKILL.md`.

For Teams bots, apply the procedure from `.github/skills/teams-bot/SKILL.md`.

For Telegram bots, apply the procedure from `.github/skills/telegram-bot/SKILL.md`.

For WhatsApp bots, apply the procedure from `.github/skills/whatsapp-bot/SKILL.md`.

Enforce all rules from `.github/instructions/bot.instructions.md`.

## Output format

Produce in this order:

### 1. Architecture summary

Short paragraph (3-5 sentences): platform(s), SDK choice and rationale, state backend, deployment model.

### 2. Required secrets

Table listing every secret the bot needs, its purpose, and where to store it:

| Secret key | Purpose | Storage |
| --- | --- | --- |
| `BOT_TOKEN` | Bot authentication | Key Vault / env |

### 3. Project structure

File tree of the scaffold (directories and key files only).

### 4. Setup steps

Numbered, copy/paste-ready commands:

1. `dotnet new web -n <BotName>` or `python -m venv .venv`
2. ...

### 5. Core files

Full content of the minimum files needed to run the bot (main entry point, handler, webhook controller).

### 6. Security checklist

From `.github/instructions/bot.instructions.md` -- confirm each item is implemented in the scaffold.

- [ ] Tokens from env/secrets; startup fails if missing.
- [ ] Webhook signature/secret validated.
- [ ] HTTP 200 returned before async processing.
- [ ] State backend appropriate for environment.
- [ ] Error handler in place.

### 7. Verification steps

Exact commands to verify the scaffold runs locally:

```bash
# Python
pip install -r requirements.txt
TELEGRAM_BOT_TOKEN=test python -m pytest tests/ -v

# C#
dotnet build
dotnet test
```

## Constraints

- Do NOT use Bot Framework SDK v4 (`Microsoft.Bot.Builder`). It is archived (EOL Dec 31 2025).
- Do NOT hardcode tokens or secrets.
- Do NOT use in-memory state for production scaffolds.
- Produce runnable code, not pseudocode.
