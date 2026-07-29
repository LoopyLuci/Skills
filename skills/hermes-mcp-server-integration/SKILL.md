---
name: hermes-mcp-server-integration
description: "Use when configuring MCP servers in Hermes config.yaml."
tags: [hermes, mcp, configuration, tool-integration, streaming]
---

# Hermes MCP Server Integration

How to add, configure, and troubleshoot MCP servers for Hermes Agent. Covers both stdio and HTTP transports.

## Config Structure (config.yaml)

```yaml
mcp_servers:
  server-name:
    # For stdio servers (command-based):
    command: "npx"                    # executable
    args: ["-y", "mcp-server-pkg"]     # arguments
    env:                               # optional env vars
      API_KEY: "sk-..."
    timeout: 120                       # per-tool-call timeout
    connect_timeout: 60                # initial connection timeout

    # OR for HTTP servers (url-based):
    url: "http://127.0.0.1:PORT/mcp"   # server URL
    headers:                            # optional HTTP headers
      Authorization: "Bearer sk-..."
    timeout: 180
    connect_timeout: 60
```

A server must have either `command` (stdio) or `url` (HTTP), not both.

## Transport Types

### Stdio Transport

Hermes spawns the server as a subprocess and communicates over stdin/stdout:

```yaml
mcp_servers:
  time:
    command: "uvx"
    args: ["mcp-server-time"]
```

### HTTP / StreamableHTTP Transport

For remote or local HTTP-based MCP servers:

```yaml
mcp_servers:
  my-server:
    url: "http://127.0.0.1:9877/mcp"
    timeout: 180
```

## Tool Naming Convention

MCP tools are prefixed with `mcp_{server_name}_{tool_name}`:

| Server Name | Tool | Result |
|-------------|------|--------|
| `hermes-telegram-bot` | `bot_status` | `mcp_hermes_telegram_bot_bot_status` |
| `filesystem` | `read_file` | `mcp_filesystem_read_file` |
| `time` | `get_time` | `mcp_time_get_time` |

Hyphens and dots become underscores.

## StreamableHTTP vs SSE Transport (FastMCP)

FastMCP supports two HTTP-based transports. StreamableHTTP is simpler (single POST endpoint):

```python
# StreamableHTTP (recommended) — single endpoint at /mcp
await mcp.run_streamable_http_async()  # POST /mcp

# SSE — requires separate SSE + message endpoints
await mcp.run_sse_async()              # GET /sse + POST /messages/
```

The Hermes MCP client works with StreamableHTTP. SSE may require additional URL configuration.

## Troubleshooting

### "Task group is not initialized"
The MCP session manager hasn't been started. Call `run_streamable_http_async()` instead of trying to mount the ASGI app manually.

### "405 Method Not Allowed"
Wrong URL path. StreamableHTTP typically serves at `/mcp`. SSE serves at `/sse`.

### "Bad Request: Missing session ID"
The MCP server is running and reachable — this is the expected first response from StreamableHTTP. The client's next request with the session ID will succeed.

### "Client must accept both application/json and text/event-stream"
The HTTP Accept header is missing `text/event-stream`. The Hermes MCP client sends this automatically; curl testing needs `-H "Accept: application/json, text/event-stream"`.

### "Failed initial connection"
Check:
1. Server process is running
2. Port is correct and not blocked
3. URL path matches the server's transport type (`/mcp` for StreamableHTTP, `/sse` for SSE)
4. Server binds to `0.0.0.0` or `127.0.0.1` matching the URL

## Testing an MCP Server

```bash
# With curl (StreamableHTTP)
curl -s http://127.0.0.1:9877/mcp -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# Expected: {"jsonrpc":"2.0","id":"server-error","error":{"code":-32600,"message":"..."}}
# (The "Missing session ID" error is confirmation the server is alive)
```

## Adding via CLI

```bash
# For HTTP servers
hermes config set mcp_servers.server-name.url "http://host:port/path"

# For stdio servers
hermes config set mcp_servers.server-name.command "npx"
hermes config set mcp_servers.server-name.args "[\"-y\", \"package\"]"
```

Changes take effect on Hermes restart.

## Security

- Stdio servers receive a **filtered environment** (only PATH, HOME, USER, etc.)
- API keys must be explicitly passed via `env:`
- Credential patterns in error messages are auto-redacted
- Sampling (server-initiated LLM requests) is enabled by default; disable with `sampling: { enabled: false }`

## Connection Lifecycle

- Persistent per-server asyncio Task in a background thread
- Auto-reconnect with exponential backoff (up to 5 retries, max 60s)
- Failed servers are "parked" — reconnect only on explicit request
- Server stats available via `get_mcp_status()` or Hermes dashboard
