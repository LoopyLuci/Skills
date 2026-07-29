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
    streamable_http_path="/mcp", # default: /mcp — Streamable HTTP endpoint
    sse_path="/sse",             # default: /sse — SSE endpoint
    # Other optional: log_level, debug, tools, dependencies, lifespan, ...
)
```

### Running

| Method | Transport | When to use |
|---|---|---|
| `await mcp.run_sse_async()` | HTTP + SSE | Server runs independently; agents connect over network |
| `await mcp.run_stdio_async()` | stdin/stdout | Hermes spawns the server as a subprocess |
| `await mcp.run_streamable_http_async()` | Streamable HTTP | Newer transport — single POST endpoint, no SSE needed |

**Critical:** `host` and `port` go in the **constructor**, not in the `run_*` calls. All three run methods take no host/port parameters.

### Streamable HTTP Transport

`run_streamable_http_async()` spawns its **own uvicorn server** internally. Key implications:

- **Cannot be embedded/mounted inside another ASGI app** — calling `streamable_http_app()` to get the raw ASGI app and mounting it via `FastAPI.mount()` or `Mount()` will fail because the Streamable HTTP session manager's task group is not initialized until `run_streamable_http_async()` is called. The error is: `RuntimeError: Task group is not initialized. Make sure to use run().`
- **Runs on its own port** — the host/port set in the constructor.
- **Requires Accept header** — clients must send `Accept: application/json, text/event-stream` or they get `-32600: Not Acceptable`.
- **JSON-RPC endpoint** — clients POST JSON-RPC 2.0 messages to `streamable_http_path` (default `/mcp`).
- **Session management** — the server manages sessions internally.

**Architecture:** If you need both a REST API/dashboard AND an MCP server, run them as two separate uvicorn instances on different ports, each in its own asyncio task:

```python
async def run_mcp():
    mcp = FastMCP("Control", host="127.0.0.1", port=8090)
    register_tools(mcp)
    await mcp.run_streamable_http_async()

async def run_dashboard():
    app = create_fastapi_app()
    config = uvicorn.Config(app, host="127.0.0.1", port=8080)
    server = uvicorn.Server(config)
    await server.serve()

asyncio.gather(run_mcp(), run_dashboard())
```

**WRONG — mounting fails:**
```python
asgi = mcp.streamable_http_app()      # task group NOT initialized
app = FastAPI()
app.mount("/mcp", asgi)                # RuntimeError on request ❌
```

### Tool Organization Pattern (50+ tools)

For large servers, organize by category with nested registration functions:

```python
def register_tools(mcp):
    @mcp.tool()
    async def bot_status() -> dict: ...

    def register_services(mcp):
        @mcp.tool()
        async def service_list() -> list[dict]: ...
    register_services(mcp)

    def register_telemetry(mcp):
        @mcp.tool()
        async def telemetry_snapshot() -> dict: ...
    register_telemetry(mcp)
```

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
    url: "http://127.0.0.1:8090/sse"    # SSE transport
    timeout: 180
    connect_timeout: 60
```

For Streamable HTTP transport:

```yaml
mcp_servers:
  my-service:
    url: "http://127.0.0.1:8090/mcp"    # Streamable HTTP
    timeout: 180
    connect_timeout: 60
```

- NOT under `mcp.servers` — that creates a wrong parallel section
- SSE transport: URL must end in `/sse` (the default `sse_path`)
- Streamable HTTP: URL matches `streamable_http_path` (default `/mcp`)
- Use `hermes config set mcp_servers.NAME.KEY VALUE` to set keys
- After config change, restart Hermes Agent for tools to appear
- Tool names in Hermes: `mcp_{server_name}_{tool_name}` (hyphens → underscores)
- **Cleanup stale entries** — if you previously created a server under an incorrect key (e.g., `mcp.servers`), remove the stale section from config.yaml manually

## Testing the Server

```bash
# Verify SSE endpoint is live
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8090/
# SSE servers: should return 200

# Verify Streamable HTTP endpoint
curl -s -w "\nHTTP %{http_code}" http://127.0.0.1:8090/mcp -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
# Should return HTTP 200 with JSON-RPC response listing all tools

# Check REST API endpoints if the server also exposes them
curl -s http://127.0.0.1:8080/api/status | python -m json.tool
```

## Known Issues & Workarounds

- **`description` parameter rejected**: FastMCP uses `instructions`, not `description`. Pass it as a string kwarg, not in the name position.
- **`run_sse_async(host=..., port=...)` fails**: Move host/port to the constructor. All `run_*` methods take no host/port parameters.
- **Streamable HTTP cannot be embedded**: `streamable_http_app()` returns an app whose session manager task group is only initialized during `run_streamable_http_async()`. Mounting it in another ASGI app causes `RuntimeError: Task group is not initialized`.
- **Streamable HTTP Accept header**: Clients must send `Accept: application/json, text/event-stream`. Hermes MCP client handles this automatically.
- **Windows signal handlers**: `loop.add_signal_handler()` raises `NotImplementedError` on Windows. Catch via `(NotImplementedError, ValueError)`.
- **Tool count verification**: 50 tools registered and verified via `list_tools()` in a production control server.
- **Stdio vs SSE vs Streamable HTTP**: Stdio — Hermes manages the subprocess. SSE — server runs independently, network-accessible. Streamable HTTP — same as SSE but single POST endpoint, no SSE stream.
- **Port migration to avoid conflicts**: Default ports (8080, 8000, 3000, 5000) are commonly used. Choose high, unusual ports (e.g., 9876, 9877) for long-lived MCP infrastructure. Update both Python defaults AND the persistent YAML config file — the YAML overrides Python defaults.
- **Python bytecode cache trap**: When changing default values in a config module, delete `__pycache__/` and any `.pyc` files. A stale `.pyc` from a prior `import` silently serves old values even after source edits.
