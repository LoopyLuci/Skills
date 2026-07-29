---
name: service-orchestration
description: "Auto-start, health-check, restart 2+ services from one CLI."
category: software-development
tags: [service-management, process-orchestration, health-checks, auto-restart, systemd, windows-scheduler, devops]
---

# Service Orchestration

Manage multiple background services as a unified system with auto-start,
health checking, crash recovery, and graceful shutdown — all from a
single CLI command.

## Trigger

Use when:
- A project has 2+ services that need to be started together (web server, API, MCP, database)
- Users need a single `start` / `stop` / `status` command for the whole stack
- Services need automatic crash recovery with exponential backoff
- You need cross-platform auto-start (systemd on Linux, Task Scheduler on Windows)
- Desktop notifications on service failure are desired

## Architecture

Two-layer approach:

```
┌─────────────────────────────────────────────────┐
│             Python CLI (user-facing)             │
│  `sov start` / `sov stop` / `sov status`        │
│  - Service definitions                          │
│  - Process spawning + tracking                  │
│  - Health check loop (every N seconds)          │
│  - Desktop notifications on crash/restart       │
│  - Colorful status table                        │
└───────────────────┬─────────────────────────────┘
                    │ delegates to
┌───────────────────▼─────────────────────────────┐
│           Rust Daemon (optional upgrade)         │
│  - HTTP control API (port 9099)                  │
│  - `/health`, `/status`, `/restart/{name}`       │
│  - Persistent process tracking via PID file      │
│  - Cross-platform signal handling (SIGTERM)      │
└─────────────────────────────────────────────────┘
```

## Project Structure

```
project-root/
├── scripts/
│   ├── sov                   # Python CLI (primary)
│   └── sov.bat               # Windows batch wrapper
├── sovereign-service/        # Rust daemon (optional upgrade)
│   ├── Cargo.toml
│   └── src/
│       ├── main.rs           # HTTP API + health loop
│       ├── config.rs         # Service definitions
│       ├── manager.rs        # Process lifecycle + restart logic
│       └── monitor.rs        # Desktop notifications
├── .sov-config.yaml          # User configuration
└── scripts/
    ├── auto-start.service    # Linux systemd unit
    └── auto-start.xml        # Windows Task Scheduler XML
```

## Service Definitions

Each service has:

```python
{
    "web-frontend": {
        "command": "npx",
        "args": ["vite", "--host", "0.0.0.0"],
        "cwd": "project/web",
        "port": 3006,
        "health_url": "http://localhost:3006/",
        "startup_order": 1,     # Lower = starts first
        "max_restarts": 10,     # Before permanent failure
    }
}
```

### Startup ordering

Services with lower `startup_order` start first and must pass health
check before the next begins:

```python
processes = sorted(procs, key=lambda x: x.config["startup_order"])
for name, proc in processes:
    proc.start()
    _wait_for_healthy(proc, timeout=30)
```

## Health Check + Auto-Restart

### Exponential backoff

```python
class ManagedProcess:
    def check_health(self):
        try:
            resp = urllib.request.urlopen(self.health_url, timeout=2)
            return resp.status == 200
        except Exception:
            return False

    def restart(self):
        self.backoff = min(self.backoff * 2, 30)
        self.stop()
        sleep(self.backoff)
        self.start()
```

### Auto-restart loop

```python
while True:
    for name, proc in procs.items():
        if not proc.is_alive() and proc.crashes < MAX_RESTARTS:
            notify(f"{name} crashed. Restarting...")
            proc.crashes += 1
            proc.start()
    time.sleep(5)
```

## Desktop Notifications

| Platform | API |
|---|---|
| Linux | `notify-send` or `notify-rust` |
| macOS | `osascript -e 'display notification "..."'` |
| Windows | PowerShell Windows Toast API |

## Graceful Shutdown

```python
signal.signal(signal.SIGINT, lambda: stop_all())

def stop_all():
    for proc in reversed(procs):
        proc.terminate()
        try: proc.wait(timeout=5)
        except TimeoutExpired: proc.kill()
```

## Cross-Platform Auto-Start

### Linux systemd

```ini
[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/bin/env python3 scripts/sov start
ExecStop=/usr/bin/env python3 scripts/sov stop
Restart=on-failure
RestartSec=10
[Install]
WantedBy=default.target
```

Install: `systemctl --user enable auto-start.service`

### Windows Task Scheduler

Export XML with LogonTrigger (10s delay), run `sov.bat start`,
RestartOnFailure (1m interval, 3 tries), HighestAvailable.

Import: `schtasks /create /xml auto-start.xml /tn "ServiceOrch"`

## Rust Daemon (Optional Upgrade)

```rust
struct ServiceManager { services: Vec<ManagedService> }
impl ServiceManager {
    async fn start_all(&mut self)  -> Result<()>;
    async fn stop_all(&mut self)   -> Result<()>;
    async fn check_all(&mut self);
}
```

## Verification

1. `sov start` boots all services, waits for health, shows dashboard
2. `sov status` shows each service's status, port, uptime
3. `sov stop` terminates all services gracefully (reverse order)
4. Killing a child triggers auto-restart + notification
5. Ctrl+C invokes graceful shutdown via SIGINT handler
6. Cross-platform auto-start configs parse correctly
