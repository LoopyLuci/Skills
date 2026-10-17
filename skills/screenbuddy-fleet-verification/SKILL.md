---
name: screenbuddy-fleet-verification
description: "Verify ScreenBuddy + ABP integration fleet end-to-end."
version: 1
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [verification, e2e, screenbuddy, abp, ipc, fleet]
    related_skills: [on-device-runtime-verification]
---

# ScreenBuddy fleet E2E verification

Verifies the ScreenBuddy desktop app and ABP integration fleet end-to-end:
the length-prefixed IPC protocol on :34567, the ABP dashboard on :8787,
and every shipped integration pattern (MCP tools, extension routes, sandbox,
fine-tune, recommend, outcome, swarm, persona, memory).

## When to use

- After cutting a ScreenBuddy or ABP release that touches the integration.
- Before reporting any integration pattern as working.
- When the user asks to "bring the fleet up" or "verify the integration."
- When an extension route returns 404 and you need to determine whether the
  extension is loaded, the route is wrong, or the auth token is missing.

## Prerequisites

- ScreenBuddy release binary at `target/release/screenbuddy.exe`
- ABP source checkout at `C:\Projects\AgenticBotPlatform`
- ABP's `.venv` Python 3.11 (hermes py3.14 venv lacks some deps)
- `DASHBOARD_TOKEN` in ABP's `.env` (48-char random string)
- `ABP_PRIVATE_DIR` pointing at `C:\Projects\ScreenBuddy\integrations\abp`

## Procedure

### 1. Start ScreenBuddy

```bash
target/release/screenbuddy.exe &
```

The IPC server listens on `127.0.0.1:34567`. Confirm with `grep -a "IPC.*listening"`
on the log. If the port is already held, kill the old PID first — a stale
process serves stale code.

### 2. Start ABP

ABP requires two environment variables that are NOT in `.env` by default:

```bash
cd C:/Projects/AgenticBotPlatform
TOKEN=$(grep DASHBOARD_TOKEN .env | cut -d= -f2)
env -u PYTHONPATH \
    DASHBOARD_TOKEN="$TOKEN" \
    ABP_PRIVATE_DIR="C:/Projects/ScreenBuddy/integrations/abp" \
    .venv/Scripts/python.exe -m uvicorn \
    "bot.dashboard.server:build_app" --factory \
    --host 127.0.0.1 --port 8787 &
```

Without `ABP_PRIVATE_DIR` the extension is not loaded and every
`/api/screenbuddy/*` route returns 404. Without `DASHBOARD_TOKEN` every
authenticated endpoint returns 503. Both are silent failures — the server
starts and serves, but the integration surface is absent.

Confirm readiness: `curl -s -H "X-Dashboard-Token: $TOKEN"
http://127.0.0.1:8787/api/agent/overview` should return a JSON object with a
`bots` array.

### 3. Run the verification script

```bash
python scripts/e2e_verify.py
```

The script speaks ScreenBuddy's length-prefixed IPC protocol (4-byte big-endian
frame length + JSON payload) and ABP's HTTP API with the dashboard token. It
exercises every integration pattern and reports PASS/FAIL per check.

### 4. Interpret results

- All green: the fleet is live and every pattern is reachable.
- Extension routes 404: `ABP_PRIVATE_DIR` is not set or the extension isn't
  in `<ABP_PRIVATE_DIR>/extensions/<name>/`.
- 503 on authenticated routes: `DASHBOARD_TOKEN` missing or wrong.
- IPC bind failure: stale ScreenBuddy process holding :34567.
- Sandbox returns `unknown tool`: the tool name is wrong — check the
  extension's registered tool names, not the function names.

## Always-on rules

- **Restart before diagnosing.** A stale process serves stale code. When a
  value appears not to propagate, confirm the running process is the one you
  just started before hunting the cause.
- **Assert on the wire format, not on storage.** A value that persisted is not
  a value that was honoured.
- **A shape check passes on an honest error message.** Asserting "non-empty"
  is satisfied by an error string. Assert the content is NOT a failure report.
- **Sandbox tool names differ from function names.** The extension registers
  tools under names like `run_shell`, not the Python function name. When a
  sandbox call returns "unknown tool", check the extension's registered tool
  names before concluding the sandbox is broken.
- **The ABP extension loader reads `<ABP_PRIVATE_DIR>/extensions/<name>/`.**
  The ScreenBuddy extension lives at
  `C:/Projects/ScreenBuddy/integrations/abp/extensions/screenbuddy/ext_screenbuddy/`.
  If `ABP_PRIVATE_DIR` is wrong or missing, the extension silently does not
  load — no error, just 404s on every extension route.

## Pitfalls

- **`os.environ.get` redacts to `***` in tool output.** When a script reads
  `DASHBOARD_TOKEN` from the environment, the tool result may show
  `***"DASHBOARD_TOKEN"]` instead of the real call, causing a SyntaxError
  in the linter. Read the token from `.env` with `open()` instead of
  `os.environ.get`.
- **`netstat -ano` shows the LISTENING PID, not the process you started.**
  If an old ABP instance is still running, the new one fails to bind and
  shuts down silently. Always check `netstat -ano | grep <port>` before
  concluding the server started.
- **`taskkill /F /PID <pid>` needs single-slash flags in git-bash.** MSYS path
  conversion mangles `//F` into an invalid argument. Use `/F /PID` not
  //PID`.
- **The ScreenBuddy IPC protocol is length-prefixed JSON, not HTTP.**
  `curl http://127.0.0.1:34567/...` returns nothing — the server speaks raw
  TCP frames. Use the Python `sb_ipc()` helper from the verification script.
- **`get_status` data is nested under `data`.** The IPC response is
  `{"status": "success", "data": {"fps": ...}}`, not a flat object.
  Assert on `reply["data"]["fps"]`, not `reply["fps"]`.
- **`list_creatures` returns the IPC's own creature store, not the app's
  runtime list.** The app loads 7 creatures at startup into a different data
  structure. The IPC's `creatures` map is only populated when someone sends
  `set_creature` or `export_creature`. An empty `list_creatures` is not a
  bug — it is the IPC's override store, not the app's live state.
- **ABP's `agent/ask` expects `{source_instance, target_instance, prompt}`,**
  not `{instance_id, message}`. The 400 error tells you the exact shape.
- **The fine-tune LoRA path is hardware-guarded.** `torch` + `CUDA` + `unsloth`
  must all be present. On a machine without them the endpoint honestly
  reports "torch is not installed" — that is correct behaviour, not a bug.

## References

- [references/api-surface.md](references/api-surface.md) — IPC commands, ABP
  endpoints, and extension routes for the ScreenBuddy + ABP integration.
- [scripts/e2e_verify.py](scripts/e2e_verify.py) — the full verification script.
