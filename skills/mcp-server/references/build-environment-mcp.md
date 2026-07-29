# Build Environment MCP Server Pattern

## Overview

MCP server that exposes build, test, lint, and analysis tools for a C/C++ project. Designed to run inside a Docker container so AI agents can fully control the build environment remotely.

## Transport

stdio (JSON-RPC over stdin/stdout) — standard for agent subprocess integration.

## Tool Set (8 tools)

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `build` | CMake configure + compile | `build_type`, `dma_mode`, `clean`, `parallel` |
| `test` | CTest runner | `filter` (regex), `verbose` |
| `lint` | Static analysis | `tool` (all/clang-tidy/clang-format/cppcheck), `fix` |
| `analyze` | Parse report.json | `report_path` |
| `file_list` | List source files | `pattern`, `directory` |
| `file_read` | Read with line numbers | `path`, `offset`, `limit` |
| `syntax_check` | Single-file compile check | `file` |
| `status` | Environment info | (none) |

## Implementation Pattern (Python)

```python
# Minimal JSON-RPC 2.0 server over stdin/stdout
# No external dependencies beyond Python 3.10+

TOOLS = [
    {
        "name": "build",
        "description": "Configure and compile the project.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "build_type": {"type": "string", "enum": ["Release", "Debug"], "default": "Release"},
                "clean": {"type": "boolean", "default": False},
            },
            "required": []
        }
    },
    # ... more tools
]

def handle_request(request: dict) -> dict:
    method = request.get("method", "")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": request.get("id"), "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "build-env", "version": "1.0.0"}
        }}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": request.get("id"), "result": {"tools": TOOLS}}
    if method == "tools/call":
        tool_name = request["params"]["name"]
        tool_args = request["params"].get("arguments", {})
        result = TOOL_DISPATCH[tool_name](tool_args)
        return {"jsonrpc": "2.0", "id": request.get("id"), "result": {
            "content": [{"type": "text", "text": json.dumps(result, indent=2, default=str)}]
        }}

# Read from stdin, write to stdout
for line in sys.stdin:
    request = json.loads(line.strip())
    response = handle_request(request)
    if response:
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
```

## Docker Integration

### Dockerfile pattern
```dockerfile
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y clang-17 cmake ninja-build python3 python3-pip
RUN python3 -m pip install mcp
COPY docker/mcp_server.py /opt/mcp/server.py
WORKDIR /workspace
ENTRYPOINT ["/opt/mcp/entrypoint.sh"]
```

### docker-compose.yml pattern
```yaml
services:
  mcp:
    build: { context: ., dockerfile: docker/Dockerfile }
    entrypoint: ["python3", "/opt/mcp/server.py"]
    command: ["--stdio"]
    stdin_open: true
    ports: ["8080:8080"]
  build:
    extends: mcp
    entrypoint: ["/opt/scripts/build.sh"]
  test:
    extends: mcp
    entrypoint: ["/opt/scripts/test.sh"]
```

## Pitfalls

- Tool descriptions under 200 chars for LLM routing
- Parameter names camelCase for tokenizer compatibility
- Idempotent handlers (MCP clients retry on timeout)
- `build` tool should generate `compile_commands.json` for `lint` tool
- Use `subprocess.run` with timeout, not `os.system`
- Capture both stdout and stderr separately
- Truncate large outputs (5KB+ for stdout, 3KB+ for stderr) to avoid context overflow

## Verification

1. `echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python3 mcp_server.py` returns tool list
2. Each tool returns structured JSON with `success` boolean
3. `build` tool produces artifacts in `build_*` directories
4. `test` tool returns pass/fail counts
5. `lint` tool returns per-linter results
