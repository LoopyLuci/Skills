---
name: audit-logging
description: "Structured audit logging who what when and tamper evidence"
---

# Audit Logging

## Structure
```python
import structlog
logger = structlog.get_logger()

logger.info("user.action", 
    user_id=123,
    action="delete_record",
    resource="invoice-456",
    ip_address="192.168.1.1",
    timestamp="2026-07-29T12:00:00Z"
)
```

## What to Log
- User ID who performed action
- What action was taken
- Resource affected
- Timestamp (ISO 8601)
- Source IP
- Success/failure
- Before/after state for mutations
