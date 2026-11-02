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
- **Full implementation never stubs**: every phase ships real code, not placeholders
- **Zero tolerance for compile errors**: rustc/cargo check must pass before moving on
- **Codebase toolchain on X: never C:**: RUSTUP_HOME=X:/Dev/rustup, CARGO_HOME=/x/Dev/cargo, CARGO_TARGET_DIR=/x/Dev/cargo-target
- **Desktop GUI = pywebview/Tauri shell, never browser dashboard**: pywebview or Tauri for the native shell
- **Generative UI is a first-class feature**: agent must create/modify/optimize UI in real time (add_button, change_layout, theme)
- **Verification-first**: integration tests in crates/*/tests/, cargo test green before moving on
- **Independent from other browser stacks**: Browzeit builds from scratch, no direct dependencies on other browsers
- **Minimal dependencies**: from-scratch parsers, no WebKit/WebKitGTK dependencies

## Project Context: Browzeit
- **Name**: Browzeit (fully independent browser)
- **Workspace**: X:\Projects\Browzeit\browzeit (Cargo workspace, NOT C: drive)
- **Drives**: X: = junction to Z:/x/, C: at 90% full — NEVER use C:
- **Architecture**: 7-crate Rust workspace: traits, types, core, engine, renderer, network, driver
- **Phases**: 1. Core (parser, DOM, CSS), 2. Network (HTTP, cookies, cache), 3. Layout/Engine, 4. Renderer (graphics), 5. Agent (autonomous), 6. Driver (desktop shell), 7. Generative UI (agent add_button/change_layout/theme)

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

## Build & Verification Commands
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

## Verification-First Workflow
- **Verify after every edit**: run `cargo check --workspace` after any structural change to parser code
- **Zero tolerance for compile errors**: rustc/cargo check must pass before moving to the next phase
- **Fix warnings before proceeding**: cargo warnings (unused variables/fields) block clean verification
- **Full implementation never stubs**: every phase ships real code, not placeholders

## Key Conventions
- **Crate names**: `browzeit-core`, `browzeit-engine`, `browzeit-renderer`, `browzeit-network`, `browzeit-driver`, `browzeit-traits`, `browzeit-types`
- **Dependency pattern**: each crate depends on its neighbors (core ← engine, etc.)
- **Trait pattern**: `browzeit-traits` defines `Parser` trait; `browzeit-core` implements it
- **Drives**: X: = junction to Z:/x/, C: at 90% full
- **Imports**: use `use browzeit_traits::Parser;` for trait imports

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
