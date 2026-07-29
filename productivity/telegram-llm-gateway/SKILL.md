---
name: telegram-llm-gateway
description: "Use Telegram as frontend for LLM queries via Hermes agent"
---

# Telegram LLM Gateway

Use Telegram as a frontend to send queries to an LLM-agent. User messages Telegram → agent processes → reply delivered back.

## How It Works (Already Configured)

This conversation is already running through a Telegram gateway. The agent sees your messages as Telegram updates and delivers responses back. Key behaviors:

| Action | How |
|--------|-----|
| Send a message | Agent receives and responds |
| Send a file | Agent can read the file from the message |
| Ask for file delivery | Use `MEDIA:` path in response |
| Long responses | Telegram splits at 4096 chars |

## Built-In Features

The Hermes Telegram gateway provides:
- Message → Agent session routing
- File attachments → Tool access
- Markdown formatting in replies
- Cron delivery to Telegram
- Multi-chat support

## File Handling

Files sent via Telegram arrive as downloads. The agent can access them:

```python
# File is saved to a temp path on the host
# Reference it with its absolute path
read_file(path="/path/to/downloaded/file.pdf")
```

To send files back, use the MEDIA: protocol:
```
MEDIA:/absolute/path/to/file.ext
```

## Message Length Limits

| Item | Limit | Behavior |
|------|-------|----------|
| Single message | 4096 chars | Telegram truncates display |
| Code block | No strict limit | Scrollable within message |
| Caption | 1024 chars | File/image descriptions |
| Keyboard buttons | 64 chars | Per button text |

## Tips

- **Start a new topic** for parallel conversations
- **Forward messages** to share content between chats
- **Use `/new` to reset** the agent's context
- **Reply in thread** to keep context with scheduling
