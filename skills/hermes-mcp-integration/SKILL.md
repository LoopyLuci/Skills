---
name: hermes-mcp-integration
description: "Use when exposing an app to Hermes over MCP."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [MCP, Hermes, Integration, Tooling, Stdio]
    related_skills: [hermes-agent, mcp-server-development]
---

# Exposing an app to Hermes over MCP

Registering an MCP server is easy; making it *usable* has three failure points
that all look like "Hermes ignores my server". Each section is symptom-first,
because that is how it presents.

> Register with the CLI, verify with the CLI, then prove a tool call changes
> something real. `hermes mcp list` showing `enabled` is not evidence any of
> that is true.

## When to Use

- Registering a local app, service, or script as an MCP server Hermes can drive.
- `hermes mcp add` reports a connection timeout or "failed to connect".
- The server connects, but its tools are missing from the session.
- Tool calls return truncated data, or the host app's stdout seems to break the
  protocol stream.

## Register with the CLI, never by editing config

`config.yaml` holds live gateway state; a stray indent corrupts it.

```bash
hermes mcp add <name> --command python --args "path/to/server.py"
hermes mcp list
hermes mcp test <name>      # connects + reports discovered tool count
```

`hermes mcp add` is **discovery-first**: it launches the server, enumerates the
tools, and prompts to enable them. A failure therefore blocks *registration*,
not just usage — see the timeout trap below.

**Clean the args afterwards.** `--connect-timeout N` and similar flags can be
appended to the persisted `args` list, which then reach your server's
`sys.argv`:

```bash
hermes config set mcp_servers.<name>.args '["path/to/server.py"]'
```

## Never block startup discovery

Discovery runs at startup with a bounded timeout. A server that waits for a
*dependency* to appear before registering its tools will time out and look like
a connection failure:

```python
# Wrong: up to 10s of polling before any tool exists
wait_for_app(attempts=20, delay=0.5)

# Right: probe once, briefly, then register regardless
if not wait_for_app(attempts=2, delay=0.2):
    print("backend not reachable; tools will error until it starts", file=sys.stderr)
```

Register tools unconditionally and let each *call* report the missing
dependency. The agent gets a clear error instead of a server that vanished.

## The mcp SDK renamed its server class

`mcp` 2.x renamed `FastMCP` to `MCPServer`, and `run()` now requires an explicit
transport. Support both rather than pinning:

```python
try:                                   # mcp >= 2.0
    from mcp.server.mcpserver import MCPServer as _Server
except ModuleNotFoundError:            # mcp 1.x
    from mcp.server.fastmcp import FastMCP as _Server

mcp = _Server("name", instructions="...")
...
try:
    mcp.run(transport="stdio")
except TypeError:                      # 1.x defaults to stdio
    mcp.run()
```

The `@mcp.tool()` decorator and tool signatures are unchanged across both.

## Tool results are content blocks, not values

A tool returning `dict`/`list` comes back as **text blocks**, and a bare list may
arrive as one block *per element*. Client-side parsers must join all text blocks
before decoding, with a Python-literal fallback:

```python
texts = [b["text"] for b in result.get("content", []) if b.get("type") == "text"]
raw = "".join(texts)                   # joining is required for lists
```

Decoding only `texts[0]` silently truncates list-returning tools.

## Keep stdout clean

If the app or a wrapper prints prompts/banners to stdout, it corrupts the stdio
JSON-RPC stream. Gate interactive output on stdin actually being a terminal —
stdout is the protocol channel, not a console.

## Verify end to end, not just discovery

`hermes mcp test` proves connect + discovery. It does **not** prove a tool works.
Drive the registered command yourself and assert an observable effect:

1. Perform the MCP `initialize` handshake over stdio yourself.
2. `tools/list`, then call a mutating tool.
3. Read state back through a second tool and assert it changed.
4. **Restore the original state** — you are driving a live app the user has open.

MCP tools reach an *already-running* session only after a new session or
`/reload-mcp`; successful registration does not retroactively add them.

## Pair with a two-suite test setup

Ship one suite at the transport/protocol level and one at the MCP level, both
requiring the real backend to be up. Neither is a unit test, and a CI job running
only unit tests will green-light a server that cannot connect.

## References

- `mcp-server-development` — building the server itself (schema design,
  transports). There are two skills by that name; the local one is the
  general-purpose guide.
- `hermes-agent` (bundled) — authoritative CLI/config reference; its
  `references/native-mcp.md` covers the full MCP surface.
