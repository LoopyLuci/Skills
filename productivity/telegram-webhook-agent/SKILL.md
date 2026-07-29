---
name: telegram-webhook-agent
description: "Let Telegram messages trigger agent responses via webhooks"
---

# Telegram Webhook Agent

Set up a webhook so incoming Telegram messages trigger the agent. This enables bidirectional communication — the user messages the agent on Telegram and it responds.

## Architecture

```
User → Telegram → Webhook URL → Hermes Gateway → Agent Processes → Reply
```

## Setup

### 1. Create a Telegram Bot

```bash
# Talk to @BotFather on Telegram
/newbot
# Name: MyAgent
# Username: MyAgent_bot
# Save the token: 123456:ABCdef...
```

### 2. Configure Hermes Gateway

Set the bot token and webhook route in `config.yaml`:

```yaml
gateway:
  telegram:
    bot_token: "123456:ABCdef..."   # From BotFather
    webhook_url: "https://your-domain.com/webhook/telegram"
    allowed_user_ids:
      - 1350214376  # Your Telegram user ID (get from @userinfobot)
```

Or via CLI:
```bash
hermes config set gateway.telegram.bot_token "123456:ABCdef..."
hermes config set gateway.telegram.webhook_url "https://your-domain.com/webhook/telegram"
hermes config set gateway.telegram.allowed_user_ids "[1350214376]"
```

### 3. Set Up the Webhook

```bash
# Register webhook with Telegram
curl -F "url=https://your-domain.com/webhook/telegram" \
     "https://api.telegram.org/bot<TOKEN>/setWebhook"

# Verify
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
```

### 4. Expose Local Server (Dev)

Use ngrok for development:

```bash
ngrok http 8080
# Copy the https://xxxx.ngrok.io URL
# Set webhook_url to https://xxxx.ngrok.io/webhook/telegram
```

## How Replies Work

1. User sends a message to the bot on Telegram
2. Telegram POSTs the update to the webhook URL
3. Hermes gateway receives it, creates a session
4. Agent processes and responds
5. Response is delivered back to the Telegram chat

## Filtering

Restrict which users can interact:

```yaml
gateway.telegram.allowed_user_ids:
  - 1350214376   # Only this user
  # - 987654321  # Add more user IDs
```

Block unknown users silently (no error message sent).

## Security

- Keep bot tokens secret — anyone with the token controls your bot
- Use `allowed_user_ids` to prevent abuse
- Set `webhook_url` to HTTPS only (Telegram rejects HTTP)
- Rotate tokens if compromised via `BotFather → /revoke`

## Troubleshooting

**Webhook not responding** — check ngrok/tunnel is running and the URL matches.

**Messages not arriving** — verify `getWebhookInfo` returns `has_custom_certificate: false` and `pending_update_count: 0`.

**Wrong user responding** — the gateway checks `allowed_user_ids` before processing.
