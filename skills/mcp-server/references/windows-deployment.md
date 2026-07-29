# Windows MCP Server Deployment

Orphan process management, port contention, and background service patterns for MCP servers on Windows.

## Windows Signal Handler Quirk

`asyncio.get_event_loop().add_signal_handler()` raises `NotImplementedError` on Windows. Always guard:

```python
try:
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(shutdown()))
except (NotImplementedError, ValueError):
    pass  # Windows
```

## Port Contention

Long-running MCP servers leave orphan uvicorn worker processes that hold TCP ports. `os.kill(pid, 9)` from git-bash's MSYS Python often fails (different process namespace), but `os.kill(pid, 0)` (process-existence check) DOES work from any Python. Use `taskkill` for actually killing:

```bash
# Find owner PID
netstat -ano | grep ":9876 " | grep LISTEN | awk '{print $NF}'
# Kill
taskkill /F /PID 12345
```

Python watchdog script (must run under Windows Python, not git-bash's MSYS):
```python
import socket, subprocess, os, time

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def free_ports(ports: list[int]):
    for port in ports:
        if is_port_in_use(port):
            result = subprocess.run(
                ["netstat", "-ano"], capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.splitlines():
                if f":{port} " in line and "LISTEN" in line:
                    pid = line.strip().split()[-1]
                    if pid and pid != "0":
                        subprocess.run(["taskkill", "/F", "/PID", pid],
                                       capture_output=True)
                        time.sleep(1)
```

## Background Process Pattern (no_agent=True Watchdog)

For keeping MCP server + dashboard alive together, use a Hermes cron job with a watchdog script:

```python
PORTS = [9876, 9877]  # dashboard, MCP server — use high, unusual ports
                      # (avoid 8080, 8000, 3000 common dev ports)

def is_running() -> bool:
    pid_alive = check_pid_file()  # os.kill(pid, 0)
    ports_ready = all(is_port_in_use(p) for p in PORTS)
    return pid_alive and ports_ready

def main():
    if is_running():
        return  # silent exit — no delivery
    free_ports(PORTS)
    start_process()
    print("✅ Services restarted")

if __name__ == "__main__":
    main()
```

Hermes cron registration:
```bash
cronjob action=create name="MCP Watchdog" schedule="every 5m" \
        script="watchdog.py" no_agent=true deliver=local
```

## Subprocess.DETACHED_PROCESS

On Windows, to start a background process that survives the parent's exit:

```python
proc = subprocess.Popen(
    [sys.executable, "server.py"],
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
)
```

This prevents the child from being killed when the parent terminal closes.

## MCP Config Cleanup

If `hermes config set` creates config entries under a wrong key (e.g., `mcp.servers` instead of `mcp_servers`), the stale section must be removed manually from `~/.hermes/config.yaml` — `hermes config unset` only removes leaf keys, not parent sections. Use a Python one-liner:

```python
import yaml
data = yaml.safe_load(open("config.yaml"))
data.pop("mcp", None)  # remove stale key
yaml.dump(data, open("config.yaml", "w"), default_flow_style=False)
```
