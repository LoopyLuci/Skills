---
name: encrypted-dns-resolver
title: Encrypted DNS Resolver
description: Use when adding DoH/DoT/DNSCrypt with fallback pooling.
category: networking
tags: [dns, doh, dot, encryption, privacy, rust]
---

# Encrypted DNS Resolver

**Trigger**: Use when implementing DNS-over-HTTPS (DoH), DNS-over-TLS (DoT), or DNSCrypt support.

## Key Libraries
- **Rust**: `hickory-resolver` (built-in DoH/DoT), `rustls`, `tokio-rustls`, `dns-over-https`
- **Python**: `dnspython` (DoH support in v2.x)

## Implementation
1. Multiplexed upstream connections via `hickory-resolver` with TLS client config
2. Round-robin across multiple DoH providers (Cloudflare, Quad9, NextDNS, custom)
3. Automatic fallback: DoH → DoT → plain UDP with configurable timeout cascade
4. Connection pooling with `tokio` — reuse TLS sessions for multiple queries
5. DNSSEC validation chain verification (RRSIG/DS/DNSKEY)

## Connected Skills
`dns-adblock-engine`, `dns-cache-layer`, `url-content-filter`, `traffic-shaper`

## Pitfalls
- DoH over HTTP/2 requires h2 crate or hyper with h2 feature
- TLS certificate pinning essential to prevent MITM on upstream DNS
- DNSSEC validation adds ~30% latency — make configurable per-domain
