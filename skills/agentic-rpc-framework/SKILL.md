---
name: agentic-rpc-framework
description: Build agentic RPC framework with green verification gate.
category: software-development
version: 1.1.0
author: Nous Research
license: MIT
metadata:
  hermes:
    tags: [agentic, rpc, rust]
    related_skills: [windows-rust-android-build-env]
---

# Agentic RPC framework

Build a persistent, query-driven Rust daemon exposing a `DaemonService` trait, a line-based JSON transport, and bindings that all speak the trait over that transport — CLI, API, MCP, ACP — then verify with a green build/fmt/clippy/test gate before claiming anything done.

## When to use

- Designing or extending the agentic RPC framework (daemon, transport, bindings, protocol).
- Adding a new binding (HTTP, MCP, ACP) on top of the existing line-based JSON protocol.

## Always-on rules

1. **X: drive enforced.** All paths, env vars, builds, toolchains on X:. `CARGO_TARGET_DIR=X:/cargo-target` and `RUSTUP_HOME=X:/Dev/rustup`. C: stays at 90% full / unused.
2. **Never stub.** Full implementation, working artifacts. A crate not exercised end-to-end is not done; a command not reachable is not done.
3. **Verification-first.** `cargo fmt --all -- --check` -> FMT_OK; `cargo clippy --workspace --all-targets -- -D warnings` -> 0 errors; `cargo test --workspace` -> green, before any claim of completion.
4. **One JSON per line, one response per line.** The line-based JSON protocol is the wire that CLI, API, MCP, and ACP all build on.
5. **No credentials.** Secrets are never preserved; replace them with `[REDACTED]`.
6. **Rust module resolution.** `pub mod foo;` resolves `foo.rs` BEFORE `foo/mod.rs` (the `/lib.rs` path is crate-root-only, never a submodule). A `foo.rs` stub silently shadows `foo/mod.rs`; before believing any "verified" claim, verify with `find crates/<crate>/src/<module>/` that the real module compiles — a stub plus one skeleton test is not verification. This caught a fake S1 spike where the real engine implementation was permanently shadowed.
7. **`write_file` stale-view guard.** `write_file` refuses to overwrite a file it last read via offset/limit (a "partial view"). Bypass by `rm` then `write_file` — the delete satisfies the guard.
8. **Feature-pin typo loop.** The salsa feature pin is `salsa`, NOT `salpa`. Always verify with `--list` that the real `salsa_engine` tests appear; use variable-based invocation `F=salsa; cargo test -p rpc-core --features "$F"`.
9. **`cargo rustc --print=cfg` is unsupported.** This cargo version rejects `cargo rustc --print=cfg` (invalid value / unexpected argument). To confirm feature activation, use `cargo metadata --no-deps`.

## Procedure

1. **Scaffold the workspace.** Workspace manifest with explicit `members` list; `[workspace.package]` for shared metadata; serde pinned `default-features = false, features = ["derive", "std"]`. All 12 crates in `members`.
2. **Core domain + engine trait.** `rpc-core`: `IncrementalEngine` trait (`apply_changes`, `query`, `cancel`) plus the `Query`/`QueryResult` wire domain (`DaemonHealth`, `CapabilitySet`, `Revision`). Use `MockEngine` as the reference implementation; gate the real engine adapter behind an opt-in feature (e.g. `salsa`).
3. **Production engine backend (external IDE-analysis library).** The real-time engine wraps a third-party IDE-analysis library (e.g. `ra_ap_ide`/parser + `ra_ap_ide_diagnostics`) behind the `IncrementalEngine` trait, so CLI/API/MCP/ACP bindings are unchanged. The wrapper owns an `AnalysisHost` (interior-mutated via `Mutex`) plus a tracked file set. `apply_changes` updates the tracked set and bumps a revision; `query(Diagnose(path))` rebuilds the ra_ap world for that path and maps the ra_ap diagnostics into the wire `rpc_diagnostics::Diagnostic` domain. Keep the wrapper behind an opt-in feature (e.g. `salsa`) so the default build stays light. **Version-sensitive gotchas (from the S1 spike):** read the INSTALLED crate source before writing — `AbsPathBuf` is in `ra_ap_paths`, `AnalysisHost` is in `ra_ap_ide`, `full_diagnostics` is a method on `Analysis` (3 args), `Diagnostic` has a `code: DiagnosticCode` (call `as_str()`), `Severity`/`AssistResolveStrategy` are in `ra_ap_ide_db`, `DiagnosticsConfig::test_sample()` builds a valid config, and `proc_macro_cwd` must use `triomphe::Arc` (not `std::sync::Arc`) over an ABSOLUTE path — on Windows `AbsPathBuf::try_from("/")` panics because `Path::is_absolute()` rejects a bare `/` (current-drive root, not drive-anchored); pass a drive-anchored path like `"X:/"` or `"C:/"`. See `references/ra-ap-lib.md` for the wiring recipe and the corrected API surface.
4. **Daemon as a library.** `rpc-daemon` is a LIBRARY exposing `DaemonService` trait (`Daemon`, `ToolRegistry`, `EngineHandle`, `LocalDaemon`). `main.rs` is only entry points: `--one-shot CMD` and `--listen <addr>`.
4. **Transport.** Line-based JSON (`one req per line`, one JSON resp per line). Newlines are mandatory on both ends (see pitfall: newline requirement).
5. **Bindings.** `rpc-cli` (TCP/stdio/self-test), `rpc-api` (in-process), then `rpc-mcp`/`rpc-acp` (translate the same trait to MCP tools / ACP proposals). Every binding uses the `DaemonService` trait, never the concrete `Daemon`.
6. **Run the F1 gate.** Build, fmt, clippy, test. Green = done.

- **Query double-tag serde bug.** `Query { kind: QueryKind }` where `QueryKind` is `#[serde(tag="kind")]` serializes the tag twice (`{"kind":{"kind":"diagnose",...}}`), so JSON `{"kind":"diagnose","path":...}` fails to deserialize with `invalid type: string "diagnose", expected internally tagged enum`. Fix: `#[serde(flatten)]` the `kind` field so the wire format is the clean `"{\"kind\":\"diagnose\",\"path\":...}` — round-trip it through a serde_json test in the self-test.
- **Transport: newline requirement.** The transport reads one JSON line at a time (`read_line`). A client that `write_all`s the request bytes without a trailing `\n` hangs forever in `read_line` — the daemon never responds and the client blocks up to the terminal timeout. Always send `\n` after the request line.
- **Daemon accept loop must not exit.** `serve` that accepts once and returns exits the process, killing the transport thread. Use a `loop { accept() }` so the daemon keeps serving; each connection runs in its own thread.
- **Rebuild while the daemon is running -> Access is denied.** Windows refuses to overwrite an executing binary. Kill the running daemon (`taskkill /F /IM rpc-daemon.exe`) before `cargo build`. Verify no daemon remains before rebuilding.
- **Dispatch must cover every op.** The transport's `dispatch` is a `match op`; an op not listed returns silently as `unknown operation`. Add the arm rather than assuming the CLI covers it.
- **Bind-address discovery.** `--listen 0` picks a random port. The log must print the bound `local_addr()` (after binding), not the pre-bound address, so clients know the real port.
- **Tool surface must be wired three ways.** `tools`/`capabilities` commands must be wired into the `DaemonService` trait, the transport dispatch, AND the CLI `build_req`/`dispatch`. One side missing and the command is invisible to that terminal.
- **Tool path format.** CLI apply flags are `--path=...` / `--content=...` (equals, no spaces). `build_req` parses via `starts_with("--path=")`; spacing-separated flags fail with exit 2.
- **External engine rebuild-per-query perf.** Wrapping a third-party IDE-analysis library behind `IncrementalEngine` by rebuilding the whole `AnalysisHost` world on every `query` is *correct but slow* (full parse + HIR each time, typically far above 100ms). It is the right *prototype* shape and the right *fallback* for a daemon with no incremental plan — but it must be replaced before the daemon is used for latency. Do not claim the sub-100ms promise on this shape; mark it explicitly as "correct, not yet fast".

- **Subsecond ThinLink (S3).** Not standalone; embedded in `dioxus-cli` (`dx serve --hotpatch`). See `references/subsecond-thinlink.md`.
- **Salsa persistence (S2).** Feature `persistence` (`v0.28.5`, MSRV 1.88). See `references/salsa-persistence.md`.
- **Recursive `Deserialize` (F2).** `Change` embeds `Vec<Change>`; derive fails. Always parse manually in transport.
- **Library `ra_ap_*` (S1).** `v0.0.358` (MSRV 1.98.0) is linkable, but the crate API shifts between point releases — inspect the INSTALLED crate source rather than trusting stale docs. Keys you will trip on: (1) `AbsPathBuf` is in `ra_ap_paths` (NOT `ra_ap_cfg`); (2) `AnalysisHost` is in `ra_ap_ide` (NOT `ra_ap_ide_db`); (3) `full_diagnostics` is a METHOD on `Analysis` (`analysis.full_diagnostics(&config, resolve, file_id) -> Cancellable<Vec<Diagnostic>>`, Cancellable = `Result<T, Cancelled>`), NOT a free fn — the free fn takes 4 args (`db, &config, resolve, file_id`); (4) `Diagnostic` fields are `code: DiagnosticCode, message: String, range: FileRange, severity: Severity, unused, experimental, fixes: Option<Vec<Assist>>, main_node` — `code` is a `DiagnosticCode` (call `.as_str()`, not `.map()`), `range` is ONE `FileRange` (with `.range.range` = `TextRange`); (5) `Severity` (Error/Warning/WeakWarning/Allow) is in `ra_ap_ide_db` and `AssistResolveStrategy` in `ra_ap_ide_db::assists`; (6) `DiagnosticsConfig::test_sample()` builds a valid config. Version coordination is also required (`triomphe` 0.1.17 matching ra_ap_ide's dependency). Use the salsa feature pin `salsa` (never `salpa`); verify with `F=salsa; cargo test -p rpc-core --features "$F"`.
## Verification gate (F1)

Run in order; stop on first failure:

1. `cargo build --workspace --all-targets` -> exit 0
2. `cargo fmt --all -- --check` -> FMT_OK
3. `cargo clippy --workspace --all-targets -- -D warnings` -> 0 errors
4. `cargo test --workspace` -> all crates green (including `rpc-cli` self-test, `rpc-api` doctest)

**Note:** `cargo rustc --print=cfg` is NOT supported by this cargo version (rejected). To confirm feature activation, use `cargo metadata --no-deps`.
\n
- **Subsecond ThinLink (S3 spike).** Not a standalone crate; embedded in `dioxus-cli` (`dx serve --hotpatch`). See `references/subsecond-thinlink.md`. Daemon-side hot-patching must shell out to `dx` CLI or replicate embedded ThinLink manually.
- **Salsa persistence (S2 spike).** Feature `persistence` (v0.28.5, MSRV 1.88). See `references/salsa-persistence.md` for `tests/persistence.rs` API (`#[salsa::input(persist)]`, `as_serialize`, `Database::deserialize`).
- **Recursive `Deserialize` failure (F2 fix).** `Change` embeds `Vec<Change>`; deriving `Deserialize` fails. Always parse recursively-structured wire types manually in `transport::run` (manual `ChangePack` construction), not via derive macros.
- **Library `ra_ap_*` feasibility (S1 spike).** `v0.0.358` (MSRV 1.98.0) linkable; version coordination required. See `references/ra-ap-lib.md`. **Note:** `docs/ENGINE.md` still shows the pre-fix `proc_macro_cwd = AbsPathBuf::try_from("/")` — that example fails on Windows (rejected by `Path::is_absolute()`); the working source uses a drive-anchored path (`"X:/"` or `"C:/"`).
- **Public repo location.** The public repo is `https://github.com/LoopyLuci/rust-rtpc` (not `nousresearch`). The `repository` field in `Cargo.toml` must match the actual remote.
- **Purpose-built ML model sizing.** When designing AI/ML components for this framework, every model must: (1) run on bare CPU (no GPU dependency); (2) improve performance/effectiveness more than the resources it consumes (measure ROI: latency removed vs latency added); (3) be sized specifically for the task (tiny NNs ~1–3 M params, trees/linear ~sub-ms). GPU acceleration (CUDA/ROCm EP) is optional; CPU EP is the floor. See `docs/ML-DESIGN.md` for the full catalog and sizing table.

### References
- `references/f1-gate.md` — verification gate procedure.
- `references/subsecond-thinlink.md` — S3 spike: subsecond runtime + ThinLink embedded in `dx`.
- `references/salsa-persistence.md` — S2 spike: salsa v0.28.5 persistence feature (`tests/persistence.rs`).
- `references/ra-ap-lib.md` — S1 spike: `ra_ap_*` library consumption (`v0.0.360` / `v0.0.358`, MSRV 1.98.0).
- `references/ml-design.md` — CPU-first ML model sizing table + ROI rules (`docs/ML-DESIGN.md` full catalog: 11 models, each with concrete param count, CPU latency, RAM, and gain:cst).
