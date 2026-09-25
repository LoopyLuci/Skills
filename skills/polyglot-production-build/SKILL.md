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
- `.pyd` + `python311.dll` embedded in frozen `_internal/`; verify `.pyd` exists after rebuild.
- Frozen EXE loader (exit 127) is loader issue, not `.pyd` error — verify `.pyd` with `.venv` Python first (direct import `spec_from_file_location`).
- `.proto` files are real source of truth — create 5 files before claiming protocol complete.
- Web bridge (`WebBridgeEngine`) needs `.setParent(self)` before frozen embed.

## Procedure

1. Foundation crates: `/crates/<mod>` (core/types, state/event log, hypervisor trait, crypto/blake3+ed25519, protocol/proto/*.proto, supervisor `.pyd`).
2. Protocol: 5 `.proto` files (`vm.proto`, `telemetry.proto`, `lifecycle.proto`, `pairing.proto`, `chat.proto`).
3. Python graceful fallback: `gui/widgets.py` `try/except`; verify `_matplotlib_available` references.
4. `.pyd` build: `cargo build --release -p vmharness-supervisor`; copy `.pyd` → frozen `_internal/`.
5. `.pyd` import verification (`.venv` Python): direct import (`spec_from_file_location`); `.start()` → `"started"`; `.state()` → `"running"`; `.stop()` → `"stopped"`.
6. Web bridge embedding: verify 2 references in rebuilt frozen EXE (`WebBridgeEngine` + `.setParent`).
7. Full rebuild: `pyinstaller --clean --noconfirm ... --add-data ".pyd;_internal" --add-data "python311.dll;." --add-data "gui;gui" --hidden-import PyQt5 ...`; verify `.exe` timestamp > `gui/main_window.py` fix.
8. End-to-end script: maintain `scripts/e2e_polylot_test.sh` (Python env, `.pyd` direct import, TypeScript 6 files, `.proto` count, frozen artifacts, web bridge, NSIS, signing key).
9. Production docs: `docs/BUILD_PLAN.md` with 6 phases, 7 durability pillars (Zero-dep core, Protocol schema, Deterministic state, Post-quantum crypto, Swappable hypervisor, Self-updating, Observable/auditable).

## Pitfalls (rule + why mechanism, imperative)

- Frozen loader exit 127: loader resolves `python311.dll` differently than `.venv`. Verify `.pyd` independently before declaring `.pyd` broken (`ls` shows 152KB; direct import works; `start()` → `started` in `.venv`).
- Never claim `.start()` passes when `sys.path.insert` fails; the loader issue masks `.pyd` validity. Always verify with direct import.
- `.proto` files must exist (count = 5); empty `proto/` directories are missing.
- Web bridge without `.setParent` produces 0 frozen references (before fix); after fix = 2. Lifecycle depends on parent widget assignment.
- Graceful fallback references: `gui/widgets.py` has `_matplotlib_available` (5 before frozen); frozen build embeds 2. `.venv` passes regardless; frozen loader depends on `python311.dll` resolution, not the fallback code.
- Build verification: every session requires `BUILD_PLAN.md` + `.proto` count (5) + `.pyd` rebuilt + web bridge (2) + `.proto` verified before reporting complete.

## References

- `references/polyglot-build-checklist.md`: Per-layer verification (python_env, rust_pyd, typescript, protocol_proto, frozen_exe, gui_fix, end_to_end, production_docs).
