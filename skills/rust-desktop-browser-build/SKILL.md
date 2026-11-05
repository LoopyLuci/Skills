---
name: rust-desktop-browser-build
description: "Rust desktop browser build on Windows: X: toolchain"
category: software-development
---
# Rust Desktop Browser Build

---
name: rust-desktop-browser-build
description: "Rust desktop browser build on Windows: X: toolchain"
tags: [rust, desktop-browser, windows, browzeit]
category: software-development
license: MIT
version: "1.0"
---
# Rust Desktop Browser Build

## When to Use
- Building a native Rust desktop browser (Browzeit) on Windows with the X: toolchain
- Implementing a multi-phase Rust library workspace with crates/traits, crates/types, crates/core, crates/engine, crates/renderer, crates/network, crates/driver
- Setting up a from-scratch browser architecture with independent, minimal-dependency crates

## Always-On Rules
## User Preferences
- **Workflows**: "proceed with all optimally" = full implementation of every phase with working artifacts, never a stub, never "next steps" substituted for implementation
- **GUI**: Desktop GUI = pywebview/Tauri shell, never browser dashboard. Use pywebview or Tauri for the native shell with webpack/Tauri integration
- **Generative UI**: agent must create/modify/optimize UI in real time (add_button, change_layout, theme)
- **Verification**: integration tests in crates/*/tests/, cargo test green before moving on
- **Zero tolerance**: compile errors and warnings block moving forward

## Project Context: Browzeit
- **Name**: Browzeit (fully independent browser)
- **Workspace**: X:\Projects\Browzeit\browzeit (Cargo workspace)
- **Drives**: X: = junction to Z:/x/, C: at 90% full — NEVER use C:
- **Architecture**: 7-crate Rust workspace: traits, types, core, engine, renderer, network, driver
- **General**: 7 phases (see below) + protocol layer + generative canvas

## Phase Execution Order

### Phase 1 — Core (Parser, DOM, CSS)
1. Define `crates/traits/Cargo.toml` (Parser trait)
2. Define `crates/types/Cargo.toml` (DOM types: Node, Element, Text, Comment)
3. Implement HTML5 parser in `crates/core/src/parser.rs` (tokenizer + tree builder)
4. Implement CSS cascade in `crates/core/src/style.rs`
5. Add integration tests in `crates/core/tests/`
6. Verify: `cargo check -p browzeit-core` and `cargo test -p browzeit-core`

### Phase 2 — Network (HTTP, Cookies, Cache)
1. Define `crates/network/Cargo.toml` (HttpClient, cookies module)
2. Implement HTTP client (rustls + hyper optional)
3. Implement cookie store and cache
4. Verify: `cargo check -p browzeit-network`

### Phase 3 — Layout/Engine
1. Implement layout engine: box model, flex/grid
2. Define `crates/engine/Cargo.toml`
3. Implement layout pipeline
4. Verify: `cargo check -p browzeit-engine`

### Phase 4 — Renderer (Graphics)
1. Define `crates/renderer/Cargo.toml` (paint, compositing modules)
2. Implement off-screen rendering and compositing
3. Verify: `cargo check -p browzeit-renderer`

### Phase 5 — Agent (Autonomous Actions)
1. Define agent interface in `crates/engine/src/agent.rs`
2. Implement agent command parsing and execution
3. Verify: `cargo check -p browzeit-engine`

### Phase 6 — Driver (Desktop Shell)
1. Define `crates/driver/Cargo.toml` (BrowserWindow, webview module)
2. Implement pywebview/Tauri shell with navigation bar and tabs
3. Verify: `cargo check -p browzeit-driver`

### Phase 7 — Generative UI
1. Add agent methods: `add_button`, `change_layout`, `theme`
2. Agent creates/modifies UI in real time
3. Verify: `cargo check --workspace` and `cargo test`

### Build & Verification Commands
```powershell
# Set X: toolchain (run once per session)
$env:RUSTUP_HOME = "X:/Dev/rustup"
$env:CARGO_HOME = "X:/Dev/cargo"
$env:CARGO_TARGET_DIR = "X:/Dev/cargo-target"

# Full workspace check
cargo check --workspace

# Core crate check
cargo check -p browzeit-core

# Run integration tests
cargo test -p browzeit-core --test sanity
```

### IPC Bridge: pywebview Python Shell ↔ Rust Engine
The browser shell is built as:
- **Python** (pywebview + WebView2): native desktop shell, GUI, agent chat, generative canvas
- **Rust** (axum HTTP server): IPC API for browser control, agent task management, SSE streaming

**Key endpoints:**
- `GET /api/browser/tabs` — list browser tabs
- `POST /api/browser/navigate` — navigate to URL
- `POST /api/agent/task` — create an agent task
- `GET /api/agent/results/{task_id}` — get task results
- `GET /api/agent/stream/{task_id}` — SSE stream for live thought streaming
- `GET /api/health` — health check

**pywebview wiring:**
1. Python starts local HTTP server (e.g., port 8765) serving `index.html` and static assets
2. Python uses `webview.create_window(url="http://127.0.0.1:8765/index.html", ...)`
3. Python server proxies API calls to Rust via HTTP client or direct Python imports
4. Rust API server listens on port 8766, Python GUI on 8765
5. SSE endpoints (`/api/agent/stream/{task_id}`) return `text/event-stream` for live thought streaming

**Python server pseudo-structure:**
```python
import webview, threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

class BrowzeitHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/"):
            # Proxy to Rust API server (http://127.0.0.1:8766)
            pass
        else:
            super().do_GET()

server = HTTPServer(("127.0.0.1", 8765), BrowzeitHandler)
threading.Thread(target=server.serve_forever, daemon=True).start()
webview.create_window("Browzeit", "http://127.0.0.1:8765/index.html")
webview.start()
```

**SSE streaming pattern (JavaScript):``
```javascript
const evtSource = new EventSource("http://127.0.0.1:8766/api/agent/stream/{task_id}");
evtSource.onmessage = (e) => {
  const data = JSON.parse(e.data);
  appendMessage(data.content, "assistant");
  updateTokens(data.token_count, data.tps);
};
```

## Tool-Use Patterns
- **`write_file` read-before-write rule**: The `write_file` tool refuses to overwrite a file that was last read with `offset`/`limit` pagination (partial view). To overwrite: (1) read the file with a full `read_file` (no offset/limit, or read from line 1 through end), then call `write_file`. Or use `patch` for targeted edits. Do NOT delete-and-recreate for files >50 lines — the `write_file` tool's stale-checksum guard will block repeated overwrites.
- **`patch` for multi-line edits**: For files with pre-existing content, `patch` works reliably where `write_file` gets blocked by the read-before-write guard. Batch multiple `patch` calls for multi-section changes.
- **Rust std naming**: `std::sync::mpsc::sync_channel` (snake_case), NOT `mpsc::SyncChannel`. Old `mpsc::SyncChannel` does not exist in Rust 2021 edition.
- **uuid crate v1.x**: `Uuid::new_v4()` has no `as_u64()` method. Use `Uuid::new_v4().as_u128() as u64` or `Uuid::new_v4().to_u128_le() as u64`. The `as_u64()` method was removed in newer uuid crate versions.
- **mpsc channel type**: `mpsc::sync_channel(n)` returns `(SyncSender, Receiver)`. The sender type is `mpsc::SyncSender<T>`, not `mpsc::Sender<T>`. Use `tx.send(())` for sync sender.

## Verification-First Workflow
- **User workflow preference**: "proceed with all optimally" means full implementation of every phase with working artifacts, never a stub and never "next steps" substituted for implementation
- **Fix warnings before proceeding**: cargo warnings (unused variables/fields) block clean verification
- **Zero tolerance for compile errors**: rustc/cargo check must pass before moving to the next phase
- **Next steps = implementation, not release advice**: when the user asks what to do next, do the work, then report results
- **Verify after every edit**: run `cargo check --workspace` after any structural change to parser code

### Rust-specific Build Patterns
- **Interior mutability on `Arc<T>`**: when a struct is wrapped in `Arc` and needs mutation, use `RefCell` for fields that change. Do NOT try to get `&mut T` through `Arc` — call `.borrow_mut()` and assign through the returned `RefMut`.
- **Write-file token mismatch**: the `write_file` tool refuses overwrites when the file was modified on disk after last read (CRLF↔LF conversion counts as a modification). To overwrite a Rust source file: (1) delete it with `terminal` first, then (2) `write_file` without reading it. For small targeted edits, use `patch` instead. Do NOT delete-and-recreate for files >50 lines.
- **Heredoc Python quoting**: `python3 << 'PYEOF'` heredocs break when content contains `'''` (triple quotes). Keep Python content simple or write via `write_file` tool.
- **`Arc` copy violation**: `Arc<T>` does not implement `Copy`. `state.clone()` creates a new `Arc` sharing the same `T`. After mutating through one clone, the other reads stale state.
- **Search for duplicate code blocks**: after editing, verify the file is structurally sound: search for duplicate code blocks using `content.find()` with a start offset; count braces with a script to find unmatched blocks; remove duplicate sections.
- **Rust `and_then` + `Result` pitfall**: chaining `.and_then()` with a closure returning `Result<T, E>` produces a nested `Result<Result<T, E>, E>`, not `Result<T, E>`. Use `?` to flatten, or wrap in `map` and match. Never return a nested `Result` from a function expecting `Result<T, E>`.
- **`RefCell` struct literal pattern**: when a struct has `RefCell` fields, every struct literal that initializes those fields must wrap the value in `RefCell::new()`. Also wrap in `RefCell` in the struct definition. Access via `field.borrow()` (shared) or `field.borrow_mut()` (mutable), and assign through the returned `RefMut` via `*field.borrow_mut() = value;`.
- **Rust build iteration workflow**: run `cargo build` directly (without piping through `tail`/`head`) — the exit code of `| tail` is that of `tail`, not `cargo`, so a build failure reports exit 0. Read the full error list from the pipeline output. Iterate on one error at a time; for E0308/E0382/E0594/E0425/E0594, read the full error block including the `help:` suggestions.
- **Borrow checker: `navigate()` pattern**: when a method needs to mutate both `self.history` and a `tab` in `self.tabs`, first get the `tab_id` via `self.current_tab_id` (not `self.current_tab()`), then use `self.tabs.iter_mut().find(|t| t.id == *tab_id)`. Calling `self.current_tab()` borrows `self` immutably, which conflicts with later mutable borrows of `self.history` and `self.tabs`.
- **Borrow checker: `set_title()` pattern**: never call `self.current_tab()` then `self.tabs.iter_mut()` in the same function. Instead, hold the tab ID (`self.current_tab_id`) and use `self.tabs.iter_mut().find(|t| t.id == *tab_id)` directly. The immutable borrow from `current_tab()` prevents the mutable borrow of `tabs`.
- **Borrow checker: `history` truncation**: when truncating `self.history` then pushing to it in the same function, compute the truncation condition first (e.g., `let truncate = match self.history.last() { ... }`), then do the truncate and push in separate statements. The `self.history.last()` call borrows `self.history` immutably, conflicting with the mutable `truncate()` and `push()` calls.

## Pitfalls
- **Always run cargo check before adding more phases** — nested impl blocks in Rust surface late
- **Nested `impl` blocks in Rust cause E0599** — flat impl blocks preferred
- **Cargo `python3`/`rustc` not on PATH** — use full path or msys shell
- **Heredoc Python scripts fail with `unexpected EOF`** — use `write_file` instead
- **sed on Rust files removes braces** — use Python scripts for multi-line edits
- **Nested impls create 'unexpected closing delimiter' errors** — check brace balance after edits
- **Cargo warnings (unused variables/fields) block clean check** — fix warnings before proceeding
- **parser.rs structure corruption**: after editing, verify the file is structurally sound: (1) search for duplicate code blocks using `content.find()` with a start offset; (2) count braces with a script to find unmatched blocks; (3) remove duplicate sections; (4) ensure `impl` blocks are properly closed with matching `}`; (5) confirm each function has a body (not just `{ }`)
- **Associated function calls**: when calling an associated function defined in the same `impl Parser` block, use `Self::make_tag_token(...)` instead of `make_tag_token(...)` — bare function calls fail with E0425 "not found in this scope"
