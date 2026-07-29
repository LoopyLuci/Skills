---
name: mcp-server-development
description: "Build custom MCP servers. Use when user wants agentic tools."
version: 1.0.0
author: Hermes Agent + User
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mcp, python, server-building, agent-tools, hermes-integration, sqlite, custom-tools]
    related_skills: [hermes-agent]
---

# MCP Server Development — Building Custom Agentic Tools

## Overview

When the user asks for "agentic tools," "MCP tools," "automation tools," or "custom MCP servers," their **default preference is to BUILD custom Python MCP servers from scratch on their laptop**, NOT to list or recommend existing third-party MCP servers. The deliverable is a working artifact backed by real code — not a catalog of what exists.

This skill covers the architecture, patterns, and pitfalls for building standalone Python MCP servers that:
- Run 100% locally with SQLite persistence
- Expose 15–25+ tools per server via the MCP protocol
- Integrate with Hermes Agent as stdio child processes
- Store all data in `~/.hermes/mcp-data/`
- Ship as independently runnable Python scripts

## When to Use

- User says "I want agentic tools" — BUILD, don't SUGGEST
- User asks for MCP servers for real estate, social media, marketing, daily life — BUILD custom local ones
- User says "custom tools that run locally on my laptop with MCP built in"
- User asks for automation tools across any domain (finance, content, CRM, scraping)
- You need to add a new capability to Hermes that doesn't exist as an MCP server

**Don't use for:**
- Configuring existing MCP servers in Hermes (use `hermes-agent` skill's `references/native-mcp.md`)
- Ad-hoc one-off tool calls (use `mcporter` skill)
- System tool design (shell scripts, desktop automations without MCP)

## Architecture

### Project Structure

```
project-root/
├── pyproject.toml
├── README.md
└── src/
    ├── common/
    │   ├── __init__.py
    │   └── db.py              # Shared SQLite utilities
    └── servers/
        ├── __init__.py
        ├── domain_one.py       # Standalone MCP server — 20+ tools
        ├── domain_two.py       # Standalone MCP server — 20+ tools
        └── domain_three.py     # Standalone MCP server — 20+ tools
```

### Each Server File Is Independently Runnable

Each `servers/*.py` file contains a complete MCP server that can be run standalone:
```bash
python src/servers/my_server.py
```
And registered in Hermes config as its own stdio subprocess.

### Shared Database Layer

All servers share a lightweight SQLite wrapper. Init at module level (outside async). Use `sqlite3.Row` as row_factory, enable WAL mode, create schema via `executescript()`.

## MCP Server Structure

### Required Pattern (MCP SDK v1.x)

```python
import asyncio
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import ServerCapabilities, ToolsCapability
import mcp.server.stdio
import mcp.types as types

# MUST: sys.path trick for standalone script imports
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

server = Server("my-server-name")
conn = init_db("my_server", SCHEMA)  # MODULE level, not async

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(name="my_tool", description="...",
            inputSchema={"type": "object", "properties": {...}, "required": [...]}),
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "my_tool":
        return [types.TextContent(type="text", text="result")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read, write):
        await server.run(read, write, InitializationOptions(
            server_name="my-server-name",
            server_version="1.0.0",
            capabilities=ServerCapabilities(tools=ToolsCapability()),  # REQUIRED
        ))

if __name__ == "__main__":
    asyncio.run(main())
```

### 🔴 Critical: InitializationOptions Capabilities

`InitializationOptions` **requires** the `capabilities` field. Without it, the server crashes with `pydantic.ValidationError`. Always include `capabilities=ServerCapabilities(tools=ToolsCapability())`.

### 🔴 Critical: Import Strategy for Standalone Scripts

Standalone runnable scripts CANNOT use relative imports (`from ..common.db import ...` fails with `ImportError: attempted relative import beyond top-level package`). Use the `sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))` hack before local imports.

### Tool Handler Pattern

Return `list[types.TextContent]` — each with `type="text"` and `text` field. Use `if/elif/else` dispatch with `raise ValueError(f"Unknown tool: {name}")`.

## Hermes Config Wiring

```yaml
mcp_servers:
  my-server:
    command: "python"
    args: ["C:/absolute/path/to/src/servers/my_server.py"]
    timeout: 30
```

On Windows, use absolute paths. On restart, Hermes spawns the subprocess and all tools appear with the `mcp_my_server_` prefix.

## Tool Design Guidelines

- Target **15–25 tools per server**
- Use `verb_noun` naming: `task_add`, `note_search`, `campaign_create`
- Write LLM-facing descriptions (80-200 chars)
- Include `"description"` on every property in inputSchema
- Use enums where possible
- Return structured text with emoji prefixes (✅ ❌ 📋 📊 ℹ️)
- Include primary result in the first line

## Database Schema Design

- Each server gets its own database at `~/.hermes/mcp-data/{name}.db`
- Create all tables in a single `SCHEMA` constant string
- Include `created_at` and `updated_at` timestamps
- Use `TEXT` for dates (ISO 8601)
- Use foreign keys for relational data
- Seed default data via module-level function called at import time

## Verification Checklist

- [ ] Server imports cleanly via `from servers.my_server import server`
- [ ] `list_tools()` returns all expected tools with valid schemas
- [ ] `capabilities=ServerCapabilities(tools=ToolsCapability())` in `InitializationOptions`
- [ ] `sys.path.insert(0, ...)` present for standalone imports
- [ ] Database init at module level (not inside async main)
- [ ] At least one tool call works: `handle_call_tool("tool", {"param": "val"})`
- [ ] All returns use `list[types.TextContent]`
- [ ] Fallback `raise ValueError(f"Unknown tool: {name}")` present
- [ ] Hermes config includes the server under `mcp_servers:`
- [ ] Server startup does not crash (test with timeout)

## Common Pitfalls

1. **Missing `capabilities` in `InitializationOptions`** — crashes with `pydantic.ValidationError`. Always include `capabilities=ServerCapabilities(tools=ToolsCapability())`.

2. **Relative imports in standalone scripts** — `from ..common.db import ...` fails because standalone scripts aren't run as a package. Use the `sys.path.insert(0, ...)` hack before local imports.

3. **Database init inside `async def main()`** — decorators registered during import may access `conn` before `main()` runs. Init at module level.

4. **`call_tool` handler not async** — MCP SDK expects async handlers. Mark with `async def`.

5. **Returning raw string instead of `list[types.TextContent]`** — MCP protocol expects content array.

6. **Forgetting user preference to BUILD** — When user asks for "tools" or "MCP tools," default to building custom local Python servers, not cataloging existing ones. "I want agentic tools" means "write code."

7. **Subprocess pipe testing on Windows** — `asyncio.create_subprocess_exec` + stdin/stdout piping is unreliable for MCP protocol testing. Test imports + `list_tools()` + `handle_call_tool()` via direct Python calls.

## One-Shot Recipes

### Create a New MCP Server from Scratch

1. Create `src/common/db.py` with shared database utilities
2. Create `src/servers/{domain}.py` with the full pattern (imports, schema, server init, list_tools, call_tool, main)
3. Add to Hermes config under `mcp_servers:`
4. Verify: import + list_tools + tool call

### Verify All Servers Work

```python
import sys; sys.path.insert(0, 'src')
from servers.my_server import server, list_tools, handle_call_tool
import asyncio

async def verify():
    tools = await list_tools()
    print(f"{len(tools)} tools")
    result = await handle_call_tool("my_tool", {"key": "val"})
    print(result[0].text[:100])

asyncio.run(verify())
```

### Scale: Add a Database Table

Add a new `CREATE TABLE` to the `SCHEMA` constant, add a new tool handler branch, add a new Tool definition to `list_tools()`. SQLite handles schema addition gracefully.