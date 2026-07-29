---
name: mcp-network-server
title: MCP Network Server
description: Use when exposing network tools via Model Context Protocol.
category: networking
tags: [mcp, protocol, agent, tools, network, rust]
---

# MCP Network Server

**Trigger**: Use when exposing firewall/network capabilities as MCP tools for AI agents.

**Libraries**: `tokio-tungstenite` (WebSocket), `serde_json`, `axum` (HTTP/SSE transport)

**Implementation**: Full MCP protocol server with JSON-RPC 2.0 over WebSocket and SSE transports. Tools: get_status, block/unblock domain, add/remove firewall rule, get query log, update blocklists. Resources: sentinel://status, stats, log/query. Per-connection state isolation. Tool input validation with JSON Schema. Event subscription for real-time alerts.

**Connected**: All other skills — this is the universal agent interface. Specifically: `dns-adblock-engine`, `firewall-rules-engine`, `ml-threat-detection`
