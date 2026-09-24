# MCP Integration for Desktop Apps

This reference covers integrating Model Context Protocol (MCP) into PyQt5 desktop applications.

## Architecture

```
webbuilder/mcp/
├── __init__.py          # Re-exports
└── server.py            # WebBuilderMCPServer + WebBuilderMCPClient
```

## Server Implementation

```python
@dataclass
class MCPRequest:
    jsonrpc: str = "2.0"
    id: Optional[str]
    method: str
    params: dict

@dataclass
class MCPResponse:
    jsonrpc: str = "2.0"
    id: Optional[str]
    result: Any = None
    error: Optional[dict] = None

class WebBuilderMCPServer:
    def __init__(self, window=None):
        self.window = window
        self.tools: dict[str, MCPTool] = {}
        self._register_default_tools()

    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        if request.method == "initialize":
            return MCPResponse(result={
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "webbuilder-mcp", "version": "1.0.0"}
            })
        elif request.method == "tools/list":
            return MCPResponse(result={"tools": self.list_tools()})
        elif request.method == "tools/call":
            tool_name = request.params.get("name")
            arguments = request.params.get("arguments", {})
            result = await self.tools[tool_name].handler(arguments)
            return MCPResponse(result={"content": [{"type": "text", "text": json.dumps(result)}]})
```

## Client Implementation

```python
class WebBuilderMCPClient:
    async def connect_server(self, name: str, command: str, args: list[str] = None) -> bool:
        process = await asyncio.create_subprocess_exec(
            command, *(args or []),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
        )
        self.servers[name] = process

    async def call_tool(self, server_name: str, tool_name: str, arguments: dict) -> dict:
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments}
        }
        process = self.servers[server_name]
        process.stdin.write((json.dumps(request) + "\n").encode())
        response = await process.stdout.readline()
        return json.loads(response.decode())
```

## PyQt5 Integration

```python
class MCPSettingsDialog(QDialog):
    # Tab 1: Server list (add/edit/remove/connect/disconnect)
    # Tab 2: Available tools from connected servers
    # Tab 3: About MCP

    def _add_server(self):
        dialog = MCPServerConfigDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            config = dialog.get_config()
            # Add to list, save to config file

    def _connect_server(self):
        # asyncio.run(self.client.connect_server(...))
        pass
```

## Pitfalls

1. **In-process MCP server** — MCP server runs IN the GUI process. A crashing tool handler crashes the app. Wrap ALL handlers in try/except.

2. **Handler context** — Tool handlers receive `self.window` to interact with the application. This means they can directly modify project state. Validate all inputs in handlers.

3. **Async in sync GUI** — MCP client uses asyncio but Qt is synchronous. Use `asyncio.run()` in QThread or `QTimer.singleShot` for async calls.

4. **Process pool isolation** — External MCP servers run as subprocesses. They CANNOT access module-level singletons from the main app. Pass all data via stdin/stdout.

5. **Tool registration order** — Register tools in `__init__` before `window` is set if the server is created before the main window. Use lazy initialization for window-dependent tools.

6. **JSON-RPC error codes** — Use -32601 for unknown method, -32603 for internal error. Don't use 0 or positive numbers for errors.

7. **Caching** — Tool list cache per server. Refresh on reconnect, not on every call.

## Testing MCP Server

```python
import asyncio
from webbuilder.mcp import get_mcp_server, MCPRequest

server = get_mcp_server()

# Test initialize
req = MCPRequest(id='1', method='initialize')
resp = asyncio.run(server.handle_request(req))
assert resp.result['protocolVersion'] == '2024-11-05'

# Test tools/list
req = MCPRequest(id='2', method='tools/list')
resp = asyncio.run(server.handle_request(req))
assert len(resp.result['tools']) > 0

# Test tools/call
req = MCPRequest(id='3', method='tools/call', params={'name': 'list_sections', 'arguments': {}})
resp = asyncio.run(server.handle_request(req))
assert resp.result is not None
```

## GUI Menu Integration

```python
# In WebBuilderWindow.setup_menu()
mcp_action = QAction("MCP Settings...", self)
mcp_action.triggered.connect(self._open_mcp_settings)
ai_menu.addAction(mcp_action)

# Handler
def _open_mcp_settings(self):
    from webbuilder.gui.mcp_dialog import MCPSettingsDialog
    dialog = MCPSettingsDialog(self)
    dialog.exec_()
```

## External Server Configuration

```python
# Default external MCP servers to suggest:
default_servers = [
    {"name": "filesystem", "command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem"]},
    {"name": "github", "command": "npx", "args": ["-y", "@modelcontextprotocol/server-github"]},
    {"name": "sqlite", "command": "npx", "args": ["-y", "@modelcontextprotocol/server-sqlite"]},
]
```