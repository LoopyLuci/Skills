---
name: log-rotation-config
description: Configure logrotate for application logs size retention
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [log, rotation, config]
---

# Log Rotation Config

## logrotate Config
```ini
/var/log/myapp/*.log {
    daily
    rotate 7
    size 100M
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
```

## Python Timed Rotating
```python
import logging.handlers
handler = logging.handlers.TimedRotatingFileHandler(
    "app.log", when="midnight", backupCount=7
)
handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
```

## Trigger

Activate this skill when the user mentions:
- log, rotation, config workflows or issues
- Building, fixing, or optimizing log rotation config


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
