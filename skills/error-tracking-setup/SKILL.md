---
name: error-tracking-setup
description: Integrate Sentry for real time error alerts and debugging
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [error, tracking, setup]
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

## Trigger

Activate this skill when the user mentions:
- error, tracking, setup workflows or issues
- Building, fixing, or optimizing error tracking setup


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
