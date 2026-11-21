# Rust Workspace Release Verification

Verification gates for a multi-crate Rust workspace that builds a desktop
application with a Python GUI shell. Each gate is a command whose output is
read, not assumed.

## Gate F1 — the release audit

```bash
cd <workspace-root>
export CARGO_HOME=<cargo-home>
export CARGO_TARGET_DIR=<target-dir>

# 1. Compile check (0 errors)
cargo check --workspace 2>&1 | tail -2

# 2. Unit + doc tests (0 failures)
cargo test --workspace 2>&1 | grep -E 'test result' | grep -cE '0 failed'

# 3. Clippy (0 errors, 0 warnings)
cargo clippy --workspace --all-targets 2>&1 | grep -cE '^error'
cargo clippy --workspace --all-targets 2>&1 | grep -cE '^warning'

# 4. Formatting (0 diffs)
cargo fmt --all --check 2>&1 | wc -l

# 5. Release build (successful)
cargo build --release --workspace 2>&1 | tail -1
```

## Rust workspace specifics

### Workspace members

A Rust workspace declares members in the root `Cargo.toml`:

```toml
[workspace]
members = ["crates/traits", "crates/types", "crates/core",
           "crates/engine", "crates/renderer", "crates/network",
           "crates/driver", "crates/api", "custode-browzeit"]
```

All members share `[workspace.package]` metadata (version, edition, license).
Per-crate version overrides are allowed in each crate's own `Cargo.toml`.

### Dependency resolution

Internal crates must reference each other explicitly. A `workspace = true`
dependency in a member's `Cargo.toml` that has no workspace-level member
definition causes:


```bash
eval: line 7: unexpected EOF while looking for matching '``'
```

Fix: convert all internal `workspace = true` dependencies to explicit `path`
references:

```toml
[dependencies]
browzeit-traits = { path = "../traits" }
browzeit-core = { path = "../core" }
browzeit-engine = { path = "../engine" }
browzeit-renderer = { path = "../renderer" }
browzeit-network = { path = "../network" }
browzeit-driver = { path = "../driver" }
browzeit-api = { path = "../api" }
custode-browzeit = { path = "../custode-browzeit" }
```

### Binary vs library

A package with `[lib] name = "browzeit" path = "src/lib.rs"` is a library,
not a binary. The binary is `browzeit-api` in `crates/api/`. Build the
workspace for release:

```bash
cargo build --release --workspace
```

Binaries land in `<CARGO_TARGET_DIR>/release/`. Expected outputs:
- `browzeit-api.exe` — the API server
- `browzeit_traits-*.rlib`, `browzeit_core-*.rlib`, etc. — compiled libraries

### Clippy auto-fix

`cargo clippy --fix --workspace --all-targets` applies auto-fixable lints.
Re-run after fixing:

```bash
cargo clippy --fix --workspace --all-targets --allow-dirty --allow-staged 2>&1 | tail -10
```

Some lints require manual fixes (e.g., `too_many_arguments` needs a
`#[allow(clippy::too_many_arguments)]` attribute or parameter grouping). The
`unnecessary_operation` warning in an `if` arm is usually a missing
`return` before `Ok(...)` in a match arm returning `Result`.

## Packaging the desktop app (Windows)

The Rust backend and Python pywebview GUI shell are packaged together:

```bash
# 1. Build release binaries
cargo build --release --workspace

# 2. Build standalone GUI executable with PyInstaller
cd gui_shell
export PATH=/x/Dev/pyenvs/codeindex/Scripts:$PATH
python -m PyInstaller --name Browzeit --onefile --windowed \
  --collect-all webview browzeit_shell.py

# Output: gui_shell/dist/Browzeit.exe
```

### Environment isolation

"conda", "venv", "uv" environments exist on Windows
(`C:\Users\<user>\...`, `C:\Dev\pyenvs\<env>\...`). Use the activated
`python.exe` path directly with PyInstaller. The Shebang (`#!/usr/bin/env
python3`) is a Unix convention — Windows `python.exe` ignores it, so run
`python -m PyInstaller` with the correct `python.exe`.

### GUI shell architecture

- Window 1 (Primary): Agent/chat UI with generative canvas (pywebview)
- Window 2 (Secondary): Browser window with real website rendering (WebView2)
- IPC: REST API (port 8767) + SSE streaming (port 8765 for HTTP server)
- Backend: Rust (axum-based API server on `browzeit_api.exe`)

## Cross-app collaboration (KotMoE + Agentic Workbench)

When both projects share a provider registry (`providers.yaml`):

- Normalize provider IDs on import: `nous`→`nous_research`,
  `opencode-zen`→`open_code_zen`, `opencode-go`→`open_code_go`, `xai`→`grok`
- Shared v1.1.0 JSON profile format
- Guarded fetch with circuit breaker (5 fails, 60s) + LRU cache (50 entries,
  5-min TTL)
- Concurrent fetching via `tokio::spawn`

## Verify released binaries

Download released executables back and verify they run. A green CI suite does
not prove the artifact works on the user's machine — run the downloaded
binary and read the crash log:

```bash
# Download and run the released exe from a clean directory
cp release/browzeit-api.exe /tmp/install-test/
cd /tmp/install-test && ./browzeit-api.exe &
sleep 5
# Check the port is listening
netstat -an | grep 8767
kill %1
```

A plain `cargo build --release` success is not verification — the artifact
itself must run.