---
name: load-testing
description: Benchmark APIs with locust ramp up concurrency and breakpoints
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [load, testing]
---

# Load Testing

## Locust
```python
# locustfile.py
from locust import HttpUser, task

class MyUser(HttpUser):
    @task
    def index(self):
        self.client.get("/")
```

## Run
```bash
pip install locust
locust -f locustfile.py --host=http://localhost:8000
# Open http://localhost:8089
```

## Key Metrics
- RPS (requests per second)
- P50/P95/P99 latency
- Error rate
- Concurrent users

## Trigger

Activate this skill when the user mentions:
- load, testing workflows or issues
- Building, fixing, or optimizing load testing


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
