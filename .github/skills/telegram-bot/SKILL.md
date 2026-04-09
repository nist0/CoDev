---
name: telegram-bot
description: Build production-grade Telegram bots in Python using python-telegram-bot v22+ (Bot API 9.5+). Covers async application setup, handler registration, ConversationHandler dialogs, webhook vs polling, persistence, and security.
argument-hint: "[feature: commands|dialogs|inline|webhook|persistence]"
user-invocable: true
---

# Telegram Bot Development (Elite)

## When to use

- Building a new Telegram bot in Python.
- Implementing multi-turn dialogs (registration, survey, wizard flows).
- Setting up a production webhook instead of polling.
- Adding inline keyboards, callbacks, or inline mode.
- Wiring up persistence for stateful conversations.

## Prerequisites

- Python 3.10+
- Bot token from @BotFather (`/newbot`)
- `pip install python-telegram-bot[all]`
  - Includes webhooks, job queue, persistence, and rate limiting extras.

## Step 1 -- Application scaffold

```python
# bot.py
import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN: str = os.environ["TELEGRAM_BOT_TOKEN"]  # fail fast if missing


async def start(update: Update, context) -> None:
    await update.message.reply_text("Hello! I am your bot. Send /help for commands.")


async def help_command(update: Update, context) -> None:
    await update.message.reply_text("/start - Welcome\n/help - This message")


async def echo(update: Update, context) -> None:
    await update.message.reply_text(update.message.text)


def build_app() -> Application:
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    return app


if __name__ == "__main__":
    build_app().run_polling()
```

## Step 2 -- Multi-turn dial (ConversationHandler)

```python
from telegram.ext import ConversationHandler

STEP_EMAIL, STEP_CONFIRM = range(2)


async def register_start(update: Update, context) -> int:
    await update.message.reply_text("What is your email address?")
    return STEP_EMAIL


async def register_email(update: Update, context) -> int:
    email = update.message.text.strip()
    # validate before storing
    if "@" not in email or "." not in email:
        await update.message.reply_text("Invalid email. Try again or /cancel.")
        return STEP_EMAIL
    context.user_data["email"] = email
    await update.message.reply_text(f"Confirm {email}? (yes / no)")
    return STEP_CONFIRM


async def register_confirm(update: Update, context) -> int:
    answer = update.message.text.strip().lower()
    if answer == "yes":
        # persist to your storage
        await update.message.reply_text("Registration complete.")
        return ConversationHandler.END
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END


async def cancel(update: Update, context) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("register", register_start)],
    states={
        STEP_EMAIL:   [MessageHandler(filters.TEXT & ~filters.COMMAND, register_email)],
        STEP_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_confirm)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    allow_reentry=True,
)
```

## Step 3 -- Inline keyboards and callbacks

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


async def choose(update: Update, context) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Option A", callback_data="a"),
            InlineKeyboardButton("Option B", callback_data="b"),
        ]
    ]
    await update.message.reply_text(
        "Pick one:", reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_callback(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()  # acknowledge -- removes loading indicator
    await query.edit_message_text(f"You chose: {query.data}")


# Register
app.add_handler(CommandHandler("choose", choose))
app.add_handler(CallbackQueryHandler(button_callback, pattern="^(a|b)$"))
```

## Step 4 -- Persistence (stateful conversations)

### Development (PicklePersistence)

```python
from telegram.ext import PicklePersistence

persistence = PicklePersistence(filepath="./bot_data.pkl")
app = ApplicationBuilder().token(BOT_TOKEN).persistence(persistence).build()
```

### Production (custom BasePersistence over Redis)

```python
import json
import redis.asyncio as aioredis
from telegram.ext import BasePersistence, PersistenceInput

class RedisPersistence(BasePersistence):
    def __init__(self, redis_url: str) -> None:
        super().__init__(
            store_data=PersistenceInput(
                bot_data=False, chat_data=True, user_data=True, callback_data=False
            )
        )
        self._redis = aioredis.from_url(redis_url)

    async def get_user_data(self):
        raw = await self._redis.get("user_data")
        return json.loads(raw) if raw else {}

    async def update_user_data(self, user_id: int, data: dict) -> None:
        all_data = await self.get_user_data()
        all_data[str(user_id)] = data
        await self._redis.set("user_data", json.dumps(all_data), ex=86400)

    # Implement remaining abstract methods similarly ...
```

## Step 5 -- Webhook (production)

```python
import hmac
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from telegram import Bot, Update

WEBHOOK_SECRET: str = os.environ["TELEGRAM_WEBHOOK_SECRET"]

fastapi_app = FastAPI()
bot = Bot(token=BOT_TOKEN)
telegram_app = build_app()


@fastapi_app.post("/telegram/webhook")
async def telegram_webhook(request: Request, background_tasks: BackgroundTasks):
    # Validate secret token header
    received_secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if not hmac.compare_digest(received_secret, WEBHOOK_SECRET):
        raise HTTPException(status_code=403, detail="Invalid secret token")

    payload = await request.json()
    update = Update.de_json(payload, telegram_app.bot)
    background_tasks.add_task(telegram_app.process_update, update)
    return {"ok": True}  # always 200 OK


@fastapi_app.on_event("startup")
async def startup():
    await telegram_app.initialize()
    await telegram_app.bot.set_webhook(
        url=f"https://{os.environ['SERVER_HOST']}/telegram/webhook",
        secret_token=WEBHOOK_SECRET,
        allowed_updates=["message", "callback_query", "inline_query"],
        drop_pending_updates=True,
    )


@fastapi_app.on_event("shutdown")
async def shutdown():
    await telegram_app.bot.delete_webhook()
    await telegram_app.shutdown()
```

### Register webhook manually via curl

```bash
curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://yourdomain.com/telegram/webhook",
    "secret_token": "'"${TELEGRAM_WEBHOOK_SECRET}"'",
    "allowed_updates": ["message", "callback_query"],
    "drop_pending_updates": true
  }'
```

## Step 6 -- Testing

```python
# pytest + python-telegram-bot test utilities
import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.mark.asyncio
async def test_start_sends_welcome():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()

    await start(update, context)

    update.message.reply_text.assert_called_once()
    args = update.message.reply_text.call_args[0]
    assert "Hello" in args[0]
```

## Self-check

- [ ] `TELEGRAM_BOT_TOKEN` loaded from env; application raises immediately if missing.
- [ ] `TELEGRAM_WEBHOOK_SECRET` set and validated on every inbound request.
- [ ] `hmac.compare_digest` used for constant-time secret comparison (no timing attack).
- [ ] Webhook always returns 200; processing dispatched to background task.
- [ ] `CallbackQueryHandler` calls `query.answer()` before any reply (removes spinner).
- [ ] `ConversationHandler.END` returned from all terminal states and fallbacks.
- [ ] Production persistence uses Redis or DB; `PicklePersistence` not used in prod.
- [ ] `drop_pending_updates=True` set on webhook registration (prevents replay on restart).
- [ ] `allowed_updates` scoped to only the update types the bot handles.

## Outputs

- Working Python bot with command handlers and optional multi-turn dialogs.
- Webhook endpoint with signature validation.
- Persistence layer wired to Redis or DB for production use.
- pytest test file for key handlers.
