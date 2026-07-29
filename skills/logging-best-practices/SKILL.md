---
name: logging-best-practices
description: "Structured logging with structlog correlation IDs and rotation"
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
