---
name: botserver-setup
description: "Use for BotServer setup, build, and updates on Windows."
version: 1.0.0
author: Jessi
platforms: [windows]
metadata:
  hermes:
    tags: [botserver, telegram, tauri, windows, setup]
---

# BotServer Setup and Management

Setting up and maintaining the LoopyLuci/BotServer app on Windows.

## Architecture

- **BotServer**: FastAPI dashboard + Python Telegram bot. Runs as `bot.main` or via Tauri GUI (`bot-server.exe`).
- **Token ownership**: Only ONE process may poll a Telegram bot token at a time. If both BotServer and Hermes gateways use the same token, you get 409 Conflict flapping.
- **Environments**: BotServer has its own venv at `BotServer/.venv`. Its Tauri release build bundles a separate copy in `target/release/.venv`.

## Key Paths (this machine)

- Checkout: `C:\Projects\BotServer`
- Venv Python: `C:\Projects\BotServer\.venv\Scripts\python.exe`
- Dashboard: http://127.0.0.1:8787
- Tauri source: `desktop-app\src-tauri`
- Release exe: `desktop-app\src-tauri\target\release\bot-server.exe`
- Installers: `desktop-app\src-tauri\target\release\bundle\{msi,nsis}\`
- Launcher vbs: `scripts\start_at_logon.vbs` (copied to Startup folder)

## Setup Steps

1. Clone: `git clone https://github.com/LoopyLuci/BotServer.git C:\Projects\BotServer`
2. `cd C:\Projects\BotServer`
3. `python -m venv .venv`
4. `.venv\Scripts\pip install -r requirements.txt`
5. Configure `.env`: manually set `DASHBOARD_TOKEN`, `TELEGRAM_BOT_TOKEN`, `ALLOWED_TELEGRAM_USER_IDS`.
6. First run: `.venv\Scripts\python -m bot.main`
7. `scripts\setup.py --check` should report "Ready to run."

## Token Handover (from Hermes gateway)

If moving an existing Telegram token from Hermes to BotServer:

1. Stop Hermes gateway: `hermes gateway stop`
2. In `C:\Users\Server\AppData\Local\hermes\.env`, comment out `TELEGRAM_BOT_TOKEN=` with `#`.
3. Restart Hermes — it reports "No messaging platforms enabled."
4. In BotServer `.env`, set the same `TELEGRAM_BOT_TOKEN=` and `ALLOWED_TELEGRAM_USER_IDS=`.
5. Start BotServer — only one poller should exist (verify with getUpdates probe: expect HTTP 409).

## IPv4 Pin (critical on this network)

IPv6 to `api.telegram.org` breaks on LONG-HELD connections here, causing bot flapping. Fix:

`.venv\Scripts\python scripts\install_ipv4_pin.py`
`.venv\Scripts\python scripts\install_ipv4_pin.py --check`  # verify

Places a `sitecustomize.py` in site-packages that filters getaddrinfo to IPv4 for `api.telegram.org` only. Must be reinstalled after any venv rebuild.

## Building the Desktop App

```powershell
$env:PATH += ";C:\Users\Server\.cargo/bin"
cd desktop-app\src-tauri
cargo tauri build
```

**Known issue**: The bundler (MSI/NSIS) hangs silently on this Windows host. Workaround: stop all Python processes first (they lock venv `.pyd` files), then build. If it still hangs, `cargo build --release` succeeds and produces `bot-server.exe` — use that directly.

## Release Build Configuration

The Tauri release build resolves `.env` and `python` from its `resource_dir` (`target/release`), NOT the checkout. Two manual fixes needed after each `cargo tauri build`:

1. **Config**: In `target/release/config/backends.yaml`, set `env_file: C:\Projects\BotServer\.env`
2. **IPv4 pin**: `.venv\Scripts\python scripts\install_ipv4_pin.py --target "C:\Projects\BotServer\desktop-app\src-tauri\target\release\.venv\Lib\site-packages"`

## Auto-Start

- Startup folder (current): `C:\Users\Server\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\BotServer.vbs`
- Task Scheduler (sturdier, needs admin): `Register-ScheduledTask` with `-AtLogOn`, `-RestartCount 5`, `-RestartInterval (New-TimeSpan -Minutes 1)`

## Updating

`git pull` → rebuild → restart. Backend code changes require a restart; frontend changes require a rebuild.

## Debugging

- **Bot flapping**: Check IPv4 pin is active. Check for duplicate pollers (only one getUpdates consumer allowed). Check Hermes `.env` doesn't have the same token active.
- **GUI starts but no backend**: Release build missing `.env` or `env_file` not set.
- **Dashboard auth failures**: Verify `X-Dashboard-Token` header matches `.env`'s `DASHBOARD_TOKEN`.
- **Build file-lock errors**: Stop all Python processes first.
