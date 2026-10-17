#!/usr/bin/env python3
"""E2E verification for the ScreenBuddy + ABP integration fleet.

Prerequisites:
  - ScreenBuddy running on 127.0.0.1:34567
  - ABP running on 127.0.0.1:8787 with ABP_PRIVATE_DIR set
  - DASHBOARD_TOKEN in ABP's .env

Usage: python e2e_verify.py
"""
import json, socket, struct, sys, urllib.request, urllib.error

SB_HOST, SB_PORT = "127.0.0.1", 34567
ABP_HOST, ABP_PORT = "127.0.0.1", 8787

# Read DASHBOARD_TOKEN from .env
TOKEN = ""
try:
    with open("C:/Projects/AgenticBotPlatform/.env") as f:
        for line in f:
            if line.startswith("DASHBOARD_TOKEN="):
                TOKEN = line.split("=", 1)[1].strip()
                break
except Exception:
    pass
if not TOKEN:
    print("FATAL: DASHBOARD_TOKEN not found in .env"); sys.exit(1)

PASS, FAIL = "PASS", "FAIL"
results = []

def sb_ipc(cmd, timeout=5.0):
    """Send one length-prefixed JSON frame to ScreenBuddy, return the reply."""
    payload = json.dumps(cmd).encode()
    frame = struct.pack(">I", len(payload)) + payload
    with socket.create_connection((SB_HOST, SB_PORT), timeout=timeout) as s:
        s.settimeout(timeout)
        s.sendall(frame)
        raw = b""
        while len(raw) < 4:
            c = s.recv(4 - len(raw))
            if not c: raise ConnectionError("closed during length prefix")
            raw += c
        (length,) = struct.unpack(">I", raw)
        body = b""
        while len(body) < length:
            c = s.recv(min(65536, length - len(body)))
            if not c: raise ConnectionError("closed during body")
            body += c
        return json.loads(body)

def abp_req(path, data=None, timeout=10.0):
    """HTTP request to ABP with the dashboard token."""
    url = f"http://{ABP_HOST}:{ABP_PORT}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json",
        "X-Dashboard-Token": TOKEN,
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            text = r.read().decode(errors="replace")
            try: return json.loads(text)
            except: return {"_nonjson": text[:200]}
    except urllib.error.HTTPError as e:
        eb = e.read().decode(errors="replace")[:300]
        try: return json.loads(eb)
        except: return {"_status": e.code, "_error": eb}

def check(name, ok, detail=""):
    s = PASS if ok else FAIL
    results.append((s, name, detail))
    print(f"  [{s}] {name}" + (f" — {detail}" if detail else ""))

# ── 1. ScreenBuddy IPC ─────────────────────────────────────────────────────
print("\n=== 1. ScreenBuddy IPC ===")
try:
    r = sb_ipc({"cmd": "ping"})
    check("IPC ping", r.get("status") == "pong", json.dumps(r)[:100])
except Exception as e:
    check("IPC ping", False, str(e)); sys.exit(1)

try:
    r = sb_ipc({"cmd": "get_status"})
    d = r.get("data", {})
    check("IPC get_status", any(k in d for k in ("fps", "uptime", "creature_count")), json.dumps(d)[:150])
except Exception as e:
    check("IPC get_status", False, str(e))

try:
    r = sb_ipc({"cmd": "get_agent_info"})
    check("IPC get_agent_info", r.get("status") == "success", json.dumps(r)[:150])
except Exception as e:
    check("IPC get_agent_info", False, str(e))

try:
    r = sb_ipc({"cmd": "memory_search", "query": "test", "limit": 3})
    check("SB memory_search", r.get("status") == "success", json.dumps(r)[:150])
except Exception as e:
    check("SB memory_search", False, str(e))

try:
    r = sb_ipc({"cmd": "send_chat", "message": "E2E test: reply with OK"})
    check("IPC send_chat", r.get("status") in ("success", "queued", "ok"), json.dumps(r)[:150])
except Exception as e:
    check("IPC send_chat", False, str(e))

# ── 2. ABP basics ──────────────────────────────────────────────────────────
print("\n=== 2. ABP basics ===")
r = abp_req("/api/agent/overview")
bots = r.get("bots", [])
check("ABP bots", len(bots) >= 2, f"{len(bots)} bots: {[b['name'] for b in bots]}")

r = abp_req("/api/agent/tools")
tools = r.get("tools", [])
check("ABP tools", len(tools) > 0, f"{len(tools)} tools")

# ── 3. Pattern A: MCP ──────────────────────────────────────────────────────
print("\n=== 3. Pattern A — MCP ===")
sb_tools = [t for t in tools if "screenbuddy" in str(t.get("name", ""))]
check("SB MCP tools", len(sb_tools) > 0, f"{len(sb_tools)} screenbuddy tools")

# ── 4. Extension routes ────────────────────────────────────────────────────
print("\n=== 4. Extension routes ===")
r = abp_req("/api/screenbuddy/status")
check("GET status", r.get("ok") is True, json.dumps(r.get("data", {}))[:150])

r = abp_req("/api/screenbuddy/finetune/status")
check("GET finetune/status", "datasets" in r or "backend" in r, json.dumps(r)[:200])

r = abp_req("/api/screenbuddy/outcome", {"ref": "ollama_local/qwen2.5:0.5b", "success": True, "latency_ms": 120})
check("POST outcome", r.get("ok") is True, json.dumps(r)[:200])

r = abp_req("/api/screenbuddy/recommend", {"prompt": "hello world", "task": "chat"})
check("POST recommend", r.get("ok") is True, json.dumps(r)[:200])

r = abp_req("/api/screenbuddy/sandbox_exec", {"tool": "run_shell", "args": {"command": "echo E2E_SANDBOX_OK"}})
check("POST sandbox_exec", r.get("ok") is True and "E2E_SANDBOX_OK" in r.get("output", ""), json.dumps(r)[:200])

# ── 5. Pattern D: Backend ──────────────────────────────────────────────────
print("\n=== 5. Pattern D — Backend ===")
r = abp_req("/api/backend/default/screenbuddy")
check("ABP backend", r.get("_status") != 404, json.dumps(r)[:200])

# ── 6. Pattern G: Memory ───────────────────────────────────────────────────
print("\n=== 6. Pattern G — Memory ===")
r = abp_req("/api/approvals")
check("ABP approvals", isinstance(r, dict) or isinstance(r, list), json.dumps(r)[:150])

# ── 7. Pattern K: Persona ──────────────────────────────────────────────────
print("\n=== 7. Pattern K — Persona ===")
r = abp_req("/api/agent/config")
check("ABP agent/config", r.get("_status") != 404, json.dumps(r)[:200])

# ── 8. Pattern M: Swarm ────────────────────────────────────────────────────
print("\n=== 8. Pattern M — Swarm ===")
r = abp_req("/api/swarms")
if isinstance(r, list):
    check("ABP swarms", True, f"{len(r)} swarms")
elif isinstance(r, dict):
    check("ABP swarms", r.get("_status") != 404, json.dumps(r)[:200])
else:
    check("ABP swarms", False, str(type(r)))

# ── 9. ABP → ScreenBuddy ask ───────────────────────────────────────────────
print("\n=== 9. ABP → ScreenBuddy ask ===")
r = abp_req("/api/agent/ask", {
    "source_instance": "screenbuddy",
    "target_instance": "screenbuddy-test",
    "prompt": "E2E test: reply with INTEGRATION_OK",
})
check("POST agent/ask", r.get("_status") != 404, json.dumps(r)[:300])

# ── 10. H1: Integration scopes ────────────────────────────────────────────
print("\n=== 10. H1 — Integration scopes ===")
r = abp_req("/api/agent/permissions")
check("ABP permissions", isinstance(r, dict) or isinstance(r, list), json.dumps(r)[:200])

# ── Summary ────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
p = sum(1 for s, _, _ in results if s == PASS)
f = sum(1 for s, _, _ in results if s == FAIL)
print(f"RESULTS: {p} passed, {f} failed")
if f:
    print("\nFailures:")
    for s, name, detail in results:
        if s == FAIL: print(f"  - {name}: {detail}")
print("\n" + "=" * 60)
print("E2E verification complete.")
