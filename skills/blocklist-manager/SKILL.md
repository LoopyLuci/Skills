---
name: blocklist-manager
title: Blocklist Manager
description: Use when downloading and merging blocklists at scale.
category: networking
tags: [blocklist, download, parse, merge, scale, rust]
---

# Blocklist Manager

**Trigger**: Use when managing, downloading, parsing, or merging blocklists at scale.

## Key Libraries
- **Rust**: `reqwest` (HTTP), `flate2`/`zstd` (compression), `serde`/`csv`
- **Python**: `httpx`, `orjson` (fast JSON), `celery` (scheduled updates)

## Implementation
1. Async downloader with ETag/If-Modified-Since support to minimize bandwidth
2. Incremental parsing: stream-process lists >100MB without loading entirely into memory
3. Deduplication: Bloom filter for initial pass, exact hash set for final merge
4. Versioned snapshots as binary formats (FlatBuffers/Cap'n Proto) for fast loading
5. Auto-update scheduler with atomic swap and rollback on parse failure
6. Compatible with AdGuard, Pi-hole, and uBlock Origin list formats

## Connected Skills
`dns-adblock-engine`, `blocklist-scale-arch`, `realtime-dashboard`, `clojure-rule-engine`

## Pitfalls
- Some blocklists exceed 500MB — streaming parser is mandatory
- ETag support varies by CDN — implement fallback to If-Modified-Since
