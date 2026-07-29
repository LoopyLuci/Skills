# FastMCP Server Patterns

Durable patterns and API quirks for building MCP servers with the `mcp` Python package's `FastMCP`.

## API Surface (Confirmed by Live Testing)

### Construction

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "Server Name",                # required: name string
    instructions="...",          # NOT "description" — that keyword is rejected
    host="127.0.0.1",            # default: 127.0.0.1
    port=8090,                   # default: 8000
    # Other optional: log_level, debug, tools, dependencies, lifespan, ...
)
```

### Running

| Method | Transport | When to use |
|---|---|---|
| `await mcp.run_sse_async()` | HTTP + SSE | Server runs independently; agents connect over network |
| `await mcp.run_stdio_async()` | stdin/stdout | Hermes spawns the server as a subprocess |
| `await mcp.run_streamable_http_async()` | Streamable HTTP | Newer SDK, check version availability |

**Critical:** `host` and `port` go in the **constructor**, not in the `run_*` calls. `run_sse_async()` takes only an optional `mount_path` parameter.

### Tool Registration

```python
@mcp.tool()
async def my_tool(required_str: str, optional_int: int = 0) -> dict:
    """Tool description — this becomes the description LLMs read for routing."""
    return {"result": "success"}
```

- Type hints auto-generate JSON Schema
- Return is always wrapped as `text` content type
- Async is preferred but sync works
- No return type annotation is also fine (`-> None`)

### Resource Registration

```python
@mcp.resource("my-scheme://path/to/{parameter}")
def my_resource(parameter: str) -> str:
    """Resource description."""
    return f"Data for {parameter}"
```

- URI templates support path parameters
- Resources are read-only, synchronous data access

### Prompt Registration

```python
@mcp.prompt()
def daily_checklist() -> str:
    """Template description."""
    return """1. Run health_check()
2. Check service_list()
3. Review telemetry_snapshot()"""
```

- Prompts can accept arguments for templated workflows
- Return type is always `str`

## Tool Discovery

After creating the server, verify all tools are registered:

```python
import asyncio
tools = asyncio.run(mcp.list_tools())
assert len(tools) >= 35  # for a full control server
assert any(t.name == "bot_status" for t in tools)
```

## Hermes MCP Config

The Hermes `mcp_servers` config is a **top-level key** in `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  my-service:
    url: "http://127.0.0.1:8090/sse"
    timeout: 180
    connect_timeout: 60
```

- NOT under `mcp.servers` — that creates a wrong parallel section
- The `/sse` path suffix is required for FastMCP SSE servers
- Use `hermes config set mcp_servers.NAME.KEY VALUE` to set keys
- After config change, restart Hermes Agent for tools to appear
- Tool names in Hermes: `mcp_{server_name}_{tool_name}` (hyphens → underscores)

## Testing the Server

```bash
# Verify SSE endpoint is live
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8090/
# Should return 200

# Check REST API endpoints if the server also exposes them
curl -s http://127.0.0.1:8090/api/status | python -m json.tool
```

## Known Issues & Workarounds

- **`description` parameter rejected**: FastMCP uses `instructions`, not `description`. Pass it as a string kwarg, not in the name position.
- **`run_sse_async(host=..., port=...)` fails**: Move host/port to the constructor. `run_sse_async` only accepts `mount_path`.
- **Tool count verification**: 50 tools registered and verified via `list_tools()` in a production control server.
- **Stdio vs SSE**: If using SSE, the server runs independently — handle lifecycle yourself. If using stdio, Hermes manages the subprocess.
