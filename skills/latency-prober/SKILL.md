---
name: latency-prober
description: Use when measuring network latency to destinations.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [latency, probe, ping, measurement, monitoring, rust]
---

# Latency Prober

**Trigger**: Use when implementing active latency measurement and monitoring.

**Libraries**: `tokio` (timers), `icmp` (raw sockets, needs CAP_NET_RAW), `ping` crate

**Implementation**: ICMP ping to configured targets at configurable intervals. TCP connect latency measurement to ports (80, 443, custom). HTTP request timing (DNS + connect + TLS + first byte). Latency histograms: min, max, avg, p50, p95, p99 for each target. Jitter calculation: variance of consecutive measurements. Packet loss percentage. MCP resource: sentinel://latency.

**Connected**: `connection-monitor`, `traffic-analyzer`, `bandwidth-monitor`, `realtime-dashboard`, `mcp-network-server`
