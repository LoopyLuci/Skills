---
name: api-rate-limiting
description: "Use when implementing API rate limiting and throttling."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [rate-limiting, throttling, API, token-bucket, leaky-bucket, quota, Redis]
    related_skills: [api-design-rest-graphql, ddos-mitigation-strategies, caching-strategies, api-gateway-load-balancing]
---

# API Rate Limiting

Implementing API rate limiting — from token bucket and sliding window through distributed rate limiting, quota management, and Redis-backed implementations.

## When to Use

- Protecting APIs from abuse and excessive traffic
- Enforcing API usage quotas per customer tier
- Preventing DDoS and brute-force attacks
- Ensuring fair resource allocation across tenants
- Implementing API monetization (rate tiers)

## Rate Limiting Algorithms

```python
import time
from collections import defaultdict

class TokenBucket:
    """Token bucket rate limiter — allows bursts up to capacity."""
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.last_refill = time.time()
    
    def allow(self, tokens: int = 1) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


class SlidingWindow:
    """Sliding window log — precise per-window counting."""
    def __init__(self, window_seconds: int = 60, max_requests: int = 100):
        self.window = window_seconds
        self.max_requests = max_requests
        self.requests = defaultdict(list)  # key -> [timestamps]
    
    def allow(self, key: str) -> bool:
        now = time.time()
        window_start = now - self.window
        self.requests[key] = [t for t in self.requests[key] if t > window_start]
        
        if len(self.requests[key]) < self.max_requests:
            self.requests[key].append(now)
            return True
        return False
```

## Common Pitfalls

1. **Synchronous blocking** — blocking the request thread for rate limiting; use async
2. **Clock skew issues** — distributed rate limiters need synchronized clocks
3. **Rate limiting health checks** — monitoring systems may trip rate limits; whitelist them
4. **No clear error format** — return 429 with Retry-After header and clear error body
5. **Single-node bottleneck** — in-memory rate limiting doesn't scale across instances

## Verification Checklist

- [ ] Algorithm matches use case (token bucket for bursts, sliding window for precise counting)
- [ ] Distributed rate limiting (Redis or similar) for multi-instance deployments
- [ ] 429 response includes Retry-After header
- [ ] Rate limit headers in response (X-RateLimit-Limit, Remaining, Reset)
- [ ] Exemptions for internal/monitoring services
- [ ] Rate limit tiers by subscription level
- [ ] Rate limit monitoring and alerts (proximity to limit)
