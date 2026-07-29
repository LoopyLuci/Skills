---
name: genesis-integration-layer
description: "Use when integrating the Skill Genesis Model into any agent."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [genesis, integration, MCP, API, plugin, agents, portability]
    related_skills: [skill-genesis-model, mcp-server, hermes-agent, autonomous-ai-agents]
---

# Genesis Integration Layer

Universal integration layer that exposes the Skill Genesis Model to any
agent framework. Supports MCP, REST API, OpenAI-compatible function calling,
Hermes Plugin, and CLI bridge.

## Architecture

```
                    ┌─────────────────────────────────────────┐
                    │         Genesis Integration Layer        │
                    ├─────────────────────────────────────────┤
                    │                                          │
  ┌──────────┐     ┌─┐  ┌──────────┐  ┌────────────┐  ┌─────┐│
  │ Claude   │─────►M├──► Genesis  │  │ OpenAI API │  │CLI  ││
  │ Desktop  │     │C│  │ Server   │  │ Server     │  │Bridge││
  ├──────────┤     │P├──└─────┬────┘  └──────┬─────┘  └──┬──┘│
  │ Cursor   │─────► ├────────┤             │            │   │
  ├──────────┤     │ │        │             │            │   │
  │ Copilot  │─────►─┘        ▼             ▼            ▼   │
  ├──────────┤          ┌──────────────────────────────┐     │
  │ Custom   │─────────►│   Skill Genesis Model v3.0   │     │
  │ Agent    │          │   (7 integrated tools)        │     │
  └──────────┘          └──────────────────────────────┘     │
                    └─────────────────────────────────────────┘
```

## Integration Methods

| Method | Best For | Setup |
|--------|----------|-------|
| **MCP Server** | Claude Desktop, Cursor, Windsurf, Copilot | `python scripts/mcp_server.py` |
| **REST API** | Custom agents, webhooks, automation | `python scripts/api_server.py` |
| **Hermes Plugin** | Hermes Agent native tools | Load skill + use `plugin_genesis.py` |
| **CLI Bridge** | Claude Code, Codex, any shell-capable agent | `python skill_genesis.py --audit` |
