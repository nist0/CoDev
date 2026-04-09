# telegram-bot examples

## Example 1 -- Minimal echo bot

```python
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

async def start(update: Update, context):
    await update.message.reply_text("Hello! Send me a message.")

async def echo(update: Update, context):
    await update.message.reply_text(update.message.text)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.run_polling()  # dev only
```

## Example 2 -- Inline keyboard with callback

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

async def ask(update: Update, context):
    keyboard = [[InlineKeyboardButton("Yes", callback_data="yes"),
                 InlineKeyboardButton("No",  callback_data="no")]]
    await update.message.reply_text("Continue?", reply_markup=InlineKeyboardMarkup(keyboard))

async def answer(update: Update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"You chose: {query.data}")

app.add_handler(CommandHandler("ask", ask))
app.add_handler(CallbackQueryHandler(answer, pattern="^(yes|no)$"))
```

## Example 3 -- Check webhook status

```bash
curl "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo"
# Returns: url, pending_update_count, last_error_message, last_error_date
```

## Example 4 -- Delete webhook (switch back to polling)

```bash
curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/deleteWebhook" \
  -d "drop_pending_updates=true"
```
