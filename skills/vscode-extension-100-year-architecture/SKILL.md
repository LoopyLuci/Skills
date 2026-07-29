---
name: vscode-extension-100-year-architecture
description: Use for 100-year VS Code extensions. 12 survival patterns.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vscode, extension, 100-year, architecture, patterns, future-proof]
    related_skills: [hermes-agent-skill-authoring]
---

# VS Code Extension 100-Year Architecture Patterns

## Overview

A 100-year architecture isn't about predicting the future — it's about building systems that **survive it**. VS Code will change (or be replaced). MCP will evolve (or be supplanted). Runtimes, OSes, security models, and workflows will shift unpredictably. These patterns isolate every assumption behind a seam, version every schema, degrade gracefully, and never require a rewrite.

## The 7 Foundational Patterns

1. **Zero hardcoded values** — load everything from config/JSON files
2. **Schema versioning** — every state file carries version, auto-migrate on load
3. **Self-healing** — corrupt state repairs from `.bak` backup
4. **Atomic writes** — `.tmp` → backup → rename
5. **Plugin ecosystems** — new tech = new config file, not code
6. **Forward compat** — unknown fields preserved on load
7. **Graceful degradation** — each subsystem fails independently

## The 12 Extension-Specific Dimensions

### 1. Protocol Abstraction Layer

**Do:** Extract `ProtocolAdapter` + `TransportLayer` interfaces. MCPServer becomes an orchestrator holding a registry of adapters.

**Don't:** Hardcode MCP via switch statements over string literals.

**Why:** MCP will version-change multiple times; each protocol is one adapter file.

### 2. VS Code API Adapter

**Do:** Wrap every `vscode.*` call behind versioned adapter classes. Auto-detect on activate.

**Don't:** Call `vscode.window.*` directly in tool handlers.

**Why:** A removed API means tool reports "unavailable," not a crash.

### 3. Plugin Tool Ecosystem

**Do:** `ToolPlugin` interface with manifest, permissions, lifecycle. Load from npm/path/WASM.

**Don't:** Hardcode all tools in TypeScript source.

**Why:** 100 years of new operations = each plugin is one installed package.

### 4. Schema-Versioned State

**Do:** Every stored document carries `_schemaVersion`. Atomic write pattern. Auto-migration.

```
.tmp → backup existing → rename .tmp → delete .bak (success) or restore .bak (failure)
```

**Don't:** Stateless servers or unversioned JSON blobs.

**Why:** Data must survive upgrades, downgrades, and corruption across decades.

### 5. Multi-Transport Resilience

**Do:** `TransportManager` starts multiple transports from config. Exponential backoff retry.

**Don't:** Single HTTP server on a hardcoded port.

**Why:** Port conflicts and new transports must be adoptable via config.

### 6. Rich Tool Self-Description

**Do:** Every tool carries version, examples, deprecation status, error codes, min VS Code version.

**Don't:** 70-character descriptions and zero metadata.

**Why:** An LLM 100 years from now must use the tool from its self-description alone.

### 7. Security Evolution Path

**Do:** Layer: audit logging → token auth → capability-based → zero-trust.

**Don't:** No auth, no audit, no isolation.

**Why:** Every phase preserves backward compatibility for legacy clients.

### 8. LLM Provider Abstraction

**Do:** Provider interface with fallback chain. Config-driven.

**Don't:** Single hardcoded endpoint.

**Why:** LLM technology evolves. Multi-provider with fallback is the only survivable approach.

### 9. Web Component UI

**Do:** Browser-native web components. Framework-agnostic. Dynamic VS Code theme integration.

**Don't:** Monolithic vanilla JS or framework lock-in (React, Vue).

**Why:** Web components survive JS framework churn.

### 10. Testing & Self-Healing

**Do:** Unit + integration + protocol compliance + chaos tests. Health monitor with auto-recovery.

**Don't:** Zero tests, no monitoring.

**Why:** Every change must be verified; failures must be detected and recovered.

### 11. Layered Versioned Config

**Do:** Load from VS Code settings → file → env → CLI → defaults. Validate with schema. Auto-migrate.

**Don't:** Only VS Code's settings.json with no versioning.

**Why:** Unknown keys preserved so newer configs don't break older versions.

### 12. Self-Documenting System

**Do:** ADRs for every decision. Tool docs generated from code. In-app `/help` command.

**Don't:** A single README that goes stale.

**Why:** Documentation is as accurate as the code — because it IS the code.

## Pattern → Dimension Quick Reference

| Pattern | Dimensions |
|---------|-----------|
| Zero hardcoded values | 1 (protocol), 6 (metadata), 11 (config) |
| Schema versioning | 4 (state), 11 (config) |
| Self-healing | 4 (state), 10 (health) |
| Atomic writes | 4 (state) |
| Plugin ecosystem | 3 (tools), 9 (UI), 7 (auth) |
| Forward compat | 2 (adapter), 4 (state), 6 (metadata), 11 (config) |
| Graceful degradation | 1 (protocol), 2 (adapter), 5 (transport), 7 (security) |

## When to Use

- Designing or reviewing any VS Code extension architecture
- Evaluating long-term system survivability (5+ year horizons)
- Planning major refactors across VS Code major versions
- Building plugin systems for editors or IDEs

## Verification Checklist

- [ ] Every external API is behind an adapter interface
- [ ] New protocol/transport/plugin = one file + config entry
- [ ] Config has `_version`, validates, auto-migrates, preserves unknown keys
- [ ] State has `_schemaVersion`, atomic writes, backup recovery
- [ ] Every tool has version, examples, deprecation metadata
- [ ] A removed VS Code API causes tool degradation, not crash
- [ ] Failing transport doesn't block other transports
- [ ] Security has evolution path from trust to zero-trust
- [ ] UI is framework-agnostic (web components)
- [ ] Tests at unit, integration, protocol, and chaos levels
- [ ] Health monitor detects and recovers subsystem failures
- [ ] Architecture decisions recorded as ADRs
