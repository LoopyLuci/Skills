---
name: redis-caching-patterns
description: "Use when implementing Redis caching and data structures."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [redis, caching, pub-sub, streams, sorted-sets, caching-strategies]
    related_skills: [caching-strategies, message-queue-patterns, api-rate-limiting]
---

# Redis Caching Patterns

Implementing Redis caching and data structures — from caching strategies through pub/sub, streams, sorted sets, and rate limiting.

## When to Use

- Implementing Redis caching layers
- Real-time data structures (leaderboards, queues)
- Pub/sub messaging and event streaming
- Distributed rate limiting and locking

## Redis Patterns

```python
import redis.asyncio as redis

class RedisCache:
    def __init__(self): self.r = redis.Redis()
    
    async def cached_query(self, key: str, ttl: int = 300):
        cached = await self.r.get(key)
        if cached: return cached
        
        result = await expensive_query()
        await self.r.setex(key, ttl, result)
        return result

# Distributed rate limiter (sliding window)
class RateLimiter:
    def __init__(self, r): self.r = r
    
    async def allow(self, key: str, max_req: int, window: int = 60):
        now = int(time.time() * 1000)
        pipe = self.r.pipeline()
        pipe.zadd(f"rl:{key}", {now: now})
        pipe.zremrangebyscore(f"rl:{key}", 0, now - window * 1000)
        pipe.zcard(f"rl:{key}")
        pipe.expire(f"rl:{key}", window + 1)
        _, _, count, _ = await pipe.execute()
        return count <= max_req
```

## Verification Checklist

- [ ] Cache strategy chosen (cache-aside, write-through, write-behind)
- [ ] TTLs set appropriately for data freshness
- [ ] Pub/sub for real-time notifications
- [ ] Streams for persistent message queues
- [ ] Sorted sets for leaderboards and range queries
- [ ] Redis Sentinel/Cluster for high availability
