---
name: proxy-server-engine
description: Use when building HTTP/SOCKS proxy with filtering.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [proxy, http, socks, forward, transparent, rust]
---

# Proxy Server Engine

**Trigger**: Use when implementing HTTP/HTTPS/SOCKS proxy server with filtering.

**Libraries**: `hyper`, `tokio`, `http`, `url`, `base64` (auth)

**Implementation**: HTTP CONNECT proxy for HTTPS tunnels. SOCKS5 protocol support (RFC 1928) with UDP ASSOCIATE. Transparent proxy via iptables REDIRECT/TPROXY. Proxy authentication (basic, digest, SOCKS5 user/pass). Request filtering by URL, domain, content-type. Connection pooling to upstream. Proxy chaining support.

**Connected**: `vpn-tunnel-engine`, `url-content-filter`, `http-https-inspector`, `application-filter`, `parental-controls`, `mcp-network-server`
