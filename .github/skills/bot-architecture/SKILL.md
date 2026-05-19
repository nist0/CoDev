---
name: bot-architecture
description: Cross-platform bot architecture patterns -- Activity/Turn model, middleware pipeline, state management, secrets hygiene, webhook vs polling, and AI integration. Applies to C# and Python across Teams, Telegram, WhatsApp, and other platforms.
argument-hint: "[platform] [concern]"

## user-invocable: true

# Bot Architecture (Cross-Platform)

## When to use

- Designing a new bot regardless of platform.

- Choosing between SDK options for a new project.

- Implementing state management, conversation flow, or middleware.

- Auditing an existing bot for security or reliability gaps.

## Core concepts

### Activity / Turn model

All modern bot SDKs (M365 Agents SDK, Teams AI Library, python-telegram-bot) share a common model:

```text
Platform  -->  Webhook / Polling  -->  Update / Activity
                                           |
                                    Middleware pipeline
                                           |
                                    Turn handler / Router
                                           |
                              Domain logic (handler function)
                                           |
                              Response sent back to platform
```

- An **Activity** (M365 Agents SDK) or **Update** (Telegram) represents one incoming event.

- A **Turn** is one round-trip: inbound activity + all processing + outbound response(s).

- A **Turn Context** provides access to the current activity, send methods, and state.

### Middleware pipeline

Register middleware in order; each middleware can short-circuit or pass through:

1. **Authentication / signature validation** -- verify the request came from the platform.

2. **Logging / tracing** -- log activity type, user ID (non-PII), and correlation ID.

3. **Error handling** -- catch unhandled exceptions; always return 200 OK to the platform.

4. **State hydration** -- load user/conversation state before the handler.

5. **Business middleware** -- rate limiting, feature flags, etc.

6. **State persistence** -- save state after the handler (or on explicit save calls).

### Handler registration

Register handlers by activity/update type:

```python
# python-telegram-bot
app.add_handler(CommandHandler("start", handle_start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CallbackQueryHandler(handle_callback))
```

```csharp
// M365 Agents SDK / Teams AI Library
protected override async Task OnMessageActivityAsync(ITurnContext<IMessageActivity> ctx, CancellationToken ct)
{
    await ctx.SendActivityAsync(MessageFactory.Text("Hello"), ct);
}
```

### State management

| Layer | Scope | Lifetime | Typical use |
| --- | --- | --- | --- |
| UserState | Per-user across all conversations | Until deleted | User preferences, profile |
| ConversationState | Per conversation | Until conversation ends | Dialog step, context |
| PrivateConversationState | Per user per conversation | Until conversation ends | Multi-turn flow state |
| Cache (Redis) | Custom key | TTL-based | Short-lived data, rate limits |

State storage backends:

- **In-memory**: only for local development; lost on restart.

- **Redis**: fast, TTL-aware; good for volatile state.

- **Azure Cosmos DB**: durable, globally distributed; built-in M365 Agents SDK adapter.

```python
# python-telegram-bot persistence (pickle-based, dev only)
persistence = PicklePersistence(filepath="bot_data")
app = ApplicationBuilder().token(TOKEN).persistence(persistence).build()

# Production: implement BasePersistence over Redis or CosmosDB
```

```csharp
// M365 Agents SDK - CosmosDB storage
var storage = new CosmosDbPartitionedStorage(new CosmosDbPartitionedStorageOptions
{
    CosmosDbEndpoint = Environment.GetEnvironmentVariable("COSMOS_ENDPOINT"),
    AuthKey = Environment.GetEnvironmentVariable("COSMOS_KEY"), // prefer managed identity
    DatabaseId = "bot-state",
    ContainerId = "conversations"
});
var userState = new UserState(storage);
var conversationState = new ConversationState(storage);
```

## Security baseline (mandatory)

### Token and secret management

```python
# Python -- always load from environment
import os
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]  # raise KeyError if missing -- fail fast
WH_SECRET = os.environ["TELEGRAM_WEBHOOK_SECRET"]
```

```csharp
// C# -- always load from configuration / Key Vault
var token = builder.Configuration["BotToken"]
    ?? throw new InvalidOperationException("BotToken config missing");
```

Never hardcode tokens. Never log them. Never commit them.

### Webhook signature validation

Validate every inbound webhook request before processing:

```python
# Telegram: check X-Telegram-Bot-Api-Secret-Token header
def validate_telegram_webhook(request, expected_secret: str) -> bool:
    received = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    return hmac.compare_digest(received, expected_secret)

# WhatsApp: verify HMAC-SHA256 signature
import hmac, hashlib
def validate_whatsapp_webhook(body: bytes, secret: str, signature_header: str) -> bool:
    expected = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_header)
```

### Always return 200 OK

Platforms retry on non-2xx. Return 200 immediately; process asynchronously:

```python
# FastAPI / Starlette pattern
@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    # Validate signature first
    validate_or_raise(request)
    payload = await request.json()
    background_tasks.add_task(process_update, payload)
    return {"ok": True}  # 200 OK immediately
```

## Conversation flow patterns

### Simple command / reply

```text
User: /help
Bot: "Here are the available commands..."
```

Register `CommandHandler` (Telegram) or `OnMessageActivityAsync` (Teams).

### Multi-turn dialog (stateful)

Use `ConversationHandler` (python-telegram-bot) or Waterfall/Component dialogs (Teams AI Library):

```python
# python-telegram-bot: ConversationHandler
from telegram.ext import ConversationHandler

STEP_NAME, STEP_AGE = range(2)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("register", start_register)],
    states={
        STEP_NAME: [MessageHandler(filters.TEXT, handle_name)],
        STEP_AGE: [MessageHandler(filters.TEXT, handle_age)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    persistent=True,
    name="registration"
)
```

### Inline keyboards and callbacks

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = [[InlineKeyboardButton("Yes", callback_data="yes"),
             InlineKeyboardButton("No",  callback_data="no")]]
reply_markup = InlineKeyboardMarkup(keyboard)
await update.message.reply_text("Confirm?", reply_markup=reply_markup)

# Handle callback
app.add_handler(CallbackQueryHandler(handle_confirm, pattern="^(yes|no)$"))
```

## Deployment patterns

### Webhook (recommended for production)

```text
Platform  --HTTPS POST-->  /webhook endpoint  -->  bot logic
```

- Requires public HTTPS URL.

- More efficient; no polling loop.

- Use ngrok or Azure Dev Tunnels for local development.

### Long polling (dev/test only)

```text
Bot  --getUpdates loop-->  Platform API  -->  process updates
```

- No public URL required.

- Only one instance can poll at a time.

- Do NOT use in production (latency, reliability issues).

## Self-check

- [ ] Tokens loaded from env/secrets; application fails fast if missing.

- [ ] Webhook signature validated before processing any payload.

- [ ] HTTP 200 returned immediately; processing is async if needed.

- [ ] State backend chosen and justified (in-memory only for dev).

- [ ] Error handler logs without PII; returns 200 to platform.

- [ ] Multi-turn flows use ConversationHandler / Dialog pattern.

- [ ] Rate limiting considered for outbound API calls.

## Outputs

- Architecture diagram (platform -> webhook -> middleware -> handler -> state).

- Verified project scaffold with security baseline.

- State management decision documented.

- Webhook deployment checklist.
