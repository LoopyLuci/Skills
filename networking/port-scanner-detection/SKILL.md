---
name: port-scanner-detection
title: Port Scanner Detection
description: Use when detecting port scans and adding dynamic blocks.
category: networking
tags: [port-scan, detection, security, dynamic-block, rust]
---

# Port Scanner Detection

**Trigger**: Use when implementing port scan detection and throttling.

**Libraries**: `pcap`, `pnet`, `dashmap` (concurrent state)

**Implementation**: Sliding window: count unique ports per source IP within time window. Configurable thresholds (N ports in M seconds). TCP flag anomaly detection (SYN-only, FIN-only, X-mas, NULL). Dynamic block: auto-add nftables/WFP rule with configurable duration. Rate limiting option. Whitelist trusted scanners.

**Connected**: `packet-capture-engine`, `firewall-rules-engine`, `connection-monitor`, `gpu-packet-classifier`
