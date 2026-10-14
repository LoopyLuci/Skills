#!/usr/bin/env python3
"""Verify a stdio MCP server speaks the handshake a client will perform.

Sends initialize + notifications/initialized + ping + tools/list as raw
JSON-RPC 2.0 frames over stdio — the exact frames an MCP client exchanges
with a StdioServerParameters-configured server — and prints the server
identity, negotiated protocol version, and the full advertised tool list.
Use before claiming a config-only MCP integration seam is verified.

Usage:
    python mcp_handshake_probe.py <server_script.py> [KEY=VALUE ...]

Extra KEY=VALUE args are merged into the child environment. Set
SCREENBUDDY_AUTOSTART=0 (or the target server's equivalent) to keep the
probe from launching the full app.
"""
import json
import os
import subprocess
import sys

if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(2)

server = sys.argv[1]
env = dict(os.environ)
for pair in sys.argv[2:]:
    key, _, value = pair.partition("=")
    env[key] = value

proc = subprocess.Popen(
    [sys.executable, server],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    env=env, text=True, bufsize=1,
)


def send(method, params=None, notify=False):
    msg = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        msg["params"] = params
    if not notify:
        msg["id"] = send.counter
        send.counter += 1
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()
    if notify:
        return None
    while True:
        line = proc.stdout.readline()
        if not line:
            raise RuntimeError("server closed stdout")
        try:
            resp = json.loads(line)
        except json.JSONDecodeError:
            continue  # servers may print non-protocol lines to stdout
        if resp.get("id") == msg["id"]:
            return resp


send.counter = 1

try:
    init = send("initialize", {
        "protocolVersion": "2025-03-26",
        "capabilities": {},
        "clientInfo": {"name": "integration-handshake-probe", "version": "1.0.0"},
    })
    send("notifications/initialized", notify=True)
    send("ping")
    tools = send("tools/list")["result"]["tools"]

    info = init["result"].get("serverInfo", {})
    print(f"initialize: OK  server={info.get('name')!r} v{info.get('version')} "
          f"protocol={init['result'].get('protocolVersion')}")
    print(f"ping: OK")
    print(f"tools/list: {len(tools)} tools")
    for t in tools:
        print(f"  - {t['name']}")
    print("HANDSHAKE_VERIFIED")
finally:
    proc.kill()

