# bot-architecture examples

## Example 1 -- Turn model diagram

```text
User sends: "hello"
  --> Platform delivers HTTPS POST to /webhook
  --> Middleware: validate signature (403 if invalid)
  --> Middleware: log correlation-id + activity type
  --> Middleware: hydrate conversation state
  --> TurnHandler: OnMessageActivityAsync / echo handler
  --> Send "Echo: hello" back to user
  --> Middleware: persist conversation state
  --> Return HTTP 200 OK
```

## Example 2 -- State backend decision

| Environment | Backend | Reason |
| --- | --- | --- |
| Local dev | In-memory | No infra required |
| Staging | Redis (Azure Cache) | Fast, TTL, stateless servers |
| Production (Teams) | CosmosDbPartitionedStorage | Durable, globally distributed |
| Production (Telegram) | Custom RedisPersistence | BasePersistence over aioredis |

## Example 3 -- Webhook vs polling

Choose webhook for production:

```bash
# Register Telegram webhook
curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://mybot.azurewebsites.net/telegram/webhook",
    "secret_token": "'"${TELEGRAM_WEBHOOK_SECRET}"'",
    "allowed_updates": ["message", "callback_query"],
    "drop_pending_updates": true
  }'
```

Use polling only for local development:

```python
# Dev only -- single instance, no public URL needed
build_app().run_polling()
```
