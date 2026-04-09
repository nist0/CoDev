---
name: bot-triage
description: "Systematically debug and triage bot issues across Teams, Telegram, WhatsApp and other platforms. Follows repro-first methodology: symptom collection, platform identification, SDK version, ranked hypotheses, and verified fix."
agent: Bot Engineer
---

# Bot Triage

## Goal

You are helping debug a bot issue. Follow the repro-first debugging workflow from `.github/instructions/reliability.instructions.md`.

Gather the following from the user (if not already provided):

1. **Platform**: Teams / Telegram / WhatsApp / Discord / other.
2. **Language and SDK version**: e.g. python-telegram-bot 22.7, M365 Agents SDK 1.x.
3. **Symptom**: exact error message, unexpected behavior, or missing response.
4. **Repro steps**: exact sequence of actions that triggers the issue.
5. **Logs**: paste relevant log lines (redact any tokens or PII).
6. **Environment**: local dev / staging / production, webhook or polling.

## Triage workflow

Apply the procedure from `.github/skills/bot-architecture/SKILL.md` to understand where in the pipeline the failure occurs.

### Step 1 -- Classify the failure layer

Determine which layer is failing:

| Layer | Symptoms | First check |
| --- | --- | --- |
| Network / platform delivery | Webhook returns non-200, timeouts | Server logs, platform dashboard |
| Signature validation | HTTP 403 on inbound requests | Secret token / HMAC config |
| Handler routing | Handler not invoked, wrong handler | Handler registration order, filter patterns |
| Business logic | Unexpected reply or no reply | Add logging inside handler |
| State management | Stale/missing state, KeyError | Storage backend health, serialization |
| Outbound API | Send fails, rate limit errors | API response body, retry logic |
| Deployment / config | Works locally, fails in prod | Env variables, port binding, TLS |

### Step 2 -- Produce ranked hypotheses

List 2-4 ranked hypotheses with rationale. Most common first:

1. **Hypothesis 1**: [cause] -- [evidence from symptoms]
2. **Hypothesis 2**: [cause] -- [evidence from symptoms]

### Step 3 -- Diagnostic commands

Provide exact, runnable commands to confirm or refute the top hypothesis:

```bash
# Check webhook is registered correctly
curl "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo"

# Check environment variable is set
python -c "import os; print(os.environ.get('TELEGRAM_BOT_TOKEN', 'MISSING'))"
```

### Step 4 -- Fix

State the minimal fix. Show the before / after code diff if relevant.

### Step 5 -- Regression prevention

Specify what test or alert would catch this automatically next time.

## Common platforms -- quick checks

### Telegram

- Check `getWebhookInfo` for pending update count, last error, and last error date.
- Verify `X-Telegram-Bot-Api-Secret-Token` header is set in `setWebhook` call.
- Confirm bot token starts with numeric ID, colon, then random string.

### Teams / M365 Agents SDK

- Verify Azure Bot Service channel `botframework://` is enabled in Azure Portal.
- Check App ID and App Secret match between Entra registration and bot configuration.
- Inspect Azure Bot Service logs in Portal -> Diagnostics -> Logs.

### WhatsApp Cloud API

- Verify GET webhook returns `hub.challenge` correctly (check Meta Webhook troubleshooter).
- Confirm `X-Hub-Signature-256` header is present and app secret matches Business App settings.
- Check Meta Developer Console -> Webhooks -> Delivery logs for failure details.

## Output format

1. **Failure layer**: which layer is failing.
2. **Ranked hypotheses** (≥ 2, most likely first).
3. **Diagnostic commands**: exact copy/paste commands.
4. **Proposed fix**: minimal change with code snippet.
5. **Regression prevention**: test or alert specification.

## Constraints

- Never ask the user to share raw bot tokens or secrets.
- Redact any token or PII in log snippets before analysis.
- All diagnostic commands must be safe (read-only where possible).
