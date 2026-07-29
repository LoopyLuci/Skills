---
name: telegram-bot-creation
description: "Create deploy and manage Telegram bots with python library"
---

# Telegram Bot Creation

Full lifecycle for creating and running Telegram bots using `python-telegram-bot` v20+.

## 1. Create the Bot

1. Open Telegram, search for **@BotFather**
2. Send `/newbot`
3. Choose a display name (e.g. `My File Bot`)
4. Choose a username ending in `bot` (e.g. `MyFileTransferBot`)
5. Save the **token** — it looks like `7234567890:AAHdqTcvCH1vGWJxfSeOfS...`

## 2. Bot Token Safety

**NEVER** commit the token to git. Use environment variables:

```python
import os
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
```

Or a `.env` file (never committed):
```
TELEGRAM_BOT_TOKEN=7234567890:AAHdqTcv...
```

## 3. Minimal Bot (python-telegram-bot v20+)

```python
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = "YOUR_TOKEN_HERE"

async def start(update: Update, context):
    await update.message.reply_text("Hello! I am active.")

async def echo(update: Update, context):
    await update.message.reply_text(update.message.text)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
```

## 4. Key Bot Features

| Feature | How | Class |
|---------|-----|-------|
| Commands | `/command` handler | `CommandHandler("cmd", fn)` |
| Text messages | Any text | `MessageHandler(filters.TEXT, fn)` |
| Inline keyboards | Buttons under messages | `InlineKeyboardButton` |
| Reply keyboards | Persistent bottom menu | `ReplyKeyboardMarkup` |
| File download | Get files from messages | `message.document.get_file()` |
| File upload | Send any file | `message.reply_document(file)` |

## 5. File Operations

```python
# Receive a file
async def handle_file(update: Update, context):
    file = await update.message.document.get_file()
    await file.download_to_drive("received_file.pdf")
    await update.message.reply_text("File received!")

# Send a file
await update.message.reply_document(
    document=open("report.pdf", "rb"),
    filename="Monthly_Report.pdf",
    caption="Here is your report"
)
```

## 6. Deployment

```bash
# Install deps
pip install python-telegram-bot

# Run (polling mode — simple, no webhook needed)
python bot.py

# Or use systemd / Docker for production
```

## 7. Common Pitfalls

- **Token exposed** — revoke immediately: BotFather → /mybots → select bot → API Token → Revoke
- **Handler order matters** — add `CommandHandler` before `MessageHandler` or commands get caught as text
- **Conversations** — use `ConversationHandler` for multi-step flows
- **Rate limits** — Telegram enforces ~30 messages/second per chat
