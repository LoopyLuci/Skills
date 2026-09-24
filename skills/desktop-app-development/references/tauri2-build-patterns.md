# Tauri 2 Build Patterns (Session 2026-09-01)

Concrete patterns for Tauri 2 apps that compile cleanly on Windows.

## Workspace Inclusion (DO include)

The Tauri app CAN be a workspace member — keep it IN the workspace. The key requirements:

1. **build.rs is mandatory** — without it, `tauri::generate_context!()` panics with `OUT_DIR env var is not set`:
   ```rust
   // diskripper-tauri/build.rs
   fn main() {
       tauri_build::build()
   }
   ```
2. **Cargo.toml** must have:
   ```toml
   [build-dependencies]
   tauri-build = "2"
   ```
3. **tauri.conf.json** must match the installed `tauri-build` schema exactly.

## Command Organization (Critical)

Define `#[tauri::command]` functions in ONE place only — `lib.rs`. Never split commands between `lib.rs` and `main.rs`.

**Pattern:**
```rust
// lib.rs — all commands here
#[tauri::command]
fn list_drives(engine: State<'_, RipEngine>) -> Result<Vec<DriveInfo>, String> { ... }

#[tauri::command]
fn get_job(job_id: String, engine: State<'_, RipEngine>) -> Result<Job, String> {
    let id = JobId(job_id);
    engine.job_manager().get_job(&id).ok_or_else(|| "Job not found".to_string())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .manage(RipEngine::new())
        .invoke_handler(tauri::generate_handler![list_drives, get_job, ...])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

// main.rs — just calls run()
fn main() {
    diskripper_tauri::run();
}
```

**Why:** Defining commands in both files causes `E0255: the name `__cmd__<name>` is defined multiple times` — Tauri's macro generates conflicting symbols.

## IPC Response Type Constraints

Tauri 2 requires command return types to implement `IpcResponse`. This FAILS:

```rust
// ERROR: Option<Job> does not implement IpcResponse
fn get_job(...) -> Result<Option<Job>, String> { ... }
```

Fix:
```rust
fn get_job(...) -> Result<Job, String> {
    engine.job_manager().get_job(&id).ok_or_else(|| "Job not found".to_string())
}
```

## Async Command Pattern

Using `async fn` directly in Tauri commands can cause `E0670: async fn is not permitted in Rust 2015` even with edition 2021 set. The robust pattern:

```rust
#[tauri::command]
fn start_image_rip(
    drive_id: String,
    output_path: String,
    engine: State<'_, RipEngine>,
) -> Result<String, String> {
    let opts = ImageOptions::default();
    let path = std::path::PathBuf::from(output_path);
    tauri::async_runtime::block_on(engine.start_image_rip(&drive_id, &path, opts))
        .map(|id| id.0)
        .map_err(|e| e.to_string())
}
```

## Dev Workflow (Critical for Tauri + React)

When using Tauri 2 with a React/Vite frontend in a separate directory, the `beforeDevCommand` must be handled carefully:

**Problem:** Tauri runs `beforeDevCommand` from the `src-tauri/` directory, not the frontend directory. Commands like `cd ../frontend && npm run dev` fail with "The system cannot find the path specified."

**Working pattern:**
1. Start the frontend dev server FIRST in a separate terminal:
   ```bash
   cd frontend && npm run dev
   ```
2. Then run Tauri dev with an EMPTY `beforeDevCommand`:
   ```json
   {
     "build": {
       "beforeDevCommand": "",
       "devUrl": "http://localhost:1420",
       "frontendDist": "../frontend/dist"
     }
   }
   ```
   ```bash
   cd src-tauri && cargo tauri dev
   ```

**Why:** An empty `beforeDevCommand` skips the npm step, relying on the already-running Vite dev server. The `devUrl` points to the correct localhost port.

**Alternative:** Use absolute paths in `beforeDevCommand` (fragile, not recommended):
```json
"beforeDevCommand": "cmd /c \"npm --prefix C:\\Projects\\MyApp\\frontend run dev\""
```

## tauri.conf.json Schema (v2.11.5)

Valid top-level bundle fields: `active`, `targets`, `icon`, `resources`, `copyright`, `category`, `shortDescription`, `longDescription`, `windows`, `linux`, `macos`, `ios`, `android`.

**NOT valid:**
- `deb` — must go under `linux: { "deb": { "depends": [] } }`
- `macOS` (capital M) — must be `macos`
- `createUpdaterArtifacts` — only valid with updater plugin
- `publisher`, `homepage` — not recognized in this schema version

**Minimal working config:**
```json
{
  "productName": "DiskRipper",
  "version": "0.1.0",
  "identifier": "com.diskripper.app",
  "build": {
    "beforeDevCommand": "",
    "devUrl": "http://localhost:1420",
    "frontendDist": "../frontend/dist"
  },
  "bundle": {
    "active": true,
    "targets": "all"
  },
  "app": {
    "windows": [{ "title": "DiskRipper", "width": 1200, "height": 800 }],
    "security": { "csp": null }
  }
}
```

**Packaging config (all targets):**
```json
{
  "bundle": {
    "active": true,
    "targets": "all",
    "copyright": "2026 Author",
    "category": "Utility",
    "shortDescription": "App description",
    "longDescription": "Longer description",
    "windows": {
      "certificateThumbprint": null,
      "digestAlgorithm": "sha256",
      "timestampUrl": ""
    },
    "linux": {
      "deb": {
        "depends": []
      }
    },
    "macos": {
      "frameworks": [],
      "minimumSystemVersion": "10.15",
      "exceptionDomain": "",
      "signingIdentity": "",
      "providerShortName": "",
      "entitlements": null
    }
  }
}
```

## Capabilities

Create `capabilities/default.json`:
```json
{
  "identifier": "default",
  "windows": ["main"],
  "permissions": ["core:default", "shell:allow-open", "dialog:default", "fs:default"]
}
```

## esbuild Postinstall (Windows)

`npm install` blocks esbuild's postinstall script on Windows. Fix:
```bash
npm install-scripts approve esbuild
npm install
```

## Edition Inheritance Fix

If a crate shows `E0670: async fn is not permitted in Rust 2015` despite workspace edition 2021:
1. Set `edition = "2021"` explicitly in the member crate's Cargo.toml (not `workspace = true`)
2. Run `cargo clean -p <crate>`
3. Re-check

This happens when workspace inheritance is ambiguous or the member crate's edition isn't resolved correctly.

## GUI Verification Workflow

When verifying a Tauri desktop app's UI:

1. Launch the dev server: `cd frontend && npm run dev`
2. Launch Tauri: `cd src-tauri && cargo tauri dev`
3. Use accessibility/semantic capture to enumerate elements
4. Click navigation elements by coordinates from accessibility bounds
5. Re-capture after each navigation to verify view switching
6. Verify empty states, error states, and action buttons render correctly
