---
name: dns-adblock-engine
title: DNS Ad-Blocking Engine
description: Use when building DNS ad-blocking with blocklist matching.
category: networking
tags: [dns, adblock, hickory, rust, blocklist, filtering]
---

# DNS Ad-Blocking Engine

**Trigger**: Use when building DNS-level ad blocking with blocklist parsing and filtering.

## Key Libraries
- **Rust**: `hickory-dns`, `hickory-client`, `hickory-proto`, `adblock` (Brave's engine)
- **Python**: `dnspython`, `asyncio`
- **Clojure**: `clara-rules` for rule-based blocklist decisions

## Implementation
1. Primary engine in Rust using `hickory-dns` for DNS protocol handling
2. Blocklist parser supporting EasyList (`||domain.com^`), hosts (`0.0.0.0 domain.com`), plain domains
3. Multi-strategy matcher: Hash set exact (O(1)) → wildcard suffix trie → subdomain walk → regex
4. LRU DNS cache using Rust's `lru` crate with configurable TTL per record type
5. Bloom filter pre-check against massive blocklists (millions of entries)

## Connected Skills
`encrypted-dns-resolver`, `dns-cache-layer`, `blocklist-manager`, `packet-capture-engine`

## Pitfalls
- Hickory DNS async runtime conflicts — use separate Tokio runtime for DNS vs packet capture
- Aho-Corasick automaton rebuild is expensive — batch domain updates
- Bloom filter false positives require exact-match fallback chain
