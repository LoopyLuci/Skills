---
name: tls-ssl-inspector
description: Use when inspecting TLS handshakes and certificate metadata.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [tls, ssl, inspection, sni, certificate, rust]
---

# TLS/SSL Inspector

**Trigger**: Use when inspecting TLS/SSL handshake metadata without decryption.

**Libraries**: `rustls`, `tokio-rustls`, `pcap`, `pnet`

**Implementation**: Parse TLS ClientHello for SNI (Server Name Indication), ALPN, supported ciphers. JA3/JA3S fingerprinting for TLS client/browser identification. Certificate chain validation and expiration checking. Passive inspection only — no MITM decryption. TLS version enforcement (block <1.2). Export SNI to protocol-identifier for categorization.

**Connected**: `protocol-identifier`, `http-https-inspector`, `pattern-matching-engine`, `url-content-filter`
