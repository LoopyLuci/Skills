---
name: rust-closure-typescript-integration
description: "Integrate Rust, Closure, WASM and TypeScript."
---

# Rust + Closure + ClosureWASM + TypeScript Integration

Use when building desktop apps that combine a Python GUI (PyQt5) with Rust native modules, a TypeScript web frontend, WASM telemetry/crypto modules, and Google Closure optimization.

## Architecture Reference

```
Python GUI (PyQt5)  →  QWebChannel  →  TypeScript Web (webpack+closure)
                                      ↓ (wasm-bindgen)
                                 Rust WASM (telemetry, crypto)
                                      ↓
                                 Rust Native (.pyd via PyO3)
                                      ↓
                              QEMU supervisor, SSH, disk I/O
```

## Procedure

### 1. Rust Workspace Setup
See `rust-native-development` skill reference `references/pyo3-python-bridge.md` for verified Cargo.toml settings.

- Workspace: `Cargo.toml` with `edition = "2021"`, `resolver = "2"`
- Crate: `edition = "2021"` (explicit), `crate-type = ["cdylib"]`
- PyO3 0.29: init uses `Bound<'_, PyModule>`; methods use `#[pymethods]`

### 2. TypeScript + Web Build
`web/package.json`: `typescript`, `webpack`, `ts-loader`, `closure-compiler` as dev dependency.
Build: `npm run build:closure` (calls `python tools/build_web.py` which runs Google Closure Compiler ADVANCED).

### 3. WASM Module (telemetry / crypto)
`wasm/telemetry/Cargo.toml`: `crate-type = ["cdylib"]`, uses `wasm-bindgen` + `js-sys`.
Build: `wasm-pack build --target web --release` produces `.js` + `.wasm`.
Web loads via `<script src="wasm/telemetry/vmharness_telemetry.js">`.

### 4. Python ↔ JS ↔ WASM Bridge
`gui/web_bridge.py`: `QWebChannel` + `QWebEnginePage`.
Register `VmHarnessBridge` object, inject `qtwebchannel.js`, load `index.html`.

### 5. Closure Optimization
`tools/build_web.py` runs `java -jar closure-compiler.jar --compilation_level ADVANCED`. Output is minified + dead-code-eliminated.

## Key Pitfalls

- **PyO3 edition**: `edition.workspace = true` is not always sufficient; set `edition = "2021"` explicitly in each crate `Cargo.toml`.
- **Async + block_on**: Do NOT use `async { ... }.await` inside `.block_on()` closures. Call `.start_async()` or `.stop_async()` directly.
- **TypeScript module resolution**: TypeScript uses CommonJS (`require`) for QWebChannel; ESM (`import`) requires `esModuleInterop` enabled and may break `webpack` bundler.
- **WASM + QWebEngine**: WASM modules load asynchronously; the web page must wait for `vmharness-ready` event before calling `VmHarnessBridge.getMetrics()`.

## References

- `rust-native-development/references/pyo3-python-bridge.md` — verified build commands and PyO3 0.29 API changes.
- `web/src/types.ts` — TypeScript types mirroring Python `VmConfig`/`VmMetrics`.
- `gui/web_bridge.py` — QWebChannel integration.
- `crates/supervisor/src/lib.rs` — verified working Rust module.
