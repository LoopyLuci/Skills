---
name: scheduled-automation
description: Automate tasks with cron systemd timers Windows Scheduler
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [scheduled, automation]
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

## Trigger

Activate this skill when the user mentions:
- scheduled, automation workflows or issues
- Building, fixing, or optimizing scheduled automation


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
