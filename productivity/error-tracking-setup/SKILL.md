---
name: error-tracking-setup
description: "Integrate Sentry for real time error alerts and debugging"
---

# Error Tracking Setup

## Sentry (Python)
```bash
pip install sentry-sdk
```

```python
import sentry_sdk
sentry_sdk.init(
    dsn="https://key@o.ingest.sentry.io/project",
    traces_sample_rate=1.0
)

# Automatic: uncaught exceptions captured
# Manual:
try:
    1 / 0
except Exception as e:
    sentry_sdk.capture_exception(e)
```

## Key Features
- Real-time error alerts
- Stack traces + context
- Performance tracing
- Release tracking
