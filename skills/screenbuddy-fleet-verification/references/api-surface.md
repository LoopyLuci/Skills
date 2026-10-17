# ScreenBuddy + ABP API surface

## ScreenBuddy IPC protocol

Length-prefixed JSON over TCP on `127.0.0.1:34567`.
Frame: `[4-byte big-endian length][JSON payload]`.

### Commands

| cmd | payload key | response |
|-----|-------------|----------|
| `ping` | — | `{"status": "pong"}` |
| `get_status` | — | `{"status": "success", "data": {"fps", "uptime_secs", "creature_count", "memory_chunks", "model_count", "tool_count", "frames"}}` |
| `list_creatures` | — | `{"status": "creature_list", "creatures": [id, ...]}` — the IPC's own store, NOT the app's runtime list |
| `get_creature` | `id` | `{"status": "success", "data": {...}}` |
| `set_creature` | `id`, `data` | `{"status": "ack"}` |
| `get_agent_info` | — | `{"status": "success", "data": {"active_agent", "active_settings"}}` |
| `send_chat` | `message` | `{"status": "success", "data": {"queued": true}}` |
| `memory_search` | `query`, `limit` | `{"status": "success", "data": {"queued": true}}` |
| `get_setting` | `key?` | `{"status": "success", "data": ...}` |
| `set_setting` | `key`, `value` | `{"status": "ack"}` |
| `list_agents` | — | `{"status": "agent_list", "agents": [...]}` |
| `activate_agent` | `id` | `{"status": "ack"}` |
| `set_animation` | `id?`, `state` | `{"status": "ack"}` |
| `set_auto_cycle` | `enabled` | `{"status": "ack"}` |

## ABP dashboard HTTP API

Base: `http://127.0.0.1:8787`
Auth: `X-Dashboard-Token: <token>` header (from `.env`)

### Core endpoints

| method | path | purpose |
|--------|------|---------|
| GET | `/api/agent/overview` | List bots/instances |
| GET | `/api/agent/tools` | All tools (includes extension tools) |
| GET | `/api/agent/config` | Agent configuration values |
| GET | `/api/agent/permissions` | Integration scopes and presets |
| POST | `/api/agent/ask` | Ask an agent — expects `{source_instance, target_instance, prompt}` |
| GET | `/api/approvals` | Memory approval queue |
| GET | `/api/swarms` | Active swarms (returns a list, not a dict) |

### ScreenBuddy extension routes

| method | path | purpose |
|--------|------|---------|
| GET | `/api/screenbuddy/status` | Creature status snapshot (fps, uptime, creatures, models, tools) |
| GET | `/api/screenbuddy/finetune/status` | Fine-tune datasets and backend state |
| POST | `/api/screenbuddy/outcome` | Report tool outcome — expects `{ref: "provider/model", success, latency_ms}` |
| POST | `/api/screenbuddy/recommend` | Get routing recommendation — expects `{prompt, task_class}` |
| POST | `/api/screenbuddy/sandbox_exec` | Run a dangerous tool in a process cell — expects `{tool, args}` |

### Extension loading

ABP loads extensions from `<ABP_PRIVATE_DIR>/extensions/<name>/`.
The ScreenBuddy extension lives at:
`C:/Projects/ScreenBuddy/integrations/abp/extensions/screenbuddy/ext_screenbuddy/`

The extension package must have a `register(api)` function that uses:
- `add_routes` — HTTP routes
- `add_panel` — Dashboard panels
- `add_mcp_tool` — MCP tools
- `add_memory_source` — Memory federation
- `add_backend` / `add_backend_class` — Backend kinds
- `add_integration_scope` / `add_integration_preset` — Scoped trust
