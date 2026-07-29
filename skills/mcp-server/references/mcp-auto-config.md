# MCP Server Auto-Load Configuration (Hermes Agent)

How to configure an MCP server to auto-start and register its tools every time Hermes Agent loads.

## Stdio Transport (command-based)

Add to `~/.hermes/config.yaml` under the top-level `mcp_servers` key:

```yaml
mcp_servers:
  my-service:
    command: "python"
    args: ["C:/path/to/mcp_server.py"]
    timeout: 120
```

Use `hermes config set`:

```bash
hermes config set mcp_servers.my-service.command python
hermes config set mcp_servers.my-service.args '["C:/path/to/mcp_server.py"]'
```

Then fix the YAML list format (config set stores as string):

```bash
sed -i "s/    args: '\\[\"C:.*\"\\]'/    args:\n      - C:\/path\/to\/mcp_server.py/" ~/.hermes/config.yaml
```

Or manually edit to ensure proper YAML list format:

```yaml
mcp_servers:
  my-service:
    command: python
    args:
      - C:/path/to/mcp_server.py
    timeout: 120
```

## HTTP Transport (url-based)

```yaml
mcp_servers:
  my-service:
    url: "http://127.0.0.1:8090/sse"
    timeout: 180
    connect_timeout: 60
```

## What Happens on Startup

1. Hermes reads `mcp_servers` from config
2. For each server, spawns a connection in a background event loop
3. Calls `tools/list` to discover available tools
4. Registers tools as `mcp_{server_name}_{tool_name}`
5. Tools auto-inject into all platform toolsets (CLI, Discord, Telegram, etc.)
6. If connection drops, auto-reconnect with exponential backoff (up to 5 retries, max 60s)

## Pitfalls

- **`mcp_servers` is TOP-LEVEL** — NOT under `mcp.servers` (wrong nesting = no discovery)
- **Hermes blocks direct edits** to config.yaml — use `hermes config set`, then fix list format manually
- **Restart required** — adding/removing servers needs agent restart (no hot-reload)
- **`args` must be a YAML list** — `hermes config set` stores it as a string; the MCP client parses `args` as YAML, so string format fails silently
- **Test with `pip show mcp`** — the mcp Python package must be installed or MCP discovery is silently skipped
