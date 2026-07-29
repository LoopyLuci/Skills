---
name: blocklist-scale-arch
title: Blocklist Scale Architecture
description: Use when scaling blocklist processing to millions of rules.
category: networking
tags: [blocklist, scale, millions, bloom, aho-corasick, performance]
---

# Blocklist Scale Architecture

**Trigger**: Use when scaling blocklist processing to millions of rules.

**Libraries**: `aho-corasick` (multi-pattern), `bloom` (Bloom filter), `scc` (concurrent map)

**Implementation**: Three-tier matching: Bloom filter pre-check (O(1), may false-positive) → Aho-Corasick automaton (O(n), exact) → regex fallback (slow path). Sharded domain map across 24 threads via `scc::HashMap`. Incremental automaton rebuild on blocklist updates (background thread, atomic swap). Memory-mapped pattern files for fast loading. LZ4 compression for on-disk storage.

**Connected**: `blocklist-manager`, `dns-adblock-engine`, `dns-cache-layer`, `pattern-matching-engine`, `gpu-packet-classifier`
