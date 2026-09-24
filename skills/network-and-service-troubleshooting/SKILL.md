---
name: network-and-service-troubleshooting
description: "Diagnose flapping services and deployment issues."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [debugging, troubleshooting, networking, bots, deployment, infrastructure, root-cause]
    related_skills: [systematic-debugging]
---

# Network and Service Troubleshooting

Diagnose flapping services, transport-level failures, and deployment issues — especially when a service "works, then stops working right after."

## When to Use

- A service/bot/API "works, then stops working right after" or flaps intermittently
- `httpx.ReadError`, `Timed out`, `Connection reset`, "polling restarted after network error"
- A build hangs silently or fails with "The process cannot access the file because it is being used by another process"
- Two processes conflict over a shared resource (bot token, port, file lock)
- A deployed app can't find its config or dependencies

## Core Principle

**Measure, don't assume — and match the probe to the real workload's shape.** Short probes pass where long-held connections fail, so a clean `curl` does not mean the network is healthy.

---

## Pattern 1: Network Route Flapping

### The insight

A broken network route (often IPv6) frequently passes **short** requests but fails on **long-held connections**. Quick `curl` and ping look clean while the actual service — which holds connections open (Telegram `getUpdates`, streaming, SSE, WebSocket) — flaps constantly. This creates a misleading "works in testing, breaks in production" picture.

### Diagnostic procedure

1. **Hold connections open** to the target host:port for as long as the real service does (Telegram ≈ 8-10s). Do a minimal read at the end. Run 8-12 rounds per route.
2. **Isolate routes separately:** `auto` (OS default), forced IPv4, forced IPv6.
3. **Identify the failing route:** it shows `TimeoutError` / `Connection reset`; the working route is clean.
4. **Scope the fix narrowly:** if only specific hosts fail, pin those hostnames only. Do not disable IPv6 globally unless *all* hosts are broken.
5. **Verify continuously:** a short "it works now" is insufficient — confirm the new route holds connections cleanly across many rounds and the reconnect rate drops to zero.

### Example: Telegram bot flapping (2026-08-26)

```
auto   : 6/8 ok — 2x TimeoutError   ← resolver returns AAAA first; v6 long-polls die
forced v4: 8/8 ok — zero failures    ← the good route
forced v6: 6/8 ok — 2x TimeoutError  ← confirms v6 is the broken route
```

### Fail-safe hostname-only IPv4 pin (venv, survives git pull)

Place a `sitecustomize.py` in the venv's `site-packages` (outside the git checkout) that filters `socket.getaddrinfo` for specific suffixes:

```python
_MARK = "_ipv4_pin_installed"
_PINNED = ("api.telegram.org", "telegram.org")

def _install():
    if getattr(socket, _MARK, False) or os.environ.get("NO_IPV4_PIN"):
        return
    _orig = socket.getaddrinfo
    def getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
        infos = _orig(host, port, family, type, proto, flags)
        if family == socket.AF_INET6:
            return infos
        name = (host.decode() if isinstance(host, bytes) else str(host or "")).strip().rstrip(".").lower()
        if not name.endswith(_PINNED):
            return infos
        v4 = [i for i in infos if i[0] == socket.AF_INET]
        return v4 or infos
    socket.getaddrinfo = getaddrinfo
    setattr(socket, _MARK, True)
```

This is in the venv's site-packages so `git pull` never touches it. **Recreating the venv wipes it** — reinstall after a venv rebuild.

### System-wide alternative (admin, reversible)

```powershell
netsh interface ipv6 set prefixpolicy ::ffff:0:0/96 60 4
```

---

## Pattern 2: Single-Consumer Resource Conflicts

### Bot tokens (Telegram, Discord, etc.)

Telegram allows **only one `getUpdates` consumer per bot token**. Two pollers produce `HTTP 409 Conflict` and flapping. This looks like the bot is broken — but it actually **proves two processes are fighting over the token.**

**To hand a token from one process to the other:**
1. Stop/disable the first process's token (comment it out, don't delete it — back up the `.env`).
2. Start the second process.
3. Verify the first process reports "no token / no messaging platforms."
4. **Do not probe `getUpdates` while the other poller runs** — use a transport-level probe (TLS connect + hold + minimal HTTP) to the API host:port. The conflict is expected and harmless; the 409 proves ownership, not breakage.

### Port conflicts

A service that starts but its expected port stays silent often means a previous instance is still bound to it. Check with `netstat -ano | grep :PORT`, find the old PID, and terminate it before restarting.

---

## Pattern 3: Windows-Specific Quirks

### BOM-less `.ps1` with non-ASCII characters

Windows PowerShell 5.1 reads BOM-less `.ps1` files as the system ANSI code page. UTF-8 characters outside ASCII (em-dashes, curly quotes, non-Latin letters) get mis-decoded, causing confusing parse errors like `Missing argument in parameter list` or `The term '-X' is not recognized`.

**Fix:** prepend a UTF-8 BOM (`0xEF 0xBB 0xBF`). This is the *opposite* of the usual "no BOM for UTF-8" rule — PowerShell 5.1 specifically needs it for non-ASCII scripts.

```python
from pathlib import Path
p = Path("script.ps1")
raw = p.read_bytes()
if not raw.startswith(b"\xef\xbb\xbf"):
    p.write_bytes(b"\xef\xbb\xbf" + raw)
```

### Task Scheduler / schtasks needs elevation

Registering a Windows Scheduled Task requires admin on most accounts. The fallback that works without elevation is the **Startup folder**:

```
C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\
```

Trade-off: starts at logon (not boot) and won't auto-restart on crash.

---

## Pattern 4: Tauri / Bundled Desktop Apps

### Release build resolves from resource_dir, not the checkout

A Tauri release build resolves its bundled `.venv` and `config/backends.yaml` from the executable's `resource_dir`, not the git checkout. The app launches but **never binds its port** if it can't find `.env`.

**Fix:** set `config/backends.yaml`'s `env_file` key to the real `.env` path.

### Build fails if the bot holds venv files open

On Windows, `cargo tauri build` fails with `os error 32` (file in use) if a running process holds files in the bundled `.venv`. **Stop the bot first**, then build. The new exe gets fresh bundles.

---

## Diagnostic Scripts

See `scripts/_probe_transport.py` — a read-only transport probe that holds TLS connections open and compares routes without calling any API method, so it never conflicts with a live bot.
