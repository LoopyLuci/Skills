---
name: multi-platform-project
description: "Multi-platform apps: protocol-first, parallel delegation."
tags: [cross-platform, multi-platform, protocol-first, protobuf, parallel-delegation, monorepo]
related_skills: [python-package-build, frontend-bootstrap, spike, service-orchestration, test-driven-development]
---

# Multi-Platform Project (Protocol-First + Parallel Delegation)

## When to Use

- A user asks to build the same app on **Android + iOS + Desktop** (or any multi-platform combination)
- The project has multiple runtime components that share a **wire protocol or data contract**
- You need to **generate a complete project tree** with shared libraries and per-platform implementations
- The request is large enough that **parallel delegation** saves wall-clock time over building each component sequentially

Do **not** use for:
- Adding a feature to an existing single-platform project (use the platform's own skill)
- A pure library with no platform-specific UI (use `spike` or a library-scaffold skill)
- A task where the platforms share so much logic that one codebase (e.g. React Native, Flutter) is a better answer

## Core Pattern

```
1.  PROTOCOL FIRST
2.  DELEGATE PLATFORMS IN PARALLEL
3.  BUILD PRIMARY PLATFORM DIRECTLY IN THIS SESSION
4.  VERIFY WITH AVAILABLE TOOLCHAINS
5.  CLEAN UP (remove temp scaffolding, verification scripts)
```

## Phase 1 — Protocol First

Before writing platform code, define the wire protocol. This becomes the contract every platform implements against.

### Recommended approach

- **Protobuf** (`.proto` file) — strongly typed, cross-platform, code-gen for Rust/Kotlin/Swift/Python
- Alternative: a JSON schema + documented message shapes (lighter weight, no code-gen)
- Keep the proto at the repo root under `protocol/`

### Structure

```
project/
├── protocol/
│   └── streamsync.proto        ← shared contract
├── shared/                     ← cross-platform shared libs
│   ├── rust/                   ← core library (serialization, crypto, discovery)
│   └── kotlin/                 ← KMP shared module (optional)
├── android/                    ← primary platform (Kotlin/Jetpack Compose)
├── ios/                        ← companion (Swift/SwiftUI)
├── desktop-rust/               ← companion (Rust + Tauri)
├── desktop-python/             ← companion (Python CLI/GUI)
└── README.md
```

### Key rules

- The proto file must be **the single source of truth** — every platform reads the same spec
- Define all message types, enums, and wrapper structures up front
- Document the message flow (discovery → handshake → transfer → completion) in the README
- Use protocol versioning for forward compatibility

### Alternative: MCP as the Unifying Protocol

For **agent-native** applications where AI agents need to control every platform, use the **Model Context Protocol** (JSON-RPC 2.0 over WebSocket/stdio) instead of Protobuf:

```
project/
├── mcp-spec/
│   └── schema.yaml              ← shared MCP tool/resource/event contract
├── rust-core/                   ← primary platform (Rust, speaks MCP natively)
├── python-bridge/               ← orchestrator (Python MCP client)
├── clojure-engine/              ← rule engine (Clojure MCP server)
├── web-frontend/                ← Svelte/TypeScript MCP client
├── ios/                         ← Swift MCP client (NEDNSSettingsManager)
├── android/                     ← Kotlin MCP client (VpnService)
└── cross-build/                 ← CI matrix
```

**Each platform implements an MCP client** that connects to the Rust core's MCP server on `ws://host:9822`. The MCP contract (10+ tools for status, block, firewall, config) is the single source of truth — identical tool signatures across every language.

| Platform | MCP Client Implementation | Transport |
|----------|--------------------------|-----------|
| Rust | `tokio-tungstenite` WebSocket server | ws:// |
| Python | `websockets` library | ws:// |
| TypeScript | `WebSocket` API (browser) | ws:// |
| Swift | `URLSessionWebSocketTask` | ws:// |
| Kotlin | raw `Socket` + buffered I/O | ws:// |

**Advantages over Protobuf:**
- No code-gen step — tools are discovered dynamically via `tools/list`
- AI agents (Hermes, Claude) can control every platform without language-specific bindings
- Runtime capability discovery — tools self-describe via JSON Schema
- Event subscription model for real-time updates
- Same protocol powers the web dashboard, mobile apps, and agent control

**Trade-off**: Higher per-message overhead (JSON vs binary), but negligible for control-plane operations.

## Phase 2 — Delegate Platform Components in Parallel

Use `delegate_task` with the **batch `tasks` array** to dispatch N platform implementations concurrently.

```
delegate_task(tasks=[
    {
        "goal": "Build the Rust core library + Tauri desktop app...",
        "context": "Protocol at <path>. Project root at <path>.",
    },
    { "goal": "Build the iOS Swift/SwiftUI companion...", "context": "..." },
    { "goal": "Build the Python desktop companion...", "context": "..." },
])
```

### Rules for subagent context

1. **Be maximally explicit** — the subagent has NO conversation history. Include absolute paths, directory trees, file names, and import paths.
2. **Each subagent owns its own directory** — never overlap paths between subagents.
3. **Give each subagent a `todo` plan first** — it should plan its files, then write them.

### Sibling file conflict warning

When subagents write under the same project root, `write_file` warns if a sibling modified a file since your last read. The file IS written; acknowledge the warning. If you must re-write a sibling's file, read it first to clear the "last-read" state.

## Phase 3 — Build Primary Platform Directly

Build the primary platform (usually the first one the user named) while subagents work.

### Android (Kotlin + Jetpack Compose)

| Layer | Key files |
|---|---|
| Build | `settings.gradle.kts`, `app/build.gradle.kts`, `gradle.properties` |
| Manifest | `AndroidManifest.xml`, `file_paths.xml`, `network_security_config.xml` |
| Theme & Nav | `Theme.kt`, `NavGraph.kt` |
| Models | `Models.kt` — Device, Transfer, StreamSession, ClipboardEntry, enums |
| Protocol | `ProtocolHandler.kt` — JSON serialization, AES-256-GCM, chunking |
| Services | `DiscoveryService.kt` (NSD), `TransferService.kt` (Ktor WS), `StreamService.kt` (ExoPlayer), `ClipboardSyncService.kt` |
| UI | Dashboard, Devices, Transfers, Stream, Settings, Clipboard, DeviceDetail, StreamPlayer |

### iOS (Swift + SwiftUI)

| Layer | Key files |
|---|---|
| Entry | `StreamSyncApp.swift`, `ContentView.swift` |
| Models | `DeviceIdentity.swift`, `DiscoveredDevice.swift`, `TransferSession.swift`, `StreamSession.swift` |
| Services | `DiscoveryService.swift` (NWBrowser), `TransferService.swift` (NWConnection), `StreamService.swift` (AVPlayer), `CryptoService.swift`, `ClipboardService.swift` |
| Views | Dashboard, Devices, Transfer, Stream, Settings, ClipboardSync |

### Desktop (Rust + Tauri)

| Layer | Key files |
|---|---|
| Backend | `src-tauri/Cargo.toml`, `build.rs`, `tauri.conf.json` |
| Rust | `main.rs` (commands), `discovery.rs`, `transfer.rs`, `crypto.rs`, `streaming.rs` |
| Frontend | `index.html` — single-page app, embedded CSS+JS, no build step |

### Desktop (Python CLI + GUI)

| Layer | Key files |
|---|---|
| Config | `pyproject.toml`, `requirements.txt`, `README.md` |
| Core | `protocol.py`, `discovery.py` (zeroconf), `transport.py` (websockets), `crypto.py` (AES-GCM), `transfer.py`, `streaming.py`, `clipboard.py`, `config.py` |
| UI | `__init__.py` (backend auto-detect), `cli_app.py` (click), `qt_app.py` (PyQt6), `tui_app.py` (textual) |
| Server | `server.py` (async WebSocket daemon) |

## Phase 4 — Ad-Hoc Verification

Create a self-contained Python script that validates what the available toolchains support.

| Platform | Can verify | Cannot verify without |
|---|---|---|
| **Rust** | `cargo test` (compile + unit tests) | `cargo tauri build` (needs node + tauri-cli) |
| **Python** | `py_compile` every `.py` | PyQt6 GUI (needs display) |
| **Kotlin/Android** | Structural: files exist, named correctly | `./gradlew assembleDebug` (needs Android SDK) |
| **Swift/iOS** | Structural: files exist, named correctly | `xcodebuild` (needs macOS + Xcode) |

**Always clean up the verifier** after running — it's a one-shot tool, not a project artifact.

## Phase 5 — Final Inventory

Run a final file count per component (files, lines, KB). Prints a completeness table.

## Common Pitfalls

### Rust: prost-build

- Add `protoc-bin-vendored = "3"` to `[build-dependencies]`
- Set `PROTOC` env var in `build.rs`
- Generated module name is **snake_case** of the proto package: `streamsync_message` → `stream_sync_message`
- Use `include!(concat!(env!("OUT_DIR"), "/streamsync.rs"))` — not relative
- `prost 0.13` generates `bytes::Bytes` for bytes fields; use `.to_vec()` for Vec
- Delete `target/` after proto changes

### Rust: third-party crate quirks

- **`mdns-sd 0.13`**: `ServiceInfo::new(type, instance, host, target, port, props: HashMap<String,String>)`. `ServiceEvent` has `ServiceResolved` and `ServiceRemoved(_, name)` — no `ServiceAdded`.
- **`aes-gcm 0.10`**: Use `Aes256Gcm::new_from_slice(key)`, 12-byte nonce prepended to ciphertext. Import `aead::{Aead, KeyInit}`, not `AeadInOut`.
- **`tokio-tungstenite 0.24`**: Bind `TcpListener` with `SocketAddr`, not `u16`. `accept_async` returns `WebSocketStream<MaybeTlsStream<TcpStream>>`.

### Python: no protobuf

Hand-write JSON message serialization matching proto shapes. No code-gen needed.

### Subagents: don't poll

`delegate_task` returns immediately. The consolidated result re-enters when all finish. Read live transcripts to watch progress.

## Verification Checklist

- [ ] Protocol file: all message types, enums, wrapper envelope defined
- [ ] Protocol version field for forward compat
- [ ] Every platform has complete directory + build config
- [ ] Rust: `cargo check` + `cargo test` pass
- [ ] Python: all `.py` files pass `py_compile`
- [ ] Source files present, named correctly, non-empty
- [ ] Verification ran and cleaned up
- [ ] README documents protocol, architecture, build
- [ ] Project structure matches the plan

### Reference files in this skill
- `references/cross-platform-firewall-threads.md` — Platform-specific firewall backends, thread pool config for 24-core CPUs, AhoCorasick API migration, Hickory DNS rename, SvelteKit + Tailwind v4 compatibility notes.
- `references/rust-build-patterns.md` — Rust crate selection and build config patterns.
