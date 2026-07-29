---
name: realtime-dashboard
title: Real-Time Dashboard
description: Use when building live network traffic visualization UI.
category: networking
tags: [dashboard, realtime, visualization, svelte, chart, ui]
---

# Real-Time Dashboard

**Trigger**: Use when implementing real-time traffic visualization for the web UI.

**Libraries**: Svelte 5, Chart.js/D3.js, WebSocket (for live updates), Tailwind CSS

**Implementation**: WebSocket connection to MCP server for live event stream. Chart.js for traffic graphs (area/line for throughput, pie for protocol distribution). Real-time query log table with infinite scroll. Gauges for block rate, latency, active connections. Auto-refresh every 1s for critical metrics. Dark theme with glass-morphism design. Drill-down from summary to per-flow detail.

**Connected**: `traffic-analyzer`, `bandwidth-monitor`, `connection-monitor`, `traffic-historical`, `mcp-network-server`, `svelte-web-dashboard`
