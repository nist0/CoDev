---
name: bot-triage
description: "Systematically debug and triage bot issues across Teams, Telegram, WhatsApp and other platforms. Follows repro-first methodology: symptom collection, platform identification, SDK version, ranked hypotheses, and verified fix."
agent: Bot Engineer

## argument-hint: "platform=<teams|telegram|whatsapp|discord|other> language=<csharp|python> [sdk=<name-version>] [symptom=<text>] [repro=<text>] [env=<local|staging|prod>]"

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

# Bot Triage

## Goal

You are helping debug a bot issue. Follow the repro-first debugging workflow from `.github/instructions/reliability.instructions.md`.

## Triage workflow

Apply the procedure from `.github/skills/bot-architecture/SKILL.md` to understand where in the pipeline the failure occurs.
For Teams issues, apply `.github/skills/teams-bot/SKILL.md`.
For Telegram issues, apply `.github/skills/telegram-bot/SKILL.md`.
For WhatsApp issues, apply `.github/skills/whatsapp-bot/SKILL.md`.
Single source of truth:

- Bot failure classification, diagnostics, and platform-specific checks are defined in `bot-architecture` and platform skills.

- Do not restate or redefine those procedures here.

Execution contract:

1. Gather missing repro facts.

2. Classify the failure layer.

3. Produce ranked hypotheses.

4. Provide exact diagnostic commands.

5. Propose the minimal fix and one regression-prevention action.

Required output sections:

- Failure layer

- Ranked hypotheses

- Diagnostic commands

- Proposed fix

- Regression prevention

## Constraints

- Never ask the user to share raw bot tokens or secrets.

- Redact any token or PII in log snippets before analysis.

- All diagnostic commands must be safe (read-only where possible).
