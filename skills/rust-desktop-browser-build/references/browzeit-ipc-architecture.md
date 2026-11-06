## IPC Bridge Architecture: pywebview Python Shell ↔ Rust axum Engine

The Browzeit desktop shell is a two-process system (not a single GUI binary):

1. **Python (pywebview + WebView2)**: native desktop shell — the window, browser chrome, agent chat panel, and generative canvas. Starts a local HTTP server (e.g., port 8765) serving `index.html` and static assets, then opens the WebView2 window via `webview.create_window(url="http://127.0.0.1:8765/index.html", ...)`.
2. **Rust (axum HTTP server)**: the IPC bridge. `crates/api` exposes REST endpoints and SSE streaming on port 8766. It owns a `GLOBAL_ORCHESTRATOR` (a `pub static mut` wrapped in `Arc<Mutex<DriverAgentOrchestrator>>`) that the Python shell's HTTP handlers access via `browzeit_api::GLOBAL_ORCHESTRATOR`.

**Key endpoints (Rust axum server, port 8766):**
- `GET /api/browser/tabs` — list browser tabs
- `POST /api/browser/navigate` — navigate to URL (JSON body `{"url": "..."}`)
- `POST /api/agent/task` — create an agent task (JSON body with `task`, `model`, `parameters`)
- `GET /api/agent/results/{task_id}` — get task results
- `GET /api/agent/stream/{task_id}` — SSE stream for live thought streaming
- `GET /api/health` — health check

**SSE streaming pattern (JavaScript):**
```javascript
const evtSource = new EventSource("http://127.0.0.1:8766/api/agent/stream/{task_id}");
evtSource.onmessage = (e) => {
  const data = JSON.parse(e.data);
  appendMessage(data.content, "assistant");
  updateTokens(data.token_count, data.tps);
};
```

**SSE endpoint pattern (Rust axum):** return `text/event-stream`, `Cache-Control: no-cache`, `Connection: keep-alive`. Stream JSON messages line-by-line.

**Python server pseudo-structure (port 8765):** `SimpleHTTPRequestHandler` on `127.0.0.1:8765` that proxies `/api/*` to the Rust server at `127.0.0.1:8766` and serves static GUI files locally. Start in a daemon thread.