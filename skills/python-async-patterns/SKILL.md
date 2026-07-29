---
name: python-async-patterns
description: "Use when implementing async Python patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [python, async, asyncio, coroutines, tasks, event-loop]
    related_skills: [cross-thread-async, python-asyncio-gui-threading, data-pipeline-streaming]
---

# Python Async Patterns

Implementing async Python — from asyncio patterns through concurrency, async context managers, and async generators.

## When to Use

- Writing async Python code
- Managing asyncio tasks and event loops
- Building async APIs and data pipelines

## Async Patterns

```python
import asyncio

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)

class AsyncCounter:
    """Async context manager pattern."""
    def __init__(self, limit): self.limit = limit
    async def __aenter__(self): return self
    async def __aexit__(self, *e): await self.close()
    async def close(self): pass
```

## Verification Checklist

- [ ] Async context managers for resources
- [ ] Task groups for structured concurrency (Python 3.11+)
- [ ] asyncio.gather with return_exceptions=True
- [ ] Semaphore for limiting concurrent tasks
- [ ] Proper cancellation handling
