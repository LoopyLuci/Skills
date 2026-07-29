---
name: mcp-server-windows
description: "Use when building MCP servers for Windows environments."
category: software-development
tags: [mcp, server, windows, tool, agent]
---
# MCP Server Windows

Building and deploying MCP (Model Context Protocol) servers on Windows.

## What is MCP

MCP is a protocol for exposing tools and resources to AI agents. An MCP server runs as a subprocess of the agent and communicates via stdio or SSE.

## Basic MCP Server (Python)

```python
# mcp_server.py
import sys
import json

def main():
    """Simple stdio-based MCP server that exposes tools."""
    # Initialize
    init_msg = json.loads(sys.stdin.readline())
    assert init_msg["method"] == "initialize"

    # Send capabilities
    response = {
        "jsonrpc": "2.0",
        "id": init_msg["id"],
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {
                    "listTools": {
                        "tools": [
                            {
                                "name": "read_file",
                                "description": "Read a file from disk",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "path": {"type": "string"}
                                    },
                                    "required": ["path"]
                                }
                            }
                        ]
                    }
                }
            }
        }
    }
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()

    # Handle requests
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)

        if req["method"] == "tools/call" and req["params"]["name"] == "read_file":
            path = req["params"]["arguments"]["path"]
            try:
                with open(path, 'r') as f:
                    content = f.read()
                result = {"content": [{"type": "text", "text": content}]}
            except Exception as e:
                result = {"isError": True, "content": [{"type": "text", "text": str(e)}]}

            resp = {
                "jsonrpc": "2.0",
                "id": req["id"],
                "result": result
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
```

## Configuration (Hermes Config)

```yaml
# In config.yaml
mcp_servers:
  my-mcp-server:
    command: python
    args:
      - "path/to/mcp_server.py"
    env:
      PYTHONUNBUFFERED: "1"
    description: "Local file system tools"
```

## Test the MCP Server

```powershell
# Send init message
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | python mcp_server.py

# Or use the MCP Inspector
npx @modelcontextprotocol/inspector python mcp_server.py
```

## Windows-Specific Considerations

```powershell
# Path handling -- normalize for Windows
$path = $args.path -replace '/', '\'

# Long paths -- ensure app.manifest has longPathAware
# Or use \\?\ prefix for paths over 260 chars

# Process lifecycle -- MCP server is managed by the agent
# Ensure clean exit on stdin EOF
```

## Pitfalls

- **Stdio MCP** requires unbuffered output -- set `PYTHONUNBUFFERED=1` or `-u` flag
- **Process lifecycle** -- MCP server starts/stops with the agent; handle cleanly
- **Path normalization** -- MCP clients may send forward-slash paths even on Windows
- **Timeout** -- long operations should use progress notifications or background tasks
- **Security** -- MCP servers run as the agent user; restrict tool access appropriately
