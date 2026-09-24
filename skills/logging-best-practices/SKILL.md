---
name: logging-best-practices
description: Structured logging with structlog correlation IDs and rotation
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [logging, best, practices]
---

# Logging Best Practices

## Structured Logging
```python
import structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer()
    ]
)
log = structlog.get_logger()
log.info("request", method="GET", path="/users", status=200)
```

## Log Rotation
```ini
# /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
```

## Trigger

Activate this skill when the user mentions:
- logging, best, practices workflows or issues
- Building, fixing, or optimizing logging best practices


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
