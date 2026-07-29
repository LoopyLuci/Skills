---
name: http-https-inspector
title: HTTP/HTTPS Inspector
description: Use when inspecting HTTP traffic and extracting metadata.
category: networking
tags: [http, https, inspection, metadata, proxy, rust]
---

# HTTP/HTTPS Inspector

**Trigger**: Use when inspecting HTTP/HTTPS traffic for content filtering.

**Libraries**: `hyper`, `http`, `pnet` (reassembly), `url`

**Implementation**: HTTP request/response parsing: method, path, headers, content-type, referer. Host-based filtering without full decryption. HTTP/2 frame parsing (h2 crate). Request frequency tracking per client. File type blocking based on Content-Type extensions. For HTTPS: rely on SNI + JA3 fingerprinting.

**Connected**: `tls-ssl-inspector`, `url-content-filter`, `application-filter`, `parental-controls`, `traffic-analyzer`
