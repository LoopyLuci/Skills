---
name: application-filter
description: Use when filtering apps via protocol identification.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [application, filter, l7, block, allow, rust]
---

# Application Filter

**Trigger**: Use when implementing application-level filtering (block Steam, Netflix, etc.).

**Libraries**: `protocol-identifier`, `ndpi-sys`, `pnet`

**Implementation**: Protocol-based application blocking: identify app via nDPI, then apply allow/block policy. Application signatures for 300+ protocols. Per-application bandwidth limits. Time-based scheduling (block games during school hours). Integration with traffic-shaper for QoS. Application usage statistics dashboard.

**Connected**: `protocol-identifier`, `http-https-inspector`, `url-content-filter`, `parental-controls`, `traffic-shaper`, `bandwidth-monitor`
