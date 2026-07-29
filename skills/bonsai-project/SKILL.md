---
name: bonsai-project
description: "Use when working on Project Bonsai or its components."
---

# Project Bonsai

**Location**: `D:\Projects\Bonsai\`
**Test Model**: `X:\models\Bonsai-1.7B-Q2_K\Bonsai-1.7B-Q2_K.gguf` (Qwen3 1.7B, Q2_K, GGUF v3)

## Components

### 1. Rust Inference Engine (`engines/bonsai-engine/`)
- Custom GGUF parser (v3 with u64 offset per tensor info entry)
- Q2_K, Q8_0, Q4_0, F32 quant support
- Pure Rust — zero external deps
- Build: `cargo build --release`
- Run: `./target/release/bonsai-engine.exe "<model.gguf>" --info`

### 2. Python Bridge (`bridges/bonsai-bridge/`)
- Pure Python GGUFReader + FastAPI server (port 8888)
- Install: `pip install -e D:\Projects\Bonsai\bridges\bonsai-bridge\`
- Run: `python -m bonsai_bridge.server --model "<model.gguf>" --port 8888`

### 3. Clojure Orchestra (`orchestra/bonsai-orchestra/`)
- Agent coordination, MCP client/server
- Run: `cd orchestra/bonsai-orchestra && clojure -M -m bonsai.orchestra`

### 4. Svelte Frontend (`ui/bonsai-ui/`)
- Svelte 5 + Vite + TS, retro punk theme (pink/green/purple)
- Pages: Chat, Models, Settings, MCP Status
- Dev: `cd ui/bonsai-ui && npm run dev`

### 5. Tauri Desktop (`desktop/bonsai-desktop/`)
- Native window + system tray + auto-starts Python backend

## API Endpoints
- `GET /api/status` — server+model status
- `POST /api/chat` — generate response
- `GET /mcp/tools` / `POST /mcp/execute` — MCP protocol

## GGUF v3 Key Detail
GGUF v3 adds a `uint64_t offset` field AFTER `uint32_t quant_type` in each tensor info entry. Without this, the parser desyncs.

## Current Status
Engine parses GGUF, provides tensor metadata, CLI info dump. Full transformer forward pass (Q2_K dequant → matmul → attention) is scaffolded. Server runs with pure-Python GGUF reader, returns model info/status. Ready for the inference kernel implementation.
