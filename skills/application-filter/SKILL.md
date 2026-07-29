---
name: application-filter
title: Application Filter
description: Use when filtering apps via protocol identification.
category: networking
tags: [application, filter, l7, block, allow, rust]
---

# Application Filter

**Trigger**: Use when implementing application-level filtering (block Steam, Netflix, etc.).

**Libraries**: `protocol-identifier`, `ndpi-sys`, `pnet`

**Implementation**: Protocol-based application blocking: identify app via nDPI, then apply allow/block policy. Application signatures for 300+ protocols. Per-application bandwidth limits. Time-based scheduling (block games during school hours). Integration with traffic-shaper for QoS. Application usage statistics dashboard.

**Connected**: `protocol-identifier`, `http-https-inspector`, `url-content-filter`, `parental-controls`, `traffic-shaper`, `bandwidth-monitor`
