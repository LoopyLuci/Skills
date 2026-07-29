---
name: hermes-telegram-bot-system
description: "Use when managing the Hermes Telegram Bot control system."
tags: [hermes, telegram, mcp, bot, service-management, dashboard, telemetry]
---

# Hermes Telegram Bot Control System

A next-generation Telegram bot control system purpose-built for AI agent use. Located at `D:\Projects\Bots\hermes-telegram-bot`.

## Architecture

```
Telegram Bot (ptb) ─┐
MCP Server (FastMCP)─┤── Core Engine ──┬── Telemetry Collector
Web Dashboard (FastAPI)─┘               ├── Service Manager
CLI / Watchdog                          ├── State Store (SQLite)
                                        └── Config Manager (YAML)
```

## Components

| File | Role |
|------|------|
| `main.py` | Entry point — orchestrates all components |
| `bot.py` | Enhanced Telegram bot with inline keyboard UI |
| `mcp_server.py` | MCP control server exposing 50+ tools |
| `dashboard.py` | Real-time web dashboard with live charts |
| `telemetry.py` | System/bot metrics collection (CPU, mem, latency, rates) |
| `service_manager.py` | Process lifecycle orchestration with auto-restart |
| `state.py` | SQLite-backed persistent state (users, services, messages, alerts) |
| `config.py` | YAML configuration with dotenv auto-loading |
| `models.py` | Shared data models (TelemetrySnapshot, Service, BotUser, AlertRule) |
| `watchdog.py` | Cron-friendly keepalive script (no_agent mode) |

## Running

```bash
# Full system (bot + dashboard + MCP)
cd D:\Projects\Bots\hermes-telegram-bot
python main.py

# Skip Telegram bot (dashboard + MCP only — for headless)
python main.py --no-bot

# Skip dashboard
python main.py --no-dashboard

# Skip MCP server
python main.py --no-mcp
```

Persistent startup via watchdog + Hermes cron:
- Watchdog script: `~/.hermes/scripts/hermes-telegram-bot-watchdog.py`
- Cron job: "Telegram Bot Watchdog" — runs every 5 minutes, no_agent mode
- Uses `subprocess.DETACHED_PROCESS` on Windows to survive terminal closure

## Ports

| Service | Port |
|---------|------|
| Dashboard | 9876 |
| MCP Server | 9877 |

## MCP Tool Surface (50+ tools)

**Bot Control:** `bot_status`, `bot_start`, `bot_stop`, `bot_restart`, `bot_config_get/set`, `bot_switch_mode`

**Service Management:** `service_list`, `service_get`, `service_register/unregister`, `service_start/stop/restart/kill`, `service_set_autorestart`, `service_logs`, `service_bulk_action`

**Telemetry:** `telemetry_snapshot`, `telemetry_history`, `telemetry_history_db`, `telemetry_latency_stats`, `telemetry_message_rate`, `telemetry_alert_create/list/delete/toggle`

**User Management:** `user_list`, `user_get`, `user_add/remove`, `user_set_role`, `user_toggle_active`, `pairing_list/approve/revoke`

**Analytics:** `message_stats`, `session_stats`, `daily_report`

**System:** `health_check`, `system_info`, `log_tail`, `gateway_log_tail`, `dashboard_status/start/stop`, `hermes_gateway_status/start/stop`

## Hermes MCP Integration

Configured in `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  hermes-telegram-bot:
    url: http://127.0.0.1:9877/mcp
    timeout: 180
    connect_timeout: 60
```

Tools are prefixed `mcp_hermes_telegram_bot_bot_status` etc.

## Telegram Bot UI (Inline Keyboards)

- **Main Menu** — status, telemetry, services, analytics, quick actions
- **Service control** — start/stop/restart/toggle auto-restart per service
- **Pagination** — services list paginated 5 per page
- **Confirmation dialogs** — destructive actions require confirm
- **Pairing flow** — unknown users get a pairing code for admin approval
