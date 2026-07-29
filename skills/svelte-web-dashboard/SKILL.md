---
name: svelte-web-dashboard
title: Svelte Web Dashboard
description: Use when building the Sentinel web UI with Svelte 5.
category: networking
tags: [svelte, frontend, ui, dashboard, typescript, vite]
---

# Svelte Web Dashboard

**Trigger**: Use when building or modifying the Sentinel web dashboard UI.

**Libraries**: Svelte 5, SvelteKit, TypeScript, Vite, Tailwind CSS 4, Chart.js, lucide-svelte

**Implementation**: SvelteKit with static adapter for SPA deployment. Routes: /dashboard, /queries, /firewall, /filters, /analytics, /settings. Component tree: Layout (Sidebar + TopBar) → Pages → Widgets. API client via fetch with TypeScript types. MCP WebSocket client for live updates. Reactive state with Svelte 5 $state/$derived runes. Responsive: mobile sidebar collapses.

**Connected**: `realtime-dashboard`, `mcp-network-server`, `rust-core-ffi`, `python-orchestrator`, `service-orchestrator`
