---
name: dns-cache-layer
description: Use when caching DNS responses with TTL and prefetch.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [dns, cache, performance, lru, concurrent, rust]
---

# DNS Cache Layer

**Trigger**: Use when implementing DNS response caching, prefetching, or negative caching.

## Key Libraries
- **Rust**: `lru`, `moka` (high-perf concurrent cache), `dashmap`, `scc`
- **Python**: `cachetools`, `aiocache`

## Implementation
1. Two-tier cache: L1 (hot, moka concurrent, ~10K) + L2 (warm, scc sharded, ~1M)
2. TTL-aware eviction with min/max bounds (clamp to configurable range)
3. Negative caching: cache NXDOMAIN with short TTL (60-300s) to reduce upstream load
4. Prefetch: predict popular domains via frequency tracking; refresh before TTL expiry
5. Serialization for persistence via `bincode` or `messagepack`

## Connected Skills
`dns-adblock-engine`, `encrypted-dns-resolver`, `realtime-dashboard`, `traffic-analyzer`

## Pitfalls
- Concurrent eviction + prefetch causes thundering herd — use `moka::try_get_with`
- Serialization must include expiry timestamps, not just TTL
