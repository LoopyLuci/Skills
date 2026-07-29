---
name: telegram-monitor-alert
description: "Send system monitoring alerts to Telegram via cron"
---

# Telegram Monitor Alert

Send system health alerts (CPU, disk, memory, uptime) to Telegram via cron jobs with `no_agent=True`.

## Watchdog Script Pattern

Create a script that checks system health and outputs a message only when something is wrong:

```bash
# scripts/disk-watchdog.sh
#!/bin/bash
THRESHOLD=90
USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$USAGE" -gt "$THRESHOLD" ]; then
    echo "⚠️  Disk Alert: $USAGE% on /"
fi
```

## Cron Job (Zero Token Cost)

```bash
hermes cron create \
  --schedule "*/10 * * * *" \
  --script "scripts/disk-watchdog.sh" \
  --no-agent \
  --deliver telegram
```

With `no_agent=True`:
- Script stdout = message body
- Empty stdout = silent (nothing to report)
- Non-zero exit = error alert sent

## Python Watchdog

```python
# scripts/system-watchdog.py
import psutil, json, os

alerts = []

# CPU
cpu = psutil.cpu_percent(interval=1)
if cpu > 90:
    alerts.append(f"🔥 CPU: {cpu}%")

# Memory
mem = psutil.virtual_memory()
if mem.percent > 90:
    alerts.append(f"🧠 Memory: {mem.percent}%")

# Disk
for part in psutil.disk_partitions():
    usage = psutil.disk_usage(part.mountpoint)
    if usage.percent > 90:
        alerts.append(f"💾 {part.mountpoint}: {usage.percent}%")

# Print alerts (becomes the message)
for a in alerts:
    print(a)
```

## What to Monitor

| Check | Command/Script | Threshold |
|-------|---------------|-----------|
| Disk usage | `df -h` | > 90% |
| CPU load | `psutil.cpu_percent()` | > 90% |
| Memory | `psutil.virtual_memory()` | > 90% |
| Uptime | `uptime` | After restart |
| Process down | `pgrep <name>` | Not running |
| Temperature | `sensors` | > 80°C |
| Network | `ping -c 1 <host>` | Packet loss |

## Alert Levels

| Level | Emoji | Action |
|-------|-------|--------|
| Info | ℹ️ | Informational |
| Warning | ⚠️ | Needs attention |
| Critical | 🔥 | Immediate action |
| Recovery | ✅ | Back to normal |
