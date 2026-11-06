---
name: desktop-gui-build
description: Create a native desktop GUI app over a CLI or Rust core
version: 1.0.0
author: user
license: MIT
tags:
  - desktop
  - tauri
  - gui
  - windows
  - verification
related_skills:
  - tauri-gui-workflow
  - verification-first-development
  - windows-python-shell-interop
---


# Desktop GUI Build

> Class-level skill: build a native desktop GUI application (Tauri 2.x on Windows) over an existing CLI or Rust/JS core, with a full screen suite, settings, a command palette, keyboard-first UX, and verification artifacts (builds, tests, end-to-end smoke test). This is the pattern the NLP-CLI desktop app used: a verified Rust core, a thin JSON-protocol service, and a vanilla-TS frontend.

## When to Use

Use this skill whenever the task involves windowed desktop GUI work on Windows where the deliverable is a real desktop app (not a browser dashboard), including:

- Scaffolding a Tauri 2.x app around an existing CLI or library core.
- Migrating or wrapping an existing command-line or library into a windowed shell.
- Adding screens, settings, a command palette, themes, or accessibility to a desktop app.
- Verifying a multi-component desktop build (Rust backend + TS/HTML/CSS frontend + native shell).

> Mandatory default for this user's desktop work: Tauri 2 (pywebview is a fallback only). A desktop GUI is a windowed native app, never a browser dashboard.

## Standing rules (apply to every instance)

1. Proceed with all in order. Full implementation, never a stub or a "will add later" placeholder. Every screen, setting, command and wiring path is implemented and connected before the deliverable is called done.
2. Verification-first with working artifacts. A working MVP means cargo check/build clean, npm run build clean, tests pass, and an end-to-end smoke test against the real binary/core all return sensible values. No invented output. If a real path is blocked, say so plainly.
3. Accessibility is default, not a polish item. Every screen is keyboard navigable, has ARIA labels where needed, visible focus, and never relies on colour alone. Test contrast at theme boundaries.
4. Generative UI as a core architectural feature where the app is user-facing: UI must be data-driven and agents must be able to add/modify/optimize components in real time, not static hand-authored HTML.
5. Next steps = implementation, not release advice. The deliverable is a working artifact plus a short report of what was verified and what is left.
6. No stubs. If a component is hard to implement, implement it partially with a clearly labelled fallback, never leave a feature unbuilt inside a done screen.
7. Command contracts live in ONE place. Tauri command names must appear in a single typed client module (backend and frontend both import from it), never hand-written in two places.

## Process

### 1. Inventory the current state (where the previous agent left off)

- Read the repo design docs first (README, ARCHITECTURE, GUI-DESIGN, GAPS, CLI, FROZEN) - they define the feature set and approved defaults.
- Read git log and git status. The commit graph is the source of truth for what code exists; untracked files are tentative.
- Walk the tree and list source, data, spec, models, docs, target dirs. Note sizes so you know what a trained model counts as and what is missing.
- Do not assume a partial feature exists because a file name suggests it. Verify each feature path by reading source or running the binary.

### 2. Decide the shell

| Option | Best for | Drawbacks |
|---|---|---|
| Tauri 2 (WebView2) | Every desktop GUI job (user default). Native window, small bundle, Rust backend. | WebView2 runtime required; dev-mode quirks on Windows. |
| pywebview + local backend | Quick wrappers, fallback when WebView2 blocked. | Heavier runtime, less native. |
| ratatui TUI (same binary) | Terminal-first products (GUI-DESIGN may propose). | Not a windowed GUI; user asked for GUI, not the default. |

Decision rule: user asked for a GUI - Tauri 2 first. If a Tauri native launch fails (no WebView2, file locks), fall back to pywebview with the same frontend bundle, then report the blocker.

### 3. Choose backend wiring

- Reuse the verified core in-process for everything derived from it (routing, teach/review, verify, training, eval). In-process usage is exactly what the CLI does internally, so the desktop shell can never drift from the CLI.
- Spawn the CLI binary as a child process only for natural subprocesses (cli(args) - e.g. diagnostics, running the command line). Keep the spawn without a console window (CREATE_NO_WINDOW on Windows).
- Prefer plain Rust Result<T, String> in the service layer, with Tauri commands as thin wrappers. Keeps the service testable without a Tauri app (cargo test + integration tests).
- Train progress: run train_observed on a background thread, observer sends JSON progress lines over an mpsc channel; the async Tauri command polls the channel and emits train-progress / train-complete events to the frontend. Cancel = a global AtomicBool (thread_local, reachable from cancel_train) the observer checks at each epoch boundary; the worker is joined and the state cleared.
- Audit log schema is the CLI's one (session, id, at_unix, input, tool, risk, args, args_sha256, answer). Never invent a new audit format.

### 4. Layout the app in the workspace

- New desktop app = a separate cargo package (packages/desktop/src-tauri/), a member of the existing workspace, never editing the existing Rust crates.
- Frontend sources in packages/desktop/src/; Vite builds to packages/desktop/dist/; tauri.conf.json build.frontendDist points at ../dist.
- build.rs builds/spawns cargo build --release -p nlp-cli in the workspace and copies target/release/nlp-cli.exe into src-tauri/bin/nlp-cli.exe, emitting nlp-cli = { env: "NLP_CLI_BIN" } so the backend knows the embedded binary path at compile time.
- Do not give the desktop app a name that collides with the CLI binary (nlp-cli.exe vs nlpcli-desktop.exe).

### 5. Build the backend service

1. audit.rs - audit log schema + append/read helpers (CLI-compatible).
2. config.rs - desktop settings: TOML next to the project, defaults(), load() (missing = defaults), atomic save() (temp + rename), settings_schema() (category tree, every field with default/origin, locked flags), export/import JSON.
3. service.rs - the service struct holding project_dir plus run_route, run_teach, run_review, audit_items/append_audit, load_spec/load_model, run_train (progress + cancel), run_verify, run_model_status, run_evaluate (in-process core -> structured + Markdown), run_tools, run_config_show, run_save_config, run_diagnostics, run_cli. All Result<T, String>.
4. commands.rs - #[tauri::command] hands that translate Tauri args into service calls plus event emission (train-progress, train-complete, train-error) plus the TRAIN_STATE global for cancel.
5. Unit tests inside each module; one integration test (src-tauri/tests/) that copies the real NLP-CLI project (spec + model + data) into a temp dir and asserts real routing decisions, teach/review round-trip, audit schema, verify truth, safety failure count = 0, config schema + save/load, diagnostics fields, and train producing a new model + sidecar. This is the wiring proof.
6. Keep cargo fmt + cargo clippy clean on the new crate (the repo standard is 0 warnings).

### 6. Build the frontend

1. Scaffold: package.json (vanilla TS + vite + @tauri-apps/api), tsconfig.json (strict + noUnusedLocals + noUnusedParameters - the repo standard), vite.config.ts (base: './', build.outDir: 'dist', dev port 1420), tauri.conf.json (window, frontendDist: '../dist', beforeDevCommand + beforeBuildCommand, devUrl, bundle), src/main.ts + src/index.html + src/global.css.
2. src/tauri-client.ts - the single typed interface over invoke + event listeners (listen('train-progress') etc.). Every screen imports here; command names match the backend exactly. Keep fetch() as a browser fallback so the same bundle works in dev/browser and native.
3. State (state.ts): a singleton with subscribe(); screens re-render on navigation and train-progress events. Persistence: settings to TOML via save_config; history via backend history command.
4. Screens (a screen base class Screen with id, title, primaryAction, render()): Ask, History, Review, Train, Model, Evaluate, Tools, Settings, Help, Diagnostics - the nine top-level screens from GUI-DESIGN.md section 4, each with one primary action.
   - Ask screen: input + decision card + trace + confirm dialog + suggestions + status line. Keyboard: Enter submit, Alt+Enter new line, Up/Down history, Ctrl+R reverse search, Ctrl+P palette.
   - Settings screen: category tree + search box; each field shows name/eff/default/origin/locked with a lock icon and reason; editable text/number/select/bool/path/list; protected paths add-only; export/import; theme picker (auto/dark/light/mono/high-contrast); colour + glyphs; history retention; keys preset/bindings; advanced log level/diagnostics.
   - Train screen: config (epochs/hidden/seed), Start with progress log + Cancel, results summary + digest + comparison with the previous model, retraining note.
   - Model screen: path, digest, verify-on-start, provenance, format/version, Verify now and Retrain.
   - Evaluate screen: T1 classifier alone, full pipeline, safety suite tables + misses + export (Markdown + JSON).
   - Tools screen: catalogue from the spec (name, risk, slots, templates, broad flags) + search + Try to fill the Ask input. Generated from the spec, never hand-maintained.
   - Command palette (Ctrl+P): fuzzy search over every action in the app with keyboard nav (Up/Down/Enter/Esc).
   - Dashboard chrome: status bar (primary action, model-verified state, theme), confirmation modal (tool + args + approve/decline), toasts, onboarding tour on first run, Diagnostics page.
5. Accessibility pass: focus-visible outlines, role/aria, live regions for toasts/status, state labels not colour alone, contrast check across themes.

### 7. Verify

1. Backend: cargo check + cargo fmt --check + cargo clippy on the new crate, cargo test (unit + integration test).
2. Frontend: npm install (project-local), npm run build (tsc && vite build) - no type errors in the console output.
3. Desktop: cargo tauri build ends with a built binary and the frontend assets embedded. If the build passes but the binary fails to run (WebView2 0x800700AA, stale binary), follow the recovery sequences: kill stale app.exe, remove src-tauri/target, rebuild.
4. End-to-end smoke test with the real project: run the service against X:\Projects\NLP_CLI (real model, real data) and print route/verify/evaluate/history results. Compare the numbers with the CLI's own reports (the desktop app's numbers must match).
5. Visual verification is not possible in this headless environment; do not claim it. Structural verification (build + tests + smoke) is the honest bar.

### 8. Deliver

- State the deliverable (path, what it contains), what was verified (commands + results), what is left (e.g. visual confirmation). No release advice - the user asked for working software.

## Windows toolchain notes (this host)

- cargo/rustc live on X: (X:\Dev\cargo\bin); cargo-tauri (tauri-cli 2.11.4) is there. Use the full path or rely on the bash env; never cargo from an unqualified cmd (cmd does not see it).
- The terminal tool runs commands through bash (git-bash/MSYS) on this host, not PowerShell/cmd. MSYS paths like /c/Users/... work; native Windows tools need C:/Users/x-style forward-slash paths (not translated). npm is npm.CMD (a batch file) - subprocess.run cannot exec it directly; use cmd /c npm ...
- Node 26, npm 11, pnpm, Python 3.14, git all present. Network access to registry.npmjs.org works, so npm install is the dependency source of truth.
- cargo tauri dev on Windows can leave a stale app.exe holding target/debug/app.exe - kill it before rebuilding; if the lock persists, temporarily rename the binary in Cargo.toml, rebuild, restore the name.
- cargo tauri dev can fail with exit 124 from a non-tty shell; prefer the manual dev flow (build frontend, start cargo tauri dev or run the binary manually and open the Vite dev server URL) over blind retries.
|- In a Tauri desktop app the frontend is served as file:// assets under base: './' - Vite must output ./assets/... references, not absolute /assets/..., or JS/CSS never load in the native window.

## Cross-platform Rust workspace integration (new)
> This section is written for the Browzeit + Custode integration work, the most recent session's lesson set. It applies to any Rust multi-crate workspace on Windows where MSYS (bash) and native Windows tools share the same workspace.

### Path resolution is the #1 failure mode
`cargo`, `rustc`, and other native Windows tools do NOT have MSYS path conversion: a path like `/x/Projects/Browzeit` is seen by `cargo` as a literal path under a `/`-prefixed drive, not as `Z:\x\Projects\Browzeit`. Rules:
- For `cargo check` / `cargo build` (run through the `terminal` tool), use the `X:\Projects\...` or `C:\Users\...` format with backslashes — this is what the native toolchain expects.
- For `Cargo.toml` dependency `path` fields, use forward slashes: `path = "X:/Projects/Browzeit/browzeit/crates/traits"`. This is valid in both MSYS and native Windows build systems.
- `cd` in bash (MSYS) maps `/x` → `Z:\x` but native tools see the raw `/x` as an unsupported prefix. Never pass MSYS-style paths to `cargo`, `rustc`, or other native Windows binaries.

### Tool write behaviors (critical pitfalls)
- `write_file` refuses to overwrite a file it has not seen in the current session, even if the file exists on disk under a different path. The fix: `read_file` the file first (even a partial view), then `write_file` or `patch` again. This was the cause of six of the source files in this session being silently written to the wrong directory.
- `patch` cannot create a new file — it requires an existing match. To create a new file, use `write_file` or `terminal`.
- `terminal` runs through bash (MSYS). Heredocs (`<< 'END'`) break on single quotes and backslashes in content. For complex file content (Rust source with `//!` doc comments, triple-quoted strings), write the file via a Python script using `open(path, 'w')` instead of a bash heredoc.

### Cargo offline and dependency resolution
- `--offline` mode will fail on any dependency that needs to be downloaded from the registry, even if the crate is written correctly and all workspace members resolve. This happened with `rustls v0.22.4` being unavailable in the offline cache. Use normal (non-offline) `cargo check` when dependencies are missing from the cache.
- Rust package names use hyphens in `Cargo.toml` (`name = "browzeit-core"`) but underscore-separated in Rust code (`use browzeit_core::...`). When referencing workspace members, match the package name exactly.

### Multi-crate workspace on Windows (this host)

Rust multi-crate workspaces on this host split MSYS (bash) and native Windows path handling. Two failure modes that repeatedly cost sessions:

1. **Relative member paths are resolved from the *member crate's* directory, not the workspace root.** From `packages/desktop/src-tauri/Cargo.toml`, the repo root (`NLP_CLI`) is *three* `..` levels up: `../../../crates/core`. Writing `../../crates/core` (two levels) resolves to `packages/crates/core` — a directory that exists but holds no `Cargo.toml`. `cargo` then fails with a `failed to read <that path>` error whose path is correct for the wrong directory; the manifest you meant to edit is untouched. Always trace the relative member path forward from the member crate, and verify with `cargo metadata --no-deps` before you invest in `cargo check`.
2. **Verify the parsed workspace before building.** After editing the workspace root `Cargo.toml` (`members` array), run `cargo metadata --no-deps --manifest-path <root>/Cargo.toml` and check that the new package appears in `workspace_members`. If it does not, re-apply the patch — the working tree can silently revert to committed content (the desktop member was lost this session, leaving only `crates/core` and `crates/cli`, and every `cargo check` failed on the stale parse). Only run `cargo check` after the parsed workspace is right; a "member not found" error can be a stale parse from an earlier member list, not a code error.

### Workspace member addition
- To add a new crate to an existing Rust workspace, append its package name to the `members` array of the workspace root `Cargo.toml`. The new crate's `Cargo.toml` must already exist (or be created) at the listed path, and its dependencies on other workspace members use a relative `path` that is resolved from the *member crate's* directory, not the workspace root (`packages/desktop/src-tauri`'s `nlpcli-core` dependency is `../../../crates/core`, three `..` levels). Then verify with `cargo metadata --no-deps --manifest-path <root>/Cargo.toml` that the new package appears in `workspace_members` before running `cargo check`.

## Overlaps and where to look instead

- tauri-gui-workflow covers a different project (Agentic Workbench / BitForge: FastAPI sidecar + React + Tauri on Windows, telemetry dashboards, sidecar management). Its patterns are not this class's pattern; do not copy its backend architecture wholesale.
- verification-first-development overlaps on the verification bar; combine its verify-all-components bar with this skill's desktop-specific steps.
- windows-python-shell-interop covers the MSYS/Windows boundary; this skill's notes above are the condensed version for desktop GUI work.

## references/

- references/desktop-gui-decision-table.md - shell choice, backend wiring choices, and the full 9-screen feature brief template.
- references/windows-desktop-toolchain.md - this host's toolchain facts and the complete dev/native-launch recovery recipes.
