---
name: rust-workspace-development
description: Rust workspace setup and cargo debugging on Windows.
trigger: Use when the user asks to build, scaffold, or fix a Rust workspace; install Rust dependencies on Windows; resolve cargo check/test failures across multiple crates; set up projects using Tauri, Axum, ed25519, rand, wasmtime, llama.cpp, or Vulkan SDK; or build ML content identification systems with audio fingerprinting, neural networks, and self-learning pipelines.
---

# Rust Workspace Development

## User Preferences

- **Proceed with all**: when the user says “proceed with all” or “properly proceed with all”, do not stop at design documents or blueprints. Build, install, compile, and verify real artifacts. Report verified tool output, not descriptions.
- **Properly proceed with all**: this phrase specifically means: execute ALL identified workstreams systematically, in order, with verification after each step. Do not stop after the first few items. Continue through the entire list until every item is complete and verified.
- **Install, don’t describe**: when the user asks you to install dependencies or tooling, run the actual install commands and verify with tool output. Do not narrate what you would install.
- **Working artifacts over explanations**: the user values compiled binaries, green tests, and real file paths over prose summaries. Keep terminal output in the final report when it proves completion.
- **Residual items**: when the user asks to “properly proceed with residual items”, they want the exact remaining blockers addressed — not a new plan, but execution of the previously identified list.

## Windows Toolchain Setup

1. **Install VS Build Tools** before compiling Rust crates that hit the MSVC linker.
   - Winget: `winget install --id Microsoft.visualstudio.2022.BuildTools --silent --accept-source-agreements --accept-package-agreements --override "--wait --passive --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"`
   - If winget returns instantly without installing, download the bootstrapper directly: `curl -L -o vs_buildtools.exe "https://aka.ms/vs/17/release/vs_BuildTools.exe"` then run `./vs_buildtools.exe --wait --passive --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended`
2. **Verify MSVC is on disk**: `ls "C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools/VC/Tools/MSVC"` should show a version folder like `14.44.35207`.
3. **Run cargo under vcvars64**: every cargo check/test/build on Windows must run inside the VS developer prompt, otherwise `link.exe` from git-bash is found first and fails.
   - Pattern: `powershell -Command "& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat'; cargo check --package <pkg>"`
4. **Confirm cl/link**: after vcvars64, `where cl` and `where link` should resolve under `...BuildTools/VC/Tools/MSVC/.../bin/Hostx64/x64/`.
5. **Install LLVM/Clang** for crates that use `bindgen` (e.g. `llama-cpp-sys-2`, `ort`, `espeak-rs`):
   - `winget install --id LLVM.LLVM -e --accept-source-agreements --accept-package-agreements`
   - Verify: `ls "/c/Program Files/LLVM/bin/" | grep libclang` → should show `libclang.dll`
   - Set `LIBCLANG_PATH="/c/Program Files/LLVM/bin"` when running cargo, or add to `.cargo/config.toml` under `[env]`.
6. **Install CMake** (required by `cmake` crate for C++ dependency builds):
   - `winget install --id Kitware.CMake -e --accept-source-agreements --accept-package-agreements`
   - Verify: `cmake --version`
7. **Install Ninja** (parallel build tool, often needed by llama.cpp):
   - `winget install --id Ninja-build.Ninja -e --accept-source-agreements --accept-package-agreements`
   - If winget fails or the binary isn't on PATH, download directly: `curl -L -o C:/Tools/ninja.exe https://github.com/ninja-build/ninja/releases/download/v1.12.1/ninja-win.zip` (extract the exe).
8. **Install Vulkan SDK** for crates with Vulkan GPU features (e.g. `llama-cpp-2/vulkan`):
   - Download from `https://sdk.lunarg.com/sdk/download/latest/windows/vulkan-sdk.exe` and run the installer silently: `./VulkanSDK-<version>-Installer.exe /S /D=C:\VulkanSDK\<version>`
   - Verify: `ls "C:/VulkanSDK/<version>/Include/vulkan/"` and `ls "C:/VulkanSDK/<version>/Lib/cmake/"` (should contain `SPIRV-HeadersConfig.cmake`)
   - Set `VULKAN_SDK="C:/VulkanSDK/<version>"` and add `C:/VulkanSDK/<version>/Lib/cmake` to `CMAKE_PREFIX_PATH` when running cargo.
9. **Install Go** for Go-based services (e.g. `services/inference/`):
   - `winget install --id GoLang.Go -e --accept-source-agreements --accept-package-agreements`
   - Verify: `go version`

## Workspace Configuration

- Root `Cargo.toml` needs `[workspace]`, `resolver = "2"`, `[workspace.package]` with `version`, `edition`, `license`, `repository`, and `[workspace.dependencies]`.
- Every member crate must use workspace inheritance consistently: `version.workspace = true`, `edition.workspace = true`, etc. If a crate breaks inheritance, change it to inline values (`edition = "2021"`) to avoid resolver confusion.
- Do **not** mix path dependencies and workspace dependencies in the same member unless the crate is intentionally external to the workspace. If a crate is listed in `members`, use `cubeworld-foo.workspace = true` inside other members, not `path = "..."`.
- Keep the Tauri app **out of the workspace** until its `Cargo.toml` and `tauri.conf.json` are fully aligned with the installed Tauri CLI. A broken Tauri crate poisons `--workspace` checks.

## `.cargo/config.toml` for Build Script Env Vars

On Windows, env vars set via `export` in bash often don't propagate to cmake/build-script processes spawned by cargo. Use `.cargo/config.toml` at the workspace root:

```toml
[env]
CMAKE = "C:/Program Files/CMake/bin/cmake.exe"
PATH = "C:/Program Files/CMake/bin;C:/Program Files/LLVM/bin;C:/Tools;{PATH}"
```

This ensures `cmake`, `clang`, `ninja` etc. are found by build scripts (e.g. `llama-cpp-sys-2/build.rs`) even when cargo is invoked from a plain bash shell without `vcvars64.bat`.

To set this up: `mkdir -p .cargo && echo '[env]\nPATH = "C:/Program Files/CMake/bin;C:/Program Files/LLVM/bin;C:/Tools;{PATH}"' > .cargo/config.toml`

## Feature-Gating Pitfalls

- **Gating imports without gating usage sites**: when you add `#[cfg(feature = "X")]` to a `use` statement, ALL usage sites of that import must also be gated with `#[cfg(feature = "X")]` or `cfg!(feature = "X")`. If usage sites are unconditional, the import must be unconditional too. Gating imports without gating all usage sites causes `E0425` / `E0433` "cannot find type in this scope" errors that look like missing dependencies but are actually cfg mismatches.
  - **Fix**: either gate every usage site, or remove the cfg gate from the import. Prefer the latter when the dependency is effectively required.
- **Gating system-dependent dependencies**: crates like `cpal` (audio) require system libraries (ALSA on Linux) that may not be present in CI. Make such dependencies optional behind a feature flag (e.g., `audio = ["cpal"]`) and gate the module with `#[cfg(feature = "audio")]` at the top of the file. This prevents cross-platform CI failures while keeping the functionality available.
- **Test module declaration in binary crates**: when adding a new test file (e.g., `relay_integration_tests.rs`) to a binary crate, you must declare it in `main.rs` with `mod relay_integration_tests;`. Without this, cargo ignores the file entirely — no compilation, no test discovery, no errors about the missing module.
- **Serde enum round-trip testing**: when testing `#[serde(tag = "type")]` enum serialization, all variants must be constructible. If a variant wraps a complex type (e.g., `PairingHandshake`), construct a simpler variant for the test (e.g., `TextIntent(String)`) or test serialization by checking JSON output contains expected fields rather than doing a full round-trip.
- **Match arm ordering with catch-all**: when using `#[cfg(feature = "X")]` on specific match arms, place the catch-all `_ =>` arm AFTER all specific arms, not before. A catch-all at the top makes later arms unreachable and triggers `unreachable_pattern` warnings.
- **Gating event enum variants across crates**: when a `#[cfg(feature = "X")]`-gated enum variant (e.g., `ConnectionEvent::Audio`) exists in one crate, all match arms in OTHER crates that reference it must either be gated with the same cfg or replaced with a catch-all `_ =>`. The variant simply doesn't exist when the feature is off, causing `E0599`.
- **Feature gating at module level**: use `#![cfg(feature = "X")]` at the top of a file to gate an entire module. This is cleaner than gating every item individually and ensures the module is completely absent when the feature is disabled.
- **Match arms with cfg on enum variants**: you cannot put `#[cfg]` directly on individual match arms for enum variants. Instead, use `#[cfg(feature = "X")] Variant => ...` as a separate match arm pattern, or replace the arm with a catch-all `_ =>` and handle the logic inside with `cfg!` macro.

## The Completion Loop Trap (Critical User Preference)

When the user says "properly proceed with all" and you complete a major phase, **STOP**. Do not generate another massive workstream or roadmap unless explicitly asked.

**Pattern that triggers user frustration:**
1. User says "proceed with all" → you complete workstreams
2. User asks "what are you actually going to do?" or "what's next" → you generate a 12-phase roadmap
3. User says "proceed with all" on the roadmap → you complete some, then generate ANOTHER roadmap
4. Repeat indefinitely

**Correct behavior:**
- After completing a major milestone, report the verified state concisely
- When the user asks "what's next", give a SHORT summary (3-5 options max) and WAIT for their selection
- Do NOT generate multi-phase roadmaps unprompted
- If you've been going back and forth for more than 2 rounds, explicitly ask: "Should I stop here and wait for your direction?"

**User's explicit preference (from session):** "A pass that does nothing is a missed learning opportunity, not a neutral outcome." — but also, endless speculative planning is NOT what "proceed with all" means. It means: execute the CURRENT scope fully, verify, then stop and report.

## Research vs. Build Discipline

When the user asks a question like "what are ALL possible ways to do X" or "how can X be expanded to be the best", they are asking for **analysis and design**, NOT a build order. Do NOT turn research requests into multi-phase implementation roadmaps.

**Pattern that triggers user frustration:**
1. User asks: "what are all possible ways to improve X?"
2. You generate a 16-section design document with 12 implementation phases
3. User says "proceed with all" expecting you to build the analysis into a concise design
4. You instead try to implement all 12 phases
5. User gets frustrated because they wanted the DESIGN, not infinite execution

**Correct behavior:**
- When asked for "all possible ways" or "comprehensive analysis": produce a CONCISE, well-organized design document. That's the deliverable.
- When asked to "proceed with all" on a design: implement ONLY the highest-priority, most-concrete items. Not every speculative phase.
- After shipping a release (e.g., v0.3.0), the optimal next step is "ship it and wait for feedback" — NOT generating more workstreams.
- Documentation should be VALUE-DENSE and CONCISE. A 1266-line design doc is not concise. Aim for the minimum viable documentation that covers all points.

## Proactive Comprehensive Scope

When the user asks for "fully featured, robust, stable" or "properly proceed with all", they want a COMPREHENSIVE audit of the ENTIRE codebase in a single pass — not just the obvious gaps.

**Pattern that triggers user frustration:**
- User: "make it fully featured, robust, stable"
- You: identify 6 items, complete them, report done
- User: asks the SAME question again because you missed half the gaps
- You: identify 5 more items, complete them
- User: asks AGAIN

**Correct behavior:**
- When the user asks for comprehensive improvement, do a FULL codebase audit FIRST
- Read every source file, identify ALL gaps (functional, architectural, UX, error handling, logging, persistence, etc.)
- Present the COMPLETE list upfront, then execute ALL of it
- Do NOT stop at the "obvious" items — dig into every module
- Categories to audit: core functionality, error handling, input validation, loading states, persistence, logging, event handling, shutdown behavior, test coverage, code quality, UI completeness

**Example (DiskRipper session):**
- First pass identified: ISO parser, Imager, Extractor, cancellation, Rock Ridge, Joliet, multi-extent, disc type, TOC, recovery, verification (11 items)
- Second pass identified: settings, events, logging, shutdown, Tauri commands, error display, validation, loading, settings UI, audio CD UI, verify UI (11 items)
- Third pass identified: UDF bug, unused imports, clippy warnings (5 items)
- ALL of these should have been identified in the FIRST audit

## Scope Discipline

The user wants YOU to decide scope, not generate infinite roadmaps for them to choose from.

**Pattern:**
- User: "proceed with all"
- You: generate 10-item todo list, complete 3, generate 10 more
- User: frustrated because you keep expanding scope

**Correct behavior:**
- When the user says "proceed with all", identify the SMALLEST set of work that achieves the goal, execute it, verify, STOP.
- Do NOT generate speculative future work. If you think of future work, put it in a "Future Work" section at the END of your report, not as new todo items.
- After shipping: "v0.3.0 is shipped. Next: wait for user feedback." NOT "here are 8 more things to build."

## Common Rust Error Patterns and Fixes

- **E0204: `Copy` cannot be implemented for types with `String` / `HashMap`**: remove `Copy` from the derive list. `LocusId(String)` must be `Clone` only.
- **E0277 / E0432: unresolved imports across modules**: when `crate::Foo` is unresolved, the type is either private or defined in a submodule not re-exported. Prefer explicit `pub use` in `lib.rs` over bare `mod foo;` assumptions.
- **E0599: no variant named `IOError` for error enum**: when using `thiserror`, variant names must match exactly. If the enum defines `Io(String)` but code references `DiskRipperError::IOError(e)`, the compile fails. Always check the actual enum definition in `error.rs` before constructing error variants.
- **E0609: no field `0` on type `&String`**: when iterating a `HashMap<String, T>`, pattern-match `(k, v)` rather than tuple-indexing.
- **E0728: `async fn` not permitted in Rust 2015**: if a crate clearly uses modern async but fails with Rust 2015-style errors, first suspect stale or partial compilation artifacts. Run `cargo clean -p <crate>` before changing edition inheritance; workspace metadata can be valid while one crate's incremental cache is corrupted.
- **Tauri build script failures**:
  - `unknown field 'tauri'` / `'package'` / `'allowlist'`: the installed `tauri-build` is newer than the config schema. Remove top-level `"tauri"`, `"package"`, or `"allowlist"` wrappers and use only the fields the installed version accepts: `productName`, `version`, `identifier`, `build`, `bundle`, `plugins`.
  - `icons/icon.ico not found`: create a stub icon file or remove `icon` arrays from `bundle`.
  - `package.metadata does not exist`: ensure `[package.metadata]` is not present; Tauri 2 uses top-level keys only.
- **Axum 0.7 handler mismatches**: `State<Arc<AppState>>` requires `use std::sync::Arc;` in every module that names `Arc`. `WebSocket::into_split()` is the current API; `split()` was removed.
- **Plugin / Wasmtime trait mismatches**: `wasmtime` does not re-export `Store`, `Instance`, `Module` as crate-root types in all versions. Import them explicitly: `use wasmtime::{Engine, Instance, Module, Store};`.
- **Duplicate crate names in Cargo.toml**: `thiserror = "2"` appearing twice in `[dependencies]` causes `error: duplicate key`. Deduplicate before checking.

## Verification Workflow

1. Run `cargo check --workspace` and capture exit code and tail output.
2. If exit is non-zero, grep for `^error\\[E` and fix the first error class before retrying. Do not stack unrelated fixes.
3. Once `cargo check` is clean, run `cargo test --workspace`.
4. For isolated crate checks during debugging, use `--package <name>` to avoid workspace-wide resolution overhead.
5. Always run under `vcvars64.bat` on Windows; otherwise linker errors will mislead you into editing correct Rust code.

## Stale-Incremental-Cleanup Workflow

When a crate fails with edition/async errors that do not match the manifest, follow this order:

1. Run `cargo metadata --format-version 1 >/dev/null` to verify manifest parsing.
2. Inspect the affected crate's `Cargo.toml` and confirm `edition`.
3. Run `cargo clean -p <crate>` to clear incremental artifacts for that crate.
4. Run targeted `cargo check -p <crate>`.
5. Only then adjust edition inheritance or code if the error persists.

This avoids unnecessary edition churn and isolates the failure from compiler cache corruption.

## Large Workspace Change Workflow

For multi-crate workspaces, prefer small, scoped changes with `cargo check --workspace` between them instead of large cross-crate patches. Typical safe sequence:

1. Update workspace `Cargo.toml` metadata or `resolver`, then verify manifest parsing with `cargo check --workspace`.
2. Add/remove crate features or optional dependencies in the affected crate’s `Cargo.toml`; keep gated `#[cfg(...)]` blocks behind those features.
3. Implement the change in one crate at a time; avoid touching unrelated crates in the same pass.
4. If `cargo check` fails on an exact-match manifest patch, reload the manifest before retrying — patch assumptions often drift from current section order.
5. When one crate has environment-specific doctest failures but unit tests pass, validate unit coverage with `cargo test --workspace --quiet -- --skip <crate>` rather than disabling tests globally.

### Non-Windows backend expansion in a Windows-hosted workspace

- Add optional platform-specific deps under `[features]` with platform-gated names.
- Use `#[cfg(any(target_os = "macos", target_os = "linux"))]` in Rust code so Windows hosts still compile the workspace.
- Validate the change on Windows by confirming `cargo check --workspace` succeeds; test the non-Windows path in CI or on a matching host.

### Excluding optional crates from default builds

- Use `default-members` in the workspace root `Cargo.toml` to exclude crates that have environment-specific failures (e.g., doctest issues on Windows MSVC). Keep them in `members` so they remain buildable on demand with `-p <crate>`.
- Pattern: list all crates in `members`, then list only the healthy/default crates in `default-members`. This keeps `cargo check --workspace` and `cargo test --workspace` working while preserving the ability to build excluded crates explicitly.

### Relay/server behavior expansion

- When hardening network services, prefer reusing an existing listener path before adding new ports or external dependencies.
- Extend dispatch tables to real handlers instead of leaving stream type arms as `Ok(())` stubs; stub handlers silently drop capability and are hard to notice at runtime.

### Resume/session cleanup pattern

- Spawn cleanup tasks near server state initialization so runtime maps (`resume_tokens`, `partial_transfers`) do not grow unbounded.
- Tune eviction on a fixed background interval instead of only on access; that keeps long-running sessions stable even under idle or disconnect-burst traffic.

## Tauri-Specific Notes

> For a complete session-proven reference covering workspace inclusion, command organization, IPC constraints, async patterns, config schema, and esbuild postinstall — see [tauri2-build-patterns.md](references/tauri2-build-patterns.md).

- Scaffold the Tauri app **after** the Rust workspace compiles. A broken Tauri crate blocks workspace checks.
- `tauri.conf.json` must match the installed `tauri-build` version. If unsure, start minimal: only `productName`, `version`, `identifier`, `build`, `bundle`.
- Create `capabilities/default.json` with `{"identifier": "default", "windows": ["main"], "permissions": ["core:default"]}`.
- Frontend scaffolding is independent: `package.json`, `vite.config.ts`, `tsconfig.json`, `index.html` do not affect Rust compilation.
- **CLI binary workspace integration**: When adding a CLI binary to a workspace member, it must use `use diskripper_core::...` imports (not `crate::` which only works for the library crate). Remove the CLI module from `lib.rs` to avoid duplicate module errors.
- **Streaming I/O**: Never read entire disc images into memory. Use async streaming with progress events (see rust-native-development pitfall #20).
### CLI Binary Workspace Integration (Proven Pattern)

When adding a CLI binary to a workspace member that wraps the library:

1. Place the binary in `src/main.rs` of the library crate (e.g., `diskripper-core/src/main.rs`)
2. Use `use diskripper_core::...` imports (NOT `crate::` which only works for the library crate)
3. Remove the CLI module from `lib.rs` to avoid duplicate module errors
4. Add `[[bin]]` declaration in `Cargo.toml`:

```toml
[[bin]]
name = "diskripper"
path = "src/main.rs"
```

5. Build with: `cargo build -p diskripper-core --bin diskripper`

**Why**: The binary crate needs to import from the library crate as an external dependency. Using `crate::` in `main.rs` fails because `main.rs` is not part of the library crate — it's a separate binary crate that depends on the library.

### MCP Server Wrapping Pattern

When the user asks to expose Rust CLI tools to AI agents (e.g., "build an MCP server so agents can use this"):

1. Build a TypeScript MCP server that wraps the CLI binary via `spawn()`
2. Use `process.env.MY_TOOL_BIN` for the binary path (never hardcode)
3. Use absolute forward-slash paths on Windows: `C:/Projects/.../diskripper.exe`
4. Set `timeout: 300+` in `~/.hermes/config.yaml` for long-running operations
5. Always build the CLI binary BEFORE testing the MCP server

```typescript
// packages/mcp-server/src/index.ts
import { spawn } from 'child_process';

const DISKRIPPER_BIN = process.env.DISKRIPPER_BIN || 'diskripper';

async function callCLI(...args: string[]): Promise<string> {
  return new Promise((resolve, reject) => {
    const child = spawn(DISKRIPPER_BIN, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (d) => { stdout += d.toString(); });
    child.stderr.on('data', (d) => { stderr += d.toString(); });
    child.on('close', (code) => {
      if (code === 0) resolve(stdout.trim());
      else reject(new Error(`exit ${code}: ${stderr.trim()}`));
    });
    child.on('error', (err) => reject(new Error(`spawn failed: ${err.message}`)));
  });
}
```

**Registration in `~/.hermes/config.yaml`:**
```yaml
mcp_servers:
  diskripper:
    command: node
    args:
      - C:/Projects/DiskRipper/packages/mcp-server/dist/cli.js
    timeout: 300
    connect_timeout: 120
```

**Testing sequence:**
```bash
# 1. Build CLI binary first
cargo build -p diskripper-core --bin diskripper

# 2. Build MCP server
cd packages/mcp-server && npm run build

# 3. Test initialize
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}' | node dist/cli.js

# 4. Test tool call with env var
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"list_drives","arguments":{}}}' | DISKRIPPER_BIN="C:/Projects/DiskRipper/target/debug/diskripper.exe" node dist/cli.js
```

### build.rs is Mandatory

Tauri 2 requires a `build.rs` that calls `tauri_build::build()`. Without it, `tauri::generate_context!()` panics at compile time with `OUT_DIR env var is not set`:

```rust
// src-tauri/build.rs
fn main() {
    tauri_build::build()
}
```

```toml
# src-tauri/Cargo.toml
[build-dependencies]
tauri-build = "2"
```

## Git Initialization on Windows Non-Interactive Sessions

When initializing a git repo in a Windows non-interactive terminal session, the first commit can hang or fail if build artifacts are staged before `.gitignore` is in place.

### Pattern

1. Create `.gitignore` before `git add`.
2. Stage sources selectively: `git add .gitignore Cargo.toml CLAUDE.md <source dirs>`.
3. If `target/` was already staged, run `git rm --cached -r target` first.
4. Configure git identity before commit: `git config user.email "dev@example.com"` and `git config user.name "Dev"`.
5. Commit with a concise message; avoid huge diffs from build directories.

### Why

Non-interactive git on Windows can stall on massive deleted-file lists from build directories. Removing `target/` from the index before committing keeps the initial diff small and avoids timeouts.

### The `git add -A` Timeout Trap (Proven September 2026)

When a workspace contains `frontend/node_modules` (or any large dependency directory), `git add -A` can timeout with exit code 124 even when `.gitignore` is correct. This happens because git still scans the directory tree to determine what to ignore.

**Symptom:**
```bash
git add -A
# (hangs for 5+ minutes, then exits with code 124)
```

**Fix:**
```bash
# 1. Ensure .gitignore exists and excludes node_modules
# 2. Remove from index if previously staged
git rm -r --cached frontend/node_modules 2>/dev/null
# 3. Stage selectively instead of -A
git add .gitignore Cargo.toml diskripper-core/ diskripper-tauri/ frontend/src/ frontend/package.json packages/ scripts/ .github/
# 4. Verify node_modules is NOT in the staged list
git status | grep node_modules  # should show nothing
# 5. Commit
git commit -m "message"
```

**Prevention:** Always create `.gitignore` BEFORE running any `git add` command. If `.gitignore` doesn't exist when `git add -A` runs, node_modules gets staged and subsequent operations become extremely slow.

## Git History Cleanup via Orphan Branch

When large files (e.g., `target/debug/*.pdb` at 100+ MB, `*.rlib` at 50+ MB) are already in git history from previous commits, `git push` fails with `GH001: Large files detected` even if `.gitignore` is correct. `git rm --cached -r target` only removes from the index, not from history.

### Pattern

1. Create an orphan branch: `git checkout --orphan temp_main`
2. Stage all current files: `git add -A`
3. Verify no large files: `git ls-files target/ | wc -l` should be 0
4. Commit: `git commit -m "vX.Y.Z: description"`
5. Delete old tag if it exists: `git tag -d vX.Y.Z`
6. Create new tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
7. Force-push the clean branch: `git push origin temp_main:main --force`
8. Switch back: `git checkout main`
9. Reset to match remote: `git reset --hard origin/main`
10. Push the tag: `git push origin vX.Y.Z`

### Why

GitHub's pre-receive hook rejects pushes containing files over 100 MB anywhere in history, not just in the latest commit. Rewriting history via orphan branch is the cleanest fix when `target/` was committed by a previous contributor or accidental `git add -A`.

### Safety

- Only force-push to `main` if you own the repository or have coordinated with the team.
- The orphan branch approach preserves all file contents but discards commit history.
- If history matters, use `git filter-repo` or BFG Repo-Cleaner instead.

## React/Tauri Frontend Wiring Pattern

Frontend TypeScript should call Tauri IPC through a thin API wrapper, not through ad-hoc `window.__cw` calls in views.

### Files

- `cubeApi.ts` — one module that imports `invoke` from `@tauri-apps/api/core` and exports typed functions (`create_cube`, `breed_cubes`, `get_cube`, `list_cubes`, `save_game`, `load_game`).
- `cw.d.ts` — TypeScript interface declarations for request/response shapes, kept in sync with Rust command signatures.
- `views/*.tsx` — consume `cubeApi.ts` only. No direct `invoke()` calls in views.

### Rule

Every Tauri command registered in Rust must have a matching typed export in `cubeApi.ts`. Every view must import from `cubeApi.ts`. This prevents signature drift between Rust and TypeScript.

## Workspace State Reporting

When the user asks for the “optimal next steps” or a codebase review, do not give a vague status. Return a compact **verified state + exact blockers** report:

- **Verified state**: real check/test results, feature additions, dep cleanup, CI additions.
- **Exact blockers**: crate-by-crate table with `Issue` and `Fix path`, not project-wide hand-waving.

This replaces narrative descriptions like “some crates have issues” with actionable triage.

## Subset Verification

When the workspace is mixed healthy/broken, verify the healthy slice directly instead of stopping at the first failure:

- `cargo check -p <healthy_pkg_a> -p <healthy_pkg_b> ...`
- `cargo test -p <healthy_pkg_a> ... --tests -- --skip <excluded_crate>`

Report the passing subset explicitly, then list the remaining broken members in the blocker table. This prevents a single broken crate from hiding all progress.

## Handling Windows Doctest/Test Gaps

Doctests can fail on Windows MSVC because `rustdoc.exe` is unavailable, while unit tests pass. Treat this as a toolchain gap, not a code failure.

- Validate unit coverage with `cargo test --workspace --quiet --tests -- --skip <crate>` or package-scoped test commands.
- In CI, skip doctests on this toolchain explicitly; add unit-test coverage to compensate.
- Do not disable testing globally; only gate the doctest execution path.

## Strict CI Configuration

Enforce strict Rust linting in CI to catch regressions early:

```yaml
env:
  RUSTFLAGS: "-D warnings"

jobs:
  check:
    steps:
      - run: cargo check --workspace
  test:
    steps:
      - run: cargo test --workspace --quiet --tests -- --skip continuum_ai
  clippy:
    steps:
      - run: cargo clippy --workspace --quiet -- -D warnings
  fmt:
    steps:
      - run: cargo fmt -- --check
  audit:
    steps:
      - run: cargo install cargo-deny --locked
      - run: cargo deny check
```

- Set `RUSTFLAGS="-D warnings"` at the job level so all cargo commands inherit it.
- Use `--tests` to avoid doctest failures on Windows MSVC.
- Add a `deny.toml` with `vulnerability = "deny"`, `unmaintained = "warn"`, `yanked = "warn"`, and explicit `[[allow]]` entries for known transitive dependencies that are unmaintained but still required.
- Run `cargo audit` separately; if it times out on registry checks, retry or run it as a scheduled workflow rather than blocking every PR.

## Performance and Size Auditing

Add performance and binary-size checks to CI:

- **Flamegraphs**: `cargo install flamegraph --locked`; generate with `cargo flamegraph --release -p <crate> --example <example>`.
- **Bloat**: `cargo install cargo-bloat --locked`; run `cargo bloat --release -p <crate>` to identify large contributors.
- **Release profile**: keep `opt-level = 3`, `lto = true`, `codegen-units = 1`, `strip = true`. Consider `panic = "abort"` only if the binary size savings outweigh stack-trace loss.

## Security Audit Workflow

When `cargo audit` reports vulnerabilities:

1. Classify by severity: critical/high → immediate bump; medium/low → track and schedule.
2. For transitive advisories without safe immediate upgrades, add `[[allow]]` rules in `deny.toml` with a comment linking the advisory and planned fix.
3. For `wasmtime` or other optional dependencies, consider making the feature default-off if the risk surface outweighs usage.
4. Document the decision in `docs/SECURITY_POLICY.md` and track unresolved advisories in a GitHub issue or project board.

## Release Automation

Provide release scripts for both Linux and Windows:

- `scripts/release.sh` — bash script that runs tests, clippy, fmt, builds release binaries, runs `cargo deny check`, updates versions, and generates a changelog stub.
- `scripts/release.bat` — Windows equivalent for contributors without bash.
- Document the release sequence: commit → push → tag → GitHub release with artifacts from `target/release/`.

## Deployment Documentation

Every deployable binary should have:

- A quick-start section with exact `cargo run --release` commands.
- Service-unit examples for systemd, NSSM, or Docker.
- Environment-variable overrides for log level, listen address, and pairing code.
- Security considerations: TLS, firewall rules, audit-log monitoring, and pairing-code hygiene.
- Troubleshooting sections for connection, pairing, input, clipboard, file transfer, audio, CPU, and relay issues.

## Relay Server Async Startup Boundary

If a relay/server binary fails with Rust 2015-style async errors despite workspace metadata:

1. Run `cargo metadata --format-version 1 >/dev/null` to verify manifest parsing.
2. Inspect the crate’s `Cargo.toml` for explicit `edition = "2021"`.
3. Run `cargo clean -p <crate>` to clear incremental artifacts.
4. If errors persist, choose:
   - **modern-rust path**: explicit `edition = "2021"` with `tokio::main` or async runtime bootstrap
   - **legacy-compat path**: sync/threaded startup with explicit runtime handoff
5. Document the chosen path in `docs/RUST_EDITION_POLICY.md`.

## Non-Windows Backend Expansion

- Add optional platform-specific deps under `[features]` with platform-gated names.
- Use `#[cfg(any(target_os = "macos", target_os = "linux"))]` in Rust code so Windows hosts still compile the workspace.
- Validate on Windows by confirming `cargo check --workspace` succeeds; test the non-Windows path in CI or on a matching host.

## Strictness Without Breaking Disabled Crates

Do not let deprecation, optional features, or excluded crates block strict builds:

- Mark unused code with `#[allow(dead_code)]`, `#[allow(unused_mut)]`, `#[allow(unused_variables)]` only on the exact unused item, not whole modules.
- Use `edition = "2021"` explicitly everywhere.
- Enforce strictness in CI: `RUSTFLAGS: "-D warnings"`, `cargo clippy -- -D warnings`, `cargo fmt -- --check`.
- Add `deny.toml` with `vulnerability = "deny"`, `unmaintained = "deny"`, `yanked = "deny"`, and `multiple-versions = "warn"`.
- Gate debug/observability behind an optional feature in release builds.
- Exclude dead or optional crates from `default-members`; keep them only under `members` so they remain buildable on demand.

## Edition/Async Boundary Blocker Triage

If a crate fails with edition-2015-style async errors despite workspace metadata, first assume it is a stale artifact or explicit edition/async boundary issue, then follow this order:

1. `cargo metadata --format-version 1 >/dev/null`
2. Inspect the crate’s own `Cargo.toml` for `edition`, and then run `cargo clean -p <crate>`.
3. Run targeted `cargo check -p <crate>`.
4. Only then decide between:
   - **modern-rust path**: explicit `edition = "2021"`, `tokio::main`/`axum` runtime bootstrap, async startup boundary
   - **legacy-compat path**: sync/thread-based startup with explicit runtime handoff

Document the chosen path in a `docs/RUST_EDITION_POLICY.md` so contributors inherit the decision.

## Cross-Crate Error Propagation

When modifying `ContinuumError` (or any core enum) in `continuum-core`:

1. Add the variant to `continuum-core/src/lib.rs`
2. Search ALL workspace members for `crate::ContinuumError` or `continuum_core::ContinuumError` references
3. Update each usage site (match arms, error conversions)
4. Run `cargo check --workspace` to catch stragglers

**Recurring pattern:** Adding error variants requires updates in every crate that imports from `continuum-core`.

## Crate Selection for 100-Year Projects

For foundational infrastructure, evaluate crate stability vs. implementation cost:

- **Implement yourself:** Small, stable protocols (STUN parsing, simple binary formats) where the RFC is clear and the code is <500 lines
- **Depend on crates:** Complex, evolving protocols (QUIC, TLS, H.264 encoding) where implementation cost is high

**Red flags for crate selection:**
- Crate was migrated to a monorepo (e.g., `stun` → webrtc-rs)
- Limited maintenance or single maintainer
- Wrapper around C library that may become incompatible

**Pattern:** For STUN (RFC 5389), a custom ~200-line parser is more durable than a potentially abandoned crate.

## ML Content Identification System

DiskRipper includes a comprehensive ML system (`diskripper-core/src/ml/`) for identifying and organizing ripped content. This is a **custom, self-learning system** — not just API wrappers.

### Architecture

```
diskripper-core/src/ml/
├── pipeline.rs              # Main orchestrator (audio/video identification)
├── audio_fingerprint.rs     # Custom audio fingerprinting (AcoustID replacement)
├── music_identification.rs  # Hybrid music ID with confidence scoring
├── video_fingerprint.rs     # Video perceptual hashing + temporal fingerprinting
├── content_classifier.rs    # Genre/type classification
├── hybrid_identifier.rs     # Multi-signal identification with confidence
├── self_learning.rs         # User feedback → training batches → model updates
├── data_management.rs       # Training data collection + augmentation
├── model_versioning.rs      # Model versioning, rollback, A/B testing
├── inference.rs             # Neural network inference (MLP/CNN)
├── training.rs              # Backpropagation training loop
├── feature_extraction.rs    # MFCCs, chroma, spectral features, video features
└── organizer.rs             # Auto-organize ripped content
```

### User Preference: Build, Don't Just Integrate

**Critical learning from session:** When the user asks for ML models, they want **custom-built models with training pipelines** — not just API wrappers around AcoustID/MusicBrainz/TMDB.

**Correct approach:**
- Build custom audio fingerprinting (AcoustID replacement)
- Build neural network inference engine
- Build training pipeline with backpropagation
- Build self-learning from user feedback
- Build smart organization
- Use APIs only as fallback/enhancement, not primary

**Anti-pattern that triggers user frustration:**
- "Let's integrate AcoustID API" — NO
- "Let's use MusicBrainz lookup" — NO (unless as fallback)
- "Let's train a model on real data" — YES
- "Let's build a self-learning pipeline" — YES

### Audio Fingerprinting (AcoustID Replacement)

Custom fingerprinting that works entirely locally:
- Spectral peaks stored as (frequency, time) tuples
- Combinatorial hashing for compact fingerprints
- Jaccard similarity for matching
- Duration similarity weighted into confidence score

### Training Pipeline

Full backpropagation training with:
- Mini-batch gradient descent
- Backpropagation with cross-entropy loss
- Validation and early stopping
- Best model checkpointing
- Training history serialization

### Self-Learning from User Feedback

The system improves from user corrections:
- Collects corrections from users
- Creates training batches (min 10 samples)
- Retrains models on feedback
- Tracks accuracy over time

### Feature Extraction

Audio features:
- MFCCs (13 coefficients, simplified mel-scale)
- Chroma (12 pitch classes)
- Spectral features (8 frequency bands)
- Zero-crossing rate
- RMS energy
- Basic statistics (mean, std, min, max)

Video features:
- Average brightness per frame
- Scene change detection (frame differences)
- Color histograms (8 bins per channel)
- Motion estimation

### Smart Content Organization

Automatic folder structure based on ML identification:
```
Music/Artist/Album/Track.ext
Movies/Title (Year)/Title.ext
TV Shows/Title/Title.ext
Software/Title/Title.ext
Games/Title/Title.ext
Other/Title.ext
```

Plus NFO file generation for media center compatibility.

### Hybrid Identification Strategy

The system combines multiple signals for maximum accuracy:
1. **Audio fingerprinting** (local, no network needed)
2. **Content classification** (genre, type detection)
3. **Metadata lookup** (when network available)
4. **User feedback** (corrections improve future predictions)

Each signal has a confidence score; the highest-confidence result is used.

### Dependencies Added

```toml
# Cargo.toml
rand = "0.8"        # Xavier weight initialization, random sampling
fastrand = "2.0"    # Efficient shuffling for training data
```

## References

- `references/diskripper-ml-system.md` — ML content identification: audio fingerprinting, neural networks, training pipelines, self-learning
- `references/diskripper-workspace-patterns.md` — DiskRipper-specific patterns: binary naming, CLI imports, streaming I/O, event-driven progress, MCP registration, git + node_modules timeout workaround, native Windows FFI, DVD IFO parsing, CD-Text, multisession CDs, FLAC, AccurateRip, system tray, auto-updater
- `references/windows-toolchain-fixes.md` — concrete error codes and fixes from this session.
- `references/tauri2-schema.md` — installed Tauri 2.6.3 / 2.11.5 config field mapping.
- `references/git-windows-init.md` — non-interactive git initialization pattern on Windows.
- `references/frontend-ipc-wiring.md` — React/Tauri IPC wiring pattern.
- `references/tauri-llama-cpp-build.md` — building Tauri apps with llama.cpp + Vulkan on Windows.
- `references/continuum-feature-gating-pitfalls.md` — cfg-gating mistakes and test-module declaration patterns from Continuum work.
- `references/continuum-stabilization-notes.md` — full session notes: workstreams, pitfalls, residual blockers, verification commands.
- `references/continuum-architecture-patterns.md` — trait abstractions for 100-year evolvability.
- `references/continuum-v1-implementation-notes.md` — v1.0 implementation learnings: ICE/STUN, mDNS, CryptoProvider, video codec, session management.
- `templates/workspace-cargo-toml.toml` — known-good workspace root template with `[workspace.dependencies]`.
- `scripts/verify-workspace.sh` — bash wrapper that runs cargo under vcvars64 on Windows.
