---
name: windows-port-management
description: "Use when managing TCP ports on Windows: conflicts, cleanup."
category: windows
tags: [windows, networking, ports, troubleshooting, process-management]
---

# Windows Port Management

Windows has unique port management quirks compared to Linux. Port conflicts from orphan processes, TIME_WAIT states, and git-bash signal handling differences are common pitfalls.

## Checking Port Usage

```bash
# List all listening ports with PIDs
netstat -ano | grep LISTEN

# Find what's on a specific port
netstat -ano | grep ":8080 " | grep LISTEN

# Show process name for a PID
tasklist //FI "PID eq 12345"

# Alternative with findstr (native cmd)
netstat -ano | findstr ":8080"
```

## Killing Processes Holding Ports

### With taskkill (most reliable on Windows)

```bash
# Force kill by PID
taskkill /F /PID 12345

# Find PID and kill in one flow
PID=$(netstat -ano | grep ":8080 " | grep LISTEN | awk '{print $NF}')
if [ -n "$PID" ] && [ "$PID" != "0" ]; then
    taskkill /F /PID "$PID"
fi
```

### Why `kill -9` often fails in git-bash

git-bash's `kill` command maps to Windows signal handling poorly. `os.kill(pid, 9)` on Windows Python also fails because:

- Windows doesn't have Unix signals
- git-bash runs in a console host that may not own the target process tree
- Orphan uvicorn/Docker subprocesses often resist `kill`

**Always use `taskkill /F /PID` on Windows for reliable process termination.**

## Python Port Detection

```python
import socket

def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    """Check if a TCP port is already bound."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0
```

## Python Port Cleanup on Windows

```python
import subprocess, os

def free_port(port: int):
    """Kill any orphan process holding a port."""
    if not is_port_in_use(port):
        return
    result = subprocess.run(
        ["netstat", "-ano"], capture_output=True, text=True, timeout=5
    )
    for line in result.stdout.splitlines():
        if f":{port} " in line and "LISTEN" in line:
            parts = line.strip().split()
            pid = parts[-1] if parts else ""
            if pid and pid != "0":
                subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True)
```

## Choosing Safe Ports

Avoid ranges commonly used on Windows dev machines:

| Range | Often Used By |
|-------|---------------|
| 3000-3999 | React/Vue dev servers |
| 5000-5999 | Flask, AirPlay receiver |
| 5432 | PostgreSQL |
| 6379 | Redis |
| 8000-8100 | Django, FastAPI, dev proxies |
| 8443 | Alternative HTTPS, webhooks |
| 27017 | MongoDB |
| 8080 | Jenkins, dev HTTP proxies |
| 9090 | Prometheus, dev consoles |

**Safe ranges (typically unused):** 9000-9999, 14000-19999, 40000-45000

## Orphan Process Prevention

When spawning long-lived Python/uvicorn servers from scripts, always detach from the parent:

```python
import subprocess

# On Windows, DETACHED_PROCESS prevents the child from dying with the parent
proc = subprocess.Popen(
    [sys.executable, "server.py"],
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
)
```

Without this, killing the parent shell/terminal leaves orphan uvicorn workers holding ports.

## Pitfalls

- **`os.kill(pid, 0)` on Windows** — process-existence check works in Windows Python but can succeed for dead processes whose PID hasn't been recycled.
- **TIME_WAIT** — after killing, a port can remain in TIME_WAIT for 30-120 seconds. Wait before restarting.
- **git-bash `ps aux`** — doesn't reliably show Windows-native processes. Use `netstat -ano` + `tasklist`.
- **Uvicorn orphans** — starting uvicorn inside an asyncio task spawns worker processes. If the parent exits, these survive as orphans holding ports. Always kill by port, not by parent PID.
