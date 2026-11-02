# Browzeit Phase Plan

## Phases Overview

### Phase 1: Core (Parser, DOM, CSS)
- `crates/traits/Cargo.toml` — Parser trait definition
- `crates/types/Cargo.toml` — DOM types (Node, Element, Text, Comment)
- `crates/core/src/parser.rs` — HTML5 tokenizer + tree builder
- `crates/core/src/style.rs` — CSS cascade
- Tests in `crates/core/tests/`

### Phase 2: Network
- `crates/network/Cargo.toml` — HttpClient, cookies, cache
- HTTP/HTTPS via rustls (optional hyper)

### Phase 3: Layout/Engine
- `crates/engine/Cargo.toml`
- Box model, flex/grid layout

### Phase 4: Renderer
- `crates/renderer/Cargo.toml` — paint, compositing

### Phase 5: Agent
- `crates/engine/src/agent.rs` — autonomous actions

### Phase 6: Driver
- `crates/driver/Cargo.toml` — BrowserWindow, pywebview shell

### Phase 7: Generative UI
- `crates/engine/src/agent.rs` — add_button, change_layout, theme

## Crate Dependency Graph
```
driver (Phase 6)
  ↕
renderer (Phase 4)
  ↕
engine (Phase 3) ← agent (Phase 5)
  ↕
core (Phase 1: parser, DOM, CSS)
  ↕
network (Phase 2)
  ↕
types (Phase 1: dom types)
  ↕
traits (Parser trait)
```

## Verification Gates
- `cargo check --workspace` — full workspace green
- `cargo test -p browzeit-core --test sanity` — parser sanity test
- All crates compile cleanly (0 errors, 0 warnings preferred)

## Workspace Layout
```
X:\Projects\Browzeit\browzeit\
├── Cargo.toml
├── crates\
│   ├── core\
│   │   ├── src\
│   │   │   ├── parser.rs
│   │   │   ├── style.rs
│   │   │   └── lib.rs
│   │   └── tests\
│   │       └── sanity.rs
│   ├── driver\
│   ├── engine\
│   ├── network\
│   ├── renderer\
│   ├── traits\
│   └── types
└── references/
    └── phase-plan.md
```
