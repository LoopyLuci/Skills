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

- **Two-lock deadlock risk**: When using `Arc<Mutex<...>>` with PyO3, acquire locks in consistent order (state first, then pid). If reversed in different methods, deadlock under concurrent Python ↔ Rust calls.
- **File-lock single-instance**: Named mutex (`Global\VM-Harness-GUI`) fails in frozen EXE (temp dir locked by first instance). Use file-based `LOCALAPPDATA` lock with `os.path.exists` + `os.getpid()` check instead — auto-cleans stale locks.
- **Frozen EXE exit 127 (missing python311.dll and .pyd)**: When launching a rebuilt `VM-Harness.exe`, exit code 127 (`command not found`) occurs because the frozen build's `python311.dll` and `vmharness_supervisor.pyd` are not copied into `dist/VM-Harness/_internal/`. After any PyInstaller rebuild, verify the `.pyd` exists in both `target/release/` and the frozen `_internal/`, and that `python311.dll` is present at `dist/VM-Harness/python311.dll`. Also verify `widgets.py` has the graceful matplotlib fallback embedded before rebuild.
- **WASM/telemetry/crypto crate build issues**: The `telemetry` and `crypto` crates use `pyo3` 0.29 which requires `edition = "2021"`. The `supervisor` crate builds cleanly but the additional crates may fail due to minor API differences (e.g., `PyDict::new`, `Bound<'_, PyModule>` init). Build only the `supervisor` crate first (`-p vmharness-supervisor`) before attempting the full workspace build.
- **Single-click tray behavior**: On Windows, `QSystemTrayIcon.setContextMenu()` causes `Trigger` signal on single-click. The handler must explicitly ignore `reason != DoubleClick`; never call `_restore_from_tray()` for `Trigger`/`Context`.
- **Subprocess console suppression**: All Python `subprocess.Popen` calls must include `creationflags=CREATE_NO_WINDOW` (0x08000000) and `startupinfo.dwFlags |= STARTF_USESHOWWINDOW`. Without this, GUI appears with a black console window.
- **Matplotlib graceful fallback in frozen builds**: `TelemetryChart` must wrap all `matplotlib.figure.Figure` and `FigureCanvasQTAgg` usage in `try/except`. When matplotlib is missing from a frozen PyInstaller bundle (common), the widget must show a placeholder label (`label.setStyleSheet("color: #64748b;")`) instead of raising `ModuleNotFoundError`. The `update_data()`, `clear()`, `set_color()`, and `export_to_png()` methods must all check `getattr(self, '_matplotlib_available', True)` before accessing `_line`, `_ax`, `self.figure`, or `self.canvas`. This was the root cause of the `ModuleNotFoundError: matplotlib` crash at `gui/widgets.py:647`.
- **NSIS onedir layout**: PyInstaller `--onedir` creates `VM-Harness/` subfolder with `_internal/`. The NSIS `File` directive must use `/r` to include the full directory tree. `File /r "dist\VM-Harness\*.*"`.
- **Build verification always**: After any Rust change, run `cargo build --release` then verify `.pyd` loads with Python (`import`, `start()`, `state()`). Never assume the build produces a valid module.

## References

- `rust-native-development/references/pyo3-python-bridge.md` — verified build commands and PyO3 0.29 API changes.
- `web/src/types.ts` — TypeScript types mirroring Python `VmConfig`/`VmMetrics`.
- `gui/web_bridge.py` — QWebChannel integration.
- `crates/supervisor/src/lib.rs` — verified working Rust module.
