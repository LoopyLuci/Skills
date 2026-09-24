---
name: svelte-web-dashboard
description: Use when building the Sentinel web UI with Svelte 5.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [svelte, frontend, ui, dashboard, typescript, vite]
---

# Svelte Web Dashboard

**Trigger**: Use when building or modifying the Sentinel web dashboard UI.

**Libraries**: Svelte 5, SvelteKit, TypeScript, Vite, Tailwind CSS 4, Chart.js, lucide-svelte

**Implementation**: SvelteKit with static adapter for SPA deployment. Routes: /dashboard, /queries, /firewall, /filters, /analytics, /settings. Component tree: Layout (Sidebar + TopBar) → Pages → Widgets. API client via fetch with TypeScript types. MCP WebSocket client for live updates. Reactive state with Svelte 5 $state/$derived runes. Responsive: mobile sidebar collapses.

**Connected**: `realtime-dashboard`, `mcp-network-server`, `rust-core-ffi`, `python-orchestrator`, `service-orchestrator`
