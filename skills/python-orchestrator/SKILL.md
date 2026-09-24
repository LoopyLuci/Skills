---
name: python-orchestrator
description: Use when orchestrating Sentinel from Python scripts.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [python, orchestration, cli, api, scripting, integration]
---

# Python Orchestrator

**Trigger**: Use when writing Python scripts to control Sentinel.

**Libraries**: `asyncio`, `websockets` (MCP client), `httpx` (REST API), `click` (CLI)

**Implementation**: Async MCP client connecting to WebSocket at ws://127.0.0.1:9822. High-level API: block_domain, allow_domain, add_rule, get_status. CLI interface via `click` for scripting. Scheduled tasks via `asyncio` for blocklist updates, report generation. Integration with Hermes Agent via Python SDK. REST API client as fallback when MCP unavailable.

**Connected**: `rust-core-ffi`, `mcp-network-server`, `service-orchestrator`, `svelte-web-dashboard`, `clojure-rule-engine`
