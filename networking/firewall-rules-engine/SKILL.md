---
name: firewall-rules-engine
title: Firewall Rules Engine
description: Use when implementing L3/L4 stateful firewall rules.
category: networking
tags: [firewall, rules, stateful, nftables, wfp, rust]
---

# Firewall Rules Engine

**Trigger**: Use when implementing Layer 3/4 firewall rules with stateful filtering.

**Libraries**: `netlink-sys`/`rtnetlink` (Linux), `nftables` crate, `windows-wfp` (Windows WFP), `nftnl`

**Implementation**: Linux via `nftables` crate (tables/chains/rules/sets, atomic batch updates). Windows via `windows-wfp` (WFP callout drivers, Fwpm* API). macOS via `pfctl` subprocess. Connection tracking: 5-tuple state table with TCP state machine. Rule priority with first-match semantics. Atomic rule swap with rollback.

**Connected**: `packet-capture-engine`, `port-scanner-detection`, `connection-tracker`, `pattern-matching-engine`, `traffic-shaper`, `service-orchestrator`
