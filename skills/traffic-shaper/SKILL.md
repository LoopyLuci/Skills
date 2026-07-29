---
name: traffic-shaper
title: Traffic Shaper
description: Use when implementing QoS bandwidth shaping and queuing.
category: networking
tags: [traffic, shaping, qos, bandwidth, queue, rust]
---

# Traffic Shaper

**Trigger**: Use when implementing traffic shaping, QoS, and bandwidth management.

**Libraries**: `tokio` (timers), `dashmap` (per-flow state), `pnet`

**Implementation**: Token bucket per-flow/per-IP rate limiting. Hierarchical Token Bucket (HTB) for multi-level QoS. DSCP packet marking for priority. Bandwidth classes: real-time (VoIP/gaming), normal (web), bulk (downloads). Per-application bandwidth limits via protocol-identifier integration. Leaky bucket for burst control. Shaping statistics dashboard.

**Connected**: `bandwidth-monitor`, `application-filter`, `connection-tracker`, `encrypted-dns-resolver`, `firewall-rules-engine`, `realtime-dashboard`
