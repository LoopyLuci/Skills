---
name: telegram-github-bridge
description: "Bridge GitHub webhooks to Telegram notifications"
---

# Telegram GitHub Bridge

Receive GitHub notifications (PRs, issues, CI, releases) directly in Telegram via webhooks.

## Option 1: GitHub Webhook → Telegram Bot

### 1. Create a webhook receiver

```python
# webhook_server.py
from flask import Flask, request
import requests
import os

app = Flask(__name__)
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

@app.route("/github-webhook", methods=["POST"])
def github_webhook():
    event = request.headers.get("X-GitHub-Event")
    payload = request.json
    if event == "pull_request":
        action = payload["action"]
        title = payload["pull_request"]["title"]
        url = payload["pull_request"]["html_url"]
        send_telegram(f"🔀 PR {action}: {title}\n{url}")
    elif event == "issues":
        action = payload["action"]
        title = payload["issue"]["title"]
        send_telegram(f"🐛 Issue {action}: {title}")
    elif event == "push":
        commits = len(payload["commits"])
        repo = payload["repository"]["full_name"]
        send_telegram(f"📦 {commits} commit(s) pushed to {repo}")
    return "OK"

app.run(port=5000)
```

### 2. Expose with ngrok

```bash
ngrok http 5000
# → https://abc123.ngrok.io
```

### 3. Configure GitHub

Go to your repo → Settings → Webhooks → Add webhook:
- Payload URL: `https://abc123.ngrok.io/github-webhook`
- Content type: `application/json`
- Select events (PR, Issues, Push, etc.)

## Option 2: GitHub CLI + Cron

```bash
hermes cron create \
  --schedule "0 9 * * *" \
  --prompt "Check my GitHub notifications and summarize anything I need to know" \
  --deliver telegram
```

## Notification Format

| Event | Format |
|-------|--------|
| PR opened | 🔀 **New PR:** [title](url) by @user |
| PR merged | ✅ **Merged:** [title](url) |
| Issue opened | 🐛 **New Issue:** [title](url) |
| CI passing | ✅ CI passed on [branch] |
| CI failing | ❌ CI failed on [branch] |
| Release | 🎉 **Release:** [tag](url) |
