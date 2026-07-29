---
name: log-rotation-config
description: "Configure logrotate for application logs size retention"
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
