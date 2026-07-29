---
name: caching-strategies
description: "Use when implementing caching strategies for applications."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [caching, redis, CDN, cache-invalidation, performance, write-through, write-behind]
    related_skills: [performance-optimization, event-driven-architecture, distributed-systems-patterns, api-design-rest-graphql]
---

# Caching Strategies

Implementing caching strategies for web applications, APIs, and distributed systems — from in-memory through distributed cache, CDN, and cache invalidation patterns.

## When to Use

- Reducing database load for frequently accessed data
- Improving API response times
- Implementing distributed caching for scalability
- Designing cache invalidation strategies
- Choosing between local, distributed, and CDN caching

## Caching Patterns

```python
CACHE_PATTERNS = {
    'cache_aside': 'App checks cache first, loads from DB on miss, populates cache',
    'read_through': 'Cache loads from DB automatically on miss',
    'write_through': 'Data written to cache and DB simultaneously',
    'write_behind': 'Data written to cache immediately, DB asynchronously',
    'write_around': 'Data written to DB directly, cache invalidated',
    'refresh_ahead': 'Cache proactively refreshes before expiration',
}

class CacheAside:
    """Cache-Aside pattern implementation."""
    def __init__(self, cache, db):
        self.cache = cache
        self.db = db
    
    def get(self, key: str) -> any:
        result = self.cache.get(key)
        if result is not None:
            return result
        result = self.db.query(key)
        self.cache.set(key, result, ttl=300)
        return result
```

## Common Pitfalls

1. **Stale data** — cache invalidation is one of the hardest problems in CS
2. **Cache stampede** — many requests miss cache simultaneously, overloading DB
3. **Thundering herd** — multiple requests regenerate cache at same time; use locking
4. **Memory overuse** — caching too much data evicts useful data; set TTLs wisely
5. **Distributed cache consistency** — nodes can have different cached versions

## Verification Checklist

- [ ] Cache hit ratio > 80% for hot data
- [ ] TTLs set appropriately for data freshness needs
- [ ] Cache stampede protection (mutex/lock on miss)
- [ ] Monitoring on cache hit/miss ratios
- [ ] Invalidation strategy defined for data updates
