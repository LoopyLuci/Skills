---
name: enhancement-reference
---
# Enhancement & Polish Reference (Polyglot Production Build)

This file is referenced by `polyglot-production-build` skill. It captures the 7 pillars and 34 concrete enhancement items verified against real artifacts from the VM-Harness session.

## Verified Artifacts Reference (Real File Paths)

- `.pyd`: `/c/Projects/QEMU-MCP/target/release/vmharness_supervisor.pyd` (152576 bytes)
- `.proto`: `/c/Projects/QEMU-MCP/crates/protocol/proto/*.proto` (count = 5: vm.proto, telemetry.proto, lifecycle.proto, pairing.proto, chat.proto)
- Protocol bindings: `/c/Projects/QEMU-MCP/crates/protocol/src/proto_bindings.py`
- GUI main: `/c/Projects/QEMU-MCP/gui/main_window.py` (WebBridgeEngine, .setParent, loader fix)
- GUI widgets: `/c/Projects/QEMU-MCP/gui/widgets.py` (graceful fallback, 2 frozen refs)
- Build script: `/c/Projects/QEMU-MCP/scripts/build_pyinstaller.py` (pyd_src embedded, 3 refs)
- Frozen loader fix: `/c/Projects/QEMU-MCP/gui/__main__.py` (line 181, sys.path.insert)
- Build docs: `/c/Projects/QEMU-MCP/docs/BUILD_PLAN.md` (1278 lines, 6 phases, 7 durability pillars)
- Flawless build plan: `/c/Projects/QEMU-MCP/docs/FLAWLESS_BUILD_PLAN.md` (176 lines, 5 phases + execution sequence)
- Enhancement polish: `/c/Projects/QEMU-MCP/docs/ENHANCEMENT_POLISH.md` (70 lines, 7 pillars, 34 items)
- E2E script: `/c/Projects/QEMU-MCP/scripts/e2e_polylot_test.sh`
- Signing key: `/c/Projects/QEMU-MCP/.vmharness_signing_key` (32 bytes)

## 7 Pillars (34 Items) — Each Verified with Real References

### 1. Runtime Performance (5)
1. Replace PyQt5 + matplotlib with pure-Rust renderer (egui + skia) — eliminates ~200MB frozen dependency
2. Restore tokio Command spawn with real QEMU binary (currently placeholder PID=99999)
3. Implement ring buffer for metrics (currently Vec, no circular buffer)
4. Add tokio async adapter for QMP TCP (verified missing in supervisor/lib.rs before fix)
5. Memory stability: verify no leaks in `tests/test_performance.py` (memory growth < 50MB after 1000 resize cycles)

### 2. Security Hardening (5)
6. Post-quantum crypto: implement Dilithium trait variant (`crypto/` scaffolded, not implemented)
7. Audit log chain: hash-chain BLAKE3 (`.audit/audit.db` exists; chain not verified)
8. Key rotation: `.vmharness_signing_key` (32 bytes Ed25519); `.proto` pairing defines rotation protocol; rotation endpoint not implemented
9. Sandbox: add seccomp-bpf filter for QEMU child process (not implemented)
10. TLS: implement mutual TLS for QMP (`cert.pem` + `key.pem` exist; TLS not enabled; `headless_server.py` line 340 has `port 8443` with HTTP only)

### 3. UX / Visual Polish (5)
11. Theme runtime switching: `gui/theme.py` (580 lines, 6 themes specified: Dark/Light/Midnight/Forest/Sunset/Ocean); verify switching works
12. Tray tooltip: `QSystemTrayIcon` verified (purple "V"); add state tooltip (running/stopped/crashed)
13. Resize grip: 8 invisible zones (20px) at corners + edges verified; bottom-right grip visible + draggable
14. Multi-monitor: `QWebEngineView` position verified; `gui/web_bridge.py` exists; `WebBridgeEngine` embedded (2 refs)
15. Accessibility: screen-reader labels for 34 panels (`tests/test_gui.py` asserts 34; labels not verified)

### 4. Build / Release Polish (5)
16. Frozen loader: `.pyd` embedded (verified); `.proto` count verified (5); loader fix (`sys.path.insert`) verified (line 181); exit 127 remains loader issue (documented, not `.pyd` error)
17. NSIS installer: `.pyd` included; `.exe` rebuilt; silent install flag (`/VERYSILENT`) not implemented
18. Code signing: `.vmharness_signing_key` verified; `signtool` not executed; no signed binary verified
19. Universal binary: macOS universal binary (`x86_64` + `aarch64`) not built; Linux musl static binary (`musl` target) not compiled
20. Self-updating: `crates/update/` scaffolded; dual-slot logic (`Slot A` + `Slot B` + atomic symlink swap + rollback) not implemented; rollback test (`3 crash` loop) not executed

### 5. Observability / Audit Polish (5)
21. Structured tracing: `tracing` crate referenced (workspace); subscriber not configured; no `tracing-subscriber` initialization
22. Metrics endpoint: `.proto` telemetry message defined; Prometheus HTTP endpoint not implemented
23. Crash reporting: `gui/__main__.py` crash-proof entry verified (mutex + atexit); crash dump file generation (not `.log`) missing
24. Health checks: `/health` endpoint for MCP server (`build_server()` exists) not verified; `server.add_tool()` calls verified (lines 97, 104, 127)
25. Log rotation: `loguru` referenced; rotation config (`rotate` + `retention`) not verified

### 6. Cross-Platform / Compatibility Polish (5)
26. Windows frozen loader: `.pyd` import verified independently; frozen EXE loader requires `sys.path.insert` fix; exit 127 is loader resolution issue (verified with direct import pattern)
27. Linux musl: `CARGO.toml` workspace includes `edition = "2024"`; `profile.release` has `panic = "abort"`; musl target not compiled (`rust-closure-typescript-integration` skill covers cross-platform)
28. macOS universal binary: no universal binary (`x86_64-apple-darwin` + `aarch64-apple-darwin`) verified; `.pyd` is Windows-specific (`.so` needed for macOS); `crates/supervisor` uses `edition = "2021"` (compatible with both)
29. Android pairing: `.proto` pairing message (`GenerateTokenRequest`/`Response`) verified; ADB path (`ADB_PATH` from `.env`) referenced; pairing token (`.vmharness_signing_key` signed) not fully verified end-to-end (requires running device connection)
30. WebAssembly (`WASM`): `wasm/telemetry/Cargo.toml` exists; `crates/supervisor/src/lib.rs` uses `pyo3` with `edition = "2021"`; WASM compilation (`cargo build --target wasm32-unknown-unknown`) not verified; `telemetry` ring buffer (TypeScript) verified present (`telemetry/RingBuffer.ts`); WASM module integration (`WasmModule`) not verified

### 7. Protocol / API Polish (4)
31. gRPC server: `.proto` service definitions verified (`lifecycle.proto` `VmLifecycle` service); Python grpc server (`grpc` package) not implemented; `mcp.server` uses `add_tool()` not grpc
32. JSON-RPC fallback: no JSON-RPC endpoint (`/jsonrpc`) exists; clients must use protobuf or direct `.pyd` import
33. Protocol version negotiation: `version.rs` defines `compatible()` (major == other.major); version negotiation (handshake + fallback to older protocol) not implemented (`start()` returns `"started"` without version check)
34. Schema registry: no `.proto` schema registry file or `.json` schema version tracking; `.proto` version is `syntax = "proto3"` with hardcoded package `vmharness.v1`

## Verification Commands Per Item (Every Enhancement)
Every item above is backed by a verified file reference (see Artifacts Reference). To re-verify any item: use `ls`, `grep`, `find`, or `cat` on the referenced file; never rely on memory.

## Build Sequence (Verified Steps — All Must Pass Before Reporting Complete)
The sequence is maintained in `docs/FLAWLESS_BUILD_PLAN.md` (176 lines):
1. Foundation crates → 2. Protocol → 3. Python graceful fallback → 4. `.pyd` build → 5. `.pyd` import verification → 6. Web bridge embedding → 7. Full rebuild → 8. E2E test → 9. Production docs (6 phases + 34 enhancements + flawless build plan) → 10. Frozen loader fix (`sys.path.insert` at line 181 of `__main__.py`)

Every claim references a real file line, count, or execution result — never memory or assumption.
