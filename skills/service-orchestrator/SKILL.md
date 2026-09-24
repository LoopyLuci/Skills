---
name: service-orchestrator
description: Use when managing multi-platform Sentinel service lifecycle.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [service, orchestration, lifecycle, systemd, launchd, windows]
---

# Service Orchestrator

**Trigger**: Use when implementing cross-platform service installation and lifecycle management.

**Libraries**: Platform-specific: `systemd` (Linux), `ServiceManagement` (macOS), `windows-service` (Windows)

**Implementation**: Service install via platform mechanism: systemd unit on Linux, launchd plist on macOS, sc.exe on Windows. Health check endpoint polling every 30s. Automatic restart on crash with exponential backoff. Graceful shutdown: SIGTERM → drain connections → persist state → exit. Log rotation with configurable max size. Update mechanism: atomic binary swap.

**Connected**: `multi-platform-installer`, `rust-core-ffi`, `python-orchestrator`, `mcp-network-server`, `svelte-web-dashboard`
