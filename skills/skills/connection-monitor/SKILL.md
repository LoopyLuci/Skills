---
name: connection-monitor
title: Connection Monitor
description: Use when monitoring active connections and their states.
category: networking
tags: [connection, monitor, active, state, tracking, rust]
---

# Connection Monitor

**Trigger**: Use when monitoring active connections and their lifecycle states.

**Libraries**: `connection-tracker`, `dashmap`, `chrono`, `tokio`

**Implementation**: Real-time active connection table: source, destination, protocol, state, duration, bytes transferred. Connection counts per state (ESTABLISHED, TIME_WAIT, etc.). Connection rate: new connections/second. Per-IP connection limits with threshold alerts. Dead connection detection and cleanup. Export to dashboard via MCP event stream.

**Connected**: `connection-tracker`, `port-scanner-detection`, `traffic-analyzer`, `bandwidth-monitor`, `realtime-dashboard`
