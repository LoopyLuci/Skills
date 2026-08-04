# Python MCP Server for Build Environments

## Complete Implementation Pattern

Minimal JSON-RPC 2.0 server over stdin/stdout. No external dependencies beyond Python 3.10+.

### Server skeleton

```python
#!/usr/bin/env python3
"""MCP server for C/C++ build environments."""
import json, sys, subprocess, re
from pathlib import Path

WORKSPACE = Path("/workspace")

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

def run_cmd(cmd, cwd=None, timeout=300):
    """Run a shell command and return structured output."""
    try:
        r = subprocess.run(cmd, cwd=cwd or str(WORKSPACE),
                           capture_output=True, text=True, timeout=timeout)
        return {"exit_code": r.returncode, "stdout": r.stdout[-5000:], "stderr": r.stderr[-3000:]}
    except subprocess.TimeoutExpired:
        return {"exit_code": -1, "stdout": "", "stderr": f"Timeout after {timeout}s"}

def handle_request(request):
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
    return {"jsonrpc": "2.0", "id": request.get("id"),
            "error": {"code": -32601, "message": f"Method not found: {method}"}}

# Stdio transport
for line in sys.stdin:
    request = json.loads(line.strip())
    response = handle_request(request)
    if response:
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
```

### Tool handler pattern

```python
def tool_build(args):
    build_type = args.get("build_type", "Release")
    clean = args.get("clean", False)
    build_dir = f"build_{args.get('dma_mode', 'stub')}"

    if clean and (WORKSPACE / build_dir).exists():
        import shutil; shutil.rmtree(WORKSPACE / build_dir)

    r = run_cmd(["cmake", "-B", build_dir, "-G", "Ninja",
                 f"-DCMAKE_BUILD_TYPE={build_type}",
                 f"-DCMAKE_C_COMPILER=clang-17",
                 f"-DCMAKE_CXX_COMPILER=clang++-17",
                 "-DCMAKE_C_COMPILER_LAUNCHER=ccache"], timeout=60)
    if r["exit_code"] != 0:
        return {"success": False, "phase": "configure", **r}

    r = run_cmd(["cmake", "--build", build_dir, "--parallel", str(nproc)], timeout=300)
    if r["exit_code"] != 0:
        return {"success": False, "phase": "build", **r}

    artifacts = [{"path": str(p.relative_to(WORKSPACE)), "size_bytes": p.stat().st_size}
                 for p in (WORKSPACE / build_dir).rglob("*")
                 if p.suffix in (".so", ".dll", ".exe")]
    return {"success": True, "build_dir": build_dir, "artifacts": artifacts}
```

## Pitfalls

- **Tool descriptions under 200 chars** — LLMs use them for routing
- **Parameter names camelCase** — LLM tokenizer compatibility
- **Idempotent handlers** — MCP clients retry on timeout
- **Truncate large outputs** — 5KB stdout, 3KB stderr to avoid context overflow
- **Use subprocess.run, not os.system** — Timeout support, structured output
- **Capture stdout and stderr separately** — Don't mix them
