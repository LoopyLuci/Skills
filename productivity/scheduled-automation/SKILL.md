---
name: scheduled-automation
description: "Automate tasks with cron systemd timers Windows Scheduler"
---

# Scheduled Automation

## Linux Cron
```bash
# Edit crontab
crontab -e

# Format: minute hour day month weekday command
0 2 * * * /usr/local/bin/backup.sh
*/30 * * * * /usr/local/bin/healthcheck.sh
```

## Windows Task Scheduler (CLI)
```bash
schtasks /create /tn "MyTask" /tr "python script.py" /sc daily /st 02:00
```

## Hermes Cron
```bash
hermes cron create --schedule "0 9 * * *" --prompt "Daily summary" --deliver telegram
```
