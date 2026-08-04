---
name: bandwidth-monitor
title: Bandwidth Monitor
description: Use when monitoring bandwidth usage per flow or device.
category: networking
tags: [bandwidth, monitor, usage, traffic, analytics, rust]
---

# Bandwidth Monitor

**Trigger**: Use when implementing bandwidth usage monitoring and reporting.

**Libraries**: `dashmap`, `tokio` (timers), `chrono`

**Implementation**: Per-flow byte/packet counters updated on each packet. Per-device aggregation: sum flows by source IP. Per-application bandwidth via protocol-identifier integration. Time-based bucketing (second, minute, hour, day). Rolling window for real-time display. Historical storage in timeseries DB. Quota enforcement with alerts. Monthly usage reports.

**Connected**: `traffic-shaper`, `traffic-analyzer`, `connection-monitor`, `connection-tracker`, `realtime-dashboard`, `traffic-historical`
