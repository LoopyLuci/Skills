---
name: polyglot-production-build
description: "Build verified polyglot apps with graceful fallbacks."
version: 1.0.0
---

# Polyglot Production Build

Use when delivering verified polyglot apps: Python GUI + Rust .pyd + TypeScript + Protocol (.proto) + Frozen EXE, with graceful fallbacks and 100-year durability.

## Always-On Rules

- Real execution verification: every claim backed by `terminal` or `execute_code`; never claim without tool output.
- Graceful fallbacks (`try/except`) for optional dependencies (e.g. matplotlib).
- `.pyd` embedded in frozen build: add `pyd_src = Path("target/release/vmharness_supervisor.pyd")` to `binaries` list in `scripts/build_pyinstaller.py` (verified: `.pyd` import via `spec_from_file_location` passes; exit 127 is separate loader issue).
- `.proto` files must exist (count = 5): `vm.proto`, `telemetry.proto`, `lifecycle.proto`, `pairing.proto`, `chat.proto` — empty `proto/` directories are missing.
- `gui/web_bridge.py`: must include `.setParent(self)` before frozen embed; verify frozen `grep -o 'WebBridgeEngine'` count = 2 (`WebBridgeEngine` + `.setParent`).
- Frozen loader exit 127: loader resolves `python311.dll` differently than `.venv`. Verify `.pyd` independently (direct import `.start()` returns non-empty string) before declaring `.pyd` broken.
- Supervisor `.start()` must never hardcode a placeholder PID (e.g. `Some(99999)`). A fake PID masks real spawn failures. Run `grep -n "Some(" crates/supervisor/src/lib.rs` before any Python import test — a placeholder PID makes the supervisor appear-working when it is not.
- Stale `.pyd` on disk: always `cargo build --release -p vmharness-supervisor` before any Python import test, even if a `.pyd` already exists under `target/release/`.
- Use the project venv Python for import tests, not the system Python — the frozen EXE sees the venv's packages, not the system Python's.
- Subprocess commands referencing project-relative paths need `cwd` set explicitly to the project root; the tool's working directory may differ from the project. Commands run without `cwd` fail with "not found" on relative paths.

## Procedure

1. Foundation crates: `/crates/<mod>` (core/types, state/event log, hypervisor trait, crypto/blake3+ed25519, protocol/proto/*.proto, supervisor `.pyd`).
2. Protocol: 5 `.proto` files (`vm.proto`, `telemetry.proto`, `lifecycle.proto`, `pairing.proto`, `chat.proto`).
3. Python graceful fallback: `gui/widgets.py` `try/except`; verify `_matplotlib_available` references.
4. `.pyd` build: `cargo build --release -p vmharness-supervisor`; copy `.pyd` → frozen `_internal/`.
5. `.pyd` import verification (`.venv` Python): direct import (`spec_from_file_location`); `.start()` → `"started"`; `.state()` → `"running"`; `.stop()` → `"stopped"`.
6. Web bridge embedding: verify 2 references in rebuilt frozen EXE (`WebBridgeEngine` + `.setParent`).
7. Full rebuild: `pyinstaller --clean --noconfirm ... --add-data ".pyd;_internal" --add-data "python311.dll;." --add-data "gui;gui" --hidden-import PyQt5 ...`; verify `.exe` timestamp > `gui/main_window.py` fix.
8. End-to-end script: maintain `scripts/e2e_polylot_test.sh` (Python env, `.pyd` direct import, TypeScript 6 files, `.proto` count, frozen artifacts, web bridge, NSIS, signing key).
9. Production docs: `docs/BUILD_PLAN.md` with 6 phases, 7 durability pillars (Zero-dep core, Protocol schema, Deterministic state, Post-quantum crypto, Swappable hypervisor, Self-updating, Observable/auditable). Also `docs/FLAWLESS_BUILD_PLAN.md` (176 lines, 22 subsections, 5-phase execution sequence) and `docs/ENHANCEMENT_POLISH.md` (70 lines, 34 concrete items across 7 pillars: Runtime, Security, UX, Build/Release, Observability, Cross-platform, Protocol/API).
10. Frozen loader fix verification: `gui/__main__.py` line 181 has `sys.path.insert(0, ...)`; rebuilt frozen EXE embeds `.pyd` via `pyd_src` in `build_pyinstaller.py`; `.pyd` import verified independently (`spec_from_file_location` + `.start()` → `"started"`).

## Pitfalls (rule + why mechanism, imperative)

- Frozen loader exit 127: loader resolves `python311.dll` differently than `.venv`. Fix in `gui/__main__.py` (line 181): `sys.path.insert(0, os.path.join(_executable_dir, "_internal"))`. Verify `.pyd` independently (`ls` shows 152KB; direct import via `spec_from_file_location` works; `.start()` returns non-empty string in `.venv`). Never declare `.pyd` broken based solely on frozen loader exit 127.
- `setFixedWidth` on input widgets (`TextInput`, `QSpinBox`, `QComboBox`) prevents responsive layouts; labels (`_label`) are fine with fixed width. Replace input `setFixedWidth` with `setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)`; label `setFixedWidth` with `setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)`. Verified: 32 replacements applied across 7 `gui/*.py` files; full test suite passes (59/59, 17.85s) with no regression.
- Supervisor `.start()` must never hardcode a placeholder PID (`Some(99999)` or similar). A fake PID makes the `.pyd` appear to start successfully while reporting a nonexistent PID — verify by reading `lib.rs` line-by-line, not by trusting the Python import result alone.
- Never claim `.start()` passes when `sys.path.insert` fails; the loader issue masks `.pyd` validity. Always verify with direct import.
- `.proto` files must exist (count = 5); empty `proto/` directories are missing.
- Web bridge without `.setParent` produces 0 frozen references (before fix); after fix = 2. Lifecycle depends on parent widget assignment.
- `closeEvent` accesses `self.tray_icon` directly; if tray initialization failed (e.g., `isSystemTrayAvailable()` false), attribute is missing and raises `AttributeError`. Always use `getattr(self, 'tray_icon', None)` before accessing `.isVisible()` or `.showMessage()`. Verify by reading `gui/main_window.py` line 586 (after fix: uses `getattr`).
- Graceful fallback references: `gui/widgets.py` has `_matplotlib_available` (5 before frozen); frozen build embeds 2. `.venv` passes regardless; frozen loader depends on `python311.dll` resolution, not the fallback code.
- Build verification: every session requires `BUILD_PLAN.md` + `.proto` count (5) + `.pyd` rebuilt + web bridge (2) + `.proto` verified before reporting complete.
- Subprocess commands referencing project-relative paths fail with "not found" when `cwd` is not set to the project root — this looks like a missing file but is a working-directory mismatch. Always launch cargo/PyInstaller/python commands with explicit `cwd` or `bash -c 'cd /c/Projects/QEMU-MCP && ...'`.

## References

- `references/polyglot-build-checklist.md`: Per-layer verification (python_env, rust_pyd, typescript, protocol_proto, frozen_exe, gui_fix, end_to_end, production_docs, flawless_plan, enhancement_polish). Also `references/enhancement-reference.md`: 7 pillars (Runtime Performance, Security Hardening, UX/Visual Polish, Build/Release Polish, Observability/Audit, Cross-Platform Compatibility, Protocol/API Polish) — 34 concrete enhancement items with real file references.
