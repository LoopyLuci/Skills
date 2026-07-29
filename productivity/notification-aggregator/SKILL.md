---
name: notification-aggregator
description: "Aggregate alerts from GitHub monitoring RSS into Telegram"
---

# Notification Aggregator

Collect events from multiple sources and deliver a single daily digest or real-time alerts to Telegram.

## Architecture

```
GitHub ─┐
Monitoring ─┤
RSS Feed ──┤──→ Hermes Cron Job → Telegram
Calendar ─┘
```

## Cron-Based Aggregation

Use `cronjob` to run periodic checks and deliver results:

```bash
# Daily digest at 8 AM
hermes cron create \
  --schedule "0 8 * * *" \
  --prompt "Check all monitored sources and summarize key events" \
  --deliver telegram
```

## Monitored Sources

### GitHub Notifications

```python
# Check unread GitHub notifications
import os, json
from urllib.request import Request, urlopen

token = os.environ["GITHUB_TOKEN"]
req = Request("https://api.github.com/notifications")
req.add_header("Authorization", f"Bearer {token}")
data = json.loads(urlopen(req).read())
notifications = [
    f"[{n['subject']['type']}] {n['subject']['title']}"
    for n in data[:10]
]
```

### RSS/Atom Feeds

Use the `blogwatcher` skill to monitor RSS feeds.

### System Monitoring

```python
import psutil
alerts = []
if psutil.cpu_percent(interval=1) > 90:
    alerts.append(f"⚠️ CPU at {cpu}%")
if psutil.virtual_memory().percent > 90:
    alerts.append(f"⚠️ Memory at {mem}%")
```

## Delivery Patterns

| Pattern | When | Example |
|---------|------|---------|
| Real-time alert | Event occurs | "🚨 Server CPU at 95%" |
| Hourly summary | Every hour | "3 GitHub PRs, 2 new emails" |
| Daily digest | Once daily | Full report of all sources |
| Threshold breach | When crossed | "Disk space below 10%" |

## Script Pattern (No-Agent Mode)

For watchdogs, use `no_agent=True` for zero-token cost:

```bash
hermes cron create \
  --schedule "*/30 * * * *" \
  --script "scripts/disk-watchdog.sh" \
  --no-agent \
  --deliver telegram
```

The script's stdout becomes the message. Empty stdout = silent (no alert).
