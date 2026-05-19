---
name: "Bot Engineering"
description: "Always-on rules for bot code files across all platforms (Teams, Telegram, WhatsApp, Discord). Non-negotiable security baseline, SDK selection, and reliability standards."

## applyTo: "**/*bot*.{cs,py},**/*bot*handler*.{cs,py},**/*webhook*.{cs,py}"

# Bot Engineering Standards

## SDK selection (mandatory)

- Use **Microsoft 365 Agents SDK** (`Microsoft.Agents.*`) for new Teams / Azure bots in C#.

- Use **Teams AI Library** when adding AI (LLM, function calling) to Teams bots.

- Use **python-telegram-bot v22+** (async) for Telegram bots in Python.

- Use **WhatsApp Business Cloud API** (Meta, `graph.facebook.com`) for WhatsApp integration.

- **NEVER** reference `Microsoft.Bot.Builder.*` / Bot Framework SDK v4 as a primary implementation -- it was archived December 31 2025. If encountered in existing code, flag for migration.

## Secrets and configuration (non-negotiable)

- Load all bot tokens, secrets, and connection strings from environment variables or a secrets manager.

- Application MUST raise / throw immediately at startup if any required secret is missing.

- Never log a token, access key, or HMAC secret -- even partially.

- Never commit secrets or placeholder values that look like real tokens.

```python
# Correct
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]  # KeyError at startup = safe fail-fast

# Wrong
BOT_TOKEN = "123456:ABC-DEF..."  # NEVER
```

## Webhook security (non-negotiable)

- Validate the platform-specific signature or secret token on EVERY inbound POST before parsing.

- Use constant-time comparison to prevent timing attacks:

  - Python: `hmac.compare_digest(a, b)`

  - C#: `CryptographicOperations.FixedTimeEquals(span_a, span_b)`

- Reject the request with HTTP 403 if validation fails; do not process the payload.

## HTTP 200 on all inbound requests

- Always return HTTP 200 OK to the platform BEFORE processing the payload.

- Dispatch business logic asynchronously (background task, queue, fire-and-forget with error handling).

- Failure to return 200 causes the platform to retry, resulting in duplicate processing.

## State management

- Never use in-memory state in production (lost on restart, breaks horizontal scaling).

- Use Redis for volatile/short-lived state; Cosmos DB for durable conversation state.

- M365 Agents SDK: prefer `CosmosDbPartitionedStorage`.

- python-telegram-bot: use a custom `BasePersistence` backed by Redis or a DB; not `PicklePersistence` in production.

## Error handling

- Wrap all turn handlers and webhook processors in a top-level try/except or global error handler.

- Log errors with correlation ID and activity type; never log user message content at ERROR level.

- Catch and handle `httpx.HTTPStatusError` / `HttpRequestException` on all outbound API calls.

## Input validation

- Validate and sanitize all user-provided text before incorporating it into database queries, templates, or outbound requests.

- Trim whitespace; enforce maximum length; reject control characters in displayed text.

## Rate limiting and retries

- Back off on platform API rate-limit responses (HTTP 429). Use exponential backoff with jitter.

- Do not retry unconditionally on 5xx; distinguish transient from permanent errors.
