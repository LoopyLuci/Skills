---
name: mcp-threat-intel
title: MCP Threat Intelligence
description: Use when exposing threat intel data via MCP to agents.
category: networking
tags: [mcp, threat, intelligence, agents, security, sharing]
---

# MCP Threat Intelligence

**Trigger**: Use when exposing threat intelligence data and feeds via MCP.

**Libraries**: `serde_json`, `tokio-tungstenite`, `reqwest` (feed fetching)

**Implementation**: MCP resource endpoints for threat intel: sentinel://threats/active, sentinel://threats/historical. Pull feeds from AlienVault OTX, AbuseIPDB, VirusTotal. Standardized threat format: IP, domain, score, category, first-seen, last-seen, tags. MCP tool: submit_threat_ioc for agent-contributed intel. STIX/TAXII format support. Automated blocklist generation from confirmed threats.

**Connected**: `mcp-network-server`, `ml-threat-detection`, `blocklist-manager`, `dns-adblock-engine`, `firewall-rules-engine`
