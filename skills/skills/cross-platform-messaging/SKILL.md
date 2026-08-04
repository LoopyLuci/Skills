---
name: cross-platform-messaging
description: "Send messages across Telegram Discord WhatsApp and email"
---

# Cross-Platform Messaging

Send the same message to multiple platforms (Telegram, Discord, WhatsApp, Email) with platform-specific formatting per channel.

## Platform Capabilities

| Feature | Telegram | Discord | WhatsApp | Email |
|---------|----------|---------|----------|-------|
| Markdown | ✅ Limited | ✅ Full | ❌ | ❌ |
| HTML | ❌ | ✅ | ❌ | ✅ |
| Files | 50MB | 25MB | 100MB | 25MB |
| Images | ✅ Photo | ✅ Embed | ✅ Compressed | ✅ Attach |
| Code blocks | ✅ | ✅ | ❌ | ❌ |
| Edit message | ✅ 48h | ✅ | ❌ | ❌ |
| Threads | ✅ Topics | ✅ Threads | ✅ Groups | ✅ Reply |

## Multi-Platform Delivery Function

```python
def deliver(platforms, message, files=None):
    for platform in platforms:
        if platform == "telegram":
            msg = tg_format(message)        # Markdown subset
            send_telegram(msg, files)
        elif platform == "discord":
            msg = discord_format(message)    # Discord markdown
            send_discord(msg, files)
        elif platform == "whatsapp":
            msg = whatsapp_format(message)   # Plain text mostly
            send_whatsapp(msg, files)
        elif platform == "email":
            msg = email_format(message)      # HTML + plain text
            send_email(msg, files)
```

## Format Converters

### Telegram Style
```python
def tg_format(text):
    # Bold: **text**
    # Code: `code`
    # No nested formatting
    return text
```

### Discord Style
```python
def discord_format(text):
    # Bold: **text**
    # Italic: *text*
    # Code: `code` or ```lang```
    # Links: [text](url) (auto-embed)
    return text
```

## Hermes Cron Multi-Delivery

```bash
hermes cron create \
  --schedule "0 8 * * *" \
  --prompt "Write a daily briefing covering today's agenda and priorities" \
  --deliver "origin,all"  # sends to Telegram + every connected channel
```

The `deliver` field supports:
- `"origin"` — back to the current chat
- `"all"` — every connected home channel
- `"telegram:chat_id,discord:channel_id"` — specific targets
- `"origin,all"` — origin + all channels
