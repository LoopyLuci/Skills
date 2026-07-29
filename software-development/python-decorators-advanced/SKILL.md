---
name: python-decorators-advanced
description: "Use when implementing advanced Python decorators."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [python, decorators, functools, wraps, class-decorators]
    related_skills: [python-async-patterns, clean-code-principles, cross-thread-async]
---

# Advanced Python Decorators

Implementing advanced Python decorators — from parameterized decorators through class decorators, decorators with arguments, and stacked patterns.

## When to Use

- Building reusable cross-cutting concerns
- Implementing caching, retry, timing decorators
- Building DSL-like APIs with decorators

## Decorator Patterns

```python
from functools import wraps
import time

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_attempts):
                try: return func(*args, **kwargs)
                except Exception as e:
                    if i == max_attempts - 1: raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.time()-start:.3f}s")
        return result
    return wrapper
```

## Verification Checklist

- [ ] @wraps used to preserve metadata
- [ ] Decorator factory with arguments pattern
- [ ] Stacking decorators in correct order
- [ ] Class-based decorators with __call__
- [ ] Async decorator support
