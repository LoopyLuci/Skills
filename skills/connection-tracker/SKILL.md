---
name: connection-tracker
title: Connection Tracker
description: Use when tracking TCP/UDP state and exporting flows.
category: networking
tags: [connection, tracking, stateful, netflow, conntrack, rust]
---

# Connection Tracker

**Trigger**: Use when implementing connection state tracking and flow table management.

**Libraries**: `dashmap`/`scc` (concurrent flow table), `etherparse`

**Implementation**: TCP state machine (CLOSED→SYN_SENT→ESTABLISHED→...→CLOSED) with per-state timeouts. UDP pseudo-state with idle timeout. ICMP echo tracking via identifier. 5-tuple key (src_ip,dst_ip,src_port,dst_port,protocol). Lock-free conntrack table with `dashmap`. Periodic flow aging. NetFlow v9 export with packet/byte counters.

**Connected**: `packet-capture-engine`, `firewall-rules-engine`, `application-filter`, `traffic-analyzer`, `connection-monitor`
