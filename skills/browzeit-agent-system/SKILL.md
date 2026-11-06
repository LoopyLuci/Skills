---
name: browzeit-agent-system
description: Build Browzeit agent system with MoE/MoA/subagents and GUI.
---

# Browzeit Agent System

The Browzeit agent system orchestrates browsers with AI agents, supporting MoE (Mixture of Experts), MoA (Mixture of Agents), subagents, swarms, and session/chat forking. The system lives in a Rust workspace (`crates/`) with a pywebview desktop GUI shell.

## Trigger

- User asks to build or extend the Browzeit browser's agent system.
- User asks for MoE/MoA routing, subagent spawning, session forking, or agent swarms.
- User asks for the desktop GUI scaffold (pywebview/Tauri) for a Rust agentic browser.
- User asks for API/CLI/MCP/ACP interfaces to control the browser agent.

## Project Layout

```
crates/
  traits/
  types/
  core/
  engine/src/
    agent/           # AgentOrchestrator + MoE/MoA/subagent/session/swarm modules
    layout.rs        # Layout engine
  renderer/
  network/
  driver/src/        # Driver shell (AgentOrchestrator wrapper + BrowserWindow)
  api/src/           # Axum REST API + SSE streaming
  gui_shell/          # Python pywebview shell
```

## Workload Phase 1: Agent Orchestrator Core

1. `AgentOrchestrator::new()` creates expert configs: `default` (gpt-4, 4096 max tokens, 0.7 temp, [text, reasoning]), `fast` (gpt-3.5-turbo, 2048 max tokens, 0.5 temp, [text]), `creative` (claude-3, 8192 max tokens, 1.0 temp, [text, creative]).
2. `register_llm_client()` wraps the LLM client behind a trait (`LLMClient: Send + Sync`) with `generate(prompt, tools) -> String` and `set_simulated_response(response)`.
3. `execute(task)` creates `AgentState` (wrapped in `Arc<...>`), runs the agent loop via `run_agent_loop()`, records telemetry, returns `Snapshot`.
4. `run_agent_loop()` iterates up to `max_steps`, calls `llm_client.generate()`, parses response via `parse_action()`, executes the action (Navigate, Extract, Click, Fill, Evaluate, SpawnSubagent, UseMoE, UseMoA, ForkSession, Done, Wait).
5. `parse_action()` maps LLM responses to actions by keyword: `done`/`exit` -> Done, `navigate` -> Navigate (extract URL), `extract` -> Extract (CSS selector), `click` -> Click, `fill` -> Fill, `eval`/`evaluate` -> Evaluate (extract code), `spawn` -> SpawnSubagent, `moe`/`ensemble` -> UseMoE, `moa`/`committee` -> UseMoA, `fork` -> ForkSession, `think`/`observe`/`wait` -> Wait, default -> Done with text.
6. `compute` the snapshot: build `Snapshot` from `Session` (url, title, body_text), create a render tree, return via `build_snapshot()`.

### AgentState (interior mutability)

```rust
#[derive(Debug, Clone)]
struct AgentState {
    id: String,
    task: Task,
    status: RefCell<AgentStatus>,
    logs: RefCell<Vec<String>>,
    start_time: Instant,
    max_steps: u32,
    steps_taken: RefCell<u32>,
    subagents: RefCell<HashMap<String, Arc<AgentState>>>,
}
```

All mutable fields must use `RefCell` for interior mutability. In struct literals: `RefCell::new(...)`.

## Workload Phase 2: MoE / MoA / Subagents / Session

### MoE (Mixture of Experts)

- `moe.rs` exports `MoERouter` with `experts: HashMap<String, ExpertConfig>`.
- `route(task) -> (String, ExpertConfig)` selects best expert by `score_expert()`:
  - +10 per matching capability (capability check: `config.capabilities.contains(&cap)`)
  - +10 if task has no tools (cheaper expert)
  - +10 * `(1.0 - latency_estimate / 5.0)` for faster experts
- `score_expert()` returns u32.
- `ExpertConfig` fields: `name`, `model`, `max_tokens`, `temperature`, `capabilities: Vec<String>`, `cost_per_token: f64`, `latency_estimate: f32`.
- `dynamic_loading` creates new `expert-{n}` if no expert scores > 0.

### MoA (Mixture of Agents)

- `moa.rs` exports `MoAAggregator` with `config: MoAConfig` and `outputs: HashMap<String, Vec<String>>`.
- `run(task, &agents, llm_client) -> String`: iterate `config.iteration_count` (3) times:
  1. Generate response from each agent via `llm_client.generate(prompt, tools)`
  2. Check convergence (all agents discuss same topic)
  3. Build consensus prompt from responses
  4. Generate consensus response
  5. If converged, break
- Aggregation: `weighted_vote` (highest score), `weighted_avg` (weighted by agent type), `consensus` (most common response)
- `MoAConfig` fields: `name`, `agents: Vec<String>`, `iteration_count: u32`, `aggregation_strategy`, `temperature`, `max_tokens`.

### Subagent Spawning

- `spawn_subagent(prompt, tools) -> Arc<AgentState>`:
  - Create `AgentState` with `id: format!("sub-{}", self.session.next_id())`
  - `task: Task::new(&prompt)` with `task.tools = tools`
  - `max_steps: 5`
  - Insert into `self.agents` (Arc clone returned)
- `AgentAction::SpawnSubagent { prompt, tools }` triggers this path in the agent loop.

### Session/chat Forking

- `fork_session(session_id, prompt) -> Session`:
  - Clone parent session via `new_session.fork_from(&parent)`
  - `new_session.add_chat(prompt.to_string())`
- `Session` tracks: `chats: Vec<String>`, `urls: Vec<String>`, `body_texts: Vec<String>`, `title`, `chat_id: u64`.
- `next_id()` increments `chat_id`. `current_url()` returns last URL or `about:blank`.

## Workload Phase 3: Driver Wrapper

`driver/src/agent.rs` provides `DriverAgentOrchestrator`:

- `use types::browser::BrowserWindow` (NOT `driver::shell::BrowserWindow`)
- `pub fn new() -> Self` (0 args, creates `BrowserWindow::new()` internally)
- Fields: `id: u64`, `browser: BrowserWindow`, `engine_orchestrator: AgentOrchestrator`, `task_queue: Vec<(String, String)>`, `results: HashMap<String, Snapshot>`, `shutdown_tx: Option<mpsc::SyncSender<()>>`.
- `result(&self, task_id: &str) -> Option<&Snapshot>` returns `self.results.get(task_id)`.
- The engine's `AgentOrchestrator` is NOT wrapped in `Arc<Mutex<>>`. The API crate wraps it externally.

## Workload Phase 4: API Server (axum)

`api/src/lib.rs` exports `DriverAgentOrchestrator` + `types` module.

- `pub mod types` contains `ApiResponse`, `BrowserTab`, `BrowserState`, `AgentTaskRequest`, `AgentTaskResponse`, `ThoughtEvent`.
- `pub static mut GLOBAL_ORCHESTRATOR: Option<Arc<std::sync::Mutex<DriverAgentOrchestrator>>>` must be `pub` for `main.rs` to access it.
- Routes:
  - `GET /` or `/api/health` -> `"ok"`
  - `GET /api/browser/tabs` -> `Json(ApiResponse)` with `BrowserTab` fixtures
  - `POST /api/browser/navigate` -> `Json(ApiResponse<()>)` with `url`
  - `POST /api/agent/task` -> `Json(ApiResponse<AgentTaskResponse>)` with `task_id`, `status`, `model`
  - `GET /api/agent/results/{task_id}` -> `Json(ApiResponse<()>)` via `GLOBAL_ORCHESTRATOR` lock
  - `GET /api/health` -> health check
- `pub async fn run()`:
  1. Create `Arc<Mutex<DriverAgentOrchestrator>>`
  2. Set `unsafe { GLOBAL_ORCHESTRATOR = Some(...) }`
  3. Build `axum::Router` with routes
  4. `let listener = TcpListener::bind("127.0.0.1:8766")`
  5. `axum::serve(listener, app).await.expect("Server failed")`

### `get_agent_results` handler

```rust
async fn get_agent_results(Path(task_id): Path<String>) -> Json<api_types::ApiResponse<()>> {
    let orchestrator = unsafe { browzeit_api::GLOBAL_ORCHESTRATOR.as_ref().and_then(|o| o.lock().ok()) };
    if let Some(orchestrator) = orchestrator {
        if let Some(_result) = orchestrator.result(&task_id) {
            Json(api_types::ApiResponse {
                success: true, data: None, error: None, task_id: Some(task_id.clone()),
            })
        } else {
            Json(api_types::ApiResponse { success: false, data: None, error: Some("Task not found".into()), task_id: Some(task_id), })
        }
    } else {
        Json(api_types::ApiResponse { success: false, data: None, error: Some("Orchestrator not initialized".into()), task_id: None, })
    }
}
```

## Workload Phase 5: GUI Shell (pywebview + SSE)

`gui_shell/browzeit_shell.py`:

- `BrowzeitHandler(SimpleHTTPRequestHandler)` serves local HTTP server on `127.0.0.1:8765`.
- Endpoints:
  - `GET /api/browser/tabs` -> `Json({"tabs": [...]})`
  - `GET /api/agent/task` -> `Json({"tasks": [...]})`
  - `GET /api/agent/stream` -> SSE (`Content-Type: text/event-stream`, `Cache-Control: no-cache`, `Connection: keep-alive`). Send `event: connected` + JSON.
  - `POST /api/browser/navigate` -> `Json({"url": url, "success": true})`
  - `POST /api/agent/task` -> creates task, simulates streaming (threaded), returns `{"task_id": ..., "status": "queued", "result": None}`
  - `POST /api/agent/stream` -> SSE for thought streaming
- `webview.create_window("Browzeit - Next-Gen Browser", "http://127.0.0.1:8765/index.html", ...)` for native shell.
- `PYTHONPATH=src pytest` for verification of Python modules.

## Verification Gate (F1)

Run in order; stop on first failure:

1. `cargo build --workspace --all-targets` -> exit 0
2. `cargo fmt --all -- --check` -> FMT_OK
3. `cargo clippy --workspace --all-targets -- -D warnings` -> 0 errors
4. `cargo test --workspace` -> all crates green (including `rpc-cli` self-test, `rpc-api` doctest)

## Rust Workspace Verification

After making any code changes, run the following sequence before declaring work complete:

1. `cargo check --workspace 2>&1 | grep "^error" | wc -l` -> must be 0 (if >0, iterate until clean)
2. `cargo check --workspace` -> must complete with only warnings (no errors)
3. `cargo fmt --all -- --check` -> must report FMT_OK
4. `cargo clippy --workspace --all-targets -- -D warnings` -> 0 errors
5. `cargo test --workspace` -> all crates green

## Pitfalls

- **CRLF line endings break patch tool**: Files in the repo have CRLF endings. Before patching, run `sed -i 's/\r$//' <file>` to convert to LF. The patch tool silently fails on CRLF files.

- **Agent module files live in a directory, not a mod.rs**: `engine/src/agent.rs` declares `pub mod moa; pub mod moi; ...` — but these modules are separate files in `engine/src/agent/`. Each must be patched as a standalone file, not written as a nested mod.rs.

- **AgentState requires interior mutability**: All mutable fields in `AgentState` use `RefCell`. In struct literals: `RefCell::new(...)` for every mutable field (status, logs, steps_taken, subagents).

- **API crate thread-safety**: The `DriverAgentOrchestrator` contains `AgentOrchestrator` which has `RefCell` fields. The API server wraps it in `Mutex<DriverAgentOrchestrator>` for thread safety. `GLOBAL_ORCHESTRATOR` must be `pub` for `main.rs` to access it.

- **Do NOT use `driver::shell::BrowserWindow`**: Use `types::browser::BrowserWindow` in the driver's agent.rs. The shell's `BrowserWindow` is a different type.

- **LLMClient import path**: `LLMClient` trait is defined in `engine/src/agent.rs` (not in `agent/protocol.rs`). Import as `use crate::agent::LLMClient;`, not `use crate::agent::protocol::LLMClient;`.

- **Agent module files are stubs**: Files like `moi.rs`, `subagent.rs`, `swarm.rs`, `session.rs` may start as 20-25 byte stubs that need full implementation. Do NOT leave them as placeholders.

- **Patch file must be re-read after external modification**: After terminal commands modify a file (e.g., `sed -i`), the patching tool may report "was modified since last read." Re-read the file, then patch again.

- **Workspace verification before declaring done**: Always run `cargo check --workspace` and confirm exit 0 with 0 errors. Warnings are acceptable (they are usually unused variable/lint warnings).

- **Rust 2024: static_mut_refs warning**: `static mut` references require `unsafe` blocks. Warnings are acceptable — only errors block the build.

- **Right-side file not written**: After a file write (cargo patch/terminal), verify with `cargo check` — changes may not land if the file was not properly flushed.

- **Heredoc corruption in bash**: Writing Rust files via `cat << 'EOF'` in bash can silently corrupt content (unbalanced quotes, escape issues). If the file does not compile, re-read it and re-write it using the `write_file` tool or `patch` tool instead of heredocs. The `write_file` tool is safe and does not mangle content. This was observed during the Browzeit implementation when `moe.rs` and `moa.rs` were repeatedly corrupted by heredoc quoting.

- **Duplicate content in SKILL.md**: When patching, check for duplicate sections (the skill file may contain repeated blocks). Verify the patch target exists before writing.

## Verification Checklist

- [ ] `cargo check --workspace` -> exit 0
- [ ] `cargo test --workspace` -> all tests green
- [ ] API server starts: `cargo run -p browzeit-api` -> port 8766 listening
- [ ] GUI shell starts: `python gui_shell/browzeit_shell.py` -> window opens
- [ ] `/api/health` returns "ok"
- [ ] `/api/browser/tabs` returns tabs list
- [ ] `/api/agent/task` creates task and streams SSE thoughts
- [ ] `/api/agent/results/{task_id}` returns results
- [ ] SSE stream shows live thought events
- [ ] GUI chat panel displays tool call results
- [ ] Canvas shows agent-generated components

### GUI verification

- Start the GUI shell: `python gui_shell/browzeit_shell.py`
- Verify the window opens and serves `http://127.0.0.1:8765/`. Do NOT use `terminal(background=true)` — pywebview requires an interactive session. Instead create a `.bat` launch script for the user.
- Verify API endpoints respond: `curl http://127.0.0.1:8766/api/health`
- Verify SSE streaming: `curl -N http://127.0.0.1:8766/api/agent/stream`

- **Agent module files live in a directory, not a mod.rs**: `engine/src/agent.rs` declares `pub mod moa; pub mod moi; ...` — but these modules are separate files in `engine/src/agent/`. Each must be patched as a standalone file, not written as a nested mod.rs.

- **AgentState requires interior mutability**: All mutable fields in `AgentState` use `RefCell`. In struct literals: `RefCell::new(...)` for every mutable field (status, logs, steps_taken, subagents).

- **API crate thread-safety**: The `DriverAgentOrchestrator` contains `AgentOrchestrator` which has `RefCell` fields. The API server wraps it in `Mutex<DriverAgentOrchestrator>` for thread safety. `GLOBAL_ORCHESTRATOR` must be `pub` for `main.rs` to access it.

- **Do NOT use `driver::shell::BrowserWindow`**: Use `types::browser::BrowserWindow` in the driver's agent.rs. The shell's `BrowserWindow` is a different type.

- **LLMClient import path**: `LLMClient` trait is defined in `engine/src/agent.rs` (not in `agent/protocol.rs`). Import as `use crate::agent::LLMClient;`, not `use crate::agent::protocol::LLMClient;`.

- **Agent module files are stubs**: Files like `moi.rs`, `subagent.rs`, `swarm.rs`, `session.rs` may start as 20-25 byte stubs that need full implementation. Do NOT leave them as placeholders.

- **Patch file must be re-read after external modification**: After terminal commands modify a file (e.g., `sed -i`), the patching tool may report "was modified since last read." Re-read the file, then patch again.

- **Workspace verification before declaring done**: Always run `cargo check --workspace` and confirm exit 0 with 0 errors. Warnings are acceptable (they are usually unused variable/lint warnings).

- **Rust 2024: static_mut_refs warning**: `static mut` references require `unsafe` blocks. Warnings are acceptable — only errors block the build.

- **Right-side file not written**: After a file write (cargo patch/terminal), verify with `cargo check` — changes may not land if the file was not properly flushed.

## Verification Checklist

- [ ] `cargo check --workspace` -> exit 0
- [ ] `cargo test --workspace` -> all tests green
- [ ] API server starts: `cargo run -p browzeit-api` -> port 8766 listening
- [ ] GUI shell starts: `python gui_shell/browzeit_shell.py` -> window opens
- [ ] `/api/health` returns "ok"
- [ ] `/api/browser/tabs` returns tabs list
- [ ] `/api/agent/task` creates task and streams SSE thoughts
- [ ] `/api/agent/results/{task_id}` returns results
- [ ] SSE stream shows live thought events
- [ ] GUI chat panel displays tool call results
- [ ] Canvas shows agent-generated components

### GUI verification

- Start the GUI shell: `python gui_shell/browzeit_shell.py`
- Verify the window opens and serves `http://127.0.0.1:8765/`. Do NOT use `terminal(background=true)` — pywebview requires an interactive session. Instead create a `.bat` launch script for the user.
- Verify API endpoints respond: `curl http://127.0.0.1:8766/api/health`
- Verify SSE streaming: `curl -N http://127.0.0.1:8766/api/agent/stream`

## User's Preferred Workflow

- "Properly proceed with all optimally" = full implementation, never stubs, never placeholder text
- "What are next steps?" = implementation, not release advice
- "Thoroughness demanded: zero tolerance for errors/bugs, full implementation never stubs"
- Desktop GUI = scaffold pywebview/Tauri, never browser dashboard
- Generative UI = agents must create, modify, and optimize UI components in real-time
- Model picker, live stream of thought, tokens per second, tokens used metrics
- Model-toggle profiles (save/load/export/import)
- Cross-app collaboration: KotMoE + Agentic Workbench share provider registry, v1.1.0 profiles

## Verification Checklist

- [ ] `cargo check --workspace` -> exit 0
- [ ] `cargo test --workspace` -> all tests green
- [ ] API server starts: `cargo run -p browzeit-api` -> port 8766 listening
- [ ] GUI shell starts: `python gui_shell/browzeit_shell.py` -> window opens
- [ ] `/api/health` returns "ok"
- [ ] `/api/browser/tabs` returns tabs list
- [ ] `/api/agent/task` creates task and streams SSE thoughts
- [ ] `/api/agent/results/{task_id}` returns results
- [ ] SSE stream shows live thought events
- [ ] GUI chat panel displays tool call results
- [ ] Canvas shows agent-generated components
